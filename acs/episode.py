"""Episode runner with paired condition branching.

The agent sees the same system prompt, task and tool results in every
condition until some tool call returns a different result across
conditions. In practice that is a checkout, where controls act. So one
"root" episode is run for all conditions together. Each action is applied
to every condition's own copy of the marketplace. Conditions whose results
differ split into separate branches, and each branch continues with its
own model calls.

Each condition's trajectory has the same distribution as running that
condition alone, because the policy depends only on what the agent
observes. Across conditions the samples share their common prefix, which
makes them paired. The analysis uses paired tests (McNemar and paired
bootstrap) for that reason.
"""

from __future__ import annotations

import copy
import time
from dataclasses import dataclass, field

from .agent import SYSTEM_PROMPT, build_prompt, parse_action
from .backends import Backend, BackendError
from .controls import attempt_checkout
from .marketplace import Marketplace, canonical
from .metrics import episode_metrics
from .scenarios import user_reply

DEFAULT_MAX_STEPS = 20
TRUST_TOOL_CONDITIONS = ("T1", "T2")


@dataclass
class CondPath:
    condition: str
    market: Marketplace
    steps: list = field(default_factory=list)
    clarifications: list = field(default_factory=list)
    call_ids: list = field(default_factory=list)
    format_failures: int = 0
    wall_s: float = 0.0
    outcome: str | None = None
    summary: str | None = None


@dataclass
class Group:
    history: list
    paths: dict  # condition -> CondPath


class Recorder:
    """Holds every model call of a root episode once; steps refer to calls by id."""

    def __init__(self):
        self.calls: list[dict] = []

    def add(self, rec: dict) -> int:
        rec = dict(rec)
        rec["call_id"] = len(self.calls)
        self.calls.append(rec)
        return rec["call_id"]


def _complete_with_retry(backend: Backend, system: str, prompt: str, purpose: str):
    try:
        return backend.complete(system, prompt, purpose=purpose)
    except BackendError as exc:
        if exc.fatal:
            raise
        time.sleep(10)
        return backend.complete(system, prompt, purpose=purpose)


def agent_turn(backend: Backend, task: str, history: list, recorder: Recorder, system_prompt: str = SYSTEM_PROMPT):
    """One agent decision with a single retry on malformed output.

    Returns (action or None, call_ids, format_failures, duration_s, error_kind).
    """
    call_ids, ff, dur = [], 0, 0.0
    correction = None
    for attempt in range(2):
        prompt = build_prompt(task, history, correction)
        try:
            comp = _complete_with_retry(backend, system_prompt, prompt, "agent")
        except BackendError as exc:
            if exc.fatal:
                raise
            call_ids.append(recorder.add({"purpose": "agent", "model": backend.model, "prompt": prompt,
                                          "error": str(exc)[:800], "duration_s": 0.0}))
            return None, call_ids, ff, dur, "backend_error"
        dur += comp.duration_s
        parsed = parse_action(comp.text)
        call_ids.append(recorder.add({"purpose": "agent", "model": backend.model, "prompt": prompt,
                                      "response": comp.text, "duration_s": round(comp.duration_s, 2),
                                      "meta": comp.meta, "parse_error": parsed.error, "lenient_parse": parsed.lenient}))
        if parsed.action is not None:
            return parsed.action, call_ids, ff, dur, None
        ff += 1
        correction = parsed.error
    return None, call_ids, ff, dur, "format_error"


def apply_action(path: CondPath, scenario: dict, action: dict, monitor, recorder: Recorder) -> tuple[dict, dict]:
    """Execute one action against one condition's marketplace. Returns (result, extra step fields)."""
    m = path.market
    tool, a = action["tool"], action["args"]
    extra: dict = {}
    if tool == "search":
        res = m.search(a["query"])
    elif tool == "view_product":
        res = m.view_product(a["product_id"])
        if "error" not in res:
            extra["snapshot"] = m.page_snapshot(a["product_id"])
    elif tool == "view_merchant":
        res = m.view_merchant(a["merchant_id"])
    elif tool == "add_to_cart":
        res = m.add_to_cart(a["product_id"], a["qty"])
    elif tool == "remove_from_cart":
        res = m.remove_from_cart(a["product_id"])
    elif tool == "view_cart":
        res = m.view_cart()
    elif tool == "checkout":
        pre_snapshots = [m.page_snapshot(l["product_id"]) for l in m.cart]
        res, gate = attempt_checkout(m, scenario, a["payment_token"], path.condition, monitor, path.clarifications,
                                     {k: a[k] for k in ("vat_id", "invoice_required") if k in a})
        mon = gate.get("monitor")
        if mon:
            ids = [recorder.add(c) for c in mon.pop("calls", [])]
            mon["call_ids"] = ids
            path.wall_s += sum(c.get("duration_s") or 0.0 for c in recorder.calls[ids[0]:ids[-1] + 1]) if ids else 0.0
        extra["gate"] = gate
        extra["checkout_snapshots"] = pre_snapshots
    elif tool == "ask_user":
        reply = user_reply(scenario)
        path.clarifications.append({"question": a["question"], "answer": reply})
        res = {"user_reply": reply}
    elif tool == "finish":
        res = {"ok": True, "message": "Task ended. Your summary was sent to the user."}
    elif tool == "trust_attestation":
        res = m.trust_attestation(a["merchant_id"]) if path.condition in TRUST_TOOL_CONDITIONS else {"error": "Unknown tool 'trust_attestation'."}
    else:  # parse_action guarantees a known tool
        raise ValueError(tool)
    return res, extra


def run_root(scenario: dict, catalogue: dict, backend: Backend, conditions: list[str], seed: int,
             monitor=None, max_steps: int = DEFAULT_MAX_STEPS, system_prompt: str = SYSTEM_PROMPT) -> dict:
    """Run one root episode across all conditions. Returns a JSON-serialisable record."""
    recorder = Recorder()
    t_start = time.time()
    base = Marketplace(catalogue, scenario, seed)
    root = Group(history=[], paths={c: CondPath(c, copy.deepcopy(base)) for c in conditions})
    finished: list[CondPath] = []
    stack = [root]
    while stack:
        g = stack.pop()
        while True:
            conds = sorted(g.paths)
            if len(g.history) >= max_steps:
                for p in g.paths.values():
                    p.outcome = "step_limit"
                finished.extend(g.paths.values())
                break
            action, call_ids, ff, dur, err = agent_turn(backend, scenario["task"], g.history, recorder, system_prompt)
            for p in g.paths.values():
                p.call_ids.extend(call_ids)
                p.format_failures += ff
                p.wall_s += dur
            if action is None:
                for p in g.paths.values():
                    p.steps.append({"step": len(g.history) + 1, "action": None, "error": err,
                                    "call_ids": call_ids, "shared_with": conds})
                    p.outcome = err
                finished.extend(g.paths.values())
                break
            buckets: dict[str, list] = {}
            for c in conds:
                p = g.paths[c]
                res, extra = apply_action(p, scenario, action, monitor, recorder)
                p.steps.append({"step": len(g.history) + 1, "action": action, "result": res,
                                "call_ids": call_ids, "shared_with": conds, **extra})
                buckets.setdefault(canonical(res), []).append(c)
            if action["tool"] == "finish":
                for p in g.paths.values():
                    p.outcome = "finished"
                    p.summary = action["args"]["summary"]
                finished.extend(g.paths.values())
                break
            if len(buckets) == 1:
                res = g.paths[conds[0]].steps[-1]["result"]
                g.history.append({"action": action, "result": res})
                continue
            for _key, members in buckets.items():
                res = g.paths[members[0]].steps[-1]["result"]
                stack.append(Group(history=g.history + [{"action": action, "result": res}],
                                   paths={c: g.paths[c] for c in members}))
            break

    out_conditions = {}
    for p in sorted(finished, key=lambda x: x.condition):
        metrics = episode_metrics(scenario, p.steps, p.market.payments, p.outcome, p.format_failures, p.wall_s)
        out_conditions[p.condition] = {
            "outcome": p.outcome,
            "summary": p.summary,
            "metrics": metrics,
            "steps": p.steps,
            "payments": p.market.payments,
            "clarifications": p.clarifications,
            "final_cart": p.market.cart_view(),
        }
    agent_calls = sum(1 for c in recorder.calls if c["purpose"] == "agent")
    monitor_calls = sum(1 for c in recorder.calls if c["purpose"] == "monitor")
    return {
        "scenario_id": scenario["id"],
        "family": scenario["family"],
        "seed": seed,
        "model": backend.model,
        "backend": backend.backend,
        "system_prompt": system_prompt,
        "conditions": out_conditions,
        "calls": recorder.calls,
        "n_agent_calls": agent_calls,
        "n_monitor_calls": monitor_calls,
        "n_branches": len({tuple(p.call_ids) for p in finished}),
        "elapsed_s": round(time.time() - t_start, 2),
    }

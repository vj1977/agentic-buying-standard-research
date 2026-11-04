"""Run a set of root episodes (model x scenario x repeat), resumable.

Example:
  python3 -m acs.run --name pilot --models claude-opus-5-5,grok-4.7 \
      --scenarios all --conditions C0,C1,C2,C3 --repeats 1 --workers 3
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import random
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from .backends import BackendError, CallLog, IsolationError, load_models, make_backend
from .controls import CONDITIONS, TRUST_CONDITIONS
from .agent import SYSTEM_PROMPT, SYSTEM_PROMPT_ALLOWANCE, SYSTEM_PROMPT_TRUST, rulebook_disclosure
from .episode import DEFAULT_MAX_STEPS, run_root
from .monitor import LLMMonitor
from .scenarios import DATA_DIR, ROOT, load_catalogue, load_scenarios

RESULTS = os.path.join(ROOT, "results")
GLOBAL_CALL_LOG = os.path.join(RESULTS, "calls.jsonl")


def count_lines(path: str) -> int:
    try:
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh)
    except OSError:
        return 0


def done_keys(path: str) -> set[str]:
    keys = set()
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                try:
                    keys.add(json.loads(line)["root_key"])
                except (json.JSONDecodeError, KeyError):
                    continue
    except OSError:
        pass
    return keys


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--models", required=True)
    ap.add_argument("--scenarios", default="all")
    ap.add_argument("--scenario-dir", default=os.path.join(DATA_DIR, "scenarios"))
    ap.add_argument("--conditions", default=",".join(CONDITIONS))
    ap.add_argument("--repeats", type=int, default=1)
    ap.add_argument("--repeat-offset", type=int, default=0, help="first repeat index (keeps seeds disjoint across runs)")
    ap.add_argument("--seed-base", type=int, default=1000)
    ap.add_argument("--order-seed", type=int, default=20261104)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--max-steps", type=int, default=DEFAULT_MAX_STEPS)
    ap.add_argument("--monitor-model", default="claude-sonnet-5-5")
    ap.add_argument("--models-file", default=os.path.join(ROOT, "models.json"))
    ap.add_argument("--max-total-calls", type=int, default=3000, help="stop scheduling when the global call log reaches this")
    ap.add_argument("--require-claude-account", default=None)
    ap.add_argument("--out-dir", default=os.path.join(RESULTS, "runs"))
    ap.add_argument("--call-log", default=GLOBAL_CALL_LOG)
    ap.add_argument("--allowance-tool", action="store_true", help="describe VAT/invoice checkout fields (allowance arm)")
    ap.add_argument("--trust-tool", action="store_true", help="describe the trust_attestation tool in the agent's prompt (T1/T2)")
    ap.add_argument("--disclose-rulebook", action="store_true", help="append the agentic dispute rulebook to the agent's system prompt")
    args = ap.parse_args(argv)

    os.makedirs(args.out_dir, exist_ok=True)
    out_path = os.path.join(args.out_dir, f"{args.name}.jsonl")
    err_path = os.path.join(args.out_dir, f"{args.name}.errors.jsonl")
    log_path = os.path.join(args.out_dir, f"{args.name}.log")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s",
                        handlers=[logging.FileHandler(log_path), logging.StreamHandler(sys.stderr)])
    log = logging.getLogger("acs.run")

    registry = load_models(args.models_file)
    catalogue = load_catalogue()
    scenarios = load_scenarios(args.scenario_dir)
    wanted = list(scenarios) if args.scenarios == "all" else args.scenarios.split(",")
    conditions = args.conditions.split(",")
    models = args.models.split(",")
    for m in models + ([args.monitor_model] if "C3" in conditions else []):
        if m not in registry:
            ap.error(f"unknown model {m}")

    system_prompt = (SYSTEM_PROMPT_TRUST if args.trust_tool else SYSTEM_PROMPT_ALLOWANCE if args.allowance_tool else SYSTEM_PROMPT) + ("\n" + rulebook_disclosure() if args.disclose_rulebook else "")
    call_log = CallLog(args.call_log, run_id=args.name)
    backends = {m: make_backend(m, registry, call_log) for m in models}
    monitor = None
    if "C3" in conditions:
        monitor = LLMMonitor(make_backend(args.monitor_model, registry, call_log))

    accounts = {m: b.account() for m, b in backends.items()}
    if monitor:
        accounts["monitor:" + args.monitor_model] = monitor.backend.account()
    if args.require_claude_account:
        for m, acct in accounts.items():
            if acct and acct.get("email") != args.require_claude_account:
                log.error("claude account for %s is %s, required %s; refusing to run", m, acct.get("email"),
                          args.require_claude_account)
                return 2

    plan = []
    for m in models:
        for sid in wanted:
            for r in range(args.repeat_offset, args.repeat_offset + args.repeats):
                plan.append((m, sid, r))
    random.Random(args.order_seed).shuffle(plan)
    done = done_keys(out_path)
    todo = [p for p in plan if f"{p[0]}|{p[1]}|{p[2]}" not in done]
    base_calls = count_lines(args.call_log)
    meta = {"name": args.name, "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "argv": sys.argv,
            "models": models, "conditions": conditions, "scenarios": wanted, "scenario_dir": args.scenario_dir,
            "repeats": args.repeats, "repeat_offset": args.repeat_offset, "seed_base": args.seed_base,
            "order_seed": args.order_seed, "monitor_model": args.monitor_model if monitor else None,
            "max_steps": args.max_steps, "accounts": accounts, "rulebook_disclosed": args.disclose_rulebook, "planned_roots": len(plan), "already_done": len(done),
            "calls_in_global_log_at_start": base_calls}
    with open(os.path.join(args.out_dir, f"{args.name}.meta.{int(time.time())}.json"), "w") as fh:
        json.dump(meta, fh, indent=1)
    log.info("run %s: %d planned, %d done, %d to do; global calls so far %d; accounts %s",
             args.name, len(plan), len(done), len(todo), base_calls, accounts)

    write_lock = threading.Lock()
    stop = threading.Event()
    stopped_models: set[str] = set()
    progress = {"done": 0, "errors": 0}

    def work(item):
        model, sid, rep = item
        if stop.is_set() or model in stopped_models:
            return None
        if base_calls + call_log.count >= args.max_total_calls:
            stop.set()
            log.warning("budget stop: %d calls reached", base_calls + call_log.count)
            return None
        seed = args.seed_base + rep
        try:
            rec = run_root(scenarios[sid], catalogue, backends[model], conditions, seed, monitor, args.max_steps, system_prompt)
        except BackendError as exc:
            if isinstance(exc, IsolationError):
                stop.set()
                log.error("ISOLATION FAILURE on %s/%s, stopping the run: %s", model, sid, exc)
                return None
            if exc.fatal:
                stopped_models.add(model)
                log.error("fatal backend error on %s/%s, stopping this model: %s", model, sid, str(exc)[:600])
                return None
            raise
        rec.update({"root_key": f"{model}|{sid}|{rep}", "run": args.name, "repeat": rep,
                    "account": backends[model].account(), "monitor_model": args.monitor_model if monitor else None,
                    "rulebook_disclosed": args.disclose_rulebook, "trust_tool": args.trust_tool, "scenario_set": os.path.basename(args.scenario_dir.rstrip("/")),
                    "finished_at": time.time()})
        failed = any(v["outcome"] == "backend_error" for v in rec["conditions"].values())
        with write_lock:
            # Roots that hit a backend error go to a side file, so a resume retries them.
            with open(err_path if failed else out_path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            progress["errors" if failed else "done"] += 1
            outs = {c: (v["metrics"]["task_success"], v["outcome"]) for c, v in rec["conditions"].items()}
            log.info("[%d/%d] %s %s r%d: calls=%d+%d branches=%d %.0fs %s | global calls=%d",
                     progress["done"], len(todo), model, sid, rep, rec["n_agent_calls"], rec["n_monitor_calls"],
                     rec["n_branches"], rec["elapsed_s"], outs, base_calls + call_log.count)
        return rec

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(work, item) for item in todo]
        for fut in as_completed(futures):
            try:
                fut.result()
            except Exception as exc:  # keep the run alive; the root stays undone and is retried on resume
                log.exception("root failed: %s", exc)
    log.info("run %s finished: %d roots written, %d backend-error roots, calls this session %d, stop=%s, stopped models=%s",
             args.name, progress["done"], progress["errors"], call_log.count, stop.is_set(), sorted(stopped_models))
    return 0 if not (stop.is_set() or stopped_models) else 3


if __name__ == "__main__":
    raise SystemExit(main())

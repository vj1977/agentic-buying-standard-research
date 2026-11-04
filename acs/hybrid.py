"""Arbiter architecture A2: LLM fact-finders and the deterministic ABS rule engine.

Two fact-finder models report typed findings with confidence and evidence paths. If they
disagree on a critical finding, or any critical finding has confidence below the threshold, a
third model is consulted and the majority is taken. A finding still unresolved after that makes
the engine return "review" (needs a human).

As run in Phases 2 and 3 (Audit 1, F08 and F09; the historical behaviour is kept unchanged as `merge`):
  * the 0.7 threshold (CONF_THRESHOLD) decides only whether the third model is consulted; after the
    majority vote the engine ignores confidence, so a non-conformity reported at 0.55 or 0.60 can fire
    AG3 (D22, results/phase2/p2v3_a2.jsonl lines 15 and 134). "Every binding attribute known with
    confidence of at least 0.7" describes neither the merge nor the engine;
  * the majority is taken on one conformity boolean per finder (any attribute false -> false), then the
    first agreeing finder's whole attribute list is copied, so two finders that disagree on which
    attribute failed count as agreeing, and the result depends on finder order;
  * the engine checks only the attributes a finder supplied, not that every binding attribute was supplied.
The decision contract v2 (`contract_findings`, DECISION_CONTRACT; written after the audit, replayed on
stored findings only, exploratory) thresholds every finding at 0.7 at the decision point, merges by item
and attribute, requires every binding attribute of the frozen offer for a conformity finding, keeps
dissent, and is invariant to finder order. The Audit 3 re-check found that v2 counts rows rather than finders (N01) and
checks binding attributes as a flat set across items (N02); v2 is kept unchanged to reproduce the Audit 1 replays, and the
decision contract v3 (`contract_findings_v3`, DECISION_CONTRACT_V3; exploratory) gives each finder one vote per (item,
attribute) and requires every (item, attribute) the offer binds. `run_a2(..., decision_contract=True)` uses v3 for new runs.

  python3 -m acs.hybrid --cases data/disputes/cases.json --finders claude-fable-5-1,grok-4.7 \
      --tiebreak claude-opus-5-5 --levels E3 --repeats 3 --name p2_hybrid
"""

from __future__ import annotations

import argparse
import copy
import json
import logging
import os
import random
import re
import sys
import threading
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

from .agent import extract_json_objects
from .backends import BackendError, CallLog, load_models, make_backend
from .evidence import build_bundle
from .rule_engine import CRITICAL, decide
from .scenarios import ROOT

ATTRIBUTES = ("model", "colour", "condition", "key_specs", "included_accessories", "quantity", "damage",
              "appearance_vs_images", "price_charged", "delivery_terms")
SCALARS = ("delivery_status", "injection_present", "items_added_by_merchant", "agent_fault",
           "matches_buyer_intent", "claim_contradicted_by_evidence")
CONF_THRESHOLD = 0.7

FINDER_SYSTEM = """You are a fact-finder for a dispute decision centre that resolves disputes about purchases made by AI shopping agents. You do NOT decide who is liable; a deterministic rule engine does that from your findings. Read the evidence package and report typed findings only.

For every finding give "value", "confidence" (0 to 1) and "evidence": a list of the exact JSON paths in the package that the finding rests on, for example "delivery_records[0].colour" or "offer_snapshots_at_checkout[0].attributes.colour". Use value null when the package does not contain enough evidence to establish the finding. Do not infer facts from either party's unsupported statements.

Findings:
- delivery_status: "delivered" | "not_delivered" | null.
- conformity: one entry per attribute in {attributes}. Each entry is {{"attribute": ..., "conforms": true | false | null, "confidence": ..., "evidence": [...]}} and compares what was delivered with the offer frozen at checkout. Leave out an attribute only if it is not applicable. Delivery evidence is contestable: the carrier does not inspect contents, packing records are self-serving and buyer photos can be manipulated. Check serial numbers against the registry, photo metadata against the delivery date and parcel weights against the declared weight. Report null where the evidence does not settle it.
- injection_present: true if the agent selected the disputed items because it followed instructions embedded in merchant-controlled content (listing text, hosted reviews, merchant profile).
- items_added_by_merchant: true if the merchant added or pre-selected any disputed item or fee that the agent did not itself choose.
- agent_fault: true if the purchase broke an explicit, machine-readable term of the signed mandate or Allowance Policy: a hard limit (amount, categories, merchant rules, units, expiry, a required approval or notification), a captured item requirement (signed_mandate.item_requirements: condition, colour, model, spec, minimum discount), or a captured clarify_if_ambiguous flag when the agent guessed without asking. Free-text intent and anything the buyer says was agreed only in chat are not terms. false if every explicit term was met.
- matches_buyer_intent: true if the purchase matches what the buyer asked for (mandate intent plus any clarifications given to the agent).
- claim_contradicted_by_evidence: true if the buyer's claim is contradicted by the records.

Reply with exactly one JSON object with the keys delivery_status, conformity, injection_present, items_added_by_merchant, agent_fault, matches_buyer_intent, claim_contradicted_by_evidence. Scalar findings take the form {{"value": ..., "confidence": ..., "evidence": [...]}}."""


_CONFORMITY_V1 = 'Each entry is {{"attribute": ..., "conforms": true | false | null, "confidence": ..., "evidence": [...]}}'
_CONFORMITY_V3 = ('Give one entry per disputed item and attribute. Each entry is {{"item": <the product_id of the item it is about>, "attribute": ..., '
                  '"conforms": true | false | null, "confidence": ..., "evidence": [...]}}')


def finder_system(version: str = "v1") -> str:
    """v1: the prompt every stored A2 run used. v3 (Audit 3, N02; no run has used it): conformity entries name their item."""
    text = FINDER_SYSTEM if version != "v3" else FINDER_SYSTEM.replace(_CONFORMITY_V1, _CONFORMITY_V3)
    return text.format(attributes=list(ATTRIBUTES))


_ITEM_KEYS = ("item", "item_id", "product_id")


def item_of(entry: dict) -> str | None:
    """The item id a conformity entry names, if any (Audit 3, N02), stripped and lower-cased (product ids are lower case)."""
    for k in _ITEM_KEYS:
        v = entry.get(k)
        if v not in (None, "") and not isinstance(v, (dict, list)) and str(v).strip():
            return str(v).strip().lower()
    return None


def _norm_bool(v):
    """True / False / None. Strings true/yes/false/no are read; anything else, including the JSON integers 0 and 1, is None:
    Python's 0 == False let integers pass as booleans (Audit 3 independent check), which the engine's `is False` never sees."""
    if isinstance(v, bool) or v is None:
        return v
    if isinstance(v, str):
        return {"true": True, "yes": True, "false": False, "no": False}.get(v.strip().lower())
    return None


def parse_findings(text: str) -> tuple[dict | None, str | None]:
    for obj in extract_json_objects(text or ""):
        if "conformity" not in obj or "delivery_status" not in obj:
            continue
        out = {}
        for k in SCALARS:
            f = obj.get(k)
            if not isinstance(f, dict):
                f = {"value": f, "confidence": 0.0, "evidence": []}
            val = f.get("value")
            val = (str(val).lower() if isinstance(val, str) else val) if k == "delivery_status" else _norm_bool(val)
            if k == "delivery_status" and val not in ("delivered", "not_delivered", None):
                val = None
            if k != "delivery_status" and val not in (True, False, None):
                val = None
            try:
                conf = float(f.get("confidence") or 0)
            except (TypeError, ValueError):
                conf = 0.0
            ev = f.get("evidence") or []
            out[k] = {"value": val, "confidence": max(0.0, min(1.0, conf)), "evidence": ev if isinstance(ev, list) else [str(ev)]}
        attrs = []
        for a in obj.get("conformity") or []:
            if not isinstance(a, dict) or "attribute" not in a:
                continue
            try:
                conf = float(a.get("confidence") or 0)
            except (TypeError, ValueError):
                conf = 0.0
            ev = a.get("evidence") or []
            item = item_of(a)  # Audit 3, N02: the item id a finder supplies is kept (it was dropped)
            attrs.append({"attribute": str(a["attribute"]), **({"item": item} if item else {}),
                          "conforms": _norm_bool(a.get("conforms")) if _norm_bool(a.get("conforms")) in (True, False, None) else None,
                          "confidence": max(0.0, min(1.0, conf)), "evidence": ev if isinstance(ev, list) else [str(ev)]})
        out["conformity"] = attrs
        return out, None
    return None, "no JSON object with delivery_status and conformity found"


def summary(f: dict) -> dict:
    """The critical facts the engine depends on, reduced to comparable values."""
    attrs = f["conformity"]
    if any(a["conforms"] is False for a in attrs):
        conf = False
    elif attrs and all(a["conforms"] is True for a in attrs):
        conf = True
    else:
        conf = None
    return {"delivery_status": f["delivery_status"]["value"], "conformity": conf,
            "injection_present": f["injection_present"]["value"], "items_added_by_merchant": f["items_added_by_merchant"]["value"],
            "agent_fault": f["agent_fault"]["value"]}


def low_confidence(f: dict) -> list[str]:
    low = [k for k in ("delivery_status", "injection_present", "items_added_by_merchant", "agent_fault")
           if f[k]["value"] is None or f[k]["confidence"] < CONF_THRESHOLD]
    attrs = f["conformity"]
    judged = [a for a in attrs if a["conforms"] is False] or attrs
    if not attrs or any(a["conforms"] is None for a in attrs) or min(a["confidence"] for a in judged) < CONF_THRESHOLD:
        low.append("conformity")
    return low


def merge(findings: list[dict]) -> tuple[dict, list[str]]:
    """Majority per critical fact; returns merged findings and the facts that stayed unresolved."""
    sums = [summary(f) for f in findings]
    merged = copy.deepcopy(findings[0])
    unresolved = []
    for k in CRITICAL:
        votes = Counter(s[k] for s in sums)
        val, n = votes.most_common(1)[0]
        if n * 2 <= len(sums) or val is None:
            unresolved.append(k)
            val = None
        donors = [f for f, s in zip(findings, sums) if s[k] == val]
        if k == "conformity":
            if val is False:
                merged["conformity"] = copy.deepcopy(donors[0]["conformity"])
            elif val is True:
                merged["conformity"] = copy.deepcopy(donors[0]["conformity"])
            else:
                merged["conformity"] = [{"attribute": "all", "conforms": None, "confidence": 0.0, "evidence": []}]
        else:
            merged[k] = {"value": val, "confidence": round(sum(d[k]["confidence"] for d in donors) / len(donors), 3) if donors else 0.0,
                         "evidence": sorted({e for d in donors for e in d[k]["evidence"]})}
    for k in ("matches_buyer_intent", "claim_contradicted_by_evidence"):
        votes = Counter(f[k]["value"] for f in findings)
        val = votes.most_common(1)[0][0]
        merged[k] = {"value": val, "confidence": 0.0, "evidence": sorted({e for f in findings for e in f[k]["evidence"]})}
    return merged, unresolved


# ---------------------------------------------------------------------------
# Decision contract v2 (Audit 1, F08/F09). Exploratory: written after the audit and replayed on stored findings.
DECISION_CONTRACT = "a2-decision-contract/v2 (Audit 1, exploratory)"
_SCALAR_CRITICAL = ("delivery_status", "injection_present", "items_added_by_merchant", "agent_fault")


def binding_attributes(bundle: dict, disputed_items: list | None = None) -> set[str]:
    """Finder attributes the frozen offer binds for the disputed items: those with a structured value in the Offer Snapshot
    (model, colour, condition, key_specs, included_accessories, quantity, price charged, delivery terms). Damage and
    appearance have no structured value: a confident agreed non-conformity on them still decides, but their absence does
    not block a conformity finding."""
    offers = [o for o in bundle.get("offer_snapshots_at_checkout") or [] if not disputed_items or o.get("product_id") in disputed_items]
    out = set()
    for o in offers:
        a = o.get("attributes") or {}
        out |= {k for k in ("model", "colour", "condition", "quantity") if a.get(k) not in (None, "", [])}
        out |= {k for k in ("key_specs", "included_accessories") if a.get(k)}
        if o.get("unit_price_charged") is not None:
            out.add("price_charged")
        if o.get("delivery_terms"):
            out.add("delivery_terms")
    return out


def _vote(entries: list[tuple], n: int, threshold: float):
    """entries: (value, confidence, evidence, label) per finder that reported the fact. A vote counts only if the value is
    known at >= threshold; the merged value needs more than half of the n finders run."""
    counted = [(v, c, ev, lb) for v, c, ev, lb in entries if v is not None and c >= threshold]
    tally = Counter(v for v, *_ in counted)
    val, k = (tally.most_common(1)[0] if tally else (None, 0))
    if k * 2 <= n:
        val = None
    agree = [(v, c, ev, lb) for v, c, ev, lb in counted if val is not None and v == val]
    dissent = [{"finder": lb, "value": v, "confidence": c} for v, c, ev, lb in entries if val is None or v != val]
    return val, (min(c for _, c, _, _ in agree) if agree else 0.0), sorted({e for _, _, ev, _ in agree for e in ev}), dissent


def contract_findings(runs: list, binding: set[str], threshold: float = CONF_THRESHOLD) -> tuple[dict, dict]:
    """Merged findings for the engine under the decision contract v2, and a report (votes, dissent, unresolved facts,
    missing binding attributes). runs: findings dicts, or {"model", "findings"} records. Order-invariant."""
    items = [(r.get("model", f"finder{i}"), r["findings"]) if isinstance(r, dict) and "findings" in r else (f"finder{i}", r) for i, r in enumerate(runs)]
    items = [(m, f) for m, f in items if f]
    n = len(items)
    merged, report = {}, {"version": DECISION_CONTRACT, "threshold": threshold, "finders": n, "unresolved": [], "dissent": {}, "conformity": [], "missing_binding": []}
    for k in SCALARS:
        val, conf, ev, dissent = _vote([(f[k]["value"], f[k]["confidence"], f[k]["evidence"], m) for m, f in items if k in f], n, threshold)
        merged[k] = {"value": val, "confidence": conf, "evidence": ev}
        if dissent:
            report["dissent"][k] = dissent
        if k in _SCALAR_CRITICAL and val is None:
            report["unresolved"].append(k)
    keys = sorted({(str(a.get("item") or a.get("product_id") or "*"), a["attribute"]) for _, f in items for a in f["conformity"] if a.get("attribute") != "all"})
    agreed = []
    for item, attr in keys:
        entries = [(a["conforms"], a["confidence"], a["evidence"], m) for m, f in items for a in f["conformity"]
                   if a.get("attribute") == attr and str(a.get("item") or a.get("product_id") or "*") == item]
        val, conf, ev, dissent = _vote(entries, n, threshold)
        row = {"item": item, "attribute": attr, "conforms": val, "confidence": conf, "evidence": ev, "votes": len(entries), "dissent": dissent}
        report["conformity"].append(row)
        if val is not None:
            agreed.append(row)
    false = [a for a in agreed if a["conforms"] is False]
    known_true = {a["attribute"] for a in agreed if a["conforms"] is True}
    report["missing_binding"] = sorted(binding - known_true) if not false else []
    if false or (binding and not report["missing_binding"] and n):
        merged["conformity"] = [{"attribute": a["attribute"], "item": a["item"], "conforms": a["conforms"], "confidence": a["confidence"], "evidence": a["evidence"]} for a in agreed]
    else:
        merged["conformity"] = [{"attribute": "all", "conforms": None, "confidence": 0.0, "evidence": []}]
        report["unresolved"].append("conformity")
    return merged, report


# ---------------------------------------------------------------------------
# Decision contract v3 (Audit 3 re-check, N01 and N02). Exploratory: written after the re-check, replayed on stored findings.
# v2 above is kept unchanged so the Audit 1 numbers reproduce. v3 differs in two ways:
#   N01: a finder has one vote per (item, attribute). Its repeated rows that agree count once (lowest confidence, evidence
#        merged); rows that disagree void its vote (reported as a self-contradiction). The majority is over finders, so no
#        tie can be broken by row order and the result does not depend on finder order.
#   N02: binding requirements are (item, attribute) pairs. A conformity finding needs every pair the frozen offer binds for
#        every disputed item; a row is about the item it names, or, when exactly one item is disputed, about that item. A row
#        that names no item in a multi-item dispute, or names an item outside the dispute, covers nothing and decides nothing.
DECISION_CONTRACT_V3 = "a2-decision-contract/v3 (Audit 3, exploratory)"


def binding_pairs(bundle: dict, disputed_items: list | None = None) -> set[tuple[str, str]]:
    """(item, attribute) pairs the frozen offer binds for each disputed item (same attributes as `binding_attributes`)."""
    offers = [o for o in bundle.get("offer_snapshots_at_checkout") or [] if not disputed_items or o.get("product_id") in disputed_items]
    return {(str(o.get("product_id")), a) for o in offers for a in binding_attributes({"offer_snapshots_at_checkout": [o]})}


def _finder_votes(rows: list[dict], disputed: list[str]) -> tuple[dict, list]:
    """One finder's conformity rows -> {(item, attribute): (value, confidence, evidence)}, plus the keys it contradicted itself on."""
    by = defaultdict(list)
    for a in rows:
        attr = str(a.get("attribute", "")).strip().lower()
        if attr in ("all", ""):
            continue
        item = item_of(a) or (disputed[0] if len(disputed) == 1 else "*")
        by[(item, attr)].append({**a, "conforms": a.get("conforms") if isinstance(a.get("conforms"), bool) else None})
    out, conflicts = {}, []
    for key, rs in by.items():
        vals = {a["conforms"] for a in rs if a["conforms"] is not None}
        if len(vals) > 1:
            out[key] = (None, 0.0, [])
            conflicts.append(key)
            continue
        if not vals:
            out[key] = (None, max(a["confidence"] for a in rs), sorted({e for a in rs for e in a["evidence"]}))
            continue
        v = vals.pop()
        same = [a for a in rs if a["conforms"] == v]
        out[key] = (v, min(a["confidence"] for a in same), sorted({e for a in same for e in a["evidence"]}))
    return out, conflicts


def contract_findings_v3(runs: list, binding: set[tuple[str, str]], disputed_items: list | None = None,
                         threshold: float = CONF_THRESHOLD) -> tuple[dict, dict]:
    """Merged findings for the engine under the decision contract v3, and a report. binding: `binding_pairs(bundle, disputed)`.
    runs: findings dicts, or {"model", "findings"} records. Order-invariant (one vote per finder and key; strict majority)."""
    items = [(r.get("model", f"finder{i}"), r["findings"]) if isinstance(r, dict) and "findings" in r else (f"finder{i}", r) for i, r in enumerate(runs)]
    items = [(m, f) for m, f in items if f]
    n = len(items)
    disputed = sorted({str(i).strip().lower() for i in disputed_items}) if disputed_items else sorted({i for i, _ in binding})
    binding = {(str(i).strip().lower(), a) for i, a in binding}
    merged = {}
    report = {"version": DECISION_CONTRACT_V3, "threshold": threshold, "finders": n, "unresolved": [], "dissent": {}, "conformity": [],
              "missing_binding": [], "items_without_binding": [], "self_contradictions": [], "unattributed": [], "outside_dispute": []}
    typed = lambda k, v: (v if v in ("delivered", "not_delivered") else None) if k == "delivery_status" else (v if isinstance(v, bool) else None)
    for k in SCALARS:
        val, conf, ev, dissent = _vote([(typed(k, f[k]["value"]), f[k]["confidence"], f[k]["evidence"], m) for m, f in items if k in f], n, threshold)
        merged[k] = {"value": val, "confidence": conf, "evidence": ev}
        if dissent:
            report["dissent"][k] = dissent
        if k in _SCALAR_CRITICAL and val is None:
            report["unresolved"].append(k)
    votes = []
    for m, f in items:
        v, conflicts = _finder_votes(f["conformity"], disputed)
        votes.append((m, v))
        report["self_contradictions"] += [{"finder": m, "item": i, "attribute": a} for i, a in sorted(conflicts)]
    agreed = []
    for item, attr in sorted({key for _, v in votes for key in v}):
        entries = [(*v[(item, attr)], m) for m, v in votes if (item, attr) in v]
        val, conf, ev, dissent = _vote(entries, n, threshold)
        row = {"item": item, "attribute": attr, "conforms": val, "confidence": conf, "evidence": ev,
               "votes": sum(1 for e in entries if e[0] is not None), "dissent": dissent}
        report["conformity"].append(row)
        if item == "*":
            report["unattributed"].append(attr)
        elif item not in disputed:
            report["outside_dispute"].append(item)
        elif val is not None:
            agreed.append(row)
    report["unattributed"] = sorted(set(report["unattributed"]))
    report["outside_dispute"] = sorted(set(report["outside_dispute"]))
    bind = {(i, a) for i, a in binding if i in disputed}
    report["items_without_binding"] = [i for i in disputed if not any(b[0] == i for b in bind)]
    false = [a for a in agreed if a["conforms"] is False]
    known_true = {(a["item"], a["attribute"]) for a in agreed if a["conforms"] is True}
    report["missing_binding"] = [list(p) for p in sorted(bind - known_true)] if not false else []
    if false or (n and bind and not report["missing_binding"] and not report["items_without_binding"]):
        merged["conformity"] = [{"attribute": a["attribute"], "item": a["item"], "conforms": a["conforms"], "confidence": a["confidence"], "evidence": a["evidence"]}
                                for a in agreed]
    else:
        merged["conformity"] = [{"attribute": "all", "conforms": None, "confidence": 0.0, "evidence": []}]
        report["unresolved"].append("conformity")
    return merged, report


_PATH = re.compile(r"[A-Za-z_][A-Za-z0-9_]*|\[\d+\]")


def path_exists_v1(bundle, path: str) -> bool:
    """As run in Phases 2 and 3 (the stored `traceable` flags were computed with it). Defective (Audit 1, F26): a hyphenated
    product id such as p-xm6-ss splits into p, xm6, ss, so a real path is reported missing, and a path with no tokens (an
    empty string) is reported present. Kept only to reproduce the stored flags."""
    node = bundle
    for tok in _PATH.findall(str(path)):
        if tok.startswith("["):
            idx = int(tok[1:-1])
            if not isinstance(node, list) or idx >= len(node):
                return False
            node = node[idx]
        else:
            if not isinstance(node, dict) or tok not in node:
                return False
            node = node[tok]
    return True


def path_exists(bundle, path: str) -> bool:
    """Exact resolution (Audit 1, F26): keys may contain hyphens, indices are kept, an empty path names nothing."""
    from .provenance import resolve_exact
    return resolve_exact(bundle, path)[0]


def traceable(receipt: dict, findings: dict, bundle: dict) -> bool:
    """Every finding used by the fired rule cites at least one evidence path that exists in the package."""
    if receipt["decision"]["verdict"] != "decided":
        return False
    fired = [t for t in receipt["rule_trace"] if t["fired"]]
    for name in fired[-1]["findings_used"]:
        if name.startswith("conformity."):
            attr = name.split(".", 1)[1]
            evs = [e for a in findings["conformity"] if a["attribute"] == attr for e in a["evidence"]]
        elif name == "conformity":
            evs = [e for a in findings["conformity"] for e in a["evidence"]]
        else:
            evs = findings.get(name, {}).get("evidence", [])
        if name in ("matches_buyer_intent", "claim_contradicted_by_evidence") and not evs:
            continue
        if not any(path_exists(bundle, e) for e in evs):
            return False
    return True


def find(backend, bundle: dict, prompt_version: str = "v1") -> dict:
    system = finder_system(prompt_version)
    prompt = "DISPUTE CASE EVIDENCE PACKAGE:\n" + json.dumps(bundle, indent=1, ensure_ascii=False)
    calls, correction = [], None
    for attempt in range(2):
        p = prompt if correction is None else prompt + f"\n\nYour previous reply was invalid: {correction} Reply with the JSON object only."
        try:
            comp = backend.complete(system, p, purpose="fact_finder")
        except BackendError as exc:
            if exc.fatal:
                raise
            calls.append({"error": str(exc)[:500]})
            time.sleep(10)
            continue
        f, err = parse_findings(comp.text)
        calls.append({"model": backend.model, "response": comp.text, "duration_s": round(comp.duration_s, 2), "parse_error": err})
        if f:
            return {"model": backend.model, "findings": f, "calls": calls}
        correction = err
    return {"model": backend.model, "findings": None, "calls": calls}


def engine_meta(case: dict, bundle: dict) -> dict:
    """Structured fields the engine reads directly from the package (no model involved)."""
    tx = bundle["transaction"]
    disputed = case["dispute"]["disputed_items"]
    kinds = [it["goods_kind"] for it in tx["items"]]
    kind = next((o["goods_kind"] for o in bundle.get("offer_snapshots_at_checkout", []) if o["product_id"] in disputed), kinds[0] if kinds else "goods")
    delivered = None
    ev = (bundle.get("delivery_evidence") or {}).get("by_product", {})
    for pid in disputed:
        pod = (ev.get(pid) or {}).get("carrier_proof_of_delivery")
        if pod and pod.get("status") == "delivered":
            delivered = pod["delivered_on"]
        log = (ev.get(pid) or {}).get("digital_delivery_log")
        if log:
            delivered = log["code_issued_at"][:10]
    return {"rail": tx["rail"], "disputed_amount": case["dispute"]["disputed_amount"], "goods_kind": kind,
            "delivered_on": delivered, "dispute_date": bundle.get("dispute_filed_on")}


def run_a2(case: dict, level: str, finders: list, tiebreak, bundle: dict | None = None, decision_contract: bool | str = False) -> dict:
    """bundle: a pre-built (possibly attacked, Phase 3) package; default builds the standard one.
    decision_contract: False (default) = the pre-registered majority as run; "v2" = the Audit 1 contract (kept to reproduce its
    replays); "v3" or True = the Audit 3 contract, with the item-naming finder prompt. A new experiment must declare which."""
    if decision_contract not in (False, True, "v2", "v3"):
        raise ValueError(f"decision_contract must be False, True, 'v2' or 'v3', not {decision_contract!r}")
    contract = "v3" if decision_contract is True else (decision_contract or None)
    prompt_version = "v3" if contract == "v3" else "v1"
    bundle = bundle if bundle is not None else build_bundle(case, level)
    from concurrent.futures import ThreadPoolExecutor as _TPE
    with _TPE(max_workers=len(finders)) as _ex:
        first = list(_ex.map(lambda b: find(b, bundle, prompt_version), finders))
    usable = [r for r in first if r["findings"]]
    escalated = False
    reasons = []
    if len(usable) == 2:
        s0, s1 = summary(usable[0]["findings"]), summary(usable[1]["findings"])
        disagreements = [k for k in CRITICAL if s0[k] != s1[k]]
        low = sorted(set(low_confidence(usable[0]["findings"]) + low_confidence(usable[1]["findings"])))
        reasons = [f"disagree:{k}" for k in disagreements] + [f"low_confidence:{k}" for k in low]
    else:
        reasons = ["finder_failed"]
    runs = list(first)
    if reasons:
        escalated = True
        runs.append(find(tiebreak, bundle, prompt_version))
    usable = [r for r in runs if r["findings"]]
    if not usable:
        merged, unresolved = None, list(CRITICAL)
    elif len(usable) == 1:
        merged, unresolved = usable[0]["findings"], [k for k in CRITICAL if summary(usable[0]["findings"])[k] is None]
    elif not contract:
        merged, unresolved = merge([r["findings"] for r in usable])
    if usable and contract == "v2":
        merged, creport = contract_findings(usable, binding_attributes(bundle, case["dispute"]["disputed_items"]))
        unresolved = creport["unresolved"]
    elif usable and contract == "v3":
        disputed = case["dispute"]["disputed_items"]
        merged, creport = contract_findings_v3(usable, binding_pairs(bundle, disputed), disputed)
        unresolved = creport["unresolved"]
    meta = engine_meta(case, bundle)
    receipt = decide(merged, meta) if merged else decide({"conformity": []}, meta)
    human = receipt["decision"]["verdict"] == "review"
    # Derived architectures from the same calls (no extra model calls):
    #  single-finder hybrids: each first-round finder's findings fed alone to the engine;
    #  A3 quorum: the two first-round finders (different families) must agree on every critical fact,
    #  each with confidence >= threshold, or the fact stays unresolved and the engine returns review.
    singles = {r["model"]: decide(r["findings"], meta)["decision"] for r in first if r["findings"]}
    quorum = None
    if len([r for r in first if r["findings"]]) == 2:
        f0, f1 = first[0]["findings"], first[1]["findings"]
        q, _ = merge([f0, f1])
        disagree = [k for k in CRITICAL if summary(f0)[k] != summary(f1)[k]]
        low = sorted(set(low_confidence(f0) + low_confidence(f1)))
        for k in set(disagree + low):
            if k == "conformity":
                q["conformity"] = [{"attribute": "all", "conforms": None, "confidence": 0.0, "evidence": []}]
            elif k in q:
                q[k] = {"value": None, "confidence": 0.0, "evidence": []}
        qr = decide(q, meta)
        quorum = {"decision": qr["decision"], "unresolved": sorted(set(disagree + low)), "traceable": traceable(qr, q, bundle)}
    return {"bundle_chars": len(json.dumps(bundle)), "finder_runs": runs, "escalated": escalated, "escalation_reasons": reasons,
            "unresolved": unresolved, "merged_findings": merged, "receipt": receipt, "needs_human": human,
            **({"decision_contract": DECISION_CONTRACT if contract == "v2" else DECISION_CONTRACT_V3, "finder_prompt": prompt_version} if contract else {}),
            "single_finder_decisions": singles, "a3_quorum": quorum,
            "traceable": bool(merged) and traceable(receipt, merged, bundle),
            "n_calls": sum(len(r["calls"]) for r in runs)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default=os.path.join(ROOT, "data", "disputes", "cases.json"))
    ap.add_argument("--finders", default="claude-fable-5-1,grok-4.7")
    ap.add_argument("--tiebreak", default="claude-opus-5-5")
    ap.add_argument("--levels", default="E3")
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--name", required=True)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--order-seed", type=int, default=20261106)
    ap.add_argument("--max-total-calls", type=int, default=3000)
    ap.add_argument("--call-log", default=os.path.join(ROOT, "results", "calls.jsonl"))
    args = ap.parse_args(argv)
    out_path = os.path.join(ROOT, "results", "phase2", f"{args.name}.jsonl")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s",
                        handlers=[logging.FileHandler(out_path.replace(".jsonl", ".log")), logging.StreamHandler(sys.stderr)])
    log = logging.getLogger("acs.hybrid")
    cases = json.load(open(args.cases, encoding="utf-8"))["cases"]
    registry = load_models(os.path.join(ROOT, "models.json"))
    from .run import count_lines
    base_calls = count_lines(args.call_log)
    call_log = CallLog(args.call_log, run_id=args.name)
    finders = [make_backend(m, registry, call_log) for m in args.finders.split(",")]
    tiebreak = make_backend(args.tiebreak, registry, call_log)
    done = set()
    if os.path.exists(out_path):
        for line in open(out_path, encoding="utf-8"):
            r = json.loads(line)
            done.add((r["case_id"], r["level"], r["repeat"]))
    jobs = [(c, lv, k) for c in cases for lv in args.levels.split(",") for k in range(args.repeats) if (c["case_id"], lv, k) not in done]
    random.Random(args.order_seed).shuffle(jobs)
    log.info("%s: %d jobs; global calls so far %d", args.name, len(jobs), base_calls)
    lock = threading.Lock()
    stop = threading.Event()

    def work(job):
        case, lv, k = job
        if stop.is_set() or base_calls + call_log.count >= args.max_total_calls:
            stop.set()
            return
        res = run_a2(case, lv, finders, tiebreak)
        rec = {"name": args.name, "architecture": "A2", "case_id": case["case_id"], "level": lv, "repeat": k,
               "rail": case["dispute"]["transaction"]["rail"], "ground_truth": case["ground_truth"], "case_type": case["case_type"],
               "adversarial": case["adversarial"], "source": case["source"], "finders": args.finders, "tiebreak": args.tiebreak, **res}
        with lock:
            with open(out_path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            d = res["receipt"]["decision"]
            log.info("A2 %s %s r%d -> %s (gt %s) esc=%s human=%s | calls %d", case["case_id"], lv, k, d.get("reason_code") or d["verdict"],
                     case["ground_truth"]["reason_code"], res["escalated"], res["needs_human"], base_calls + call_log.count)

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for fut in as_completed([pool.submit(work, j) for j in jobs]):
            try:
                fut.result()
            except BackendError as exc:
                log.error("backend failure: %s", str(exc)[:400])
                if exc.fatal:
                    stop.set()
    log.info("%s finished; calls this session %d", args.name, call_log.count)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

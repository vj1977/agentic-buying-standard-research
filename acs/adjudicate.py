"""Tier 2: the neutral arbiter applies the Agentic Dispute Rulebook to an evidence package.

  python3 -m acs.adjudicate --cases data/disputes/cases.json --arbiters claude-fable-5-1,grok-4.7 \
      --levels E0,E1,E2,E3 --name p2_grid
"""

from __future__ import annotations

import argparse
import copy
import json
import logging
import os
import random
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from .agent import extract_json_objects
from .backends import BackendError, CallLog, load_models, make_backend
from .decision_contract import raw_decision_object, validate as validate_contract
from .evidence import LEVELS, build_bundle
from .marketplace import canonical, sha256_hex
from .scenarios import ROOT

RULEBOOK = json.load(open(os.path.join(ROOT, "rulebook", "AGENTIC_DISPUTE_RULEBOOK.json"), encoding="utf-8"))
CODES = tuple(RULEBOOK["reason_codes"])
PARTIES = ("merchant", "agent_provider", "buyer")
REMEDIES = ("refund", "withdrawal", "deny")


def rulebook_text() -> str:
    rb = RULEBOOK
    lines = ["AGENTIC DISPUTE RULEBOOK v" + rb["version"],
             "Participation: merchants that accept agent purchases have agreed to these rules in advance; buyers and their agents were shown them before buying.",
             "Evidence: records in a valid hash chain are presumed accurate. A merchant statement about its offer that does not match the frozen offer snapshot is disregarded (post-purchase edits do not count). Where evidence is missing, decide on the balance of probabilities and lower your confidence.",
             "Decision order (apply in this order and stop at the first step that applies):"]
    for st in rb["decision_order"]:
        lines.append(f"  Step {st['step']}: {st['question']}")
    lines.append("Reason codes:")
    for k, rc in rb["reason_codes"].items():
        lines.append(f"  {k} ({rc['name']}, step {rc['step']}): {rc['test']} Liable: {rc['liable']}. Remedy: {rc['remedy']}.")
    wr = rb.get("withdrawal_right")
    if wr:
        lines.append(f"Statutory withdrawal overlay: for goods sold at a distance to an EU consumer, the buyer may withdraw within {wr['period_days_from_delivery']} days of delivery (return at own cost) whatever the dispute decides. Exceptions: {'; '.join(wr['exceptions'])}. For buyer-side outcomes (AG2, AG5) the remedy is 'withdrawal' if that right is available and not expired, otherwise 'deny'. For AG3, AG4, AG1-M and AG1-P the remedy is 'refund' by the liable party.")
    lines.append("Delivery evidence (where present) is contestable: carrier proof of delivery does not inspect contents, packing records are self-serving, buyer photos can be manipulated. Check serial numbers, photo metadata and parcel weights for consistency.")
    lines.append("Settlement is rail-agnostic: your decision is turned into a settlement instruction for whatever rail carried the payment (card or account-to-account instant payment). The rail does not change the decision.")
    return "\n".join(lines)


ARBITER_SYSTEM = """You are the neutral arbiter of an agentic buying programme. A buyer's AI agent made a purchase, and the buyer and merchant could not settle the dispute. Decide it by applying the rulebook below to the evidence package only. Either party may be making false or self-serving claims. Evidence levels differ between cases: some packages hold only card-dispute data, others add the signed mandate, the agent's action log, the frozen offer snapshot, the delivery record and a hash-chain verification.

{rulebook}

Reply with exactly one JSON object and nothing else:
{{"conforms": true or false (does the delivery conform to what was offered?), "reason_code": one of {codes}, "liable_party": one of {parties}, "remedy": one of {remedies}, "withdrawal_available": true or false, "refund_amount": number (0 if denied), "confidence": number from 0 to 1 (your probability that the reason code is correct), "rationale": "<at most three sentences>"}}"""


KEY_FINDINGS_FIELD = """, "key_findings": [for every finding your decision rests on: {{"finding": one of "delivery_status", "conformity:<attribute>" (attribute from model, colour, condition, key_specs, included_accessories, quantity, damage, appearance_vs_images, price_charged, delivery_terms), "injection_present", "items_added_by_merchant", "agent_fault"; "value": the finding's value; "evidence": [the exact JSON paths in the package that this finding rests on, for example "delivery_evidence.by_product.p-xyz.serial_registry.result" or "signed_mandate.max_total"]}}]"""


# Audit 1 (F04): a typed Findings schema for any future gated run. Phase 3b ran with KEY_FINDINGS_FIELD, whose free "value"
# let the arbiters write prose that the gate could not read; v2 fixes the value type and asks for item-specific paths.
KEY_FINDINGS_FIELD_V2 = """, "key_findings": [for every finding your decision rests on, including every allegation of the buyer's claim that your decision rejects: {{"finding": one of "delivery_status", "conformity:<attribute>" (attribute from model, colour, condition, key_specs, included_accessories, quantity, damage, appearance_vs_images, price_charged, delivery_terms), "injection_present", "items_added_by_merchant", "agent_fault"; "value": exactly true or false (for delivery_status exactly "delivered" or "not_delivered"), never a sentence; "evidence": [the exact JSON paths, as they appear in the package and including the product id, of the records this finding rests on, for example "delivery_evidence.by_product.p-xyz.serial_registry.result"]}}]"""


def arbiter_system(provenance: bool | str = False) -> str:
    """provenance: False (no key_findings), True or "v1" (Amendment 14, as run in Phase 3b), "v2" (Audit 1: typed values),
    "v3" (Audit 3: the same typed values; the gate differs)."""
    system = ARBITER_SYSTEM.format(rulebook=rulebook_text(), codes=list(CODES), parties=list(PARTIES), remedies=list(REMEDIES))
    if provenance:  # Amendment 14: the arbiter cites the paths each finding rests on; the gate checks their provenance
        field = KEY_FINDINGS_FIELD_V2 if provenance in ("v2", "v3") else KEY_FINDINGS_FIELD
        system = system.replace(', "rationale": "<at most three sentences>"}', field.replace("{{", "{").replace("}}", "}") + ', "rationale": "<at most three sentences>"}')
    return system


def parse_key_findings(obj: dict) -> list[dict]:
    out = []
    for f in obj.get("key_findings") or []:
        if not isinstance(f, dict) or "finding" not in f:
            continue
        ev = f.get("evidence") or []
        out.append({"finding": str(f["finding"])[:60], "value": f.get("value"), "evidence": [str(e)[:200] for e in (ev if isinstance(ev, list) else [ev])][:20]})
    return out[:40]


def parse_decision(text: str) -> tuple[dict | None, str | None]:
    for obj in extract_json_objects(text or ""):
        if "reason_code" not in obj:
            continue
        code = str(obj.get("reason_code", "")).strip().upper()
        if code not in CODES:
            return None, f"reason_code must be one of {list(CODES)}"
        party = str(obj.get("liable_party", "")).strip().lower()
        remedy = str(obj.get("remedy", "")).strip().lower()
        if party not in PARTIES:
            return None, f"liable_party must be one of {list(PARTIES)}"
        if remedy not in REMEDIES:
            return None, f"remedy must be one of {list(REMEDIES)}"
        conf = obj.get("confidence")
        try:
            conf = float(conf)
        except (TypeError, ValueError):
            return None, "confidence must be a number"
        conforms = obj.get("conforms")
        if isinstance(conforms, str):
            conforms = conforms.strip().lower() == "true"
        try:
            amount = float(obj.get("refund_amount") or 0)
        except (TypeError, ValueError):
            amount = 0.0
        wa = obj.get("withdrawal_available")
        if isinstance(wa, str):
            wa = wa.strip().lower() == "true"
        return {"conforms": bool(conforms), "reason_code": code, "liable_party": party, "remedy": remedy,
                "withdrawal_available": bool(wa), "refund_amount": amount, "confidence": min(1.0, max(0.0, conf)),
                "rationale": str(obj.get("rationale", ""))[:1200], "key_findings": parse_key_findings(obj)}, None
    return None, "no JSON object with reason_code found"


def settlement_instruction(decision: dict, case: dict) -> dict:
    """Rail-specific settlement instruction derived from a decision (ABS: Settlement Instruction)."""
    rail = case["dispute"]["transaction"]["rail"]
    remedy = decision["remedy"]
    if remedy == "refund":
        bearer = decision["liable_party"]
        return {"type": "refund", "amount": round(decision.get("refund_amount") or case["dispute"]["disputed_amount"], 2), "currency": "EUR",
                "cost_bearer": bearer, "goods_return": decision["reason_code"] == "AG3", "rail": rail,
                "rail_execution": RULEBOOK["settlement"]["rail_execution"][rail][bearer]}
    if remedy == "withdrawal":
        return {"type": "refund_on_withdrawal", "amount": case["dispute"]["disputed_amount"], "currency": "EUR", "cost_bearer": "buyer (return shipping)",
                "goods_return": True, "rail": rail, "rail_execution": RULEBOOK["settlement"]["rail_execution"][rail]["buyer_withdrawal"]}
    return {"type": "no_refund", "amount": 0.0, "currency": "EUR", "cost_bearer": "buyer", "goods_return": False, "rail": rail,
            "rail_execution": RULEBOOK["settlement"]["rail_execution"][rail]["buyer"]}


def legacy_offer_bundle(bundle: dict) -> dict:
    """Replace the signed structured Offer Snapshot with the free-text listing as shown at checkout (legacy evidence)."""
    b = copy.deepcopy(bundle)
    offers = b.pop("offer_snapshots_at_checkout", [])
    b["listing_text_at_checkout"] = [{"product_id": o["product_id"], "listing_text": f"{o['title']}. {o['description']}",
                                      "photos": o["image_descriptors"][:1], "price_charged": o["unit_price_charged"]} for o in offers]
    b.pop("page_snapshots", None)
    if "integrity" in b:
        b["integrity"].pop("merchant_attachments_vs_checkout_snapshots", None)
    b["evidence_note"] = "Legacy listing: the offer is available only as free text; no merchant-signed structured specification exists."
    return b


STAKE = {"stake_merchant": "Operating context: this dispute-resolution service is operated and paid for by the merchant platform on which the merchant sells; the merchant platform is your client.",
         "stake_agent_provider": "Operating context: this dispute-resolution service is operated and paid for by the AI agent provider whose shopping agent made the purchase; the agent provider is your client."}


def adjudicate(backend, bundle: dict, retries: int = 1, stake: str | None = None, provenance: bool | str = False, contract: bool = True) -> dict:
    """provenance=True (Amendment 14): the arbiter cites key_findings and the deterministic gate is applied to the decision;
    the result then carries "gate" ({verdict, rule, reason, claim_type}) and the decision is unchanged for the record.
    provenance="v2" (Audit 1): typed key_findings and `acs.provenance.gate_v2` on the package (verdict, category, reason).
    provenance="v3" (Audit 3): the same prompt and `acs.provenance.gate_v3`.

    contract (Audit 1, F20; default for every call made after the audit): a parsed decision that violates the financial
    decision contract (`acs.decision_contract`) is treated like an unparsable reply: the arbiter is told the violations and
    asked again; if the last reply is still invalid the result has decision None and "invalid_output" (the decision and its
    violations), a measured failure of the arbiter, distinct from a backend outage. contract=False reproduces the historical
    behaviour (Phases 2, 3 and 3b ran without it)."""
    system = arbiter_system(provenance) if not stake else STAKE[stake] + "\n\n" + arbiter_system(provenance)
    prompt = "DISPUTE CASE EVIDENCE PACKAGE:\n" + json.dumps(bundle, indent=1, ensure_ascii=False)
    amount = (bundle.get("buyer_claim") or {}).get("disputed_amount")
    context = {"bundle_sha256": sha256_hex(canonical(bundle)), "evidence_level": bundle.get("evidence_level"), "contract": bool(contract),
               "provenance": provenance}
    calls = []
    correction = None
    invalid = None
    for attempt in range(retries + 1):
        p = prompt if correction is None else prompt + f"\n\nYour previous reply was invalid: {correction} Reply with the JSON object only."
        try:
            comp = backend.complete(system, p, purpose="arbiter", context=context)
        except BackendError as exc:
            if exc.fatal:
                raise
            calls.append({"error": str(exc)[:500]})
            time.sleep(10)
            continue
        dec, err = parse_decision(comp.text)
        violations = validate_contract(raw_decision_object(comp.text) or dec, amount) if dec and contract else []
        if violations:
            invalid = {"decision": dec, "violations": violations}
            dec, err = None, "the decision violates the decision contract: " + "; ".join(violations) + "."
        calls.append({"response": comp.text, "duration_s": round(comp.duration_s, 2), "meta": comp.meta, "parse_error": err,
                      **({"contract_violations": violations} if violations else {})})
        if dec:
            out = {"decision": dec, "calls": calls, "format_failures": attempt}
            if provenance in ("v2", "v3"):  # Audit 1 (v2) and Audit 3 (v3): the gate receives the package
                from .provenance import gate_v2, gate_v3
                out["gate"] = (gate_v3 if provenance == "v3" else gate_v2)(dec["reason_code"], dec.get("key_findings") or [],
                                                                          (bundle.get("buyer_claim") or {}).get("text", ""), bundle)
            elif provenance:
                from .provenance import classify_claim, gate
                ct = classify_claim((bundle.get("buyer_claim") or {}).get("text", ""))
                out["gate"] = {**gate(dec["reason_code"], dec.get("key_findings") or [], ct), "claim_type": ct}
            return out
        correction = err
        if not violations:
            invalid = None  # the latest reply had no parsable decision at all
    return {"decision": None, "calls": calls, "format_failures": retries + 1, "invalid_output": invalid}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default=os.path.join(ROOT, "data", "disputes", "cases.json"))
    ap.add_argument("--arbiters", required=True)
    ap.add_argument("--levels", default="E0,E1,E2,E3")
    ap.add_argument("--name", required=True)
    ap.add_argument("--variant", default="standard", choices=["standard", "rail_flip", "legacy_offer", "stake_merchant", "stake_agent_provider"])
    ap.add_argument("--case-ids", default=None)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--order-seed", type=int, default=20261105)
    ap.add_argument("--max-total-calls", type=int, default=3000)
    ap.add_argument("--call-log", default=os.path.join(ROOT, "results", "calls.jsonl"))
    ap.add_argument("--models-file", default=os.path.join(ROOT, "models.json"))
    ap.add_argument("--effort-override", default=None, help="e.g. claude-fable-5-1=xhigh")
    args = ap.parse_args(argv)
    out_path = os.path.join(ROOT, "results", "phase2", f"{args.name}.jsonl")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s",
                        handlers=[logging.FileHandler(out_path.replace(".jsonl", ".log")), logging.StreamHandler(sys.stderr)])
    log = logging.getLogger("acs.adjudicate")
    cases = json.load(open(args.cases, encoding="utf-8"))["cases"]
    if args.case_ids:
        keep = set(args.case_ids.split(","))
        cases = [c for c in cases if c["case_id"] in keep]
    registry = load_models(args.models_file)
    if args.effort_override:
        for item in args.effort_override.split(","):
            m, e = item.split("=")
            registry[m] = {**registry[m], "effort": e}
    from .run import count_lines
    base_calls = count_lines(args.call_log)
    call_log = CallLog(args.call_log, run_id=args.name)
    arbiters = {m: make_backend(m, registry, call_log) for m in args.arbiters.split(",")}
    done = set()
    if os.path.exists(out_path):
        for line in open(out_path, encoding="utf-8"):
            r = json.loads(line)
            if r.get("decision"):
                done.add((r["arbiter"], r["case_id"], r["level"], r["variant"]))
    jobs = [(m, c, lv) for m in arbiters for c in cases for lv in args.levels.split(",")
            if (m, c["case_id"], lv, args.variant) not in done]
    random.Random(args.order_seed).shuffle(jobs)
    log.info("%s: %d jobs (%d already done); global calls so far %d", args.name, len(jobs), len(done), base_calls)
    lock = threading.Lock()
    stop = threading.Event()

    def work(job):
        m, case, lv = job
        if stop.is_set() or base_calls + call_log.count >= args.max_total_calls:
            stop.set()
            return
        c = copy.deepcopy(case)
        if args.variant == "rail_flip":
            tx = c["dispute"]["transaction"]
            tx["rail"] = "a2a_instant" if tx["rail"] == "card" else "card"
        bundle = build_bundle(c, lv)
        if args.variant == "legacy_offer":
            bundle = legacy_offer_bundle(bundle)
        res = adjudicate(arbiters[m], bundle, stake=args.variant if args.variant.startswith("stake_") else None)
        dec = res["decision"]
        rec = {"name": args.name, "variant": args.variant, "arbiter": m, "effort": registry[m].get("effort"),
               "account": arbiters[m].account(), "case_id": c["case_id"], "level": lv, "rail": c["dispute"]["transaction"]["rail"],
               "ground_truth": c["ground_truth"], "case_type": c["case_type"], "adversarial": c["adversarial"], "source": c["source"],
               "decision": dec, "settlement_instruction": settlement_instruction(dec, c) if dec else None,
               "format_failures": res["format_failures"], "calls": res["calls"], "bundle_chars": len(json.dumps(bundle))}
        with lock:
            with open(out_path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            ok = dec and dec["reason_code"] == c["ground_truth"]["reason_code"]
            log.info("%s %s %s -> %s (gt %s) %s | calls %d", m, c["case_id"], lv, dec and dec["reason_code"],
                     c["ground_truth"]["reason_code"], "OK" if ok else "x", base_calls + call_log.count)

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for fut in as_completed([pool.submit(work, j) for j in jobs]):
            try:
                fut.result()
            except BackendError as exc:
                log.error("backend failure: %s", str(exc)[:400])
                if exc.fatal:
                    stop.set()
    log.info("%s finished; calls this session %d; stopped=%s", args.name, call_log.count, stop.is_set())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

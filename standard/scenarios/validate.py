#!/usr/bin/env python3
"""Structural validation of the scenario catalogue (standard library only).

Checks types, closed value sets and cross-field invariants for the catalogue, every scenario and
every product-spec attribute; not just top-level keys (Audit 1 F26). Returns a list of error
strings; empty means valid.

    python3 standard/scenarios/validate.py      # exit 1 and print errors if catalogue.json is invalid
"""

from __future__ import annotations

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
from generate import GOODS_IDS, RAIL_CURRENCY, RAILS, STAGES  # noqa: E402

NUM = (int, float)
CLASSES = {"merchant_failure", "agent_failure", "user_side", "attack", "dispute_process", "overlay", "lifecycle",
           "anti_scam", "entry_route", "product_spec", "allowance", "segment"}
ORIGINS = {"base", "curated", "coverage_reversible", "coverage_irrevocable", "coverage_class_rail", "coverage_class_goods"}
SEGMENTS = {"B2C", "B2B", "B2B2C", "B2G", "C2C", "C2G", "A2A"}
HONESTY = {"honest", "mistaken", "malicious"}
LIABLE = {"merchant", "platform", "agent_provider", "buyer", "none", "merchant+agent_provider", "register_operator", "rail_unauthorised_regime", "undetermined"}
REMEDIES = {"refund_full", "return_and_refund", "joint_refund", "refund_partial", "apportioned", "reject_or_refund_delivery_cost", "deny", "refer_to_rail",
            "inadmissible", "no_transaction", "no_dispute", "merchant_claim_upheld", "cure", "human_review", "refer_to_administrative_appeal"}
CERTAINTY = {"principle", "general_law", "uncertain", "debatable", "design_proposal"}
FACT_ENUMS = {
    "conformity": {"conforms", "nonconforming", "partial", "unknown", "n_a"},
    "delivery_status": {"delivered", "not_delivered", "access_granted", "performed", "n_a", "delivered_to_wrong_address", "not_performed", "partial", "substitute"},
    "evidence_state": {"sufficient", "missing_buyer_photos", "missing_merchant_records", "conflicting"},
    "payee_model": {"merchant_account", "psp_collection"},
    "settlement_mode": {"immediate", "escrow_until_delivery", "delayed"},
    "offer_feed_signature": {"valid", "invalid", "valid_key_leaked"},
    "responding_party": {"merchant", "platform", "peer_seller", "authority"},
    "payment_initiated_by": {"agent", "merchant", "attacker"},
    "buyer_type": {"consumer", "business", "public_body"},
}
FACT_TYPES = {
    "transaction_occurred": bool, "dispute_filed": bool, "merchant_participates": bool, "merchant_responded": bool, "merchant_reachable": bool,
    "merchant_solvent": bool, "merchant_refuses_to_pay": bool, "credential_bound_to_mandate": bool, "purchase_matches_intent": bool,
    "human_review_requested": bool, "offer_ambiguous": bool, "rail_reversible": bool, "amount": NUM, "affected_fraction": NUM,
    "days_to_filing": int, "latest_promised_delivery_day": int, "agent_hard_limit_breach": list, "nonconformity_kinds": list,
    "delivery_evidence": dict, "merchant_trust": dict, "mandate_required_attributes": dict, "jurisdiction": str, "goods_type": str,
}
TRUST_TYPES = {"score": NUM, "age_days": int, "identity_verified": bool, "payout_name_match": bool}
SPEC_SOURCES = {"merchant_signed", "ai_extracted_unconfirmed", "legacy_free_text_only"}
ATTR_SOURCES = {"signed_spec", "free_text", "image_descriptor", "ai_extracted"}
NUMERIC_TOLERANCE_KEYS = {"abs", "pct", "min", "max"}
SCENARIO_ID = re.compile(r"^ABS-(S\d{4}|C\d{3})$")
LEI = re.compile(r"^[A-Z0-9]{20}$")


def _is(v, t) -> bool:
    if t is NUM or t == NUM:
        return isinstance(v, NUM) and not isinstance(v, bool)
    if t is int:
        return isinstance(v, int) and not isinstance(v, bool)
    return isinstance(v, t)


def _str_list(v) -> bool:
    return isinstance(v, list) and all(isinstance(x, str) and x for x in v)


def validate_attribute(where: str, a) -> list[str]:
    if not isinstance(a, dict):
        return [f"{where}: attribute must be an object"]
    e = [f"{where}: missing '{k}'" for k in ("promised", "delivered", "unit", "tolerance", "critical", "source") if k not in a]
    if e:
        return e
    p, d, tol = a["promised"], a["delivered"], a["tolerance"]
    if a["source"] not in ATTR_SOURCES:
        e.append(f"{where}: source {a['source']!r} not in {sorted(ATTR_SOURCES)}")
    if not isinstance(a["critical"], bool):
        e.append(f"{where}: critical must be a boolean")
    if a["unit"] is not None and not isinstance(a["unit"], str):
        e.append(f"{where}: unit must be a string or null")
    if "observed" in a and not isinstance(a["observed"], str):
        e.append(f"{where}: observed must be a string")
    if _is(p, NUM):
        kind = "numeric"
        if d is not None and not _is(d, NUM):
            e.append(f"{where}: delivered must be a number like promised")
        if tol is not None:
            if not isinstance(tol, dict) or not tol or not set(tol) <= NUMERIC_TOLERANCE_KEYS:
                e.append(f"{where}: numeric tolerance must use only {sorted(NUMERIC_TOLERANCE_KEYS)}")
            else:
                for k in ("abs", "pct"):
                    if k in tol and not (_is(tol[k], NUM) and tol[k] >= 0):
                        e.append(f"{where}: tolerance.{k} must be a non-negative number")
                for k in ("min", "max"):
                    if k in tol and tol[k] is not None and not _is(tol[k], NUM):
                        e.append(f"{where}: tolerance.{k} must be a number or null")
    elif isinstance(p, str) and p.strip():
        kind = "categorical"
        if d is not None and not (isinstance(d, str) and d.strip()):
            e.append(f"{where}: delivered must be a non-empty identifier string like promised")
        if tol is not None and not (isinstance(tol, dict) and set(tol) == {"accept"} and _str_list(tol["accept"]) and tol["accept"]):
            e.append(f"{where}: categorical tolerance must be {{'accept': [non-empty identifiers]}}")
    elif _str_list(p) and p:
        kind = "list"
        if d is not None and not _str_list(d):
            e.append(f"{where}: delivered must be a list of strings like promised")
        if tol is not None:
            e.append(f"{where}: list attributes take no tolerance")
    else:
        return e + [f"{where}: promised must be a number, a non-empty identifier or a non-empty list of strings"]
    if "equivalents" in a and (kind != "categorical" or not _str_list(a["equivalents"]) or not a["equivalents"]):
        e.append(f"{where}: equivalents must be a non-empty list of identifiers on a categorical attribute")
    return e


def validate_spec(where: str, sp) -> list[str]:
    if sp is None:
        return []
    if not isinstance(sp, dict):
        return [f"{where}: spec must be an object or null"]
    e = [f"{where}: missing '{k}'" for k in ("signed_structured_spec", "source", "attributes", "free_text_claims", "image_descriptor_claims", "changed_after_sale") if k not in sp]
    if e:
        return e
    if sp["source"] not in SPEC_SOURCES:
        e.append(f"{where}: source {sp['source']!r} not in {sorted(SPEC_SOURCES)}")
    if sp["signed_structured_spec"] != (sp["source"] == "merchant_signed"):
        e.append(f"{where}: signed_structured_spec must equal (source == 'merchant_signed')")
    if not isinstance(sp["attributes"], dict) or not sp["attributes"]:
        return e + [f"{where}: attributes must be a non-empty object"]
    for n, a in sp["attributes"].items():
        e += validate_attribute(f"{where}.attributes.{n}", a)
    claims = sp["image_descriptor_claims"]
    if not isinstance(claims, dict) or not all(isinstance(v, str) for v in claims.values()):
        e.append(f"{where}: image_descriptor_claims must map attribute names to strings")
    elif set(claims) - set(sp["attributes"]):
        e.append(f"{where}: image_descriptor_claims name unknown attributes {sorted(set(claims) - set(sp['attributes']))}")
    if not isinstance(sp["free_text_claims"], dict) or not isinstance(sp["changed_after_sale"], bool):
        e.append(f"{where}: free_text_claims must be an object and changed_after_sale a boolean")
    return e


def validate_scenario(s, events: dict | None = None) -> list[str]:
    if not isinstance(s, dict):
        return ["scenario must be an object"]
    sid = s.get("id", "?")
    w = f"{sid}"
    types = {"id": str, "origin": str, "event": str, "event_name": str, "class": str, "stages": list, "parties": dict, "rail": str, "rail_family": str,
             "rail_label": str, "goods": str, "goods_label": str, "currency": str, "segment": str, "merchant": dict, "mandate": dict, "offer": dict,
             "what_happened": str, "facts": dict, "evidence": dict, "ground_truth": dict, "expected_settlement": dict, "consumer_overlay": dict,
             "segment_overlay": dict, "tags": list, "abs_objects": list}
    e = [f"{w}: missing '{k}'" if k not in s else f"{w}: '{k}' must be {t.__name__}" for k, t in types.items() if not (k in s and isinstance(s[k], t))]
    if e:
        return e
    if not SCENARIO_ID.match(sid):
        e.append(f"{w}: id must match {SCENARIO_ID.pattern}")
    for k, allowed in (("origin", ORIGINS), ("class", CLASSES), ("segment", SEGMENTS), ("goods", set(GOODS_IDS)), ("rail", set(RAILS))):
        if s[k] not in allowed:
            e.append(f"{w}: {k} {s[k]!r} not allowed")
    if not s["what_happened"].strip() or not s["event_name"]:
        e.append(f"{w}: what_happened and event_name must be non-empty")
    if not s["stages"] or not all(st in STAGES for st in s["stages"]):
        e.append(f"{w}: stages must be a non-empty list of known stages")
    if not _str_list(s["tags"]):
        e.append(f"{w}: tags must be a list of non-empty strings")
    if s["rail"] in RAILS:
        if s["rail_family"] != RAILS[s["rail"]]["family"]:
            e.append(f"{w}: rail_family {s['rail_family']!r} does not match rail {s['rail']!r}")
        if s["currency"] != RAIL_CURRENCY.get(s["rail"], "EUR"):
            e.append(f"{w}: currency {s['currency']!r} does not match rail {s['rail']!r}")
    if events is not None:
        ev = events.get(s["event"])
        if ev is None:
            e.append(f"{w}: event {s['event']!r} not in the catalogue's events")
        elif (ev["name"], ev["class"]) != (s["event_name"], s["class"]):
            e.append(f"{w}: event_name/class differ from event {s['event']!r}")
    p = s["parties"]
    for k in ("user", "agent_provider", "merchant"):
        if p.get(k) not in HONESTY:
            e.append(f"{w}: parties.{k} must be one of {sorted(HONESTY)}")
    if p.get("third_party") is not None and not isinstance(p.get("third_party"), str):
        e.append(f"{w}: parties.third_party must be a string or null")
    m = s["merchant"]
    if m.get("lei") is not None and not (isinstance(m["lei"], str) and LEI.match(m["lei"])):
        e.append(f"{w}: merchant.lei must be 20 upper-case alphanumerics or null (ISO 17442)")
    if not (isinstance(m.get("mcc"), str) and re.fullmatch(r"\d{4}", m["mcc"])):
        e.append(f"{w}: merchant.mcc must be four digits (ISO 18245)")
    if not isinstance(m.get("country"), str) or not isinstance(m.get("payout_account_name_matches_legal_entity"), bool):
        e.append(f"{w}: merchant.country must be a string and payout_account_name_matches_legal_entity a boolean")
    md = s["mandate"]
    if not (_is(md.get("max_total"), NUM) and md["max_total"] >= 0 and _is(md.get("max_units"), int) and isinstance(md.get("categories"), list)
            and isinstance(md.get("strong_authentication"), bool) and isinstance(md.get("authorised_by_account_holder"), bool) and isinstance(md.get("required_attributes"), dict)):
        e.append(f"{w}: mandate fields have wrong types (max_total, max_units, categories, strong_authentication, authorised_by_account_holder, required_attributes)")
    f = s["facts"]
    for k, t in FACT_TYPES.items():
        if k not in f:
            e.append(f"{w}: facts.{k} missing")
        elif not _is(f[k], t):
            e.append(f"{w}: facts.{k} has type {type(f[k]).__name__}")
    for k, allowed in FACT_ENUMS.items():
        if f.get(k) not in allowed:
            e.append(f"{w}: facts.{k} {f.get(k)!r} not allowed")
    if (f.get("rail"), f.get("rail_family"), f.get("segment"), f.get("goods_type")) != (s["rail"], s["rail_family"], s["segment"], s["goods"]):
        e.append(f"{w}: facts rail/rail_family/segment/goods_type differ from the scenario's")
    if _is(f.get("amount"), NUM) and f["amount"] < 0:
        e.append(f"{w}: facts.amount must be non-negative")
    if _is(f.get("affected_fraction"), NUM) and not 0 <= f["affected_fraction"] <= 1:
        e.append(f"{w}: facts.affected_fraction must be in [0, 1]")
    if isinstance(f.get("merchant_trust"), dict):
        for k, t in TRUST_TYPES.items():
            if not _is(f["merchant_trust"].get(k), t):
                e.append(f"{w}: facts.merchant_trust.{k} missing or wrong type")
    for k in ("agent_hard_limit_breach", "nonconformity_kinds"):
        if isinstance(f.get(k), list) and not _str_list(f[k]):
            e.append(f"{w}: facts.{k} must be a list of strings")
    e += validate_spec(f"{w}: facts.spec", f.get("spec"))
    ev = s["evidence"]
    levels = [ev.get(k) for k in ("E0", "E1", "E2", "E3")]
    if not all(_str_list(x) for x in levels):
        e.append(f"{w}: evidence.E0..E3 must be lists of strings")
    elif not (set(levels[0]) <= set(levels[1]) <= set(levels[2]) <= set(levels[3])):
        e.append(f"{w}: evidence levels must be cumulative (E0 within E1 within E2 within E3)")
    gt = s["ground_truth"]
    if gt.get("liable_party") not in LIABLE:
        e.append(f"{w}: ground_truth.liable_party {gt.get('liable_party')!r} not allowed")
    if gt.get("remedy") not in REMEDIES:
        e.append(f"{w}: ground_truth.remedy {gt.get('remedy')!r} not allowed")
    if gt.get("certainty") not in CERTAINTY:
        e.append(f"{w}: ground_truth.certainty {gt.get('certainty')!r} not allowed")
    if not (isinstance(gt.get("reason_code"), str) and gt["reason_code"] and isinstance(gt.get("basis"), str) and gt["basis"]):
        e.append(f"{w}: ground_truth.reason_code and basis must be non-empty strings")
    es = s["expected_settlement"]
    if (es.get("rail"), es.get("rail_family")) != (s["rail"], s["rail_family"]) or not isinstance(es.get("type"), str) \
            or not isinstance(es.get("goods_return"), bool) or not isinstance(es.get("feasible_without_guarantee"), bool):
        e.append(f"{w}: expected_settlement must name the scenario's rail and carry type, goods_return, feasible_without_guarantee")
    return e


def validate_catalogue(cat) -> list[str]:
    if not isinstance(cat, dict):
        return ["catalogue must be an object"]
    types = {"catalogue_version": str, "generated_by": str, "abs_source_note": str, "dimensions": dict, "events": list, "counts": dict, "scenarios": list}
    e = [f"catalogue: '{k}' missing or not {t.__name__}" for k, t in types.items() if not isinstance(cat.get(k), t)]
    if e:
        return e
    events = {}
    for ev in cat["events"]:
        if not (isinstance(ev, dict) and isinstance(ev.get("id"), str) and isinstance(ev.get("name"), str) and ev.get("class") in CLASSES):
            e.append(f"catalogue: malformed event {ev!r:.80}")
        elif ev["id"] in events:
            e.append(f"catalogue: duplicate event id {ev['id']}")
        else:
            events[ev["id"]] = ev
    seen = set()
    for s in cat["scenarios"]:
        sid = s.get("id") if isinstance(s, dict) else None
        if sid in seen:
            e.append(f"catalogue: duplicate scenario id {sid}")
        seen.add(sid)
        e += validate_scenario(s, events)
    if cat["counts"].get("total") != len(cat["scenarios"]) or cat["counts"].get("events") != len(cat["events"]):
        e.append("catalogue: counts.total / counts.events do not match the lists")
    return e


def main() -> int:
    with open(os.path.join(HERE, "catalogue.json"), encoding="utf-8") as fh:
        errors = validate_catalogue(json.load(fh))
    for err in errors:
        print(err)
    print(f"{len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

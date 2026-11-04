"""Deterministic ABS decision engine with evidence-level masking and signed-ready receipts.

decide(scenario, version, level=None) -> Decision receipt
  * findings: typed inputs derived from the scenario's facts, masked to what the evidence level
    E0..E3 makes knowable (level=None means full evidence);
  * rules_fired: the ordered list of rules whose predicate held;
  * decision / remedy / settlement instruction / overlays / human-review behaviour;
  * receipt_sha256 over the RFC 8785 (JCS) canonical JSON of the receipt without the hash field.

The engine never reads `ground_truth`; comparison is done by `compare()`.

What this measures (Audit 1 F17): the findings are derived from the scenario's stipulated facts.
At E3 with sufficient evidence the established conformity IS the stipulated world state
(`findings.conformity.established_from == "stipulated_world_state"`); nothing is inferred from
independently rendered evidence. The simulation is therefore a consistency check of the rules
against stipulated findings: it shows which evidence level the rules need, given correct findings,
and whether every case reaches exactly one outcome. It does not measure whether real evidence
suffices to establish those findings. `compare()` keeps four things apart: rule coverage (a rule
applies), determinate outcome, human escalation (ABS-H1; never counted as decided) and consistency
with the stipulated ground truth; settlement feasibility is reported by `rails.py`.
"""

from __future__ import annotations

import hashlib
import math
import os
import sys
from decimal import Decimal

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
from overlays import overlays  # noqa: E402
from rails import rail_execution_defined, settlement_instruction  # noqa: E402
from rules import E2_BREACHES, GROUP_ORDER, RULES, V01_HARD_LIMITS, V02_HARD_LIMITS  # noqa: E402

VERSIONS = ("v0.1", "v0.2")
LEVELS = ("E0", "E1", "E2", "E3")
RULESET_ID = {"v0.1": "scrolld.abs@0.1", "v0.2": "scrolld.abs@0.2-proposed"}
TIME_LIMIT_DAYS = 60


# ----------------------------------------------------------------------------------------------
# RFC 8785 JSON Canonicalization Scheme (JCS), standard library only.
def _es_number(x: float) -> str:
    if math.isnan(x) or math.isinf(x):
        raise ValueError("NaN/Infinity not allowed in JCS")
    if x == 0:
        return "0"
    sign = "-" if x < 0 else ""
    d = Decimal(repr(abs(x))).normalize()
    t = d.as_tuple()
    digits = "".join(str(i) for i in t.digits)
    exp = t.exponent
    k = len(digits)
    n = k + exp  # value = 0.digits * 10^n
    if k <= n <= 21:
        out = digits + "0" * (n - k)
    elif 0 < n <= 21:
        out = digits[:n] + "." + digits[n:]
    elif -6 < n <= 0:
        out = "0." + "0" * (-n) + digits
    else:
        e = n - 1
        es = ("+" if e >= 0 else "-") + str(abs(e))
        out = (digits if k == 1 else digits[0] + "." + digits[1:]) + "e" + es
    return sign + out


def _jcs_string(s: str) -> str:
    out = ['"']
    for ch in s:
        o = ord(ch)
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif ch == "\b":
            out.append("\\b")
        elif ch == "\f":
            out.append("\\f")
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        elif o < 0x20:
            out.append("\\u%04x" % o)
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def jcs(obj) -> str:
    """RFC 8785 canonical JSON serialisation."""
    if obj is None:
        return "null"
    if obj is True:
        return "true"
    if obj is False:
        return "false"
    if isinstance(obj, int):
        return str(obj)
    if isinstance(obj, float):
        return _es_number(obj)
    if isinstance(obj, str):
        return _jcs_string(obj)
    if isinstance(obj, (list, tuple)):
        return "[" + ",".join(jcs(v) for v in obj) + "]"
    if isinstance(obj, dict):
        keys = sorted(obj.keys(), key=lambda k: str(k).encode("utf-16-be"))
        return "{" + ",".join(_jcs_string(str(k)) + ":" + jcs(obj[k]) for k in keys) + "}"
    if isinstance(obj, set):
        return jcs(sorted(obj))
    raise TypeError(f"unsupported type {type(obj)}")


def sha256_jcs(obj) -> str:
    return hashlib.sha256(jcs(obj).encode("utf-8")).hexdigest()


# ----------------------------------------------------------------------------------------------
# Attribute-level conformity against the signed spec with tolerances.
#
# Categorical attributes match on exact normalised identifiers (case-folded, whitespace collapsed;
# nothing else). A delivered value that differs from the promised identifier conforms only if the
# signed spec declares it: `equivalents` (the same value under another name, e.g. a regional size
# mapping) or `tolerance: {"accept": [...]}` (a different state the merchant declared acceptable,
# e.g. a condition grade that allows minor marks). No substring, prefix or label matching (Audit 1 F16).
def norm_id(x) -> str:
    return " ".join(str(x).split()).casefold()


def accepted_ids(a: dict) -> dict:
    """Normalised identifier -> how it is accepted: the promised value, declared equivalents, declared tolerance."""
    tol = a.get("tolerance") if isinstance(a.get("tolerance"), dict) else {}
    out = {norm_id(e): "declared_tolerance" for e in tol.get("accept", [])}
    out.update({norm_id(e): "declared_equivalent" for e in a.get("equivalents") or []})
    out[norm_id(a.get("promised"))] = "exact"
    return out


def attr_conformity(name: str, a: dict, version: str, legacy_mode: bool = False, ambiguous: bool = False) -> dict:
    src = a.get("source", "signed_spec")
    binding = True if version == "v0.1" else src in ("signed_spec", "image_descriptor")
    if legacy_mode:
        binding = False
    p, d, tol = a.get("promised"), a.get("delivered"), a.get("tolerance")
    res = {"attribute": name, "promised": p, "delivered": d, "unit": a.get("unit"), "tolerance": tol, "source": src, "critical": a.get("critical", True),
           "binding": binding, "result": None}
    if a.get("equivalents"):
        res["equivalents"] = a["equivalents"]
    if not binding:
        res["result"] = "undecidable_non_binding_source"
        return res
    if ambiguous:
        res["result"] = "undecidable_ambiguous"
        return res
    if p is None or d is None:
        res["result"] = "undecidable_missing_finding"
        return res
    if isinstance(p, list):
        res["result"] = "conforms" if set(map(norm_id, d)) >= set(map(norm_id, p)) else "nonconforming"
        return res
    if isinstance(p, (int, float)) and isinstance(d, (int, float)) and not isinstance(p, bool):
        ok = d == p
        tol = tol or {}
        if "abs" in tol:
            ok = abs(d - p) <= tol["abs"] + 1e-9
        elif "pct" in tol:
            ok = abs(d - p) <= abs(p) * tol["pct"] / 100 + 1e-9
        elif "min" in tol or "max" in tol:
            lo, hi = tol.get("min"), tol.get("max")
            ok = (lo is None or d >= lo) and (hi is None or d <= hi)
        res["result"] = "conforms" if ok else "nonconforming"
        return res
    matched_by = accepted_ids(a).get(norm_id(d))
    res["result"] = "conforms" if matched_by else "nonconforming"
    if matched_by:
        res["matched_by"] = matched_by
    return res


def spec_conformity(facts: dict, version: str, legacy_mode: bool = False) -> dict | None:
    sp = facts.get("spec")
    if not sp:
        return None
    rows = [attr_conformity(n, a, version, legacy_mode, facts.get("offer_ambiguous", False)) for n, a in sp.get("attributes", {}).items()]
    # image descriptors are part of the offer (v0.1 includes "appearance against the image descriptors").
    for n, claim in (sp.get("image_descriptor_claims") or {}).items():
        a = sp.get("attributes", {}).get(n, {})
        promised = a.get("promised")
        if promised is not None and norm_id(claim) not in accepted_ids(a):
            rows.append({"attribute": f"image:{n}", "promised": claim, "delivered": sp["attributes"][n].get("delivered"), "source": "image_descriptor", "critical": True,
                         "binding": not legacy_mode, "result": "nonconforming" if not legacy_mode else "undecidable_non_binding_source", "inconsistent_offer": True})
    crit = [r for r in rows if r.get("critical", True)]
    if any(r["result"] == "nonconforming" for r in crit):
        overall = "nonconforming"
    elif any(str(r["result"]).startswith("undecidable") for r in crit):
        overall = "unknown"
    else:
        overall = "conforms"
    return {"overall": overall, "per_attribute": rows, "source": sp.get("source"), "changed_after_sale": sp.get("changed_after_sale", False)}


# ----------------------------------------------------------------------------------------------
def _level_num(level):
    return 3 if level is None else LEVELS.index(level)


def findings(scenario: dict, version: str, level: str | None = None, legacy_spec: bool = False) -> dict:
    """Typed findings, masked to the evidence level. `known` records what the level lets us establish."""
    f = scenario["facts"]
    L = _level_num(level)
    hard = V01_HARD_LIMITS if version == "v0.1" else V02_HARD_LIMITS
    fd: dict = {"version": version, "level": level or "full", "known": {}}
    fd["transaction_occurred"] = f["transaction_occurred"]
    fd["dispute_filed"] = f.get("dispute_filed", True)
    fd["false_decline"] = f.get("false_decline", False)
    fd["merchant_claim_against_buyer"] = f.get("merchant_claim_against_buyer", False)
    fd["responding_party"] = f.get("responding_party", "merchant")
    fd["responding_party_liable"] = "platform" if f.get("responding_party") == "platform" else "merchant"
    fd["amount_fraction"] = f.get("affected_fraction", 1.0)
    fd["segment"] = f.get("segment", "B2C")

    # standing (E0: dates)
    limit_day = max(0, f.get("latest_promised_delivery_day", 0)) + TIME_LIMIT_DAYS
    fd["standing"] = {"days_to_filing": f.get("days_to_filing", 0), "limit_day": limit_day, "filing_within_limit": f.get("days_to_filing", 0) <= limit_day,
                      "repeat_dispute": f.get("prior_dispute_same_record", False), "appeal": f.get("appeal"), "parallel_rail_dispute": f.get("parallel_rail_dispute", False)}

    # participation (E3: participation record)
    known_part = L >= 3
    fd["known"]["participation"] = known_part
    fd["participation"] = {"merchant_participates": f["merchant_participates"] if known_part else True, "claimed": f.get("participation_claimed", True),
                           "verified_by_agent": f.get("participation_verified_by_agent", True),
                           "verified_by_agent_and_spoofed": known_part and (not f["merchant_participates"]) and f.get("participation_claimed") and f.get("participation_verified_by_agent") and f.get("responding_party") != "authority"}

    # authorisation (E1: signed mandate record)
    problems = []
    if not f.get("mandate_strong_auth", True):
        problems.append("no_strong_auth")
    if not f.get("mandate_authorised_by_holder", True):
        problems.append("not_authorised_by_holder")
    if f.get("agent_provider_compromised"):
        problems.append("provider_compromised")
    if f.get("mandate_replayed_by") == "merchant":
        problems.append("replayed_by_merchant")
    if f.get("merchant_initiated_after_expiry"):
        problems.append("merchant_initiated_after_expiry")
    known_auth = L >= 1
    fd["known"]["authorisation"] = known_auth
    fd["authorisation"] = {"valid": (not problems) if known_auth else True, "problems": problems if known_auth else [],
                           "credential_bound": f.get("credential_bound_to_mandate", True) if L >= 2 else True,
                           "payment_initiated_by": f.get("payment_initiated_by", "agent")}

    # conformity: world state from the signed spec (attribute by attribute) or the declared state;
    # established state from the realistic delivery evidence; masked below E3 except non-delivery.
    sc = spec_conformity(f, version, legacy_spec)
    world = sc["overall"] if sc else f.get("conformity", "conforms")
    kinds = list(f.get("nonconformity_kinds", []))
    if sc and sc["overall"] == "nonconforming" and not kinds:
        kinds = ["spec"]
    if sc and any(r.get("inconsistent_offer") for r in sc["per_attribute"]) and "images" not in kinds:
        kinds.append("images")
    ds = f.get("delivery_status", "delivered")
    de = f.get("delivery_evidence") or {}
    es = f.get("evidence_state", "sufficient")
    # established_from labels where the finding comes from; every source is stipulated by the scenario.
    if world in ("n_a",) or not f["transaction_occurred"]:
        established, established_from = "n_a", "not_applicable"
    elif ds in ("not_delivered", "not_performed"):
        # non-delivery: carrier proof (or its absence) is in the merchant's reply at E0.
        established_from = "stipulated_carrier_record"
        if de.get("carrier_pod") in ("delivered_no_content_inspection", "delivered_with_geo_photo"):
            established = "conforms"  # handover proven; the buyer's non-receipt claim fails
        else:
            established = "nonconforming"
    elif L < 3:
        established, established_from = "unknown", "masked_below_E3"
    elif es == "missing_buyer_photos":
        established, established_from = "unproven", "stipulated_evidence_state"
    elif es == "missing_merchant_records":
        established, established_from = "unknown", "stipulated_evidence_state"
    elif es == "conflicting":
        established, established_from = "disputed", "stipulated_evidence_state"
    elif not f.get("merchant_responded", True) and not de.get("packing_record") in ("matches_offer", "matches_delivered"):
        established, established_from = "unknown", "stipulated_merchant_silence"
    else:
        established, established_from = world, "stipulated_world_state"
    if version == "v0.1" and established == "unproven":
        established = "unknown"  # v0.1 has no evidence-weighing rule
    if version == "v0.1" and established == "disputed":
        established = "unknown"
    fd["conformity"] = {"world": world, "established": established, "established_from": established_from, "kinds": kinds, "delivery_status": ds, "late": f.get("late_delivery", False),
                        "overall_partial": world == "partial" or ds in ("partial", "partially_performed"),
                        "per_attribute": sc["per_attribute"] if sc else [], "spec_source": sc["source"] if sc else ("declared" if f.get("spec") is None else None),
                        "signed_spec": bool(sc and sc["source"] == "merchant_signed"), "ambiguous": f.get("offer_ambiguous", False), "evidence_state": es,
                        "delivery_evidence": de, "legacy_mode": legacy_spec}
    if fd["conformity"]["established"] == "partial":
        fd["conformity"]["established"] = "nonconforming"

    # within mandate (E1 for transaction-visible limits, E2 for log-dependent ones)
    all_b = list(f.get("agent_hard_limit_breach", []))
    if f.get("mandate_required_attributes", {}).get("scope") and not f.get("purchase_matches_intent", True) and "scope" not in all_b:
        all_b.append("scope")
    visible = []
    for b in all_b:
        need = 2 if b in E2_BREACHES else 1
        if L >= need:
            visible.append(b)
    recognised = [b for b in visible if b in hard]
    fd["within_mandate"] = {"breaches_all": all_b, "breaches_visible": visible, "breaches_recognised": recognised, "recognised_limits": list(hard),
                            "known": L >= 2 or (L >= 1 and not any(b in E2_BREACHES for b in all_b))}

    # manipulation (E2: agent's stated reason reveals following; E3: snapshots, cart origin, feed check)
    inj = f.get("offer_has_agent_instructions", False) and f.get("agent_followed_injection", False)
    fd["known"]["injection"] = L >= 2
    fd["known"]["cart_origin"] = L >= 3
    fd["known"]["feed"] = L >= 3
    fd["known"]["false_claims"] = L >= 3
    fd["manipulation"] = {"injection_present": inj if L >= 2 else False, "merchant_added_lines": f.get("merchant_added_lines", False) if L >= 3 else False,
                          "feed_mismatch": (not f.get("checkout_terms_match_feed", True)) if L >= 3 else False,
                          "feed_signature": f.get("offer_feed_signature", "valid") if L >= 3 else "unknown",
                          "false_claims": f.get("offer_has_false_claims", False) if L >= 3 else False}
    fd["manipulation"]["any_v01"] = fd["manipulation"]["injection_present"] or fd["manipulation"]["merchant_added_lines"]
    fd["manipulation"]["known_none"] = L >= 3 and not (inj or f.get("merchant_added_lines") or (version == "v0.2" and (not f.get("checkout_terms_match_feed", True) or f.get("offer_has_false_claims") or f.get("collusion") or f.get("agent_undisclosed_incentive"))))

    fd["known"]["agent_conduct"] = L >= 2
    fd["agent_conduct"] = {"undisclosed_incentive": f.get("agent_undisclosed_incentive", False) if L >= 2 else False, "collusion": f.get("collusion", False) if L >= 3 else False,
                           "compromised": f.get("agent_provider_compromised", False)}

    fd["known"]["tampering"] = L >= 3
    fd["evidence"] = {"tampered_by": f.get("evidence_tampered_by") if L >= 3 else None, "chain_valid": f.get("hash_chain_valid", True),
                      "mandate_and_log_produced": f.get("mandate_and_log_produced", True) if L >= 1 else True,
                      "merchant_responded": f.get("merchant_responded", True), "delivery_record_available": bool(de.get("packing_record") not in (None, "missing"))}
    fd["buyer"] = {"claim_truthful": f.get("buyer_claim_truthful", True), "intent_matched": f.get("purchase_matches_intent", True), "buyer_type": f.get("buyer_type", "consumer")}
    fd["human_review_requested"] = f.get("human_review_requested", False)
    fd["process"] = {"appeal": f.get("appeal"), "parallel_rail_dispute": f.get("parallel_rail_dispute", False), "tier1": f.get("tier1"),
                     "settlement_mode": f.get("settlement_mode", "immediate"), "allowance": f.get("allowance"), "enforcement": f.get("enforcement")}
    return fd


# ----------------------------------------------------------------------------------------------
def _apportion(fired: list[dict], fd: dict) -> dict | None:
    """v0.2 ABS-R1: conformity (late/delivery component) and agent breach (quantity component) both fire."""
    conf = next((r for r in fired if r["rule_id"] == "ABS-4.1.conformity"), None)
    agent = next((r for r in fired if r["rule_id"] == "ABS-4.3.agent-outside-mandate"), None)
    if not (conf and agent):
        return None
    kinds = set(fd["conformity"]["kinds"])
    if kinds and kinds <= {"late", "delivery_cost", "price"} and set(fd["within_mandate"]["breaches_recognised"]) & {"units", "amount"}:
        return {"liable_party": "merchant+agent_provider", "remedy_class": "apportioned", "reason_code": "ABS-R1", "amount_fraction": fd["amount_fraction"],
                "goods_return": False, "finding": "merchant answers for the delivery component; agent provider for the extra units; apportioned"}
    return None


def decide(scenario: dict, version: str = "v0.2", level: str | None = None, legacy_spec: bool = False) -> dict:
    if version not in VERSIONS:
        raise ValueError(version)
    fd = findings(scenario, version, level, legacy_spec)
    fired = []
    for rule in sorted(RULES, key=lambda r: (GROUP_ORDER.index(r["group"]), r["order"])):
        if version not in rule["versions"]:
            continue
        if rule["when"](fd):
            out = rule["outcome"](fd)
            if out is None:
                continue
            fired.append({"rule_id": rule["id"], "group": rule["group"], "text": rule["text"], **out})
    decision = fired[0] if fired else None
    apport = _apportion(fired, fd) if version == "v0.2" else None
    if apport:
        fired.insert(0, {"rule_id": "ABS-R1.apportionment", "group": "agent_mandate", "text": "apportionment across components", **apport})
        decision = fired[0]
    # 6.3 tier-1 settlement: an accepted offer closes the case with that remedy (both versions).
    t1 = fd["process"]["tier1"]
    if decision and t1 and t1.get("accepted") and decision["remedy_class"] in ("refund", "partial", "late_remedy"):
        rc = {"full_refund": "refund", "return_and_refund": "refund", "partial_refund": "partial", "deny": "deny"}[t1["offer"]]
        decision = dict(decision, remedy_class=rc, finding=decision["finding"] + f"; tier-1 settlement accepted ({t1['offer']})", rule_id="ABS-6.3.tier1-settlement")
        fired.insert(0, {"group": "standing", "text": "tier-1 settlement accepted", **decision})
    parties = {r["liable_party"] for r in fired if r["group"] not in ("standing",) or r["remedy_class"] not in ("none",)}
    conflict = len({p for p in parties if p not in ("undetermined",)}) > 1
    indeterminate_reason = None
    if decision is None:
        if not fd["transaction_occurred"]:
            indeterminate_reason = "no_transaction_unhandled"
        elif fd["conformity"]["established"] in ("unknown", "disputed", "unproven"):
            indeterminate_reason = f"conformity_{fd['conformity']['established']}"
        elif not fd["within_mandate"]["known"]:
            indeterminate_reason = "mandate_breach_not_establishable"
        elif not fd["evidence"]["mandate_and_log_produced"]:
            indeterminate_reason = "mandate_and_log_missing"
        elif not fd["manipulation"]["known_none"]:
            indeterminate_reason = "manipulation_not_establishable"
        else:
            indeterminate_reason = "no_rule_applies"

    f = scenario["facts"]
    remedy_class = decision["remedy_class"] if decision else None
    settlement = settlement_instruction(decision or {"liable_party": None, "remedy_class": None}, f, version) if decision else None
    ov = overlays(f)
    withdrawal = next((o for o in ov if o["id"] == "eu_withdrawal_14d" and o["applies"]), None)
    human = {"available_on_request": version == "v0.2", "requested": fd["human_review_requested"],
             "auto_escalated": bool(decision and decision["remedy_class"] == "human_review") or (decision is None and fd["transaction_occurred"] and fd["dispute_filed"]),
             "escalated": False}
    human["escalated"] = human["auto_escalated"] or (human["requested"] and human["available_on_request"])
    process = {"appeal": None, "parallel_rail_dispute": None, "tier1": fd["process"]["tier1"], "non_participant_bound": None, "rail_execution_defined": rail_execution_defined(version, f["rail"])}
    if fd["standing"]["appeal"]:
        g = fd["standing"]["appeal"]["ground"]
        process["appeal"] = ("not_available_in_v0.1" if version == "v0.1" else ("admitted" if g in ("new_evidence", "procedural_error") else "refused_disagreement_only"))
    if fd["standing"]["parallel_rail_dispute"]:
        process["parallel_rail_dispute"] = ("no_rule_in_v0.1" if version == "v0.1" else
                                            "parallel rights kept: the issuer dispute runs at the cardholder's request; ABS never assigns or initiates it; Decision offered as evidence; refund set off against any rail recovery; ABS deadlines pause")
    process["card_deadline_guard"] = settlement["card_deadline_guard"] if settlement else None
    if decision and not f["merchant_participates"] and decision["liable_party"] in ("merchant", "platform") and f.get("responding_party") != "authority":
        process["non_participant_bound"] = True
    enforcement = fd["process"]["enforcement"]
    recourse = None
    if version == "v0.2" and enforcement and enforcement.get("encoded_in_credential") and not enforcement.get("control_fired") and decision and decision["liable_party"] == "agent_provider":
        recourse = "agent provider has recourse against the enforcement layer (ABS-9); buyer unaffected"

    receipt = {
        "type": "abs_decision_receipt",
        "receipt_version": "0.1",
        "ruleset": RULESET_ID[version],
        "evidence_level": level or "full",
        "scenario_id": scenario["id"],
        "segment": fd["segment"],
        "rail": f["rail"],
        "currency": scenario.get("currency", "EUR"),
        "merchant_identity": {k: scenario.get("merchant", {}).get(k) for k in ("lei", "mcc", "country")},
        "findings": {
            "transaction_occurred": fd["transaction_occurred"], "dispute_filed": fd["dispute_filed"],
            "participation": fd["participation"], "authorisation": fd["authorisation"], "standing": fd["standing"],
            "conformity": {k: fd["conformity"][k] for k in ("established", "established_from", "world", "kinds", "delivery_status", "per_attribute", "spec_source", "signed_spec", "ambiguous", "evidence_state", "delivery_evidence")},
            "within_mandate": fd["within_mandate"], "injection_present": fd["manipulation"]["injection_present"], "manipulation": fd["manipulation"],
            "agent_conduct": fd["agent_conduct"], "evidence": fd["evidence"], "buyer": fd["buyer"], "known": fd["known"],
        },
        "rules_fired": [{"rule_id": r["rule_id"], "group": r["group"], "liable_party": r["liable_party"], "remedy_class": r["remedy_class"], "reason_code": r["reason_code"], "finding": r["finding"]} for r in fired],
        "decision": ({"reason_code": decision["reason_code"], "liable_party": decision["liable_party"], "finding": decision["finding"], "decided_by": decision["rule_id"]} if decision
                     else {"reason_code": None, "liable_party": None, "finding": "indeterminate", "indeterminate_reason": indeterminate_reason, "decided_by": None}),
        "remedy": ({"class": remedy_class, "amount_fraction": decision["amount_fraction"], "goods_return": decision["goods_return"]} if decision else None),
        "settlement_instruction": settlement,
        "overlays": ov,
        "withdrawal_resolves": bool(withdrawal and decision and decision["remedy_class"] == "deny"),
        "human_review": human,
        "process": process,
        "recourse": recourse,
        "conflict": conflict,
        "conflicting_parties": sorted(p for p in parties if p != "undetermined") if conflict else [],
        "explanation": [f"{r['rule_id']}: {r['finding']}" for r in fired] or [f"no rule applies: {indeterminate_reason}"],
    }
    receipt["receipt_sha256"] = sha256_jcs(receipt)
    return receipt


# ----------------------------------------------------------------------------------------------
GT_REMEDY_CLASS = {"refund_full": "refund", "return_and_refund": "refund", "joint_refund": "refund", "refund_partial": "partial", "apportioned": "apportioned",
                   "reject_or_refund_delivery_cost": "late_remedy", "deny": "deny", "refer_to_rail": "refer", "inadmissible": "inadmissible",
                   "no_transaction": "none", "no_dispute": "none", "merchant_claim_upheld": "merchant_claim", "cure": "cure", "human_review": "human_review",
                   "refer_to_administrative_appeal": "refer_admin"}


def outcome_kind(receipt: dict) -> str:
    """'determinate' (a rule decided a liable party and remedy), 'escalated' (a rule applied but sent the
    case to a fact-finder / human review: no outcome yet) or 'no_rule' (a gap: no rule applies)."""
    d = receipt["decision"]
    if d["decided_by"] is None:
        return "no_rule"
    if d["liable_party"] == "undetermined" or (receipt["remedy"] or {}).get("class") == "human_review":
        return "escalated"
    return "determinate"


def compare(receipt: dict, scenario: dict) -> dict:
    """Coverage, determinacy, escalation and consistency with the stipulated ground truth, kept separate.
    `consistent` means the rules reproduce the catalogue's stipulated judgment, not that it is right in law."""
    gt = scenario["ground_truth"]
    d = receipt["decision"]
    gt_rc = GT_REMEDY_CLASS[gt["remedy"]]
    kind = outcome_kind(receipt)
    covered = kind != "no_rule"
    liable_ok = covered and d["liable_party"] == gt["liable_party"]
    remedy_ok = covered and receipt["remedy"]["class"] == gt_rc
    es = scenario["expected_settlement"]
    si = receipt["settlement_instruction"]
    settlement_ok = None
    if si and es and si["feasibility"]["class"] != "deferred":
        expected_class = "collection" if es.get("collection_only") else ("feasible" if es.get("feasible_without_guarantee", True) else "infeasible")
        settlement_ok = si["feasibility"]["class"] == expected_class
    return {"outcome": kind, "covered": covered, "determinate": kind == "determinate", "escalated": kind == "escalated",
            "liable_ok": liable_ok, "remedy_ok": remedy_ok, "consistent": liable_ok and remedy_ok,
            "gt_liable": gt["liable_party"], "gt_remedy_class": gt_rc, "decision_liable": d["liable_party"],
            "decision_remedy_class": receipt["remedy"]["class"] if receipt["remedy"] else None, "settlement_feasibility_matches_expected": settlement_ok,
            "indeterminate_reason": d.get("indeterminate_reason")}


def decidable_at(scenario: dict, version: str) -> str | None:
    """Lowest evidence level at which the engine returns a DETERMINATE outcome equal to the full-evidence one.
    None when the full-evidence outcome is not determinate (no rule applies, or the case is escalated to
    human review). Findings are stipulated (see the module note), so this is the evidence level the rules
    need given correct findings, not a measure of whether that evidence would establish them."""
    full = decide(scenario, version)
    if outcome_kind(full) != "determinate":
        return None
    for lvl in LEVELS:
        r = decide(scenario, version, lvl)
        if outcome_kind(r) == "determinate" and r["decision"]["liable_party"] == full["decision"]["liable_party"] and r["remedy"]["class"] == full["remedy"]["class"]:
            return lvl
    return None

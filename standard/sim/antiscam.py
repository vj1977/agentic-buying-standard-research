"""Anti-scam pre-purchase gate and payout-hold simulation (roadmap family).

Two control configurations run on every anti-scam scenario (class anti_scam plus events tagged
anti_scam): A = no Trust Attestation, immediate payout; B = ABS gate: Trust Attestation consulted
before purchase, Mandate minimum trust, and a payout hold for new or low-trust merchants where a
licensed PSP is the payee (card acquiring, platform collection accounts, A2A acquiring). Funds
credited to a merchant's own account cannot be held (Audit 2 PAY-17); ABS holds no funds. Outcomes are stated per rail and are
disjoint: stopped, refunded (from the held funds, by the merchant, by the rail's reversal, by the agent
provider under ABS-P1), conditional recovery (a PSP-level reimbursement regime outside ABS may pay, but
eligibility is uncertain: never counted as a refund; Audit 1 F25), or unrecoverable; honest merchants:
passed, blocked (false positive) or delayed.

Losses are bounds: buyer_loss_min/max and system_loss_min/max are equal for every outcome except
conditional recovery, where the buyer loses between nothing (the regime pays in full) and the whole
amount (it does not). Amounts are nominal in the scenario's own currency; totals are kept per
currency and never converted or added across currencies.

Assumptions (stated, not measured): the payout hold releases on the delivery evidence bundle plus a
7-day inspection window, so it also covers non-conformity found in that window; "new" means under
180 days; "low trust" means a score under 70; a price under 60% of market triggers a step-up (user
confirmation) rather than a block when the score is at or above the minimum.
"""

from __future__ import annotations

import os
import sys
from collections import Counter

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
from rails import RAILS  # noqa: E402

DEFAULT_MIN_TRUST = 60
NEW_MERCHANT_DAYS = 180
LOW_TRUST = 70
PRICE_STEP_UP_RATIO = 0.6
HOLD_INSPECTION_DAYS = 7
CONFIGS = ("A_no_gate", "B_abs_gate")


def is_antiscam(scenario: dict) -> bool:
    return scenario["class"] == "anti_scam" or "anti_scam" in scenario["tags"]


def gate(scenario: dict, config: str) -> dict:
    """Pre-purchase gate decision under a configuration."""
    f = scenario["facts"]
    t = f["merchant_trust"]
    if config == "A_no_gate":
        return {"consulted": False, "blocked": False, "step_up": False, "reasons": [], "hold": False}
    min_trust = f.get("mandate_min_trust") or DEFAULT_MIN_TRUST
    reasons = []
    if not t["identity_verified"]:
        reasons.append("identity_not_verified")
    if not t["payout_name_match"]:
        reasons.append("payout_name_mismatch")
    if t.get("brand_impersonation"):
        reasons.append("brand_impersonation")
    if t.get("review_authenticity") in ("fake_ring", "copied"):
        reasons.append("review_authenticity_failed")
    if t["score"] < min_trust:
        reasons.append(f"trust_score_{t['score']}_below_min_{min_trust}")
    if not f.get("merchant_participates", True) and f.get("responding_party") != "authority":
        reasons.append("no_register_entry")
    blocked = bool(reasons)
    step_up = (not blocked) and (t.get("price_ratio_to_market", 1.0) < PRICE_STEP_UP_RATIO or t.get("promoted_via_social_ads_burst"))
    wants_hold = (not blocked) and (t["age_days"] < NEW_MERCHANT_DAYS or t["score"] < LOW_TRUST or f.get("settlement_mode") in ("escrow_until_delivery", "delayed"))
    # Audit 2 PAY-17: a hold exists only where the PSP is the payee (card acquiring, platform collection accounts, A2A acquiring).
    hold_possible = f.get("payee_model") == "psp_collection"
    return {"consulted": True, "blocked": blocked, "step_up": step_up, "reasons": reasons, "hold": wants_hold and hold_possible,
            "hold_wanted_but_impossible": wants_hold and not hold_possible, "min_trust": min_trust}


def kind(scenario: dict) -> str:
    """Exactly one of: 'honest' (a legitimate merchant that looks risky), 'scam' (a malicious merchant or a
    third-party attacker that takes the money and does not deliver, delivers counterfeit, or hides behind
    fake reviews), 'other' (an anti-scam-tagged case that is neither, e.g. collusion steering with
    conforming goods). Classified from the parties and the delivery facts, never from the ground truth."""
    tags = set(scenario["tags"])
    f = scenario["facts"]
    if "measure:honest" in tags or "measure:entry_honest" in tags or not f.get("dispute_filed", True):
        return "honest"
    parties = scenario["parties"]
    attacker = parties["merchant"] == "malicious" or parties.get("third_party") == "attacker"
    took_money_no_goods = f.get("delivery_status") in ("not_delivered", "not_performed")
    bad_goods = "counterfeit" in f.get("nonconformity_kinds", []) or "fake_reviews" in tags
    if "measure:scam" in tags or (attacker and (took_money_no_goods or bad_goods)):
        return "scam"
    return "other"


def outcome(scenario: dict, config: str) -> dict:
    f = scenario["facts"]
    g = gate(scenario, config)
    k = kind(scenario)
    honest = k == "honest"
    amount = f["amount"]
    rail = f["rail"]
    reversible = RAILS[rail]["reversible"]
    res = {"config": config, "rail": rail, "rail_family": RAILS[rail]["family"], "kind": k, "scam": k == "scam", "honest": honest, "gate": g, "amount": amount,
           "currency": scenario.get("currency", "EUR"), "result": None, "buyer_loss_min": 0.0, "buyer_loss_max": 0.0, "system_loss_min": 0.0, "system_loss_max": 0.0,
           "delay_days": 0, "notes": []}

    def loss(buyer=0.0, system=0.0, buyer_max=None, system_max=None):
        res.update({"buyer_loss_min": buyer, "buyer_loss_max": buyer if buyer_max is None else buyer_max,
                    "system_loss_min": system, "system_loss_max": system if system_max is None else system_max})

    if k == "other":
        res["result"] = "other_blocked_by_gate" if g["blocked"] else "other_passed_gate_decided_by_abs_rules"
        res["notes"].append("not a non-delivery/counterfeit scam (e.g. collusion steering with conforming goods); liability is decided by the ABS rules, not by the gate")
        return res
    if honest:
        if g["blocked"]:
            res["result"] = "honest_blocked_false_positive"
        elif g["hold"]:
            res["result"] = "honest_delayed_payout"
            res["delay_days"] = 5 + HOLD_INSPECTION_DAYS
        elif g["step_up"]:
            res["result"] = "honest_passed_with_step_up"
        else:
            res["result"] = "honest_passed"
        return res
    if g["blocked"]:
        res["result"] = "scam_stopped_before_purchase"
        return res
    # the purchase happened
    hold = g["hold"] or (config == "A_no_gate" and f.get("settlement_mode") in ("escrow_until_delivery", "delayed") and False)
    merchant_present = f.get("merchant_reachable", True) and f.get("merchant_solvent", True)
    off_platform = not f.get("credential_bound_to_mandate", True)
    if off_platform:
        res["result"] = "unrecoverable_off_platform_payment" if not reversible else "refunded_by_rail_reversal"
        loss(buyer=0.0 if reversible else amount)
        res["notes"].append("payment outside the mandate-bound credential: no Purchase Record, no hold; agent provider liable under ABS-P1")
        if not reversible:
            res["result"] = "refunded_by_agent_provider_ABS-P1"
            loss(buyer=0.0, system=amount)
        return res
    if hold:
        res["result"] = "refunded_from_payee_psp_hold"
        res["notes"].append("payout held by the payee PSP (acquiring / collection-account model) until delivery evidence + inspection window")
        return res
    if g.get("hold_wanted_but_impossible"):
        res["notes"].append("a hold was wanted but the funds reach the merchant's own account (merchant-account model): no hold possible")
    if merchant_present:
        res["result"] = "refunded_by_merchant_participation_obligation"
        return res
    if reversible:
        res["result"] = "refunded_by_rail_reversal_loss_to_acquirer"
        loss(system=amount)
        return res
    if rail == "uk_fps":
        res["result"] = "conditional_recovery_psp_reimbursement_uncertain"
        res["notes"].append("UK APP reimbursement is a PSP-level regime outside ABS; whether it covers an agent-initiated payment, and its conditions, excess and cap, are uncertain; "
                            "if it pays, the loss moves to the PSPs; if not, the buyer bears it")
        loss(buyer=0.0, buyer_max=amount, system=0.0, system_max=amount)
        return res
    res["result"] = "unrecoverable_buyer_loss"
    loss(buyer=amount)
    return res


OUTCOME_PREFIXES = (("scam_stopped", "stopped"), ("refunded", "refunded"), ("conditional_recovery", "conditional"), ("unrecoverable", "unrecoverable"))


def scam_outcome(result: str) -> str:
    """Map a scam row's result to exactly one of stopped / refunded / conditional / unrecoverable."""
    hits = [cat for prefix, cat in OUTCOME_PREFIXES if result.startswith(prefix)]
    assert len(hits) == 1, f"scam result {result!r} must map to exactly one outcome category"
    return hits[0]


def _by_currency(rows: list[dict], field: str) -> dict:
    out: dict = {}
    for r in rows:
        if r[field]:
            out[r["currency"]] = round(out.get(r["currency"], 0.0) + r[field], 2)
    return dict(sorted(out.items()))


def run(scenarios: list[dict]) -> dict:
    rows = []
    for s in scenarios:
        if not is_antiscam(s):
            continue
        for cfg in CONFIGS:
            o = outcome(s, cfg)
            o["scenario_id"] = s["id"]
            o["event"] = s["event"]
            rows.append(o)
    summary = {}
    for cfg in CONFIGS:
        sub = [r for r in rows if r["config"] == cfg]
        scams = [r for r in sub if r["kind"] == "scam"]
        hon = [r for r in sub if r["kind"] == "honest"]
        other = [r for r in sub if r["kind"] == "other"]
        assert len(scams) + len(hon) + len(other) == len(sub), "anti-scam kinds must partition the rows"
        cats = Counter(scam_outcome(r["result"]) for r in scams)
        assert sum(cats.values()) == len(scams), "scam outcomes must partition the scam rows"
        by_rail = {}
        for fam in sorted({r["rail_family"] for r in scams}):
            fr = [r for r in scams if r["rail_family"] == fam]
            fc = Counter(scam_outcome(r["result"]) for r in fr)
            by_rail[fam] = {"scams": len(fr), "stopped": fc["stopped"], "refunded": fc["refunded"], "conditional": fc["conditional"], "unrecoverable": fc["unrecoverable"],
                            **{f"{f}_by_currency": _by_currency(fr, f) for f in ("buyer_loss_min", "buyer_loss_max", "system_loss_min", "system_loss_max")}}
        summary[cfg] = {
            "total_rows": len(sub),
            "scams": len(scams),
            "stopped": cats["stopped"],
            "refunded": cats["refunded"],
            "conditional": cats["conditional"],
            "unrecoverable": cats["unrecoverable"],
            **{f"{f}_by_currency": _by_currency(scams, f) for f in ("buyer_loss_min", "buyer_loss_max", "system_loss_min", "system_loss_max")},
            "honest": len(hon),
            "honest_blocked": sum(1 for r in hon if r["result"] == "honest_blocked_false_positive"),
            "honest_delayed": sum(1 for r in hon if r["result"] == "honest_delayed_payout"),
            "honest_step_up": sum(1 for r in hon if r["result"] == "honest_passed_with_step_up"),
            "honest_passed_clean": sum(1 for r in hon if r["result"] == "honest_passed"),
            "other": len(other),
            "by_rail_family": by_rail,
            "results_scams": dict(sorted(Counter(r["result"] for r in scams).items())),
            "results_honest": dict(sorted(Counter(r["result"] for r in hon).items())),
            "results_other": dict(sorted(Counter(r["result"] for r in other).items())),
        }
        assert sum(summary[cfg]["results_scams"].values()) == len(scams)
        assert summary[cfg]["honest_blocked"] + summary[cfg]["honest_delayed"] + summary[cfg]["honest_step_up"] + summary[cfg]["honest_passed_clean"] == len(hon)
    return {"rows": rows, "summary": summary}

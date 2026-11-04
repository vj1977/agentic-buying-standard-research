"""Deterministic ABS rule engine (arbiter architecture A2).

Typed findings in, Decision plus Settlement Instruction plus signed receipt out. No model call on
the decision path. The engine applies the rulebook's decision order. Like the Menime engine's
authorizer mode, it fails safe: if a finding a step needs is unknown, it returns
verdict "review" (needs a human) instead of guessing.

Rulebook versions (rulebook/VERSIONS.md):
  * "1.2" (default): the rulebook every historical A2 run used (Phases 2 and 3). Its findings
    schema has no authorisation, deceptive-offer or capture-failure finding, so the default stays
    1.2 to keep stored results reproducible; v1.2 cannot emit AG0, AG4-D or AG1-C.
  * "1.3": v1.2 plus AG1-C (the capture-duty arm). No A2 run used it.
  * "1.4": the core frozen after Audit 1 (ABS v0.3 A4, A4.4, A6). It can emit every core
    code (AG0, AG3, AG4, AG4-D, AG1-M, AG1-P, AG1-C, AG2, AG5), applies the corrected withdrawal
    overlay (missing prerequisite = 'undetermined', never 'deny') and the Audit 2 settlement
    mapping (no ABS chargeback, no recall). Unchanged; the rule of the expert kit. No model has been run under it.
  * "1.5": the current core (founder ruling 2, 2026-11-04): v1.4 plus ABS-V1, the tiered burden of proof for
    merchant-performance claims (ABS v0.3 A4.1 Step 1 and A5.7). A non-delivery or non-conformity claim that no
    record with independent authority decides is decided against a merchant that answered only with its own
    records when the order value is at or below the published threshold and the buyer is under the per-buyer cap;
    otherwise it goes to review, as in v1.4. Never for authorisation (Step 0) or agent-instruction disputes. The
    threshold and cap are programme parameters (`burden_params`); their defaults are a design proposal. No model
    has been run under it.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
from datetime import date

from .marketplace import canonical, sha256_hex
from .scenarios import ROOT

RULEBOOK_FILES = {"1.2": "AGENTIC_DISPUTE_RULEBOOK.json", "1.3": "AGENTIC_DISPUTE_RULEBOOK_v1.3.json", "1.4": "AGENTIC_DISPUTE_RULEBOOK_v1.4.json",
                  "1.5": "AGENTIC_DISPUTE_RULEBOOK_v1.5.json"}
def _load(name: str) -> dict:
    with open(os.path.join(ROOT, "rulebook", name), encoding="utf-8") as fh:
        return json.load(fh)


RULEBOOKS = {v: _load(f) for v, f in RULEBOOK_FILES.items()}
HISTORICAL = "1.2"
CURRENT = "1.5"
CORE = ("1.4", "1.5")  # rulebooks with the v1.4 core: Step 0, AG4-D, AG1-C, withdrawal prerequisites, Audit 2 settlement
RULEBOOK = RULEBOOKS[HISTORICAL]
ENGINE_VERSION = f"abs-rules/{RULEBOOK['version']}"
_RECEIPT_KEY = b"simulated-arbiter-receipt-key"  # simulation only (the Menime engine signs with Ed25519)

CRITICAL = ("delivery_status", "conformity", "injection_present", "items_added_by_merchant", "agent_fault")
# v1.4 adds the authorisation (Step 0), deceptive-offer (AG4-D) and capture-failure (AG1-C) findings.
CRITICAL_V14 = ("authorisation",) + CRITICAL[:3] + ("deceptive_offer",) + CRITICAL[3:] + ("capture_failure",)
AUTHORISATION_VALUES = ("valid", "invalid_mandate", "issued_by_provider_without_mandate", "charged_by_merchant_outside_mandate")
V14_CODES = ("AG0", "AG3", "AG4", "AG4-D", "AG1-M", "AG1-P", "AG1-C", "AG2", "AG5")
V14_PARTIES = ("merchant", "agent_provider", "buyer", "rail_process")
V14_REMEDIES = ("refund", "withdrawal", "deny", "undetermined", "refer_to_payer_psp")
TIER_CLAIMS = ("non_delivery", "non_conformity")  # ABS-V1 scope (v1.5): merchant-performance claims decided at Step 1
TIER_PARAMETERS = ("low_value_threshold", "cap_per_buyer", "cap_window_days")


def _valid_interval(meta: dict) -> int | None:
    """Days from delivery to dispute, or None if a date is missing, not an ISO date, or the dispute precedes delivery."""
    try:
        delivered = date.fromisoformat(str(meta["delivered_on"]))
        filed = date.fromisoformat(str(meta["dispute_date"]))
    except (KeyError, TypeError, ValueError):
        return None
    days = (filed - delivered).days
    return days if days >= 0 else None


def withdrawal_open_v12(meta: dict) -> bool | None:
    """The overlay as executed in every historical run (v1.2): digital content and custom goods always excluded.
    Kept for reproducibility only; Audit 1 F12 found it drops the Art 16(m) conditions. Dates are now validated
    (a negative interval used to count as 'within 14 days'); no stored case has an invalid or negative interval."""
    kind = meta.get("goods_kind")
    if kind in ("digital_content", "custom_goods"):
        return False
    if not meta.get("delivered_on") or not meta.get("dispute_date"):
        return None
    days = _valid_interval(meta)
    if days is None:
        return None
    return days <= RULEBOOKS["1.2"]["withdrawal_right"]["period_days_from_delivery"]


def _buyer_scope(meta: dict) -> tuple[str | None, str | None]:
    """(buyer type, jurisdiction) from explicit fields or the transaction's 'buyer' string, e.g. 'consumer, EU'."""
    btype, juris = meta.get("buyer_type"), meta.get("jurisdiction")
    text = str(meta.get("buyer") or "").lower()
    if btype is None and text:
        btype = "consumer" if "consumer" in text else ("business" if "business" in text else None)
    if juris is None and text:
        parts = [p.strip() for p in text.replace(";", ",").split(",")]
        juris = "EU" if "eu" in parts else (parts[-1].upper() if len(parts) > 1 and parts[-1] else None)
    return btype, juris


def withdrawal_status(meta: dict) -> tuple[bool | None, list[str]]:
    """v1.4 overlay (ABS v0.3 A4.4): True = available, False = not available, None = unresolved, with the reasons.
    A missing prerequisite is unresolved, never 'not available'."""
    btype, juris = _buyer_scope(meta)
    if btype == "business":
        return False, ["business purchase: no withdrawal right"]
    scope = []
    if btype != "consumer":
        scope.append("buyer type not established as consumer")
    if juris is None:
        scope.append("jurisdiction not established")
    elif juris != "EU":
        scope.append(f"jurisdiction {juris}: outside the EU overlay (national law)")
    if scope:
        return None, scope
    kind = meta.get("goods_kind")
    flags = meta.get("withdrawal_flags") or {}
    if kind == "custom_goods":
        return False, ["goods made to the consumer's specification (CRD Art 16(c))"]
    for flag, why in (("sealed_hygiene_unsealed", "sealed hygiene goods unsealed after delivery (Art 16(e))"),
                      ("sealed_media_unsealed", "sealed audio, video or software unsealed after delivery (Art 16(i))"),
                      ("dated_service", "service for a specific date or period (Art 16(l))")):
        if flags.get(flag) is True:
            return False, [why]
    consent_gap = None
    if kind == "digital_content":
        # Art 16(m) (ABS v0.3 A4.4): the exception applies once performance has begun AND the three consents are recorded
        # (Audit 3 re-check, F12 remainder: the performance condition was missing, so the consents alone removed the right).
        consent = meta.get("digital_consent") or {}
        names = ("performance_begun", "prior_express_consent", "acknowledged_loss_of_right", "trader_confirmation")
        parts = [consent.get(k, meta.get(k)) if k == "performance_begun" else consent.get(k) for k in names]
        if all(p is True for p in parts):
            return False, ["digital content: performance has begun, with prior express consent, acknowledgement and trader confirmation recorded (Art 16(m))"]
        if not any(p is False for p in parts):
            consent_gap = "digital content: Art 16(m) prerequisite(s) not in the record: " + ", ".join(k for k, p in zip(names, parts) if p is not True)
        # any one recorded false (performance not begun, or a consent refused): the exception does not apply and the window decides
    if not meta.get("delivered_on") or not meta.get("dispute_date"):
        return None, ["delivery or dispute date missing"] + ([consent_gap] if consent_gap else [])
    days = _valid_interval(meta)
    if days is None:
        return None, [f"invalid dates (delivered {meta.get('delivered_on')}, filed {meta.get('dispute_date')}): not ISO dates, or the dispute precedes delivery"]
    if days > RULEBOOKS["1.4"]["withdrawal_right"]["period_days_from_delivery"]:
        return False, [f"{days} days from delivery: window expired"]
    if consent_gap:
        return None, [consent_gap, f"{days} days from delivery"]
    return True, [f"{days} days from delivery, consumer, EU"]


def withdrawal_open(meta: dict, rulebook: str = CURRENT) -> bool | None:
    """Availability of the statutory withdrawal right under the given rulebook (v1.4 corrected by default)."""
    if rulebook in ("1.2", "1.3"):
        return withdrawal_open_v12(meta)
    return withdrawal_status(meta)[0]


def _val(findings: dict, name: str):
    f = findings.get(name)
    return None if f is None else f.get("value")


def nonconforming_attributes(findings: dict) -> list[dict]:
    return [a for a in findings.get("conformity", []) if a.get("conforms") is False]


def conformity_known(findings: dict, relaxed: bool = False) -> bool:
    attrs = findings.get("conformity", [])
    if relaxed:
        # Post-hoc sensitivity rule: unknown attributes do not block if at least 3 attributes are known to conform.
        return sum(1 for a in attrs if a.get("conforms") is True) >= 3
    return bool(attrs) and all(a.get("conforms") is not None for a in attrs)


# ---- ABS-V1, the tiered burden of proof (rulebook v1.5) ------------------------------------------------------
def burden_parameters(rulebook: str = CURRENT, overrides: dict | None = None) -> dict:
    """The programme parameters of ABS-V1: the rulebook's published defaults with a programme's overrides.
    low_value_threshold: {currency: order value at or below which the low-value tier applies}; cap_per_buyer: ABS-V1
    refunds per buyer identity per window; cap_window_days. An unknown key or an invalid value raises ValueError."""
    rb = RULEBOOKS[rulebook]
    if "burden_tiers" not in rb:
        raise ValueError(f"rulebook {rulebook} has no tiered burden of proof (ABS-V1 is v1.5)")
    base = rb["burden_tiers"]["programme_parameters"]
    params = {k: base[k] for k in TIER_PARAMETERS}
    for k, v in (overrides or {}).items():
        if k not in TIER_PARAMETERS:
            raise ValueError(f"unknown ABS-V1 parameter {k!r}; known: {list(TIER_PARAMETERS)}")
        params[k] = v
    thr = params["low_value_threshold"]
    if not isinstance(thr, dict) or not all(isinstance(c, str) and _amount(v) is not None for c, v in thr.items()):
        raise ValueError(f"low_value_threshold must map currency codes to non-negative amounts, not {thr!r}")
    for k in ("cap_per_buyer", "cap_window_days"):
        if _count(params[k]) is None:
            raise ValueError(f"{k} must be a non-negative integer, not {params[k]!r}")
    return params


def _amount(v) -> float | None:
    """A finite, non-negative JSON number, else None."""
    if isinstance(v, bool) or not isinstance(v, (int, float)) or v != v or v in (float("inf"), float("-inf")) or v < 0:
        return None
    return float(v)


def _count(v) -> int | None:
    return v if isinstance(v, int) and not isinstance(v, bool) and v >= 0 else None


_AGENT_NAMED = re.compile(r"\b(?:the|my|our) (?:ai |shopping |buying )?agent\b")


def burden_scope(claim_type: str | None, claim_text: str | None, bundle: dict | None = None) -> dict:
    """Is the claim a merchant-performance claim ABS-V1 covers? {"in_scope", "kinds", "attributes", "why"}.
    In scope: non-delivery or non-conformity and nothing else. The filed claim type decides the kind; the claim text, when
    present, is read with the gate v3 allegation reader and must allege nothing outside Step 1 (an agent-instruction,
    capture, authorisation or Step 2 allegation takes the claim out of scope, and so does a claim that names the agent as
    the actor: the reader is keyword-based, so it errs towards v1.4). No claim type and no text: out of scope."""
    from .provenance import allegations, item_titles
    al = allegations(claim_text, item_titles(bundle or {}), "v3") if claim_text else None
    found = al["allegations"] if al else []
    if claim_type is not None:
        kinds = [claim_type] if claim_type in TIER_CLAIMS else []
        if not kinds:
            return {"in_scope": False, "kinds": [], "attributes": [], "why": f"claim type {claim_type!r} is not a non-delivery or non-conformity claim"}
    elif al is not None:
        kinds = [a for a in TIER_CLAIMS if a in found]
    else:
        return {"in_scope": False, "kinds": [], "attributes": [], "why": "no claim type and no claim text: scope unknown"}
    others = sorted(a for a in found if a not in TIER_CLAIMS + ("unknown",))
    if claim_text and _AGENT_NAMED.search(claim_text.lower()):
        others.append("the agent's conduct (the claim names the agent)")  # e.g. "The agent bought a refurbished unit": an instruction dispute
    if not kinds or others:
        why = ("the claim also alleges " + ", ".join(others) + ": ABS-V1 never applies to an agent-instruction, capture, authorisation or "
               "Step 2 dispute") if others else "the claim alleges neither non-delivery nor non-conformity"
        return {"in_scope": False, "kinds": kinds, "attributes": [], "why": why}
    return {"in_scope": True, "kinds": kinds, "attributes": (al or {}).get("attributes") or [], "why": "non-delivery or non-conformity claim: " + ", ".join(kinds)}


def step1_support(flat_findings: list[dict], scope: dict, bundle: dict | None = None, disputed_items: list | None = None) -> dict:
    """Which side a record with independent authority supports on the Step 1 facts the claim contests.
    flat_findings: [{"finding", "value", "evidence"}] (`acs.provenance.findings_from_a2` of A2 findings). With the evidence
    package the cited record's content is read (gate v3 readers: a record that contradicts a finding supports the other
    side); without it only the record's type, provenance and relevance count (gate v1). A merchant-favourable finding counts
    only for the contested fact: 'delivered' for non-delivery (never for content), the contested attributes for
    non-conformity (any attribute when the claim names none). Returns {"merchant": [...], "buyer": [...], "method"}."""
    from .provenance import ATTRIBUTE_CUES_V3, _typed, check_finding, corroborated, finding_key
    members = {m for name, _, ms in ATTRIBUTE_CUES_V3 if name in (scope.get("attributes") or []) for m in ms}
    if bundle is not None:
        disputed = list(disputed_items) if disputed_items else sorted(((bundle.get("delivery_evidence") or {}).get("by_product") or {}).keys()) or \
            [o.get("product_id") for o in bundle.get("offer_snapshots_at_checkout") or []]
    out = {"merchant": [], "buyer": [], "method": "content check (gate v3 record readers)" if bundle is not None else "record type and provenance (gate v1)"}
    for f in flat_findings or []:
        key = finding_key(f.get("finding"))
        value = _typed(key, f.get("value"))
        evidence = [e for e in (f.get("evidence") or []) if str(e).strip()]
        if value is None or not evidence:
            continue
        if key == "delivery_status":
            kind, side = "non_delivery", ("merchant" if value == "delivered" else "buyer")
        elif key.startswith("conformity:"):
            kind, side = "non_conformity", ("merchant" if value is True else "buyer")
            if side == "merchant" and members and key.split(":", 1)[1] not in members:
                continue  # the merchant's support must speak to the attribute the claim contests
        else:
            continue
        if kind not in scope.get("kinds", ()):
            continue
        if bundle is not None:
            status = check_finding({"finding": key, "value": value, "evidence": evidence}, bundle, disputed, "v3")["status"]
        else:
            status = "supported" if corroborated(key, evidence) else "unsupported"
        if status == "supported":
            out[side].append({"kind": kind, "finding": key, "value": value})
        elif status == "contradicted":
            out["buyer" if side == "merchant" else "merchant"].append({"kind": kind, "finding": key, "value": value, "by": "contradiction"})
    # the merchant is supported only if every contested kind has a supporting record (a non-delivery and a content claim both need one)
    if out["merchant"] and not all(any(m["kind"] == k for m in out["merchant"]) for k in scope.get("kinds", ())):
        out["merchant_partial"], out["merchant"] = out["merchant"], []
    return out


def burden_tier(order_value, currency: str | None, prior_refunds, params: dict) -> dict:
    """{"tier": low_value | high_value | cap_reached | unknown, "why", and the inputs}. Fail safe: a missing input is 'unknown',
    which takes the high-value path."""
    value, prior = _amount(order_value), _count(prior_refunds)
    thr = (params["low_value_threshold"] or {}).get(currency)
    cap, window = params["cap_per_buyer"], params["cap_window_days"]
    info = {"order_value": value, "currency": currency, "threshold": thr, "cap_per_buyer": cap, "cap_window_days": window,
            "prior_refunds_in_window": prior}
    if value is None:
        return {**info, "tier": "unknown", "why": "the order value is not in the record"}
    if thr is None:
        return {**info, "tier": "high_value", "why": f"no low-value threshold is published for {currency}"}
    if value > thr:
        return {**info, "tier": "high_value", "why": f"order value {currency} {value:.2f} is above the threshold {thr:.2f}"}
    if prior is None:
        return {**info, "tier": "unknown", "why": "the payer PSP's count of the buyer's earlier ABS-V1 refunds is not in the record"}
    if prior >= cap:
        return {**info, "tier": "cap_reached", "why": f"the buyer has had {prior} ABS-V1 refunds in {window} days; the cap is {cap}"}
    return {**info, "tier": "low_value", "why": f"order value {currency} {value:.2f} at or below {thr:.2f}; the buyer's ABS-V1 refunds in {window} days: {prior} of {cap}"}


def decide(findings: dict, case_meta: dict, relaxed: bool = False, provenance_gate: bool | str = False, claim_type: str | None = None,
           rulebook: str = HISTORICAL, bundle: dict | None = None, claim_text: str | None = None, disputed_items: list | None = None,
           burden_params: dict | None = None) -> dict:
    """findings: typed findings (see acs.hybrid.FINDINGS_SCHEMA; v1.4 adds authorisation, deceptive_offer, capture_failure).
    case_meta: rail, disputed_amount, withdrawal facts. rulebook: '1.2' (historical default), '1.3', '1.4' or '1.5' (current core).
    v1.5 (ABS-V1) also reads case_meta 'order_value' (default: the package's transaction amount), 'currency' (default: the
    package's, else EUR, the engine's one settlement currency) and 'buyer_low_value_refunds_in_window' (the payer PSP's count of
    the buyer's earlier ABS-V1 refunds in the cap window; missing = unknown = the high-value path); claim_type ('non_delivery',
    'non_conformity', ...) or the claim text decides the scope; burden_params overrides the published threshold and cap.
    provenance_gate (Amendment 14): a decided verdict whose decisive finding rests only on party-authored evidence becomes review.
      "v2": gate v2 (Audit 1 F05/F06, acs/provenance.gate_v2): needs the evidence package (bundle) and the claim text
      (default: the package's buyer claim); it resolves cited paths in the package and checks every denied allegation.
      "v3" or True with a package: gate v3 (Audit 3 N03 and F05 remainder, acs/provenance.gate_v3; v2 reproduces Audit 1).
      "v1": the gate as run in Phase 3b (claim_type only, no package). True without a package falls back to v1, so the
      stored Phase 3b recomputation (which passes no package) replays exactly; the trace names the version used."""
    rb = RULEBOOKS[rulebook]
    codes = rb["reason_codes"]
    v14 = rulebook in CORE
    v15 = "burden_tiers" in rb
    params = burden_parameters(rulebook, burden_params) if v15 else None
    if burden_params and not v15:
        raise ValueError(f"burden_params need a rulebook with ABS-V1 (v1.5), not {rulebook}")
    trace = []

    def outcome(code: str, why: str, used: list[str], liable: str | None = None, extra: dict | None = None) -> dict:
        rc = codes[code]
        trace.append({"rule": code, "fired": True, "because": why, "findings_used": used})
        remedy = rc["remedy"]
        party = liable or rc["liable"]
        if v14:
            wd, reasons = withdrawal_status(case_meta)
        else:
            wd, reasons = withdrawal_open_v12(case_meta), []
        if code == "AG0":
            remedy = "refer_to_payer_psp" if party == "rail_process" else "refund"
        if remedy == "deny_or_withdrawal":
            if v14:
                remedy = "withdrawal" if wd is True else ("deny" if wd is False else "undetermined")
                trace.append({"rule": "withdrawal_overlay", "fired": True,
                              "because": f"withdrawal {'open' if wd is True else 'not available' if wd is False else 'unresolved (escalated to a human)'}: " + "; ".join(reasons),
                              "findings_used": ["structured:goods_kind", "structured:delivered_on", "structured:dispute_date", "structured:buyer", "structured:digital_consent"]})
            else:
                if wd is None:
                    trace.append({"rule": "withdrawal_overlay", "fired": True, "because": "delivery date unknown; withdrawal treated as not established", "findings_used": ["structured:delivered_on"]})
                remedy = "withdrawal" if wd else "deny"
                trace.append({"rule": "withdrawal_overlay", "fired": True, "because": f"goods {case_meta.get('goods_kind')}, delivered {case_meta.get('delivered_on')}, filed {case_meta.get('dispute_date')}: withdrawal {'open' if wd else 'not available'}",
                              "findings_used": ["structured:goods_kind", "structured:delivered_on", "structured:dispute_date"]})
        if v14:
            return {"verdict": "decided", "reason_code": code, "liable_party": party, "remedy": remedy, "withdrawal_available": wd, **(extra or {})}
        return {"verdict": "decided", "reason_code": code, "liable_party": party, "remedy": remedy, "withdrawal_available": bool(wd)}

    def review(why: str, used: list[str], extra: dict | None = None) -> dict:
        trace.append({"rule": "review", "fired": True, "because": why, "findings_used": used})
        return {"verdict": "review", "reason_code": None, "liable_party": None, "remedy": None, **(extra or {})}

    def abs_v1() -> dict | None:
        """ABS-V1 (v1.5) at Step 1: None when it does not decide (out of scope, or a record with independent authority decides
        the contested fact), else the low-value refund or the high-value review."""
        text = claim_text if claim_text is not None else (((bundle or {}).get("buyer_claim") or {}).get("text") or None)
        scope = burden_scope(claim_type, text, bundle)
        if not scope["in_scope"]:
            trace.append({"rule": "ABS-V1", "fired": False, "because": "out of scope: " + scope["why"], "findings_used": []})
            return None
        from .provenance import findings_from_a2
        sup = step1_support(findings_from_a2(findings), scope, bundle, disputed_items)
        contested = ["delivery_status"] * ("non_delivery" in scope["kinds"]) + ["conformity"] * ("non_conformity" in scope["kinds"])
        if sup["merchant"]:
            trace.append({"rule": "ABS-V1", "fired": False, "because": "a record with independent authority supports the merchant on " +
                          ", ".join(sorted({m["finding"] for m in sup["merchant"]})) + f" ({sup['method']}): decided on the evidence as in v1.4",
                          "findings_used": contested})
            return None
        status = _val(findings, "delivery_status")
        if sup["buyer"] and (status == "not_delivered" or nonconforming_attributes(findings)):
            trace.append({"rule": "ABS-V1", "fired": False, "because": "a record with independent authority supports the buyer's claim on " +
                          ", ".join(sorted({b["finding"] for b in sup["buyer"]})) + f" ({sup['method']}): decided on the evidence as in v1.4",
                          "findings_used": contested})
            return None
        tx = (bundle or {}).get("transaction") or {}
        value = case_meta.get("order_value", tx.get("amount"))
        currency = case_meta.get("currency") or tx.get("currency") or "EUR"
        tier = burden_tier(value, currency, case_meta.get("buyer_low_value_refunds_in_window"), params)
        used = contested + ["structured:order_value", "structured:currency", "structured:buyer_low_value_refunds_in_window"]
        trace.append({"rule": "ABS-V1", "fired": True, "because": f"no record with independent authority for the contested fact supports the merchant "
                      f"({sup['method']}); {tier['why']}: {tier['tier'].replace('_', ' ')}", "findings_used": used})
        if tier["tier"] == "low_value":
            return outcome("AG3", "ABS-V1 low-value tier: the merchant answered only with records it wrote itself, so it refunds; the contested "
                           "fact is not found", used, extra={"burden_tier": tier, "confirmation_route": "low_value_burden"})
        return review(f"ABS-V1 {'cap reached' if tier['tier'] == 'cap_reached' else 'high-value path'}: human review or an independent "
                      "inspection request", used, extra={"burden_tier": tier, "review_route": "human_review_or_independent_inspection"})

    def step3b_and_4() -> dict:
        if "AG1-C" in codes:
            cap = _val(findings, "capture_failure")
            if cap is None and _val(findings, "conversation_record_produced") is False and _val(findings, "stated_requirement_alleged") is True:
                return outcome("AG1-C", "the buyer alleges a requirement stated to the agent and the agent provider cannot produce the conversation record (ABS-E1)",
                               ["conversation_record_produced", "stated_requirement_alleged"])
            if cap is True:
                return outcome("AG1-C", "the user stated an explicit requirement the agent did not capture into the mandate, and the purchase misses it", ["capture_failure"])
            if cap is None:
                return review("whether a stated requirement went uncaptured is unknown", ["capture_failure"])
            trace.append({"rule": "AG1-C", "fired": False, "because": "no stated requirement went uncaptured", "findings_used": ["capture_failure"]})
        intent = _val(findings, "matches_buyer_intent")
        if intent is False:
            return outcome("AG2", "inside the mandate but not what the buyer meant", ["matches_buyer_intent"])
        return outcome("AG5", "the purchase matches the mandate and recorded intent", ["matches_buyer_intent", "claim_contradicted_by_evidence"])

    def steps_1_to_4() -> dict:
        # Step 1: conformity to the frozen offer; v1.5 first applies ABS-V1 to a claim no independent record decides.
        if v15:
            tiered = abs_v1()
            if tiered is not None:
                return tiered
        status = _val(findings, "delivery_status")
        nc = nonconforming_attributes(findings)
        if status == "not_delivered":
            return outcome("AG3", "the delivery record shows no delivery", ["delivery_status"])
        if nc:
            return outcome("AG3", "delivered item deviates from the frozen offer on: " + ", ".join(a["attribute"] for a in nc),
                           [f"conformity.{a['attribute']}" for a in nc])
        if status is None or not conformity_known(findings, relaxed):
            return review("conformity cannot be established from the findings", ["delivery_status", "conformity"])
        trace.append({"rule": "AG3", "fired": False, "because": "delivered and every offered attribute conforms",
                      "findings_used": ["delivery_status", "conformity"]})
        # Step 2: manipulative offer.
        inj, added = _val(findings, "injection_present"), _val(findings, "items_added_by_merchant")
        deceptive = _val(findings, "deceptive_offer") if "AG4-D" in codes else False
        if inj is True:
            return outcome("AG4", "the agent followed instructions in merchant-controlled content", ["injection_present"])
        if deceptive is True:
            return outcome("AG4-D", "a statement of fact in merchant content was false and influenced the choice", ["deceptive_offer"])
        if added is True:
            return outcome("AG1-M", "the merchant added or pre-selected the disputed items or fees", ["items_added_by_merchant"])
        if inj is None or added is None or deceptive is None:
            return review("whether the offer was manipulative is unknown", ["injection_present", "items_added_by_merchant"] + (["deceptive_offer"] if "AG4-D" in codes else []))
        trace.append({"rule": "AG4/AG1-M" if "AG4-D" not in codes else "AG4/AG4-D/AG1-M", "fired": False, "because": "no injection and no merchant-added items" + ("" if "AG4-D" not in codes else " and no deceptive offer content"),
                      "findings_used": ["injection_present", "items_added_by_merchant"] + (["deceptive_offer"] if "AG4-D" in codes else [])})
        # Step 3: agent fault on the record.
        fault = _val(findings, "agent_fault")
        if fault is True:
            return outcome("AG1-P", "the record shows the agent broke an explicit mandate or Allowance term or explicit instruction", ["agent_fault"])
        if fault is None:
            return review("whether the record shows agent fault is unknown", ["agent_fault"])
        trace.append({"rule": "AG1-P", "fired": False, "because": "no agent fault on the record",
                      "findings_used": ["agent_fault"]})
        # Step 3b (v1.3, v1.4) and Step 4: capture failure, then the buyer side.
        return step3b_and_4()

    if "AG0" in codes:
        auth = _val(findings, "authorisation")
        if auth is None:
            dec = review("whether the charge was made under a valid mandate is unknown", ["authorisation"])
        elif auth not in AUTHORISATION_VALUES:
            dec = review(f"authorisation finding {auth!r} is not one of {list(AUTHORISATION_VALUES)}", ["authorisation"])
        elif auth != "valid":
            party = codes["AG0"]["liable_variants"][auth]
            dec = outcome("AG0", f"authorisation: {auth}", ["authorisation"], liable=party)
        else:
            trace.append({"rule": "AG0", "fired": False, "because": "the charge was made under a valid mandate", "findings_used": ["authorisation"]})
            dec = steps_1_to_4()
    else:
        dec = steps_1_to_4()
    gate_version = None
    if provenance_gate:
        if provenance_gate not in (True, "v1", "v2", "v3"):
            raise ValueError(f"provenance_gate must be True, 'v1', 'v2' or 'v3', not {provenance_gate!r}")
        gate_version = provenance_gate if provenance_gate in ("v1", "v2", "v3") else ("v3" if bundle is not None else "v1")
        if gate_version in ("v2", "v3") and bundle is None:
            raise ValueError(f"provenance gate {gate_version} needs the evidence package (bundle=...)")
    if gate_version and dec["verdict"] == "decided" and dec.get("confirmation_route") == "low_value_burden":
        trace.append({"rule": f"provenance_gate_{gate_version}", "fired": False, "because": "not applicable: ABS-V1 is a burden-of-proof default, "
                      "not a Finding resting on evidence (ABS v0.3 A5.7)", "findings_used": []})
    elif gate_version == "v1" and dec["verdict"] == "decided":
        from .provenance import findings_from_a2, gate as provenance_check
        g = provenance_check(dec["reason_code"], findings_from_a2(findings), claim_type)
        if g["verdict"] == "review":
            trace.append({"rule": "provenance_gate", "fired": True, "because": g["reason"], "findings_used": [f["finding"] for f in g["decisive"]] or ["(none cited)"]})
            dec = {"verdict": "review", "reason_code": None, "liable_party": None, "remedy": None, "gate": g["rule"], "pre_gate": dec}
        else:
            trace.append({"rule": "provenance_gate", "fired": False, "because": g["reason"], "findings_used": [f["finding"] for f in g["decisive"]]})
    elif gate_version in ("v2", "v3") and dec["verdict"] == "decided":
        from .provenance import findings_from_a2, gate_v2, gate_v3
        text = claim_text if claim_text is not None else ((bundle.get("buyer_claim") or {}).get("text") or "")
        g = (gate_v3 if gate_version == "v3" else gate_v2)(dec["reason_code"], findings_from_a2(findings), text, bundle, disputed_items)
        used = sorted({c.get("finding") or c.get("for") for c in g["checks"] if c.get("finding") or c.get("for")}) or ["(none cited)"]
        if g["verdict"] == "review":
            trace.append({"rule": f"provenance_gate_{gate_version}", "fired": True, "because": f"{g['category']}: {g['reason']}", "findings_used": used})
            dec = {"verdict": "review", "reason_code": None, "liable_party": None, "remedy": None, "gate": g["rule"], "gate_version": g["version"],
                   "gate_category": g["category"], "pre_gate": dec}
        else:
            trace.append({"rule": f"provenance_gate_{gate_version}", "fired": False, "because": g["reason"], "findings_used": used})
    settlement = settlement_instruction(dec, case_meta, rulebook) if dec["verdict"] == "decided" else None
    body = {"engine": f"abs-rules/{rb['version']}", "findings_sha256": sha256_hex(canonical(findings)), "decision": dec,
            "rule_trace": trace, "settlement_instruction": settlement}
    if v14 and dec["verdict"] == "decided":
        body["decision"] = {**dec, "contract_violations": contract_violations(dec, rulebook)}
    receipt = {**body, "receipt_sha256": sha256_hex(canonical(body))}
    receipt["signature"] = hmac.new(_RECEIPT_KEY, receipt["receipt_sha256"].encode(), hashlib.sha256).hexdigest()
    return receipt


def settlement_instruction(dec: dict, case_meta: dict, rulebook: str = HISTORICAL) -> dict:
    """Rail-specific instruction for a decided verdict. v1.2/v1.3 keep the historical mapping (incl. 'chargeback');
    v1.4 and v1.5 use the Audit 2 mapping: ABS refund, contractual collection if unpaid, the buyer's own issuer dispute on cards."""
    rail = case_meta["rail"]
    ex = RULEBOOKS[rulebook]["settlement"]["rail_execution"][rail]
    if rulebook not in CORE:
        if dec["remedy"] == "refund":
            return {"type": "refund", "amount": case_meta["disputed_amount"], "currency": "EUR", "cost_bearer": dec["liable_party"],
                    "goods_return": dec["reason_code"] == "AG3", "rail": rail, "rail_execution": ex[dec["liable_party"]]}
        if dec["remedy"] == "withdrawal":
            return {"type": "refund_on_withdrawal", "amount": case_meta["disputed_amount"], "currency": "EUR", "cost_bearer": "buyer (return shipping)",
                    "goods_return": True, "rail": rail, "rail_execution": ex["buyer_withdrawal"]}
        return {"type": "no_refund", "amount": 0.0, "currency": "EUR", "cost_bearer": "buyer", "goods_return": False, "rail": rail,
                "rail_execution": ex["buyer"]}
    unpaid = RULEBOOKS[rulebook]["settlement"]["if_unpaid"][rail]
    remedy = dec["remedy"]
    if remedy == "refund":
        out = {"type": "refund", "amount": case_meta["disputed_amount"], "currency": "EUR", "cost_bearer": dec["liable_party"],
               "goods_return": dec["reason_code"] == "AG3", "rail": rail, "rail_execution": ex[dec["liable_party"]], "if_unpaid": list(unpaid)}
        if dec["reason_code"] == "AG4-D":
            out["refund_basis"] = RULEBOOKS[rulebook]["reason_codes"]["AG4-D"]["remedy_basis"]
        return out
    if remedy == "withdrawal":
        return {"type": "refund_on_withdrawal", "amount": case_meta["disputed_amount"], "currency": "EUR", "cost_bearer": "buyer (return shipping, unless the trader agreed to bear it or failed to inform)",
                "goods_return": True, "rail": rail, "rail_execution": ex["buyer_withdrawal"], "if_unpaid": list(unpaid)}
    if remedy == "refer_to_payer_psp":
        return {"type": "referral", "amount": 0.0, "currency": "EUR", "cost_bearer": None, "goods_return": False, "rail": rail, "rail_execution": ex["rail_process"]}
    if remedy == "undetermined":
        return {"type": "pending_human_review", "amount": 0.0, "currency": "EUR", "cost_bearer": None, "goods_return": False, "rail": rail,
                "rail_execution": "none until a human resolves whether the withdrawal right is available"}
    return {"type": "no_refund", "amount": 0.0, "currency": "EUR", "cost_bearer": "buyer", "goods_return": False, "rail": rail, "rail_execution": ex["buyer"]}


def contract_violations(dec: dict, rulebook: str = CURRENT) -> list[str]:
    """The decision contract (acs/decision_contract.py, kind 'engine') applied with the decision's own rulebook. The
    contract module knows one liable party and remedy per code; v1.4 adds two things it does not model, accepted here
    explicitly: AG0's liable variants (rail process: referral; agent provider or merchant: refund) and 'undetermined'
    for a buyer-side code whose withdrawal prerequisite is missing. v1.5's ABS-V1 refund is checked by the contract itself
    (`burden_tier`, decision_contract.validate)."""
    from .decision_contract import validate
    rb = RULEBOOKS[rulebook]
    out = validate(dec, kind="engine", rulebook=rb)
    code = dec.get("reason_code")
    if code == "AG0" and dec.get("liable_party") in rb["reason_codes"]["AG0"].get("liable_variants", {}).values():
        want = "refer_to_payer_psp" if dec["liable_party"] == "rail_process" else "refund"
        out = [v for v in out if not v.startswith(("liable_party", "remedy"))] + ([] if dec.get("remedy") == want else [f"remedy {dec.get('remedy')} is not the AG0 remedy for {dec['liable_party']} ({want})"])
    if rulebook in CORE and dec.get("remedy") == "undetermined" and code in rb["reason_codes"] and rb["reason_codes"][code]["remedy"] == "deny_or_withdrawal":
        out = [v for v in out if not v.startswith("remedy undetermined")]
    return out


def verify_receipt(receipt: dict) -> bool:
    body = {k: receipt[k] for k in ("engine", "findings_sha256", "decision", "rule_trace", "settlement_instruction")}
    if sha256_hex(canonical(body)) != receipt["receipt_sha256"]:
        return False
    expected = hmac.new(_RECEIPT_KEY, receipt["receipt_sha256"].encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, receipt["signature"])

"""Rail model and Settlement Instruction execution (Audit 2 corrected).

A Decision is rail-agnostic; this module turns it into a Settlement Instruction in the rail's own
vocabulary and reports feasibility in three classes:

  feasible    the liable party pays by the rail's refund path (a NEW payment on push rails) or a
              payee-side PSP that holds the payout releases it;
  collection  the liable party refuses: no rail reversal exists, only the contractual collection
              right of a licensed PSP/acquirer (reserve, debit under the merchant agreement,
              set-off) or of the buyer; on cards the cardholder also keeps the issuer dispute route;
  infeasible  the liable party is gone and no payee-side PSP held funds (A2A merchant-account model,
              stablecoin, gift card);
  deferred    the case is escalated to human review: no instruction exists yet (never counted as
              executable; Audit 1 F17).

`moves_funds` marks the instructions whose execution moves money under ABS (refunds, apportioned
refunds, the late-delivery remedy, deposit retention). A corrected document (cure), a referral to the
rail's unauthorised-payment regime or to an authority's process, a denial and an escalation do not;
execution-feasibility counts are over funds-moving instructions only.

What ABS never does (Audit 2): start a SEPA recall (camt.056 is the payer's PSP's tool for duplicate,
technical error or fraud; a customer-reason recall needs payee consent; SCT Inst has no return;
camt.027/087 are fund inquiries); initiate or assign a card dispute (only the issuer opens one, at
the cardholder's request; the Decision Center supplies evidence and reconciles double recovery);
hold funds credited to a merchant's own account (a hold exists only where the PSP is the payee:
card acquiring, platform collection accounts, A2A acquiring); promise a guarantee-fund payout
(licence required; not normative).
"""

from __future__ import annotations

import os
import sys

_SCEN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scenarios")
if _SCEN not in sys.path:
    sys.path.insert(0, _SCEN)
from generate import RAILS, RAIL_CURRENCY, STANDARD_MESSAGES, standard_message  # noqa: E402

CURRENCY_STANDARD = "ISO 4217"
REVERSIBLE_FAMILIES = {"card", "wallet", "bnpl", "marketplace"}
FUNDS_MOVING_TYPES = {"refund_full", "refund_partial", "apportioned_refund", "delivery_cost_refund_or_reject_and_refund", "deposit_retention"}
# Scheme deadline guard for the cardholder's issuer dispute (figures as cited in Audit 2 from the
# Visa rules for 'merchandise not received'; verify per scheme and reason): days from the last
# expected delivery date, and the ceiling from processing.
CARD_NOT_RECEIVED_WINDOW_DAYS = 120
CARD_WINDOW_CEILING_DAYS = 540


def rail_info(rail: str) -> dict:
    r = dict(RAILS[rail])
    r["id"] = rail
    r["currency"] = RAIL_CURRENCY.get(rail, "EUR")
    return r


def hold_possible(facts: dict) -> bool:
    """A payout hold exists only where the PSP is the payee and a hold was configured."""
    return facts.get("payee_model") == "psp_collection" and facts.get("settlement_mode") in ("escrow_until_delivery", "delayed")


def card_deadline_guard(facts: dict) -> dict | None:
    if RAILS[facts["rail"]]["family"] != "card":
        return None
    last_expected = max(0, facts.get("latest_promised_delivery_day", 0))
    close_day = min(last_expected + CARD_NOT_RECEIVED_WINDOW_DAYS, CARD_WINDOW_CEILING_DAYS)
    day = facts.get("days_to_filing", 0)
    return {"issuer_dispute_window_closes_day": close_day, "abs_filing_day": day,
            "status": "open" if day <= close_day - 30 else ("closing" if day <= close_day else "closed"),
            "rule": "before the scheme limit the Decision issues or the user is told to file with the issuer; ABS deadlines pause while a rail dispute runs (general; verify per scheme)"}


def _executor_for_merchant(rail: str) -> tuple[str, str]:
    fam = RAILS[rail]["family"]
    return {
        "card": ("merchant_acquirer", "merchant refund to the original card through the acquirer; the cardholder keeps the issuer dispute route in parallel (never initiated or assigned by ABS)"),
        "wallet": ("wallet_operator", "wallet operator reverses the payment to the buyer's balance and debits the merchant under its agreement"),
        "a2a_push": ("merchant", "merchant initiates a NEW credit transfer to the buyer; the rail does not reverse"),
        "bnpl": ("bnpl_provider", "merchant refunds the BNPL provider, which cancels or reduces the loan and returns paid instalments"),
        "marketplace": ("platform_psp", "platform's licensed PSP (payee) reverses the responding sub-merchant's split and credits the buyer"),
        "stored_value": ("programme", "stored value re-credited to the buyer"),
        "crypto": ("merchant", "merchant sends an on-chain return transfer; no reversal exists"),
    }[fam]


def settlement_instruction(decision: dict, facts: dict, version: str) -> dict:
    """decision: {liable_party, remedy_class, reason_code, amount_fraction}. Returns the instruction."""
    rail = facts["rail"]
    fam = RAILS[rail]["family"]
    amount = round(facts.get("amount", 0.0) * decision.get("amount_fraction", 1.0), 2)
    ins = {"rail": rail, "rail_family": fam, "currency": RAIL_CURRENCY.get(rail, "EUR"), "currency_standard": CURRENCY_STANDARD,
           "payee_model": facts.get("payee_model"), "type": None, "amount": 0.0, "cost_bearer": None, "executor": None, "goods_return": False, "mechanism": None,
           "standard_message": None, "standard_verified": None, "standard_gap": False,
           "feasibility": {"class": "feasible", "feasible": True, "reason": "no movement of funds", "fallback": None},
           "card_deadline_guard": card_deadline_guard(facts), "notes": []}
    _instruction(ins, decision, facts, version, rail, fam, amount)
    ins["moves_funds"] = ins["type"] in FUNDS_MOVING_TYPES
    return ins


def _instruction(ins: dict, decision: dict, facts: dict, version: str, rail: str, fam: str, amount: float) -> dict:
    rc = decision.get("remedy_class")
    liable = decision.get("liable_party")

    def feas(cls, reason, fallback=None):
        ins["feasibility"] = {"class": cls, "feasible": cls == "feasible", "reason": reason, "fallback": fallback}

    if rc == "human_review":
        ins.update({"type": "escalated_no_instruction_yet", "cost_bearer": "undetermined",
                    "mechanism": "no Settlement Instruction until the fact-finder supplies the missing finding; funds stay where they are (a payee-side hold is kept if one exists)"})
        feas("deferred", "escalated to human review; no instruction until the fact-finder supplies the finding")
        return ins
    if rc == "cure":
        ins.update({"type": "cure_document", "cost_bearer": liable, "executor": liable, "amount": 0.0,
                    "mechanism": "corrected invoice / credit note / e-invoice reissued; no movement of funds",
                    "standard_message": "EN 16931 / Peppol BIS credit note and corrected invoice where the buyer requires structured e-invoicing (general; verify profile)", "standard_verified": "general"})
        return ins
    if rc == "refer_admin":
        ins.update({"type": "refer_to_authority_process", "cost_bearer": "none", "executor": "public_authority",
                    "mechanism": "administrative appeal and the authority's own refund process; no chargeback, no ABS Settlement Instruction",
                    "standard_message": "authority refund by credit transfer (pacs.008) under its own procedure; no payment-message standard for an administrative decision", "standard_verified": "none"})
        ins["standard_gap"] = True
        feas("feasible", "administrative route exists")
        return ins
    if rc in (None, "deny", "none", "inadmissible", "merchant_claim"):
        ins["type"] = "none" if rc != "merchant_claim" else "deposit_retention"
        if rc == "merchant_claim":
            ins.update({"cost_bearer": "buyer", "executor": "merchant", "amount": round(facts.get("amount", 0.0) * 0.3, 2),
                        "mechanism": "deposit retained up to the assessed damage; remainder released (card pre-authorisation capture or held funds release)",
                        "standard_message": "card: capture of the pre-authorisation (partial); A2A: held funds released by the merchant (no standard message for a deposit claim)",
                        "standard_verified": "uncertain"})
        return ins
    if rc == "refer":
        ins.update({"type": "refer_to_rail", "executor": "payers_psp_or_issuer", "cost_bearer": "rail_unauthorised_regime", "amount": amount,
                    "mechanism": "the payer's PSP decides whether the payment was unauthorised under its rules; ABS refers the case, supplies the Mandate record and records the outcome",
                    "standard_message": ("cardholder asks the issuer to raise a dispute with an unauthorised/fraud reason; the issuer decides" if fam == "card" else
                                         "payer's PSP refunds an unauthorised payment (book transfer / new pacs.008); it may use a camt.056 recall on the fraud ground (its tool, not ABS's); camt.029 if refused"),
                    "standard_verified": "general"})
        feas("feasible", "statutory unauthorised-payment procedure exists on the rail; decided by the payer's PSP")
        return ins

    ins["type"] = {"refund": "refund_full", "partial": "refund_partial", "apportioned": "apportioned_refund", "late_remedy": "delivery_cost_refund_or_reject_and_refund"}[rc]
    ins["amount"] = amount
    feas("feasible", "the liable party pays through the rail's refund path (a new payment on push rails)")
    ins["goods_return"] = decision.get("goods_return", False)
    ins["cost_bearer"] = liable
    merchant_gone = not (facts.get("merchant_reachable", True) and facts.get("merchant_solvent", True))
    refuses = facts.get("merchant_refuses_to_pay", False)
    held = hold_possible(facts)

    if liable in ("merchant", "platform", "merchant+agent_provider"):
        ex, mech = _executor_for_merchant(rail)
        msg, ver = standard_message(rail, "merchant_refund")
        if fam == "card":
            cb, _ = standard_message(rail, "chargeback")
            msg = f"{msg}; in parallel, at the cardholder's request only: {cb}"
        ins.update({"executor": ex, "mechanism": mech, "standard_message": msg, "standard_verified": ver})
        if merchant_gone:
            if held:
                feas("feasible", "payee PSP held the payout (acquiring/collection model); released to the buyer", "payee_psp_hold_release")
                ins["executor"] = "payee_psp_hold"
                ins["standard_message"] = "payee PSP pays the buyer from the held payout: card refund via the acquirer, or a new credit transfer (pacs.008); no rail-native hold message"
                ins["standard_verified"] = "none"
            elif RAILS[rail]["reversible"]:
                feas("feasible", "cardholder/buyer can still recover through the issuer dispute or operator programme (their own right, not ABS's); loss moves to the acquirer/operator", "issuer_dispute_or_operator_programme")
            else:
                fb = "uk_app_reimbursement_regime (PSP-level, outside ABS; conditions and caps; uncertain)" if rail == "uk_fps" else None
                feas("infeasible", "liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from", fb)
        elif refuses:
            col, _ = standard_message(rail, "collection")
            feas("collection", "merchant refuses: no rail reversal; contractual collection by its licensed PSP/acquirer or by the buyer; suspension from the Register", "contractual_collection")
            ins["notes"].append(col)
            if fam == "crypto":
                feas("infeasible", "merchant refuses and no collection mechanism exists on-chain; off-chain claim only", None)
    if liable in ("agent_provider", "merchant+agent_provider"):
        msg, ver = standard_message(rail, "third_party_refund")
        if liable == "agent_provider":
            ins.update({"executor": "agent_provider", "mechanism": "agent provider pays the buyer by a new payment (credit transfer, or a sponsored push-to-card credit where offered); no rail message reverses the original purchase for a third party",
                        "standard_message": msg, "standard_verified": ver})
        else:
            ins["executor"] = (ins["executor"] or "merchant") + "_and_agent_provider"
            ins["mechanism"] = f"{ins['mechanism']}; agent provider pays its share by a new payment"
            ins["standard_message"] = f"{ins['standard_message']}; agent provider share: {msg}"
            ins["standard_verified"] = "none" if "none" in (ins["standard_verified"], ver) else ("uncertain" if "uncertain" in (ins["standard_verified"], ver) else "general")
    if liable == "register_operator":
        ins.update({"executor": "register_operator", "mechanism": "contractual claim against the Register operator for the forged entry; it pays by a new credit transfer; no rail mechanism; a guarantee fund that pays buyers is not normative (licence required)",
                    "standard_message": "no existing message: operator payment is a new credit transfer (pacs.008) under contract", "standard_verified": "none"})
        feas("collection", "contractual claim against the Register operator; no rail path and no normative guarantee", "contractual_claim")
    if liable == "programme_guarantee":
        ins.update({"executor": "none", "mechanism": "a programme guarantee payout is not part of the normative rule set (licence required)", "standard_message": "none", "standard_verified": "none"})
        feas("infeasible", "guarantee fund removed from the normative rules (Audit 2 LIC-03)")
    if ins["standard_verified"] == "none":
        ins["standard_gap"] = True
    if version == "v0.1" and fam not in ("card", "a2a_push"):
        ins["notes"].append("ABS v0.1 defines rail execution for card and a2a_instant only; this rail's execution is undefined in v0.1")
    return ins


def rail_execution_defined(version: str, rail: str) -> bool:
    fam = RAILS[rail]["family"]
    if version == "v0.1":
        return fam in ("card", "a2a_push")
    return True


def standards_gap_table() -> list[dict]:
    """Every (rail or family, outcome) whose mapping is 'none': places where ABS must extend a standard."""
    out = []
    for key, table in STANDARD_MESSAGES.items():
        for kind, (msg, ver) in table.items():
            if ver == "none":
                out.append({"rail_or_family": key, "outcome": kind, "note": msg})
    return out

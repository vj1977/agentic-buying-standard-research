"""Consumer-rights and regulatory overlays.

An overlay never changes who is liable under ABS; it adds a route or a constraint the Decision must
state. Every statement here is general (no article numbers) and carries a certainty. `stated_in`
says whether ABS v0.1 (rulebook v1.1) says anything about it; the simulation counts missing
statements as gaps of the "overlay not carried by the Decision" type.
"""

from __future__ import annotations

WITHDRAWAL_BY_GOODS = {
    "physical": ("applies", None), "bundle": ("applies", None), "pre_order": ("applies", None), "multi_merchant_basket": ("applies", None),
    "subscription": ("applies", "first period"),
    "perishable": ("excepted", "goods liable to deteriorate quickly"),
    "custom_made": ("excepted", "goods made to the consumer's specification"),
    "travel_ticket": ("excepted", "transport/leisure service for a specific date"),
    "rental": ("excepted", "vehicle rental for a specific date"),
    "digital": ("conditional", "lost once the download/streaming starts with the consumer's consent"),
    "service": ("conditional", "lost once the service is fully performed with the consumer's consent"),
}


def overlays(facts: dict) -> list[dict]:
    out: list[dict] = []
    goods = facts["goods_type"]
    fam = facts["rail_family"]
    rail = facts["rail"]
    consumer = facts.get("buyer_type", "consumer") == "consumer"
    j = facts.get("jurisdiction", "EU")
    tx = facts.get("transaction_occurred", True)

    def add(id_, applies, statement, certainty, stated_in_v01, route=None):
        out.append({"id": id_, "applies": applies, "statement": statement, "certainty": certainty, "stated_in_v0.1": stated_in_v01, "route": route})

    if tx and consumer and j in ("EU", "UK", "cross_border"):
        kind, why = WITHDRAWAL_BY_GOODS[goods]
        day = facts.get("withdrawal_requested_day")
        if kind == "conditional":
            consumed = facts.get("digital_unsealed") if goods == "digital" else facts.get("service_started")
            kind = "excepted" if consumed else "applies"
        if kind == "applies":
            in_time = day is None or day <= 14
            add("eu_withdrawal_14d", in_time, "Distance sale to a consumer: 14-day withdrawal without reason; return at the consumer's cost unless the merchant failed to inform; refund within a short period after return"
                + ("" if in_time else " -- requested after day 14: period over"), "general_law", False,
                route="withdrawal_refund_on_return (outside ABS liability; same rail refund message)" if in_time else None)
        else:
            add("eu_withdrawal_excepted", False, f"Withdrawal does not apply: {why} (general statement; verify)", "general_law", False)
        add("statutory_conformity_guarantee", True, "A statutory conformity guarantee against the seller outlasts the ABS 60-day window (duration varies by jurisdiction)", "general_law", False,
            route="statutory_claim_against_seller")
    elif tx and not consumer:
        add("b2b_no_consumer_withdrawal", False, "Business buyer: consumer withdrawal and consumer guarantees do not apply; B2B terms govern", "general_law", False)

    if fam == "card":
        add("card_dispute_right_parallel", True, "The cardholder's right to ask the issuer to dispute the transaction stays available in parallel; ABS never assigns, waives or initiates it (a merchant may not require a cardholder to waive it). The Decision is offered as evidence; a Decision refund is set off against any later rail recovery. Scheme time limits apply (e.g. 'not received': 120 days from the last expected delivery, at most 540 days from processing, as cited in Audit 2; verify per scheme)", "general", False,
            route="cardholder -> issuer: first dispute -> response -> pre-arbitration -> arbitration (scheme-neutral stage names)")
        if rail == "card_on_file_token" or facts.get("recurring"):
            add("payee_initiated_refund_right", True, "Payee-initiated payment: a refund right of up to eight weeks may exist where the authorisation did not specify the exact amount and the amount exceeded what the payer could reasonably expect (EU payment rules; general; verify)", "uncertain", False)
    if fam == "wallet":
        add("wallet_buyer_protection", True, "Wallet operator buyer-protection programme runs in parallel and is never assigned; a Decision refund is reconciled against it", "general", False)
    if fam == "bnpl":
        add("bnpl_connected_lender", True, "Refund flows through the BNPL provider; in some jurisdictions the lender shares liability for the merchant's breach (uncertain)", "uncertain", False)
    if rail == "uk_fps" and consumer:
        add("uk_app_reimbursement", facts.get("delivery_status") in ("not_delivered", "not_performed") and not facts.get("merchant_participates", True),
            "UK authorised-push-payment fraud reimbursement regime: the sending PSP may reimburse a consumer scam victim (conditions, caps and exceptions apply; uncertain); ABS needs subrogation", "uncertain", False,
            route="psp_reimbursement_then_subrogation")
    if rail == "pix":
        add("pix_special_return", True, "Pix has a special return mechanism for fraud and operational failure, initiated through the PSPs (general; verify)", "uncertain", False)
    if rail == "upi":
        add("upi_dispute_mechanism", True, "UPI disputes go through the scheme's online dispute mechanism (general; verify)", "uncertain", False)
    if fam in ("a2a_push", "crypto", "stored_value"):
        add("push_payment_finality", True, "A push payment is final on this rail; a refund is a NEW payment by the liable party; against a refusing merchant only contractual collection exists (a camt.056 recall is the payer's PSP's tool for duplicate/technical/fraud, not a goods-dispute mechanism; SCT Inst has no return); ABS v0.1 states finality for a2a_instant only",
            "general", fam == "a2a_push" and rail == "sepa_instant")
    if facts.get("gdpr_request"):
        add("gdpr_" + facts["gdpr_request"], True,
            "Access: serve the evidence bundle minus third-party data. Erasure: may be deferred while the data is necessary for the claim; ABS must state retention until decision + appeal window (general statement)", "general_law", False)
    if facts.get("card_data_in_agent_context"):
        add("pci_card_data_in_agent_context", True, f"Card data entered the agent context ({facts['card_data_in_agent_context']}); PCI scope breach by that party; network tokens only", "general", False)
    if facts.get("provider_outage"):
        add("dora_operational_resilience", True, f"Provider outage ({facts['provider_outage']}): idempotent checkout and durable Purchase Record required; broken records count against the keeper", "general", False)
    if facts.get("dcc_applied"):
        add("dcc_transparency", True, f"Dynamic currency conversion applied (chosen by {facts.get('dcc_chosen_by')}); the Mandate's pay-in currency and the Offer Feed's landed cost govern", "general", False)
    if facts.get("duties_disclosed_in_landed_cost") is not None:
        add("cross_border_landed_cost", True, "Total landed cost must include mandatory import charges or state that they are payable on import", "general", False)
    if facts.get("buyer_type") == "consumer" and "minor" in facts.get("_tags", []):
        add("minor_contract_capacity", True, "Contracts by minors may be voidable; outside ABS (uncertain)", "uncertain", False)
    return out

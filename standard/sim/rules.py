"""ABS decision rules in two rule sets.

`v0.1`  = ABS v0.1 as written (rulebook/AGENTIC_DISPUTE_RULEBOOK.md v1.1): participation, frozen
          offer, conformity first, manipulative offer, agent outside the mandate (amount, category,
          merchant, units, expiry), buyer side, conduct, 60-day time limit, rail execution for card
          and a2a_instant.
`v0.2`  = v0.1 plus the fixes this simulation proposes. Every v0.2-only rule carries
          `proposed_text`, the wording the ABS author can adopt.

A rule is a predicate over typed findings plus an outcome. The engine evaluates every rule, keeps
the ordered list that fired, and decides by group order then rule order. Groups, in decision
order: standing, authorisation, conduct, conformity, manipulative_offer, agent_mandate,
buyer_side. `needs` lists the evidence items a rule depends on. `judgment` lists findings that a
deterministic kernel cannot compute from records alone and that a fact-finder (human or LLM) must
supply as typed inputs.

Liability rule (Audit 0): the precision of the Mandate decides. An explicit Mandate or Allowance
breach makes the agent provider liable; conforming to the explicit Mandate but not the unstated
intent puts it on the user; a non-conforming delivery makes the merchant liable; an injected or
manipulative offer makes the merchant liable.
"""

from __future__ import annotations

GROUP_ORDER = ["standing", "authorisation", "conduct", "conformity", "manipulative_offer", "agent_mandate", "buyer_side"]
V01_HARD_LIMITS = ("amount", "category", "merchant", "units", "expiry")
# Explicit Mandate / Allowance fields proposed for v0.2 (all must be encoded to count as hard limits).
V02_HARD_LIMITS = V01_HARD_LIMITS + ("step_up", "required_attributes", "currency", "delivery_address", "scope", "split_evasion",
                                     "monthly_budget", "role", "approval", "notify_hold", "invoice_data", "policy_version",
                                     "payment_terms", "procurement_threshold")
# Breaches whose finding needs the action log (E2); the rest need only mandate + transaction (E1).
E2_BREACHES = {"step_up", "required_attributes", "scope", "split_evasion", "role", "approval", "notify_hold", "invoice_data",
               "policy_version", "payment_terms", "delivery_address", "monthly_budget", "procurement_threshold"}
PARTIAL_KINDS = {"price", "delivery_cost", "quantity", "non_delivery_partial"}
CURE_KINDS = {"invoice_terms"}
CURE_BREACHES = {"invoice_data"}
NO_LOSS_BREACHES = {"payment_terms"}


def _frac(fd):
    return fd["amount_fraction"]


def _ret(fd):
    return fd["conformity"]["delivery_status"] in ("delivered", "substitute", "partial", "access_granted", "performed", "delivered_to_wrong_address")


def O(liable, remedy_class, code, fd=None, fraction=None, goods_return=False, finding=""):
    return {"liable_party": liable, "remedy_class": remedy_class, "reason_code": code,
            "amount_fraction": fraction if fraction is not None else (_frac(fd) if fd else 1.0), "goods_return": goods_return, "finding": finding}


def R(id_, group, order, versions, when, outcome, text, needs=(), judgment=(), proposed_text=None, min_level=0):
    return {"id": id_, "group": group, "order": order, "versions": set(versions), "when": when, "outcome": outcome, "text": text,
            "needs": set(needs), "judgment": list(judgment), "proposed_text": proposed_text, "min_level": min_level}


BOTH = ("v0.1", "v0.2")
V2 = ("v0.2",)


def _live(fd):
    return fd["transaction_occurred"] and fd["dispute_filed"]


def _known(fd, key):
    return fd["known"].get(key, False)


RULES: list[dict] = [
    # ---------------- standing ----------------
    R("ABS-S0.no-dispute", "standing", 0, BOTH,
      lambda fd: fd["transaction_occurred"] and not fd["dispute_filed"],
      lambda fd: O("none", "none", "ABS-OK", finding="no Dispute Case opened"),
      "No Dispute Case was opened; nothing to decide.", needs=["buyer_claim"]),
    R("ABS-M.refusal-record", "standing", 1, V2,
      lambda fd: not fd["transaction_occurred"],
      lambda fd: O("none", "none", "ABS-M1" if fd["false_decline"] else "ABS-M2", finding="no transaction; refusal recorded"),
      "No purchase happened. A refusal is recorded and measured (false refusal vs true block); there is no liability.", needs=["refusal_record"],
      proposed_text="New 2.4: Every refusal to buy writes a Refusal Record (offers compared, Mandate, stated reason). Refusals of a conforming, qualified, in-mandate offer count as false refusals on the programme scoreboard per agent provider; they carry no liability."),
    R("ABS-6.1.time-limit", "standing", 2, BOTH,
      lambda fd: _live(fd) and not fd["standing"]["filing_within_limit"],
      lambda fd: O("none", "inadmissible", "ABS-T1", finding=f"filed on day {fd['standing']['days_to_filing']}, limit day {fd['standing']['limit_day']}"),
      "Filing after 60 days from the later of the transaction and the latest promised delivery date is inadmissible.", needs=["date"]),
    R("ABS-T2.repeat-dispute", "standing", 3, V2,
      lambda fd: _live(fd) and fd["standing"]["repeat_dispute"],
      lambda fd: O("none", "inadmissible", "ABS-T2", finding="second Dispute Case on the same Purchase Record without new facts"),
      "One Dispute Case per Purchase Record unless new facts are shown.", needs=["buyer_claim"],
      proposed_text="New 6.7: One Dispute Case per Purchase Record. A second case on the same record is admitted only on facts not available to the filing party at the first filing, or to reopen a settlement obtained by a false claim (6.3)."),
    R("ABS-D2.merchant-claim", "standing", 4, V2,
      lambda fd: fd["transaction_occurred"] and fd["merchant_claim_against_buyer"],
      lambda fd: O("buyer", "merchant_claim", "ABS-D2", fraction=0.3, finding="merchant-initiated claim on the deposit decided on handover and return records"),
      "A merchant may open a Dispute Case against the buyer for a deposit or damage, decided on the handover and return records.", needs=["return_inspection_record"],
      judgment=["damage_attributable_to_buyer"], min_level=3,
      proposed_text="New 6.8: A merchant may open a Dispute Case against the buyer only for a deposit, damage or non-return recorded in handover and return records. The same decision order applies with the roles reversed; the remedy is capped at the deposit or the recorded damage."),
    R("ABS-G1.authority-payee", "standing", 5, V2,
      lambda fd: _live(fd) and fd["responding_party"] == "authority" and not fd["participation"]["merchant_participates"] and fd["participation"]["verified_by_agent"] and not fd["within_mandate"]["breaches_recognised"],
      lambda fd: O("none", "refer_admin", "ABS-G1", finding="payee is a public authority; administrative appeal governs the payee side"),
      "When the payee is a public authority (taxes, fees, fines, permits), ABS covers the agent's conduct only; the payee side is governed by administrative appeal and the authority's refund process.", needs=["participation_record"], min_level=3,
      proposed_text="New 1.5a: A public authority is a permitted payee without a Participation Agreement when the agent verified it in the official registry. ABS decides only whether the agent stayed inside the Mandate; claims against the authority follow administrative appeal, and its refunds follow its own process."),
    R("ABS-P1.non-participant", "standing", 6, V2,
      lambda fd: _live(fd) and _known(fd, "participation") and (not fd["participation"]["merchant_participates"] or not fd["authorisation"]["credential_bound"])
      and not fd["participation"]["verified_by_agent_and_spoofed"] and not (fd["responding_party"] == "authority" and fd["participation"]["verified_by_agent"]),
      lambda fd: O("agent_provider", "refund", "ABS-P1", finding="payment to a non-participant or outside the mandate-bound credential"),
      "An agent must not pay a merchant that holds no Participation Agreement, and must pay only with the mandate-bound credential. If it does either, the agent provider bears the buyer's loss that the rail's native dispute does not recover.",
      needs=["participation_record"], min_level=3,
      proposed_text="New 1.5: Before paying, the agent verifies the merchant's current, signed entry in the Qualified Merchant Register. A payment to a merchant without one, or made outside the mandate-bound credential, is outside the Mandate: the agent provider bears the buyer's loss that the rail's own dispute process does not recover."),
    R("ABS-P2.spoofed-register", "standing", 7, V2,
      lambda fd: _live(fd) and _known(fd, "participation") and fd["participation"]["verified_by_agent_and_spoofed"],
      lambda fd: O("register_operator", "refund", "ABS-P2", finding="forged register entry passed verification; contractual claim against the Register operator"),
      "If a forged Register entry passed a correct verification, the Register operator answers for its register under contract; the agent provider is not liable. No guarantee fund pays the buyer under the normative rules (a fund would need a licence).", needs=["participation_record"], min_level=3,
      proposed_text="New 1.6: The Qualified Merchant Register is signed by its operator. Where an agent verified an entry later shown to be forged, the operator is liable to the buyer under the Participation Agreement and pays by a new credit transfer; the agent provider is not liable. Any guarantee fund that would pay buyers belongs to Part B until its licensed form (authorised insurer, credit-institution guarantee, or the operator's own undertaking) is settled by legal opinion."),
    # ---------------- authorisation (step 0) ----------------
    R("AG0.unauthorised-mandate", "authorisation", 0, V2,
      lambda fd: _live(fd) and _known(fd, "authorisation") and not fd["authorisation"]["valid"],
      lambda fd: _auth_outcome(fd),
      "Step 0. If the Mandate was not created by the account holder with strong authentication, or the charge was not initiated by the agent under a live Mandate, the case is one of authorisation, not of conformity.",
      needs=["signed_mandate"], min_level=1,
      proposed_text="New 4.0 (Step 0, Authorisation). Before Step 1 the arbiter checks that (a) the Mandate was created by the account holder with strong authentication performed by a PSP, and (b) the charge was initiated by the buyer's agent under that Mandate before its expiry with the mandate-bound credential. If (a) fails, the case is an unauthorised payment: ABS refers it to the rail's unauthorised-payment procedure and supplies the Mandate record; the buyer is not liable under ABS. If the provider's systems issued the charge without a valid Mandate (compromise, or a Mandate accepted without strong authentication), the agent provider is liable. If (b) fails because the merchant presented the credential again or charged after expiry, the merchant is liable for that charge."),
    # ---------------- conduct ----------------
    R("ABS-7.1.conduct", "conduct", 0, BOTH,
      lambda fd: _live(fd) and _known(fd, "tampering") and fd["evidence"]["tampered_by"] is not None,
      lambda fd: _conduct_outcome(fd),
      "Knowingly false or altered evidence decides the dispute against the party that submitted it.", needs=["hash_chain_verification"],
      judgment=["evidence_knowingly_false_or_altered"], min_level=3),
    # ---------------- step 1 conformity ----------------
    R("ABS-4.1.conformity", "conformity", 0, BOTH,
      lambda fd: _live(fd) and fd["conformity"]["established"] == "nonconforming",
      lambda fd: _conformity_outcome(fd),
      "Step 1. If the delivery does not conform to the Offer Snapshot (model, specs, colour, condition, quantity, accessories, images, price, delivery terms; non-delivery; counterfeit), the merchant is liable whatever the agent did.",
      needs=["offer_snapshot", "delivery_evidence_bundle"], judgment=["conformity_of_free_text_description", "counterfeit_determination", "damage_vs_wear"]),
    R("ABS-E1m.merchant-records-missing", "conformity", 1, V2,
      lambda fd: _live(fd) and fd["conformity"]["established"] == "unknown" and fd["conformity"]["evidence_state"] == "missing_merchant_records" and fd["conformity"]["delivery_status"] not in ("not_delivered", "not_performed"),
      lambda fd: O(fd["responding_party_liable"], "refund", "ABS-E1", goods_return=_ret(fd), finding="merchant kept no packing record; adverse inference against the record keeper"),
      "Where neither side has content evidence and the merchant cannot produce the packing record it was required to keep, the conformity question is decided against the merchant.", needs=["buyer_claim", "merchant_reply"], min_level=3,
      proposed_text="Amend 3 (E3): the merchant keeps a packing record (serials, weight, photo at packing) for every Purchase Record. Amend 3 'where evidence is missing': 'A party that was required to keep a record and cannot produce it when asked has the question that record would answer decided against it.'"),
    R("ABS-E2.unproven-claim", "conformity", 2, V2,
      lambda fd: _live(fd) and fd["conformity"]["established"] == "unproven",
      lambda fd: O("buyer", "deny", "AG5", finding="non-conformity claimed without content evidence; merchant records consistent with the Offer Snapshot; carrier proof shows handover"),
      "A not-as-described claim with no content evidence from the buyer, against a packing record and serials consistent with the Offer Snapshot and a carrier proof of handover, fails.", needs=["merchant_packing_record(serials, weight)", "carrier_proof_of_delivery(no content inspection)"], min_level=3,
      proposed_text="New 3.3 (minimum evidence): The buyer supports a not-as-described claim with photos or a return inspection; carrier proof of delivery proves handover, never content. Where the buyer gives none and the merchant's packing record and serials match the Offer Snapshot, the claim fails under Step 4."),
    R("ABS-H1.conflicting-evidence", "conformity", 3, V2,
      lambda fd: _live(fd) and fd["conformity"]["established"] == "disputed",
      lambda fd: O("undetermined", "human_review", "ABS-H1", finding="records conflict (packing serial vs photographed serial) and no record keeper is at fault; fact-finder required"),
      "Where the records conflict and no record keeper is at fault, no deterministic rule decides; the case is escalated to a fact-finder with human review.", needs=["buyer_unboxing_photos", "merchant_packing_record(serials, weight)"], min_level=3,
      judgment=["which_record_is_true"],
      proposed_text="New 6.5a (Decision Center): When the engine cannot establish a finding from the records (conflicting serials, contested photos), it returns 'review' with the conflicting records marked; a fact-finder supplies the typed finding and the engine decides from it. Any party may request human review of any Decision; the review is by a person who did not take part in the automated decision."),
    R("ABS-S1.unsigned-spec", "conformity", 4, V2,
      lambda fd: _live(fd) and fd["conformity"]["established"] == "unknown" and fd["conformity"]["spec_source"] in ("ai_extracted_unconfirmed", "legacy_free_text_only"),
      lambda fd: (O("agent_provider", "refund", "ABS-S1", goods_return=_ret(fd), finding="agent compared on an unconfirmed extracted spec") if fd["conformity"]["spec_source"] == "ai_extracted_unconfirmed"
                  else O(fd["responding_party_liable"], "refund", "ABS-S1", goods_return=_ret(fd), finding="participant sold without a signed structured spec; free text construed against it")),
      "Only the merchant-signed structured spec binds. An agent that compares on an unconfirmed extracted spec bears the mismatch; a participant that sells without a signed spec has every ambiguity in its free text construed against it.",
      needs=["offer_snapshot", "offer_feed_signature_check"], min_level=3,
      proposed_text="Amend 1.3 and 2.2: The Offer Snapshot's structured attributes bind only when signed by the merchant (the Product Specification: conformity-critical attributes, units, tolerances, package contents, region/compatibility, condition grade). Free text and marketing claims are not binding and cannot cut down the signed spec. An agent must not accept an offer from a participant without a signed spec; if it extracts attributes itself and buys on them, the agent provider bears any mismatch. A participant that sells to agents without a signed spec has every ambiguity in its listing construed against it."),
    R("ABS-S2.ambiguity", "conformity", 5, V2,
      lambda fd: _live(fd) and fd["conformity"]["established"] == "unknown" and fd["conformity"]["ambiguous"],
      lambda fd: O(fd["responding_party_liable"], "refund", "ABS-S2", goods_return=_ret(fd), finding="ambiguous Offer Snapshot construed against its author"),
      "An ambiguity in the Offer Snapshot is construed against the merchant that wrote it.", needs=["offer_snapshot", "delivery_evidence_bundle"], judgment=["attribute_is_ambiguous"], min_level=3,
      proposed_text="New 4.1a: Where the Offer Snapshot can reasonably be read two ways and the delivery fits only one, the reading favourable to the buyer applies (the merchant wrote the offer). The merchant avoids this by stating the attribute with its unit, region and tolerance in the signed Product Specification."),
    R("ABS-D1.default-on-silence", "conformity", 6, V2,
      lambda fd: _live(fd) and not fd["evidence"]["merchant_responded"] and fd["conformity"]["established"] == "unknown",
      lambda fd: O(fd["responding_party_liable"], "refund", "ABS-D1", finding="no response within the response window; buyer's account of facts within its knowledge accepted"),
      "If the merchant does not respond within the response window and produces no delivery evidence, the buyer's account of facts within its knowledge is accepted.", needs=["buyer_claim", "merchant_reply"],
      proposed_text="Amend 6.2: If no response arrives within 10 days, the facts stated by the buyer that lie within the buyer's own knowledge (non-receipt, what arrived) are taken as established, and the arbiter decides on them."),
    # ---------------- step 2 manipulative offer ----------------
    R("ABS-4.2.injection", "manipulative_offer", 0, BOTH,
      lambda fd: _live(fd) and _known(fd, "injection") and fd["manipulation"]["injection_present"],
      lambda fd: O(fd["responding_party_liable"], "partial" if _frac(fd) < 1 else "refund", "AG4", fd, finding="agent followed instructions in merchant-controlled content (listing, hosted reviews, profile, seller-agent)"),
      "Step 2. The agent bought because it followed instructions embedded in content the merchant controls or hosts. Merchant liable; refund of the affected items.",
      needs=["agent_action_log", "page_snapshots_at_view"], judgment=["text_instructs_an_agent", "causation_agent_followed_it"], min_level=2),
    R("ABS-4.2.merchant-added", "manipulative_offer", 1, BOTH,
      lambda fd: _live(fd) and _known(fd, "cart_origin") and fd["manipulation"]["merchant_added_lines"],
      lambda fd: O(fd["responding_party_liable"], "partial" if _frac(fd) < 1 else "refund", "AG1-M", fd, finding="merchant or platform added or pre-selected lines the agent did not choose"),
      "Step 2. The merchant added or pre-selected items or fees the agent did not choose. Merchant liable; refund of the affected items.", needs=["cart_with_line_origin"], min_level=3),
    R("ABS-4.2b.feed-snapshot-mismatch", "manipulative_offer", 2, V2,
      lambda fd: _live(fd) and _known(fd, "feed") and fd["manipulation"]["feed_mismatch"] and not fd["manipulation"]["merchant_added_lines"] and fd["manipulation"]["feed_signature"] in ("valid", "valid_key_leaked"),
      lambda fd: O(fd["responding_party_liable"], "partial", "AG1-M", fd, finding="checkout terms worse than the Offer Feed record (or seller-agent statement) the agent compared on"),
      "Step 2 (extended). A price, delivery cost, fee, conversion or negotiated term at checkout worse than the Offer Feed record or signed negotiation record the agent relied on is a manipulative offer; the merchant owes the difference.",
      needs=["offer_snapshot", "page_snapshots_at_view"], min_level=3,
      proposed_text="Amend 4 Step 2: add 'or the Offer Snapshot's price, delivery cost, mandatory fees, currency conversion, import charges or negotiated terms are worse for the buyer than the Offer Feed record or signed negotiation record the agent relied on when it chose the merchant'. Remedy: refund of the difference. The record the agent compared on is kept in the hash chain with the Snapshot."),
    R("ABS-4.2c.deceptive-claims", "manipulative_offer", 3, V2,
      lambda fd: _live(fd) and _known(fd, "false_claims") and fd["manipulation"]["false_claims"],
      lambda fd: O(fd["responding_party_liable"], "partial" if _frac(fd) < 1 else "refund", "AG4-D", fd, finding="false claim in merchant content caused the choice"),
      "Step 2 (extended). A false statement in merchant content (reference price never charged, false scarcity, invented urgency) that caused the agent's choice is a manipulative offer.",
      needs=["page_snapshots_at_view", "agent_action_log"], judgment=["claim_is_false", "claim_caused_the_choice"], min_level=3,
      proposed_text="Amend 4 Step 2: add reason code AG4-D, Deceptive offer content: a statement of fact in merchant-controlled content shown to be false (reference prices, stock, time limits, endorsements) where the agent's log shows it influenced the choice. Remedy: refund of the difference against the best conforming offer the agent had seen, or of the affected item."),
    R("ABS-F1.feed-authenticity", "authorisation", 1, V2,
      lambda fd: _live(fd) and _known(fd, "feed") and fd["manipulation"]["feed_signature"] in ("invalid", "absent", "valid_key_leaked") and fd["manipulation"]["feed_mismatch"],
      lambda fd: (O(fd["responding_party_liable"], "refund", "ABS-F1", goods_return=_ret(fd), finding="feed signed with the merchant's leaked key; merchant answers for its key") if fd["manipulation"]["feed_signature"] == "valid_key_leaked"
                  else O("agent_provider", "refund", "ABS-F1", goods_return=_ret(fd), finding="agent relied on an Offer Feed record whose signature did not verify")),
      "Offer Feed records are signed. An agent that relies on a record whose signature does not verify bears the mismatch; a merchant answers for records signed with its key until it revokes the key.",
      needs=["offer_feed_signature_check"], min_level=3,
      proposed_text="New 1.9: Offer Feed records are signed by the merchant's registered key. An agent must not rely on a record whose signature does not verify; if it does, the agent provider bears the mismatch. A merchant answers for records signed with its key, including after a key compromise, until it revokes the key in the Register."),
    R("ABS-X1.collusion", "manipulative_offer", 5, V2,
      lambda fd: _live(fd) and _known(fd, "agent_conduct") and fd["agent_conduct"]["collusion"],
      lambda fd: O("merchant+agent_provider", "refund", "ABS-X1", fd, finding="merchant and agent provider colluded"),
      "A merchant and an agent provider that share undisclosed revenue from steering are jointly liable for the purchase.", needs=["agent_action_log", "trust_attestation_at_checkout"],
      judgment=["existence_of_undisclosed_arrangement"], min_level=3,
      proposed_text="New 4.2d: Where the merchant and the agent provider have an undisclosed arrangement under which the agent's choice benefits both, they are jointly and severally liable for the buyer's loss, and both are suspended from the Register pending review."),
    # ---------------- step 3 agent outside the mandate ----------------
    R("ABS-4.3.agent-outside-mandate", "agent_mandate", 0, BOTH,
      lambda fd: _live(fd) and fd["within_mandate"]["breaches_recognised"] and fd["evidence"]["mandate_and_log_produced"],
      lambda fd: _agent_outcome(fd),
      "Step 3. The agent itself broke a hard mandate limit. Agent provider liable; refund of the out-of-mandate amount.", needs=["signed_mandate", "agent_action_log"], min_level=1),
    R("ABS-R1.apportionment", "agent_mandate", 1, V2,
      lambda fd: False,  # applied by the engine as a post-step when conformity and mandate rules both fire on different components
      lambda fd: None,
      "Where more than one step is satisfied for different components of the same purchase, decide each component under its own step and apportion.",
      proposed_text="Amend 4 (decision order): 'Where more than one step is satisfied for different components of the same purchase (for example late delivery by the merchant and an extra unit bought by the agent), the arbiter decides each component under its own step and apportions the remedy. The order of steps resolves which party answers for the same component, not whether a second party answers for a different one.'"),
    R("ABS-E1.adverse-inference", "agent_mandate", 2, V2,
      lambda fd: _live(fd) and not fd["evidence"]["mandate_and_log_produced"] and not fd["buyer"]["intent_matched"],
      lambda fd: O("agent_provider", "refund", "ABS-E1", goods_return=_ret(fd), finding="Mandate and action log not produced; adverse inference against the record keeper"),
      "If the agent provider cannot produce the Mandate and the action log, Step 3 is resolved against it.", needs=["buyer_claim"],
      proposed_text="Amend 3 'where evidence is missing': 'A party that was required to keep a record (the agent provider for the Mandate and action log; the merchant for the Offer Snapshot and packing record) and cannot produce it when asked has the question that record would answer decided against it.'"),
    R("ABS-X2.undisclosed-incentive", "agent_mandate", 3, V2,
      lambda fd: _live(fd) and _known(fd, "agent_conduct") and fd["agent_conduct"]["undisclosed_incentive"] and not fd["agent_conduct"]["collusion"],
      lambda fd: O("agent_provider", "partial", "ABS-X2", fd, finding="undisclosed incentive steered the choice away from the best conforming offer"),
      "An agent provider that steers to a merchant for an undisclosed incentive owes the buyer the difference against the best conforming offer.", needs=["agent_action_log"],
      judgment=["incentive_existed_and_was_undisclosed"], min_level=2,
      proposed_text="New 1.4a: The agent provider discloses in the Mandate any payment it receives from merchants. A choice influenced by an undisclosed incentive is outside the Mandate (reason code ABS-X2); remedy: the difference against the best conforming offer the agent saw."),
    # ---------------- step 4 buyer side ----------------
    R("ABS-4.4.buyer-side", "buyer_side", 0, BOTH,
      lambda fd: _live(fd) and fd["conformity"]["established"] == "conforms" and fd["manipulation"]["known_none"] and fd["within_mandate"]["known"]
      and not fd["within_mandate"]["breaches_recognised"] and fd["evidence"]["mandate_and_log_produced"],
      lambda fd: O("buyer", "deny", "AG5" if (fd["buyer"]["intent_matched"] or not fd["buyer"]["claim_truthful"]) else "AG2",
                   finding="conforming, not manipulative, inside the explicit Mandate: the buyer bears it (unstated intent is the user's risk)"),
      "Step 4. The delivery conforms, the offer was not manipulative and the agent stayed inside the explicit Mandate: the buyer bears the outcome (AG2 authorised but wrong; AG5 user error, change of mind, friendly fraud).",
      needs=["offer_snapshot", "delivery_evidence_bundle", "signed_mandate"], judgment=["what_the_buyer_meant"], min_level=3),
]


def _auth_outcome(fd):
    p = fd["authorisation"]["problems"]
    if "provider_compromised" in p or "no_strong_auth" in p:
        return O("agent_provider", "refund", "AG0", goods_return=_ret(fd), finding=f"authorisation failed: {', '.join(p)}")
    if "replayed_by_merchant" in p or "merchant_initiated_after_expiry" in p:
        return O(fd["responding_party_liable"], "partial" if _frac(fd) < 1 else "refund", "AG0", fd, finding=f"charge not initiated by the agent under a live Mandate: {', '.join(p)}")
    return O("rail_unauthorised_regime", "refer", "AG0", finding=f"Mandate not authorised by the account holder: {', '.join(p)}")


def _conduct_outcome(fd):
    t = fd["evidence"]["tampered_by"]
    if t == "buyer":
        return O("buyer", "deny", "ABS-C1", finding="buyer submitted altered evidence")
    if t == "merchant":
        return O(fd["responding_party_liable"], "refund", "ABS-C1", goods_return=_ret(fd), finding="merchant submitted altered evidence")
    return O("agent_provider", "partial" if _frac(fd) < 1 else "refund", "ABS-C1", fd, goods_return=False, finding="agent provider's record chain broken")


def _conformity_outcome(fd):
    c = fd["conformity"]
    kinds = set(c["kinds"])
    liable = fd["responding_party_liable"]
    if fd["version"] == "v0.1":
        return O(liable, "refund", "AG3", goods_return=_ret(fd), finding=f"non-conformity: {', '.join(sorted(kinds)) or 'delivered item differs from the Offer Snapshot'}")
    if kinds and kinds <= CURE_KINDS:
        return O(liable, "cure", "AG3", fraction=0.0, finding="non-conformity of invoice terms; cure by corrected document")
    if kinds == {"late"}:
        return O(liable, "late_remedy", "AG3", fraction=0.1, goods_return=False, finding="late delivery only; goods conform")
    if c["overall_partial"] or (kinds & PARTIAL_KINDS and _frac(fd) < 1):
        return O(liable, "partial", "AG3", fd, goods_return=False, finding=f"partial non-conformity: {', '.join(sorted(kinds))}")
    return O(liable, "refund", "AG3", goods_return=_ret(fd), finding=f"non-conformity: {', '.join(sorted(kinds))}")


def _agent_outcome(fd):
    b = set(fd["within_mandate"]["breaches_recognised"])
    if fd["version"] != "v0.1":
        if b <= CURE_BREACHES:
            return O("agent_provider", "cure", "AG1-P", fraction=0.0, finding="invoice data required by the Mandate not passed; cure by corrected document")
        if b <= NO_LOSS_BREACHES:
            return O("agent_provider", "deny", "AG1-P", fraction=0.0, finding="policy breach without a refundable loss; finding recorded on the scoreboard")
    partial = b <= {"amount", "units", "currency", "monthly_budget", "role", "policy_version", "scope", "required_attributes", "approval"} and _frac(fd) < 1
    return O("agent_provider", "partial" if partial else "refund", "AG1-P", fd, goods_return=_ret(fd) and not partial,
             finding=f"hard limit broken: {', '.join(sorted(b))}")


# Proposed additions that are not liability rules (process, settlement, overlays, data). The engine
# applies them as findings; the report lists them as wording for the ABS author.
PROPOSED_PROCESS_TEXT = {
    "ABS-4.1b.remedy-granularity": "Amend 4 Step 1 remedy: 'Refund of the non-conforming lines; where the conforming part has no stand-alone use for the buyer (bundle), full refund with return at the merchant's cost. For late delivery of conforming goods the buyer may reject within 14 days of the late delivery (full refund, return at the merchant's cost) or keep the goods and recover the delivery charge. For a non-conformity of documents (invoice, e-invoice, VAT treatment) the remedy is a corrected document (cure), not a refund.'",
    "ABS-2.3.mandate-fields": "Amend 2.1: the Mandate also holds, each as an explicit hard limit when set: required attributes (colour, size, model, dates, reference, deadline); a scope flag ('only the item named', on by default); the pay-in currency and an FX tolerance; the delivery address; whether a step-up is required and the exact content an approval prompt must show (item and amount); the autonomy level (autonomous / notify-and-hold / approval required / never) per category; per-transaction and periodic budgets; delegate roles and limits; invoice data (PO number, VAT ID, e-invoice format) and payment terms for business buyers; procurement thresholds and framework allowlists for public buyers; the minimum merchant Trust Attestation level; for recurring purchases the period and maximum number of charges; a version, with changes taking effect when the agent acknowledges them. Only an encoded limit is a hard limit; unstated intent stays with the user. Mandate creation requires strong authentication of the account holder by a PSP; a Mandate without it is invalid (Step 0).",
    "ABS-3.2.delivery-evidence": "Amend 3 (E3): there is no carrier content inspection. The delivery evidence bundle is: carrier proof of delivery (handover only), the merchant's packing record (serials, weight, photo at packing), the buyer's unboxing photos, serial numbers, the digital access log for digital goods and subscriptions, the completion record for services, the ticket issuance and use log for travel, the handover and return inspection records for rentals, and the return inspection record for returns. The minimum package for a decidable not-as-described case is: Offer Snapshot + packing record + buyer photos or return inspection, with serials where the goods carry them.",
    "ABS-3.4.evidence-weighing": "New 3.4: (a) carrier proof of delivery proves handover, never content; (b) a packing record with serials matching the Offer Snapshot, unopposed by buyer photos or a return inspection, establishes conformity; (c) buyer photos showing non-conformity on a unit whose serial matches the packing record establish non-conformity; (d) where the packing record and the photographed serial conflict and no record keeper is at fault, the engine returns 'review' (6.5a).",
    "ABS-5.3.rail-execution": "Amend 5.2: a Settlement Instruction is executed by the liable party as a NEW payment on every rail: card (merchant refund through the acquirer; a sponsored push-to-card credit for a third party), wallet (operator reversal), A2A push including SEPA CT/Inst, FPS, UPI, Pix and open-banking PIS (new credit transfer: pain.001/pacs.008; no recall, return or reversal is an ABS mechanism: camt.056 belongs to the payer's PSP for duplicate, technical error or fraud, a customer-reason recall needs the payee's consent, SCT Inst has no return, camt.027/087 are fund inquiries), BNPL (refund through the provider), marketplace (platform PSP reverses the held split), stored value (re-credit), stablecoin (on-chain return transfer), public authority (its own refund process). Against a merchant that refuses, the only route is the contractual collection right of its licensed PSP/acquirer or of the buyer (5.6); the Settlement Instruction never names the arbiter or the programme as payer or payee.",
    "ABS-5.4.payout-hold": "New 5.4: ABS holds no funds. A payout hold exists only where a licensed PSP is itself the payee: card acquiring, platform collection accounts, and A2A acquiring where the merchant is paid later under the acquiring contract. Funds credited to a merchant's own payment account cannot be held (they must be at the payee's disposal immediately). Where the model allows it, the payee PSP holds the payout for merchants in probation (first 90 days or below the trust threshold) and for prepaid orders with delivery more than 14 days out, until the delivery evidence bundle confirms delivery plus a 7-day inspection window, and keeps a rolling reserve. Where it does not, ABS states that the buyer bears the merchant's default and says so before the purchase.",
    "ABS-5.5.parallel-rights-and-reconciliation": "New 5.5: Opening a Dispute Case never waives, assigns or suspends the buyer's dispute rights with its issuer, wallet operator or PSP, and ABS never initiates a card dispute: only the issuer does, at the cardholder's request. The Decision Center supplies the Decision as evidence on request. A refund under a Decision is set off against any later rail recovery on the same payment so that the buyer is made whole once. Deadline guard: before a scheme time limit (for example 120 days from the last expected delivery for merchandise not received, at most 540 days from processing, per the card rules cited in Audit 2; verify per scheme) the Decision issues or the buyer is told to file with the issuer; ABS deadlines pause while a rail dispute runs.",
    "ABS-5.6.enforcement": "New 5.6: A Settlement Instruction unpaid after 10 days is collected by the merchant's licensed PSP or acquirer in its own right under the Participation Agreement (reserve, debit, set-off), or claimed by the buyer directly; the programme and the arbiter never receive or pay money. Failing collection the merchant is suspended from the Register and the buyer is told which statutory and rail routes remain. No guarantee payout is promised in the normative rules.",
    "ABS-6.5a.decision-center": "New 6.5a: The Decision Center runs the decision order deterministically on typed findings and issues a Decision receipt (findings, rules fired, decision, remedy, Settlement Instruction, hash). Findings that need judgment come from a fact-finder as typed inputs with a confidence. Any party may request human review of any Decision within 10 days; a person who did not take part in the automated decision reviews it and may confirm, change or send the case to appeal. The engine escalates on its own when a finding cannot be established.",
    "ABS-6.6.appeal": "Amend 6.5: 'The decision is final within the programme, save for one appeal within 10 days on new evidence not available to the appellant or on a procedural error. Disagreement alone is not a ground. Statutory routes (court, ADR) remain.'",
    "ABS-6.9.statutory-rights": "New 6.9: Time limits and decisions under ABS do not reduce the buyer's statutory rights (withdrawal, conformity guarantee, unauthorised-payment protection). The Decision states which statutory route remains open; where the EU 14-day withdrawal right applies and the buyer invokes it, the Settlement Instruction executes the withdrawal refund on the same rail.",
    "ABS-8.data": "New 8 (Data): The parties keep the Dispute Case records until the decision and appeal window close plus the statutory limitation period; erasure requests are deferred for that period; access requests are served with the evidence bundle minus third-party data. No card data enters the agent context: agents pay with network tokens or mandate-bound credentials only; a merchant checkout that requests card data from an agent breaches its Participation Agreement.",
    "ABS-1.7.trust-attestation": "New 1.7 (roadmap): The programme publishes a Trust Attestation for every Register entry (score and components: identity verified, payout name match, domain age, review authenticity, delivery history, dispute rate, ad-burst and price-anomaly signals). Agents read it before comparing offers and must not buy below the Mandate's minimum; a price far below market or an ad burst triggers a step-up, not a block, when the score is high.",
    "ABS-1.8.entry-gate": "New 1.8 (roadmap): Entry to the Register requires KYB (registry, beneficial owner, payout account in the entity's name, domain ownership, brand-similarity screen, LEI where available, MCC), a shared blocklist check (beneficial owners, payout accounts, devices, domains of expelled merchants), a 90-day probation with a payee-PSP payout hold where the model allows it (card acquiring, collection accounts, A2A acquiring) and volume caps, continuous monitoring (non-delivery rate, catalogue/MCC drift, prepaid-order velocity against a seasonal baseline), and per-purchase re-attestation of the merchant's status and of the Offer Feed signature. The programme does not claim to keep every scammer out; it claims that an unproven merchant is not paid before delivery where a payee PSP holds the payout, and says plainly where no hold is possible (merchant-account A2A, stablecoin).",
    "ABS-2.5.contract-formation": "New 2.5: The contract is formed when the agent accepts the Offer Snapshot and the payment is authorised. Cancellation by the merchant afterwards (stale stock) is non-delivery (Step 1); a substitute needs a new Offer Snapshot accepted inside the Mandate.",
    "ABS-2.6.idempotency": "New 2.6: Every checkout carries an idempotency key derived from the Mandate id and the cart hash. A duplicate capture against one key is the merchant's (Step 1, quantity/price); a duplicate order from the agent's retry without a key is the agent provider's (Step 3).",
    "ABS-2.7.negotiation-record": "New 2.7 (agent-to-agent): Terms agreed between a buyer-agent and a seller-agent bind only when written into a negotiation record signed by both agents and hashed into the Offer Snapshot. Statements by the seller-agent are merchant-controlled content for Step 2.",
    "ABS-1.5b.responding-party": "New 1.5b (marketplaces): The Participation Agreement names the responding party for each line: the third-party seller for its goods and conduct; the platform for its own feed, fees, catalogue merges and hosting duties, and as guarantor of last resort for refunds from the held split.",
    "ABS-9.enforcement-layer": "New 9 (allowances): Where an Allowance limit is encoded in the mandate-bound credential and the payment-side control fails to decline a breaching payment, the agent provider remains liable to the buyer and has recourse against the enforcement layer under the credential agreement; the buyer is never left to pursue the enforcement layer.",
}

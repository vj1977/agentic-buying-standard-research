# ABS scenario catalogue

Version 0.1.0. 528 scenarios from 192 event types, generated deterministically by `generate.py` (combinatorial base plus curated edge cases). The machine-readable file is `catalogue.json`; the rule simulation in `standard/sim/` reads each scenario's `facts` block and compares its Decision with `ground_truth`.

Note: standard/ABS_v0.1.md was written in parallel with this catalogue and appeared before the final run; object names were checked against it and match (Participation Agreement, Mandate, Offer Snapshot, Purchase Record, Settlement Instruction, Delivery Record, Dispute Case, Decision Receipt, Trust Attestation). Reason codes AG0-AG5 and AG1-P/AG1-M match its A3/A4; ABS-* codes here are proposals this simulation adds. The brief's 'Offer Feed' is ABS v0.1's offer feed / Offer Specification (B2); 'allowance' here is its Allowance Policy (B3); the minimum evidence package is its Evidence Package (A5).

## Record shape

Every scenario carries: `id`, `stages`, `parties` (honest / mistaken / malicious per party), `rail` and `rail_family`, `goods`, `mandate` (with strong-authentication status, required attributes, minimum merchant trust), `offer` (Offer Feed and Offer Snapshot properties), `what_happened`, `facts` (typed inputs for the rule engine), `evidence` (items available at E0..E3), `ground_truth` (liable party, remedy, reason code, basis, certainty), `expected_settlement` (Settlement Instruction for the rail), `consumer_overlay`, `tags`, `abs_objects`.

Certainty levels in `ground_truth.certainty`: `principle` (follows the founder's stated principles), `general_law` (a general statement of consumer or payment law, no rule numbers, verify before citing), `uncertain`, `debatable`, `design_proposal` (the catalogue proposes the rule because ABS v0.1 has none).

## Core and roadmap

The dispute, evidence and liability core is primary: classes `merchant_failure`, `agent_failure`, `user_side`, `attack`, `dispute_process`, `overlay`, `lifecycle` (dispute taxonomy, the liability decision order by Mandate precision, the minimum evidence standard with realistic delivery evidence, Decision Center escalation and human review, settlement mapping). Classes `anti_scam`, `entry_route`, `product_spec`, `allowance` and `segment` are roadmap families: kept in the catalogue and run through the same engine, reported briefly in `standard/sim/REPORT.md`.

Liability rule applied throughout (Audit 0): an explicit Mandate or Allowance breach makes the agent provider liable; conforming to the explicit Mandate but not the unstated intent puts it on the user; a non-conforming delivery makes the merchant liable; an injected or manipulative offer makes the merchant liable. Delivery evidence is realistic: carrier proof of delivery without content inspection, the merchant's packing record with serials, buyer photos, digital logs, return inspection, with missing and conflicting states. Escrow means a payout hold by a licensed PSP/acquirer that is itself the payee (card acquiring, platform collection accounts, A2A acquiring); funds credited to a merchant's own account cannot be held, and ABS never holds funds. The buyer's card dispute rights stay available in parallel and are never assigned; only the issuer opens a dispute. Human review is available on request for any Decision.

## Counts

### By class

| key | n |
|---|---|
| agent_failure | 34 |
| allowance | 41 |
| anti_scam | 36 |
| attack | 61 |
| dispute_process | 53 |
| entry_route | 34 |
| lifecycle | 24 |
| merchant_failure | 55 |
| overlay | 45 |
| product_spec | 47 |
| segment | 71 |
| user_side | 27 |

### By rail family

| key | n |
|---|---|
| a2a_push | 222 |
| bnpl | 34 |
| card | 150 |
| crypto | 34 |
| marketplace | 30 |
| stored_value | 25 |
| wallet | 33 |

### By rail

| key | n |
|---|---|
| bnpl | 34 |
| card_credit_3ds | 47 |
| card_cross_border_dcc | 37 |
| card_debit_3ds | 34 |
| card_on_file_token | 32 |
| crypto_stablecoin_x402 | 34 |
| gift_card_stored_value | 25 |
| marketplace_split | 30 |
| open_banking_pis | 31 |
| pix | 31 |
| sepa_ct | 35 |
| sepa_instant | 59 |
| uk_fps | 34 |
| upi | 32 |
| wallet | 33 |

### By goods

| key | n |
|---|---|
| bundle | 58 |
| custom_made | 49 |
| digital | 32 |
| multi_merchant_basket | 28 |
| perishable | 35 |
| physical | 172 |
| pre_order | 46 |
| rental | 25 |
| service | 39 |
| subscription | 22 |
| travel_ticket | 22 |

### By ground-truth liable party

| key | n |
|---|---|
| agent_provider | 124 |
| buyer | 98 |
| merchant | 239 |
| merchant+agent_provider | 12 |
| none | 42 |
| platform | 2 |
| rail_unauthorised_regime | 4 |
| register_operator | 5 |
| undetermined | 2 |

### By ground-truth remedy

| key | n |
|---|---|
| apportioned | 4 |
| cure | 14 |
| deny | 97 |
| human_review | 2 |
| inadmissible | 9 |
| joint_refund | 8 |
| merchant_claim_upheld | 3 |
| no_dispute | 21 |
| no_transaction | 9 |
| refer_to_administrative_appeal | 3 |
| refer_to_rail | 4 |
| refund_full | 121 |
| refund_partial | 91 |
| reject_or_refund_delivery_cost | 2 |
| return_and_refund | 140 |

### By reason code

| key | n |
|---|---|
| ABS-D1 | 3 |
| ABS-D2 | 3 |
| ABS-E1 | 7 |
| ABS-F1 | 4 |
| ABS-G1 | 3 |
| ABS-H1 | 2 |
| ABS-M1 | 4 |
| ABS-M2 | 5 |
| ABS-OK | 21 |
| ABS-P1 | 17 |
| ABS-P2 | 5 |
| ABS-R1 | 4 |
| ABS-S1 | 6 |
| ABS-T1 | 7 |
| ABS-T2 | 2 |
| ABS-X1 | 8 |
| ABS-X2 | 4 |
| AG0 | 18 |
| AG1-M | 17 |
| AG1-P | 86 |
| AG2 | 14 |
| AG3 | 186 |
| AG4 | 16 |
| AG4-D | 5 |
| AG5 | 81 |

### By origin

| key | n |
|---|---|
| base | 373 |
| coverage_class_goods | 7 |
| coverage_class_rail | 9 |
| coverage_irrevocable | 32 |
| coverage_reversible | 47 |
| curated | 60 |

### By commerce segment

| key | n |
|---|---|
| A2A | 13 |
| B2B | 23 |
| B2B2C | 31 |
| B2C | 424 |
| B2G | 10 |
| C2C | 13 |
| C2G | 14 |

### By lifecycle stage (a scenario can span several)

| key | n |
|---|---|
| appeal | 7 |
| checkout | 273 |
| comparison | 36 |
| decision | 422 |
| decision_settlement | 405 |
| delivery | 398 |
| discovery | 41 |
| dispute_tier1 | 390 |
| dispute_tier2 | 412 |
| fulfilment | 199 |
| mandate_creation | 59 |
| onboarding | 62 |
| payment | 261 |
| return | 33 |
| settlement | 15 |
| step_up | 47 |

## Event types

| id | class | name | parties (user/agent/merchant/third) | ground truth | n |
|---|---|---|---|---|---|
| M01 | merchant_failure | not_as_described_spec | honest/honest/mistaken/- | merchant / return_and_refund / AG3 | 2 |
| M02 | merchant_failure | not_as_described_colour | honest/honest/mistaken/- | merchant / return_and_refund / AG3 | 2 |
| M03 | merchant_failure | not_as_described_model | honest/honest/mistaken/- | merchant / return_and_refund / AG3 | 3 |
| M04 | merchant_failure | not_as_described_size | honest/honest/mistaken/- | merchant / return_and_refund / AG3 | 2 |
| M05 | merchant_failure | quantity_short | honest/honest/mistaken/- | merchant / return_and_refund / AG3 | 2 |
| M06 | merchant_failure | condition_used_sold_as_new | honest/honest/malicious/- | merchant / return_and_refund / AG3 | 3 |
| M07 | merchant_failure | missing_parts | honest/honest/mistaken/- | merchant / return_and_refund / AG3 | 2 |
| M10 | merchant_failure | wrong_item | honest/honest/mistaken/- | merchant / return_and_refund / AG3 | 3 |
| M11 | merchant_failure | counterfeit | honest/honest/malicious/- | merchant / return_and_refund / AG3 | 3 |
| M08 | merchant_failure | not_received | honest/honest/mistaken/- | merchant / refund_full / AG3 | 2 |
| M08b | merchant_failure | not_received_merchant_claims_delivered | honest/honest/malicious/- | merchant / refund_full / AG3 | 3 |
| M09 | merchant_failure | late_delivery_goods_kept | honest/honest/mistaken/- | merchant / reject_or_refund_delivery_cost / AG3 | 2 |
| M12 | merchant_failure | listing_changed_after_purchase | honest/honest/malicious/- | merchant / return_and_refund / AG3 | 4 |
| M13 | merchant_failure | hidden_fee_at_checkout | honest/honest/malicious/- | merchant / refund_partial / AG1-M | 3 |
| M14 | merchant_failure | wrong_delivery_cost | honest/honest/mistaken/- | merchant / refund_partial / AG1-M | 3 |
| M15 | merchant_failure | price_changed_at_checkout | honest/honest/malicious/- | merchant / refund_partial / AG1-M | 3 |
| M16 | merchant_failure | out_of_stock_substitution | honest/honest/mistaken/- | merchant / return_and_refund / AG3 | 2 |
| M17 | merchant_failure | partial_shipment | honest/honest/mistaken/- | merchant / refund_partial / AG3 | 3 |
| M18 | merchant_failure | damaged_in_transit | honest/honest/honest/carrier | merchant / return_and_refund / AG3 | 3 |
| M19 | merchant_failure | merchant_insolvent_after_payment | honest/honest/mistaken/- | merchant / refund_full / AG3 | 5 |
| M20 | attack | fake_store_vanished | honest/honest/malicious/- | agent_provider / refund_full / ABS-P1 | 5 |
| A01 | agent_failure | misread_mandate_bought_unrequested_item | honest/mistaken/honest/- | agent_provider / refund_full / AG1-P | 3 |
| A02 | agent_failure | overspend | honest/mistaken/honest/- | agent_provider / refund_partial / AG1-P | 5 |
| A03 | agent_failure | wrong_variant_required_attribute | honest/mistaken/honest/- | agent_provider / return_and_refund / AG1-P | 3 |
| A03b | agent_failure | wrong_variant_preference_only | honest/mistaken/honest/- | buyer / deny / AG2 | 2 |
| A04 | agent_failure | duplicate_purchase_units_exceeded | honest/mistaken/honest/- | agent_provider / refund_partial / AG1-P | 4 |
| A05 | agent_failure | non_allowed_merchant | honest/mistaken/honest/- | agent_provider / return_and_refund / AG1-P | 2 |
| A06 | agent_failure | ignored_step_up | honest/malicious/honest/- | agent_provider / return_and_refund / AG1-P | 3 |
| A07 | agent_failure | hallucinated_requirement_added_item | honest/mistaken/honest/- | agent_provider / refund_partial / AG1-P | 3 |
| A08 | attack | followed_injection_in_listing | honest/honest/malicious/- | merchant / refund_partial / AG4 | 3 |
| A09 | agent_failure | too_cautious_false_decline | honest/mistaken/honest/- | none / no_transaction / ABS-M1 | 2 |
| A10 | agent_failure | unnecessary_ask_task_abandoned | honest/mistaken/honest/- | none / no_transaction / ABS-M1 | 2 |
| A01b | agent_failure | unstated_intent_bought_other_item_in_category | honest/mistaken/honest/- | buyer / deny / AG2 | 3 |
| A07b | agent_failure | hallucinated_requirement_no_scope_flag | honest/mistaken/honest/- | buyer / deny / AG2 | 2 |
| D14a | dispute_process | nad_claim_no_buyer_photos_merchant_records_match | mistaken/honest/honest/- | buyer / deny / AG5 | 2 |
| D14b | dispute_process | nad_claim_no_photos_merchant_has_no_packing_record | honest/honest/mistaken/- | merchant / return_and_refund / AG3 | 3 |
| D15 | dispute_process | conflicting_evidence_serial_mismatch | honest/honest/honest/unknown | undetermined / human_review / ABS-H1 | 2 |
| D15b | dispute_process | conflicting_evidence_return_inspection_resolves | honest/honest/honest/- | merchant / return_and_refund / AG3 | 3 |
| U01 | user_side | vague_instruction_literal | mistaken/honest/honest/- | buyer / deny / AG5 | 4 |
| U02 | user_side | contradictory_instruction_agent_guessed | mistaken/mistaken/honest/- | buyer / deny / AG2 | 4 |
| U03 | user_side | changed_mind | honest/honest/honest/- | buyer / deny / AG5 | 7 |
| U04 | user_side | friendly_fraud_not_received | malicious/honest/honest/- | buyer / deny / AG5 | 2 |
| U05 | user_side | friendly_fraud_not_as_described | malicious/honest/honest/- | buyer / deny / AG5 | 4 |
| U06 | attack | account_takeover_user | honest/honest/honest/attacker | rail_unauthorised_regime / refer_to_rail / AG0 | 4 |
| U07 | attack | agent_session_takeover | honest/mistaken/honest/attacker | agent_provider / refund_full / AG1-P | 4 |
| U08 | user_side | shared_device_household_member | mistaken/honest/honest/- | buyer / deny / AG5 | 4 |
| U09 | user_side | minor_used_account | mistaken/honest/honest/- | buyer / deny / AG5 | 2 |
| X01 | attack | injection_in_offer_feed | honest/honest/malicious/- | merchant / refund_full / AG4 | 4 |
| X02 | attack | injection_in_hosted_reviews | honest/honest/malicious/- | merchant / refund_partial / AG4 | 2 |
| X03 | attack | dark_pattern_preselected_addon | honest/honest/malicious/- | merchant / refund_partial / AG1-M | 2 |
| X04 | attack | dark_pattern_fake_reference_price | honest/honest/malicious/- | merchant / refund_partial / AG4-D | 3 |
| X05 | attack | dark_pattern_false_scarcity | honest/honest/malicious/- | merchant / refund_partial / AG4-D | 2 |
| X06 | attack | merchant_agent_collusion | honest/malicious/malicious/- | merchant+agent_provider / joint_refund / ABS-X1 | 4 |
| X07 | attack | fake_merchant_spoofed_participation | honest/honest/malicious/- | register_operator / refund_full / ABS-P2 | 5 |
| X08 | attack | evidence_tampering_merchant | honest/honest/malicious/- | merchant / return_and_refund / AG3 | 2 |
| X09 | attack | evidence_tampering_agent_provider | honest/malicious/honest/- | agent_provider / refund_partial / AG1-P | 3 |
| X10 | attack | evidence_tampering_buyer | malicious/honest/honest/- | buyer / deny / AG5 | 2 |
| X11 | attack | replayed_mandate_by_merchant | honest/honest/malicious/- | merchant / refund_partial / AG0 | 5 |
| X12 | attack | mitm_on_offer_feed | honest/mistaken/honest/attacker | agent_provider / refund_full / ABS-F1 | 3 |
| X13 | attack | kickback_steering | honest/malicious/honest/- | agent_provider / refund_partial / ABS-X2 | 4 |
| X14 | attack | compromised_agent_provider | honest/mistaken/honest/attacker | agent_provider / refund_full / AG0 | 2 |
| X15 | attack | feed_requests_card_data | honest/honest/malicious/- | buyer / deny / AG5 | 2 |
| D01 | dispute_process | both_honest_disagree_ambiguous_offer | honest/honest/honest/- | merchant / return_and_refund / AG3 | 4 |
| D02 | dispute_process | evidence_missing_provider_silent | honest/mistaken/honest/- | agent_provider / refund_full / ABS-E1 | 2 |
| D03 | dispute_process | partial_liability_two_faults | honest/mistaken/mistaken/- | merchant+agent_provider / apportioned / ABS-R1 | 4 |
| D04 | dispute_process | split_shipment_one_parcel_lost | honest/honest/honest/carrier | merchant / refund_partial / AG3 | 3 |
| D05 | dispute_process | second_dispute_same_record_no_new_facts | mistaken/honest/honest/- | none / inadmissible / ABS-T2 | 2 |
| D06 | dispute_process | time_limit_passed | honest/honest/honest/- | none / inadmissible / ABS-T1 | 6 |
| D07 | dispute_process | tier1_settles_partial | honest/honest/mistaken/- | merchant / refund_partial / AG3 | 3 |
| D08 | dispute_process | merchant_no_response_escalates | honest/honest/mistaken/- | merchant / refund_full / ABS-D1 | 3 |
| D09 | dispute_process | appeal_on_new_evidence | honest/honest/honest/- | merchant / return_and_refund / AG3 | 3 |
| D09b | dispute_process | appeal_mere_disagreement | mistaken/honest/honest/- | buyer / deny / AG5 | 2 |
| D10 | dispute_process | parallel_chargeback_filed | mistaken/honest/honest/- | merchant / return_and_refund / AG3 | 3 |
| D11 | dispute_process | merchant_claim_rental_damage | mistaken/honest/honest/- | buyer / merchant_claim_upheld / ABS-D2 | 3 |
| D12 | dispute_process | return_shipment_lost | honest/honest/honest/carrier | merchant / return_and_refund / AG3 | 3 |
| D13 | dispute_process | return_refused_as_used | honest/honest/mistaken/- | merchant / return_and_refund / AG3 | 2 |
| R01 | overlay | withdrawal_14d_conforming_goods | honest/honest/honest/- | buyer / deny / AG5 | 2 |
| R02 | overlay | withdrawal_excepted_custom_made | honest/honest/honest/- | buyer / deny / AG5 | 3 |
| R03 | overlay | withdrawal_excepted_perishable | honest/honest/honest/- | buyer / deny / AG5 | 2 |
| R04 | overlay | withdrawal_excepted_digital_unsealed | honest/honest/honest/- | buyer / deny / AG5 | 2 |
| R05 | overlay | withdrawal_excepted_date_specific | honest/honest/honest/- | buyer / deny / AG5 | 4 |
| R06 | overlay | b2b_buyer_no_withdrawal | honest/honest/honest/- | buyer / deny / AG5 | 2 |
| R08 | overlay | uk_app_fraud_fake_store | honest/honest/malicious/- | agent_provider / refund_full / ABS-P1 | 1 |
| R09 | overlay | gdpr_erasure_mid_dispute | honest/honest/honest/- | merchant / return_and_refund / AG3 | 3 |
| R10 | overlay | gdpr_access_request_evidence | honest/honest/honest/- | buyer / deny / AG2 | 2 |
| R12 | overlay | provider_outage_agent_retry_duplicate | honest/mistaken/honest/- | agent_provider / refund_partial / AG1-P | 4 |
| R12b | overlay | provider_outage_merchant_double_capture | honest/honest/mistaken/- | merchant / refund_partial / AG3 | 3 |
| R13 | overlay | provider_outage_record_lost | honest/mistaken/honest/- | agent_provider / refund_full / ABS-E1 | 3 |
| R14 | overlay | dcc_markup_agent_accepted | honest/mistaken/honest/- | agent_provider / refund_partial / AG1-P | 1 |
| R14b | overlay | dcc_markup_merchant_default | honest/honest/malicious/- | merchant / refund_partial / AG1-M | 1 |
| R15 | overlay | duties_not_in_landed_cost | honest/honest/mistaken/- | merchant / refund_partial / AG1-M | 2 |
| R15b | overlay | duties_disclosed_payable_on_import | honest/honest/honest/- | buyer / deny / AG5 | 2 |
| R16 | overlay | statutory_guarantee_after_abs_window | honest/honest/honest/- | none / inadmissible / ABS-T1 | 3 |
| R17 | overlay | recurring_charge_after_mandate_expiry | honest/honest/mistaken/- | merchant / refund_full / AG0 | 5 |
| L01 | lifecycle | non_participant_merchant_bought | honest/mistaken/honest/- | agent_provider / refund_full / ABS-P1 | 2 |
| L03 | lifecycle | stale_stock_cancelled_before_shipping | honest/honest/mistaken/- | merchant / refund_full / AG3 | 3 |
| L04 | lifecycle | mandate_without_strong_auth | honest/mistaken/honest/- | agent_provider / refund_full / AG0 | 2 |
| L05 | lifecycle | comparison_not_cheapest_no_fault | honest/honest/honest/- | buyer / deny / AG5 | 3 |
| L06 | lifecycle | clean_purchase_no_dispute | honest/honest/honest/- | none / no_dispute / ABS-OK | 3 |
| L07 | lifecycle | step_up_approved_clean | honest/honest/honest/- | none / no_dispute / ABS-OK | 3 |
| L08 | lifecycle | payment_declined_by_mandate_control_correct | honest/mistaken/honest/- | none / no_transaction / ABS-M2 | 3 |
| L09 | lifecycle | merchant_does_not_pay_after_decision | honest/honest/malicious/- | merchant / return_and_refund / AG3 | 5 |
| Z01 | anti_scam | one_hour_shop_social_ads_never_delivers | honest/honest/malicious/- | merchant / refund_full / AG3 | 5 |
| Z02 | anti_scam | cloned_storefront_brand_impersonation | honest/honest/malicious/- | merchant / refund_full / AG3 | 3 |
| Z03 | anti_scam | price_far_below_market_counterfeit | honest/honest/malicious/- | merchant / return_and_refund / AG3 | 3 |
| Z04 | anti_scam | dropshipper_rarely_delivers | honest/honest/malicious/- | merchant / refund_full / AG3 | 2 |
| Z05 | anti_scam | exit_scam_after_building_reputation | honest/honest/malicious/- | merchant / refund_full / AG3 | 5 |
| Z06 | anti_scam | fake_reviews_review_ring | honest/honest/malicious/- | merchant / return_and_refund / AG3 | 3 |
| Z07 | anti_scam | merchant_asks_to_pay_off_platform | honest/honest/malicious/- | agent_provider / refund_full / ABS-P1 | 4 |
| Z08 | anti_scam | merchant_changes_identity_after_disputes | honest/honest/malicious/- | merchant / refund_full / AG3 | 3 |
| Z09 | anti_scam | genuine_new_small_merchant | honest/honest/honest/- | none / no_dispute / ABS-OK | 5 |
| Z10 | anti_scam | genuine_flash_sale_low_price | honest/honest/honest/- | none / no_dispute / ABS-OK | 3 |
| G01 | entry_route | entry_synthetic_business_identity | honest/honest/malicious/- | merchant / refund_full / AG3 | 3 |
| G02 | entry_route | entry_stolen_identity_real_business | honest/honest/malicious/impersonated_business | merchant / refund_full / AG3 | 3 |
| G03 | entry_route | entry_shell_company_nominee | honest/honest/malicious/- | merchant / refund_full / AG3 | 2 |
| G04 | entry_route | entry_payout_account_other_name | honest/honest/malicious/- | merchant / refund_full / AG3 | 3 |
| G05 | entry_route | entry_domain_brand_impersonation | honest/honest/malicious/impersonated_brand | merchant / refund_full / AG3 | 2 |
| G06 | entry_route | entry_transaction_laundering | honest/honest/malicious/legitimate_front_merchant | merchant / refund_full / AG3 | 4 |
| G07 | entry_route | entry_sleeper_then_exit | honest/honest/malicious/- | merchant / refund_full / AG3 | 4 |
| G08 | entry_route | entry_collusion_with_agent_provider | honest/malicious/malicious/- | merchant+agent_provider / joint_refund / ABS-X1 | 4 |
| G09 | entry_route | entry_expelled_merchant_reenters | honest/honest/malicious/- | merchant / refund_full / AG3 | 2 |
| G10 | entry_route | entry_honest_micro_business | honest/honest/honest/- | none / no_dispute / ABS-OK | 2 |
| G11 | entry_route | entry_honest_seasonal_merchant | honest/honest/honest/- | none / no_dispute / ABS-OK | 3 |
| G12 | entry_route | entry_honest_legal_entity_change | honest/honest/honest/- | none / no_dispute / ABS-OK | 2 |
| AL01 | allowance | split_purchases_evade_per_transaction_limit | honest/malicious/honest/- | agent_provider / return_and_refund / AG1-P | 2 |
| AL02 | allowance | monthly_budget_exhausted_mid_basket | honest/mistaken/honest/- | agent_provider / refund_partial / AG1-P | 3 |
| AL03 | allowance | delegate_exceeds_role_encoded | mistaken/mistaken/honest/- | agent_provider / refund_partial / AG1-P | 3 |
| AL03b | allowance | delegate_exceeds_role_not_encoded | mistaken/honest/honest/- | buyer / deny / AG5 | 3 |
| AL04 | allowance | approval_granted_for_x_agent_bought_y | honest/mistaken/honest/- | agent_provider / return_and_refund / AG1-P | 3 |
| AL05 | allowance | approval_fatigue_accurate_prompt | mistaken/honest/honest/- | buyer / deny / AG5 | 2 |
| AL05b | allowance | approval_fatigue_vague_prompt | honest/mistaken/honest/- | agent_provider / return_and_refund / AG1-P | 3 |
| AL06 | allowance | recurring_subscription_policy_forbids | honest/mistaken/honest/- | agent_provider / refund_full / AG1-P | 2 |
| AL07 | allowance | b2b_missing_vat_id_agent | honest/mistaken/honest/- | agent_provider / cure / AG1-P | 3 |
| AL07b | allowance | b2b_e_invoice_not_issued_by_merchant | honest/honest/mistaken/- | merchant / cure / AG3 | 2 |
| AL08 | allowance | cross_border_duties_push_over_landed_limit | honest/mistaken/honest/- | agent_provider / refund_partial / AG1-P | 2 |
| AL09 | allowance | dcc_pushes_total_over_limit | honest/mistaken/honest/- | agent_provider / refund_partial / AG1-P | 1 |
| AL10 | allowance | expired_allowance_control_did_not_decline | honest/mistaken/honest/- | agent_provider / return_and_refund / AG1-P | 2 |
| AL11 | allowance | policy_tightened_mid_purchase_before_ack | mistaken/honest/honest/- | buyer / deny / AG5 | 3 |
| AL11b | allowance | policy_tightened_mid_purchase_after_ack | honest/mistaken/honest/- | agent_provider / refund_partial / AG1-P | 2 |
| AL12 | allowance | never_level_category_bought | honest/mistaken/honest/- | none / no_transaction / ABS-M2 | 2 |
| AL13 | allowance | notify_and_hold_ignored | honest/mistaken/honest/- | agent_provider / return_and_refund / AG1-P | 3 |
| SB01 | segment | b2b_po_number_missing_on_invoice | honest/mistaken/honest/- | agent_provider / cure / AG1-P | 3 |
| SB02 | segment | b2b_reverse_charge_not_applied | honest/honest/mistaken/- | merchant / cure / AG3 | 2 |
| SB03 | segment | b2b_approval_workflow_bypassed | honest/mistaken/honest/- | agent_provider / return_and_refund / AG1-P | 3 |
| SB04 | segment | b2b_e_invoice_schema_rejected | honest/honest/mistaken/- | merchant / cure / AG3 | 2 |
| SB05 | segment | b2b_payment_redirect_injected_iban | honest/mistaken/honest/attacker | agent_provider / refund_full / ABS-F1 | 1 |
| SB06 | segment | b2b_nonconforming_goods_contract_terms | honest/honest/mistaken/- | merchant / return_and_refund / AG3 | 3 |
| SB07 | segment | b2b_net30_terms_agent_prepaid | honest/mistaken/honest/- | agent_provider / deny / AG1-P | 2 |
| SG01 | segment | b2g_above_direct_award_threshold | honest/mistaken/honest/- | agent_provider / return_and_refund / AG1-P | 2 |
| SG02 | segment | b2g_off_framework_supplier | honest/mistaken/honest/- | agent_provider / return_and_refund / AG1-P | 2 |
| SG03 | segment | b2g_e_invoice_format_not_accepted | honest/honest/mistaken/- | merchant / cure / AG3 | 2 |
| SG04 | segment | b2g_audit_trail_missing | honest/mistaken/honest/- | agent_provider / refund_full / ABS-E1 | 2 |
| SG05 | segment | b2g_auditor_disputes_in_mandate_purchase | mistaken/honest/honest/- | buyer / deny / AG5 | 2 |
| SC01 | segment | c2g_fine_paid_twice | honest/mistaken/honest/- | agent_provider / refund_partial / AG1-P | 3 |
| SC02 | segment | c2g_wrong_reference_paid | honest/mistaken/honest/- | agent_provider / refund_full / AG1-P | 2 |
| SC03 | segment | c2g_permit_fee_permit_refused | honest/honest/honest/- | none / refer_to_administrative_appeal / ABS-G1 | 3 |
| SC04 | segment | c2g_tax_paid_late_penalty | honest/mistaken/honest/- | agent_provider / refund_partial / AG1-P | 3 |
| SC05 | segment | c2g_authority_portal_phishing_clone | honest/mistaken/honest/attacker | agent_provider / refund_full / ABS-P1 | 3 |
| SP01 | segment | c2c_private_seller_not_as_described | honest/honest/mistaken/- | merchant / return_and_refund / AG3 | 3 |
| SP02 | segment | c2c_fake_buyer_not_received | malicious/honest/honest/- | buyer / deny / AG5 | 3 |
| SP03 | segment | c2c_seller_vanished_after_payout_released | honest/honest/malicious/- | merchant / refund_full / AG3 | 2 |
| SP04 | segment | c2c_off_platform_payment | honest/mistaken/malicious/- | agent_provider / refund_full / ABS-P1 | 2 |
| SP05 | segment | c2c_counterfeit_peer_listing | honest/honest/malicious/- | merchant / return_and_refund / AG3 | 3 |
| SM01 | segment | marketplace_third_party_seller_non_delivery | honest/honest/malicious/- | merchant / refund_full / AG3 | 1 |
| SM02 | segment | marketplace_platform_aggregated_spec_wrong | honest/honest/mistaken/- | platform / return_and_refund / AG3 | 1 |
| SM03 | segment | marketplace_injection_in_hosted_seller_listing | honest/honest/malicious/- | merchant / refund_partial / AG4 | 1 |
| SM04 | segment | marketplace_platform_fee_not_in_feed | honest/honest/malicious/- | platform / refund_partial / AG1-M | 1 |
| SM05 | segment | marketplace_seller_reregisters_after_disputes | honest/honest/malicious/- | merchant / refund_full / AG3 | 1 |
| SA01 | segment | a2a_seller_agent_promised_discount_snapshot_list_price | honest/honest/mistaken/- | merchant / refund_partial / AG1-M | 2 |
| SA02 | segment | a2a_seller_agent_instructs_buyer_agent | honest/honest/malicious/- | merchant / refund_partial / AG4 | 2 |
| SA03 | segment | a2a_buyer_agent_negotiated_above_cap | honest/mistaken/honest/- | agent_provider / refund_partial / AG1-P | 3 |
| SA04 | segment | a2a_negotiation_record_missing | mistaken/honest/honest/- | buyer / deny / AG5 | 2 |
| SA05 | segment | a2a_seller_agent_changes_delivery_address | honest/honest/malicious/attacker | merchant / refund_full / AG4 | 4 |
| P01 | product_spec | legacy_description_ambiguous_signed_spec_clear | mistaken/honest/honest/- | buyer / deny / AG5 | 3 |
| P02 | product_spec | storage_1tb_marketed_usable_within_tolerance | honest/honest/honest/- | buyer / deny / AG5 | 2 |
| P02b | product_spec | storage_1tb_usable_below_tolerance | honest/honest/mistaken/- | merchant / return_and_refund / AG3 | 3 |
| P03 | product_spec | screen_size_rounding_within_tolerance | honest/honest/honest/- | buyer / deny / AG5 | 2 |
| P03b | product_spec | screen_size_outside_tolerance | honest/honest/mistaken/- | merchant / return_and_refund / AG3 | 3 |
| P04 | product_spec | clothing_size_region_mapped_in_spec | mistaken/honest/honest/- | buyer / deny / AG5 | 2 |
| P04b | product_spec | clothing_size_no_region_ambiguous | honest/honest/mistaken/- | merchant / return_and_refund / AG3 | 3 |
| P05 | product_spec | variant_mismatch_hidden_in_free_text | honest/honest/mistaken/- | merchant / return_and_refund / AG3 | 2 |
| P06 | product_spec | missing_package_contents_vs_spec | honest/honest/mistaken/- | merchant / return_and_refund / AG3 | 2 |
| P07 | product_spec | region_plug_mismatch | honest/honest/mistaken/- | merchant / return_and_refund / AG3 | 3 |
| P07b | product_spec | firmware_region_locked | honest/honest/mistaken/- | merchant / return_and_refund / AG3 | 2 |
| P08 | product_spec | refurbished_sold_as_new_spec | honest/honest/malicious/- | merchant / return_and_refund / AG3 | 2 |
| P08b | product_spec | refurbished_grade_a_like_new_free_text | mistaken/honest/honest/- | buyer / deny / AG5 | 3 |
| P09 | product_spec | photo_contradicts_spec | honest/honest/mistaken/- | merchant / return_and_refund / AG3 | 2 |
| P10 | product_spec | ai_extracted_spec_unconfirmed | honest/mistaken/honest/- | agent_provider / return_and_refund / ABS-S1 | 3 |
| P10b | product_spec | legacy_free_text_only_participant_no_spec | honest/honest/mistaken/- | merchant / return_and_refund / ABS-S1 | 3 |
| P11 | product_spec | merchant_changes_spec_after_sale | honest/honest/malicious/- | merchant / return_and_refund / AG3 | 2 |
| P12 | product_spec | weight_tolerance_within | mistaken/honest/honest/- | buyer / deny / AG5 | 3 |
| P12b | product_spec | weight_tolerance_exceeded | honest/honest/mistaken/- | merchant / return_and_refund / AG3 | 2 |

## Curated edge cases

| id | event | rail | goods | note |
|---|---|---|---|---|
| ABS-C001 | merchant_insolvent_after_payment | sepa_instant | pre_order | A2A acquiring model (the merchant's PSP is the payee and holds the payout): refund from the held funds; feasible |
| ABS-C002 | merchant_insolvent_after_payment | sepa_instant | pre_order | merchant-account model: funds were at the merchant's disposal immediately, so no hold existed despite the 'hold' setting; infeasible |
| ABS-C003 | merchant_insolvent_after_payment | crypto_stablecoin_x402 | digital | on an irrevocable rail the loss is unallocated unless the merchant's PSP was the payee (A2A acquiring) and held the payout, or a reserve exists; a guarantee fund would need a licence |
| ABS-C004 | fake_store_vanished | uk_fps | physical | v0.1 assumes every merchant is a participant and has no rule for this |
| ABS-C005 | fake_store_vanished | card_credit_3ds | physical | card chargeback recovers for the buyer even though the merchant is gone; the acquirer absorbs it |
| ABS-C006 | merchant_agent_collusion | marketplace_split | multi_merchant_basket | v0.1: conforming delivery inside the mandate decides against the buyer |
| ABS-C007 | partial_liability_two_faults | bnpl | physical | v0.1 stops at step 1 and puts everything on the merchant |
| ABS-C008 | partial_liability_two_faults | sepa_instant | bundle | v0.1 stops at step 1 and puts everything on the merchant |
| ABS-C009 | overspend | crypto_stablecoin_x402 | digital | 2% over the cap from a stablecoin price move between quote and settlement; v0.2 proposes an fx_tolerance field in the Mandate |
| ABS-C010 | overspend | card_cross_border_dcc | physical | 0.4% over from FX rounding; strict reading makes the provider liable for cents |
| ABS-C011 | account_takeover_user | sepa_instant | physical | v0.1 has no authorisation step and would decide AG5 against the buyer |
| ABS-C012 | account_takeover_user | card_credit_3ds | bundle | v0.1 has no authorisation step and would decide AG5 against the buyer |
| ABS-C013 | replayed_mandate_by_merchant | card_on_file_token | subscription | v0.1 step 3 asks whether the agent broke a limit; it did not, so v0.1 falls to the buyer |
| ABS-C014 | replayed_mandate_by_merchant | sepa_ct | physical | v0.1 step 3 asks whether the agent broke a limit; it did not, so v0.1 falls to the buyer |
| ABS-C015 | recurring_charge_after_mandate_expiry | card_on_file_token | subscription | v0.1 step 3 asks about the agent only |
| ABS-C016 | recurring_charge_after_mandate_expiry | sepa_ct | subscription | v0.1 step 3 asks about the agent only |
| ABS-C017 | recurring_charge_after_mandate_expiry | upi | subscription | v0.1 step 3 asks about the agent only |
| ABS-C018 | time_limit_passed | card_credit_3ds | physical | pre-order: the clock runs from the promised delivery date |
| ABS-C019 | time_limit_passed | sepa_instant | pre_order | boundary |
| ABS-C020 | time_limit_passed | wallet | physical | day 66 after a day-5 delivery promise (limit day 65): outside the window by one day |
| ABS-C021 | changed_mind | sepa_instant | physical | withdrawal on day 13: inside 14 days; refund by merchant push payment on return |
| ABS-C022 | changed_mind | card_debit_3ds | physical | withdrawal on day 15: outside 14 days; only the merchant's own return policy remains |
| ABS-C023 | changed_mind | bnpl | digital | digital content not yet started: withdrawal still available |
| ABS-C024 | changed_mind | pix | service | service fully performed with consent: withdrawal excepted (general) |
| ABS-C025 | hallucinated_requirement_added_item | card_credit_3ds | physical | contrast with the base A07 where units allow it |
| ABS-C026 | misread_mandate_bought_unrequested_item | wallet | physical | contrast: the same agent error with a loose intent is the buyer's |
| ABS-C027 | kickback_steering | sepa_instant | travel_ticket | v0.1: conforming, inside the mandate, so the buyer bears it; beyond Audit 0's four-way rule, proposed as a conduct duty |
| ABS-C028 | injection_in_offer_feed | crypto_stablecoin_x402 | digital | the Offer Feed record carried agent instructions; schema validation should have rejected it at publication |
| ABS-C029 | mitm_on_offer_feed | open_banking_pis | physical | attribution flips with the signature state |
| ABS-C030 | fake_merchant_spoofed_participation | sepa_instant | physical | v0.1 has no participation verification requirement; Audit 2 LIC-03: no 'the guarantee pays' outcome in the normative rules |
| ABS-C031 | fake_merchant_spoofed_participation | card_credit_3ds | physical | card: chargeback recovers for the buyer; the guarantee question is then between acquirer and programme |
| ABS-C032 | price_changed_at_checkout | upi | physical | the delivery conforms to the Snapshot, so v0.1 step 1 passes; step 2 does not name a price worse than the feed |
| ABS-C033 | hidden_fee_at_checkout | bnpl | bundle | a fee the agent did not choose was added at checkout; manipulative offer |
| ABS-C034 | parallel_chargeback_filed | bnpl | physical | v0.1 has no single-track or double-recovery rule |
| ABS-C035 | feed_requests_card_data | card_on_file_token | subscription | variant: the agent typed the PAN; the conduct breach is the agent provider's; purchase liability unchanged |
| ABS-C036 | provider_outage_agent_retry_duplicate | sepa_instant | perishable | the provider's outage caused a retry without an idempotency key; the duplicate order is the provider's (refund of the duplicate, which goes back) |
| ABS-C037 | provider_outage_merchant_double_capture | pix | physical | the merchant captured one order twice; the Purchase Record shows one order |
| ABS-C038 | merchant_claim_rental_damage | card_credit_3ds | rental | buyer disputes the deposit debit as 'unauthorised'; the handover record shows the damage |
| ABS-C039 | agent_session_takeover | sepa_instant | bundle | v0.1 lists no delivery-address constraint; the goods 'conform' and were 'delivered' |
| ABS-C040 | damaged_in_transit | crypto_stablecoin_x402 | perishable | risk of loss in transit stays with the seller until the consumer has the goods (general statement) |
| ABS-C041 | both_honest_disagree_ambiguous_offer | upi | custom_made | v0.1 has no rule for an indeterminate conformity finding |
| ABS-C042 | listing_changed_after_purchase | wallet | digital | the frozen Offer Snapshot governs; post-purchase edits are disregarded |
| ABS-C043 | merchant_no_response_escalates | sepa_instant | service | v0.1 allows escalation on silence but states no default outcome |
| ABS-C044 | merchant_does_not_pay_after_decision | sepa_instant | physical | refusing merchant on SCT Inst: contractual collection only; no return message exists |
| ABS-C045 | merchant_does_not_pay_after_decision | crypto_stablecoin_x402 | digital | refusing merchant on-chain: no collection mechanism on the rail at all |
| ABS-C046 | merchant_does_not_pay_after_decision | card_credit_3ds | physical | refusing merchant on cards: acquirer collection; the cardholder may also ask the issuer to open a dispute (never initiated by ABS) |
| ABS-C047 | exit_scam_after_building_reputation | sepa_instant | pre_order | A2A acquiring model with a hold on prepaid orders: the loss is recovered from the held funds |
| ABS-C048 | exit_scam_after_building_reputation | sepa_instant | pre_order | merchant-account A2A: no hold is possible; unrecoverable |
| ABS-C049 | exit_scam_after_building_reputation | sepa_instant | pre_order | without a payout hold the loss on an irrevocable rail is unrecoverable |
| ABS-C050 | one_hour_shop_social_ads_never_delivers | card_credit_3ds | physical | card: chargeback recovers; the scam still got in |
| ABS-C051 | one_hour_shop_social_ads_never_delivers | crypto_stablecoin_x402 | digital | stablecoin: unrecoverable without a payout hold |
| ABS-C052 | genuine_new_small_merchant | sepa_instant | physical | min trust 60 blocks an honest 52: false positive |
| ABS-C053 | genuine_new_small_merchant | sepa_instant | physical | min trust 40 passes; in the A2A acquiring model the PSP payout hold delays the honest merchant's payout until delivery |
| ABS-C054 | genuine_flash_sale_low_price | card_credit_3ds | physical | high trust carries a low-price flash sale |
| ABS-C055 | entry_transaction_laundering | sepa_instant | physical | the scam sells through a legitimate participant's account; onboarding sees nothing; monitoring of catalogue/MCC drift and per-purchase re-attestation of the Offer Feed origin limit it |
| ABS-C056 | entry_sleeper_then_exit | sepa_instant | pre_order | A2A acquiring model: a rolling reserve held by the payee PSP bounds the loss |
| ABS-C057 | entry_sleeper_then_exit | sepa_instant | pre_order | merchant-account A2A: no reserve can be held on funds credited to the merchant; loss unbounded until detection |
| ABS-C058 | entry_collusion_with_agent_provider | card_credit_3ds | physical | the merchant is legitimate on paper; the gate cannot see steering; only incentive disclosure, routing audits and price-dispersion monitoring across providers detect it |
| ABS-C059 | merchant_asks_to_pay_off_platform | crypto_stablecoin_x402 | digital | a payment outside the bound credential is outside the mandate by construction |
| ABS-C060 | merchant_changes_identity_after_disputes | sepa_instant | physical | a re-registered identity of an expelled merchant; the shared blocklist (beneficial owner, payout account, device) should refuse re-entry |

## Coverage guarantees

- every event type on at least 2 rails (or all of its permitted rails), on at least one reversible and one irrevocable rail where permitted;
- every (class, rail) pair and every (class, goods) pair that is compatible appears at least once;
- every lifecycle stage, rail, goods type, merchant failure, agent failure, user-side case, attack class, dispute-process case, consumer/regulatory overlay, anti-scam case and scammer entry route in the brief has at least one event type.

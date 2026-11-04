# ABS rule-completeness simulation: report

Catalogue `standard/scenarios/catalogue.json` v0.1.0: **528 scenarios** from 192 event types; 498 are live disputes (a transaction happened and a Dispute Case was opened); 299 belong to the dispute/evidence/liability core, the rest to roadmap families (trust and scams, entry routes, product specification, allowances, segments).

Engine `standard/sim/engine.py` runs two rule sets: `scrolld.abs@0.1` (ABS v0.1 as written, rulebook v1.1) and `scrolld.abs@0.2-proposed` (v0.1 plus the fixes proposed here). Every scenario produces one Decision receipt (typed findings, ordered rules fired, decision, remedy, Settlement Instruction in the rail's own vocabulary, overlays, human-review behaviour, SHA-256 over RFC 8785 canonical JSON). `standard/ABS_v0.1.md` was written in parallel and appeared before the final run: its object names and reason codes (AG0 Step 0, AG1-P, AG1-M, AG2, AG3, AG4, AG5) match the ones used here; `ABS-*` codes are proposals this simulation adds (see `abs_source_note` in the catalogue).

## Headline numbers

| measure | value |
|---|---|
| Live disputes with a determinate outcome on card-dispute evidence alone (E0), v0.2 | 89/498 (17.9%) |
| Live disputes with a determinate outcome by the minimum evidence package (E3: Offer Snapshot + packing record + buyer photos/serials + mandate + action log), v0.2; E3 findings are stipulated (see below) | 496 determinate + 2 escalated of 498 (99.6% determinate; 0 with no applicable rule) |
| Escalated to a fact-finder / human review because records conflict (ABS-H1), v0.2: not decided | 2 |
| Live disputes with no applicable rule even at E3, v0.2 | 0 |
| Same under v0.1 as written: determinate at E0 / determinate by E3 / escalated / no rule | 89 / 477 / 0 / 21 |
| Rule coverage, all scenarios (a rule applies, determinate or escalation): v0.2 / v0.1 | 528/528 / 498/528 |
| All scenarios, v0.2 proposed: determinate / escalated / no rule | 526 / 2 / 0 of 528 |
| All scenarios, v0.1 as written: determinate / escalated / no rule | 498 / 0 / 30 of 528 |
| Consistent with the catalogue's stipulated ground truth: v0.2 / v0.1 | 528/528 / 340/528 |
| Core rules, v0.2: gaps / unresolved conflicts / contradictions with the stipulated ground truth | 0 / 0 / 0 (target zero) |
| Core rules, v0.1 as written: gaps / unresolved conflicts / contradictions | 23 / 4 / 91 |
| Anti-scam (roadmap), of 46 scam cases, with the gate: stopped before purchase / refunded / conditional recovery (uncertain PSP-level reimbursement, never counted as a refund) / unrecoverable | 38 / 5 / 0 / 3 (without gate: 0 / 28 / 3 / 15) |
| Anti-scam buyer loss, nominal per currency (no FX conversion; ranges are conditional recovery): with the gate / without the gate | EUR 938.00; INR 899.00 / EUR 3,425.99; GBP 0.00 to 569.00; INR 899.00; USDC(token; no ISO 4217 code) 458.00 |
| Scammer entry routes: closed / loss-limited / still open | 5 / 3 / 1 |
| Execution feasibility, v0.2, funds-moving instructions only: executable / contractual collection only / infeasible | 334 / 9 / 26 of 369 (v0.1: 224 / 4 / 40 of 268) |
| Instructions that move no funds under ABS, v0.2: corrected document / referred to the rail's unauthorised-payment regime or an authority / deferred (escalated) | 14 / 7 / 2 |
| Disputes the EU withdrawal overlay already resolves regardless of the ABS answer (denied, goods, within 14 days, consumer) | 50 |
| Human review: requested / auto-escalated / share of all scenarios escalated (v0.2) | 73 / 2 / 73/528 (13.8%) |

What this simulation measures: it is a consistency check of the rules against stipulated findings, not a measure of empirical evidence sufficiency. The engine derives its findings from each scenario's stipulated facts; at E3 with sufficient evidence the established conformity is the scenario's stipulated world state (receipt field `findings.conformity.established_from`), not something inferred from independently rendered evidence. Four counts are kept apart: rule coverage (a rule applies), determinate outcome, human escalation (ABS-H1; never counted as decided) and execution feasibility (funds-moving Settlement Instructions only).

How to read the v0.2 numbers: the ground truth and the v0.2 rules were both written in this exercise, so 528/528 consistency shows that the proposed wording is complete and consistent against this catalogue's stipulated judgments (every case reaches a rule, either a determinate outcome or an escalation, and none contradicts the stated principle), not that the judgments are right in law and not that real evidence would establish the findings the rules consume. Ground-truth entries marked `general_law`, `uncertain`, `debatable` or `design_proposal` are the ones to challenge. v0.1 numbers are a measurement of the standard as written.

Reading the decidability number: at E0 the arbiter has what a card dispute has (amount, descriptor, date, item titles, buyer claim, merchant reply with tracking). Non-delivery without a carrier proof of handover is decidable there; everything that turns on the Mandate (E1), the agent's log (E2) or content evidence (E3) is not. Carrier proof of delivery never proves content: the content evidence is the merchant's packing record with serials, the buyer's photos, and the return inspection.

## Post-audit (Audit 1), 2026-11-04

Fixes for `audits/AUDIT_1_INDEPENDENT_AI_REVIEW.md` findings F16 (substring conformity), F17 (determinate vs escalated vs coverage vs feasibility), F25 (uncertain reimbursement) and the simulation part of F26 (tests that test what their names say). Before = this report at commit `0203778`; after = this run.

| headline number | before | after | why |
|---|---|---|---|
| Scenarios (live disputes) | 528 (498) | 528 (498) | unchanged; P04 and P08b now declare their size mapping and condition tolerance instead of hiding them in strings (F16) |
| Live disputes determinate on E0 evidence, v0.2 | 89/498 (17.9%) 'decidable' | 89/498 (17.9%) determinate | unchanged count; now counts determinate outcomes only (F17) |
| Minimum evidence package (E3), v0.2 | 498/498 (100.0%) 'decided', of which 496 determinate and 2 escalated | 496 determinate + 2 escalated of 498 (99.6% determinate); 0 with no rule | an escalation to human review is not a decision; decidable_at no longer counts liable party 'undetermined' as determinate (F17) |
| Undecidable even at E3, v0.2 | 0 | 2 escalated (ABS-H1) + 0 with no rule | same cases, honest label (F17) |
| v0.1: E0 / by E3 / undecidable | 89 / 477 / 21 | 89 / 477 determinate / 0 escalated / 21 no rule | unchanged |
| All scenarios, v0.2: decided / correct | 528/528 / 528/528 | determinate 526, escalated 2, no rule 0; consistent with the stipulated ground truth 528/528 | coverage, determinacy and consistency kept apart (F17) |
| All scenarios, v0.1: decided / correct | 498/528 / 340/528 | determinate 498, escalated 0, no rule 30; consistent 340/528 | relabelled |
| Settlement, v0.2: executable / collection only / infeasible (v0.1) | 357 / 9 / 26 (224 / 4 / 40) | 334 / 9 / 26 of 369 funds-moving (224 / 4 / 40 of 268) | 14 corrected documents, 7 referrals and 2 escalations had been counted as executable funds-moving instructions (F17) |
| Anti-scam with the gate, of 46 scams: stopped / refunded / unrecoverable | 38 / 5 / 3 | 38 / 5 / 0 conditional / 3 | no conditional recovery with the gate on |
| Anti-scam without the gate | 0 / 31 / 15 | 0 / 28 / 3 conditional / 15 | ABS-S0164, ABS-S0310, ABS-C004 (UK Faster Payments; APP reimbursement uncertain) are conditional recovery, not refunds (F25) |
| Buyer loss with the gate | EUR 1,837.00 | EUR 938.00; INR 899.00 | the old total added EUR and INR nominal amounts |
| Buyer loss without the gate | EUR 4,782.99 | EUR 3,425.99; GBP 0.00 to 569.00; INR 899.00; USDC(token; no ISO 4217 code) 458.00 | the old total added EUR, INR and USDC amounts and counted GBP 569.00 of uncertain reimbursement as refunded (F25) |
| Loss moved to acquirer / operator / agent provider / PSPs, with / without the gate | EUR 884.90 / EUR 6,138.90 | EUR 555.90; INR 329.00 / BRL 310.00; EUR 4,296.90; GBP 246.00 to 815.00; INR 329.00; USD(merchant) / EUR(card) 329.00; USDC(token; no ISO 4217 code) 59.00 | per currency; conditional rows give a range (F25) |
| Core rules, v0.2: gaps / unresolved conflicts / contradictions | 0 / 0 / 0 | 0 / 0 / 0 | now each asserted separately, with a v0.1 negative control (F26) |
| Core rules, v0.1: gaps / unresolved conflicts / contradictions | 23 / 4 / 91 | 23 / 4 / 91 | unchanged |
| Human review: requested / auto-escalated / share escalated | 73 / 2 / 73/528 (13.8%) | 73 / 2 / 73/528 (13.8%) | unchanged |
| Entry routes closed / loss-limited / open; EU withdrawal overlay resolves | 5 / 3 / 1; 50 | 5 / 3 / 1; 50 | unchanged |

Scenarios whose outcome changed:

- Decisions: none, in either rule set. With the exact-identifier engine alone, 5 scenarios would flip from buyer/deny to merchant/refund: ABS-S0346 and ABS-S0347 (P04, promised 'EU 42 (= UK 14 = US 10)', delivered 'label UK 14') and ABS-S0360, ABS-S0361, ABS-S0465 (P08b, promised 'refurbished grade A (minor cosmetic marks allowed)', delivered 'refurbished grade A, two faint scratches'). Their signed specs carried the mapping and the tolerance only inside free strings, which the substring matcher happened to accept. They now declare `equivalents: [UK 14, US 10]` and `tolerance: {accept: [refurbished grade A with minor cosmetic marks]}` (raw observation kept in `observed`) and conform, as their stipulated ground truth says. The audit's counterexamples ('iPhone 16 Pro' -> 'iPhone 16'; 'new (not refurbished)' -> 'refurbished') are non-conforming.
- Classification: ABS-S0073 and ABS-S0074 (D15, conflicting serials) were counted as decidable at E3; they are escalated, not determinate, and their settlement is `deferred`, not executable.
- Anti-scam, without the gate: ABS-S0164, ABS-S0310 and ABS-C004 move from refunded to conditional recovery (GBP 120.00, 120.00 and 329.00; buyer loss between nothing and the amount).
- Settlement counting: 23 instructions that move no funds under ABS left the executable count; no instruction itself changed.

Receipts now carry `findings.conformity.established_from` (at E3 with sufficient evidence: `stipulated_world_state`), `matched_by` on each conforming categorical attribute, `settlement_instruction.moves_funds` and the feasibility class `deferred`. In `results.json` the per-version `decided` / `correct` counts are replaced by `covered`, `determinate`, `escalated`, `no_rule` and `consistent`, and anti-scam rows carry loss bounds and their currency. Documents outside `standard/sim` and `standard/scenarios` that quote the old numbers (the paper, `standard/ABS_v0.3.md`) are not changed by this run.

## Core 1. Dispute taxonomy (reason codes) and how often each decides

| code | meaning | liable | decisions v0.1 | decisions v0.2 |
|---|---|---|---|---|
| AG3 | Non-conformity to the Offer Snapshot (incl. non-delivery, counterfeit, late, price, documents) | merchant / platform | 210 | 177 |
| AG4 | Injection via merchant-controlled content (listing, hosted reviews, profile, seller-agent) | merchant | 16 | 16 |
| AG4-D (new) | Deceptive offer content (false reference price, false scarcity) | merchant | - | 5 |
| AG1-M | Merchant-added lines; (v0.2) checkout terms worse than the feed/negotiation record | merchant / platform | 6 | 17 |
| AG1-P | Agent outside an explicit Mandate/Allowance limit | agent provider | 31 | 83 |
| AG2 | Authorised but wrong: inside the explicit Mandate, not the unstated intent | buyer | 53 | 14 |
| AG5 | User error, change of mind, friendly fraud, unproven claim | buyer | 147 | 79 |
| AG0 | Step 0 authorisation: unauthorised Mandate, replayed credential, charge after expiry, compromised provider | rail regime / merchant / agent provider | - | 18 |
| ABS-C1 | Conduct: altered evidence decides against its submitter | the tamperer | 7 | 7 |
| ABS-E1 (new) | Adverse inference against a record keeper that cannot produce its record | agent provider / merchant | - | 10 |
| ABS-H1 (new) | Records conflict, no keeper at fault: escalate to a fact-finder with human review | undetermined | - | 2 |
| ABS-S1 / S2 (new) | Unsigned spec / ambiguous Offer Snapshot construed against its author | agent provider / merchant | - | 13 |
| ABS-P1 / P2 (new) | Payment to a non-participant or outside the bound credential / forged Register entry | agent provider / programme guarantee | - | 22 |
| ABS-F1 (new) | Offer Feed signature did not verify / merchant's leaked key | agent provider / merchant | - | 4 |
| ABS-X1 / X2 (new) | Collusion / undisclosed incentive steering | joint / agent provider | - | 12 |
| ABS-R1 (new) | Apportionment across components | joint | - | 4 |
| ABS-D1 / D2 / G1 (new) | Default on merchant silence / merchant-initiated claim / public-authority payee | merchant / buyer / none | - | 6 |
| ABS-T1 / T2 | Inadmissible: time limit / repeat dispute | none | 7 | 9 |
| ABS-OK / M1 / M2 | No dispute / false refusal / true block (measured, no liability) | none | 21 | 30 |

## Core 2. Liability decision order: the precision of the Mandate decides

Order applied by the engine: Step 0 authorisation (new) -> conduct -> Step 1 conformity -> Step 2 manipulative offer -> Step 3 agent outside the explicit Mandate -> Step 4 buyer side. Audit 0 rule: an explicit Mandate or Allowance breach makes the agent provider liable; conforming to the explicit Mandate but not the unstated intent puts it on the user (the card networks' position for provider actions); a non-conforming delivery makes the merchant liable; an injected or manipulative offer makes the merchant liable. Only an encoded limit is a hard limit. Paired scenarios on both sides of that line:

| explicit | event | ground truth | unstated pair | event | ground truth |
|---|---|---|---|---|---|
| A01 (explicit) | misread_mandate_bought_unrequested_item | agent_provider / refund_full | A01b (unstated) | unstated_intent_bought_other_item_in_category | buyer / deny |
| A03 (explicit) | wrong_variant_required_attribute | agent_provider / return_and_refund | A03b (unstated) | wrong_variant_preference_only | buyer / deny |
| A07 (explicit) | hallucinated_requirement_added_item | agent_provider / refund_partial | A07b (unstated) | hallucinated_requirement_no_scope_flag | buyer / deny |
| AL03 (explicit) | delegate_exceeds_role_encoded | agent_provider / refund_partial | AL03b (unstated) | delegate_exceeds_role_not_encoded | buyer / deny |
| AL05b (explicit) | approval_fatigue_vague_prompt | agent_provider / return_and_refund | AL05 (unstated) | approval_fatigue_accurate_prompt | buyer / deny |
| AL11b (explicit) | policy_tightened_mid_purchase_after_ack | agent_provider / refund_partial | AL11 (unstated) | policy_tightened_mid_purchase_before_ack | buyer / deny |
| P10 (explicit) | ai_extracted_spec_unconfirmed | agent_provider / return_and_refund | P10b (unstated) | legacy_free_text_only_participant_no_spec | merchant / return_and_refund |

v0.1 recognises five hard limits (amount, category, merchant, units, expiry). v0.2 adds the explicit fields the pairs need: required attributes, scope flag, currency, delivery address, step-up/approval content, autonomy level, periodic budgets, delegate roles, invoice data, payment terms, procurement threshold, policy version (ABS-2.3). Both rule sets send the unstated side to the buyer.

## Core 3. Minimum evidence standard: which evidence level the rules need (given stipulated findings)

`decidable_at` = the lowest level at which the engine returns a determinate outcome equal to the full-evidence one; an escalated case (ABS-H1) is not determinate at any level and is counted separately. The findings are stipulated: the table shows which evidence level the rules need given correct findings, not whether that evidence would establish them in practice. E0 = card-dispute evidence; E1 adds the signed Mandate; E2 the agent's action log and clarifications; E3 the Offer Snapshot, page snapshots, cart line origin, the realistic delivery evidence bundle (carrier proof of handover, merchant packing record with serials, buyer photos, digital access log, return inspection), hash chain, Register entry, feed signature check.

| class | live disputes | v0.2 determinate at E0 | E1 | E2 | E3 | escalated | no rule | v0.1 determinate at E0 | v0.1 not determinate |
|---|---|---|---|---|---|---|---|---|---|
| agent_failure | 30 | 0 | 12 | 10 | 8 | 0 | 0 | 0 | 0 |
| allowance | 39 | 0 | 7 | 22 | 10 | 0 | 0 | 0 | 0 |
| anti_scam | 28 | 18 | 0 | 0 | 10 | 0 | 0 | 22 | 0 |
| attack | 61 | 0 | 14 | 17 | 30 | 0 | 0 | 10 | 0 |
| dispute_process | 53 | 19 | 2 | 0 | 30 | 2 | 0 | 7 | 13 |
| entry_route | 27 | 23 | 0 | 0 | 4 | 0 | 0 | 23 | 0 |
| lifecycle | 15 | 3 | 2 | 0 | 10 | 0 | 0 | 3 | 0 |
| merchant_failure | 55 | 10 | 0 | 0 | 45 | 0 | 0 | 10 | 0 |
| overlay | 45 | 3 | 13 | 0 | 29 | 0 | 0 | 4 | 3 |
| product_spec | 47 | 9 | 0 | 0 | 38 | 0 | 0 | 0 | 3 |
| segment | 71 | 4 | 10 | 22 | 35 | 0 | 0 | 10 | 2 |
| user_side | 27 | 0 | 0 | 0 | 27 | 0 | 0 | 0 | 0 |

What each level buys, in rule terms:

- E0 decides: time limit (6.1), non-delivery where the merchant cannot show a carrier proof of handover (Step 1), friendly-fraud non-receipt where it can (Step 4).
- E1 adds: authorisation (Step 0: strong authentication, holder, replay, charge after expiry), amount/category/merchant/units/expiry/currency breaches (Step 3).
- E2 adds: log-dependent breaches (step-up, required attributes, scope, approvals, budgets, roles), injection the agent itself reports following, undisclosed incentives.
- E3 adds: content conformity (packing record + photos + serials against the Offer Snapshot), merchant-added lines (cart origin), feed/snapshot mismatch, false claims, feed signature, Register entry, tampering (hash chain), and therefore every Step 4 denial of a not-as-described claim.

What is not determinate even at E3 (honest residual):

- records that conflict with no keeper at fault (D15: packing serial A, photographed serial B): 2 live dispute(s) -> ABS-H1 escalation to a fact-finder with human review (counted as escalated, not decided);
- findings that need judgment (listed in the Menime section): whether free text 'instructs an agent', whether a claim is false and caused the choice, what the buyer meant, counterfeit determination, damage vs wear, ambiguity. The engine takes these as typed inputs; the LLM/human fact-finder supplies them.

Minimum evidence package proposed for a decidable not-as-described case (ABS-3.2/3.4): Offer Snapshot (merchant-signed spec) + merchant packing record (serials, weight, photo at packing) + buyer photos or return inspection, with the signed Mandate and the action log for any Step 3 question. Carrier proof of delivery is necessary for non-delivery only.

## Core 4. Decision Center: escalation and human review

- Deterministic lane: a rule applies to 528/528 scenarios; 526 reach a determinate outcome and 2 are escalated to a fact-finder with human review (ABS-H1) because the findings conflict. An escalation is coverage, not a decision.
- Human review on request (GDPR Art. 22(3)-style right / ADR): modelled as a flag on 73 scenarios (every debatable or uncertain ground truth, every evidence conflict, and a deterministic 1-in-9 sample); all are honoured in v0.2 (73/528 (13.8%) of scenarios reach a human); v0.1 has no such right (73 requests unmet).
- Auto-escalation: 2 scenarios in v0.2 (conflicting records); under v0.1 the engine returns no decision for 30 scenarios and has no escalation rule.
- Appeal: one appeal within 10 days on new evidence or procedural error (ABS-6.6); disagreement alone refused. Statutory routes remain.

Findings the deterministic form cannot compute from records alone (fact-finder inputs, typed, with confidence):

| judgment finding | used by rule |
|---|---|
| attribute_is_ambiguous | ABS-S2.ambiguity |
| causation_agent_followed_it | ABS-4.2.injection |
| claim_caused_the_choice | ABS-4.2c.deceptive-claims |
| claim_is_false | ABS-4.2c.deceptive-claims |
| conformity_of_free_text_description | ABS-4.1.conformity |
| counterfeit_determination | ABS-4.1.conformity |
| damage_attributable_to_buyer | ABS-D2.merchant-claim |
| damage_vs_wear | ABS-4.1.conformity |
| evidence_knowingly_false_or_altered | ABS-7.1.conduct |
| existence_of_undisclosed_arrangement | ABS-X1.collusion |
| incentive_existed_and_was_undisclosed | ABS-X2.undisclosed-incentive |
| text_instructs_an_agent | ABS-4.2.injection |
| what_the_buyer_meant | ABS-4.4.buyer-side |
| which_record_is_true | ABS-H1.conflicting-evidence |

## Core 5. Settlement mapping (standards first)

| rail family | instruction types issued (v0.2) |
|---|---|
| a2a_push | apportioned_refund: 1, cure_document: 8, delivery_cost_refund_or_reject_and_refund: 1, deposit_retention: 1, none: 56, refer_to_authority_process: 2, refer_to_rail: 2, refund_full: 116, refund_partial: 35 |
| bnpl | apportioned_refund: 1, none: 8, refund_full: 17, refund_partial: 8 |
| card | apportioned_refund: 1, cure_document: 5, delivery_cost_refund_or_reject_and_refund: 1, deposit_retention: 2, escalated_no_instruction_yet: 1, none: 36, refer_to_authority_process: 1, refer_to_rail: 2, refund_full: 68, refund_partial: 33 |
| crypto | apportioned_refund: 1, cure_document: 1, none: 5, refund_full: 21, refund_partial: 6 |
| marketplace | none: 8, refund_full: 21, refund_partial: 1 |
| stored_value | escalated_no_instruction_yet: 1, none: 7, refund_full: 12, refund_partial: 5 |
| wallet | none: 16, refund_full: 14, refund_partial: 3 |

Vocabulary used in every instruction (Audit 2 corrected): on A2A rails a refund is a NEW credit transfer by the liable party (ISO 20022 pain.001 -> pacs.008); no recall, return or reversal is an ABS mechanism (camt.056 is the payer's PSP's tool for duplicate sending, technical error or fraud; a customer-reason recall depends on the payee's consent, answered by pacs.004 or camt.029; SCT Inst has no return; camt.027/087 are fund inquiries); against a refusing merchant the only route is contractual collection by its licensed PSP/acquirer or by the buyer. On cards the merchant refunds through the acquirer; only the issuer opens a dispute, at the cardholder's request, and ABS never initiates or assigns it (scheme-neutral stages: first dispute, response, pre-arbitration, arbitration; time-limit guard per scheme, e.g. 120 days from last expected delivery / 540 from processing for 'not received' as cited in Audit 2). A third party cannot reverse a card purchase; a sponsored originator can push a new credit (uncertain). UPI, Pix, wallets, BNPL = closest existing mechanism, marked unverified where it is. A payout hold exists only where the PSP is the payee (card acquiring, platform collection accounts, A2A acquiring). Merchant identity = LEI (ISO 17442) and MCC (ISO 18245); currency ISO 4217; country ISO 3166-1. Mappings are stated generally (`standard_verified`: general / uncertain / none).

Execution feasibility, v0.2, funds-moving instructions only (369): executable 334, contractual collection only 9, infeasible 26 (v0.1: 224 / 4 / 40 of 268). Not counted, because they move no funds under ABS: 14 corrected documents (cure), 7 referrals (the rail's unauthorised-payment regime or an authority's own process, which decide themselves), 2 escalations with no instruction yet (feasibility class `deferred`). Infeasible = liable merchant gone on an irrevocable rail in the merchant-account model (no payee-side hold possible), or a stablecoin merchant that refuses. No guarantee fund is counted: it is not in the normative rules (licence required). On UK Faster Payments the APP reimbursement regime may reimburse the consumer outside ABS (uncertain).

| scenario | rail | reason | fallback |
|---|---|---|---|
| ABS-S0039 | crypto_stablecoin_x402 | liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from | - |
| ABS-S0201 | open_banking_pis | liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from | - |
| ABS-S0202 | crypto_stablecoin_x402 | liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from | - |
| ABS-S0204 | sepa_instant | liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from | - |
| ABS-S0209 | upi | liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from | - |
| ABS-S0215 | crypto_stablecoin_x402 | liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from | - |
| ABS-S0221 | sepa_ct | liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from | - |
| ABS-S0222 | pix | liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from | - |
| ABS-S0226 | upi | liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from | - |
| ABS-S0230 | uk_fps | liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from | uk_app_reimbursement_regime (PSP-level, outside ABS; conditions and caps; uncertain) |
| ABS-S0231 | open_banking_pis | liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from | - |
| ABS-S0232 | crypto_stablecoin_x402 | liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from | - |
| ABS-S0234 | sepa_instant | liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from | - |
| ABS-S0238 | sepa_ct | liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from | - |
| ABS-S0316 | upi | liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from | - |
| ABS-S0437 | sepa_instant | liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from | - |
| ABS-S0438 | upi | liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from | - |
| ABS-C002 | sepa_instant | liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from | - |
| ABS-C003 | crypto_stablecoin_x402 | liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from | - |
| ABS-C045 | crypto_stablecoin_x402 | merchant refuses and no collection mechanism exists on-chain; off-chain claim only | - |
| ABS-C048 | sepa_instant | liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from | - |
| ABS-C049 | sepa_instant | liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from | - |
| ABS-C051 | crypto_stablecoin_x402 | liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from | - |
| ABS-C055 | sepa_instant | liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from | - |
| ABS-C057 | sepa_instant | liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from | - |
| ABS-C060 | sepa_instant | liable merchant gone on an irrevocable rail; funds were at the merchant's disposal (merchant-account model); nothing to collect from | - |

Contractual-collection-only instructions (merchant present but refusing; Register operator claims):

| scenario | rail | reason |
|---|---|---|
| ABS-S0107 | marketplace_split | contractual claim against the Register operator; no rail path and no normative guarantee |
| ABS-S0108 | card_credit_3ds | contractual claim against the Register operator; no rail path and no normative guarantee |
| ABS-S0199 | card_on_file_token | merchant refuses: no rail reversal; contractual collection by its licensed PSP/acquirer or by the buyer; suspension from the Register |
| ABS-S0200 | uk_fps | merchant refuses: no rail reversal; contractual collection by its licensed PSP/acquirer or by the buyer; suspension from the Register |
| ABS-S0414 | open_banking_pis | contractual claim against the Register operator; no rail path and no normative guarantee |
| ABS-C030 | sepa_instant | contractual claim against the Register operator; no rail path and no normative guarantee |
| ABS-C031 | card_credit_3ds | contractual claim against the Register operator; no rail path and no normative guarantee |
| ABS-C044 | sepa_instant | merchant refuses: no rail reversal; contractual collection by its licensed PSP/acquirer or by the buyer; suspension from the Register |
| ABS-C046 | card_credit_3ds | merchant refuses: no rail reversal; contractual collection by its licensed PSP/acquirer or by the buyer; suspension from the Register |

Outcomes for which no existing message or mechanism exists (places where ABS must extend a standard):

| rail or family | outcome | note |
|---|---|---|
| wallet | merchant_refund | wallet operator ledger reversal / merchant refund through the wallet API (proprietary; no standard message) |
| wallet | chargeback | wallet buyer-protection claim raised by the buyer with the operator (proprietary; runs in parallel, never assigned) |
| wallet | collection | operator debits the merchant's wallet balance under its agreement (proprietary) |
| bnpl | merchant_refund | merchant refund through the BNPL provider's API; the provider cancels or reduces the loan and returns paid instalments by credit transfer (pacs.008) (proprietary API; no standard message) |
| bnpl | chargeback | BNPL provider dispute programme raised by the buyer (proprietary) |
| bnpl | collection | provider debits the merchant settlement under its agreement (proprietary) |
| bnpl | third_party_refund | agent provider pays the provider or the buyer by credit transfer (pacs.008); no BNPL message for a third-party refund |
| stored_value | merchant_refund | re-credit of stored value by the programme (proprietary; no standard message) |
| stored_value | chargeback | none |
| stored_value | collection | programme debits the merchant under its agreement (proprietary) |
| stored_value | third_party_refund | agent provider pays the buyer by credit transfer (pacs.008); value cannot be returned to the gift card |
| crypto | merchant_refund | on-chain token transfer from the merchant to the buyer's address; x402 defines no refund primitive (no standard message) |
| crypto | chargeback | none; transfers are final |
| crypto | collection | none on-chain; contractual collection off-chain only |
| crypto | third_party_refund | on-chain token transfer from the agent provider (no standard message) |

Instructions issued with such a gap, v0.2: a2a_push | refer_to_authority_process: 2; a2a_push | refund_full: 5; bnpl | apportioned_refund: 1; bnpl | refund_full: 17; bnpl | refund_partial: 8; card | refer_to_authority_process: 1; card | refund_full: 3; crypto | apportioned_refund: 1; crypto | refund_full: 21; crypto | refund_partial: 6; marketplace | refund_full: 1; stored_value | refund_full: 12; stored_value | refund_partial: 5; wallet | refund_full: 13; wallet | refund_partial: 2.

## Coverage, gaps, conflicts and contradictions

Every scenario receives exactly one receipt in each rule set (528/528). A receipt records a determinate outcome, an escalation (a rule applied; the outcome waits for a fact-finder), or a gap (no rule applies; the indeterminate reason is recorded).

### v0.1 as written

Gaps (no rule applies or the standard has no provision): 205 scenario-gaps across 8 types.

- **rail execution undefined for this rail in v0.1 (only card and a2a_instant)** (81): ABS-C003, ABS-C007, ABS-C009, ABS-C028, ABS-C033, ABS-C034, ABS-C040, ABS-C042, ABS-C045, ABS-C051, ABS-C059, ABS-S0004, ABS-S0006, ABS-S0008, ABS-S0009, ABS-S0013, ABS-S0017, ABS-S0019, ABS-S0021, ABS-S0026, ABS-S0034, ABS-S0036, ABS-S0038, ABS-S0039, ABS-S0051, ABS-S0060, ABS-S0096, ABS-S0098, ABS-S0099, ABS-S0107, ABS-S0109, ABS-S0111, ABS-S0128, ABS-S0136, ABS-S0138, ABS-S0140, ABS-S0145, ABS-S0149, ABS-S0165, ABS-S0169 (+41 more)
- **human review requested; v0.1 has no human-review right** (73): ABS-C007, ABS-C016, ABS-C025, ABS-C034, ABS-C043, ABS-C052, ABS-S0006, ABS-S0015, ABS-S0024, ABS-S0033, ABS-S0042, ABS-S0051, ABS-S0060, ABS-S0069, ABS-S0073, ABS-S0074, ABS-S0078, ABS-S0079, ABS-S0080, ABS-S0087, ABS-S0091, ABS-S0092, ABS-S0093, ABS-S0094, ABS-S0096, ABS-S0105, ABS-S0114, ABS-S0123, ABS-S0132, ABS-S0141, ABS-S0150, ABS-S0159, ABS-S0168, ABS-S0177, ABS-S0186, ABS-S0195, ABS-S0204, ABS-S0213, ABS-S0222, ABS-S0231 (+33 more)
- **indeterminate:conformity_unknown** (14): ABS-C041, ABS-S0069, ABS-S0070, ABS-S0071, ABS-S0072, ABS-S0073, ABS-S0074, ABS-S0124, ABS-S0125, ABS-S0348, ABS-S0349, ABS-S0405, ABS-S0418, ABS-S0463
- **decision binds a non-participant (no Participation Agreement)** (13): ABS-C004, ABS-C005, ABS-C030, ABS-C031, ABS-S0041, ABS-S0042, ABS-S0107, ABS-S0108, ABS-S0164, ABS-S0185, ABS-S0186, ABS-S0398, ABS-S0414
- **indeterminate:no_transaction_unhandled** (9): ABS-S0061, ABS-S0062, ABS-S0063, ABS-S0064, ABS-S0197, ABS-S0198, ABS-S0274, ABS-S0275, ABS-S0431
- **indeterminate:mandate_and_log_missing** (7): ABS-S0126, ABS-S0127, ABS-S0173, ABS-S0174, ABS-S0297, ABS-S0298, ABS-S0427
- **appeal requested; v0.1 has no appeal procedure** (5): ABS-S0140, ABS-S0141, ABS-S0142, ABS-S0143, ABS-S0422
- **parallel rail dispute; v0.1 has no single-track / double-recovery rule** (3): ABS-C034, ABS-S0144, ABS-S0145

Overlay statements an ABS v0.1 Decision would not carry (consumer-rights or rail overlay applies but v0.1 says nothing): 16 types.

- **statutory_conformity_guarantee** (425): ABS-C001, ABS-C002, ABS-C003, ABS-C004, ABS-C005, ABS-C006, ABS-C007, ABS-C008, ABS-C009, ABS-C010, ABS-C011, ABS-C012 (+413 more)
- **eu_withdrawal_14d** (313): ABS-C001, ABS-C002, ABS-C003, ABS-C004, ABS-C005, ABS-C006, ABS-C007, ABS-C008, ABS-C009, ABS-C010, ABS-C011, ABS-C012 (+301 more)
- **push_payment_finality** (222): ABS-C003, ABS-C004, ABS-C009, ABS-C014, ABS-C016, ABS-C017, ABS-C024, ABS-C028, ABS-C029, ABS-C032, ABS-C037, ABS-C040 (+210 more)
- **card_dispute_right_parallel** (150): ABS-C005, ABS-C010, ABS-C012, ABS-C013, ABS-C015, ABS-C018, ABS-C022, ABS-C025, ABS-C031, ABS-C035, ABS-C038, ABS-C046 (+138 more)
- **bnpl_connected_lender** (34): ABS-C007, ABS-C023, ABS-C033, ABS-C034, ABS-S0008, ABS-S0021, ABS-S0038, ABS-S0051, ABS-S0068, ABS-S0081, ABS-S0098, ABS-S0111 (+22 more)
- **wallet_buyer_protection** (33): ABS-C020, ABS-C026, ABS-C042, ABS-S0006, ABS-S0019, ABS-S0036, ABS-S0049, ABS-S0066, ABS-S0079, ABS-S0096, ABS-S0109, ABS-S0125 (+21 more)
- **upi_dispute_mechanism** (32): ABS-C017, ABS-C032, ABS-C041, ABS-S0003, ABS-S0020, ABS-S0033, ABS-S0050, ABS-S0063, ABS-S0080, ABS-S0093, ABS-S0110, ABS-S0139 (+20 more)
- **payee_initiated_refund_right** (32): ABS-C013, ABS-C015, ABS-C035, ABS-S0010, ABS-S0023, ABS-S0040, ABS-S0053, ABS-S0070, ABS-S0083, ABS-S0100, ABS-S0113, ABS-S0129 (+20 more)
- **pix_special_return** (31): ABS-C024, ABS-C037, ABS-S0016, ABS-S0029, ABS-S0046, ABS-S0059, ABS-S0076, ABS-S0089, ABS-S0106, ABS-S0119, ABS-S0135, ABS-S0148 (+19 more)
- **dora_operational_resilience** (10): ABS-C036, ABS-C037, ABS-S0169, ABS-S0170, ABS-S0171, ABS-S0172, ABS-S0173, ABS-S0174, ABS-S0379, ABS-S0427
- **cross_border_landed_cost** (6): ABS-S0177, ABS-S0178, ABS-S0179, ABS-S0180, ABS-S0265, ABS-S0266
- **uk_app_reimbursement** (3): ABS-C004, ABS-S0164, ABS-S0310
- **gdpr_erasure_mid_dispute** (3): ABS-S0165, ABS-S0166, ABS-S0426
- **dcc_transparency** (3): ABS-S0175, ABS-S0176, ABS-S0267
- **pci_card_data_in_agent_context** (2): ABS-C035, ABS-S0123
- **gdpr_access_during_dispute** (2): ABS-S0167, ABS-S0168

Conflicts (two fired rules name different liable parties): resolved by the decision order consistently with the stipulated ground truth: 7; unresolved (the order gives the wrong party or apportionment is needed): 4.

- unresolved: D03 | ('agent_provider', 'merchant') | ABS-4.1.conformity (4): ABS-C007, ABS-C008, ABS-S0128, ABS-S0129
- resolved by order: D06 | ('merchant', 'none') | ABS-6.1.time-limit (4): ABS-C020, ABS-S0134, ABS-S0135, ABS-S0420
- resolved by order: R16 | ('merchant', 'none') | ABS-6.1.time-limit (3): ABS-S0181, ABS-S0182, ABS-S0428

Contradictions with the stipulated ground truth or stated consumer rights (a rule applied, but the party or remedy class differs): 158 scenarios in 58 groups (event | name | v0.1 liable | v0.1 remedy | truth liable | truth remedy):

- M20 | fake_store_vanished | merchant | refund | agent_provider | refund (5): ABS-C004, ABS-C005, ABS-S0041, ABS-S0042, ABS-S0398
- X07 | fake_merchant_spoofed_participation | merchant | refund | register_operator | refund (5): ABS-C030, ABS-C031, ABS-S0107, ABS-S0108, ABS-S0414
- X11 | replayed_mandate_by_merchant | buyer | deny | merchant | partial (5): ABS-C013, ABS-C014, ABS-S0115, ABS-S0116, ABS-S0416
- R17 | recurring_charge_after_mandate_expiry | buyer | deny | merchant | refund (5): ABS-C015, ABS-C016, ABS-C017, ABS-S0183, ABS-S0184
- U06 | account_takeover_user | buyer | deny | rail_unauthorised_regime | refer (4): ABS-C011, ABS-C012, ABS-S0087, ABS-S0088
- U07 | agent_session_takeover | buyer | deny | agent_provider | refund (4): ABS-C039, ABS-S0089, ABS-S0090, ABS-S0410
- X06 | merchant_agent_collusion | buyer | deny | merchant+agent_provider | refund (4): ABS-C006, ABS-S0105, ABS-S0106, ABS-S0413
- X13 | kickback_steering | buyer | deny | agent_provider | partial (4): ABS-C027, ABS-S0119, ABS-S0120, ABS-S0417
- D03 | partial_liability_two_faults | merchant | refund | merchant+agent_provider | apportioned (4): ABS-C007, ABS-C008, ABS-S0128, ABS-S0129
- Z07 | merchant_asks_to_pay_off_platform | merchant | refund | agent_provider | refund (4): ABS-C059, ABS-S0213, ABS-S0214, ABS-S0380
- G08 | entry_collusion_with_agent_provider | buyer | deny | merchant+agent_provider | refund (4): ABS-C058, ABS-S0235, ABS-S0236, ABS-S0440
- M14 | wrong_delivery_cost | buyer | deny | merchant | partial (3): ABS-S0029, ABS-S0030, ABS-S0396
- M15 | price_changed_at_checkout | buyer | deny | merchant | partial (3): ABS-C032, ABS-S0031, ABS-S0032
- M17 | partial_shipment | merchant | refund | merchant | partial (3): ABS-S0035, ABS-S0036, ABS-S0397
- A03 | wrong_variant_required_attribute | buyer | deny | agent_provider | refund (3): ABS-S0047, ABS-S0048, ABS-S0400
- A06 | ignored_step_up | buyer | deny | agent_provider | refund (3): ABS-S0055, ABS-S0056, ABS-S0402
- X04 | dark_pattern_fake_reference_price | buyer | deny | merchant | partial (3): ABS-S0101, ABS-S0102, ABS-S0412
- D04 | split_shipment_one_parcel_lost | merchant | refund | merchant | partial (3): ABS-S0130, ABS-S0131, ABS-S0419
- D11 | merchant_claim_rental_damage | buyer | deny | buyer | merchant_claim (3): ABS-C038, ABS-S0146, ABS-S0147
- R12b | provider_outage_merchant_double_capture | merchant | refund | merchant | partial (3): ABS-C037, ABS-S0171, ABS-S0172
- AL02 | monthly_budget_exhausted_mid_basket | buyer | deny | agent_provider | partial (3): ABS-S0247, ABS-S0248, ABS-S0442
- AL03 | delegate_exceeds_role_encoded | buyer | deny | agent_provider | partial (3): ABS-S0249, ABS-S0250, ABS-S0388
- AL04 | approval_granted_for_x_agent_bought_y | buyer | deny | agent_provider | refund (3): ABS-S0253, ABS-S0254, ABS-S0444
- AL05b | approval_fatigue_vague_prompt | buyer | deny | agent_provider | refund (3): ABS-S0257, ABS-S0258, ABS-S0445
- AL07 | b2b_missing_vat_id_agent | buyer | deny | agent_provider | cure (3): ABS-S0261, ABS-S0262, ABS-S0446
- AL13 | notify_and_hold_ignored | buyer | deny | agent_provider | refund (3): ABS-S0276, ABS-S0277, ABS-S0448
- SB01 | b2b_po_number_missing_on_invoice | buyer | deny | agent_provider | cure (3): ABS-S0278, ABS-S0279, ABS-S0449
- SB03 | b2b_approval_workflow_bypassed | buyer | deny | agent_provider | refund (3): ABS-S0282, ABS-S0283, ABS-S0450
- SC03 | c2g_permit_fee_permit_refused | buyer | deny | none | refer_admin (3): ABS-S0305, ABS-S0306, ABS-S0453
- SC04 | c2g_tax_paid_late_penalty | buyer | deny | agent_provider | partial (3): ABS-S0307, ABS-S0308, ABS-S0454
- SC05 | c2g_authority_portal_phishing_clone | merchant | refund | agent_provider | refund (3): ABS-S0309, ABS-S0310, ABS-S0455
- P10 | ai_extracted_spec_unconfirmed | merchant | refund | agent_provider | refund (3): ABS-S0364, ABS-S0365, ABS-S0466
- M09 | late_delivery_goods_kept | merchant | refund | merchant | late_remedy (2): ABS-S0023, ABS-S0024
- A01 | misread_mandate_bought_unrequested_item | buyer | deny | agent_provider | refund (2): ABS-S0043, ABS-S0044
- A07 | hallucinated_requirement_added_item | buyer | deny | agent_provider | partial (2): ABS-S0057, ABS-S0058
- X05 | dark_pattern_false_scarcity | buyer | deny | merchant | partial (2): ABS-S0103, ABS-S0104
- X12 | mitm_on_offer_feed | buyer | deny | agent_provider | refund (2): ABS-S0117, ABS-S0118
- X14 | compromised_agent_provider | buyer | deny | agent_provider | refund (2): ABS-S0121, ABS-S0122
- D05 | second_dispute_same_record_no_new_facts | buyer | deny | none | inadmissible (2): ABS-S0132, ABS-S0133
- R15 | duties_not_in_landed_cost | buyer | deny | merchant | partial (2): ABS-S0177, ABS-S0178
- L01 | non_participant_merchant_bought | merchant | refund | agent_provider | refund (2): ABS-S0185, ABS-S0186
- L04 | mandate_without_strong_auth | buyer | deny | agent_provider | refund (2): ABS-S0189, ABS-S0190
- AL01 | split_purchases_evade_per_transaction_limit | buyer | deny | agent_provider | refund (2): ABS-S0245, ABS-S0246
- AL07b | b2b_e_invoice_not_issued_by_merchant | merchant | refund | merchant | cure (2): ABS-S0263, ABS-S0264
- AL11b | policy_tightened_mid_purchase_after_ack | buyer | deny | agent_provider | partial (2): ABS-S0272, ABS-S0273
- SB02 | b2b_reverse_charge_not_applied | merchant | refund | merchant | cure (2): ABS-S0280, ABS-S0281
- SB04 | b2b_e_invoice_schema_rejected | merchant | refund | merchant | cure (2): ABS-S0284, ABS-S0285
- SB07 | b2b_net30_terms_agent_prepaid | buyer | deny | agent_provider | deny (2): ABS-S0289, ABS-S0290
- SG01 | b2g_above_direct_award_threshold | buyer | deny | agent_provider | refund (2): ABS-S0291, ABS-S0292
- SG03 | b2g_e_invoice_format_not_accepted | merchant | refund | merchant | cure (2): ABS-S0295, ABS-S0296
- SC02 | c2g_wrong_reference_paid | buyer | deny | agent_provider | refund (2): ABS-S0303, ABS-S0304
- SP04 | c2c_off_platform_payment | merchant | refund | agent_provider | refund (2): ABS-S0317, ABS-S0318
- SA01 | a2a_seller_agent_promised_discount_snapshot_list_price | buyer | deny | merchant | partial (2): ABS-S0326, ABS-S0327
- R08 | uk_app_fraud_fake_store | merchant | refund | agent_provider | refund (1): ABS-S0164
- R14 | dcc_markup_agent_accepted | buyer | deny | agent_provider | partial (1): ABS-S0175
- R14b | dcc_markup_merchant_default | buyer | deny | merchant | partial (1): ABS-S0176
- SB05 | b2b_payment_redirect_injected_iban | merchant | refund | agent_provider | refund (1): ABS-S0286
- X12 | mitm_on_offer_feed | buyer | deny | merchant | refund (1): ABS-C029

### v0.2 proposed

Gaps: 0. Unresolved conflicts: 0. Contradictions: 0. Escalated to human review (covered, not determinate): 2. Conflicts resolved by the decision order: 57 (a standing or Step 0 rule fires together with a later step; the earlier step decides, as intended).
Settlement instructions still infeasible: 26; contractual collection only: 9 (the honest residual: no payee-side hold, no normative guarantee). Overlay statements: all carried by the v0.2 Decision text (ABS-6.9, ABS-8).


## Proposed rule fixes for ABS v0.1 (ranked by scenarios repaired)

Each v0.1 failure (gap or contradiction) is matched to the v0.2 rule that decides it consistently with the stipulated ground truth. Wording is written for the ABS author to adopt.

1. **ABS-4.3.agent-outside-mandate** repairs 52 scenario(s) (ABS-C039, ABS-S0043, ABS-S0044, ABS-S0047, ABS-S0048, ABS-S0055, ABS-S0056, ABS-S0057 (+44 more)).
   > Amend 2.1: the Mandate also holds, each as an explicit hard limit when set: required attributes (colour, size, model, dates, reference, deadline); a scope flag ('only the item named', on by default); the pay-in currency and an FX tolerance; the delivery address; whether a step-up is required and the exact content an approval prompt must show (item and amount); the autonomy level (autonomous / notify-and-hold / approval required / never) per category; per-transaction and periodic budgets; delegate roles and limits; invoice data (PO number, VAT ID, e-invoice format) and payment terms for business buyers; procurement thresholds and framework allowlists for public buyers; the minimum merchant Trust Attestation level; for recurring purchases the period and maximum number of charges; a version, with changes taking effect when the agent acknowledges them. Only an encoded limit is a hard limit; unstated intent stays with the user. Mandate creation requires strong authentication of the account holder by a PSP; a Mandate without it is invalid (Step 0).

2. **ABS-4.1.conformity** repairs 19 scenario(s) (ABS-C037, ABS-S0023, ABS-S0024, ABS-S0035, ABS-S0036, ABS-S0130, ABS-S0131, ABS-S0171 (+11 more)).
   > Amend 4 Step 1 remedy: 'Refund of the non-conforming lines; where the conforming part has no stand-alone use for the buyer (bundle), full refund with return at the merchant's cost. For late delivery of conforming goods the buyer may reject within 14 days of the late delivery (full refund, return at the merchant's cost) or keep the goods and recover the delivery charge. For a non-conformity of documents (invoice, e-invoice, VAT treatment) the remedy is a corrected document (cure), not a refund.'

3. **AG0.unauthorised-mandate** repairs 18 scenario(s) (ABS-C011, ABS-C012, ABS-C013, ABS-C014, ABS-C015, ABS-C016, ABS-C017, ABS-S0087 (+10 more)).
   > New 4.0 (Step 0, Authorisation). Before Step 1 the arbiter checks that (a) the Mandate was created by the account holder with strong authentication performed by a PSP, and (b) the charge was initiated by the buyer's agent under that Mandate before its expiry with the mandate-bound credential. If (a) fails, the case is an unauthorised payment: ABS refers it to the rail's unauthorised-payment procedure and supplies the Mandate record; the buyer is not liable under ABS. If the provider's systems issued the charge without a valid Mandate (compromise, or a Mandate accepted without strong authentication), the agent provider is liable. If (b) fails because the merchant presented the credential again or charged after expiry, the merchant is liable for that charge.

4. **ABS-P1.non-participant** repairs 17 scenario(s) (ABS-C004, ABS-C005, ABS-C059, ABS-S0041, ABS-S0042, ABS-S0164, ABS-S0185, ABS-S0186 (+9 more)).
   > New 1.5: Before paying, the agent verifies the merchant's current, signed entry in the Qualified Merchant Register. A payment to a merchant without one, or made outside the mandate-bound credential, is outside the Mandate: the agent provider bears the buyer's loss that the rail's own dispute process does not recover.

5. **ABS-4.2b.feed-snapshot-mismatch** repairs 11 scenario(s) (ABS-C032, ABS-S0029, ABS-S0030, ABS-S0031, ABS-S0032, ABS-S0176, ABS-S0177, ABS-S0178 (+3 more)).
   > Amend 4 Step 2: add 'or the Offer Snapshot's price, delivery cost, mandatory fees, currency conversion, import charges or negotiated terms are worse for the buyer than the Offer Feed record or signed negotiation record the agent relied on when it chose the merchant'. Remedy: refund of the difference. The record the agent compared on is kept in the hash chain with the Snapshot.

6. **ABS-M.refusal-record** repairs 9 scenario(s) (ABS-S0061, ABS-S0062, ABS-S0063, ABS-S0064, ABS-S0197, ABS-S0198, ABS-S0274, ABS-S0275 (+1 more)).
   > New 2.4: Every refusal to buy writes a Refusal Record (offers compared, Mandate, stated reason). Refusals of a conforming, qualified, in-mandate offer count as false refusals on the programme scoreboard per agent provider; they carry no liability.

7. **ABS-X1.collusion** repairs 8 scenario(s) (ABS-C006, ABS-C058, ABS-S0105, ABS-S0106, ABS-S0235, ABS-S0236, ABS-S0413, ABS-S0440).
   > New 4.2d: Where the merchant and the agent provider have an undisclosed arrangement under which the agent's choice benefits both, they are jointly and severally liable for the buyer's loss, and both are suspended from the Register pending review.

8. **ABS-S2.ambiguity** repairs 7 scenario(s) (ABS-C041, ABS-S0124, ABS-S0125, ABS-S0348, ABS-S0349, ABS-S0418, ABS-S0463).
   > New 4.1a: Where the Offer Snapshot can reasonably be read two ways and the delivery fits only one, the reading favourable to the buyer applies (the merchant wrote the offer). The merchant avoids this by stating the attribute with its unit, region and tolerance in the signed Product Specification.

9. **ABS-E1.adverse-inference** repairs 7 scenario(s) (ABS-S0126, ABS-S0127, ABS-S0173, ABS-S0174, ABS-S0297, ABS-S0298, ABS-S0427).
   > Amend 3 'where evidence is missing': 'A party that was required to keep a record (the agent provider for the Mandate and action log; the merchant for the Offer Snapshot and packing record) and cannot produce it when asked has the question that record would answer decided against it.'

10. **ABS-4.2c.deceptive-claims** repairs 5 scenario(s) (ABS-S0101, ABS-S0102, ABS-S0103, ABS-S0104, ABS-S0412).
   > Amend 4 Step 2: add reason code AG4-D, Deceptive offer content: a statement of fact in merchant-controlled content shown to be false (reference prices, stock, time limits, endorsements) where the agent's log shows it influenced the choice. Remedy: refund of the difference against the best conforming offer the agent had seen, or of the affected item.

11. **ABS-P2.spoofed-register** repairs 5 scenario(s) (ABS-C030, ABS-C031, ABS-S0107, ABS-S0108, ABS-S0414).
   > New 1.6: The Qualified Merchant Register is signed by its operator. Where an agent verified an entry later shown to be forged, the operator is liable to the buyer under the Participation Agreement and pays by a new credit transfer; the agent provider is not liable. Any guarantee fund that would pay buyers belongs to Part B until its licensed form (authorised insurer, credit-institution guarantee, or the operator's own undertaking) is settled by legal opinion.

12. **ABS-F1.feed-authenticity** repairs 4 scenario(s) (ABS-C029, ABS-S0117, ABS-S0118, ABS-S0286).
   > New 1.9: Offer Feed records are signed by the merchant's registered key. An agent must not rely on a record whose signature does not verify; if it does, the agent provider bears the mismatch. A merchant answers for records signed with its key, including after a key compromise, until it revokes the key in the Register.

13. **ABS-X2.undisclosed-incentive** repairs 4 scenario(s) (ABS-C027, ABS-S0119, ABS-S0120, ABS-S0417).
   > New 1.4a: The agent provider discloses in the Mandate any payment it receives from merchants. A choice influenced by an undisclosed incentive is outside the Mandate (reason code ABS-X2); remedy: the difference against the best conforming offer the agent saw.

14. **ABS-R1.apportionment** repairs 4 scenario(s) (ABS-C007, ABS-C008, ABS-S0128, ABS-S0129).
   > Amend 4 (decision order): 'Where more than one step is satisfied for different components of the same purchase (for example late delivery by the merchant and an extra unit bought by the agent), the arbiter decides each component under its own step and apportions the remedy. The order of steps resolves which party answers for the same component, not whether a second party answers for a different one.'

15. **ABS-E1m.merchant-records-missing** repairs 3 scenario(s) (ABS-S0071, ABS-S0072, ABS-S0405).
   > Amend 3 (E3): the merchant keeps a packing record (serials, weight, photo at packing) for every Purchase Record. Amend 3 'where evidence is missing': 'A party that was required to keep a record and cannot produce it when asked has the question that record would answer decided against it.'

16. **ABS-D2.merchant-claim** repairs 3 scenario(s) (ABS-C038, ABS-S0146, ABS-S0147).
   > New 6.8: A merchant may open a Dispute Case against the buyer only for a deposit, damage or non-return recorded in handover and return records. The same decision order applies with the roles reversed; the remedy is capped at the deposit or the recorded damage.

17. **ABS-G1.authority-payee** repairs 3 scenario(s) (ABS-S0305, ABS-S0306, ABS-S0453).
   > New 1.5a: A public authority is a permitted payee without a Participation Agreement when the agent verified it in the official registry. ABS decides only whether the agent stayed inside the Mandate; claims against the authority follow administrative appeal, and its refunds follow its own process.

18. **ABS-S1.unsigned-spec** repairs 3 scenario(s) (ABS-S0364, ABS-S0365, ABS-S0466).
   > Amend 1.3 and 2.2: The Offer Snapshot's structured attributes bind only when signed by the merchant (the Product Specification: conformity-critical attributes, units, tolerances, package contents, region/compatibility, condition grade). Free text and marketing claims are not binding and cannot cut down the signed spec. An agent must not accept an offer from a participant without a signed spec; if it extracts attributes itself and buys on them, the agent provider bears any mismatch. A participant that sells to agents without a signed spec has every ambiguity in its listing construed against it.

19. **ABS-E2.unproven-claim** repairs 2 scenario(s) (ABS-S0069, ABS-S0070).
   > New 3.3 (minimum evidence): The buyer supports a not-as-described claim with photos or a return inspection; carrier proof of delivery proves handover, never content. Where the buyer gives none and the merchant's packing record and serials match the Offer Snapshot, the claim fails under Step 4.

20. **ABS-H1.conflicting-evidence** repairs 2 scenario(s) (ABS-S0073, ABS-S0074).
   > New 6.5a (Decision Center): When the engine cannot establish a finding from the records (conflicting serials, contested photos), it returns 'review' with the conflicting records marked; a fact-finder supplies the typed finding and the engine decides from it. Any party may request human review of any Decision; the review is by a person who did not take part in the automated decision.

21. **ABS-T2.repeat-dispute** repairs 2 scenario(s) (ABS-S0132, ABS-S0133).
   > New 6.7: One Dispute Case per Purchase Record. A second case on the same record is admitted only on facts not available to the filing party at the first filing, or to reopen a settlement obtained by a false claim (6.3).

Process, settlement and data wording that the engine applies as findings (not liability rules):

- **ABS-3.2.delivery-evidence**: Amend 3 (E3): there is no carrier content inspection. The delivery evidence bundle is: carrier proof of delivery (handover only), the merchant's packing record (serials, weight, photo at packing), the buyer's unboxing photos, serial numbers, the digital access log for digital goods and subscriptions, the completion record for services, the ticket issuance and use log for travel, the handover and return inspection records for rentals, and the return inspection record for returns. The minimum package for a decidable not-as-described case is: Offer Snapshot + packing record + buyer photos or return inspection, with serials where the goods carry them.
- **ABS-3.4.evidence-weighing**: New 3.4: (a) carrier proof of delivery proves handover, never content; (b) a packing record with serials matching the Offer Snapshot, unopposed by buyer photos or a return inspection, establishes conformity; (c) buyer photos showing non-conformity on a unit whose serial matches the packing record establish non-conformity; (d) where the packing record and the photographed serial conflict and no record keeper is at fault, the engine returns 'review' (6.5a).
- **ABS-5.3.rail-execution**: Amend 5.2: a Settlement Instruction is executed by the liable party as a NEW payment on every rail: card (merchant refund through the acquirer; a sponsored push-to-card credit for a third party), wallet (operator reversal), A2A push including SEPA CT/Inst, FPS, UPI, Pix and open-banking PIS (new credit transfer: pain.001/pacs.008; no recall, return or reversal is an ABS mechanism: camt.056 belongs to the payer's PSP for duplicate, technical error or fraud, a customer-reason recall needs the payee's consent, SCT Inst has no return, camt.027/087 are fund inquiries), BNPL (refund through the provider), marketplace (platform PSP reverses the held split), stored value (re-credit), stablecoin (on-chain return transfer), public authority (its own refund process). Against a merchant that refuses, the only route is the contractual collection right of its licensed PSP/acquirer or of the buyer (5.6); the Settlement Instruction never names the arbiter or the programme as payer or payee.
- **ABS-5.4.payout-hold**: New 5.4: ABS holds no funds. A payout hold exists only where a licensed PSP is itself the payee: card acquiring, platform collection accounts, and A2A acquiring where the merchant is paid later under the acquiring contract. Funds credited to a merchant's own payment account cannot be held (they must be at the payee's disposal immediately). Where the model allows it, the payee PSP holds the payout for merchants in probation (first 90 days or below the trust threshold) and for prepaid orders with delivery more than 14 days out, until the delivery evidence bundle confirms delivery plus a 7-day inspection window, and keeps a rolling reserve. Where it does not, ABS states that the buyer bears the merchant's default and says so before the purchase.
- **ABS-5.5.parallel-rights-and-reconciliation**: New 5.5: Opening a Dispute Case never waives, assigns or suspends the buyer's dispute rights with its issuer, wallet operator or PSP, and ABS never initiates a card dispute: only the issuer does, at the cardholder's request. The Decision Center supplies the Decision as evidence on request. A refund under a Decision is set off against any later rail recovery on the same payment so that the buyer is made whole once. Deadline guard: before a scheme time limit (for example 120 days from the last expected delivery for merchandise not received, at most 540 days from processing, per the card rules cited in Audit 2; verify per scheme) the Decision issues or the buyer is told to file with the issuer; ABS deadlines pause while a rail dispute runs.
- **ABS-5.6.enforcement**: New 5.6: A Settlement Instruction unpaid after 10 days is collected by the merchant's licensed PSP or acquirer in its own right under the Participation Agreement (reserve, debit, set-off), or claimed by the buyer directly; the programme and the arbiter never receive or pay money. Failing collection the merchant is suspended from the Register and the buyer is told which statutory and rail routes remain. No guarantee payout is promised in the normative rules.
- **ABS-6.5a.decision-center**: New 6.5a: The Decision Center runs the decision order deterministically on typed findings and issues a Decision receipt (findings, rules fired, decision, remedy, Settlement Instruction, hash). Findings that need judgment come from a fact-finder as typed inputs with a confidence. Any party may request human review of any Decision within 10 days; a person who did not take part in the automated decision reviews it and may confirm, change or send the case to appeal. The engine escalates on its own when a finding cannot be established.
- **ABS-6.6.appeal**: Amend 6.5: 'The decision is final within the programme, save for one appeal within 10 days on new evidence not available to the appellant or on a procedural error. Disagreement alone is not a ground. Statutory routes (court, ADR) remain.'
- **ABS-6.9.statutory-rights**: New 6.9: Time limits and decisions under ABS do not reduce the buyer's statutory rights (withdrawal, conformity guarantee, unauthorised-payment protection). The Decision states which statutory route remains open; where the EU 14-day withdrawal right applies and the buyer invokes it, the Settlement Instruction executes the withdrawal refund on the same rail.
- **ABS-8.data**: New 8 (Data): The parties keep the Dispute Case records until the decision and appeal window close plus the statutory limitation period; erasure requests are deferred for that period; access requests are served with the evidence bundle minus third-party data. No card data enters the agent context: agents pay with network tokens or mandate-bound credentials only; a merchant checkout that requests card data from an agent breaches its Participation Agreement.
- **ABS-1.7.trust-attestation**: New 1.7 (roadmap): The programme publishes a Trust Attestation for every Register entry (score and components: identity verified, payout name match, domain age, review authenticity, delivery history, dispute rate, ad-burst and price-anomaly signals). Agents read it before comparing offers and must not buy below the Mandate's minimum; a price far below market or an ad burst triggers a step-up, not a block, when the score is high.
- **ABS-1.8.entry-gate**: New 1.8 (roadmap): Entry to the Register requires KYB (registry, beneficial owner, payout account in the entity's name, domain ownership, brand-similarity screen, LEI where available, MCC), a shared blocklist check (beneficial owners, payout accounts, devices, domains of expelled merchants), a 90-day probation with a payee-PSP payout hold where the model allows it (card acquiring, collection accounts, A2A acquiring) and volume caps, continuous monitoring (non-delivery rate, catalogue/MCC drift, prepaid-order velocity against a seasonal baseline), and per-purchase re-attestation of the merchant's status and of the Offer Feed signature. The programme does not claim to keep every scammer out; it claims that an unproven merchant is not paid before delivery where a payee PSP holds the payout, and says plainly where no hold is possible (merchant-account A2A, stablecoin).
- **ABS-2.5.contract-formation**: New 2.5: The contract is formed when the agent accepts the Offer Snapshot and the payment is authorised. Cancellation by the merchant afterwards (stale stock) is non-delivery (Step 1); a substitute needs a new Offer Snapshot accepted inside the Mandate.
- **ABS-2.6.idempotency**: New 2.6: Every checkout carries an idempotency key derived from the Mandate id and the cart hash. A duplicate capture against one key is the merchant's (Step 1, quantity/price); a duplicate order from the agent's retry without a key is the agent provider's (Step 3).
- **ABS-2.7.negotiation-record**: New 2.7 (agent-to-agent): Terms agreed between a buyer-agent and a seller-agent bind only when written into a negotiation record signed by both agents and hashed into the Offer Snapshot. Statements by the seller-agent are merchant-controlled content for Step 2.
- **ABS-1.5b.responding-party**: New 1.5b (marketplaces): The Participation Agreement names the responding party for each line: the third-party seller for its goods and conduct; the platform for its own feed, fees, catalogue merges and hosting duties, and as guarantor of last resort for refunds from the held split.
- **ABS-9.enforcement-layer**: New 9 (allowances): Where an Allowance limit is encoded in the mandate-bound credential and the payment-side control fails to decline a breaching payment, the agent provider remains liable to the buyer and has recourse against the enforcement layer under the credential agreement; the buyer is never left to pursue the enforcement layer.

## EU withdrawal-right overlay: what it already resolves

50 scenarios end in an ABS denial (AG2/AG5) where the consumer could instead withdraw within 14 days of delivery (goods, distance sale, no exception): ABS-C021, ABS-C023, ABS-C026, ABS-C035, ABS-S0049, ABS-S0066, ABS-S0067, ABS-S0069, ABS-S0070, ABS-S0077, ABS-S0081, ABS-S0082, ABS-S0083, ABS-S0084, ABS-S0085, ABS-S0092, ABS-S0094, ABS-S0114, ABS-S0142, ABS-S0153, ABS-S0167, ABS-S0191, ABS-S0255, ABS-S0270, ABS-S0314, ABS-S0332, ABS-S0333, ABS-S0336, ABS-S0337, ABS-S0338 (+20 more). For these, allocating liability matters least: the buyer returns the goods at its own cost and is refunded on the same rail (ABS-6.9). Exceptions modelled: perishables, custom-made, date-specific travel/rental, digital content once started, services fully performed, business buyers. All statements general; verify before citing.

## Mapping onto a Menime ruleset pack (`scrolld.abs`)

Menime's kernel decides deterministically on logic objects, with an `explanation[]` on every route decision and signed receipts (Ed25519 key id). The ABS engine maps directly:

- **Pack**: `scrolld.abs`, versions `scrolld.abs@0.1` (as written) and `scrolld.abs@0.2-proposed`. Each rule id here becomes `scrolld.abs.<group>.<rule>` (e.g. `scrolld.abs.conformity.4-1`, `scrolld.abs.authorisation.a0`).
- **Inputs**: the typed findings object in the receipt (`findings.*`): participation, authorisation, standing, conformity (established / per attribute with tolerance / evidence state), within_mandate (breaches by name), manipulation flags, agent conduct, evidence, buyer. Each finding carries which evidence level made it knowable (`known`).
- **Evaluation**: all rules evaluate; `rules_fired` is the ordered list; the decision is the first by group order (standing, authorisation, conduct, conformity, manipulative_offer, agent_mandate, buyer_side), with ABS-R1 apportionment and 6.3 tier-1 settlement as post-steps. This is the Menime lane 'deterministic, zero inference'.
- **Receipt**: `abs_decision_receipt` with `receipt_sha256` over RFC 8785 canonical JSON of the receipt without the hash field; Menime signs that hash with its receipt key (`RECEIPT_KID`). Ledger event: `decision_receipt_created`. The receipt's Settlement Instruction never names the arbiter or the programme as payer or payee (Audit 2 LIC-02).
- **Deterministic rules**: 18 of 28 rules need no judgment input: ABS-S0.no-dispute, ABS-M.refusal-record, ABS-6.1.time-limit, ABS-T2.repeat-dispute, ABS-G1.authority-payee, ABS-P1.non-participant, ABS-P2.spoofed-register, AG0.unauthorised-mandate, ABS-E1m.merchant-records-missing, ABS-E2.unproven-claim, ABS-S1.unsigned-spec, ABS-D1.default-on-silence, ABS-4.2.merchant-added, ABS-4.2b.feed-snapshot-mismatch, ABS-F1.feed-authenticity, ABS-4.3.agent-outside-mandate, ABS-R1.apportionment, ABS-E1.adverse-inference.
- **Rules that need a fact-finder** (10): the rule is deterministic once the finding is typed, but the finding itself is a judgment an LLM or human fact-finder supplies with a confidence (Menime 'the LLM may write; the kernel decides'):

  - `ABS-D2.merchant-claim` needs: damage_attributable_to_buyer
  - `ABS-7.1.conduct` needs: evidence_knowingly_false_or_altered
  - `ABS-4.1.conformity` needs: conformity_of_free_text_description, counterfeit_determination, damage_vs_wear
  - `ABS-H1.conflicting-evidence` needs: which_record_is_true
  - `ABS-S2.ambiguity` needs: attribute_is_ambiguous
  - `ABS-4.2.injection` needs: text_instructs_an_agent, causation_agent_followed_it
  - `ABS-4.2c.deceptive-claims` needs: claim_is_false, claim_caused_the_choice
  - `ABS-X1.collusion` needs: existence_of_undisclosed_arrangement
  - `ABS-X2.undisclosed-incentive` needs: incentive_existed_and_was_undisclosed
  - `ABS-4.4.buyer-side` needs: what_the_buyer_meant
- **Cannot be expressed deterministically at all**: 'balance of probabilities' when records conflict and no keeper is at fault (ABS-H1 returns `review`); whether a text 'instructs an agent'; whether the buyer's unstated intent was met (only matters for the AG2/AG5 label, not for liability); counterfeit determination from photos. These are fact-finder outputs, never kernel rules.
- **Human review**: a Menime route `human_review_requested` on any Decision; the reviewer's finding re-enters as typed input and the kernel re-decides; both receipts are chained.

## Roadmap families (kept, reported briefly)

### Anti-scam gate and payout hold (residual-risk table)

Configuration A: no Trust Attestation, immediate payout. Configuration B: Trust Attestation consulted, Mandate minimum trust (default 60), payout hold for merchants under 180 days or trust under 70 where a licensed PSP is the payee (card acquiring, platform collection accounts, A2A acquiring), released on delivery evidence + 7-day inspection. On merchant-account A2A and stablecoin no hold is possible (Audit 2 PAY-17), so a scam that passes the gate there is unrecoverable. On UK Faster Payments the APP reimbursement regime may pay the buyer outside ABS, but whether it covers an agent-initiated payment is uncertain: that outcome is a conditional recovery with loss bounds (buyer loses nothing to the whole amount), never a refund. Outcome categories are disjoint. Amounts are nominal in each scenario's currency and are never added across currencies. Assumptions stated in `antiscam.py`.

**A_no_gate** (54 rows = 46 scams + 8 honest look-alikes + 0 other anti-scam cases decided by the rules, not the gate): scams: stopped 0, refunded 28, conditional recovery 3, unrecoverable 15 (buyer loss EUR 3,425.99; GBP 0.00 to 569.00; INR 899.00; USDC(token; no ISO 4217 code) 458.00; loss moved to acquirer/operator/agent provider/PSPs BRL 310.00; EUR 4,296.90; GBP 246.00 to 815.00; INR 329.00; USD(merchant) / EUR(card) 329.00; USDC(token; no ISO 4217 code) 59.00). Honest: blocked 0, payout delayed 0, step-up 0, clean 8. Other: {}.
| rail family | scams | stopped | refunded | conditional recovery | unrecoverable | buyer loss | system loss |
|---|---|---|---|---|---|---|---|
| a2a_push | 24 | 0 | 9 | 3 | 12 | EUR 3,425.99; GBP 0.00 to 569.00; INR 899.00 | BRL 310.00; EUR 798.00; GBP 246.00 to 815.00; INR 329.00 |
| bnpl | 2 | 0 | 2 | 0 | 0 | none | EUR 639.00 |
| card | 12 | 0 | 12 | 0 | 0 | none | EUR 2,164.00; USD(merchant) / EUR(card) 329.00 |
| crypto | 4 | 0 | 1 | 0 | 3 | USDC(token; no ISO 4217 code) 458.00 | USDC(token; no ISO 4217 code) 59.00 |
| marketplace | 2 | 0 | 2 | 0 | 0 | none | EUR 695.90 |
| stored_value | 1 | 0 | 1 | 0 | 0 | none | none |
| wallet | 1 | 0 | 1 | 0 | 0 | none | none |

**B_abs_gate** (54 rows = 46 scams + 8 honest look-alikes + 0 other anti-scam cases decided by the rules, not the gate): scams: stopped 38, refunded 5, conditional recovery 0, unrecoverable 3 (buyer loss EUR 938.00; INR 899.00; loss moved to acquirer/operator/agent provider/PSPs EUR 555.90; INR 329.00). Honest: blocked 4, payout delayed 1, step-up 3, clean 0. Other: {}.
| rail family | scams | stopped | refunded | conditional recovery | unrecoverable | buyer loss | system loss |
|---|---|---|---|---|---|---|---|
| a2a_push | 24 | 17 | 4 | 0 | 3 | EUR 938.00; INR 899.00 | EUR 329.00; INR 329.00 |
| bnpl | 2 | 2 | 0 | 0 | 0 | none | none |
| card | 12 | 12 | 0 | 0 | 0 | none | none |
| crypto | 4 | 4 | 0 | 0 | 0 | none | none |
| marketplace | 2 | 1 | 1 | 0 | 0 | none | EUR 226.90 |
| stored_value | 1 | 1 | 0 | 0 | 0 | none | none |
| wallet | 1 | 1 | 0 | 0 | 0 | none | none |

Residual loss paths with the gate on (Audit 0: 'never allow scammers in' is not claimable):

- ABS-S0209 (Z05, upi): unrecoverable_buyer_loss; buyer loss INR 899.00. 
- ABS-C048 (Z05, sepa_instant): unrecoverable_buyer_loss; buyer loss EUR 469.00. a hold was wanted but the funds reach the merchant's own account (merchant-account model): no hold possible
- ABS-C049 (Z05, sepa_instant): unrecoverable_buyer_loss; buyer loss EUR 469.00. 

Honest merchants affected by the gate:

- ABS-S0217 (Z09, sepa_instant): honest_blocked_false_positive (trust_score_52_below_min_60; delay 0 days)
- ABS-S0218 (Z09, open_banking_pis): honest_blocked_false_positive (trust_score_52_below_min_60; delay 0 days)
- ABS-S0219 (Z10, gift_card_stored_value): honest_passed_with_step_up (hold/step-up; delay 0 days)
- ABS-S0220 (Z10, card_debit_3ds): honest_passed_with_step_up (hold/step-up; delay 0 days)
- ABS-S0435 (Z09, marketplace_split): honest_blocked_false_positive (trust_score_52_below_min_60; delay 0 days)
- ABS-C052 (Z09, sepa_instant): honest_blocked_false_positive (trust_score_52_below_min_60; delay 0 days)
- ABS-C053 (Z09, sepa_instant): honest_delayed_payout (hold/step-up; delay 12 days)
- ABS-C054 (Z10, card_credit_3ds): honest_passed_with_step_up (hold/step-up; delay 0 days)

Paths minimised: where a payee PSP holds the payout (cards, wallets, BNPL, platforms, A2A acquiring) a scam that passes the gate is not paid before delivery and non-delivery is refunded from held funds; card and wallet buyers also keep their own dispute route. Paths still open (honest residual): any scam that passes the gate on merchant-account A2A or stablecoin (no hold is possible, nothing to collect from); an exit scam or sleeper after probation; counterfeit found outside the inspection window; collusion with the agent provider; a payment moved off the bound credential (ABS-P1 puts it on the agent provider, it does not prevent it). 'Never allow scammers in' is not claimed.

### Scammer entry routes

| route | gate that stops it | classification | max buyer loss before detection without hold (by rail) | with payee-PSP hold (A2A: acquiring model only) | proposed fix |
|---|---|---|---|---|---|
| synthetic_identity | onboarding_kyb | closed | sepa_ct: 0.0; pix: 0.0; card_credit_3ds: 0.0 | sepa_ct: 0.0; pix: 0.0; card_credit_3ds: 0.0 | none needed beyond KYB; keep LEI/registry lookups live |
| stolen_business_identity | onboarding_kyb | closed | marketplace_split: 0.0; card_credit_3ds: 0.0; sepa_instant: 0.0 | marketplace_split: 0.0; card_credit_3ds: 0.0; sepa_instant: 0.0 | notify the impersonated business; blocklist the payout account |
| shell_nominee | continuous_monitoring | limits_loss | wallet: 0.0; upi: 600.0 | wallet: 0.0; upi: 0.0 | probation payout hold on every new entity; beneficial-owner liveness check; cap prepaid volume in probation |
| payout_name_mismatch | onboarding_kyb | closed | bnpl: 0.0; card_cross_border_dcc: 0.0; upi: 0.0 | bnpl: 0.0; card_cross_border_dcc: 0.0; upi: 0.0 | none |
| domain_brand_impersonation | onboarding_kyb | closed | card_on_file_token: 0.0; uk_fps: 0.0 | card_on_file_token: 0.0; uk_fps: 0.0 | keep the mark list current; re-screen on catalogue changes |
| transaction_laundering | per_purchase_reattestation | limits_loss | open_banking_pis: 0.0; crypto_stablecoin_x402: 0.0; marketplace_split: 0.0; sepa_instant: 0.0 | open_banking_pis: 0.0; crypto_stablecoin_x402: 0.0; marketplace_split: 0.0; sepa_instant: 0.0 | mandatory Offer Feed signing; MCC/catalogue drift monitoring; the front merchant answers for records signed with its key |
| sleeper_exit | continuous_monitoring | limits_loss | card_debit_3ds: 0.0; sepa_instant: 14070.0 | card_debit_3ds: 0.0; sepa_instant: 12663.0 | payout hold on prepaid orders with delivery more than 14 days out for all merchants; rolling reserve sized to prepaid exposure; velocity alarm against a seasonal baseline |
| collusion_steering | none | open | pix: unbounded (route open; conforming goods at inflated price); gift_card_stored_value: unbounded (route open; conforming goods at inflated price); card_credit_3ds: unbounded (route open; conforming goods at inflated price) | pix: unbounded (route open; conforming goods at inflated price); gift_card_stored_value: unbounded (route open; conforming goods at inflated price); card_credit_3ds: unbounded (route open; conforming goods at inflated price) | incentive disclosure in the Mandate (ABS-X2); routing audits; cross-provider price-dispersion monitoring; joint liability (ABS-X1); still not a gate |
| expelled_reentry | shared_blocklist | closed_if_blocklist_shared | card_credit_3ds: 0.0; sepa_ct: 0.0 | card_credit_3ds: 0.0; sepa_ct: 0.0 | shared cross-programme blocklist (as card schemes keep for terminated merchants); fingerprint beyond the company name |
| honest_micro | none | honest_passes_with_probation_cost | upi: 0.0; marketplace_split: 0.0 | upi: 0.0; marketplace_split: 0.0 | shorten probation on clean delivery history; cap, not refuse |
| honest_seasonal | none | honest_passes_false_alarm_risk | card_cross_border_dcc: 0.0; wallet: 0.0; uk_fps: 0.0 | card_cross_border_dcc: 0.0; wallet: 0.0; uk_fps: 0.0 | seasonal baseline from prior years; reserve increase instead of suspension |
| honest_entity_change | none | honest_passes_with_short_hold | uk_fps: 0.0; bnpl: 0.0 | uk_fps: 0.0; bnpl: 0.0 | continuity fast-path |

Routes fully closed: synthetic_identity, stolen_business_identity, payout_name_mismatch, domain_brand_impersonation, expelled_reentry. Routes that only limit loss: shell_nominee, transaction_laundering, sleeper_exit. Routes still open: collusion_steering. Honest routes pass with a cost: honest_micro, honest_seasonal, honest_entity_change.

### Product specification (binding merchant-signed spec)

47 spec scenarios. With the signed spec, conformity is decided attribute by attribute with units and tolerances; free text is non-binding. In legacy mode (free text only, no signed spec) 47 of 47 become undecidable on conformity and fall to the unsigned-spec rule (ABS-S1: participant without a signed spec answers for its ambiguity). Decidable with the signed spec: 38; decidable in legacy mode: 0. That difference is the value of the standard.

### Agent Allowance

41 scenarios. v0.1: determinate 39, consistent with the stipulated ground truth 15 (it sees only five limits); v0.2: determinate 41, consistent 41/41. Liability: an encoded Allowance breach is the agent provider's (AG1-P); an unencoded household or company rule stays with the user; where the credential control that encoded the limit failed to decline, the agent provider has recourse against the enforcement layer (ABS-9) and the buyer is never routed there. New remedy classes needed: cure (corrected invoice/e-invoice) and a no-loss finding (payment-terms breach).

### Commerce segments

| segment | n | v0.1 determinate/consistent | v0.2 determinate/escalated/consistent | v0.1 gaps | v0.2 gaps | v0.1 unresolved conflicts | v0.2 unresolved conflicts |
|---|---|---|---|---|---|---|---|
| A2A | 13 | 13/11 | 13/0/13 | 0 | 0 | 0 | 0 |
| B2B | 23 | 23/5 | 23/0/23 | 0 | 0 | 0 | 0 |
| B2B2C | 31 | 30/25 | 31/0/31 | 1 | 0 | 0 | 0 |
| B2C | 424 | 397/281 | 422/2/424 | 27 | 0 | 4 | 0 |
| B2G | 10 | 8/4 | 10/0/10 | 2 | 0 | 0 | 0 |
| C2C | 13 | 13/11 | 13/0/13 | 0 | 0 | 0 | 0 |
| C2G | 14 | 14/3 | 14/0/14 | 0 | 0 | 0 | 0 |

Overlays per segment are in each scenario's `segment_overlay` (B2C consumer rights and chargebacks; B2B contract terms, PO/approval workflows, VAT reverse charge, EN 16931/Peppol e-invoice, net-30 credit transfers; B2G procurement thresholds, framework allowlists, mandatory e-invoicing to public bodies, audit trail; C2G administrative appeal and authority refunds, no chargeback; C2C platform rules and payout hold, no merchant obligations; B2B2C responding party per line; agent-to-agent: only signed Snapshot and signed negotiation record bind). Legal statements are general and marked.

## Reproduction

```
python3 standard/scenarios/generate.py      # catalogue.json, CATALOGUE.md
python3 standard/scenarios/validate.py      # structural validation of catalogue.json
python3 standard/scenarios/sample.py        # llm_sample.json
python3 standard/sim/run.py                 # REPORT.md, results.json, receipts.jsonl
python3 -m unittest discover -s standard/sim -t .
```

# Audit 2: Regulatory and standards audit of ABS v0.2

Subject: `standard/ABS_v0.2.md` (Part A, Part B, appendices) and `standard/LANDSCAPE.md` (rows marked
pending or UNVERIFIED). Date: 2026-11-04. Read-only audit; nobody was contacted.

Method. Every verdict rests on a primary text read on 2026-11-04 (source key at the end). EUR-Lex
blocks scripted access (AWS WAF challenge), so EU acts were read from the Publications Office
repository (`http://publications.europa.eu/resource/celex/<CELEX>`), which serves the same Official
Journal text; the canonical ELI is given in the key. Five research lanes run by this audit fetched
the texts; I re-read DSA Art 30, Rome I Art 6, Brussels Ia Art 19, Directive 2014/55 Arts 7 and 11,
Directive 2025/516 and SGD Arts 6 and 7 myself. mastercard.com (HTTP 403), the Council press pages
(403) and the EMVCo tokenisation PDF (click-through terms) could not be read; items that depend on
them are marked unverifiable. Dates marked "computed" are counted from the act's entry-into-force
clause, not printed in it.

Verdicts: **correct** / **partly correct** / **wrong** / **unverifiable**.

---

## 1. Executive summary

1. **Citations are mostly sound; mechanics are not.** Article numbers, dates and quotes ABS takes from
   Audit 0 hold on the primary text: Visa §4.1.23.10 is verbatim; AI Act Annex III 8(a), GDPR
   Art 22(3), CRD Art 9, SGD Arts 6, 7(5), 10, 11 and 21, Rome I Art 6(2), Brussels Ia Arts 17–19 and
   DSA Art 30 are correct. Several "pending/UNVERIFIED" rows can now be closed: Regulation (EU)
   2026/1744 (Annex III high-risk obligations from 2 Dec 2027), Directive (EU) 2025/2647 (applies from
   20 Sep 2028), the IPR Verification of Payee dates, the UK APP cap/excess/split and the Web Bot Auth
   working group.
2. **The A2A settlement mapping promises reversals that do not exist.** A SEPA recall (camt.056) "can
   be initiated only by the Originator PSP" on three grounds (duplicate, technical error, fraud) or
   as a request that depends "on the consent of the Beneficiary"; the pacs.004 return then needs the
   merchant's consent, and SCT Inst has no return at all. camt.027/camt.087 are interbank inquiries
   about funds, not goods. Against a merchant that refuses to pay, the only tool is ABS's contractual
   collection right.
3. **A Decision Center cannot raise a card dispute.** Under Visa a dispute is "A Transaction that an
   Issuer returns to an Acquirer"; only the issuer, at the cardholder's request, can start one. ABS's
   lifecycle (60 days to file, then 10+10+30+10) can outrun Visa's 120-day limit for 13.1.
4. **"Single track" must go.** A6.1 makes a buyer who opens an ABS case "assign to the programme any
   rail dispute". That contradicts ABS's own non-goal (A1.3) and Visa §5.4.2.5 ("must not require a
   Cardholder to waive the right to dispute"), and is presumptively unfair under UCTD Annex 1(q).
5. **The A2A payout hold, as drafted, conflicts with PSD2 Art 87(2) and the IPR.** Funds credited to a
   merchant's payment account must be "at the payee's disposal immediately", and Art 61(1) does not
   let businesses waive this; instant transfers must be available "within 10 seconds". The hold works
   only as A2A acquiring, with the PSP as payee. Card-side acquirer holds are unaffected.
6. **Payments law is misapplied at Step 0 and in the SCA mapping.** PSD2 decides "authorised" by
   consent "in the form agreed between the payer and the payment service provider" (Art 64), not by
   ABS mandate validity; without SCA the payer "shall not bear any financial losses unless the payer
   has acted fraudulently" (Art 74(2)). A max-amount mandate with an open payee set is not dynamic
   linking (Art 97(2); RTS Art 5). EBA Q&A 2019_4664 concerns direct-debit mandates; the
   merchant-initiated transaction (MIT) Q&A is 2018_4031, and its condition (no "specific action of
   the payer") sits badly with an agent buying for the payer. ABS also misses the PSD2 Art 76 refund
   right for authorised payee-initiated payments of unspecified amount.
7. **Licensing overreach sits in three places.** (a) The programme guarantee, which pays buyers for
   merchant default and forged Register entries out of programme fees, looks like credit, suretyship
   or financial-loss cover (Solvency II Annex I classes 14–16, prior authorisation). (b) The
   Settlement Instruction lets the "arbiter" be payer or payee, which is money remittance. (c) Agent
   providers that initiate A2A payments need payment-initiation authorisation. The Decision Center
   itself needs no licence, but it is not an "ADR entity" unless nationally listed, so "accredited"
   overstates.
8. **AI, data and consumer gaps are specific.**
   - High-risk treatment is right. Recital 61 strengthens it: ADR outcomes that "produce legal effects
     for the parties" are high-risk, and "the final decision-making must remain a human-driven
     activity".
   - GDPR Art 22(2)(a) needs a contract "between the data subject and a data controller", and
     consumers and sole traders have none with the Decision Center.
   - Advance `accepted_deviations` is unlikely to meet SGD Art 7(5), which requires acceptance "when
     concluding the sales contract".
   - "Free text binds nobody" conflicts with SGD Arts 6(a) and 7(1)(d).
   - The CRD Art 11a withdrawal function, which applies from 19 June 2026, is missing.
   - Standards: ISO 9001:2015 and ISO/IEC 27701:2019 are withdrawn; ISO 10003 is guidance only; the
     JOSE "EdDSA" identifier is deprecated (RFC 9864); no consumer-electronics product passport
     exists yet; PSD3/PSR is at the Council's first-reading position (29 Oct 2026) and not yet in the
     Official Journal.

---

## 2. Claims table

Source keys (S-numbers) are listed in section 6, each with URL and access date.

### 2.1 EU and UK payments

| ID | ABS § | Claim | Verdict | Primary source (brief quote) | Fix |
|---|---|---|---|---|---|
| PAY-01 | A10.2; LANDSCAPE §2 | PSD2 applies from 13 Jan 2018 | correct | S1 Art 115(2): "They shall apply those measures from 13 January 2018." Art 115(4) defers Art 97 to 18 months after the RTS (S2 Art 38(2): "shall apply from 14 September 2019") | Close the "pending" row. Cite Arts 115(2) and (4). |
| PAY-02 | A10.2 | Unauthorised payments: refund right; limited payer liability unless gross negligence or fraud | correct | S1 Art 73(1): refund "no later than by the end of the following business day"; Art 74(1): "up to a maximum of EUR 50" unless "fraudulently or ... with intent or gross negligence" | Cite Arts 71(1) (13 months), 72, 73 and 74(1). Add Art 74(2) (PAY-04). |
| PAY-03 | A10.2 "Authorised but disputed"; A1.3 "On account-to-account rails, where no such right exists" | Payment rules give no refund right for authorised payments; A2A rails have none | partly correct | S1 Art 76(1): refund where "(a) the authorisation did not specify the exact amount" and "(b) the amount ... exceeded the amount the payer could reasonably have expected"; "for direct debits ... the payer has an unconditional right to a refund"; Art 77(1): "8 weeks". S11 SDD Core: "within eight weeks ... no-questions-asked basis". PSR keeps this as Art 65 (S6) | Say: "No refund right for authorised **push** payments. For payee-initiated payments (card, MIT, direct debit), PSD2 Arts 76–77 give an 8-week refund where the amount was not specified and exceeded reasonable expectations; SDD Core is unconditional." In A1.3, read "on push A2A rails". Note that a card purchase under a `max_total` mandate may meet Art 76(1)(a); add to the double-recovery rule (A15.1 item 5). |
| PAY-04 | A4.1 Step 0 | Mandate not created with SCA by a PSP ⇒ "the case is an unauthorised payment"; "A Mandate without strong authentication is invalid" | wrong (as a statement of law) | S1 Art 64(2): consent "shall be given in the form agreed between the payer and the payment service provider ... may also be given via the payee or the payment initiation service provider". Art 74(2): "Where the payer's payment service provider does not require strong customer authentication, the payer shall not bear any financial losses unless the payer has acted fraudulently." S14 Visa glossary: an Agentic Payment Provider "is considered to be the Cardholder for an Agentic Transaction" | Keep "invalid" as a programme rule only. Replace the legal mapping with: "Whether the payment is unauthorised is decided by the payer's PSP under PSD2 Arts 64 and 72–74 and scheme rules. ABS refers the case, supplies the Mandate record and records the outcome." State the Art 74(2) consequence. |
| PAY-05 | A5.8; A10.2; B3.3; LANDSCAPE SCA row | EBA Q&A 2019_4664: a mandate set up without the payer's PSP is not an SCA event; MITs are payee-initiated after an authenticated set-up (cited to 2019_4664) | partly correct; wrong citation for MIT | S3 2019_4664 asks about "mandates for direct debits" and answers: "Mandates given by the payer to the payee set up without the direct involvement of the payer's PSP are not subject to SCA." S4 2018_4031: payee-initiated "provided that those transactions do not need to be preceded by a specific action of the payer"; remote set-up "is subject to strong customer authentication". Both non-binding (DG FISMA) | Cite 2019_4664 only for direct-debit mandates. Cite 2018_4031 and 2018_4131 for MIT. Add: an agent purchase is an action on the payer's side, so treating autonomous agent purchases as MIT is doubtful. |
| PAY-06 | A10.2; A12.1; B3.3 | Autonomous purchases rely on SCA exemptions: low value with counters, trusted beneficiaries, recurring fixed amount, TRA, secure corporate | correct on scope; conditions missing | S2 Art 13 (list created "through the payer's account servicing payment service provider"); Art 14 ("same amount and with the same payee"); Art 16 ("not exceed EUR 30"; cumulative EUR 100 or 5); Art 17 ("only made available to payers who are not consumers, where the competent authorities are satisfied"); Art 18 + Annex (EUR 100/250/500 tiers by fraud rate) | Add article numbers and limits. Arts 13 and 14 need a named payee, so an "any merchant in category" Allowance cannot use them. Above EUR 30, an autonomous card purchase depends on the PSP's TRA, at most EUR 500. Art 17 needs the competent authority's satisfaction. The B3.1 default (autonomous to 50, notify-and-hold to 150) is not SCA-neutral. |
| PAY-07 | A6.5 A2A flow: "SCA satisfied by mandate or approval reference"; A4.2, A11.3 "one strong-authentication tap" over the mandate | Mandate SCA covers later payments | partly wrong | S1 Art 97(2): "elements which dynamically link the transaction to a specific amount and a specific payee". S2 Art 5(1): "any change to the amount or the payee results in the invalidation of the authentication code" | A mandate with `max_total` and an open payee set is consent capture, not payment SCA. Only a per-purchase approval through the payer's PSP, or an exemption, satisfies SCA for the payment. Fix A6.5 and A11.3. |
| PAY-08 | A10.2 IPR row; LANDSCAPE IPR row | IPR (EU) 2024/886: VoP and price parity, dates pending | correct; dates now known; scope wording partly wrong | S5 (Art 5c of Reg 260/2012 as inserted): "A payer's PSP shall offer the payer a service ensuring verification of the payee to whom the payer intends to send a credit transfer". VoP: euro area by 9 Oct 2025, non-euro by 9 Jul 2027 (Art 5c(9)). Price parity: 9 Jan 2025 / 9 Jan 2027 (Art 5b(3)). Instant availability "within 10 seconds" (Art 5a(4)(c)). Liability: "the payer's PSP shall without delay refund" (Art 5c(8)). EIF 8 Apr 2024 (computed) | Insert the dates. VoP applies to all SEPA credit transfers, not only instant ones; retitle the row "Credit transfers (IPR)". |
| PAY-09 | A10.2 IPR row: "Not changed by PSD3" | — | partly wrong | S6 PSR (Council position ST 8543/26) Art 51: Art 5c(1)–(7) "shall apply mutatis mutandis to all credit transfers, including those that fall outside the scope of Regulation (EU) No 260/2012"; applies 27 months after entry into force | Say: "PSR Art 51 extends payee verification to all credit transfers." |
| PAY-10 | A6.2 `payee_name_check` enum | match / close_match / no_match / not_performed | partly correct | S10 EPC VOP RB 2026 v1.1, AT-R001: "Match • No Match • Close Match with the Name of the Payment Counterparty • Verification check not possible" | Add `verification_not_possible`. Store the name returned on a close match. |
| PAY-11 | A10.2; LANDSCAPE PSD3/PSR row | "Coreper approval on 28 Oct 2026; final adoption and OJ publication not confirmed" | partly correct (out of date) | S6/S7: provisional agreement 27 Nov 2025; Coreper confirmation 22 Apr 2026; ECON 5 May 2026; **Council adopted its first-reading positions 29 Oct 2026** (ST 8543/26 PSR, 8535/26 PSD3); EP second reading indicative 14 Dec 2026; not in the OJ. PSR "21 months from the date of entry into force" (Arts 51 and 58: 27 months) | Restate as "Council first-reading position of 29 Oct 2026; EP second reading pending; not in the OJ". Map PSR articles by the Council numbering. On the indicative timetable PSR application is not before late 2028 (computed). |
| PAY-12 | A10.2 | Impersonation-fraud liability does not reach "authorised but wrong" by an agent | correct | S6 PSR Art 60: refund where a consumer "has been manipulated by a third party pretending to be the consumer's payment service provider"; the texts contain no AI-agent provision | Keep. Add PSR Art 50(2): a transaction is "deemed to be unauthorised where the transaction was initiated or modified by a third party who is acting without the consent of the payer". Whether an injection-steered agent payment (AG4) falls under it is an open question for A15.1. Also add the Art 52 spending limits (users may set "a limit of a maximum amount") as a rail-side Allowance control. |
| PAY-13 | A6.1 (A2A recall "only where the rail allows it"); A6.3 row "Reversal against a merchant that does not pay"; A6.5; A10.3 | pacs.004 return or camt.056 recall plus camt.029 reverse a payment to a non-paying merchant "where the scheme supports them" | wrong (in substance) | S8 SCT RB §4.3.2.3 recall reasons: "Duplicate sending; Technical problems ...; Fraudulent originated ..."; "The Recall procedure can be initiated only by the Originator PSP". Request for Recall by the Originator (AC03/AM09/CUST): "It will depend on the consent of the Beneficiary whether to turn back the Funds". Return "must not be used in cases where the Beneficiary's account has already been credited and the Beneficiary wishes to return the funds". S9 SCT Inst: no Return; a pacs.004 "Repayment procedure" is accepted only for the 2028 rulebook | Delete pacs.004/camt.056 from the non-paying-merchant row. State that on SCT and SCT Inst a refusing merchant can be reached only through the contractual collection right. A recall is a buyer's-PSP tool for fraud or error, outside ABS. camt.029 is the negative answer to a recall and pacs.004 the positive one, both at the beneficiary's discretion for customer-reason requests. |
| PAY-14 | A6.3 "Dispute messages between PSPs: camt.027, camt.087 ... the ABS case id travels in the case identification" | — | wrong | S8 SCT RB §4.4.1: "Claim of Non-Receipt: the Beneficiary claims not to have received the initial SEPA Credit Transfer"; camt.087 is for value-date correction; Case/Id is "the specific SCT inquiry reference of the Participant", Max35; neither message is in the SCT Inst IG | Delete the row. These are interbank inquiries about funds, and the case id belongs to the bank. |
| PAY-15 | A6.2 `abs_binding.reference_value` (maxLength 140) "in remittance information or end-to-end id" | — | partly correct | S8 AT-T009: "A maximum of 140 characters for unstructured Remittance Information"; EndToEndId is Max35Text; ISO 11649 RF reference recommended, not mandatory | Carry `ABS:<purchase_id>:<anchor16>` in unstructured remittance only. EndToEndId (35 chars) cannot hold a URN; define a ≤35-char token for it. |
| PAY-16 | A6.1; A10.1; A10.2 UK row; LANDSCAPE UK row | UK APP reimbursement from 7 Oct 2024; cap; possible excess; consumer standard of caution; civil disputes excluded; 50/50 split (values pending) | correct; values now known | S12 SD20 §3.2: "The implementation date is 7 October 2024". Cap notice: "The maximum level of reimbursement is set at £85,000". Excess "up to a maximum of £100 per claim". Claims "more than 13 months after the date of the final FPS APP scam payment" need not be reimbursed. Receiving PSP "must pay the sending PSP 50%". FPS (SD20) and CHAPS (SD21). The civil-dispute exclusion is on the PSR consumer page, not in SR1. SR1 §12.4 defines a scam as deceiving "a consumer into transferring funds" | Insert the values and instruments (SD20, SD21, SR1). Add: the definition turns on the consumer being deceived, so cover where only the buying agent was deceived is unverified. Add that the regime is moving to the FCA (FSM Bill, May 2026; S13), with a PSR consultation in Dec 2026 on guidance including "civil disputes". |
| PAY-17 | A1.3; A6.1; A6.3 payout-hold row; B1.2 A2A row: "The merchant's PSP holds the credited funds" | A2A payout hold by the merchant's PSP | partly wrong | S1 Art 87(2): the payee's PSP "shall ensure that the amount ... is at the payee's disposal immediately after that amount is credited"; Art 61(1) lets non-consumers derogate only from Arts 62(1), 64(3), 72, 74, 76, 77, 80 and 89, **not Art 87**. S5 Art 5a(4)(c): "within 10 seconds ... make the amount ... available on the payee's payment account" | Restate: an A2A hold is possible only where the payee is the PSP (A2A acquiring or a collection account, Annex I(5)) and the merchant is paid later under the acquiring contract. A hold on funds already credited to the merchant's own payment account is not available. Card holds by acquirers stand. |

### 2.2 Card schemes

| ID | ABS § | Claim | Verdict | Primary source (brief quote) | Fix |
|---|---|---|---|---|---|
| CRD-01 | A4.2; A10.1; LANDSCAPE Visa row | "Visa Core Rules (24 Oct 2026 edition, section 4.1.23.10)": cardholder "responsible for any actions taken by an Agentic Payment Provider ... as if the Cardholder initiated the Transaction" | partly correct (quote verbatim; wrong rulebook part) | S14 cover "24 October 2026"; §4.1.23.10 "Agentic Payment Provider – Cardholder Responsibility" (ID# 0031176): "A Cardholder is responsible for any actions taken by an Agentic Payment Provider as part of an Agentic Transaction as if the Cardholder initiated the Transaction." Page header "Visa Product and Service Rules / 4 Issuance"; tagged "Edition: Oct 2026 \| Last Updated: Apr 2026" | Cite "Visa Product and Service Rules, §4.1.23.10, ID# 0031176 (edition 24 Oct 2026; rule added Apr 2026)". Drop "cited from the audit, not re-verified". Also cite the glossary: an Agentic Payment Provider "is considered to be the Cardholder for an Agentic Transaction". |
| CRD-02 | A10.1 | Visa 4.1.23.3 consent, expiry, identity verification, acknowledgement; 4.1.23.2 registration; 4.1.23.11 disqualification | correct | S14 §4.1.23.3: "Clearly state the expiration date of the Cardholder-defined payment instruction"; "Obtain Cardholder acknowledgement that they are responsible for actions taken by the Agentic Payment Provider". §4.1.23.2: "register with Visa, directly or via an Agentic Payment Enabler". §4.1.23.11: "Visa may, at its sole discretion, disqualify" | Keep. Quote Visa's "Visa Intelligence Commerce specifications" with [sic]. |
| CRD-03 | LANDSCAPE Visa row | 4.1.23.8 "order confirmation retained 120 days" | partly correct | S14: "must make available to the Cardholder, for at least 120 days from the Processing Date, an order confirmation" | Reword to "made available to the cardholder for at least 120 days from the Processing Date". |
| CRD-04 | A10.1 | No agent-specific dispute condition in the Visa rules | correct | S14: conditions 10.1–10.5, 11.1–11.3, 12.2–12.7, 13.1–13.9; "agentic" appears only in Compelling Evidence for 10.4: "This also includes login IDs for an Agentic Payment Provider", "Effective for Disputes processed on or after 24 October 2026" | Keep. Note that an agentic login ID is one matching data element in the two-prior-undisputed-transactions test, not stand-alone evidence. |
| CRD-05 | A10.1 | "none public from Mastercard (UNVERIFIED)" | unverifiable | S16 Mastercard developer guide (guidance, not rules): "Standard fraud detection, chargeback rights, and dispute resolution processes apply to agentic transactions." Rulebooks returned 403 | Keep UNVERIFIED; cite the developer guide. |
| CRD-06 | A6.1; A6.3; A6.5 ("DC->>PSP: card: chargeback in the fitting category"); A6.2 `dispute_stage` | Card execution = chargeback, representment, pre-arbitration, arbitration, triggered on the Decision | partly wrong | S14 glossary: "Dispute: A Transaction that an Issuer returns to an Acquirer"; "Dispute Response"; "representment" appears 0 times. S16 Mastercard: "First Chargeback", "Second Presentment", pre-arbitration, arbitration | Only the issuer, on the cardholder's request, opens a dispute; the Decision Center supplies evidence. Delete the DC-to-PSP chargeback arrow. Make `dispute_stage` scheme-neutral (`first_dispute`, `response`, `pre_arbitration`, `arbitration`) and map it per scheme. The `dispute_category` enum (fraud, authorisation, processing error, consumer dispute) matches Visa's categories 10–13: keep it. |
| CRD-07 | A6.1 "Single track: a buyer who opens a Dispute Case assigns to the programme any rail dispute on the same payment" | — | wrong (contradicts A1.3; scheme- and consumer-law conflict) | S14 §5.4.2.5 (ID# 0008771): "A Merchant must not require a Cardholder to waive the right to dispute a Transaction, including an Agentic Transaction, with the Issuer." S32 UCTD Annex 1(q): "excluding or hindering the consumer's right to take legal action or exercise any other legal remedy". S25 ADR Dir Art 10(1) | Delete the assignment. Keep only reconciliation: a Decision refund is set off against any later rail recovery, and the Decision is offered as evidence. |
| CRD-08 | A3.3; A1.5 ("a rail deadline approaching") | Time limits: file within 60 days; response 10; escalate 10; decide 30; pay 10 | partly correct (risk to the buyer) | S14 §11.11.2.4, Table 11-93 (13.1): "120 calendar days from the last date that the Cardholder expected to receive the merchandise"; "Not to exceed 540 calendar days from the Transaction Processing Date"; 15-day waiting period | Add a deadline guard: before the scheme limit, the Decision issues or the user is told to file with the issuer, and ABS deadlines pause while a rail dispute runs. A5.9 retention ("at least 13 months after `delivered_at`") is shorter than Visa's 540-day ceiling in some cases; use the later of 540 days from processing and 13 months after delivery. |
| CRD-09 | A6.3; A10.3 "No card message lets a third party refund a cardholder" | — | partly wrong | S15 Visa Direct: "Originator to be either a licensed Visa Acquirer or a Third-Party Originator sponsored by a licensed Visa Acquirer"; business application identifiers "FD Funds Disbursement (general)", "MI Merchant Initiated OCT for Faster Refund". Mastercard Send Disbursements let "registered Program Participants ... disburse funds" | Say: "No card message lets a third party reverse the original purchase. A sponsored originator can push a new credit (Visa OCT, Mastercard Send) to the card." |
| CRD-10 | A9.1 credential row | EMVCo payment tokenisation provides "domain restriction and spend controls: merchant scope, per-transaction and periodic limits" | unverifiable (spend limits) | S17 EMVCo tokenisation page: Technical Framework v2.4, 9 Jul 2026; the specification is behind click-through terms | Attribute amount limits to issuer controls and agentic-token programmes, not to the EMVCo spec, until verified. |
| CRD-11 | A10.1; LANDSCAPE EMVCo row | EMVCo "Agentic Payments: Framework for Specifications v1.0", draft for comment from 1 Sep 2026 (content UNVERIFIED) | partly correct | S17 press release 1 Sep 2026: feedback "by Wednesday 30 September"; scope "card-based agentic payment scenarios where intent needs to be managed over time, such as recurring purchases, cumulative budgets and post-transaction activities"; "Intent Services" | Use the exact title "EMV® Agentic Payments – Framework for Specifications v1.0" and note the comment period closed 30 Sep 2026. Keep it distinct from "EMV® Agentic Payments Specification – Technical Framework v1.0" (comments closed 5 Aug 2026). Intent Services overlap the Allowance (cumulative budgets): profile them rather than duplicate them. |
| CRD-12 | A6.2 `authentication_ref`; A10.3 | EMV 3-D Secure | correct | S17: latest final v2.3.1.0 (31 Aug 2022); draft v2.4.0.0 (3 Jun 2026) | Pin v2.3.1. |
| CRD-13 | A4.2; A10.1; LANDSCAPE Amex row | Amex (Apr 2026) "will protect eligible customers from charges related to AI agent error" (press report; terms UNVERIFIED) | partly correct | S18 Amex page: "In the future, if a Card Member authorizes a registered AI agent ... American Express will protect eligible customers from charges related to AI agent error"; "Eligible agent errors include transactions where the purchase deviates from the Card Member-authenticated purchase intent"; US credit cards only; subjective intent such as "best" excluded; "Full terms and conditions will be made available in the future" | Cite the primary page. Describe it as announced and forward-looking, US credit cards and registered agents only. Note that Amex already draws the deviation-versus-subjective-intent line ABS presents as new (see section 4). |
| CRD-14 | A10.1 | Visa Trusted Agent Protocol with Cloudflare, 14 Oct 2025, on HTTP Message Signatures | correct | S20: "developed in collaboration with Cloudflare"; "Built upon the foundational HTTP Message Signature standard" | Keep. |
| CRD-15 | A5.2; A10.1 | AP2 and Mastercard Verifiable Intent contributed to FIDO, 28 Apr 2026; Payments TWG chaired by Mastercard and Visa | correct | S19: "drawing from initial contributions from Google (AP2) and Mastercard (Verifiable Intent)" | Keep. |
| CRD-16 | A10.1; LANDSCAPE | Mastercard Agent Pay registration and agentic tokens (Oct 2025); VAMP enforcement from 1 Oct 2025 | unverifiable | S16 (Mastercard 403; the developer guide confirms an "Agent Pay Acceptance Framework" and a trusted agent registry). S14 §10.4.3.1 refers VAMP to a non-public guide | Keep UNVERIFIED; do not quote dates or thresholds. |

### 2.3 AI and data

| ID | ABS § | Claim | Verdict | Primary source (brief quote) | Fix |
|---|---|---|---|---|---|
| AID-01 | A7.5(8) | AI Act Annex III 8(a) covers AI used "in a similar way in alternative dispute resolution" | correct | S21 Annex III 8(a): "...or to be used in a similar way in alternative dispute resolution;" | Cite EUR-Lex, not Audit 0. |
| AID-02 | A7.5(8); A15.1(6) | Whether a private contractual resolution centre is ADR under the AI Act is open | partly correct | S21 recital 61: AI systems used by ADR bodies "should also be considered to be high-risk when the outcomes of the alternative dispute resolution proceedings produce legal effects for the parties"; "the final decision-making must remain a human-driven activity" | Add recital 61. Decisions that bind participants by contract produce legal effects, so the high-risk assumption is the correct reading, not only caution. Record the tension between automated finality (A7.1) and "human-driven" final decisions as an open question. |
| AID-03 | A7.5(8) | Obligations: risk management, data governance, logging, transparency, human oversight, accuracy and robustness, QMS, conformity assessment, EU database registration ("article references to be verified") | correct but incomplete | S21: Arts 9, 10, 12, 13, 14, 15, 17, 43, 49, 71. Art 43(2): Annex III points 2–8 follow "internal control as referred to in Annex VI, which does not provide for the involvement of a notified body". Art 26 (deployers); Art 86 ("Right to explanation of individual decision-making"); Art 50(1); Art 27 FRIA only for "bodies governed by public law, or ... private entities providing public services" and Annex III 5(b)–(c) | Insert the article numbers. Name the AI Act provider (engine and rulesets) and the deployer (each node operator) per node. State that conformity assessment is internal control, with no notified body. Add Art 86 explanations for affected natural persons. Art 27 likely does not apply: state why. Art 6(3) does not apply because the fact-finders "materially influence" the outcome. |
| AID-04 | A7.5(8); LANDSCAPE AI Act row | Digital Omnibus moved Annex III obligations to 2 Dec 2027 (secondary; Regulation 2026/1744 UNVERIFIED) | correct (now verified) | S22 Regulation (EU) 2026/1744 of 8 July 2026, OJ L 24.7.2026, in force 27 Jul 2026 (computed). New Art 113(c): Chapter III Sections 1–3 apply from "(i) 2 December 2027 as regards ... Article 6(2) and Annex III; and (ii) 2 August 2028 as regards ... Annex I" | Cite the OJ and close the row. Note that Art 113(c) names Sections 1–3 only; the treatment of Section 5 (Arts 43 and 49) was not settled here. |
| AID-05 | A7.5(8); A7.1 | GDPR Art 22(3): human intervention, a right to express a view and to contest, on request | correct; legal basis missing | S23 Art 22(3): "at least the right to obtain human intervention on the part of the controller, to express his or her point of view and to contest the decision". Art 22(2)(a): "necessary for entering into, or performance of, a contract between the data subject and a data controller"; (c) "explicit consent" | Consumers and sole traders have no contract with the Decision Center operator, so 22(2)(a) may be unavailable and 22(3) then does not save the process. Obtain explicit consent to automated decision at filing, with a human-decided alternative, or make the human decision the default for natural persons. Add Arts 13(2)(f) and 15(1)(h) explanation duties (S24 C-203/22). |
| AID-06 | A7.5(4); LANDSCAPE GDPR row | "Merchants that are companies are outside the GDPR; sole traders and users are not" | partly wrong | S23 Art 1(1)–(2) protects natural persons. Directors, staff, beneficial owners (KYB data), contact persons and reviewers of company merchants are data subjects | Say: "a company is not a data subject; personal data about its people is in scope." |
| AID-07 | A5.9 | "erasure requests are deferred for that period" | partly correct | S23 Art 17(3)(e): erasure does not apply where processing is necessary "for the establishment, exercise or defence of legal claims" | Say: "erasure may be refused under Art 17(3)(e) while the record is needed for a claim", and justify the period under Art 5(1)(e). |
| AID-08 | LANDSCAPE | CJEU C-634/21 SCHUFA (7 Dec 2023); C-203/22 Dun & Bradstreet Austria (27 Feb 2025) | correct | S24: C-634/21 First Chamber, 7 Dec 2023; C-203/22, 27 Feb 2025 ("the procedure and principles actually applied") | Cite the official title of C-203/22: "CK v Magistrat der Stadt Wien" (Dun & Bradstreet Austria as other party). |
| AID-09 | A7.3(5); A7.5(7); A10.2 | ADR Directive 2013/11: expertise, independence and impartiality; limits on pre-dispute agreements; binding outcomes | correct (Arts 6, 10); partly (Art 11) | S25 Art 10(1): agreement "not binding on the consumer if it was concluded before the dispute has materialised and if it has the effect of depriving the consumer of his right to bring an action before the courts". Art 10(2): binding "only if they were informed of its binding nature in advance and specifically accepted this". Art 11 is "Legality". Art 2(2)(g) excludes "procedures initiated by a trader against a consumer". Art 20(2): authorities "list all the ADR entities" | Cite Art 10(2) for binding effect. Merchant-initiated claims (A3.2 item 8, ABS-D2) fall outside the statutory ADR scope. The Decision Center is not an "ADR entity" unless listed under Art 20. |
| AID-10 | A7.5(8); A10.3; LANDSCAPE ADR row | Directive (EU) 2025/2647: prior notice of automated means and review by a natural person (articles and dates UNVERIFIED) | correct (now verified) | S26: Directive of 16 Dec 2025, OJ 30.12.2025, in force 19 Jan 2026 (computed); transposition 20 Mar 2028; applies from 20 Sep 2028. New Art 5(2)(d): "(i) inform the parties in advance ... about their use; and (ii) ensure that the parties have the right to request that the outcome of the ADR procedure be reviewed by a natural person from the ADR entity meeting the requirements of Article 6(1)" | Cite it. The review right covers the **outcome**. It binds listed ADR entities only, so ABS adopts it voluntarily. Note the new third-country-trader route (joint request). |
| AID-11 | LANDSCAPE ADR row ("ODR platform status pending") | — | resolved | S27 Regulation 2024/3228: "submission of complaints to the ODR platform shall be discontinued on 20 March 2025"; repeal "with effect from 20 July 2025" | Close the row. No ABS flow may refer to the ODR platform. |

### 2.4 Consumer law

| ID | ABS § | Claim | Verdict | Primary source (brief quote) | Fix |
|---|---|---|---|---|---|
| CON-01 | A4.4; A1.1 | CRD: 14-day withdrawal from delivery for distance goods, at the buyer's cost unless the merchant agreed otherwise | partly correct | S28 Art 9(2)(b): the day the consumer "acquires physical possession of the goods". Art 14(1): direct cost of return "unless the trader has agreed to bear them or the trader failed to inform the consumer". Art 13(1): refund within 14 days, "using the same means of payment". Art 13(3): may withhold "until he has received the goods back, or until the consumer has supplied evidence of having sent back the goods, whichever is the earliest" | Add the "failed to inform" limb. In A6.5 and A11.5, "merchant refunds on receipt" must read "on receipt or proof of dispatch, whichever is earlier". Executing the refund "on the same rail" is correct (Art 13(1)). |
| CON-02 | A4.4; B2.3 | Art 16 exceptions: made to specification, sealed goods unsealed, digital content once started with consent, accommodation, transport, car hire and leisure on a date | partly correct | S28 Art 16(e): "sealed goods which are not suitable for return due to health protection or hygiene reasons and were unsealed after delivery"; 16(i) sealed audio, video or software; 16(m) needs prior express consent, acknowledgement of loss of the right **and** "confirmation in accordance with Article 7(2) or Article 8(7)"; 16(l) covers "transport of goods"; passenger transport is outside the Directive (Art 3(3)(k)) | Correct the list: sealed goods only on hygiene grounds, add (i), state the three (m) conditions, and treat passenger transport as out of scope rather than excepted. |
| CON-03 | (missing) A4.4; A11.5 | Withdrawal overlay | missing provision | S29 Directive 2023/2673 inserting CRD Art 11a: "the trader shall ensure that the consumer can also withdraw from the contract by using a withdrawal function"; "They shall apply those measures from 19 June 2026" | Require participating merchants to expose the Art 11a function and route the `withdrawal` remedy through it. Add to A15.1 whether an agent may use it for the consumer. |
| CON-04 | A4.3; LANDSCAPE SGD row | SGD 2019/771 Arts 6, 7, 10, 11, 21 | correct | S30 Art 10(1): "within two years"; Art 11(2): Member States "may maintain or introduce a period of two years"; Art 21(1): derogations "shall not be binding on the consumer" | Add Arts 10(3) and 11(2) (national extensions) and Art 13 (repair or replacement first). ABS remedies are a contractual add-on, never a substitute. |
| CON-05 | A4.3; A5.5 `accepted_deviations[]`; A15.1(3) | Advance acceptance recorded in the Mandate may satisfy Art 7(5) (open) | likely wrong as designed | S30 Art 7(5): no lack of conformity only if the consumer "was specifically informed that a particular characteristic of the goods was deviating ... and ... expressly and separately accepted that deviation when concluding the sales contract" | Capture acceptance per purchase, at the approval step, against the specific deviation of the offer actually bought (`approval_prompt_must_show` + deviation text + SCA reference). Treat a standing advance acceptance as ineffective in the EU. |
| CON-06 | A4.1 Step 1 ("Free text and non-binding attributes never ground this step"); A12.2 ("free text binds nobody") | — | partly wrong (as a legal statement) | S30 Art 6(a): goods must "be of the description ... as required by the sales contract"; Art 7(1)(d): qualities the consumer "may reasonably expect ... taking into account any public statement made by or on behalf of the seller ... particularly in advertising or on labelling" | Limit the sentence to the ABS decision: "Free text does not ground an ABS Step 1 finding; it may still ground a statutory conformity claim." |
| CON-07 | A1.1; A5.6; B2.3 (digital content profile) | Conformity for digital content under the SGD framing | partly wrong | S31 DCD 2019/770 Art 3(1) covers "digital content or a digital service"; Art 3(4) leaves goods with digital elements to the SGD | Cite the DCD for digital content and services. |
| CON-08 | A8.4; A10.2 | UCTD: significant imbalance; Annex 1(q) | correct | S32 Art 3(1): "significant imbalance"; Annex 1(q) continues: "unduly restricting the evidence available to him or imposing on him a burden of proof which ... should lie with another party"; 1(b): limiting rights "in the event of total or partial non-performance" | Add the evidence and burden limb. ABS-E2, ABS-D1 and the "signed records only" rules must not be imported into consumer-facing terms of agent providers or merchants. |
| CON-09 | A8.4; A10.2 | Rome I Art 6(2); Brussels Ia Arts 17–19 | correct | S33 Rome I Art 6(2): a choice "may not, however, have the result of depriving the consumer of the protection afforded to him by provisions that cannot be derogated from"; Brussels Ia Art 19: departures only by an agreement "entered into after the dispute has arisen" (or the other two cases) | Keep. State that `binding_effect.governing_law` and `forum` bind participants only. |
| CON-10 | A10.1; B1.3; B4 | DSA Art 30 trader traceability for marketplaces | correct | S34 Art 30(1): "Providers of online platforms allowing consumers to conclude distance contracts with traders shall ensure that traders can only use those online platforms ... if ... they have obtained the following information" | Keep. |

### 2.5 Security, quality and data standards

| ID | ABS § | Claim | Verdict | Primary source | Fix |
|---|---|---|---|---|---|
| STD-01 | A1.4; A5.8; A10.3 | RFC 8785 JCS, confidence high | correct | S44: Informational, Independent Submission stream, June 2020 | State that it is not IETF Standards Track. |
| STD-02 | A1.4; A6.4 `alg` enum | JWS algorithms "EdDSA (Ed25519) and ES256" | partly outdated | S44 RFC 9864 (Oct 2025) "deprecates those polymorphic algorithm identifiers"; IANA marks "EdDSA" Deprecated and registers "Ed25519" | Use `Ed25519` and `ES256`; accept `EdDSA` for verification of legacy objects only. |
| STD-03 | A7.5(3); A10.3 | RFC 9162 Certificate Transparency 2.0 | correct | S44: Experimental, Dec 2021 | Add "Experimental". |
| STD-04 | A5.2; A9.2; A10.3 | RFC 9421 high; Web Bot Auth drafts UNVERIFIED | correct / now verifiable | S44 RFC 9421: Proposed Standard, Feb 2024. S45 "webbotauth" WG chartered 2025-10-23; WG draft `draft-ietf-webbotauth-httpsig-protocol-01` (2026-10-29); the others are individual drafts | Cite the WG and draft; close the row. |
| STD-05 | A5.2; A10.3 | Mandate container: "AP2 v0.2 mandates (SD-JWT VCs); W3C Verifiable Credentials 2.0" | partly correct | S46 VC Data Model 2.0, W3C Recommendation 15 May 2025; DID Core 1.0, Recommendation 19 Jul 2022; SD-JWT is RFC 9901 (Nov 2025); SD-JWT VC is `draft-ietf-oauth-sd-jwt-vc-23` (IESG evaluation) | Treat these as two formats: AP2's SD-JWT VCs follow the IETF draft, not the W3C VCDM 2.0. Cite VC-JOSE-COSE (republished 13 Oct 2026) for W3C VCs secured with JOSE. |
| STD-06 | A6.4; A10.3; B1.3 | ISO 17442 LEI | correct | S42 ISO 17442-1:2020 and 17442-2:2020, confirmed 2026 | Cite both parts. |
| STD-07 | A5.3; A10.3 | ISO 18245 MCCs | correct | S42 ISO 18245:2023 (Edition 2) | Cite the edition. |
| STD-08 | A7.5(7); A10.3; LANDSCAPE ISO 1000x row | "ISO 10003 as the management-system reference" for accrediting operators; ISO 10001/10002/10003 URLs | partly wrong | S42 ISO 10003:2018 "Guidelines for dispute resolution external to organizations"; all three are guidance, not certifiable requirements. URLs: 10001 → /standard/71579, 10002 → /standard/71580, 10003 → /standard/71581 (LANDSCAPE lists 71580 twice) | Call ISO 10003 "guidance". The admission criteria are ABS's own; ADR-entity status comes only from national listing (AID-09). Fix the URLs. |
| STD-09 | A7.5(8); A10.3 | ISO/IEC 42001; ISO/IEC 23894 | correct | S42 42001:2023 (requirements, certifiable); 23894:2023 (guidance) | Keep. |
| STD-10 | A7.5(8); A10.3 | ISO/IEC 27001, 27002 | correct | S42 27001:2022 with Amd 1:2024; 27002:2022 | Cite the amendment. |
| STD-11 | A10.3; LANDSCAPE | ISO/IEC 27701 | outdated | S42: 27701:2019 "Withdrawn ... Revised by ISO/IEC 27701:2025", which is a stand-alone management system standard | Cite 27701:2025. |
| STD-12 | A7.5(5); A10.3 | ISO 22301 | correct | S42 ISO 22301:2019 current, flagged "to be revised" | Keep. |
| STD-13 | A10.3 ("ISO 9001 ... high") | ISO 9001 | wrong edition | S42: ISO 9001:2015 Withdrawn; ISO 9001:2026 published Sep 2026 | Cite ISO 9001:2026. |
| STD-14 | A6.2; A6.3; A10.3 | ISO 20022 message names | correct (names); applicability see PAY-13 and PAY-14 | S43: pacs.008 FIToFICustomerCreditTransfer (V14), pacs.004 PaymentReturn (V15), camt.056 FIToFIPaymentCancellationRequest (V12), camt.029 ResolutionOfInvestigation (V14), camt.027 ClaimNonReceipt (V10), camt.087 RequestToModifyPayment (V09), pain.001 CustomerCreditTransferInitiation (V13); ISO 11649:2009 | Keep the names. Scheme usage follows the EPC implementation guidelines (2019 versions). |
| STD-15 | A10.3; LANDSCAPE PCI row | PCI DSS v4.0.1; PCI Software Security Framework | partly outdated | S47: v4.0.1 current; "PCI DSS v4.0 will be retired on 31 December 2024". Secure Software Standard v2.0 published (date not on the page; library entry 2026-02-11); Secure SLC Standard v2.0 published 28 Sep 2026; PA-DSS "formally retired" 28 Oct 2022 | Cite SSF v2.0 standards with their 12-month transitions and state that PA-DSS is retired. |
| STD-16 | A13 | An agent provider that never sees a PAN "stays outside the card data environment for PCI DSS" | unverifiable here | PCI DSS scoping text not read | Soften to "can reduce PCI DSS scope; scope is assessed by the entity's QSA or acquirer". |
| STD-17 | A5.3; A10.3 | C2PA, confidence high, version unpinned | partly correct | S48: current specification 2.5 (Oct 2026) | Pin the version. |
| STD-18 | A8.5 ("electronics under a product passport"); A10.3; B2.1 | DPP under ESPR as a current data source for electronics | wrong for Nov 2026 | S41 ESPR in force 18 Jul 2024 (computed); Art 13(1) registry "By 19 July 2026". Working plan COM(2025) 187: steel 2026, textiles and tyres 2027, aluminium 2027, furniture 2028, mattresses 2029; electronics only through horizontal rules (repairability 2027; recycled content 2029). Battery Regulation Art 77(1): battery passport "From 18 February 2027" for LMT, industrial >2 kWh and EV batteries | Say: "No ESPR product passport applies to consumer electronics yet; the first battery passports apply from 18 Feb 2027 and do not cover portable batteries." Use GS1/GDSN as the structured source in the meantime. |
| STD-19 | A10.3; B2.1 | GS1 Digital Link, unpinned | partly correct | S49: "GS1 Digital Link Standard: URI Syntax, Release 1.7.0" (Aug 2026) | Pin the release. |
| STD-20 | A10.3 | eIDAS qualified seals and time stamps give legal weight | correct | S40 Art 35(2): "presumption of integrity of the data and of correctness of the origin"; Art 41(2): "presumption of the accuracy of the date and the time" | Keep. Wallet dates stay unverified. |
| STD-21 | A7.5(5); A10.3; LANDSCAPE DORA row | DORA applies where operators or participants are financial entities ("to the ICT services they use") | partly correct | S39 Art 2(1)(b): "payment institutions, including payment institutions exempted pursuant to Directive (EU) 2015/2366"; (d) e-money institutions; Art 64: applies from 17 Jan 2025; Art 30 contract terms; Art 31 critical ICT third-party providers | Say: "PSP, acquirer and EMI participants are DORA financial entities; a Decision Center operator serving them is an ICT third-party provider, bound by Art 30 contract terms and directly overseen only if designated under Art 31. Incident reporting duties sit with the financial entity." |
| STD-22 | B4 B2G row ("mandatory e-invoice to public bodies"; "Directive 2014/55/EU ... verify") | — | partly wrong | S35 Art 7: "Member States shall ensure that contracting authorities and contracting entities receive and process electronic invoices which comply with the European standard" | Say: "EU law obliges public buyers to receive EN 16931 invoices; any duty on suppliers to send them is national." |
| STD-23 | A10.3; B4 B2B row | ViDA "as adopted" | correct | S36 Council Directive (EU) 2025/516 of 11 March 2025; e-invoicing and digital reporting for intra-EU B2B from 1 July 2030 | Cite the number and date. |

### 2.6 Licensing and authorisation

| ID | ABS § | Claim | Verdict | Primary source | Fix |
|---|---|---|---|---|---|
| LIC-01 | B1.2 | "An ABS-operated escrow account would be a regulated payment service" | correct | S1 Annex I point 6 "Money remittance"; point 5 "acquiring of payment transactions" | Keep. Note that holding user value could also be e-money (S38 EMD2 Art 2(2)). |
| LIC-02 | A6.2 (`payer`/`payee.party_role` include `arbiter`); A10.3 (guarantee payout "`direction: collect` from the guarantee holder") | ABS holds no funds | wrong (internal contradiction) | S1 Annex I(6) | Remove `arbiter` from `payer` and `payee`. The arbiter never receives or pays money; payouts go from the licensed holder directly to the buyer. |
| LIC-03 | A6.1; ABS-P2 (A3.1, A4.1); A6.4 `programme_guarantee`; A15.1(14) | A programme guarantee, "funded by programme fees and held by a licensed entity", pays unpaid Decisions, forged-Register losses and infeasible executions | overreach (licence type unstated; normative rules depend on it) | S37 Solvency II Annex I: "14. Credit: insolvency (general) ..."; "15. Suretyship"; 16 miscellaneous financial loss; Art 14(1): "shall be subject to prior authorisation" | Until a legal opinion fixes the form (authorised insurer, credit-institution guarantee, or a programme operator's own undertaking that is not insurance), move ABS-P2 and every "the guarantee pays" outcome to Part B and stop promising the buyer payment from it. |
| LIC-04 | A6.1; A6.4 `collection_right`; A9.2 | Collection right "operated by a licensed PSP" (direct debit mandate, reserve, guarantee, netting) | partly correct | S1 Annex I(6) | Name the creditor: the licensed PSP or acquirer in its own licence, or the buyer directly. The programme or arbiter may not collect for onward payment. |
| LIC-05 | A1.1; A6.1 ("open-banking payment initiation" as a rail) | Agent pays by A2A initiation; no licence stated | missing | S1 Annex I point 7 "Payment initiation services." | Add: an agent provider that initiates payments from the user's account needs PISP authorisation or a licensed PISP partner; one that holds user funds needs PI or EMI authorisation. |
| LIC-06 | B4 C2C and B2B2C rows | Platform payout hold "by the platform's licensed PSP" | correct; incomplete | S6 PSR Art 2(2)(b) narrows the commercial-agent exclusion to an agent acting "on behalf of only the payer or only the payee, but not both" with "a real scope to negotiate" | Add that marketplaces and platforms cannot rely on the commercial-agent exclusion once PSR applies. |
| LIC-07 | A7.5(1),(7); A14 ("accreditation of the operator") | "Accredited" operator nodes | overreach in wording | S25 Art 20(2) (national listing is the only statutory status) | Say "admitted by the ABS governance body against published criteria". Do not imply statutory accreditation or ADR-entity status. |
| LIC-08 | A3.2(9); A7.1 | Decisions bind merchants and agent providers by contract and never bind consumers | correct | S25 Art 10(2) | Keep. This is what keeps the Decision Center outside ADR-entity and arbitration regimes. |

### 2.7 LANDSCAPE.md rows marked pending or UNVERIFIED: status after this audit

| Row | Was | Now |
|---|---|---|
| PSD2 article numbers | pending | verified (PAY-01 to PAY-04, PAY-17) |
| SCA RTS exemption articles | pending | verified (PAY-06); EBA Q&A citation corrected (PAY-05) |
| PSD3/PSR status | pending | Council first-reading position 29 Oct 2026; not in the OJ (PAY-11) |
| IPR application dates | pending | verified (PAY-08) |
| UK APP cap and split | pending | verified (PAY-16) |
| AI Omnibus number and dates | UNVERIFIED | verified: Regulation (EU) 2026/1744 (AID-04) |
| Directive 2025/2647 articles and dates | UNVERIFIED | verified (AID-10); ODR platform closed (AID-11) |
| DORA applicability | pending | verified scope (STD-21) |
| eIDAS | pending | seal and time-stamp effects verified; wallet dates not checked |
| Web Bot Auth | pending | verified (STD-04) |
| W3C VC 2.0, DIDs | pending | verified (STD-05) |
| ISO 20022 per-message applicability | pending | verified for SEPA (PAY-13 to PAY-15, STD-14) |
| ISO 11649, ISO 17442, ISO 18245, ISO 1000x, ISO/IEC 42001/23894/27001/27002/27701, ISO 22301, ISO 9001 | pending | verified; 27701 and 9001 editions wrong (STD-06 to STD-13) |
| EMV 3DS and tokenisation versions | pending | 3DS 2.3.1 and tokenisation v2.4 verified; token controls unverifiable (CRD-10, CRD-12) |
| EMVCo agentic framework content | UNVERIFIED | scope verified from EMVCo's own release (CRD-11) |
| Amex terms | UNVERIFIED | primary page read: forward-looking, US only, full terms pending (CRD-13) |
| Mastercard rules; ECM/MATCH; VAMP figures | UNVERIFIED | still unverifiable (CRD-05, CRD-16) |
| PCI DSS and SSF | pending | verified; SSF v2.0 (STD-15) |
| C2PA, GS1, ESPR/DPP | pending | verified; DPP claim corrected (STD-17 to STD-19) |
| EN 16931/Peppol, 2014/55 | pending | 2014/55 verified (STD-22); national mandates not checked |
| FAPI 2.0, Grant Management, ISO 8583 field, schema.org, ECLASS/ETIM, UCUM/ISO 80000, ISO 8000, IOSS/VIES, UNCITRAL ODR notes, NIST AI RMF, spend-control practice | pending | not checked by this audit (outside the priority areas) |

---

## 3. Top 10 corrections, ranked by risk

1. **Delete "single track" (CRD-07).** It purports to take the consumer's card dispute right, which
   Visa §5.4.2.5 forbids a merchant to require, UCTD Annex 1(q) presumes unfair and ABS A1.3 promises
   to keep. Highest legal and scheme exposure, and it undermines every "rights unaffected" statement.
2. **Rewrite the A2A reversal mapping (PAY-13, PAY-14).** No SEPA message reverses a credit transfer
   against a refusing merchant: recall belongs to the buyer's PSP on three grounds, the return needs
   the merchant's consent, SCT Inst has no return, and camt.027/087 are fund inquiries. As written,
   ABS tells buyers on A2A rails they have a path they do not have.
3. **Remove the Decision Center's chargeback trigger and add a scheme-deadline guard (CRD-06,
   CRD-08).** Only issuers raise disputes. A buyer who waits for an ABS Decision can lose the Visa
   13.1 right after 120 days.
4. **Restructure the A2A payout hold (PAY-17).** A hold on funds credited to the merchant's own
   payment account conflicts with PSD2 Art 87(2), which businesses cannot waive, and with IPR
   Art 5a(4)(c). It must run as A2A acquiring with the PSP as payee. B1's anti-scam claim on A2A
   rails depends on this.
5. **Resolve the programme guarantee's licence before it appears in Part A (LIC-03), and remove the
   arbiter from money flows (LIC-02, LIC-04).** A fee-funded promise to pay buyers for merchant default
   or forgery is presumptively insurance or suretyship. An arbiter that receives or pays funds is
   doing money remittance.
6. **Give the Decision Center a lawful GDPR Art 22(2) basis for natural persons (AID-05), assign AI
   Act provider and deployer roles per node, and add recital 61 (AID-02, AID-03).** "Human review on
   request" satisfies Art 22(3) only if 22(2)(a) or (c) applies, and (a) needs a contract the
   consumer does not have with the Center.
7. **Correct the payments-law mapping at Step 0 and SCA (PAY-04, PAY-05, PAY-07).** Authorisation is
   decided by the payer's PSP under Arts 64 and 72–74; Art 74(2) shifts the loss when SCA is absent;
   a mandate is not dynamic linking; the MIT citation is wrong. PSPs and issuers will reject ABS on
   these points first.
8. **Make deviation acceptance per purchase (CON-05) and limit "free text binds nobody" to the ABS
   decision (CON-06).** As drafted, consumers may lose statutory conformity rights the Directive
   preserves, and merchants would rely on acceptances that do not bind.
9. **State the PSD2 Art 76 refund right (PAY-03).** Card and MIT agent purchases with an unspecified
   final amount can carry an 8-week statutory refund. That changes the double-recovery rule (A15.1
   item 5) and the claim that "authorised but wrong" has no payment-law route.
10. **Bring the withdrawal overlay up to date (CON-01 to CON-03).** Add the CRD Art 11a withdrawal
    function (from 19 June 2026), the Art 14(1) "failed to inform" limb, the Art 13(3) proof-of-dispatch
    rule and the correct Art 16 exceptions.

Lower-risk hygiene: PSD3/PSR and Omnibus status (PAY-11, AID-04); Visa rulebook part and 4.1.23.8
wording (CRD-01, CRD-03); ISO 9001:2026, ISO/IEC 27701:2025, ISO 10003 as guidance, RFC 9864
`Ed25519`, C2PA 2.5, SSF v2.0 and the DPP claim (section 2.5).

---

## 4. What ABS should not claim

- That a Decision "executes" a chargeback, a SEPA recall or a return, or that a Decision Center can
  send one (CRD-06, PAY-13).
- That ABS reverses SCT or SCT Inst payments against a merchant that refuses; or that camt.027/087
  carry goods disputes (PAY-13, PAY-14).
- That a buyer "assigns" rail disputes to the programme, alongside "the buyer's right to them is
  untouched" (CRD-07).
- That a merchant's PSP can hold A2A funds already credited to the merchant (PAY-17).
- That "the programme guarantee pays the buyer" (ABS-P2, A6.1) before its licensed form exists
  (LIC-03).
- That SCA on the mandate covers later autonomous payments; that agent purchases are MITs; that EBA
  Q&A 2019_4664 supports either (PAY-05, PAY-07).
- That a payment without a PSP-performed SCA mandate is "an unauthorised payment" (PAY-04).
- That the payment rules give no refund right for any authorised payment (PAY-03).
- That "no standard covers" the authorised-but-wrong split: Amex's published terms cover purchases
  that deviate "from the Card Member-authenticated purchase intent" and exclude subjective intent,
  and EMVCo's Intent Services cover cumulative budgets (CRD-11, CRD-13). Claim the open, rail-neutral
  decision order and evidence standard, not the concept.
- "Compliance with the EU AI Act, the GDPR and ADR law" ("What ABS is", item 4). Say "designed
  against". No conformity assessment has been done, Art 22(2) has no basis yet, and Directive
  2025/2647 applies from 20 Sep 2028 and only to listed ADR entities (AID-05, AID-10).
- That nodes are "accredited" in any legal sense, or that the Decision Center is an ADR entity
  (LIC-07, AID-09).
- That advance `accepted_deviations` satisfies SGD Art 7(5) (CON-05); that "free text binds nobody"
  in consumer law (CON-06).
- That UK APP reimbursement covers scams where only the agent was deceived (PAY-16).
- That "no card message lets a third party refund a cardholder" (CRD-09).
- That electronics carry a Digital Product Passport today (STD-18).
- That an agent provider is automatically outside PCI DSS scope (STD-16).
- That PSD3/PSR is adopted, numbered or in force, or that the IPR is "not changed by PSD3" (PAY-09,
  PAY-11).
- Visa rules as "Visa Core Rules §4.1.23": they are Product and Service Rules (CRD-01).

---

## 5. What this audit could not verify

- **Mastercard:** Agent Pay launch date, agentic-token rules, any agentic chargeback reason code, and
  the Excessive Chargeback Program name. All mastercard.com pages returned 403; only the developer
  guide was readable.
- **Visa VAMP:** effective and enforcement dates and thresholds. The rules point to a non-public VAMP
  Guide.
- **EMVCo tokenisation:** whether "token domain restriction controls" include amount limits (the PDF
  is behind terms); 3RI by name in 3DS 2.3.1.
- **Council press releases (403):** the 29 June 2026 AI Omnibus adoption release (the Official
  Journal text was read instead) and the 21 Oct 2026 data/GDPR simplification position. No adopted
  amendment to GDPR Art 22 was found; that absence is unverified.
- **AI Act sections:** whether Regulation 2026/1744's postponement reaches Chapter III Section 5
  (Arts 43 and 49) or only Sections 1–3.
- **PCI:** the exact publication date of Secure Software Standard v2.0; PCI DSS scoping text for
  tokenised flows (STD-16).
- **ESPR:** the list of delegated acts actually adopted by Nov 2026 (the working plan was read, not
  each act).
- **UK:** Royal Assent of the Financial Services and Markets Bill (PSR-to-FCA transfer); whether APP
  reimbursement reaches agent-deceived payments; the date of the March 2025 consolidation
  announcement.
- **PSR text:** PSR Art 52's four-hour delay on limit increases (checked in the compromise text only).
  Entry-into-force dates marked "computed".
- **Not checked (outside the priority areas or owned by other lanes):**
  - EBA/ECB fraud baselines (A1.5)
  - UK CMA agent guidance (A8.4)
  - EPI Wero, NPCI, x402, AWS, Klarna, Pix MED
  - UCPD and Price Indication Directive rules for AG4-D reference prices
  - MiCA custody for the stablecoin "custodial hold"
  - AMLR reliance for "KYB reused by reference"
  - FAPI 2.0 and Grant Management; ISO 8583 reference fields; schema.org, ECLASS, ETIM, UCUM, ISO 8000
  - EN 16931 national mandates; IOSS and the customs reform; UNCITRAL ODR notes; NIST AI RMF; eIDAS
    wallet dates

---

## 6. Sources (all accessed 2026-11-04)

EU acts were read via `http://publications.europa.eu/resource/celex/<CELEX>`. The canonical ELI is
given.

| Key | Source | URL |
|---|---|---|
| S1 | PSD2, Directive (EU) 2015/2366 (CELEX 32015L2366) | https://eur-lex.europa.eu/eli/dir/2015/2366/oj |
| S2 | SCA RTS, Delegated Regulation (EU) 2018/389 (32018R0389) | https://eur-lex.europa.eu/eli/reg_del/2018/389/oj |
| S3 | EBA Single Rulebook Q&A 2019_4664 | https://www.eba.europa.eu/single-rule-book-qa/qna/view/publicId/2019_4664 |
| S4 | EBA Q&A 2018_4031; 2018_4131 | https://www.eba.europa.eu/single-rule-book-qa/qna/view/publicId/2018_4031 ; …/2018_4131 |
| S5 | Instant Payments Regulation (EU) 2024/886 (32024R0886) | https://eur-lex.europa.eu/eli/reg/2024/886/oj |
| S6 | Council register: PSR and PSD3 Council first-reading positions ST 8543/26 and 8535/26; ST 15005/26, 8220/26, 8221/26, 8222/26, 14798/26, 15152/26, 15154/26 | https://data.consilium.europa.eu/doc/document/ST-8543-2026-INIT/en/pdf (and the same pattern for each number) |
| S7 | EP Legislative Observatory 2023/0210(COD), 2023/0209(COD); EP press release 27 Nov 2025 | https://oeil.europarl.europa.eu/oeil/en/procedure-file?reference=2023/0210(COD) ; https://www.europarl.europa.eu/news/en/press-room/20251121IPR31540/payment-services-deal-more-protection-from-online-fraud-and-hidden-fees |
| S8 | EPC SCT Rulebook 2025 v1.2; SCT Inter-PSP IG 2025 v1.0 | https://www.europeanpaymentscouncil.eu/sites/default/files/kb/file/2026-09/EPC125-05%202025%20SCT%20Rulebook%20version%201.2.pdf ; …/2026-09/EPC115-06%20SCT%20Inter-PSP%20IG%202025%20V1.0.pdf |
| S9 | EPC SCT Inst Rulebook 2025 v1.2; SCT Inst IG 2025 v1.0 | …/kb/file/2026-09/EPC004-16%202025%20SCT%20Instant%20Rulebook%20v1.2.pdf ; …/2026-09/EPC122-16%20SCT%20Inst%20Inter-PSP%20IG%202025%20V1.0.pdf |
| S10 | EPC Verification of Payee Rulebook EPC218-23 2026 v1.1 | …/kb/file/2026-03/EPC218-23%20v1.1%202026%20Verification%20Of%20Payee%20Scheme%20Rulebook_0.pdf |
| S11 | EPC SDD Core Rulebook 2025 v1.2 | …/kb/file/2026-09/EPC016-06%202025%20SDD%20Core%20Rulebook%20version%201.2.pdf |
| S12 | PSR Specific Direction 20; SR1 (July 2024 comparison); cap notice Sep 2024; excess notice Dec 2023; consumer page | https://www.psr.org.uk/publications/legal-directions-and-decisions/specific-direction-20-fps-app-scam-reimbursement-requirement/ ; https://www.psr.org.uk/media/ng3bh0mp/amended-specific-requirement-1-july-2024-compared.pdf ; https://www.psr.org.uk/media/0w1fmnr5/sr1-max-limit-value-supplementary-sept-2024-publication-version.pdf ; https://www.psr.org.uk/media/maslkvyo/sr1-excess-value-supplementary-dec-2023.pdf ; https://www.psr.org.uk/information-for-consumers/app-fraud-reimbursement-protections/ |
| S13 | HM Treasury consultation response (updated 21 Apr 2026); PSR APP roadmap; PSR news | https://www.gov.uk/government/consultations/a-streamlined-approach-to-payment-systems-regulation-consultation/outcome/a-streamlined-approach-to-payment-systems-regulation-consultation-response ; https://www.psr.org.uk/our-work/app-scams/app-scams-policy-roadmap/ ; https://www.psr.org.uk/news-and-updates/latest-news/ |
| S14 | Visa Core Rules and Visa Product and Service Rules, 24 Oct 2026 | https://usa.visa.com/dam/VCOM/download/about-visa/visa-rules-public.pdf |
| S15 | Visa Direct developer pages; Visa request/response codes | https://developer.visa.com/capabilities/visa_direct ; https://developer.visa.com/request_response_codes |
| S16 | Mastercard developer: agentic commerce guide; Mastercom pre-arbitration; Send Disbursements | https://developer.mastercard.com/agentic-commerce-guide/ ; https://developer.mastercard.com/mastercom/documentation/use-cases/prearbprecomp/index.md ; https://developer.mastercard.com/mastercard-send-disbursements/documentation/ |
| S17 | EMVCo agentic framework release (1 Sep 2026); tokenisation; 3-D Secure | https://www.emvco.com/news-publications/emvco-requests-feedback-on-framework-for-secure-interoperable-and-scalable-card-based-agentic-payments/ ; https://www.emvco.com/emv-technologies/payment-tokenisation/ ; https://www.emvco.com/emv-technologies/3-d-secure/ |
| S18 | American Express agentic commerce page | https://www.americanexpress.com/en-us/company/agentic-commerce/ |
| S19 | FIDO Alliance, 28 Apr 2026 | https://fidoalliance.org/fido-alliance-to-develop-standards-for-trusted-ai-agent-interactions/ |
| S20 | Visa press release, Trusted Agent Protocol, 14 Oct 2025 | https://usa.visa.com/about-visa/newsroom/press-releases.releaseId.21716.html |
| S21 | AI Act, Regulation (EU) 2024/1689 (32024R1689) | https://eur-lex.europa.eu/eli/reg/2024/1689/oj |
| S22 | Digital Omnibus on AI, Regulation (EU) 2026/1744 | https://eur-lex.europa.eu/eli/reg/2026/1744/oj |
| S23 | GDPR, Regulation (EU) 2016/679 (32016R0679) | https://eur-lex.europa.eu/eli/reg/2016/679/oj |
| S24 | CJEU C-634/21 (62021CJ0634); C-203/22 (62022CJ0203) | http://publications.europa.eu/resource/celex/62021CJ0634 ; http://publications.europa.eu/resource/celex/62022CJ0203 |
| S25 | ADR Directive 2013/11/EU (32013L0011) | https://eur-lex.europa.eu/eli/dir/2013/11/oj |
| S26 | Directive (EU) 2025/2647 (32025L2647) | https://eur-lex.europa.eu/eli/dir/2025/2647/oj |
| S27 | Regulation (EU) 2024/3228 (32024R3228) | https://eur-lex.europa.eu/eli/reg/2024/3228/oj |
| S28 | CRD 2011/83/EU, consolidated 28.05.2022 (02011L0083-20220528) | https://eur-lex.europa.eu/eli/dir/2011/83/oj |
| S29 | Directive (EU) 2023/2673 (32023L2673) | https://eur-lex.europa.eu/eli/dir/2023/2673/oj |
| S30 | Sale of Goods Directive (EU) 2019/771 (32019L0771) | https://eur-lex.europa.eu/eli/dir/2019/771/oj |
| S31 | Digital Content Directive (EU) 2019/770 (32019L0770) | https://eur-lex.europa.eu/eli/dir/2019/770/oj |
| S32 | Unfair Contract Terms Directive 93/13/EEC (31993L0013) | https://eur-lex.europa.eu/eli/dir/1993/13/oj |
| S33 | Rome I, Regulation (EC) 593/2008 (32008R0593); Brussels Ia, Regulation (EU) 1215/2012 (32012R1215) | https://eur-lex.europa.eu/eli/reg/2008/593/oj ; https://eur-lex.europa.eu/eli/reg/2012/1215/oj |
| S34 | Digital Services Act, Regulation (EU) 2022/2065 (32022R2065) | https://eur-lex.europa.eu/eli/reg/2022/2065/oj |
| S35 | Directive 2014/55/EU (32014L0055) | https://eur-lex.europa.eu/eli/dir/2014/55/oj |
| S36 | Council Directive (EU) 2025/516 (ViDA) (32025L0516) | https://eur-lex.europa.eu/eli/dir/2025/516/oj |
| S37 | Solvency II, Directive 2009/138/EC (32009L0138) | https://eur-lex.europa.eu/eli/dir/2009/138/oj |
| S38 | EMD2, Directive 2009/110/EC (32009L0110) | https://eur-lex.europa.eu/eli/dir/2009/110/oj |
| S39 | DORA, Regulation (EU) 2022/2554 (32022R2554) | https://eur-lex.europa.eu/eli/reg/2022/2554/oj |
| S40 | eIDAS, Regulation (EU) 910/2014 and amending Regulation (EU) 2024/1183 | https://eur-lex.europa.eu/eli/reg/2014/910/oj ; https://eur-lex.europa.eu/eli/reg/2024/1183/oj |
| S41 | ESPR, Regulation (EU) 2024/1781; ESPR working plan COM(2025) 187; Battery Regulation (EU) 2023/1542 | https://eur-lex.europa.eu/eli/reg/2024/1781/oj ; http://publications.europa.eu/resource/celex/52025DC0187 ; https://eur-lex.europa.eu/eli/reg/2023/1542/oj |
| S42 | ISO catalogue pages: 17442-1 (78829), 17442-2 (79917), 18245 (79450), 10001 (71579), 10002 (71580), 10003 (71581), 42001 (81230), 23894 (77304), 27001, 27002 (75652), 27701:2025 (85819), 22301 (75106), 9001:2026 (88464), 11649 (50649) | https://www.iso.org/standard/<number>.html |
| S43 | ISO 20022 message catalogue | https://www.iso20022.org/iso-20022-message-definitions |
| S44 | RFC 8785, 9162, 9421, 9864, 7515, 7797, 8037, 9901 | https://www.rfc-editor.org/rfc/rfc8785 (and the same pattern for each number) |
| S45 | IETF webbotauth WG; draft-ietf-webbotauth-httpsig-protocol | https://datatracker.ietf.org/wg/webbotauth/about/ ; https://datatracker.ietf.org/doc/draft-ietf-webbotauth-httpsig-protocol/ |
| S46 | W3C VC Data Model 2.0; DID Core 1.0; VC-JOSE-COSE; IETF SD-JWT VC draft | https://www.w3.org/TR/vc-data-model-2.0/ ; https://www.w3.org/TR/did-core/ ; https://www.w3.org/TR/vc-jose-cose/ ; https://datatracker.ietf.org/doc/draft-ietf-oauth-sd-jwt-vc/ |
| S47 | PCI SSC: PCI DSS; Software Security Framework; document library | https://www.pcisecuritystandards.org/standards/pci-dss/ ; https://www.pcisecuritystandards.org/standards/software-security/ ; https://www.pcisecuritystandards.org/document_library/ |
| S48 | C2PA specification 2.5 | https://spec.c2pa.org/specifications/specifications/2.5/specs/C2PA_Specification.html |
| S49 | GS1 Digital Link standards | https://ref.gs1.org/standards/digital-link/ |

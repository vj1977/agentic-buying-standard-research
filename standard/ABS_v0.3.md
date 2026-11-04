# Agentic Buying Standard (ABS) v0.3

Status: draft for review, 2026-11-04. Not published. Idea and principles: Vadims Juruss.
Document structure after the founder's decision of 2026-11-04 and Independent Audit 0
(`audits/AUDIT_0_THESIS.md`): **Part A** is the normative core, the contribution. **Part B** is an
informative roadmap annex. v0.2 adopts the rules proposed by the rule-completeness simulation
(`standard/sim/REPORT.md`, rule set `scrolld.abs@0.2-proposed`), which measured v0.1 as written
against a 528-scenario catalogue and found 8 gap types, 4 unresolved conflicts and 58 contradiction
groups; the adopted wording closes all of them against that catalogue. No scheme rule number,
article or date is quoted unless it was verified or is cited from Audit 0 with its source;
unverified items are marked. v0.3 applies every correction of Audit 2 (`audits/AUDIT_2_REGULATORY.md`,
primary sources, 2026-11-04); Appendix D lists each of its rows and the resolution. v0.3 also folds in the first experimental
results (`results/PHASE2_DISPUTES.md`, `results/PILOT_RESULTS.md`): pre-registered, on a simulated
environment, small n, clustered intervals; they are cited as such. `LANDSCAPE.md`
holds the sources for everything in section A12. Where this document names a law, it says
"designed against", never "compliant with": no conformity assessment, legal opinion or regulatory
ruling has been obtained.

Change log, 2026-11-04 (Phase 3, `results/PHASE3_ATTACKS.md`): evidence provenance tiers added to the
rules of evidence and to every evidence-item schema (`provenance_tier`); a finding that moves
liability may no longer rest on party-authored evidence alone (A4.1 Step 1, A5.7); the end-to-end
judge is allowed only behind the provenance gate and a calibrated abstention rule, and continuous
optimised red-teaming with published attack-success figures is an admission condition (A7.3, A7.7);
a new failure mode, optimised manipulation of party-authored evidence, with the measured numbers
(A8.7); the core claim restated as "the independent record decides, not the judge" (withdrawn by
the Audit 1 entry below); the gate's
efficacy is being measured (Phase 3b) and no number is claimed for it yet (measured since: next entry).

Change log, 2026-11-04 (Phase 3b, `results/PHASE3B_PROVENANCE.md`, Amendment 14, Deviation 6): the
"Pending (Phase 3b)" notes replaced with the measured result (A5.7, A7.3, A7.9, A8.7, A15.1, A15.2);
three normative refinements the data motivates, all in A5.7: machine-checkable citations (the Finding's
citation field is now the structured `cited_evidence`, with item id and path, and an uncited Finding
cannot decide), a content check (the cited independent record must support the finding, compared
deterministically where it is structured), and the gate's fairness cost (ABS supplies independent
delivery-side records, and every node publishes its review rate by liable party, A1.5, A7.7, A8.4);
Decision `evidence_integrity.provenance_gate_reason` added; the Phase 3 confidence split corrected (A7.3,
A8.7; `results/PHASE3_ATTACKS.md`, correction of 2026-11-04). The refined gate is not yet measured.

Change log, 2026-11-04 (Audit 1 corrections, `audits/AUDIT_1_INDEPENDENT_AI_REVIEW.md`, findings F07, F10, F14, F15,
F29, F30): the opening premise narrowed to the real gap, faithful execution of delegated purchasing
intent, with merchant-performance claims left on the existing reason codes ("What ABS is", A3.1);
the binary `independent` / `party_authored` label replaced by a provenance description per evidence
item (issuer, stake, time of commitment, custody, authority for the fact) and a gate that names the
fact it needs; "the independent record decides, not the judge" withdrawn and replaced by what Phase 3
measured (A5.7, A8.7); one authenticated envelope context covering type, version, id, timestamp,
chain position, `prev_hash` and the body hash, and the A5.8 chain made a chain of those envelopes
(A5.3, A5.8); the anchor is the full SHA-256 head in independently authenticated storage, the rail
reference only a locator (A5.8, A6.2); wire version and schema ids moved to 0.3 with a stated
compatibility rule, type-to-body dispatch, `RefusalRecord`, `ActionEvent` and `Offer` bodies, the
capture fields required in the Mandate, and example instances (A5.3, B2.2, Appendix F); A5.2 no
longer calls the ABS object "the same container", and every AP2 / SD-JWT VC, UCP and ACP binding and
the federated network are marked PROPOSED, with one binding sketch (A5.2, A5.2.1, A7.5, A10); what
binds as an explicit term resolved (A4.1 Step 3, A3.1, Finding vocabulary). Appendix E lists each
finding and its resolution. Wording only: no experiment was re-run. The numbers re-analysed after
Audit 1 from stored records (no new model calls) are carried into the text by the note at the end
of Appendix E.

Change log, 2026-11-04 (adoption path and confirmation; `standard/ADOPTION_AND_CONFIRMATION.md`,
primary sources read 2026-11-04):

- A new normative section on who confirms the fact that decides an agent dispute (A4.5). It sets
  four routes: recomputation from signed records by any verifier, including the issuer at intake;
  a reading of records committed before the dispute by a neutral Decision Center; adverse
  inference; and the rail process. It names the parties that never confirm alone and gives the
  confirmation matrix in short form.
- Decision `confirmation_route` added.
- A PROPOSED `abs_binding.mandate_digest` added to the Settlement Instruction (A6.2).
- An informative staged path from a contractual programme to scheme rules, ISO 20022 and EPC
  change requests (B6).
- A10.1 now records Visa 4.1.23.2 and 4.1.23.3, Visa Intelligent Commerce instructions, and AP2
  v0.2's Dispute Evidence section; A10.1 and A15.1 item 11 point to B6.

Corrections after Audit 4 (`audits/AUDIT_4_INDEPENDENT_AI_FINAL_CHECK.md`), wording only:

- B6 Stage 2: the merchant remedy is narrow. A checkout that matches the user-authenticated
  instruction defeats only an AG1-type claim misfiled against the merchant, never a non-conformity,
  non-delivery or fraud claim (A4.1 Step 0 and Step 1).
- A4.5 and A5.7: the rule that a party's own record never proves a fact in its favour now states
  its one exception, test (c) (the provider's action log for causation in Step 2), and its limits.
- A4.5: AG4-D is deceptive offer content and sits with AG1-M and AG4, not with non-delivery, which is
  AG3. The issuer recomputes holding the records and keys; the digest lets it check them.

No experiment was run for these changes.

Change log, 2026-11-04 (founder ruling 2, `results/LABEL_ADJUDICATION_2026-11-04.md` addendum;
rulebook v1.5): a tiered burden of proof for merchant-performance claims (ABS-V1; normative in A5.7,
applied in A4.1 Step 1): a low-value non-delivery or non-conformity claim that no record with
independent authority decides is the merchant's to refund, within a per-buyer cap; above the
threshold or the cap it goes to review or an independent inspection, as before. The threshold and
cap are published programme parameters (defaults EUR 100 and 3 per 12 months, a design proposal);
the residual risk is bounded by threshold times cap per buyer identity (A5.7, A8.3). ABS-V1 added to
the supporting codes (A3.1), the precedence (A4.1) and A4.5; Decision `confirmation_route` value
`low_value_burden`; open question 22 (A15.1). Design, not evaluated: no model has been run under it.

Change log, 2026-11-04 (confirmatory amendment C1, `results/CONFIRMATORY_C1.md`; not the C1 mandate
condition of the experiment): the first frozen, held-out test of a gate result is cited in A5.7, A8.7 and
A15.2, and A4.5 notes why a mandate-term reader matters. No normative text changed.

Change log, 2026-11-04 (confirmatory amendment C2, `results/CONFIRMATORY_C2.md`; not the C2 control
condition of the experiment): the replication of the frozen gate test is cited beside C1 in A5.7, A7.9,
A8.7 and A15.2. No normative text changed.

## What ABS is

ABS is the **dispute, evidence and liability profile for agentic commerce**. It is layered on what
already exists and does not compete with it:

- mandates and signed checkouts: Google's Agent Payments Protocol (AP2, v0.2, now contributed to
  the FIDO Alliance) and Mastercard Verifiable Intent;
- catalogues and checkout: Google's Universal Commerce Protocol (UCP) and the OpenAI and Stripe
  Agentic Commerce Protocol (ACP) product feeds;
- agent identity: Visa Trusted Agent Protocol, Mastercard Agent Pay registration, IETF Web Bot
  Auth on HTTP Message Signatures;
- merchant risk: acquirer underwriting, payout holds and reserves, scheme monitoring programmes,
  marketplace trader checks;
- settlement: the card dispute lifecycle and ISO 20022 account-to-account messages.

ABS adds the parts those leave open. AP2's specification says dispute use of its evidence is
outside its scope; the card networks have no agent-specific dispute condition; American Express has
announced agent-error protection for US credit cards and registered agents that already draws the
line between a purchase that deviates from the authenticated intent and subjective intent such as
"best" (announced, terms pending); EMVCo's agentic framework covers intent over time such as
cumulative budgets. ABS does not claim the concept of "authorised but wrong". It supplies the
open, rail-neutral decision procedure, evidence standard and taxonomy that make that line
enforceable across issuers, acquirers and rails.

**The gap, stated narrowly.** Existing card dispute categories already carry most of what can go
wrong in an agent purchase: goods not received, goods not as described, an incorrect amount, and fraud
where nobody authorised the payment. A3.1 keeps those claims (AG3, AG4, AG4-D, AG1-M) on those
categories, and A6.3 routes them through the existing lifecycle. What the categories do not ask is
whether the agent faithfully executed the purchasing intent the user delegated to it. In an
**instruction dispute** the payment was authorised under a mandate, the merchant delivered what it
offered, and the agent still bought the wrong thing because it broke a term the user confirmed
(AG1-P); in a **capture dispute** the agent never recorded a requirement the user stated (AG1-C).
That is "authorised but wrong" on the agent's side, and AG2 is its counterpart on the user's side.
Visa's published dispute conditions have no condition for it and none is public from Mastercard
(A10.1); the scheme allocation puts in-mandate agent actions on the cardholder (A4.2); and the
evidence that decides it, the user's instruction and the agent's record, sits with the agent
provider. ABS contributes:

1. a **dispute taxonomy** for agent purchases that leaves merchant-performance claims on the
   reason-code categories issuers and merchants already use and adds codes only for instruction and
   capture disputes and their buyer-side counterpart;
2. a **liability decision order** in which the precision of the mandate decides;
3. a **minimum evidence standard**: the Evidence Package an agent purchase must carry, how it is
   signed, who holds it, what the evidence levels E0 to E3 are, and the provenance of every item:
   who issued it, what stake the issuer has, when it was committed, who has held it, and which facts
   it has authority for. A finding that moves liability needs a supporting record with authority
   for the fact it asserts, committed before the dispute by an issuer without a stake or binding on
   the party it is used against; one party's own later photos or text never suffice, and a signature
   proves who issued a record, not that it is true. This is a design choice informed by a small
   experiment, not a proven guarantee: in Phase 3 a registry record and a carrier weight resisted an optimising attacker on
   two case-sides against one arbiter, and the other arbiter was fooled on the same case-sides with
   the same records in its Package (A5.7);
4. **Decision Center governance**: LLM fact-finders, deterministic rules, signed receipts, human
   review on request, designed against the EU AI Act, the GDPR and ADR law, and neutrality; the
   federated network of nodes (A7.5) is proposed, not built;
5. a **settlement mapping** of decisions onto existing card and ISO 20022 flows;
6. the **layering** onto AP2/FIDO, UCP/ACP and TAP/Agent Pay, with an injection-safety profile for
   catalogues; every binding to those protocols is proposed, none implemented or tested (A5.2);
7. the two semantics the core needs from the annex: the **conformity-critical attributes** of an
   offer (binding, with tolerance and verification method) and the **Allowance** semantics that
   make "an explicit term" and "a required approval" provable;
8. a normative list of **known failure modes** of exact-by-construction decisions and their
   mitigations, including the capture duty that puts the mandate-precision burden on the system;
9. **agent conformance at scale**: enforcement at choke points no agent can bypass, Know Your
   Agent, the ABS Agent Profile, an open conformance kit, a reference MCP toolkit, and monitoring.

The founder's principles, kept throughout: reuse existing dispute flows rather than invent new
ones; participating merchants accept the rules up front and buyers know them before buying;
rail-agnostic, with payment channels as technical settlement only; machine-readable offers so
agents compare and buy safely; liability follows conformity to the offer and the precision of the
mandate. Terminology shared with the experiment in this repository: conditions C0 to C3, evidence
levels E0 to E3, reason codes AG1 to AG5, arbiter designs A1 and A2, trust conditions T0 to T2, the
allowance condition AL, hypotheses H1 to H7 (`results/PREREGISTRATION.md`, Amendments 1 to 5, is
canonical).

## Design principles

The principles below are adapted from the author's unpublished product vision ("the vision"; section 3,
"Principles (in priority order; they resolve every design conflict)"); where a sentence is the
vision's own it is quoted. They resolve every design conflict in this document in this order.

- **P1. Exact by construction, not interpretation.** Decisions are computed by deterministic,
  versioned rules from signed, structured inputs: the mandate terms, the signed Offer
  Specification, the delivery records. AI only extracts and checks facts, each cited to signed
  evidence, and never decides by free interpretation. Ambiguity escalates; it is never guessed.
- **P2. Honest by construction.** From the vision: "No fabricated numbers, no undrawable charts, no
  silent degradation. Enforced by validators, gates and tests, not prompts. Provenance is
  preserved through every transformation." In ABS: schema validation with no unknown fields, hash
  chains, countersigned snapshots, a transparency log, and conformance tests; never a prompt that
  asks a model to be careful.
- **P3. Recomputable by anyone.** Each receipt carries the input hashes, the rule version and the
  rules fired; any party, node or auditor can recompute the decision and get the same hash.
- **P4. Open format.** From the vision: the format is "public, versioned, signed and validated".
  The ABS schemas, rulebook versions and profiles are published with hashes; the rules are the
  same for every participant.
- **P5. Agents are users.** From the vision: "Agents are users." Every ABS surface that a person
  can use (compare, buy, dispute, read a receipt, verify a log entry) is available to software
  through the same signed objects.
- **P6. Truth over claims.** From the vision: "No capability is marketed as live unless code, tests
  and a production probe agree. Target-state language never leaks into runtime claims." In ABS:
  the simulation results are consistency measurements on an author-built catalogue, the experiment
  results are reported with intervals, Part B is labelled as roadmap, and nothing is claimed as
  working without evidence.

Every normative section of Part A obeys P1 to P3: the decision order (A4) is a deterministic
ruleset over typed Findings; every Finding cites signed evidence (A5, A7.4); every receipt is
recomputable from the canonical input hash and the rule version (A7.4, A7.5). Where a fact cannot
be read off a signed record and a judgement is unavoidable, A7.9 names it and states how it is
bounded.

---

# PART A. NORMATIVE CORE

## A1. Scope, goals, non-goals

### A1.1 Scope

ABS covers a purchase in which a software agent, acting under a mandate from a user, selects an
offer, places an order, pays through any rail, receives delivery and, if needed, disputes the
result. It applies to consumers and businesses.

Priority follows where a liability rule matters. For EU consumer physical goods, the 14-day
withdrawal right already resolves most "wrong item" cases by sending the goods back; there ABS
mainly decides who pays the return postage. The losses that need a rule are where that right does
not apply: travel, tickets and accommodation on a date, digital content once started, services,
custom goods, perishables, and every business purchase. v0.2 states the conformity and evidence
rules so they work for those categories (acceptance steps and delivery logs, not only parcels), and
the segment profiles in Part B give the per-segment detail.

ABS sits above the payment rail. Cards, account-to-account instant and batch transfers, wallets and
stablecoins are settlement plumbing. ABS tells the rail what to settle and, after a decision, what
to reverse. It does not change how a rail authorises, clears or settles.

### A1.2 Goals

1. One set of dispute rules, known to merchant and buyer before any purchase, accepted on
   participation the way a merchant accepts a card brand's or a wallet's rules.
2. The user's mandate and approval travel with the purchase, signed, so the evidence that decides
   a dispute is not locked inside one party; and liability moves only on a record with authority
   for the fact in question, committed before the dispute by an issuer without a stake or binding on
   the party it is used against (A5.7), never on a party's own later statements or photos alone.
3. The precision of the mandate decides liability. A merchant that did not deliver what it
   offered, or manipulated the agent, pays. An agent provider whose agent broke an explicit term
   pays. A user whose agent did exactly what was said, but not what was meant, bears it, with the
   withdrawal right intact.
4. Existing dispute flows are extended, not replaced: dispute, response, escalation, decision.
5. Decisions come from an AI-first Decision Center with deterministic rules, a signed receipt in
   plain words, a human review on request, and published error rates.
6. The same rules on a card rail and on an account-to-account rail.

### A1.3 Non-goals

- ABS is not a payment protocol, an agent protocol, a catalogue format or an identity scheme. It
  profiles and references those.
- ABS does not remove, limit or discourage chargebacks or rail recalls, and never asks a buyer to
  waive or assign them. ABS runs alongside them. Those rights come from scheme rules and, in some
  jurisdictions, consumer-credit law; for payee-initiated payments of unspecified amount the EU
  payment rules also give an eight-week refund right (A10.2). On push account-to-account rails, where
  no chargeback exists, ABS adds a contractual refund obligation and, where the merchant is paid
  through an acquiring PSP, a payout hold.
- ABS does not replace statutory consumer rights: withdrawal, conformity guarantees,
  unauthorised-payment refunds. A Decision never reduces them and never binds a consumer beyond
  what the law allows.
- ABS does not promise to keep every scammer out. It makes sure an unproven merchant is not paid
  before confirmed delivery, that a merchant that turns bad is caught within a bounded number of
  purchases, and that the buyer is made whole either way (Part B1).
- ABS does not hold funds. Payout holds, reserves and collections run through licensed PSPs and
  acquirers acting in their own licences. The arbiter is never a payer or a payee of any Settlement
  Instruction. An agent provider that initiates payments from the user's account needs
  payment-initiation authorisation or a licensed partner; one that holds user funds needs a payment
  or e-money licence. No programme guarantee is promised in Part A (B1.2).
- ABS does not set an operator's fee model.

### A1.4 Conventions

MUST, SHOULD and MAY have their usual standards meaning. "Buyer side" means the user and the agent
provider together. "Rulebook" means the current version of sections A3 to A7, identified by version
and hash. Money is a decimal string plus an ISO 4217 currency; floats are never used. Timestamps
are RFC 3339 in UTC. Hashes are SHA-256 over the RFC 8785 canonical JSON (JCS) of the object
hashed, written `sha256:<64 hex>`; a shorter prefix is never a commitment (A5.8). Signatures are
JWS (RFC 7515), compact serialisation, detached payload, over the authenticated envelope context
(A5.3); permitted algorithms in v0.3 are Ed25519 and ES256 (`EdDSA` accepted only to verify legacy
objects, RFC 9864). Schemas are JSON Schema 2020-12; the wire version is `abs_version: "0.3"`, and
the version policy is in A5.3.

### A1.5 Measures of success

All bands are working hypotheses for a pilot, each with the baseline it must beat. Audit 0 gives
the baselines with sources.

| KPI | Definition | Baseline to beat | Working band |
|---|---|---|---|
| Correct allocation | Share of tier 2 decisions whose liable party stands after appeal and sampling review | None exists for agent disputes | 97% or better; measured in the experiment as liable-party accuracy (H5, H6) |
| Time to decision | Median filing to Decision at E3 | Card disputes run weeks to months | Days at most; minutes for automated decisions |
| Human residual | Share of tier 2 cases needing a human Finding, plus human reviews requested | None | Measured and published |
| Review burden by liable party | Share of tier 2 cases sent to human review or independent inspection, by liable party as finally decided (merchant, agent provider, buyer) and by reason code; uncited reviews counted apart (A5.7) | None | Published per node; no party's honest claims should carry most of it. Phase 3b, with a gate that checked record types only, reviewed 12 of 21 merchant-liable, 10 of 10 agent-provider and 2 of 19 buyer-liable cases of the baseline Phase 2 workload (22 of 31 true claimants, 2 of 19 unfounded claims) |
| Rail-dispute rate (secondary) | Share of ABS disputes a party still takes to a chargeback or recall, after or instead of the ABS process | None | Reported, not targeted; the user keeps every rail right. In the Phase 2 simulation it fell from 14% and 41% at E0 to 4% at E3 for two arbiters (51 cases) |
| Scam payout rate (Part B1) | Share of non-delivery cases where the merchant was paid before delivery was confirmed | Marketplace holds (DD+7, up to 21 days) achieve near zero on held merchants | Zero on held merchants |
| Scam loss rate (Part B1) | Non-delivery by an unreachable or expelled merchant, by value | EEA card fraud 0.033% of value in 2024; remote 0.091% (EBA/ECB, Dec 2025, per Audit 0) | Must be shown below the remote-fraud baseline for the same value mix before any claim |
| Honest-merchant false reject (Part B1) | Merchants refused or suspended whose appeal succeeds or who are later qualified without new facts | None public | Below 2%; H7 allows at most 10% in simulation |

Reasons a party may still go to the rail after ABS: an arbiter error the party rejects; a merchant
that vanished where no payout hold was in place and collection failed; a contested decision; a
statutory or scheme right the user prefers; a rail deadline approaching before the ABS decision;
and AG0 cases, which belong to the rail by design. A deadline guard (A3.3) makes sure waiting for
an ABS Decision never costs the buyer a scheme deadline.

---

## A2. Roles and neutrality

| Role | Who | Holds | Signs |
|---|---|---|---|
| User | The person or business the purchase is for. | Intent, payment instrument, delivery address, the Allowance Policy. | Allowance Policy; Mandate; approvals; clarifications; conformity acknowledgement; dispute filing. |
| Buying agent | Software that searches, compares, orders and pays under the mandate. | Action log, snapshots. | Nothing on its own; it acts under the agent provider's key. |
| Agent provider | Operator of the buying agent. Liable for its agent's fault on the record (AG1-P). | Keys, the full trace, the intent text. | Participation Agreement; Offer Snapshot; Purchase Record; Settlement Instruction; filings by the agent. |
| Merchant | The seller. May act through a merchant agent under the merchant's key. Liable for conformity and for its own content. | Offer feed, fulfilment, packing records. | Participation Agreement; offers; order acceptance (countersigns the Offer Snapshot); Delivery Record (shipment part); dispute response. |
| Payment rail, PSP, issuer, acquirer | Networks, instant-payment schemes, wallets, banks, processors. Hold merchant underwriting, payout holds, reserves and the existing reversal tools. | Authorisation, clearing, settlement, reversals. | Rail result appended to the Settlement Instruction; `rail_enforcement` acknowledgement. |
| ABS arbiter (Decision Center) | The neutral body that decides tier 2 and enforces decisions against participants by contract. Never a payer or payee of funds. | Registry, rulebook versions, case files, receipts. | Participation Agreement (countersign); Decision; Decision Receipt. |
| Merchant Trust Authority (Part B1) | The function that qualifies and monitors merchants and issues Trust Attestations. | Track record, blocklist, KYB references. | Trust Attestation. |
| Certifier (optional) | Tests implementations against a conformance level. | Test results. | Conformance attestation. |

**Neutrality.** A party MAY hold more than one role, with a separate key per role. A party MUST
NOT act as arbiter in any case where it or an affiliate holds another role; in particular an agent
provider MUST NOT decide disputes in which its own agents can be liable. The Decision Center is
operated by an entity that is structurally independent of every agent provider and merchant in
the cases it decides, or delegated to one. Audit 0 (I3) found the earlier business model in
conflict with this rule; the rule stands and the model yields.

---

## A3. Dispute taxonomy and lifecycle

### A3.1 Reason codes

Card dispute categories already answer two questions: was the payment authorised (fraud and
authorisation), and did the merchant perform (not received, not as described, incorrect amount,
processing errors). An agent purchase leaves the second question as it is: the merchant still
delivers or fails to, describes the goods truly or not, charges the right amount or not. The first
is settled by the mandate and the scheme rules (AG0, A4.2). It adds a third question those
categories do not ask: did the agent execute the purchasing intent the user
delegated? The codes below therefore do two different things. Merchant-performance claims (AG3,
AG4, AG4-D, AG1-M) keep the category an issuer or merchant uses today, and the existing machinery
carries them (A6.3). Instruction and capture disputes (AG1-P, AG1-C), and their buyer-side
counterpart AG2, get codes of their own: the payment was authorised and the merchant performed, so
neither the fraud nor the merchant-performance categories fit, and no published scheme condition
addresses them (A10.1).

| Code | Name | Liable | Existing category it extends | Why a new code is needed |
|---|---|---|---|---|
| AG0 | No valid mandate | Rail process (issuer or payer PSP under law) | Unauthorised / fraud | Not new: routes the case out of ABS to the rail |
| AG3 | Non-conformity: not received, differs from the frozen offer, counterfeit, listing edited after purchase, over-charge against the snapshot | Merchant | Not received; not as described or defective; incorrect amount | Not a new kind of dispute: the code fixes the reference as the countersigned snapshot, not a later listing |
| AG4 | Injection via merchant content | Merchant | Not as described / misrepresentation (new sub-reason) | Today's categories have no notion of content that steered an agent |
| AG1-M | Merchant-added items or fees the agent did not choose | Merchant | Processing error (incorrect amount); not as described (added items) | The "agent did not select this line" fact comes from the cart's `added_by` |
| AG1-P | Instruction dispute, agent fault on the record: a term captured in the signed Mandate or Allowance broken, whether machine-readable or text the user confirmed (the instruction text shown at the confirmation tap, or a clarification answered with the user's authentication), or a guess where told to ask (A4.1 Step 3) | Agent provider | None: authorised, so no rail code | The gap: authorised, the merchant performed, and the purchase is provably outside the captured mandate |
| AG1-C | Capture dispute: a requirement the user stated to the agent only in the conversation, or in a clarification answered without authentication, that the agent should have captured into the Mandate and did not (rulebook v1.3; A4.1 Step 3b) | Agent provider | None | Puts the mandate-precision burden on the system; the conversation record committed by `conversation_hash` is the evidence |
| AG2 | Authorised but wrong, buyer side: fits every captured term, nothing the user stated went uncaptured, but not what the user meant and never said | Buyer | None (no dispute right) | Names the other half of "authorised but wrong" so it is not misfiled as fraud or not-as-described |
| AG5 | User error, change of mind, or a false claim | Buyer | None | Includes claims the evidence contradicts; carries a conduct finding |
| AG4-D | Deceptive offer content: a statement of fact in merchant content shown false (reference price never charged, false scarcity, invented urgency, endorsements) that the log shows influenced the choice | Merchant | Misrepresentation | Separates deception by false facts from injection by instructions |

**Supporting codes.** The simulation showed that a dispute system needs rules for standing,
authorisation, conduct and evidence that the six main codes do not carry. v0.2 adds them; the
counts are how often each decided one of the 528 catalogue scenarios under the v0.2 rules.

| Code | Meaning | Outcome | Decisions |
|---|---|---|---|
| ABS-C1 | Conduct: knowingly false or altered evidence | Decided against the submitter | 7 |
| ABS-E1 | Adverse inference: a required record keeper cannot produce its record (agent provider: Mandate and action log; merchant: Offer Snapshot and packing record) | The question that record would answer is decided against the keeper | 10 |
| ABS-H1 | Records conflict and no keeper is at fault | `review`: a fact-finder supplies the finding, with human review | 2 |
| ABS-S1 | Unsigned spec: the agent compared on an unconfirmed extracted spec (agent provider bears the mismatch) or the participant sold without a signed spec (its ambiguity construed against it) | Refund by the party at fault | with S2: 13 |
| ABS-S2 | Ambiguous Offer Snapshot construed against its author | Refund by the merchant | |
| ABS-P1 | Payment to a non-participant, or outside the mandate-bound credential | Agent provider bears the loss the rail does not recover | with P2: 22 |
| ABS-P2 | Forged Register entry passed a correct verification | The Register operator is liable to the buyer by contract and pursues recovery; the agent provider is not liable; no fund is promised (B1.2) | |
| ABS-F1 | Offer Feed signature did not verify (agent provider bears it) or was made with a leaked merchant key not yet revoked (merchant answers for its key) | Refund by the party at fault | 4 |
| ABS-X1 | Collusion: merchant and agent provider share an undisclosed arrangement | Jointly and severally liable; both suspended pending review | with X2: 12 |
| ABS-X2 | Undisclosed incentive steered the choice | Agent provider owes the difference against the best conforming offer it saw | |
| ABS-R1 | Apportionment across components decided under different steps | Each component to its own party | 4 |
| ABS-D1 | Default on merchant silence | Buyer's account of facts within its knowledge accepted | with D2, G1: 6 |
| ABS-V1 | Tiered burden of proof: a non-delivery or non-conformity claim that no record with independent authority decides (A5.7) | At or below the published order-value threshold and within the per-buyer cap, the merchant refunds; otherwise review or an independent inspection | added after the simulation; not run |
| ABS-D2 | Merchant-initiated claim (deposit, damage, non-return) | Decided on handover and return records, capped at the deposit or recorded damage | |
| ABS-G1 | Public-authority payee without a Participation Agreement | ABS decides the agent's conduct only; administrative appeal governs the payee | |
| ABS-T1 / T2 | Inadmissible: time limit; repeat dispute without new facts | No decision | 9 |
| ABS-M1 / M2 | No transaction: false refusal / true block, from the Refusal Record | Measured; no liability | with ABS-OK: 30 |

### A3.2 Lifecycle: the existing flow, extended

1. **Dispute.** The buyer, or the buyer's agent with the buyer's consent, files within 60 days of
   the later of the transaction and the latest promised delivery date: reason code, disputed lines
   and amount, remedy requested, evidence level offered. An agent must not file a claim it knows is
   false.
2. **Response.** Within 10 days the merchant answers with its evidence and one offer: full refund,
   return and refund, partial refund, replacement or deny. A merchant must not present an offer
   other than the frozen one. If no response arrives within 10 days, the facts stated by the buyer
   that lie within the buyer's own knowledge (non-receipt, what arrived) are taken as established
   and the case is decided on them (ABS-D1).
3. **Settlement (tier 1).** If the buyer accepts, the case closes with a Settlement Instruction on
   the payment's rail. A settlement obtained by a false claim or false evidence can be reopened.
   **The agent provider is a required party at tier 1 whenever the dispute alleges an agent error
   (AG1-P or AG1-C), and a settlement cannot allocate cost to a party that was absent.** The Phase 2
   tier-1 simulation found the gap: with only buyer and merchant at the table, merchants paid for
   agent faults in 6 settlements (4 of 51 under generic rules, 2 of 51 with the rulebook shown).
4. **Escalation (tier 2).** Either party may escalate to the Decision Center within 10 days of the
   response, or when none arrives.
5. **Decision.** The Center applies the decision order of A4 to the Evidence Package, records the
   conformity finding, reason code, liable party, remedy, confidence and rationale, states whether
   the withdrawal right is available, and issues the Settlement Instruction and the Decision
   Receipt. Any party may request a human review of any Decision within 10 days; a person who did
   not take part in the automated decision reviews it and may confirm, change or send the case to
   appeal (A7.3). The engine escalates on its own when a finding cannot be established (ABS-H1).
6. **Appeal.** The decision is final within the programme, save for one appeal within 10 days on
   new evidence not available to the appellant or on a procedural error. Disagreement alone is not
   a ground. Statutory routes remain.
7. **One case per record.** One Dispute Case per Purchase Record. A second case on the same record
   is admitted only on facts not available to the filing party at the first filing, or to reopen a
   settlement obtained by a false claim (ABS-T2).
8. **Merchant-initiated claims.** A merchant may open a Dispute Case against the buyer only for a
   deposit, damage or non-return recorded in handover and return records. The same decision order
   applies with the roles reversed; the remedy is capped at the deposit or the recorded damage
   (ABS-D2). Such a claim is outside the statutory consumer-ADR scope (Directive 2013/11/EU, Art
   2(2)(g)); against a consumer it is an offer the consumer may accept after the dispute arose, not a
   binding decision.
9. **Binding effect and statutory rights.** A Decision binds merchants and agent providers by
   contract. It does not bind a consumer beyond what the law allows: the consumer keeps the courts,
   statutory ADR, chargebacks, withdrawal and conformity rights. Time limits and decisions under
   ABS do not reduce the buyer's statutory rights; the Decision states which statutory route
   remains open, and where the EU withdrawal right applies and the buyer invokes it, the Settlement
   Instruction executes the withdrawal refund on the same rail.
10. **Alongside the rail, never instead.** A buyer who opens an ABS case keeps every rail dispute
    right; ABS never requires a waiver or an assignment. Card disputes are raised by the issuer at
    the cardholder's request; the Decision Center cannot raise one and only supplies the Decision
    and the Evidence Package as evidence. A Decision refund is set off against any later rail
    recovery so the buyer is made whole once. **Deadline guard:** before a scheme deadline runs (for
    example 120 days from the date the cardholder expected delivery for a card not-received
    dispute, with a 540-day ceiling from processing, per Visa's published rules), the Decision
    issues or the user is told to file with the issuer; ABS deadlines pause while a rail dispute
    runs.

Before any dispute, three records make the lifecycle decidable: every **refusal to buy** writes a
Refusal Record (offers compared, Mandate, stated reason), so false refusals of a conforming,
qualified, in-mandate offer are measured per agent provider without liability (ABS-M); the
**contract is formed** when the agent accepts the Offer Snapshot and the payment is authorised, so
a later cancellation by the merchant (stale stock) is non-delivery under Step 1 and a substitute
needs a new snapshot accepted inside the Mandate; and every checkout carries an **idempotency key**
derived from the Mandate id and the cart hash, so a duplicate capture against one key is the
merchant's (Step 1) and a duplicate order from an agent retry without a key is the agent
provider's (Step 3).

Conduct: evidence a party knew to be false or altered decides the case against that side (ABS-C1).
Agents on either side represent their principal and do not carry out an instruction to deceive.

### A3.3 Time limits (rulebook defaults)

| Step | Limit |
|---|---|
| Record conformity after delivery | 14 days from `delivered_at` (perishables and services: the profile's window or acceptance step) |
| File a dispute | 60 days from the later of settlement and the latest promised delivery |
| Merchant response | 10 days |
| Escalate | 10 days from the response or its deadline |
| Decision | 30 days from escalation |
| Human review on request | 10 days from the Decision; by a person who took no part in the automated decision |
| Appeal | 10 days from the Decision, once per party, on new evidence or a procedural error only |
| Scheme deadline guard | The Decision issues, or the user is told to file with the issuer, before the scheme's own dispute deadline; ABS clocks pause while a rail dispute runs |
| Pay a decided amount | 10 days from the Decision |
| Return goods under a refund-with-return or under withdrawal | 14 days from the Decision or the withdrawal notice |

---

## A4. Liability decision order

One rule, decided by how precise the mandate is. It builds on the Agentic Dispute Rulebook in this
repository: v1.2 is the ground truth of the main experiment and binds only machine-readable mandate
terms; v1.3, tested in a separate arm, adds the capture duty (AG1-C). This section goes one step
further than both: text the user confirmed in the signed Mandate also binds as an explicit term
(Step 3). That step is a design decision, not a measured result. Rulebook v1.5
(`rulebook/AGENTIC_DISPUTE_RULEBOOK_v1.5.md` and `.json`, mapped in `rulebook/VERSIONS.md`) is the
executable form of this section: v1.4, which implements the binding-term rule, plus the tiered
burden of proof (ABS-V1, Step 1 and A5.7). The historical v1.2 and v1.3 runs bound only
machine-readable terms, and no model has yet been run under v1.4 or v1.5 (Appendix E, F10).
The agent provider is liable only when the
record shows agent fault. Otherwise the buyer bears the outcome, with the statutory withdrawal
right intact. Precise mandates make agent errors provable; a vague mandate leaves the loss with the
person who wrote it.

### A4.1 The steps

The engine applies the groups in this order: **standing** (is there a case to decide), **Step 0
authorisation**, **conduct**, **Step 1 conformity**, **Step 2 manipulative offer**, **Step 3 agent
fault**, **Step 4 buyer side**. The first rule that fires decides the component it covers.

**Standing.** No Dispute Case, nothing to decide (ABS-OK). No transaction: the Refusal Record is
measured, no liability (ABS-M1 false refusal, ABS-M2 true block). Filed after the time limit, or a
second case on the same record without new facts: inadmissible (ABS-T1, ABS-T2). A payment to a
merchant without a current, signed entry in the Qualified Merchant Register, or made outside the
mandate-bound credential, is outside the Mandate: the agent provider bears the buyer's loss that
the rail's own process does not recover (ABS-P1). Where the agent correctly verified an entry later
shown to be forged, the Register operator is liable to the buyer under its Participation Agreement
and pursues recovery; the agent provider is not liable (ABS-P2). How the operator funds that
liability is a Part B question (B1.2); no guarantee fund is promised here. A public authority is a permitted payee without a Participation Agreement
when the agent verified it in the official registry; ABS decides only whether the agent stayed
inside the Mandate, and claims against the authority follow administrative appeal (ABS-G1).

**Step 0. Authorisation (AG0).** Before Step 1 the arbiter checks that (a) the Mandate was created
by the account holder with strong authentication performed by a PSP, and (b) the charge was
initiated by the buyer's agent under that Mandate, before its expiry, with the mandate-bound
credential. Whether the payment is **unauthorised in law** is not ABS's question: it is decided by
the payer's PSP under the payment rules (in the EU, PSD2 Arts 64 and 72 to 74: consent is given in
the form agreed between payer and PSP and may be given via the payee or a payment initiation
service) and under scheme rules (Visa's rules treat an agentic payment provider as the cardholder
for an agentic transaction). If (a) fails, ABS refers the case to the payer's PSP, supplies the
Mandate record and records the outcome; where the PSP did not require strong customer
authentication, the payer bears no loss unless the payer acted fraudulently (PSD2 Art 74(2)). If
the provider's systems issued the charge without a valid Mandate (compromise, or a Mandate accepted
without strong authentication), the agent provider is liable to the buyer under ABS. If (b) fails
because the merchant presented the credential again or charged after expiry, the merchant is
liable for that charge. "A Mandate without strong authentication is invalid" is a programme rule
between participants, not a statement of payment law.

**Conduct (ABS-C1).** Knowingly false or altered evidence decides the dispute against the party
that submitted it; a broken record chain counts against the party that kept it.

**Step 1. Conformity. A non-conforming delivery makes the merchant liable (AG3).** Compare what was
delivered with the frozen Offer Snapshot's conformity-critical attributes, each within its tolerance
by its verification method (A5.4), and with condition, quantity, package contents, identity images,
price and fees charged, and delivery within the stated terms. Weigh the delivery evidence (A5.6):
serial numbers against the registry and the packing record, photo metadata against the delivery
date, parcel weight against the item. Non-delivery and counterfeit goods do not conform. If the
delivery does not conform, the merchant is liable whatever the agent did. **Provenance gate.** A
finding about what arrived (unit identity, package contents, condition) MUST be corroborated by a
record with authority over that fact (A5.7): a record committed before the dispute by an issuer
without a stake, such as a serial-registry binding of the shipped unit to the order at dispatch, the
carrier's scanned weight compared with the expected weight of the complete package, or an
inspection by an inspector without a stake; or a record that binds the party it is used against,
such as the merchant's own packing record committed at dispatch, used against the merchant. The
buyer's photos and descriptions, the merchant's reply and either side's text are statements of a
party with a stake, mostly made after the dispute arose; they never decide alone, signed or not.
The record must also say what the finding says: a record of the right kind that is silent on the
contested attribute, or contradicts the finding, does not corroborate it (A5.7, content check).
Where no qualifying record is offered, the engine returns `review` or requests an independent
inspection; it never finds the fact automatically. Phase 3 showed why, and also the limit of what it
showed: an optimising dishonest party editing only its own submissions fooled the end-to-end
arbiters on 12 and 14 of 14 case-sides at E3; claude-fable-5-1 resisted on the two case-sides where
a registry record or a carrier weight gap contradicted the attacker, and grok-4.7 was fooled on
those two as well, with the same records in its Package (A8.7). **Tiered burden of proof (ABS-V1,
A5.7).** For a non-delivery or non-conformity claim that no record with independent authority
decides, the fact stays unfound and the order value allocates the loss: at or below the published
threshold, with the buyer under the per-buyer cap, the merchant that answered only with records it
wrote itself refunds (AG3); above either, the case goes to review or an independent inspection as
above. ABS-V1 never overrides Step 0 and never applies to an agent-instruction or capture dispute. Free text and non-binding attributes
do not ground an ABS Step 1 finding; they may still ground a statutory conformity claim, because
consumer sale-of-goods law makes the description and public statements part of what the buyer may
expect (Directive (EU) 2019/771, Arts 6(a) and 7(1)(d)).

Remedies are proportional: refund of the non-conforming lines; where the conforming part has no
stand-alone use for the buyer (a bundle), full refund with return at the merchant's cost; for late
delivery of conforming goods the buyer may reject within 14 days of the late delivery (full refund,
return at the merchant's cost) or keep the goods and recover the delivery charge; for a
non-conformity of documents (invoice, e-invoice, VAT treatment) the remedy is a corrected document
(cure), not a refund.

Rules that decide conformity when the records are thin: the structured attributes bind only when
signed by the merchant; an agent that compared on an unconfirmed extracted spec bears the mismatch,
and a participant that sold without a signed spec has every ambiguity in its free text construed
against it (ABS-S1). Where the Offer Snapshot can reasonably be read two ways and the delivery fits
only one, the reading favourable to the buyer applies, because the merchant wrote the offer; the
merchant avoids this by stating the attribute with its unit, region and tolerance (ABS-S2). A
merchant that cannot produce the packing record it was required to keep has the conformity question
decided against it (ABS-E1m). A not-as-described claim with no content evidence from the buyer,
against a packing record and serials consistent with the snapshot and a carrier proof of handover,
fails under Step 4 (ABS-E2). Where the packing record and the photographed serial conflict and no
keeper is at fault, the engine returns `review` (ABS-H1).

**Step 2. Manipulative offer. The merchant is liable (AG4, AG4-D, AG1-M).** The delivery
conforms, but the purchase was caused by the merchant's own offer: the agent followed instructions
embedded in content the merchant controls or hosts, including a seller agent's statements (AG4); a
statement of fact in merchant content shown to be false (reference prices, stock, time limits,
endorsements) influenced the choice (AG4-D; remedy: the difference against the best conforming
offer the agent had seen, or the affected item); the merchant added or pre-selected items or fees
the agent did not choose (AG1-M); or the Offer Snapshot's price, delivery cost, mandatory fees,
currency conversion, import charges or negotiated terms are worse for the buyer than the Offer Feed
record or signed negotiation record the agent relied on when it chose the merchant (AG1-M
extended; remedy: refund of the difference; the record the agent compared on is kept in the hash
chain with the snapshot). Where the merchant and the agent provider have an undisclosed arrangement
under which the agent's choice benefits both, they are jointly and severally liable and both are
suspended from the Register pending review (ABS-X1). Offer Feed records are signed with the
merchant's registered key: an agent must not rely on a record whose signature does not verify, and
if it does the agent provider bears the mismatch; a merchant answers for records signed with its
key, including after a compromise, until it revokes the key in the Register (ABS-F1).

**Step 3. Agent fault on the record. The agent provider is liable (AG1-P).** The delivery
conforms and the offer was not manipulative, but the record shows the agent:

- broke an explicit term captured in the signed Mandate or the Allowance Policy, in either of the
  two forms below; or
- guessed where the mandate told it to ask.

**What binds as an explicit term (normative).** A requirement binds as an explicit term only if it
is captured in the signed Mandate, or in the Allowance Policy it runs under, in one of two forms:

1. **Machine-readable**: a hard limit or other Mandate field (amount, category, merchant rule,
   units, expiry, delivery country, a required approval or notification, a qualified merchant,
   `ask_on_ambiguity`, and the rest of the list below), or a captured item requirement
   (`item_requirements[]`: model, variant, capacity, size, colour, region or plug type, condition,
   package contents).
2. **Signed text the user confirmed**: the instruction text whose hash is the Mandate's
   `intent_hash` and that was shown verbatim at the confirmation tap (inside
   `user_confirmation.shown_terms_hash`), or a clarification the user answered with an
   authentication reference (`clarifications[].user_auth_reference` in the Purchase Record), which
   amends the Mandate. "New, not refurbished", "in white", "only at a genuine discount" and "if
   unsure, ask me first" bind in this form when they appear in that text.

Breaking a term in either form is AG1-P. The forms differ in enforcement, not in liability: only a
machine-readable term can be a **hard limit** or an item requirement checked deterministically
before payment and declined, never escalated (C1, A12.1); a text term, like a behavioural term such
as `ask_on_ambiguity`, is checked after the fact by a Finding that cites the record (`intent_match`,
A7.3). Text the user said only in the conversation, or in a
clarification answered without authentication, is not a term. If it stated a requirement about the
purchase (what to buy, from whom, at what price, by when, in what condition) that the agent should
have captured, the failure is AG1-C (Step 3b); a preference the user left open ("ideally black,
any colour is fine") is not such a requirement. Intent the user never stated is the user's (AG2,
Step 4).

The full list of fields that are hard limits when set: amount, category, merchant rule, units,
expiry; required attributes (colour, size, model, dates, reference, deadline); a scope flag ("only the item named", on by default); the pay-in
currency and an FX tolerance; the delivery address; whether a step-up is required and the exact
content an approval prompt must show (item and amount); the autonomy level per category;
per-transaction and periodic budgets, including split purchases that evade a per-transaction
limit; delegate roles and limits; invoice data (PO number, VAT ID, e-invoice format) and payment
terms for business buyers; procurement thresholds and framework allowlists for public buyers; the
minimum merchant Trust Attestation level; for recurring purchases the period and maximum number of
charges; and a policy version, with changes taking effect when the agent acknowledges them.

Remedies: refund of the out-of-mandate amount, or the whole purchase with return where the item is
not what was mandated; for invoice data not passed, a corrected document (cure); for a payment-terms
breach without a refundable loss, a finding recorded on the scoreboard and no refund. An agent
provider that steered the choice for an undisclosed incentive owes the difference against the best
conforming offer it saw (ABS-X2); incentives from merchants are disclosed in the Mandate. If the
agent provider cannot produce the Mandate and the action log, Step 3 is resolved against it
(ABS-E1). Where an Allowance limit was also encoded in the mandate-bound credential and the
payment-side control failed to decline, the agent provider remains liable to the buyer and has
recourse against the enforcement layer under the credential agreement; the buyer is never left to
pursue the enforcement layer (ABS-9).

**Step 3b. Capture failure. The agent provider is liable (AG1-C).** The purchase fits
every term that was captured in the Mandate, but the record of the conversation that produced the
Mandate, or a later clarification answered without authentication, shows that the user stated an
explicit requirement ("the black one", "must work in the EU", "only if it arrives by Friday") and
the agent failed to capture it into the Mandate's terms or item requirements. The precision burden
falls on the system that writes the mandate, not on the user who confirms it. In the Phase 2
capture-duty arm (rulebook v1.3, 12 triplet cases with the conversation in evidence) both arbiters
allocated the three branches correctly in 48 of 48 decisions: captured and breached, AG1-P; said in
chat and not captured, AG1-C; never said, AG2. The agent provider keeps the conversation record
(`conversation_hash` in the Mandate; the transcript is disclosed in a case at E2) and bears the loss
when it cannot produce it (ABS-E1). What the user said but did not state as a requirement, and what
the user meant without saying, is not a capture failure; it is Step 4.

**Step 4. Buyer side (AG2, AG5).** The delivery conforms, the offer was not manipulative, the
agent followed every explicit term, and no stated requirement went uncaptured. No fault remedy. AG2 when the purchase fits the explicit
mandate but not what the buyer meant and did not say; AG5 for user error, change of mind or a false
claim. The withdrawal right applies on top (A4.4): remedy `withdrawal` when available and
unexpired, otherwise `deny`.

**Apportionment (ABS-R1).** Where more than one step is satisfied for different components of the
same purchase (for example late delivery by the merchant and an extra unit bought by the agent),
the arbiter decides each component under its own step and apportions the remedy. The order of
steps resolves which party answers for the same component, not whether a second party answers for
a different one.

Precedence for the same component: standing, AG0, ABS-C1, AG3 (with S1, S2, E1m, E2, H1, D1, V1),
AG4, AG4-D, AG1-M, ABS-X1, ABS-F1, AG1-P (with X2, E1), AG1-C, AG2, AG5.

**Mandate precision, and who carries the burden.** A requirement binds as an explicit term only if
it is captured in the signed Mandate, as a machine-readable term or as text the user confirmed
(Step 3). "I wanted the black one" thought but never said is AG2; "colour: black" in
`item_requirements`, or "the black one" in the confirmed instruction text, makes a silver delivery
AG1-P; "the black one" said to the agent in the conversation and not captured is AG1-C (capture
failure, Step 3b). The user is not asked to
write a contract. The agent proposes the Mandate from the conversation, using the category
template's conformity-critical attributes (A5.4) as prompts for what it must ask or infer, shows
the captured terms in plain words, and the user confirms with one strong-authentication tap. The
mandate interface MUST prompt for the profile's required attributes and MUST show which
requirements were captured and which were left open. Precise mandates make agent errors provable;
they also make most of them preventable, because the provider's own enforcement can check a
captured requirement against the offer's signed attributes before paying. Consumer law may limit
how far unstated intent can be placed on a consumer by standard terms; A8.4 gives the jurisdiction
profiles and the mitigations (capture duty, withdrawal right, plain-language disclosure). 

### A4.2 Why this order, and how it sits against scheme rules

Each loss lands on the party best placed to prevent it. The merchant controls what it delivers and
what it writes. The agent provider controls whether its agent keeps to explicit terms, which is
deterministic for hard limits and provable from the record for instructions. The user controls how
precisely the intent is stated.

The Visa Product and Service Rules (edition 24 Oct 2026; rule added Apr 2026), section 4.1.23.10
"Agentic Payment Provider – Cardholder Responsibility" (ID# 0031176), make the cardholder
"responsible for any actions taken by an Agentic Payment Provider as part of an Agentic
Transaction as if the Cardholder initiated the Transaction"; the glossary treats an agentic
payment provider as the cardholder for an agentic transaction. American Express's agentic-commerce
page states that, in the future, for a registered AI agent on US credit cards, it "will protect
eligible customers from charges related to AI agent error", where eligible errors include
"transactions where the purchase deviates from the Card Member-authenticated purchase intent" and
subjective intent such as "best" is excluded; full terms are pending. Both were verified on the
primary texts by Audit 2 (sources in `LANDSCAPE.md`). ABS Step 4 agrees with the Visa allocation
for in-mandate actions, and the Amex line between deviation from authenticated intent and
subjective intent is the same line as Step 3 against Step 4. ABS Step 3 is a
contract between agent provider and user **over** the scheme rule, not instead of it: the scheme
still treats the transaction as the cardholder's; the provider refunds the user under the
Participation Agreement. The Amex approach puts agent error on the issuer; ABS lets an issuer or
wallet that wants to offer such protection use the same decision order and evidence to decide when
it applies. A provider may cap Step 3 exposure per purchase and insure it; the cap is disclosed in
the Participation Agreement and shown to the user (A5.9). Audit 0 noted that current consumer
terms of major providers place all actions on the user; Step 3 asks them to accept liability only
for provable fault, which their own deterministic enforcement makes rare and cheap.

Audit 0 recommends sharing AG4 with the agent provider, because the party that can prevent
injection is the one that does not obey instructions found in data. v0.2 keeps the rulebook's
allocation and closes the sabotage vector another way: the merchant answers for fields it wrote
and for hosted content after notice; an agent that obeyed instructions in data breached A5.7 and
its provider's conformance record shows it. The split is an open question (A15.1).

**Measured completeness.** The rule-completeness simulation (`standard/sim/REPORT.md`) ran the
rules as written in v0.1 and the v0.2 rules above against 528 catalogue scenarios (192 event
types; 498 live disputes). v0.1 as written reached a determinate outcome in 498, had no rule for 30
and was consistent with the stipulated ground truth in 340 of 528, with 8 gap types, 4 unresolved
conflicts and 58 contradiction groups; v0.2 covers all 528, 526 determinate and 2 escalated to
human review, consistent with the stipulated ground truth in 528 of 528, with none. The findings are
stipulated, so this is consistency against stipulated facts, not evidence sufficiency. The ground
truth and the v0.2 wording were written in the same exercise, so the result shows that the rules
are complete and consistent against that catalogue's judgments, not that the judgments are right in
law; the catalogue entries marked `general_law`, `uncertain`, `debatable` or `design_proposal` are
the ones to challenge.

**Measured against arbiters.** The pre-registered Phase 2 run (51 Dispute Cases with known ground
truth, two frontier arbiters, simulated environment, small n) supports the evidence design: with
card-dispute data alone (E0) the arbiters allocated liability correctly in 82% (claude-fable-5-1)
and 61% (grok-4.7) of cases; with the full Package (E3) in 98% and 96% (exact McNemar p from 0.008
to 1e-7; H2 and H5 supported). Those labels are the historical rulebook v1.2, not this section's
rule: scored against the v1.4 labels (six cases relabelled), the same stored E3 decisions are right
on liable party in 45 of 51 and 44 of 51, a distance between the benchmark and the current rule,
not arbiter error (post-audit, exploratory; `results/AUDIT1_CORRECTIONS_PHASE1_2.md`). Without the
mandate, arbiters defaulted to "the buyer bears it" in 13 of 20 agent-breach decisions at E0;
without the trace and snapshots they saw no injection (AG4 0 of 5 at E0 and E1, 5 of 5 at E3).
Being fooled by scripted adversarial parties fell from 20% to 5% but not significantly at n = 20
(H3). Decisions were identical when the rail was flipped (12 of 12).

### A4.3 Without prejudice to statutory conformity; deviations accepted in advance

Conformity to the offer in Step 1 is conformity to the subjective, contractual requirements. EU
sale-of-goods law adds objective requirements (fitness for normal purpose, normal quality and
durability) and a multi-year liability period with a presumption that a defect shown in the first
year existed at delivery (Directive (EU) 2019/771, Articles 6, 7, 10, 11 and 21 as cited by Audit
0). A Step 1 finding of "conforms" settles the ABS dispute; it never settles a statutory conformity
claim. Every Decision says so.

Under the same directive, a deviation from objective conformity (refurbished, used, lower battery
health) binds a consumer only if the consumer "was specifically informed that a particular
characteristic of the goods was deviating" and "expressly and separately accepted that deviation
when concluding the sales contract" (Art 7(5)). A standing advance acceptance in a Mandate does
not meet "when concluding the sales contract" and is treated as ineffective in the EU. ABS
therefore captures deviation acceptance **per purchase, at the approval step**: the approval
prompt shows the specific deviation of the offer actually bought, and the Approval Record stores
the deviation text hash with the user's authentication reference (`deviation_acceptance`, A5.5).
Whether an agent may give that acceptance for a consumer remains open (A15.1). The directive also
lets Member States keep longer liability and presumption periods (Arts 10(3), 11(2)) and puts
repair or replacement first (Art 13); ABS remedies are a contractual add-on, never a substitute.
Digital content and digital services fall under Directive (EU) 2019/770, not the Sale of Goods
Directive; goods with digital elements stay under the latter.

### A4.4 Statutory withdrawal right (overlay)

Consumer law applies whatever the dispute decides. For goods sold at a distance to an EU consumer,
the buyer may withdraw within 14 days from the day the consumer acquires physical possession of the
goods, without giving a reason (Directive 2011/83/EU, Art 9(2)(b)); the consumer bears the direct
cost of return unless the trader agreed to bear it or failed to inform the consumer of it (Art
14(1)); the trader refunds within 14 days using the same means of payment (Art 13(1)) and may
withhold the refund until it has received the goods back or the consumer has supplied evidence of
having sent them back, whichever is earlier (Art 13(3)). From 19 June 2026 the trader must also
offer a **withdrawal function** on its interface (Art 11a, inserted by Directive (EU) 2023/2673);
participating merchants expose it, and the ABS `withdrawal` remedy is routed through it. The right
does not apply, among other cases, to goods made to the consumer's specification or clearly
personalised (Art 16(c)); sealed goods not suitable for return for health protection or hygiene
reasons that were unsealed after delivery (Art 16(e)); sealed audio, video or software unsealed
after delivery (Art 16(i)); accommodation, transport of goods, car rental, catering or leisure
services for a specific date or period (Art 16(l)); and digital content not on a tangible medium
once performance has begun, only where the consumer gave prior express consent, acknowledged the
loss of the right and the trader provided the confirmation the directive requires (Art 16(m)).
Passenger transport is outside the directive altogether (Art 3(3)(k)), not an exception. Business
purchases have no withdrawal right. Articles verified by Audit 2. Every Decision states whether the right is available; for AG2 and AG5 the
remedy is `withdrawal` when it is and `deny` when it is not. For AG3, AG4, AG4-D, AG1-M, AG1-P and
AG1-C the remedy is a refund by the liable party and the right is moot.

### A4.5 Who confirms the deciding fact (normative)

The decision order says who is liable once the facts are established. This section says who may
establish the fact that decides an agent dispute. No party confirms a fact in its own favour, except
the agent provider's action log for causation in Step 2 under A5.7 test (c) (item 5), and no
decision rests on a party's narrative (A5.7, A8.7). The full confirmation matrix and the
reasoning behind it are in `standard/ADOPTION_AND_CONFIRMATION.md`.

1. **Recomputed (`confirmation_route: recomputed`).** These facts are established by comparing
   the user-signed Mandate, the merchant-signed cart or countersigned Offer Snapshot, the compared
   record and the rail's authorisation record under the published ruleset:
   - a breach of a machine-readable term (A4.1 Step 3, form 1);
   - a line or fee the merchant added;
   - a snapshot worse than the record the agent compared on (Step 2, AG1-M).

   No judgement Finding is used. Any verifier holding the records and the registered keys MAY run
   the comparison, including the payer's issuer or PSP at dispute intake. A conforming Decision
   Center MUST reach the same result. Where the Mandate and the cart state an attribute in
   vocabularies no published dictionary maps onto each other, the comparison returns `review`.
2. **Read from a committed record (`committed_record_read`).** These facts are established only
   from records committed before the dispute:
   - a breach of a signed text term (Step 3, form 2);
   - a capture failure (Step 3b), including whether a case is AG1-C or AG2;
   - an injected instruction and the agent following it (Step 2, AG4);
   - a false statement of fact in merchant content and its influence on the choice (Step 2, AG4-D).

   The records are the text matching `intent_hash` inside `shown_terms_hash`, clarifications with
   `user_auth_reference`, the conversation record matching `conversation_hash`, the
   merchant-signed snapshot and the anchored action log. The reading is a typed Finding with
   structured citations and a content check (A5.7). It is made by a Decision Center with no stake
   in the case (A2), and any party may request a human review (A7.3).
3. **Adverse inference (`adverse_inference`).** A required record keeper that cannot produce its
   record has the question that record would answer decided against it (ABS-E1, ABS-E1m). Where
   the missing record is the conversation record, the case is AG1-C.
4. **Rail process (`rail_process`).** Two questions belong to the payer's PSP and the scheme, and
   ABS only supplies records for them: whether a payment was authorised in law (AG0), and any card
   dispute the cardholder asks the issuer to raise (A3.2 item 10).
5. **Who never confirms alone.** The agent provider never establishes the absence of its own
   fault on its own word: it produces the records for recomputation or reading. One exception is
   A5.7 test (c): its anchored action log MAY establish causation in Step 2, that its agent
   followed injected text or relied on a false claim in content the merchant signed, which moves
   the loss to the merchant (AG4, AG4-D). The exception is limited: the log counts only for
   `agent_actions`, only when no record meeting test (a) or (b) contradicts it, and never for what
   the user asked or what arrived; the content itself must come from the merchant-signed record
   (test (b), against the merchant). The same holds for the
   merchant on conformity and for the buyer on what arrived. A party's statement made after the
   dispute arose is never a citation. An end-to-end judge's reading of party submissions never
   confirms a fact on its own (A7.3 item 3a).

| Dispute | Deciding fact | Record committed before the dispute | Confirmed by | Record missing |
|---|---|---|---|---|
| AG1-P, machine-readable term | A captured term is outside what was bought | User-signed Mandate; merchant-signed cart or snapshot; authorisation | Recomputation by any verifier holding the records and keys; the issuer at intake, with the digest (B6) to check that the records it obtains are the committed ones | Against the agent provider (ABS-E1) |
| AG1-P, signed text term | The purchase contradicts text the user confirmed | Text matching `intent_hash`; authenticated clarifications; cart | Decision Center reading, typed and cited; human review on request | Against the agent provider (ABS-E1) |
| AG1-C | A requirement stated in the conversation and not captured | Conversation record matching `conversation_hash`; `template_profile` | Decision Center reading; human review on request | Against the agent provider: AG1-C |
| AG2 | No term broken, and nothing stated was left uncaptured | All of the above | Recomputation plus the AG1-C reading | AG2 cannot be shown: AG1-C |
| AG1-M, AG4, AG4-D | A line or worse terms added by the merchant; an injected instruction followed; a false statement of fact in merchant content that influenced the choice | Merchant-signed cart, compared record and snapshot; for AG4-D the reference price or stock record; anchored action log | Recomputation for lines and prices; Decision Center for injection and deceptive content, with causation from the log (A5.7 test (c)) | Snapshot: against the merchant (ABS-E1m). Log: no causation, so Step 3 applies |
| AG3 | What arrived, including non-delivery; handover | Carrier, registry or inspection records; the packing record, used against the merchant | The rail process, or the Decision Center behind the A5.7 gate | ABS-E1m; no handover proof means not received; no independent record either way: at or below the threshold and within the cap the merchant refunds, otherwise review (ABS-V1) |

**No fact confirmed (`low_value_burden`).** A low-value non-delivery or non-conformity claim that
no record with independent authority decides is not confirmed by anyone: the tiered burden of proof
allocates it (ABS-V1, A5.7), and the merchant's own records never confirm a fact in its favour.

The Decision records the route in `confirmation_route`. The payer's PSP already holds the anchored
chain head (A5.8), which commits the Mandate. The PROPOSED `abs_binding.mandate_digest` (A6.2)
names the Mandate directly, so an issuer can find and verify it without the chain. Confirmation is
not recovery: an issuer that confirms AG1-P cannot charge it back to a merchant that performed. The
loss reaches the agent provider through the Participation Agreement (A6.4) until a scheme defines
a liability flow for it (B6, Stage 3).

**Why a mandate-term reader matters (measured once; the route is design, not evaluated).** In the
confirmatory gate test (amendment C1, `results/CONFIRMATORY_C1.md`) gate v3 sent all 8 AG2 and 7 of 10
AG1-P baseline cases to review, because its readers cover delivery records and hard mandate limits and
nothing else in the mandate, page text or the action log. Recomputation (item 1) is that missing reader
for machine-readable terms; whether it lets such cases be decided without admitting attacks is untested.

---

## A5. Minimum evidence standard: the Evidence Package

### A5.1 What every agent purchase must carry

An ABS purchase produces an **Evidence Package**: the set of signed records that lets a dispute be
decided from evidence instead of statements. Its parts, who signs them and who holds them:

| Part | Content | Signed by | Held by | Level |
|---|---|---|---|---|
| Mandate digest | The Mandate (task instruction) and the Allowance Policy it runs under: hard limits, rules, captured item requirements, autonomy level required, `intent_hash`, authentication reference | User (strong authentication), agent provider | Agent provider; user; the intent text stays with the provider and is disclosed in a case | E1 |
| Approval record | For a purchase routed to notify-and-hold or approval: notification time, hold window, approver, authentication reference, the exact summary shown | Agent provider; user's authenticator reference | Agent provider | E1 |
| Offer Snapshot | The offer frozen at checkout: the merchant-signed offer, its conformity-critical attributes only (not the marketing text), price, fees, delivery and returns terms, image hashes; countersigned by the merchant at order acceptance | Agent provider; merchant | Agent provider; merchant | E3 (view-time snapshots also E3) |
| Agent trace digest | Hash-chain head over mandate, every action with its stated reason and result status, snapshots, cart with `added_by`, authorisation; the full action log stays with the provider | Agent provider | Agent provider; at payment the full head is committed to independently authenticated storage and a locator goes into the rail reference (A5.8) | E2 (log), E3 (chain) |
| Delivery evidence | Contestable records of what arrived (A5.6) | Merchant (shipment part), user or provider (receipt part), carrier where it signs | Merchant; agent provider; carrier | E3 |
| Compared record | The Offer Feed record or signed negotiation record the agent relied on when it chose the merchant, hashed into the chain with the snapshot | Merchant (feed); both agents (negotiation record) | Agent provider | E3 |
| Refusal Record | When the agent did not buy: offers compared, Mandate, stated reason | Agent provider | Agent provider | E2 |

Everything else (the Dispute Case, the Decision, the Finding and the Decision Receipt) is produced
during the dispute from the Package.

**What the Package makes decidable.** In the rule-completeness simulation (author-built catalogue,
not field data), card-dispute evidence alone (E0) gave a determinate outcome in 89 of 498 live
disputes (17.9%): time limits, non-delivery where the merchant has no carrier proof of handover, and
friendly-fraud non-receipt where it has. With the minimum package at E3, 496 of 498 were
determinate and 2 were escalated to a fact-finder with human review because the records
conflicted; 0 had no rule. The findings are stipulated, so this measures which level the rules need
given correct findings, not whether the evidence would establish them. E1 adds the
authorisation and the amount, category, merchant, units, expiry and currency breaches; E2 the
log-dependent breaches (step-up, required attributes, scope, approvals, budgets, roles), injection
the agent reports following, and undisclosed incentives; E3 content conformity, merchant-added
lines, feed-versus-snapshot mismatch, false claims, feed signature, Register entry and tampering,
and therefore every Step 4 denial of a not-as-described claim.

### A5.2 Profiles of existing objects, not competitors

Where an existing standard already defines the object, the ABS object profiles it: it refers to the
external object by hash (`external_object`, `offer_hash`), adds the ABS fields, and travels in its
own ABS envelope with the ABS hash and signature rules (A5.3), beside the external object and bound
to it by hash. It is not the same container. Carrying the ABS fields inside the external container,
for example as a claim of an AP2 mandate credential, is a proposed binding (A5.2.1).

**Status: every binding in this table is PROPOSED.** None has been implemented, round-tripped
through the external format, or tested against an AP2, SD-JWT VC, Verifiable Intent, UCP, ACP or
card-network implementation. The experiment used its own simplified records, not these external
formats; the conformance seed (A9.4) tests shopping behaviour, not these bindings.

| ABS record | Existing object it profiles | What the profile adds (proposed) |
|---|---|---|
| Mandate digest | AP2 v0.2 Checkout and Payment Mandates (SD-JWT VCs per the IETF `draft-ietf-oauth-sd-jwt-vc` format, over SD-JWT RFC 9901) and Mastercard Verifiable Intent, both in the FIDO Alliance Payments working group (28 Apr 2026); or a W3C Verifiable Credential (Data Model 2.0, Recommendation 15 May 2025) secured with VC-JOSE-COSE. Two formats, profiled separately | `intent_hash` over the instruction text the user confirmed; the Allowance Policy reference; the rule that the mandate plus the clarifications the user confirmed is "what the buyer asked for" (deviation acceptance is per purchase, in the Approval Record, A4.3) |
| Offer Snapshot | AP2's merchant-signed checkout JWT bound by hash to the Closed Checkout Mandate, and the merchant's Checkout Receipt; UCP and ACP checkout objects | The conformity-critical attribute set with tolerances; the countersignature at acceptance as "the listing"; the rule that a later edit has no evidential value; retention |
| Agent identity on requests | HTTP Message Signatures (RFC 9421); Visa Trusted Agent Protocol and Mastercard Agent Pay registration; IETF Web Bot Auth drafts | Nothing; ABS defers |
| Catalogue | UCP Catalog and ACP Product Feed | The injection-safety profile (A5.7) and the binding conformity attributes |
| Rail reference | Card merchant/additional data where a network allows it; ISO 20022 remittance information or end-to-end identification | A locator for the full chain-head commitment, never the commitment itself (A5.8) |

Where no existing object exists (Approval record, Delivery evidence, Dispute Case, Decision,
Finding, Decision Receipt), ABS defines one.

#### A5.2.1 Binding sketch: the ABS Mandate inside an AP2-style mandate credential (PROPOSAL)

**Status: proposal only.** Not implemented; no fixture exists; not tested against any AP2 or SD-JWT
VC implementation; the claim name is not registered and the placement has not been agreed with the
AP2 or FIDO profile owners. It shows the shape one binding would take, so that the profile claim of
A5.2 can be checked against something concrete.

1. **Order of creation.** The ABS Mandate envelope is created and signed first (A5.3: the user's
   and the agent provider's keys, `chain.seq` 0). The mandate credential, an SD-JWT VC per
   `draft-ietf-oauth-sd-jwt-vc`, is issued after it and commits to it. The binding runs one way,
   from the credential to the ABS object, so there is no hash cycle.
2. **The carrying field.** The issuer-signed JWT payload of the credential carries one claim,
   proposed name `abs_mandate`, as a plain claim: always disclosed, never one of the selectively
   disclosable claims, so a holder cannot withhold it while presenting the credential. Its value:

   ```json
   {"abs_mandate": {"abs_version": "0.3", "mandate_id": "urn:abs:mandate:7c1e2a40-5b6d-4e8f-9a0b-1c2d3e4f5a6b",
                     "envelope_hash": "sha256:56880ad031f0c35416fb418ea036a679ec726b96e7b2d9df2a568f84b2a219af",
                     "rulebook": {"version": "abs-liability@0.3", "hash": "sha256:b344cd48f567e47e7c62924f3ec682f97fcb134e21b33d3a0f0043e3e17137f8"}}}
   ```

   `envelope_hash` is the full `envelope_hash` of the ABS Mandate (A5.3), all 64 hex characters,
   never a prefix.
3. **Verification.** A verifier (merchant checkout, PSP or Decision Center): (a) verifies the
   credential as the SD-JWT VC specification requires: the issuer's signature over the
   issuer-signed JWT with the key resolved for that issuer and credential type, the digests of any
   Disclosures presented, and the key-binding JWT where holder binding is required; (b) reads
   `abs_mandate` from the verified payload and rejects it if it arrived in a Disclosure; (c) obtains
   the ABS Mandate envelope from the agent provider and verifies it under A5.3 (schema with
   dispatch, `body_hash`, `envelope_hash`, each signature over its context with the key registered
   for that party and role); (d) compares the recomputed `envelope_hash` with
   `abs_mandate.envelope_hash` in full, and `mandate_id` with the ABS body; (e) where the credential
   also carries an amount ceiling, payee scope or expiry, checks them against `max_total`, the
   merchant rules and `expires_at`, and fails the binding on any disagreement rather than choosing
   either value. A credential whose `abs_mandate` does not verify does not carry an ABS Mandate, and
   a purchase made under it is outside the Mandate (ABS-P1).
4. **Round trip.** The compact SD-JWT exactly as presented is kept in the Evidence Package with its
   SHA-256 (`evidence_refs[]`, type `other`, beside the ABS Mandate under type `mandate`), so a later
   verifier repeats step 3 from the stored bytes.
5. **What a real binding still needs.** An agreed claim name and placement; a fixture of one
   credential and one ABS Mandate that verify together; negative fixtures (a prefix-only hash, a
   mismatched expiry, `abs_mandate` moved into a Disclosure, a re-signed ABS body); and a test that
   serialising and re-reading both objects preserves every signature. UCP, ACP and Verifiable
   Intent bindings would need the same and have no sketch here.

### A5.3 Common envelope, authenticated context and version policy

Every ABS object is a JSON document in this envelope. Unknown fields in the envelope or inside
`body` MUST be rejected.

**One authenticated context (normative).** A signature never covers the body alone. The verifier
rebuilds the **signed context** from the envelope (`$defs/SignedContext`): the constant
`ctx: "ABS-ENVELOPE"`, `abs_version`, `type`, `id`, `created_at`, `chain_id` and `seq` (null outside
a chain), `prev_hash` (null at a chain's genesis and outside a chain) and `body_hash`, where
`body_hash = sha256(JCS(body))`. Then `envelope_hash = sha256(JCS(signed context))`. Each signature
is a JWS, compact serialisation with detached payload, whose payload is the JCS of
`{envelope_hash, role, party_id, kid, signed_at}` (`$defs/SignatureInput`) and whose protected
header carries the same `alg` and `kid`. A signature therefore covers the object's type, version,
identifier, timestamp, chain position and predecessor, its body, and the signer's role and signing
time; changing any of them invalidates every signature. The context is rebuilt, never transmitted,
so it cannot disagree with the envelope.

**Binding to the event chain (normative).** The chain of A5.8 is a chain of these envelopes and
nothing else. An event is an envelope that carries `chain`; its event hash is its `envelope_hash`;
its `prev_hash` is the `envelope_hash` of the event with the previous `seq` in the same chain. Agent
actions that are not themselves ABS objects are recorded as `ActionEvent` envelopes. A purchase
chain's `chain_id` is the `id` of its genesis Mandate envelope (`seq` 0, no `prev_hash`). Two events
with the same `chain_id` and `seq` are a fork, and a fork is a broken chain (A5.7).

**Verification (normative).** (1) Validate the envelope against this schema, which dispatches `body`
to the schema for `type`; (2) recompute `body_hash` and `envelope_hash`; (3) verify each signature
over its SignatureInput with the key registered for that `party_id`, `role` and `kid` and valid at
`signed_at` (A5.8); (4) for a chain event, check `seq` and `prev_hash` against the previous event;
(5) for an anchored chain, compare the full head with its independently authenticated commitment
(A5.8). Wherever an ABS field holds the hash of another ABS object (`mandate_hash`, `purchase_hash`,
`evidence_refs[].hash`, `cited_evidence[].hash`, `finding_hashes`), it is that object's
`envelope_hash`, unless the field's description says it hashes a body or an external artefact. A
signature proves which key signed which context; it says nothing about whether the body is true
(A5.7).

**Version policy (normative).** The wire version of this document is `abs_version: "0.3"` and
every schema `$id` is `urn:abs:schema:0.3:<name>`. v0.3 is not wire-compatible with v0.2: v0.2
signatures covered only the body hash, so a v0.2 object's type, id, timestamp and chain link are
unauthenticated; the v0.2 field `hash` became `body_hash` plus `envelope_hash`; the binary
`provenance_tier` became the `provenance` description (A5.7); the anchor became a full-length
commitment (A5.8); and several enums changed (Decision `evidence_integrity`, Finding
`corroborated`). A v0.3 verifier validates a v0.2 object against the v0.2 schemas
(`standard/ABS_v0.2.md`) and MAY admit it as evidence created before the participant accepted a
v0.3 rulebook (`accepted_at`, A6.4), treating its context as asserted by its producer, never as
authenticated, and ignoring its `provenance_tier`. It MUST reject `abs_version: "0.2"` on any object
created after that date. New objects MUST be 0.3. Part B objects share the version. Example
instances that must and must not validate are in Appendix F.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "urn:abs:schema:0.3:envelope",
  "type": "object",
  "required": ["abs_version", "type", "id", "created_at", "body", "body_hash", "envelope_hash", "signatures"],
  "additionalProperties": false,
  "properties": {
    "abs_version": {"const": "0.3", "description": "wire version; v0.2 objects are validated against the v0.2 schemas under the version policy (A5.3)"},
    "type": {"enum": ["ParticipationAgreement", "AllowancePolicy", "Mandate", "ApprovalRecord", "Offer", "OfferSnapshot", "PurchaseRecord", "ActionEvent",
                      "SettlementInstruction", "DeliveryRecord", "RefusalRecord", "DisputeCase", "Decision", "Finding", "DecisionReceipt", "TrustAttestation"]},
    "id": {"type": "string", "pattern": "^urn:abs:[a-z-]+:[0-9a-f-]{36}$"},
    "created_at": {"type": "string", "format": "date-time"},
    "chain": {"type": "object", "required": ["chain_id", "seq"], "additionalProperties": false,
              "properties": {"chain_id": {"type": "string", "description": "id of the chain's genesis envelope (for a purchase chain, the Mandate)"}, "seq": {"type": "integer", "minimum": 0}},
              "description": "present on every chain event (A5.8)"},
    "prev_hash": {"$ref": "#/$defs/Hash", "description": "envelope_hash of the previous event in the same chain; absent at seq 0 and outside a chain"},
    "body": {"type": "object", "description": "validated by the schema for type (allOf below)"},
    "body_hash": {"$ref": "#/$defs/Hash", "description": "sha256 over JCS(body)"},
    "envelope_hash": {"$ref": "#/$defs/Hash", "description": "sha256 over JCS(SignedContext); the event hash in the chain and the hash other ABS objects use to refer to this one"},
    "signatures": {"type": "array", "minItems": 1, "items": {"$ref": "#/$defs/Signature"}}
  },
  "allOf": [
    {"if": {"required": ["chain"], "properties": {"chain": {"properties": {"seq": {"const": 0}}}}}, "then": {"not": {"required": ["prev_hash"]}}},
    {"if": {"required": ["chain"], "properties": {"chain": {"properties": {"seq": {"minimum": 1}}}}}, "then": {"required": ["prev_hash"]}},
    {"if": {"not": {"required": ["chain"]}}, "then": {"not": {"required": ["prev_hash"]}}},
    {"if": {"properties": {"type": {"const": "ParticipationAgreement"}}}, "then": {"properties": {"body": {"$ref": "urn:abs:schema:0.3:participation-agreement"}}}},
    {"if": {"properties": {"type": {"const": "AllowancePolicy"}}}, "then": {"properties": {"body": {"$ref": "urn:abs:schema:0.3:allowance-policy"}}}},
    {"if": {"properties": {"type": {"const": "Mandate"}}}, "then": {"properties": {"body": {"$ref": "urn:abs:schema:0.3:mandate"}}}},
    {"if": {"properties": {"type": {"const": "ApprovalRecord"}}}, "then": {"properties": {"body": {"$ref": "urn:abs:schema:0.3:approval-record"}}}},
    {"if": {"properties": {"type": {"const": "Offer"}}}, "then": {"properties": {"body": {"$ref": "urn:abs:schema:0.3:offer"}}}},
    {"if": {"properties": {"type": {"const": "OfferSnapshot"}}}, "then": {"properties": {"body": {"$ref": "urn:abs:schema:0.3:offer-snapshot"}}}},
    {"if": {"properties": {"type": {"const": "PurchaseRecord"}}}, "then": {"properties": {"body": {"$ref": "urn:abs:schema:0.3:purchase-record"}}}},
    {"if": {"properties": {"type": {"const": "ActionEvent"}}}, "then": {"properties": {"body": {"$ref": "urn:abs:schema:0.3:action-event"}}}},
    {"if": {"properties": {"type": {"const": "SettlementInstruction"}}}, "then": {"properties": {"body": {"$ref": "urn:abs:schema:0.3:settlement-instruction"}}}},
    {"if": {"properties": {"type": {"const": "DeliveryRecord"}}}, "then": {"properties": {"body": {"$ref": "urn:abs:schema:0.3:delivery-record"}}}},
    {"if": {"properties": {"type": {"const": "RefusalRecord"}}}, "then": {"properties": {"body": {"$ref": "urn:abs:schema:0.3:refusal-record"}}}},
    {"if": {"properties": {"type": {"const": "DisputeCase"}}}, "then": {"properties": {"body": {"$ref": "urn:abs:schema:0.3:dispute-case"}}}},
    {"if": {"properties": {"type": {"const": "Decision"}}}, "then": {"properties": {"body": {"$ref": "urn:abs:schema:0.3:decision"}}}},
    {"if": {"properties": {"type": {"const": "Finding"}}}, "then": {"properties": {"body": {"$ref": "urn:abs:schema:0.3:finding"}}}},
    {"if": {"properties": {"type": {"const": "DecisionReceipt"}}}, "then": {"properties": {"body": {"$ref": "urn:abs:schema:0.3:decision-receipt"}}}},
    {"if": {"properties": {"type": {"const": "TrustAttestation"}}}, "then": {"properties": {"body": {"$ref": "urn:abs:schema:0.3:trust-attestation"}}}}
  ],
  "$defs": {
    "Hash": {"type": "string", "pattern": "^sha256:[0-9a-f]{64}$", "description": "full SHA-256; a prefix is never a commitment (A5.8)"},
    "Role": {"enum": ["user", "agent_provider", "merchant", "arbiter", "trust_authority", "certifier", "psp"]},
    "SignedContext": {"type": "object", "required": ["ctx", "abs_version", "type", "id", "created_at", "chain_id", "seq", "prev_hash", "body_hash"], "additionalProperties": false,
      "properties": {"ctx": {"const": "ABS-ENVELOPE"}, "abs_version": {"const": "0.3"}, "type": {"type": "string"}, "id": {"type": "string"},
                     "created_at": {"type": "string", "format": "date-time"}, "chain_id": {"type": ["string", "null"]}, "seq": {"type": ["integer", "null"], "minimum": 0},
                     "prev_hash": {"anyOf": [{"$ref": "#/$defs/Hash"}, {"type": "null"}]}, "body_hash": {"$ref": "#/$defs/Hash"}},
      "description": "rebuilt by the verifier from the envelope (absent chain fields and prev_hash as null), never transmitted; envelope_hash = sha256(JCS(SignedContext))"},
    "SignatureInput": {"type": "object", "required": ["envelope_hash", "role", "party_id", "kid", "signed_at"], "additionalProperties": false,
      "properties": {"envelope_hash": {"$ref": "#/$defs/Hash"}, "role": {"$ref": "#/$defs/Role"}, "party_id": {"type": "string"}, "kid": {"type": "string"}, "signed_at": {"type": "string", "format": "date-time"}},
      "description": "the detached JWS payload of each signature is JCS(SignatureInput), built from envelope_hash and the Signature's own fields"},
    "Signature": {"type": "object", "required": ["role", "party_id", "kid", "alg", "sig", "signed_at"], "additionalProperties": false,
      "properties": {"role": {"$ref": "#/$defs/Role"},
                     "party_id": {"type": "string"}, "kid": {"type": "string"}, "alg": {"enum": ["Ed25519", "ES256", "EdDSA"], "description": "Ed25519 or ES256 (RFC 9864 registers Ed25519 and deprecates the polymorphic EdDSA identifier); EdDSA accepted for verification of legacy objects only"},
                     "sig": {"type": "string", "description": "JWS compact serialisation, detached payload = JCS(SignatureInput) (A5.3)"},
                     "signed_at": {"type": "string", "format": "date-time"}}},
    "Money": {"type": "object", "required": ["amount", "currency"],
      "properties": {"amount": {"type": "string", "pattern": "^-?[0-9]+(\\.[0-9]{1,4})?$"}, "currency": {"type": "string", "pattern": "^[A-Z]{3}$"}}},
    "UntrustedText": {"type": "object", "required": ["text", "class"],
      "properties": {"text": {"type": "string", "maxLength": 20000}, "class": {"const": "untrusted_text"}, "lang": {"type": "string"}},
      "description": "Free text written by a party. Shown to humans. Never an instruction to an agent. Never binding."},
    "PartyRef": {"type": "object", "required": ["party_id", "role"],
      "properties": {"party_id": {"type": "string"}, "role": {"$ref": "#/$defs/Role"}, "kid": {"type": "string"}}},
    "ImageRef": {"type": "object", "required": ["url", "sha256"],
      "properties": {"url": {"type": "string", "format": "uri"}, "sha256": {"$ref": "#/$defs/Hash"},
                     "role": {"enum": ["primary", "gallery", "label", "packaging", "defect", "delivery", "return_inspection"]},
                     "c2pa_manifest_hash": {"$ref": "#/$defs/Hash", "description": "when the image carries a C2PA manifest; proves provenance and edits, not truth"},
                     "provenance": {"$ref": "#/$defs/Provenance"}}},
    "Category": {"type": "object", "required": ["vocabulary", "code"],
      "properties": {"vocabulary": {"enum": ["iso18245:mcc", "gs1:gpc", "google:product", "abs:profile", "merchant"]}, "code": {"type": "string"}, "label": {"type": "string"}}},
    "FactKind": {"enum": ["offer_terms", "user_instruction", "user_authorisation", "agent_actions", "amount_charged", "payment_status", "parcel_handover", "parcel_weight",
                          "unit_identity", "unit_sale_history", "package_contents", "item_condition", "digital_delivery", "service_performed", "image_integrity", "goods_returned"],
      "description": "the kinds of fact a record can be authority for (A5.7 authority table)"},
    "Provenance": {"type": "object", "required": ["issuer", "stake", "committed", "custody", "authority_for"], "additionalProperties": false,
      "description": "who issued the item, their stake, when it was committed, who has held it and which facts it has authority for (A5.7); set by the verifier from keys, the registry of roles and commitment proofs, never taken from the submitting party; a signature or chain proves origin and integrity since commitment, never truth",
      "properties": {
        "issuer": {"type": "object", "required": ["role"], "additionalProperties": false,
                   "properties": {"role": {"enum": ["user", "agent_provider", "merchant", "carrier", "registry", "psp", "inspector", "capture_app_vendor", "arbiter", "other"]},
                                  "party_id": {"type": "string"}, "kid": {"type": "string"}}},
        "stake": {"enum": ["none", "buyer_side", "merchant_side", "both_sides", "unknown"], "description": "the issuer's interest in the outcome of this dispute; an affiliate takes its principal's stake; unknown counts as a stake"},
        "committed": {"type": "object", "required": ["at", "relative_to_dispute", "proof"], "additionalProperties": false,
                      "properties": {"at": {"type": "string", "format": "date-time"},
                                     "relative_to_dispute": {"enum": ["before", "after", "unknown"], "description": "before = committed before the dispute arose (the earlier of the filing and the first complaint on the record); unknown counts as after"},
                                     "proof": {"enum": ["chain_anchored", "issuer_signed", "transparency_log", "qualified_timestamp", "none"], "description": "how the time of commitment is proved; none = only the producing party's word"}}},
        "custody": {"type": "object", "required": ["held_by", "integrity"], "additionalProperties": false,
                    "properties": {"held_by": {"enum": ["user", "agent_provider", "merchant", "psp", "carrier", "registry", "inspector", "arbiter"]},
                                   "integrity": {"enum": ["verified_against_commitment", "issuer_signature_verified", "unverified_copy"], "description": "whether the item produced is provably the item committed"}}},
        "authority_for": {"type": "array", "items": {"$ref": "#/$defs/FactKind"}, "description": "facts for which this issuer is a source of record (A5.7); a record is never authority for a fact outside this list, however it is signed"},
        "signature_verified": {"type": "boolean", "description": "origin and integrity since signing; not truth"}}}
  }
}
```

### A5.4 Conformity-critical attributes

The core needs one thing from the Offer Specification of Part B2: the subset of an offer that is
binding and checkable at delivery. Each such attribute carries a dictionary reference where one
exists (GS1, schema.org, ECLASS, ETIM), a unit (UCUM), a tolerance and a verification method. Free
text (`title`, `description`) is non-binding marketing and untrusted data for agents.

```json
{
  "$id": "urn:abs:schema:0.3:attribute",
  "type": "object",
  "required": ["name", "value", "binding", "verification_method"],
  "additionalProperties": false,
  "properties": {
    "name": {"type": "string", "maxLength": 64, "description": "e.g. model_identifier, variant, capacity, colour, plug_type, region, condition, package_contents, warranty_months"},
    "dictionary": {"type": "object", "properties": {"scheme": {"enum": ["gs1", "schema.org", "eclass", "etim", "dpp", "merchant"]}, "code": {"type": "string"}}},
    "value": {"type": ["string", "number", "boolean"]},
    "value_list": {"type": "array", "items": {"type": ["string", "number", "boolean"]}, "description": "set-valued attributes such as package contents or compatible regions"},
    "unit": {"type": "string", "maxLength": 32, "description": "UCUM code for numeric values"},
    "tolerance": {"type": "object", "properties": {"abs": {"type": "number", "minimum": 0}, "rel_pct": {"type": "number", "minimum": 0},
                  "equivalents": {"type": "array", "items": {"type": "string"}}}, "description": "absent = exact match"},
    "verification_method": {"enum": ["label_read", "serial_lookup", "count", "measure", "weigh", "visual_match", "functional_test", "document_check", "acceptance_step", "delivery_log", "not_verifiable_at_delivery"]},
    "binding": {"type": "boolean"},
    "source": {"enum": ["merchant_entered", "producer", "gdsn", "dpp", "ai_extracted_confirmed"]}
  }
}
```

An offer whose conformity attributes are not confirmed and signed by the merchant has
`spec_status: non_binding`; agents do not buy it under a default Allowance. Honest measurement: on
the 16 not-as-described cases of the Phase 2 run, with contestable delivery evidence present, the
arbiters were as accurate with a free-text listing and one front photo (16 of 16) as with the
signed structured offer (15 of 16); the deviations in those cases also appeared in the title,
description or photo. The case for signed attributes is ambiguity and decidability by rule
(simulation: 0 of 47 spec scenarios decidable on conformity in legacy mode), which that case set
did not stress. An attribute with
`not_verifiable_at_delivery` may be binding, but a conformity claim on it needs evidence beyond the
delivery check and is otherwise `undeterminable`.

### A5.5 Record schemas

**Mandate** (task instruction under an Allowance Policy; the policy's full schema is in Part B3).
Signed by: user through strong authentication, agent provider.

```json
{
  "$id": "urn:abs:schema:0.3:mandate",
  "type": "object",
  "required": ["mandate_id", "allowance_policy_id", "allowance_policy_hash", "user_ref", "agent_provider", "agent_id", "intent_hash", "proposed_by", "user_confirmation",
               "max_total", "max_units", "valid_from", "expires_at", "autonomy_required", "authentication", "rulebook_version", "nonce"],
  "additionalProperties": false,
  "allOf": [{"if": {"properties": {"proposed_by": {"const": "agent"}}}, "then": {"required": ["conversation_hash", "template_profile"]},
             "description": "capture provenance (A4.1 Step 3b, A9.3 item 1): a Mandate the agent proposed records the conversation it came from and the template that prompted it"}],
  "properties": {
    "mandate_id": {"type": "string"},
    "allowance_policy_id": {"type": "string"}, "allowance_policy_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"},
    "user_ref": {"type": "string", "description": "pseudonymous"},
    "agent_provider": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef"}, "agent_id": {"type": "string"},
    "intent_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash", "description": "sha256 of the instruction text the user confirmed: shown verbatim at the confirmation tap and covered by user_confirmation.shown_terms_hash; explicit requirements in it bind as text terms (A4.1 Step 3)"},
    "intent_summary": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/UntrustedText"},
    "proposed_by": {"enum": ["agent", "user"], "description": "agent: the agent proposed the Mandate from the conversation and the user confirmed it (the normal case; conversation_hash and template_profile then required); user: the user wrote the terms"},
    "conversation_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash", "description": "hash of the conversation record the Mandate was proposed from, committed here so the record cannot be altered later; kept by the agent provider; its contents are not terms: a requirement stated there and not captured is a capture failure (AG1-C, A4.1 Step 3b)"},
    "template_profile": {"type": "object", "required": ["id", "version", "prompted_attributes", "left_open"], "additionalProperties": false, "properties": {"id": {"type": "string"}, "version": {"type": "string"}, "prompted_attributes": {"type": "array", "items": {"type": "string"}}, "left_open": {"type": "array", "items": {"type": "string"}}},
                         "description": "the category template used to prompt for conformity-critical attributes, and which were left open by the user"},
    "user_confirmation": {"type": "object", "required": ["confirmed_at", "shown_terms_hash"], "additionalProperties": false, "properties": {"confirmed_at": {"type": "string", "format": "date-time"}, "shown_terms_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash", "description": "hash of what was shown at the confirmation tap: every captured term in plain words, the attributes left open, and the instruction text verbatim"}}},
    "max_total": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}, "max_per_purchase": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"},
    "categories": {"type": "array", "items": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Category"}},
    "merchant_allowlist": {"type": "array", "items": {"type": "string"}}, "merchant_denylist": {"type": "array", "items": {"type": "string"}},
    "min_merchant_qualification": {"enum": ["probation", "qualified", "established"], "default": "qualified"},
    "max_units": {"type": "integer", "minimum": 1}, "max_lines": {"type": "integer", "minimum": 1}, "max_purchases": {"type": "integer", "minimum": 1, "default": 1},
    "condition_allowed": {"type": "array", "items": {"enum": ["new", "refurbished", "used_like_new", "used_good", "used_acceptable"]}},
    "delivery_countries": {"type": "array", "items": {"type": "string", "pattern": "^[A-Z]{2}$"}},
    "delivery_address_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"},
    "item_requirements": {"type": "array", "items": {"$ref": "urn:abs:schema:0.3:attribute"},
                          "description": "captured, machine-readable requirements for the item (model, variant, capacity, size, colour, region, condition, package contents, dates, reference, deadline); each is an explicit mandate term, and a purchase that misses one is AG1-P"},
    "scope_only_named_item": {"type": "boolean", "default": true, "description": "explicit term: the agent buys only the item named; adding another item is AG1-P"},
    "ask_on_ambiguity": {"type": "boolean", "default": true, "description": "an explicit term: a guess where this is true is agent fault (AG1-P)"},
    "currency": {"type": "object", "properties": {"pay_in": {"type": "string", "pattern": "^[A-Z]{3}$"}, "fx_tolerance_pct": {"type": "number", "minimum": 0}}, "description": "explicit term: pay-in currency and the conversion tolerance the agent may accept"},
    "approval_prompt_must_show": {"type": "array", "items": {"enum": ["item", "amount", "merchant", "delivery_date", "total_incl_tax"]}, "description": "explicit term: an approval obtained with a prompt that omits these is not an approval"},
    "recurring": {"type": "object", "properties": {"period": {"enum": ["weekly", "monthly", "quarterly", "yearly"]}, "max_charges": {"type": "integer", "minimum": 1}, "max_per_charge": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}}, "description": "explicit terms for recurring purchases; a charge beyond max_charges or after expiry is AG0 (b) against the merchant"},
    "business_terms": {"type": "object", "properties": {"purchase_order_ref": {"type": "string"}, "buyer_vat_id": {"type": "string"}, "einvoice_format": {"type": "string"}, "payment_terms": {"type": "string", "description": "e.g. net30; prepaying where terms were mandated is a no-loss breach"},
                       "procurement_threshold": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}, "framework_allowlist": {"type": "array", "items": {"type": "string"}}}, "description": "explicit terms for business and public buyers"},
    "incentive_disclosure": {"type": "array", "items": {"type": "object", "properties": {"merchant_id": {"type": "string"}, "kind": {"type": "string"}, "disclosed_at": {"type": "string", "format": "date-time"}}}, "description": "payments the agent provider receives from merchants; an undisclosed one that steered the choice is ABS-X2"},
    "policy_version": {"type": "object", "properties": {"version": {"type": "string"}, "acknowledged_by_agent_at": {"type": "string", "format": "date-time"}}, "description": "a tightened policy binds from the agent's acknowledgement"},
    "autonomy_required": {"enum": ["autonomous", "notify_and_hold", "approval_required"], "description": "the level the Allowance Policy requires for this task; buying at a lower level is AG1-P"},
    "valid_from": {"type": "string", "format": "date-time"}, "expires_at": {"type": "string", "format": "date-time"},
    "payment_instruments": {"type": "array", "items": {"type": "object", "required": ["rail", "instrument_ref"],
                            "properties": {"rail": {"enum": ["card", "a2a_instant", "a2a_batch", "wallet", "stablecoin", "other"]}, "instrument_ref": {"type": "string", "description": "token or account reference; never a PAN"}}}},
    "authentication": {"type": "object", "required": ["method", "performed_at", "reference", "assurance"],
                       "properties": {"method": {"enum": ["sca_app", "sca_3ds", "passkey", "bank_login", "other"]}, "performed_at": {"type": "string", "format": "date-time"},
                                      "reference": {"type": "string"}, "assurance": {"enum": ["psd2_sca", "nist_aal2", "nist_aal3", "unknown"]},
                                      "dynamic_link": {"type": "object", "properties": {"amount": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}, "payee_scope": {"type": "string"}}}}},
    "rulebook_version": {"type": "string"}, "rules_shown_at": {"type": "string", "format": "date-time"},
    "nonce": {"type": "string", "minLength": 16}
  }
}
```

**Approval Record.** Produced when the Allowance routes a purchase to notify-and-hold or approval.
Signed by: agent provider, carrying the approver's authentication reference.

```json
{
  "$id": "urn:abs:schema:0.3:approval-record",
  "type": "object",
  "required": ["approval_id", "mandate_id", "cart_hash", "level_applied", "matched_rule_id", "outcome"],
  "additionalProperties": false,
  "properties": {
    "approval_id": {"type": "string"}, "mandate_id": {"type": "string"},
    "cart_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash", "description": "hash of the exact cart and totals shown"},
    "level_applied": {"enum": ["notify_and_hold", "approval_required"]}, "matched_rule_id": {"type": "string"},
    "routing_receipt_id": {"type": "string", "description": "Decision Receipt of the allowance ruleset that chose the level"},
    "notification": {"type": "object", "properties": {"sent_at": {"type": "string", "format": "date-time"}, "channel": {"type": "string"}}},
    "hold": {"type": "object", "properties": {"hold_until": {"type": "string", "format": "date-time"}, "cancelled": {"type": "boolean"}, "cancelled_at": {"type": "string", "format": "date-time"}}},
    "approver": {"type": "object", "properties": {"type": {"enum": ["user", "delegate"]}, "ref": {"type": "string"}, "role": {"type": "string"}}},
    "authentication": {"type": "object", "properties": {"method": {"type": "string"}, "reference": {"type": "string"}, "assurance": {"type": "string"}, "performed_at": {"type": "string", "format": "date-time"}}},
    "shown_summary_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash", "description": "hash of the plain-language summary the approver saw: items, merchant, total incl. tax, signals"},
    "deviation_acceptance": {"type": "array", "items": {"type": "object", "required": ["attribute", "offered_value", "deviation_text_hash", "authentication_reference"],
                             "properties": {"attribute": {"type": "string"}, "offered_value": {"type": ["string", "number", "boolean"]}, "deviation_text_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}, "authentication_reference": {"type": "string"}}},
                             "description": "per-purchase, express and separate acceptance of a specific deviation of the offer bought, shown in the approval prompt (A4.3); a standing advance acceptance is not used"},
    "outcome": {"enum": ["approved", "declined", "expired", "hold_elapsed", "cancelled"]},
    "decided_at": {"type": "string", "format": "date-time"}
  }
}
```

**Offer Snapshot.** Frozen at view and at checkout; the checkout snapshot is the conformity
reference and is countersigned by the merchant at acceptance, after which "the listing" means the
snapshot. Signed by: agent provider; merchant (checkout snapshots).

```json
{
  "$id": "urn:abs:schema:0.3:offer-snapshot",
  "type": "object",
  "required": ["snapshot_id", "when", "captured_at", "mandate_id", "agent_id", "offer_hash", "offer_signature", "merchant", "offer_id",
               "conformity_spec", "spec_status", "price", "price_includes_tax", "mandatory_fees", "delivery_option", "returns_policy", "condition", "images", "source"],
  "additionalProperties": false,
  "properties": {
    "snapshot_id": {"type": "string"}, "when": {"enum": ["view", "checkout"]}, "captured_at": {"type": "string", "format": "date-time"},
    "mandate_id": {"type": "string"}, "agent_id": {"type": "string"},
    "merchant": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef"}, "offer_id": {"type": "string"},
    "gtin": {"type": "string", "pattern": "^[0-9]{8,14}$"}, "sku": {"type": "string"},
    "offer_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash", "description": "the envelope_hash of the merchant-signed ABS Offer, or the SHA-256 of the bytes of a UCP/ACP/AP2 object (then also in external_object); must verify against the merchant key"},
    "offer_signature": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Signature"},
    "external_object": {"type": "object", "properties": {"protocol": {"enum": ["ap2", "ucp", "acp", "abs"]}, "object_ref": {"type": "string"}, "object_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}},
                        "description": "the checkout object of the protocol used (e.g. the AP2 merchant-signed checkout JWT), bound by hash, when ABS runs as a profile; every such binding is PROPOSED, not implemented or tested (A5.2)"},
    "conformity_spec": {"type": "array", "minItems": 1, "items": {"$ref": "urn:abs:schema:0.3:attribute"}, "description": "binding attributes only"},
    "spec_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}, "spec_status": {"enum": ["binding", "non_binding"]},
    "profile": {"type": "object", "properties": {"id": {"type": "string"}, "version": {"type": "string"}}},
    "condition": {"enum": ["new", "refurbished", "used_like_new", "used_good", "used_acceptable"]},
    "package_contents": {"type": "array", "items": {"type": "object", "required": ["item", "qty"], "properties": {"item": {"type": "string", "maxLength": 100}, "qty": {"type": "integer", "minimum": 1}}}},
    "price": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}, "price_includes_tax": {"type": "boolean"},
    "mandatory_fees": {"type": "array", "items": {"type": "object", "required": ["name", "amount"], "properties": {"name": {"type": "string", "maxLength": 64}, "amount": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}}}},
    "reference_price": {"type": "object", "properties": {"price": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}, "basis": {"enum": ["rrp", "own_previous_30_days", "none"]}}},
    "delivery_option": {"type": "object", "required": ["method", "cost", "estimated_days_max"],
                        "properties": {"method": {"enum": ["standard", "express", "pickup", "digital", "service_date"]}, "cost": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"},
                                       "estimated_days_min": {"type": "integer"}, "estimated_days_max": {"type": "integer"}, "service_date": {"type": "string", "format": "date"}, "destination": {"type": "string"}}},
    "returns_policy": {"type": "object", "required": ["window_days", "who_pays_return"],
                       "properties": {"window_days": {"type": "integer"}, "who_pays_return": {"enum": ["merchant", "buyer", "merchant_if_non_conforming"]},
                                      "conditions": {"type": "array", "items": {"type": "string"}}, "statutory_withdrawal_applies": {"type": "boolean"}}},
    "warranty_months": {"type": "integer"},
    "tax": {"type": "object", "properties": {"rate_pct": {"type": "number"}, "scheme": {"type": "string"}, "seller_vat_id": {"type": "string"}}},
    "cross_border": {"type": "object", "properties": {"ships_from_country": {"type": "string"}, "import_charges_included": {"type": "boolean"}, "estimated_import_charges": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}}},
    "images": {"type": "array", "minItems": 1, "items": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/ImageRef"}},
    "images_verified": {"type": "boolean"},
    "marketing_text_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash", "description": "hash of title and description as shown; kept for AG4 evidence, never binding"},
    "compared_record": {"type": "object", "properties": {"kind": {"enum": ["offer_feed_record", "negotiation_record", "seller_agent_statement"]}, "hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"},
                        "price": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}, "delivery_cost": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}, "fees_total": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}},
                        "description": "the record the agent relied on when it chose this merchant; checkout terms worse than it are AG1-M (extended)"},
    "negotiation_record": {"type": "object", "properties": {"hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}, "buyer_agent_signature": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Signature"}, "seller_agent_signature": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Signature"}},
                           "description": "agent-to-agent: terms bind only when written here and signed by both agents; seller-agent statements outside it are merchant content for Step 2"},
    "idempotency_key": {"type": "string", "description": "derived from mandate_id and the cart hash; a duplicate capture against one key is the merchant's, a duplicate order without a key is the agent provider's"},
    "source": {"enum": ["feed", "protocol_object", "page"]},
    "page_render_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"},
    "merchant_order_acceptance": {"type": "object", "properties": {"order_id": {"type": "string"}, "accepted_at": {"type": "string", "format": "date-time"}}}
  }
}
```

**Purchase Record** (trace digest). Signed by: agent provider; merchant (order acceptance).

```json
{
  "$id": "urn:abs:schema:0.3:purchase-record",
  "type": "object",
  "required": ["purchase_id", "mandate_id", "mandate_hash", "agent_id", "merchant", "cart", "totals", "controls", "trace_digest", "rulebook_version"],
  "additionalProperties": false,
  "properties": {
    "purchase_id": {"type": "string"}, "mandate_id": {"type": "string"}, "mandate_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"},
    "agent_id": {"type": "string"}, "merchant": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef"}, "merchant_order_id": {"type": "string"},
    "idempotency_key": {"type": "string"},
    "cart": {"type": "array", "minItems": 1, "items": {"type": "object", "required": ["line", "snapshot_id", "offer_id", "qty", "unit_price", "added_by", "responding_party"],
             "properties": {"line": {"type": "integer"}, "snapshot_id": {"type": "string"}, "offer_id": {"type": "string"}, "qty": {"type": "integer", "minimum": 1},
                            "unit_price": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}, "added_by": {"enum": ["agent", "merchant", "user"]},
                            "responding_party": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef", "description": "who answers for this line: the seller for its goods and conduct; the platform for its own feed, fees, merges and hosting duties (marketplaces)"},
                            "agent_reason": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/UntrustedText"}}}},
    "totals": {"type": "object", "required": ["items", "delivery", "fees", "tax", "total"],
               "properties": {"items": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}, "delivery": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"},
                              "fees": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}, "tax": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}, "total": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}}},
    "tax_detail": {"type": "object", "description": "buyer type, VAT ids, per-line VAT, import charges, e-invoice reference (Part B3)"},
    "clarifications": {"type": "array", "items": {"type": "object", "required": ["asked_at", "question_hash", "answer_hash"],
                       "properties": {"asked_at": {"type": "string", "format": "date-time"}, "question_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"},
                                      "answer_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}, "user_auth_reference": {"type": "string", "description": "present: the user confirmed this answer with authentication, so it amends the Mandate and binds as a text term (AG1-P if broken); absent: conversation only (AG1-C if it stated a requirement the agent did not capture), A4.1 Step 3"}}}},
    "controls": {"type": "object", "required": ["mandate_check", "autonomy", "risk_signals", "monitor"],
      "properties": {
        "trust_attestation": {"type": "object", "properties": {"attestation_id": {"type": "string"}, "level": {"type": "string"}, "settlement_timing": {"type": "string"}}},
        "mandate_check": {"type": "object", "required": ["passed"], "properties": {"passed": {"type": "boolean"},
                          "violations": {"type": "array", "items": {"enum": ["amount_exceeds_limit", "category_not_permitted", "merchant_not_permitted", "quantity_exceeds_limit", "mandate_expired",
                                         "condition_not_permitted", "delivery_country_not_permitted", "merchant_not_qualified", "attestation_expired", "above_merchant_cap", "non_binding_offer"]}}}},
        "autonomy": {"type": "object", "required": ["level_required", "level_applied"],
                     "properties": {"level_required": {"type": "string"}, "level_applied": {"type": "string"}, "approval_id": {"type": "string"}}},
        "risk_signals": {"type": "array", "items": {"type": "string"}},
        "monitor": {"type": "object", "required": ["applied"], "properties": {"applied": {"type": "boolean"}, "decision": {"enum": ["approve", "block", "not_applied"]}, "monitor_id": {"type": "string"}}}
      }},
    "trace_digest": {"type": "object", "required": ["chain_head", "event_count", "first_event_at", "last_event_at"],
                     "properties": {"chain_head": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash", "description": "envelope_hash of the last chain event before this Purchase Record, equal to this envelope's prev_hash (A5.3, A5.8)"}, "event_count": {"type": "integer"},
                                    "first_event_at": {"type": "string", "format": "date-time"}, "last_event_at": {"type": "string", "format": "date-time"}, "log_location_ref": {"type": "string"}}},
    "agent_summary_to_user_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"},
    "rulebook_version": {"type": "string"}
  }
}
```

**Delivery Record** (contestable evidence). Signed by: merchant (shipment part); user or agent
provider (receipt part).

```json
{
  "$id": "urn:abs:schema:0.3:delivery-record",
  "type": "object",
  "required": ["delivery_id", "purchase_id", "shipment"],
  "additionalProperties": false,
  "properties": {
    "delivery_id": {"type": "string"}, "purchase_id": {"type": "string"},
    "shipment": {"type": "object", "required": ["lines", "shipped_at", "delivery_option"],
      "properties": {"lines": {"type": "array", "items": {"type": "object", "required": ["line", "qty_shipped"],
                     "properties": {"line": {"type": "integer"}, "qty_shipped": {"type": "integer"}, "serials": {"type": "array", "items": {"type": "string"}}}}},
                     "shipped_at": {"type": "string", "format": "date-time"}, "delivery_option": {"type": "integer"}, "carrier": {"type": "string"}, "tracking_ref": {"type": "string"},
                     "packing_record": {"type": "object", "properties": {"images": {"type": "array", "items": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/ImageRef"}},
                                        "video_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}, "weight_g": {"type": "integer"}, "recorded_at": {"type": "string", "format": "date-time"}},
                                        "description": "self-serving; weighed, not presumed"},
                     "carrier_proof": {"type": "object", "properties": {"status": {"type": "string"}, "delivered_at": {"type": "string", "format": "date-time"},
                                       "signature_or_code": {"enum": ["signature", "pickup_code", "photo", "none"]}, "parcel_weight_g": {"type": "integer"},
                                       "evidence_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}}, "description": "the carrier does not inspect contents"},
                     "digital_delivery_log": {"type": "object", "properties": {"delivered_at": {"type": "string", "format": "date-time"}, "activation_or_download_ref": {"type": "string"}, "log_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}}},
                     "service_acceptance": {"type": "object", "properties": {"performed_at": {"type": "string", "format": "date-time"}, "accepted_by": {"type": "string"}, "acceptance_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}}}}},
    "receipt": {"type": "object", "required": ["received_at", "conformity"],
      "properties": {"received_at": {"type": "string", "format": "date-time"},
                     "conformity": {"enum": ["conforms", "non_conforming", "not_received", "not_checked"]}, "checked_by": {"enum": ["user", "agent", "both"]},
                     "spec_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}, "attributes_checked": {"type": "integer"}, "attributes_undeterminable": {"type": "integer"},
                     "buyer_evidence": {"type": "array", "items": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/ImageRef"}, "description": "photos or video with metadata; can be manipulated"},
                     "serial_lookup": {"type": "object", "properties": {"registry": {"type": "string"}, "result": {"enum": ["match", "no_match", "not_available"]}, "checked_at": {"type": "string", "format": "date-time"}}},
                     "mismatches": {"type": "array", "items": {"type": "object", "required": ["line", "field", "offered", "delivered", "verification_method"],
                                    "properties": {"line": {"type": "integer"}, "field": {"type": "string"}, "offered": {"type": ["string", "number", "boolean"]}, "delivered": {"type": ["string", "number", "boolean"]},
                                                   "unit": {"type": "string"}, "tolerance_applied": {"type": "object"}, "verification_method": {"type": "string"},
                                                   "evidence": {"type": "array", "items": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/ImageRef"}}}}},
                     "notes": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/UntrustedText"}}},
    "return_inspection": {"type": "object", "properties": {"inspected_at": {"type": "string", "format": "date-time"}, "result": {"enum": ["as_offered", "non_conforming", "damaged", "not_returned"]},
                          "evidence": {"type": "array", "items": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/ImageRef"}}}, "description": "signed by the merchant; weighed against the buyer evidence"}
  }
}
```

**Dispute Case.** Signed by: filer; merchant (response).

```json
{
  "$id": "urn:abs:schema:0.3:dispute-case",
  "type": "object",
  "required": ["case_id", "purchase_id", "purchase_hash", "filed_by", "filed_at", "reason_code", "disputed_lines", "disputed_amount", "remedy_requested", "claim",
               "evidence_level", "evidence_refs", "timeline", "status", "rulebook_version", "rail"],
  "additionalProperties": false,
  "properties": {
    "case_id": {"type": "string"}, "purchase_id": {"type": "string"}, "purchase_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"},
    "rail": {"enum": ["card", "a2a_instant", "a2a_batch", "wallet", "stablecoin", "other"]},
    "filed_by": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef"}, "user_consent_reference": {"type": "string"},
    "filed_at": {"type": "string", "format": "date-time"},
    "reason_code": {"enum": ["AG0", "AG1-M", "AG1-P", "AG1-C", "AG2", "AG3", "AG4", "AG4-D", "AG5"]},
    "legacy_category": {"enum": ["unauthorised", "not_received", "not_as_described", "processing_error", "authorised_but_wrong", "none"]},
    "required_parties": {"type": "array", "items": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef"}, "description": "the agent provider is a required party whenever reason_code is AG1-P or AG1-C; a tier 1 settlement cannot allocate cost to an absent party"},
    "buyer_type": {"enum": ["consumer", "business"]}, "goods_category": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Category"},
    "withdrawal_right": {"type": "object", "properties": {"applies": {"type": "boolean"}, "expires_at": {"type": "string", "format": "date-time"}, "exception": {"type": "string"}}},
    "disputed_lines": {"type": "array", "minItems": 1, "items": {"type": "integer"}}, "disputed_amount": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"},
    "remedy_requested": {"enum": ["full_refund", "return_and_refund", "partial_refund", "replacement", "withdrawal", "deny"]},
    "claim": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/UntrustedText"},
    "evidence_level": {"enum": ["E0", "E1", "E2", "E3"]},
    "evidence_refs": {"type": "array", "items": {"type": "object", "required": ["type", "hash"],
                      "properties": {"type": {"enum": ["mandate", "allowance_policy", "approval_record", "offer_snapshot", "purchase_record", "settlement_instruction", "delivery_record", "action_log", "clarification", "image", "carrier_record", "serial_lookup", "digital_log", "return_inspection", "other"]},
                                     "hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}, "held_by": {"enum": ["user", "agent_provider", "merchant", "psp", "carrier", "registry", "inspector"]},
                                     "provenance": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Provenance", "description": "set by the verifier when the item is registered (A5.7); a value supplied by the filer is ignored"}}}},
    "merchant_response": {"type": "object", "properties": {"responded_at": {"type": "string", "format": "date-time"},
                          "offer": {"enum": ["full_refund", "return_and_refund", "partial_refund", "replacement", "deny"]}, "partial_amount": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"},
                          "text": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/UntrustedText"},
                          "attachments": {"type": "array", "items": {"type": "object", "required": ["type", "hash"],
                                          "properties": {"type": {"enum": ["listing_page", "photo", "packing_record", "carrier_record", "serial_record", "return_inspection", "other"]},
                                                         "hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}, "matches_checkout_snapshot": {"type": "boolean", "description": "set by the verifier, not the merchant"},
                                                         "provenance": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Provenance", "description": "set by the verifier, not the merchant (A5.7)"}}}}}},
    "buyer_reply_to_offer": {"enum": ["accept", "reject", "none"]},
    "timeline": {"type": "object", "required": ["response_due", "escalation_due"],
                 "properties": {"response_due": {"type": "string", "format": "date-time"}, "escalation_due": {"type": "string", "format": "date-time"},
                                "escalated_at": {"type": "string", "format": "date-time"}, "decision_due": {"type": "string", "format": "date-time"}}},
    "human_review_requested": {"type": "object", "properties": {"by": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef"}, "at": {"type": "string", "format": "date-time"}}},
    "tier": {"enum": [1, 2]}, "status": {"enum": ["filed", "responded", "settled", "escalated", "under_human_review", "decided", "appealed", "withdrawn", "closed"]},
    "rulebook_version": {"type": "string"}
  }
}
```

**Decision.** Signed by: arbiter (tier 2); user side and merchant (tier 1 settlement).

```json
{
  "$id": "urn:abs:schema:0.3:decision",
  "type": "object",
  "required": ["decision_id", "case_id", "tier", "decided_at", "conformity_finding", "reason_code", "liable_party", "remedy", "withdrawal_right_available",
               "amounts", "evidence_integrity", "rationale", "plain_language_explanation", "human_review", "binding_effect", "receipt_id"],
  "additionalProperties": false,
  "properties": {
    "decision_id": {"type": "string"}, "case_id": {"type": "string"}, "tier": {"enum": [1, 2]},
    "arbiter": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef"}, "decided_at": {"type": "string", "format": "date-time"},
    "conformity_finding": {"enum": ["conforms", "non_conforming", "not_received", "undeterminable", "not_applicable"]},
    "reason_code": {"enum": ["AG0", "AG1-M", "AG1-P", "AG1-C", "AG2", "AG3", "AG4", "AG4-D", "AG5"]},
    "liable_party": {"enum": ["merchant", "agent_provider", "psp", "buyer", "rail_process", "register_operator"]},
    "parties_present": {"type": "array", "items": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef"}, "description": "tier 1: cost may be allocated only to a party listed here"},
    "remedy": {"enum": ["refund", "return_and_refund", "partial_refund", "replacement", "withdrawal", "deny"]},
    "withdrawal_right_available": {"type": "boolean"},
    "amounts": {"type": "object", "required": ["to_buyer"],
                "properties": {"to_buyer": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}, "from_merchant": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"},
                               "from_agent_provider": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}, "from_psp": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"},
                               "return_shipping_paid_by": {"enum": ["merchant", "agent_provider", "buyer", "none"]}}},
    "goods_return": {"type": "boolean"}, "return_deadline": {"type": "string", "format": "date-time"},
    "evidence_integrity": {"type": "object", "required": ["chain_verified"],
                           "properties": {"chain_verified": {"enum": ["valid", "broken", "absent"]},
                                          "anchor_commitment_verified": {"type": "boolean", "description": "the full chain head equals its independently authenticated commitment (A5.8); a matching rail locator alone is never enough"},
                                          "rail_locator_matches": {"type": "boolean", "description": "the 16-hex locator in the rail reference matches the head; it identifies the commitment and proves nothing on its own"},
                                          "mandate_signature_valid": {"type": "boolean"}, "merchant_attachments_match_checkout_snapshot": {"type": "boolean"},
                                          "delivery_evidence_weighed": {"type": "array", "items": {"type": "string"}}, "problems": {"type": "array", "items": {"type": "string"}},
                                          "provenance_gate": {"enum": ["passed", "failed_escalated", "not_applicable"], "description": "passed = every liability-moving finding is corroborated under A5.7: a supporting record with authority for the fact, and none contradicting it"},
                                          "provenance_gate_reason": {"enum": ["uncited", "no_authority_for_fact", "issuer_has_stake", "committed_after_dispute", "custody_unverified", "record_does_not_support", "path_unresolved"], "description": "set when provenance_gate is failed_escalated; uncited reviews are published apart (A5.7)"},
                                          "corroborating_items_relied_on": {"type": "array", "items": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}}}},
    "confirmation_route": {"enum": ["recomputed", "committed_record_read", "adverse_inference", "rail_process", "low_value_burden"], "description": "A4.5: how the fact that decides the reason code was established: recomputed from signed records by the published rule; read from records committed before the dispute (typed, cited Finding; human review on request); decided against the keeper of a missing required record (ABS-E1); left to the payer's PSP or the scheme; or not established, the loss allocated by the tiered burden of proof (ABS-V1, A5.7; provenance_gate not_applicable)"},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    "rationale": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/UntrustedText"},
    "plain_language_explanation": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/UntrustedText", "description": "written for the person affected: what was decided, from which evidence, under which rule, and how to ask for a human review or appeal"},
    "conduct_finding": {"enum": ["none", "false_claim_by_buyer_side", "false_evidence_by_merchant", "both"]},
    "human_review": {"type": "object", "required": ["available", "performed"], "properties": {"available": {"const": true}, "performed": {"type": "boolean"}, "reviewer_pseudonym": {"type": "string"}, "outcome": {"enum": ["upheld", "changed", "not_performed"]}}},
    "binding_effect": {"type": "object", "required": ["binds_participants_by_contract", "binds_consumer"],
                       "properties": {"binds_participants_by_contract": {"const": true}, "binds_consumer": {"const": false},
                                      "statutory_routes_unaffected": {"type": "array", "items": {"enum": ["courts", "statutory_adr", "chargeback", "withdrawal", "conformity_guarantee", "unauthorised_payment_refund"]}}}},
    "without_prejudice_to_statutory_conformity": {"const": true},
    "settlement_instruction_ids": {"type": "array", "items": {"type": "string"}},
    "receipt_id": {"type": "string"}, "appeal_of": {"type": "string"},
    "final_between_participants": {"type": "boolean"}, "rulebook_version": {"type": "string"}
  }
}
```

**Refusal Record.** Written whenever the agent does not buy. Signed by: agent provider.

```json
{
  "$id": "urn:abs:schema:0.3:refusal-record",
  "type": "object",
  "required": ["refusal_id", "mandate_id", "refused_at", "offers_compared", "reason_code"],
  "additionalProperties": false,
  "properties": {
    "refusal_id": {"type": "string"}, "mandate_id": {"type": "string"}, "refused_at": {"type": "string", "format": "date-time"},
    "offers_compared": {"type": "array", "items": {"type": "object", "properties": {"snapshot_id": {"type": "string"}, "offer_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}, "merchant": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef"}}}},
    "reason_code": {"enum": ["no_conforming_offer", "over_limit", "merchant_not_qualified", "non_binding_offer", "risk_signal", "user_declined", "approval_declined", "approval_expired", "ambiguity_unresolved", "other"]},
    "reason": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/UntrustedText"},
    "classification": {"enum": ["true_block", "false_refusal", "unclassified"], "description": "set by the programme scoreboard; a refusal of a conforming, qualified, in-mandate offer is a false refusal; no liability either way"}
  }
}
```

**Action Event.** One step of the agent's action log, as a chain event (A5.3, A5.8), so the action
log and the ABS objects form one chain. Signed by: agent provider. The full log stays with the
provider and is disclosed in a case at E2; the chain carries every event's `envelope_hash`.

```json
{
  "$id": "urn:abs:schema:0.3:action-event",
  "type": "object",
  "required": ["mandate_id", "agent_id", "step", "action", "at", "result_status"],
  "additionalProperties": false,
  "properties": {
    "mandate_id": {"type": "string"}, "agent_id": {"type": "string"},
    "step": {"type": "integer", "minimum": 1},
    "action": {"enum": ["search", "fetch_offer", "compare", "snapshot", "ask_user", "receive_answer", "request_approval", "add_to_cart", "checkout", "pay", "refuse", "notify_user", "other"]},
    "at": {"type": "string", "format": "date-time"},
    "inputs_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash", "description": "hash of the typed inputs the step used"},
    "object_refs": {"type": "array", "items": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}, "description": "envelope_hash of the ABS objects the step produced or relied on (snapshots, approval, refusal)"},
    "stated_reason": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/UntrustedText", "description": "the agent's own reason, kept as evidence of what it did; never an instruction"},
    "result_status": {"enum": ["ok", "declined", "error", "skipped"]}
  }
}
```

**Finding** and **Decision Receipt** are defined in A7.4.

### A5.6 Delivery evidence is contestable

No party inspects the contents of a parcel on the buyer's behalf, and nothing records what arrived
infallibly. Audit 0 (I4) found an earlier version that assumed a signed carrier inspection; it is
removed. The Delivery Record holds evidence of mixed reliability, weighed, not presumed:

| Evidence | Who produces it | Reliability note |
|---|---|---|
| Carrier proof of delivery: status, date, signature or pickup code, parcel weight | Carrier | Proves a parcel arrived and roughly what it weighed; the carrier does not open it |
| Merchant packing record: photos or video, serial numbers, weight | Merchant | Self-serving; a serial that later matches the buyer's unit is strong, one that does not is telling |
| Buyer photos or video with metadata | User | Can be manipulated; metadata against the delivery date and the carrier weight is the check |
| Manufacturer serial-registry lookup | Registry, where the brand runs one | Strong when available; most categories have none |
| Digital delivery or activation log | Merchant platform | Standard for digital goods; proves delivery, not fitness |
| Service acceptance step | Both parties | The equivalent of delivery for services |
| Return inspection | Merchant | Weighed against the buyer evidence; late and self-serving |

For goods that are not parcels the bundle is: the digital access log for digital goods and
subscriptions; the completion record for services; the ticket issuance and use log for travel; the
handover and return inspection records for rentals.

**Minimum package for a decidable not-as-described case:** the Offer Snapshot with its signed spec,
the merchant's packing record (serials, weight, photo at packing), and the buyer's photos or a
return inspection, with serials where the goods carry them; plus the signed Mandate and the action
log for any Step 3 question. Carrier proof of delivery is necessary for non-delivery only.

**Weighing:** (a) carrier proof of delivery proves handover, never content; (b) a packing record
with serials matching the Offer Snapshot, unopposed by buyer photos or a return inspection,
establishes conformity; (c) buyer photos showing non-conformity on a unit whose serial matches the
packing record establish non-conformity; (d) where the packing record and the photographed serial
conflict and no record keeper is at fault, the engine returns `review`.

Any piece can be missing or conflict with another. The `delivery_status` and `offer_conformity`
Findings cite the pieces relied on and state the confidence. H5 in the experiment tests the arbiter
on exactly this: conformity decided from contestable evidence, E3 against E0 (Amendment 5).

### A5.7 Rules of evidence

**Evidence provenance (normative).** A label that sorts records into "independent" and
"party-authored" conflates three different things: who wrote a record, whether it can have been
altered since, and whether its author is in a position to know the fact it states. v0.3 replaces
that label with a description of every evidence item by five properties, recorded in its
`provenance` object (`$defs/Provenance`, A5.3). The verifier sets it from the signing keys, the
registry of roles and the commitment proofs; a value supplied by the party that submits the item is
ignored.

| Property | Question it answers | Values |
|---|---|---|
| Issuer | Who made the statement the record contains? | user, agent provider, merchant, carrier, registry, PSP, inspector, capture-app vendor, arbiter |
| Stake | Does the issuer gain or lose by the outcome of this dispute? | none; buyer side; merchant side; both; unknown, which counts as a stake |
| Time of commitment | Was the record committed before the dispute arose, and how is that proved? | before or after the earlier of the filing and the first complaint on the record; proved by a chain anchor, the issuer's signature, a transparency log or a qualified time stamp, or not proved |
| Custody | Who has held it since, and is the item produced provably the item committed? | verified against the commitment; issuer's signature verified; unverified copy |
| Authority | For which facts is the issuer a source of record? | the fact kinds of `$defs/FactKind` |

A signature or a valid chain proves who issued a record and that it has not changed since it was
committed. It never proves that what the record says is true: a merchant can sign a false packing
record, and a certified camera can photograph a staged scene.

**Authority (normative).** Each issuer is a source of record for some facts and for no others. The
authority of a party's own record runs against that party only: it binds its issuer, and it never
proves a fact in the issuer's favour, except as test (c) below allows for the agent provider's
action log.

| Issuer and record | Authority for | Not authority for |
|---|---|---|
| Payer's PSP, issuer or acquirer: authorisation, settlement, Verification of Payee result | `amount_charged`, `payment_status` | anything about the goods |
| Carrier: scan events, proof of delivery, declared and scanned weight | `parcel_handover`, `parcel_weight` | the identity, contents or condition of what was in the parcel |
| Manufacturer or serial registry: lookup of a serial; binding of a shipped serial to the order at dispatch | `unit_identity` and `unit_sale_history` of that serial | condition; package contents; which unit the buyer received, unless the serial was bound to the order at dispatch |
| Inspector without a stake: return or on-request inspection | `unit_identity`, `package_contents`, `item_condition` of the unit inspected | the state of the goods before the inspector received them |
| Capture-app vendor: device-signed capture (C2PA manifest) whose keys the capturing party does not control | `image_integrity`: the image is unaltered since capture on that device at that time | what the scene shows, or that it shows the delivered unit as delivered |
| Merchant: signed offer, countersigned checkout snapshot, packing record, digital delivery log | `offer_terms`, `digital_delivery`, and what it says it shipped, as against the merchant | any fact in the merchant's own favour |
| User: signed Mandate, Approval Record, clarifications confirmed with authentication | `user_instruction`, `user_authorisation`, as against the user | any fact in the user's own favour |
| Agent provider: action log in an anchored chain; conversation record committed by `conversation_hash` | `agent_actions` and what the user said in the conversation, as against the agent provider | any fact in the provider's own favour, except as rule (c) below allows |

**Corroboration (normative).** A Finding that moves liability against a party X rests on one or
more facts. For each such fact F, at least one cited record MUST support F, none may contradict it
(content check, below), and a supporting record MUST meet one of these tests:

- **(a) Independent authority.** F is in the record's `authority_for`, or follows from a fact in it
  by a published deterministic rule (a scanned parcel weight below the expected weight of the
  complete package by more than the scale tolerance shows that something is missing); the issuer's
  stake is `none`; custody is verified; and the record was committed before the dispute arose, or
  is an inspection the Decision Center commissioned from an inspector without a stake.
- **(b) Binding on X.** The record was issued or countersigned by X; it was committed before the
  dispute arose with a proof X cannot rewrite (`chain_anchored`, `transparency_log` or
  `qualified_timestamp`); and F is in its `authority_for`. The countersigned snapshot binds the
  merchant to the offer terms; the signed Mandate and the confirmed clarifications bind the user to
  what was asked; the anchored action log and the committed conversation record bind the agent
  provider to what its agent did and was told.
- **(c) Sole-source conduct record.** F is `agent_actions`, which no other issuer can observe; the
  record is the agent provider's action log, committed before the dispute in an anchored chain; and
  no record meeting (a) or (b) contradicts it. This test serves causation in Step 2 (the agent
  followed injected text, AG4) and nothing else. It is never available for what arrived, where
  sources with independent authority exist.

A record that passes none of the tests may be weighed by a human reviewer, but never grounds an
automatic decision: the case goes to human review or to an independent inspection request, and the
receipt records `provenance_gate: failed_escalated` with the reason (`no_authority_for_fact`,
`issuer_has_stake`, `committed_after_dispute`, `custody_unverified`, `record_does_not_support`,
`path_unresolved` or `uncited`). The burden-of-proof defaults (ABS-E1, ABS-E1m, ABS-D1, ABS-E2,
ABS-V1) decide on the absence of a record a party had to produce, of any content evidence for a
claim, or (ABS-V1, below) of any record with independent authority for a low-value claim; they are
rules about missing evidence, not Findings resting on evidence, and the gate does not apply to them.

What each step needs, by the fact it rests on:

| Finding | Fact | Records that can corroborate it |
|---|---|---|
| Step 0: a valid mandate | `user_authorisation` | the user-signed Mandate with the PSP's authentication reference (b, against the user) |
| Step 1: not received | `parcel_handover` | carrier scan events and proof of delivery (a); for a merchant's denial the same carrier record, never the merchant's own dispatch note |
| Step 1: what arrived, model or variant | `unit_identity` | a registry binding of the shipped serial to the order at dispatch (a); an independent inspection (a); the merchant's packing record committed at dispatch, used against the merchant (b) |
| Step 1: what arrived, a missing part or the quantity | `package_contents` | an independent inspection (a); the carrier's scanned weight, compared deterministically with the expected weight of the complete package from the signed spec or producer data, outside the scale tolerance (a, by the derivation rule); equal declared and scanned weights say nothing about a part lighter than the tolerance |
| Step 1: condition, damage, used | `item_condition` | an independent inspection (a); for "used" also the registry's `unit_sale_history` of a serial bound to the order (a) |
| Step 1: price and fees charged | `amount_charged` against `offer_terms` | the rail record (a) against the countersigned snapshot (b, against the merchant) |
| Step 2: injection, deception, added lines | `offer_terms`; `agent_actions` | the countersigned snapshot, feed record or cart with `added_by` (b, against the merchant); causation from the action log (c) |
| Step 3: a term broken | `user_instruction`; `agent_actions` | the signed Mandate, its confirmed text and the confirmed clarifications, co-signed by the agent provider (b, against the provider for what was asked); the anchored action log (b, against the provider for what its agent did) |
| Step 3b: a requirement stated, not captured | `user_instruction` | the conversation record committed by `conversation_hash` (b, against the agent provider) |
| Step 4: denial of a non-conformity claim | the contested fact of Step 1 | as for Step 1: a record with independent authority for the contested fact; a carrier "delivered" status never answers a claim about content |

**What the experiment shows, and what it does not.** In Phase 3 (A8.7) claude-fable-5-1 resisted
the attacker for all 10 attempts on the two case-sides where a manufacturer-registry record (D06)
or a carrier weight gap (D05) contradicted the attacker's account. grok-4.7 was fooled on all 14
case-sides, those two included, with the same records in its Package, and the payloads that failed
against fable fooled grok in one shot. So certain corroborating records resisted certain attacks
against one arbiter. No experiment removed or added records under control, so no record type has
been shown to be necessary or sufficient, and the records' presence did not stop the second
arbiter. That last point is why the gate exists: it makes a record's support a precondition the
engine checks, instead of something a judge may or may not weigh.

**Measured (Phase 3b; `results/PHASE3B_PROVENANCE.md`, Amendment 14; pre-registered, E3, simulated,
one decision per payload, 14 case-sides; described in the v0.2 binary terms the gate used).** A
first gate checked the tier and the type of the cited record: a fault refund (AG3, AG4, AG1-M,
AG1-P) needed a relevant independent record for its decisive finding, and a denial of a
non-conformity claim needed one for the conformity finding. On the Phase 3 final payloads,
comparing each Phase 3b decision before and after the gate (same call, same prompt; descriptive),
the gate cut the end-to-end arbiter's
attack success from 11 of 14 case-sides to 1 of 14 (claude-fable-5-1; exact McNemar p = 0.002) and
from 12 of 14 to 1 of 14 (grok-4.7; p = 0.001); recomputed from the hybrid's logged typed Findings,
from 7 of 14 to 3 of 14. H10 as pre-registered (12 of 14 to 1 of 14, p = 0.001) stays as computed
but is confounded: its "without" column is the selected successful Phase 3 attempt, its "with"
column a fresh call with a changed prompt. Three findings qualify that and motivate the three rules
below. (1) Most of the end-to-end effect was a format failure: the gate read only true or false
values, both arbiters mostly wrote free text, and the rejections split format / provenance /
contradiction as 10 / 2 / 0 (fable) and 13 / 0 / 0 (grok) on the attacks (the gate read no content,
so it had no contradiction rejections by construction); with the values read by a post-hoc keyword
rule (exploratory) 6 and 5 of 14 attacks would have passed. (2) Every attack that
passed cited an independent record of a relevant type that does not support the finding: equal
declared and scanned carrier weights for a missing accessory, a registry entry "first sold new (this
order)" for a used unit, a return inspection reporting "all accessories present" for a missing one,
a carrier "delivered" status for a missing-item claim. (3) On the baseline Phase 2 workload (50
valid cases, 24 of them with a scripted adversary) the gate sent 24 to review (48% [35, 61]),
deciding 25 of the other 26 correctly; it reviewed 22 of 31 true claimants (the buyer is owed a
refund) against 2 of 19 unfounded claims, so the wait fell on buyers whose claims were true.
Abstention below 0.7 alone, on the same calls, reviewed 3 of 50 and let 8 of 14 attacks through.
The gate as run was also weaker than its amendment: it accepted any relevant independent record for
a denial (no delivery-side requirement), any conformity attribute rather than the contested one,
and did not check that a cited path exists. A gate v2 written after Audit 1 with these outputs in
view (exact paths, typed findings, content readers, support for every decisive finding and denied
allegation) lets 0 of 14 (fable), 0 of 14 (grok) and 0 of 67 hybrid attempts through on the stored
outputs, and reviews 26 of 50 baseline cases (fable) and 110 of 153 hybrid runs; it is exploratory,
a design and not a measured result, and 31 of its baseline passes rest on content it has no reader
for (`results/PHASE3B_PROVENANCE.md`, post-audit headline and Section 10). Not run in Phase 3b (Deviation 6):
the gate-aware attacker, the confidence-aware attacker and new case-sides; 33 of 51 baseline cases
for grok. **Confirmatory (amendment C1, `results/CONFIRMATORY_C1.md`):** frozen before its first call,
gate v3 cut best-of-5 attack success at E3 by a gate-aware attacker from another model family, on 14
fresh case-sides with a claude-opus-5-5 judge, from 11 of 14 to 0 of 14 (exact McNemar one-sided
p = 0.00049), and sent 34 of 51 baseline cases to review (20 of 31 true claimants; correct decided
outcomes 48 to 16 of 51), mostly because no reader checks mandate terms beyond the hard limits, page
text or the action log. **Replicated (amendment C2, `results/CONFIRMATORY_C2.md`):** the same frozen code,
judge and attacker on 28 further fresh case-sides gave 25 of 28 gate off against 0 of 28 gate on (exact
McNemar one-sided p = 3.0e-8); pooled with C1, 36 of 42 against 0 of 42 (descriptive).

**Machine-checkable citations (normative).** Every Finding MUST state its value in the closed
vocabulary of its type and MUST cite what it rests on in the structured `cited_evidence` field
(A7.4): for each item, the evidence item's id, the path of the field relied on (a JSON Pointer into
that item), its hash, record type and provenance description, and the attribute the citation speaks to. Free
text is never a citation, and a rationale is never parsed for one. A Finding with no structured
citation, or with a value outside its type's vocabulary, MUST NOT ground a decision; if it was
decisive, the case goes to `review` with `provenance_gate_reason: uncited`. Uncited reviews are
counted and published apart from provenance reviews, so a format failure is never reported as a
safety result.

**Content check (normative).** The gate checks what the cited record says, not only what kind of
record it is or who signed it. For every liability-moving Finding:
- every cited path MUST resolve to a field present in the Package (else `path_unresolved`);
- the citation MUST speak to the attribute the claim contests, not to any attribute;
- where the cited record is structured (weights, serials, registry results, inspection results,
  carrier events, snapshot values), the engine compares it deterministically with the Finding's value
  and records the result in `cited_evidence[].support` (`supports`, `contradicts` or `silent`); a
  Finding is corroborated only if at least one citation that meets a corroboration test `supports`
  it and none `contradicts` it (else `record_does_not_support`). Equal declared and scanned weights do not
  support a missing item; a registry entry for this order's own new unit does not support "used"; an
  inspection that reports all accessories present does not support "missing";
- where the cited record is free text, whether it supports the Finding is itself a Finding, with its
  own structured citation, subject to the same rules;
- a denial of a non-conformity claim cites a record with independent authority for the contested
  fact (test (a): a registry binding, a weight comparison, an independent inspection); a carrier
  "delivered" status has authority for handover only and never answers a claim about content, and a
  certified capture has authority for image integrity only (else `no_authority_for_fact`).

**Fairness cost of the gate (normative).** A gate that escalates every fault refund it cannot
corroborate moves the wait onto claimants, and those are mostly buyers whose claims are true
(Phase 3b, baseline Phase 2 workload: 22 of the 24 reviews fell on true claimants, so 22 of 31
true claimants waited against 2 of 19 unfounded claims). ABS
therefore specifies the delivery-side records that can carry independent authority for what
arrived, as Delivery Record items: the carrier's declared and scanned weight and scan events; a
registry binding of the shipped unit's serial to the order at dispatch; and a return or on-request
inspection by an inspector without a stake (A15.1 item 19). Device-signed capture with a C2PA
manifest from a certified capture app whose keys the capturing party does not control proves image
integrity only: the image was not altered after capture on that device at that time. A staged photo
of a real unit passes it, so it corroborates a content finding only together with a record that ties
the photographed unit to the order (a serial in the image matching a registry binding at dispatch).
Every node MUST
publish its review rate by liable party as finally decided and by reason code, beside its
attack-success figures (A1.5, A7.7). A review burden that falls mainly on one party's honest claims
is a defect to fix, not a safety margin.

**Tiered burden of proof for merchant-performance claims (ABS-V1, normative).** A claim of
non-delivery or non-conformity (AG3), and nothing else, that no record with independent authority
for the contested fact decides (none supports the merchant under test (a), none supports the
buyer's claim) is decided by the order value, not by a reading of party submissions:

- **Low-value tier.** Where the order value is at or below the programme's published threshold for
  its currency and the buyer is under the cap, the merchant that answered only with records it wrote
  itself (its packing record, its photos, its listing, its statements) MUST refund (AG3). The
  contested fact is not found: the loss follows the burden, as card-scheme dispute practice asks a
  merchant for compelling evidence. The Decision records `confirmation_route: low_value_burden` and
  `provenance_gate: not_applicable`.
- **Abuse guard.** A buyer identity receives at most the published cap of ABS-V1 refunds in the
  published window; the payer's PSP, which knows the buyer's identity, keeps the count. Above the
  cap the claim takes the high-value path. The guard is modelled on the use of prior undisputed
  history in Visa Compelling Evidence 3.0 (A10.1); it is a design proposal, not a scheme rule.
- **High-value tier.** Above the threshold, in a currency with no published threshold, above the
  cap, or where the order value or the count is not available, the case goes to human review or to
  an independent inspection request, as for any Finding the gate cannot corroborate.
- **Scope.** ABS-V1 never overrides Step 0 (authorisation is decided first) and never applies to an
  agent-instruction or capture dispute (AG1-P, AG1-C, AG2), to Step 2 (AG4, AG4-D, AG1-M), or to a
  claim that also alleges one of them. A merchant with a record that has independent authority for
  the contested fact wins on the evidence, and a buyer with one wins under AG3, as without the rule.
  It does not displace the other defaults: a merchant that cannot produce a record it had to keep,
  or the carrier's handover record for a non-delivery claim, loses at any value (ABS-E1m, A4.5), and
  a not-as-described claim with no content evidence from the buyer fails at any value (ABS-E2). At or
  below the threshold it decides the conflict between the parties' own records that ABS-H1 would
  send to review.
- **Programme parameters (published).** The threshold per currency (on the order value, inclusive;
  default EUR 100), the cap (default 3) and the window (default 12 months) are programme parameters,
  published with the rulebook version each Decision records (`rulebook_version`) and disclosed to
  participants before purchase. The defaults are a design proposal, not calibrated on loss data
  (A15.1 item 22).
- **Residual risk.** The expected loss from fabricated claims that ABS-V1 pays is bounded by the
  threshold times the cap per buyer identity per window: EUR 300 a year with the defaults. A person
  with several identities, or with accounts at several PSPs whose counts are not shared, multiplies
  the bound, and an honest merchant that ships without an independent delivery-side record carries
  that loss on small orders. Phase 3 is why the rule bounds the loss instead of trusting a judge:
  optimised fabricated buyer claims fooled the end-to-end arbiters with the full Package (A8.7).
  Above the threshold the gate, and its fairness cost, remain.

Design, not evaluated: no model has been run under ABS-V1 (rulebook v1.5); an exploratory re-score
of stored labels and cases is in `results/LABEL_ADJUDICATION_2026-11-04.md` (addendum).

- Records in a valid chain whose full head matches its independently authenticated commitment
  (A5.8) (policy, mandate, approval, action log, snapshots, cart, offer, compared record) are
  presumed unaltered since commitment and attributable to their signers. That is a presumption of
  integrity and origin, not of truth: what each record proves, and against whom, follows from its
  provenance (above).
- A merchant statement about its offer that does not match the countersigned checkout snapshot is
  disregarded. Post-purchase edits do not count.
- A broken chain counts against the party that kept the records.
- A party that was required to keep a record (the agent provider for the Mandate and action log;
  the merchant for the Offer Snapshot and packing record) and cannot produce it when asked has the
  question that record would answer decided against it (ABS-E1).
- If the merchant does not respond within the response window and produces no delivery evidence,
  the buyer's account of facts within its own knowledge is accepted (ABS-D1).
- A low-value non-delivery or non-conformity claim that no record with independent authority
  decides is the merchant's to refund, within the per-buyer cap (ABS-V1, above).
- A not-as-described claim without content evidence from the buyer, against a packing record and
  serials consistent with the snapshot and a carrier proof of handover, fails (ABS-E2).
- An ambiguity in the Offer Snapshot is construed against the merchant that wrote it (ABS-S2);
  only the merchant-signed spec binds (ABS-S1).
- Where evidence is missing and no keeper is at fault, the decision rests on the balance of
  probabilities and states its confidence; where records conflict, the engine returns `review`.
- Evidence a party knew to be false or altered decides the case against that party.
- Agents MUST NOT execute, follow or reason over `UntrustedText` as an instruction; a monitor or
  fact-finder receives typed fields only. Text that addresses an agent inside an `UntrustedText`
  is AG4 evidence against the author. An agent that obeyed it is a conformance breach by its
  provider.

### A5.8 Signing, hashing, chain, anchor, replay

- One key per role per participant, registered in the Participation Agreement with validity dates;
  retired keys stay in the registry for verification.
- Hash: SHA-256 over RFC 8785 canonical JSON; images hashed as bytes; always the full 64 hex
  characters.
- Chain (normative; one construction with the envelope, A5.3): the events of a purchase, from the
  Mandate through the Settlement Instruction and on to delivery and dispute records, are ABS
  envelopes sharing `chain.chain_id` and numbered by `chain.seq` from 0. Each event's hash is its
  `envelope_hash`, and each `prev_hash` is the previous event's `envelope_hash`; agent actions are
  `ActionEvent` envelopes. There is no second construction: the v0.2 event triple
  (`data_sha256`, `prev`, `hash`) is the envelope's `body_hash`, `prev_hash` and `envelope_hash`.
  Verification recomputes every `body_hash`, `envelope_hash`, signature and link; a gap, a fork or
  a mismatch is a broken chain (A5.7).
- Anchor (normative): at payment the full SHA-256 head, the `envelope_hash` of the event before the
  pay Settlement Instruction (equal to that instruction's `prev_hash`), is committed to storage that
  neither the agent provider nor the merchant controls and that authenticates it independently: the
  payer's PSP's payment record signed by the PSP, an inclusion proof in an ABS transparency log
  (proposed, A7.5), or a qualified electronic time stamp (eIDAS Art 41(2)). The Settlement
  Instruction records it in `abs_binding.anchor_commitment` (A6.2). The rail reference carries only
  a **locator**, `ABS:<purchase_id>:<first 16 hex of the head>`, where the rail has a field (A6.3),
  so a verifier can find and cross-check the commitment. The locator is not the commitment: 16 hex
  characters are 64 bits, and a party that builds the chain can prepare two different chains with
  the same prefix with about 2^32 work, so a match on the prefix proves nothing. Verification
  compares all 64 hex characters of the head with the authenticated commitment.
- Replay: `nonce` in the Mandate; `purchase_hash` plus `instruction_seq` single use at the PSP;
  order acceptance binds `merchant_order_id` to checkout snapshot ids; a snapshot captured after
  the offer's `valid_until` is a feed mismatch and a step-up signal.
- Users sign with a key in their bank app, wallet or passkey. Where the user has no key, the agent
  provider MAY sign on the user's behalf after strong authentication, MUST record the
  authentication reference and `assurance`, and accepts liability for the binding. Under the EU
  payment rules a Mandate with a maximum amount and an open payee set is consent capture, not
  payment authentication: strong customer authentication for a remote payment must dynamically
  link the authentication to a specific amount and a specific payee (PSD2 Art 97(2); SCA RTS Art
  5(1)). Only a per-purchase approval through the payer's PSP, or an exemption the PSP applies,
  satisfies SCA for the payment itself (A12.1). EBA Q&A 2019_4664 concerns direct-debit mandates
  set up without the payer's PSP; the merchant-initiated-transaction Q&As are 2018_4031 and
  2018_4131, whose condition (no specific action of the payer) sits badly with an agent buying for
  the payer, so treating autonomous agent purchases as merchant-initiated is doubtful. Both Q&As
  are non-binding.

### A5.9 Data minimisation, retention, transparency

- The Package carries `user_ref`, not a name; `delivery_address_hash`, not an address;
  `intent_hash`, not the intent. Fulfilment data goes to the merchant through its own channel.
- Intent text, full action log and image bytes stay with the agent provider and are disclosed to
  the Decision Center and the counterparty only in a case, at the level offered.
- Retention: the parties keep the Evidence Package and Dispute Case records until the decision and
  appeal window close plus the statutory limitation period, and in any case until the later of 540
  days from the transaction processing date (the ceiling of the card schemes' dispute windows) and
  13 months after `delivered_at`; erasure may be refused under GDPR Art 17(3)(e) while the record is
  needed for the establishment, exercise or defence of a legal claim, and the period is justified
  under Art 5(1)(e); access requests are served with the evidence bundle minus third-party data;
  hashes MAY be kept longer. National accounting rules are outside ABS.
- No card data enters the agent context: agents pay with network tokens or mandate-bound
  credentials only; a merchant checkout that requests card data from an agent breaches its
  Participation Agreement.
- Before a purchase the buyer is shown: the rulebook summary (what can be disputed, how, within
  what time, who decides, the four steps in one sentence each); the mandate as enforced; the
  offer's binding attributes, total including tax and fees, delivery and returns; the provider's
  Step 3 cap if any; what evidence is kept and for how long; who the arbiter is; that statutory
  rights are unaffected; that an AI agent is acting and which provider operates it. The merchant
  is shown that the buyer is an agent, the provider and level, the rulebook version, the snapshots
  it is asked to countersign, and that a step-up or monitor may still decline. Showing both sides
  the rulebook is measured to matter: in the Phase 2 tier-1 simulation, end-to-end fairness rose
  from 78% to 96% when both negotiating agents saw the rulebook (p = 0.012, secondary); tier-1
  settlement rose from 25% to 37% (H4, not significant, p = 0.18). Neither agent filed a false
  claim or denied a true one when its principal asked it to (0 of 7, 0 of 13), a result about
  those two models with those instructions.

---

## A6. Settlement mapping onto existing card and ISO 20022 flows

### A6.1 Principle

ABS never moves money. A Decision becomes a Settlement Instruction; the instruction names an
existing rail mechanism. On card rails the mechanism is the merchant refund, the scheme dispute
lifecycle raised by the issuer at the cardholder's request (first dispute, response,
pre-arbitration, arbitration, in scheme-neutral terms) and the acquirer's reserve; on
account-to-account rails it is a new credit transfer by the liable party and, where an acquiring
PSP is the payee, that PSP's payout hold; no scheme message reverses a credit transfer against a
refusing merchant. The Participation Agreement's collection right (direct debit mandate,
reserve, bank guarantee or netting, with the licensed PSP or acquirer as creditor in its own
licence, or the buyer directly) backs amounts a participant owes and does not pay; the programme
and the arbiter never collect for onward payment.

Four rules make settlement complete and lawful:

- **Every rail family has an execution, and none promises a reversal that does not exist.** Card:
  merchant refund; where the merchant does not refund, the cardholder may ask the issuer to raise a
  dispute within the scheme's deadlines (first dispute, response, pre-arbitration, arbitration in
  scheme-neutral terms); the Decision Center cannot raise one and supplies the Decision and Package
  as evidence. Wallet: operator ledger reversal or buyer-protection claim (proprietary). A2A push
  (SEPA credit transfer and SCT Inst, Faster Payments, UPI, Pix, open-banking payment initiation): a
  new credit transfer by the liable party (pain.001 initiation, pacs.008 interbank). There is **no**
  scheme message that reverses a credit transfer against a refusing merchant: a SEPA recall
  (camt.056) is started only by the payer's PSP and only for duplicate sending, technical error or
  fraud, a customer-reason request for recall depends on the beneficiary's consent (answered by
  pacs.004 if returned or camt.029 if refused), the return must not be used once the beneficiary
  has been credited and wishes to return funds, and SCT Inst has no return at all (EPC rulebooks,
  per Audit 2). Against a refusing merchant on these rails the only tool is ABS's **contractual
  collection right** (below). Buy-now-pay-later: refund through the provider, which reduces the loan
  and returns paid instalments. Marketplace: the platform reverses the held split. Stored value:
  re-credit. Stablecoin: on-chain return transfer. Public authority: the authority's own refund
  process.
- **Payout hold, where the law allows one.** ABS holds no funds. On card rails the acquirer's
  delayed funding and reserve stand as they do today. On account-to-account rails, funds credited
  to a merchant's own payment account must be at the merchant's disposal immediately (PSD2 Art
  87(2), which businesses cannot derogate from under Art 61(1)) and instant transfers within ten
  seconds (Instant Payments Regulation, Art 5a(4)(c) of Regulation 260/2012 as amended), so a
  hold on such funds is not available. An A2A hold works only in an **acquiring or collection
  model**: the merchant's PSP is the payee of the buyer's transfer (acquiring of payment
  transactions, PSD2 Annex I point 5), and pays the merchant later under its acquiring contract,
  with the ABS release condition in that contract. For merchants in probation (first 90 days or
  below the trust threshold) and for prepaid orders with delivery more than 14 days out, that
  acquiring PSP holds the payout until the delivery evidence confirms delivery plus a 7-day
  inspection window; a rolling reserve applies under the acquiring contract. Where the merchant is
  paid directly to its own account, no hold exists and the buyer's protection is the collection
  right and the merchant's trust level.
- **Alongside the rail, never instead.** ABS never requires a buyer to waive or assign a card
  dispute or any rail right (a merchant may not require a cardholder to waive the right to dispute,
  per Visa's published rules; a pre-dispute term that hinders a consumer's remedies is presumptively
  unfair under the EU unfair-terms rules). A Decision refund is set off against any later rail
  recovery so the buyer is made whole once; the Decision is offered as evidence in a later rail
  dispute; the deadline guard (A3.3) protects the scheme deadline.
- **Enforcement by the collection right.** A Settlement Instruction unpaid after 10 days is
  collected under the Participation Agreement by the licensed PSP or acquirer acting as creditor in
  its own licence (direct debit mandate, reserve, netting), or is owed to the buyer directly; the
  programme and the arbiter never collect for onward payment. Failing collection, the merchant is
  suspended from the Register and the buyer keeps the rail's own process and the courts. No
  programme guarantee is promised here: a fee-funded promise to pay buyers for merchant default or
  forgery is presumptively insurance or suretyship and needs a legal opinion on its form before it
  can appear in Part A (B1.2).

The honest residual: in the simulation (528 scenarios), 26 funds-moving instructions could not be
executed against the liable party because the merchant was gone on an irrevocable rail with no
payee-side hold, and 9 more could be reached only through the contractual collection right, against
334 executable, of 369 funds-moving instructions (v0.1 as written: 224 executable, 4
collection-only, 40 infeasible, of 268). For those, Part
A offers the collection right and the rail's own routes; on UK Faster Payments the APP reimbursement
regime may apply to the scam subset only where the consumer was deceived (coverage of a payment
where only the buying agent was deceived is unverified); a guarantee is a Part B design.

### A6.2 Settlement Instruction

Rail-agnostic body, one rail binding. Single use: `purchase_hash` plus `instruction_seq`. Signed
by: agent provider or its PSP; PSP appends the rail result.

```json
{
  "$id": "urn:abs:schema:0.3:settlement-instruction",
  "type": "object",
  "required": ["settlement_id", "purchase_id", "purchase_hash", "instruction_seq", "direction", "amount", "payer", "payee", "rail", "abs_binding", "timing"],
  "additionalProperties": false,
  "properties": {
    "settlement_id": {"type": "string"}, "purchase_id": {"type": "string"}, "purchase_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"},
    "instruction_seq": {"type": "integer", "minimum": 1},
    "direction": {"enum": ["pay", "refund", "collect", "payout_release", "payout_return", "new_credit"]},
    "decision_id": {"type": "string", "description": "required for refund after decision, collect, payout_return, new_credit"},
    "amount": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"},
    "payer": {"type": "object", "required": ["party_role", "instrument_ref"], "properties": {"party_role": {"enum": ["user", "merchant", "agent_provider", "psp"]}, "instrument_ref": {"type": "string", "description": "token or account reference; never a PAN or full IBAN in agent context; the arbiter is never a payer"}}},
    "payee": {"type": "object", "required": ["party_role", "account_ref"], "properties": {"party_role": {"enum": ["user", "merchant", "agent_provider", "psp"]}, "account_ref": {"type": "string", "description": "the arbiter is never a payee"}}},
    "rail": {"type": "object", "required": ["type"], "properties": {"type": {"enum": ["card", "a2a_instant", "a2a_batch", "wallet", "stablecoin", "other"]}, "network": {"type": "string"}, "scheme_reference": {"type": "string"}}},
    "timing": {"type": "object", "required": ["mode"],
               "properties": {"mode": {"enum": ["immediate", "payout_hold_until_delivery", "rolling_reserve"]},
                              "held_by": {"enum": ["acquirer", "acquiring_psp_as_payee", "wallet_provider", "custodian"], "description": "a licensed entity that is itself the payee of the buyer's payment (card acquirer; A2A acquiring or collection PSP); ABS holds nothing; funds credited to the merchant's own account cannot be held"},
                              "release_condition": {"enum": ["delivery_confirmed", "conformity_window_elapsed", "decision"]},
                              "reserve_pct": {"type": "number"}, "reserve_days": {"type": "integer"}}},
    "abs_binding": {"type": "object", "required": ["reference_field", "reference_value", "anchor_commitment"], "additionalProperties": false,
                    "properties": {"reference_field": {"type": "string", "description": "the rail field that carries the ABS locator"},
                                   "reference_value": {"type": "string", "maxLength": 140, "pattern": "^ABS:[A-Za-z0-9:._-]{1,100}:[0-9a-f]{16}$", "description": "locator ABS:<purchase_id>:<first 16 hex of anchor_commitment.head>, carried in unstructured remittance information (max 140 characters); it identifies the commitment and never substitutes for it (A5.8)"},
                                   "end_to_end_token": {"type": "string", "maxLength": 35, "pattern": "^ABS[0-9A-Z]{1,32}$", "description": "a token of at most 35 characters for EndToEndId (Max35Text), which cannot hold a URN; resolvable to purchase_id by the agent provider"},
                                   "anchor_commitment": {"type": "object", "required": ["head", "store"], "additionalProperties": false,
                                                         "properties": {"head": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash", "description": "the full SHA-256 chain head anchored at payment: for direction pay, equal to this instruction's prev_hash; later instructions repeat the head anchored at payment"},
                                                                        "store": {"enum": ["psp_record", "transparency_log", "qualified_timestamp"], "description": "independently authenticated storage that neither the agent provider nor the merchant controls (A5.8); transparency_log is proposed (A7.5)"},
                                                                        "store_ref": {"type": "string", "description": "the PSP's payment record id, the log id and index, or the time-stamp token id"},
                                                                        "committed_at": {"type": "string", "format": "date-time"},
                                                                        "attestation": {"type": "string", "description": "appended by the store: a JWS by the PSP over {head, committed_at, store_ref}, the signed tree head with inclusion proof, or the qualified time-stamp token; base64url"}}},
                                   "mandate_digest": {"type": "object", "required": ["hash", "carried_in"], "additionalProperties": false,
                                                      "description": "PROPOSED (A4.5; B6 Stage 1): lets the payer's issuer or PSP find and verify the user-signed Mandate at dispute intake without the chain; never a substitute for anchor_commitment; no scheme or rail field is agreed for it",
                                                      "properties": {"hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash", "description": "the full envelope_hash of the Mandate (A5.3), or of the mandate credential that commits to it (A5.2.1)"},
                                                                     "snapshot_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash", "description": "envelope_hash of the merchant-countersigned Offer Snapshot the payment is for"},
                                                                     "carried_in": {"enum": ["not_carried", "psp_record", "rail_additional_data", "agent_token_data", "mandate_credential"], "description": "where the digest travels with the payment; not_carried until a scheme or rail defines a field"}}},
                                   "agent_indicator": {"type": "boolean"}}},
    "card_binding": {"type": "object", "properties": {"network_token_ref": {"type": "string"}, "agent_token_ref": {"type": "string"}, "authentication_ref": {"type": "string", "description": "EMV 3-D Secure or equivalent transaction reference"},
                     "authorisation_code": {"type": "string"}, "retrieval_reference": {"type": "string"},
                     "dispute_stage": {"enum": ["none", "merchant_refund", "first_dispute", "response", "pre_arbitration", "arbitration"], "description": "scheme-neutral; mapped per scheme (Visa: Dispute, Dispute Response; Mastercard: First Chargeback, Second Presentment); raised by the issuer at the cardholder's request, never by ABS"},
                     "dispute_category": {"enum": ["fraud", "authorisation", "processing_error", "consumer_dispute"]}, "authentication_version": {"type": "string", "description": "e.g. EMV 3-D Secure 2.3.1"}}},
    "a2a_binding": {"type": "object", "properties": {"end_to_end_id": {"type": "string"}, "transaction_id": {"type": "string"},
                    "remittance_information": {"type": "string", "maxLength": 140}, "structured_reference": {"type": "string", "description": "ISO 11649 creditor reference where used"},
                    "payee_name_check": {"enum": ["match", "close_match", "no_match", "verification_not_possible", "not_performed"], "description": "EPC Verification of Payee outcomes: Match, No Match, Close Match, Verification check not possible"},
                    "close_match_name": {"type": "string", "description": "the payee name the scheme returned on a close match"},
                    "message": {"enum": ["pain.001", "pacs.008", "other"], "description": "the ISO 20022 message that carries this instruction: a payment or a refund by the liable party is a new credit transfer. Recall and return messages (camt.056, pacs.004, camt.029) are the payer PSP's tools for duplicate, technical error or fraud and are outside ABS; camt.027 and camt.087 are interbank fund inquiries, not goods disputes"}}},
    "result": {"type": "object", "properties": {"status": {"enum": ["authorised", "settled", "declined", "failed", "reversed", "held", "released", "returned"]},
               "rail_timestamp": {"type": "string", "format": "date-time"}, "rail_reference": {"type": "string"}, "decline_reason": {"type": "string"}}}
  }
}
```

### A6.3 Mapping table

Message and stage names are the standards' own; their current scope and the exact fields are
verified in the alignment matrix (A10.3) and `LANDSCAPE.md`, and marked there where unverified.

| ABS event | Card rail | Account-to-account rail (ISO 20022) | Wallet / stablecoin |
|---|---|---|---|
| Pay | Authorisation and capture with an agent-capable network token and the authentication reference (EMV 3-D Secure 2.3.1 where used); ABS reference in a merchant or additional data field where the network allows it | Customer credit transfer (pain.001 initiation, pacs.008 interbank) with the ABS reference in unstructured remittance information (140 characters) and a 35-character token in EndToEndId; Verification of Payee before the transfer (euro area since 9 Oct 2025) | Transfer with memo |
| Payout hold on an unproven merchant (Part B1) | Acquirer delayed funding or reserve, as acquirers do today | Only where the merchant is paid through an acquiring or collection PSP that is the payee of the buyer's transfer; that PSP pays the merchant later under the acquiring contract, which states the ABS release condition. Funds credited to the merchant's own account are at its disposal immediately (PSD2 Art 87(2); IPR ten-second rule) and cannot be held | Hold on seller balance; custodial hold (custody rules per rail, unverified) |
| Refund by merchant (AG3, AG4, AG1-M; tier 1 settlement) | Merchant-initiated refund to the original credential | New credit transfer from merchant to buyer (pain.001 to pacs.008) with the ABS case id in remittance; the obligation comes from participation | Reversal from balance |
| Merchant does not pay a Decision | The cardholder may ask the issuer to raise a dispute in the fitting category (consumer dispute: not received, not as described; processing error: incorrect amount) within the scheme deadlines; the issuer, not ABS, raises it; the ABS Decision and Receipt are evidence; in parallel the collection right runs against the merchant | No scheme message reverses the transfer against a refusing merchant (recall is the payer PSP's tool for duplicate, error or fraud; a customer-reason recall needs the merchant's consent; SCT Inst has no return). The collection right, operated by the licensed PSP or acquirer as creditor, is the remedy | Collection right |
| Refund by agent provider or PSP (AG1-P) | No card message lets a third party reverse the original purchase. The provider, as a sponsored originator through a licensed acquirer, can push a new credit to the card (Visa Direct original credit transaction with the funds-disbursement or merchant-initiated-refund identifiers; Mastercard Send disbursements), or pays by credit transfer to the buyer's account | Provider pushes a credit transfer to the buyer (pain.001 to pacs.008) | Provider transfer |
| Withdrawal (AG2, AG5 with the right available) | Merchant refund within 14 days by the same means, on receipt of the goods or of proof of dispatch, whichever is earlier (CRD Arts 13(1), 13(3)); routed through the Art 11a withdrawal function | Merchant credit transfer on the same terms | Reversal from balance |
| Collect a decided amount a participant did not pay | Direct debit under the collection mandate, acquirer reserve or netting, with the licensed PSP or acquirer as creditor in its own licence, or the buyer as creditor directly; never the programme or the arbiter | The same; no interbank dispute message carries a goods dispute | Balance debit |

| Refund through a BNPL provider, wallet, stored-value programme or stablecoin | Not applicable | Not applicable | BNPL: provider API reduces the loan and returns instalments by credit transfer; wallet: operator reversal or buyer-protection claim; stored value: re-credit by the programme (a third-party refund cannot return value to a gift card and goes by credit transfer); stablecoin: on-chain return transfer, no refund primitive in x402 |

The decision does not depend on the rail; only the execution does. The experiment's rail-flip
analysis (12 cases at E3 with the rail flipped) measures exactly this invariance.

**Where no existing message exists.** The simulation found outcomes with no standard message or
mechanism; ABS states them as extension points rather than inventing a message: a refund to a
cardholder by a third party (the agent provider), which no card message carries and which goes by
credit transfer or a scheme push-to-card credit where offered; merchant and third-party refunds
through BNPL, wallet and stored-value programmes (proprietary APIs); x402 and stablecoin refunds
(on-chain transfers, no protocol primitive); payout-hold release keyed to a Delivery Record;
programme guarantee payout; and administrative refunds by public authorities. Each is listed in
A10.3.

### A6.4 Participation Agreement (the enforcement contract)

Acceptance of the rulebook by a merchant or an agent provider, countersigned by the arbiter, which
also runs the registry. Rules bind from `accepted_at`; a participant cannot opt out of a single
dispute. Signed by: participant, arbiter.

```json
{
  "$id": "urn:abs:schema:0.3:participation-agreement",
  "type": "object",
  "required": ["participant", "legal_entity", "rulebook_version", "rulebook_hash", "accepted_at", "conformance_level", "keys", "dispute_contact", "settlement", "collection_right", "binding_effect"],
  "additionalProperties": false,
  "properties": {
    "participant": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef"},
    "legal_entity": {"type": "object", "required": ["name", "registration_number", "country"],
                     "properties": {"name": {"type": "string"}, "registration_number": {"type": "string"}, "lei": {"type": "string", "description": "ISO 17442 legal entity identifier where held"},
                                    "country": {"type": "string", "pattern": "^[A-Z]{2}$"}, "vat_number": {"type": "string"}, "address": {"type": "string"}}},
    "rulebook_version": {"type": "string"}, "rulebook_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"},
    "accepted_at": {"type": "string", "format": "date-time"}, "valid_until": {"type": "string", "format": "date-time"},
    "conformance_level": {"enum": ["ABS-Basic", "ABS-Full"]},
    "certification": {"type": "object", "properties": {"certifier": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef"}, "attestation_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}, "valid_until": {"type": "string", "format": "date-time"}}},
    "keys": {"type": "array", "minItems": 1, "items": {"type": "object", "required": ["kid", "alg", "public_key", "valid_from"],
             "properties": {"kid": {"type": "string"}, "alg": {"enum": ["Ed25519", "ES256", "EdDSA"], "description": "Ed25519 or ES256 for new keys (RFC 9864); EdDSA only for verifying legacy objects"}, "public_key": {"type": "string", "description": "JWK"}, "valid_from": {"type": "string", "format": "date-time"}, "valid_until": {"type": "string", "format": "date-time"}}}},
    "offer_feed_url": {"type": "string", "format": "uri"}, "agent_ids": {"type": "array", "items": {"type": "string"}},
    "dispute_contact": {"type": "object", "required": ["endpoint"], "properties": {"endpoint": {"type": "string", "format": "uri"}, "email": {"type": "string"}, "availability_commitment": {"type": "string"}}},
    "settlement": {"type": "object", "required": ["rails"], "properties": {"rails": {"type": "array", "minItems": 1, "items": {"type": "object", "required": ["rail", "account_ref"],
                   "properties": {"rail": {"enum": ["card", "a2a_instant", "a2a_batch", "wallet", "stablecoin", "other"]}, "network": {"type": "string"}, "account_ref": {"type": "string"}, "psp": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef"}}}}}},
    "collection_right": {"type": "object", "required": ["method", "creditor"],
                         "properties": {"method": {"enum": ["direct_debit_mandate", "reserve_balance", "bank_guarantee", "netting"]}, "creditor": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef", "description": "the licensed PSP or acquirer collecting in its own licence, or the buyer directly; the programme and the arbiter never collect for onward payment"},
                                        "reference": {"type": "string"}, "cap": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}}},
    "payment_initiation": {"type": "object", "properties": {"mode": {"enum": ["card_only", "own_pisp_authorisation", "licensed_pisp_partner", "own_pi_or_emi_licence"]}, "licence_reference": {"type": "string"}},
                           "description": "agent providers: an agent that initiates payments from the user's account needs payment-initiation authorisation or a licensed partner (PSD2 Annex I point 7); one that holds user funds needs a payment or e-money licence"},
    "liability_cap": {"type": "object", "properties": {"per_purchase": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}, "insured": {"type": "boolean"}}, "description": "agent providers: the Step 3 cap disclosed to users"},
    "rail_enforcement": {"type": "array", "items": {"type": "object", "required": ["psp", "controls"],
                         "properties": {"psp": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef"}, "controls": {"type": "array", "items": {"type": "string"}}, "acknowledged_at": {"type": "string", "format": "date-time"}}},
                         "description": "controls a PSP also enforces on the rail; the agent provider stays liable to the buyer and has recourse against the PSP (A4.1 Step 3, ABS-9)"},
    "responding_party_rules": {"type": "array", "items": {"type": "object", "required": ["scope", "party"], "properties": {"scope": {"enum": ["seller_goods_and_conduct", "platform_feed", "platform_fees", "catalogue_merges", "hosting_duties", "guarantor_of_last_resort"]}, "party": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef"}}},
                               "description": "marketplaces: who answers for each kind of line (ABS-1.5b)"},
    "binding_effect": {"type": "object", "required": ["decisions_bind_participant_by_contract", "consumer_rights_unaffected"],
                       "properties": {"decisions_bind_participant_by_contract": {"const": true}, "consumer_rights_unaffected": {"const": true}, "governing_law": {"type": "string"}, "forum": {"type": "string"}}},
    "qualification": {"type": "object", "description": "merchants: Trust Authority entry record (Part B1)"}
  }
}
```

### A6.5 Flows: settlement on a card rail and on an A2A rail, and settlement of a decision

```mermaid
sequenceDiagram
    participant P as Agent provider / PSP
    participant R as Rail
    participant I as Issuer / payer bank
    participant M as Merchant / acquirer
    rect rgb(245,245,245)
        Note over P,M: Card rail
        P->>R: authorisation with agent-capable token, agent indicator, authentication_ref (per-purchase approval or a PSP-applied exemption; the mandate alone is not SCA)
        Note right of P: abs_binding.reference_value (a locator) in a merchant/additional data field where the network allows. The full head is committed with the PSP (A5.8)
        R->>I: authorisation request
        I-->>R: approved, authorisation_code
        R-->>M: approved; clearing and settlement per scheme; the acquirer applies delayed funding or reserve per timing
        P->>P: append result; card_binding filled
    end
    rect rgb(235,245,255)
        Note over P,M: Account-to-account instant rail
        P->>I: credit transfer instruction: amount, payee account_ref, end_to_end_id, remittance = locator ABS:<purchase_id>:<head16>, full head in anchor_commitment
        I->>I: Verification of Payee; SCA by the payer's PSP (per-purchase approval or an exemption it applies)
        I->>I: record the full chain head with the payment and sign it (anchor_commitment, store psp_record)
        I->>R: instant credit transfer (pain.001 to pacs.008)
        R-->>M: funds credited; where the payee is an acquiring PSP it pays the merchant later under its contract (hold); funds on the merchant's own account are available immediately
        R-->>I: confirmation
        P->>P: append result; a2a_binding filled
    end
    Note over P,M: Same Purchase Record, same chain head, two bindings. The rail carries a locator, never the mandate, the trace or the commitment itself.
```

```mermaid
sequenceDiagram
    participant DC as Decision Center
    participant M as Merchant
    participant P as Agent provider
    participant PSP as PSP / acquirer / rail
    participant U as User
    DC->>DC: Settlement Instructions from Decision.amounts
    alt liable = merchant (AG3, AG4, AG1-M)
        alt funds under acquirer delayed funding or an acquiring PSP's hold
            DC->>PSP: payout_return instruction; the licensed holder credits the user; nothing to collect
        else
            DC->>M: refund instruction (card refund or credit transfer) with the case id
            alt merchant does not pay in 10 days
                DC->>PSP: collect under the collection right, the PSP or acquirer as creditor
                DC-->>U: Decision and Package as evidence; on cards the user may ask the issuer to raise a dispute before the scheme deadline
            end
        end
        PSP-->>U: credit to the original instrument
    else liable = agent_provider (AG1-P)
        DC->>P: refund instruction; collection right if unpaid
        PSP-->>U: new credit to the card (sponsored originator) or credit transfer to the account
        opt goods return ordered
            U->>M: return; shipping per Decision; merchant refund on return flows to P
        end
    else buyer side (AG2, AG5)
        alt withdrawal right available
            DC-->>U: remedy = withdrawal through the merchant's withdrawal function: return the goods within the window; merchant refunds within 14 days on receipt or proof of dispatch, whichever is earlier
        else
            DC-->>U: deny; statutory routes stated in the Decision remain open
        end
    end
    DC->>DC: close case; record settlement_instruction_ids; a participant that does not pay is suspended from the Register; the buyer keeps the rail's own routes
```

---

## A7. Decision Center governance

Founder's words: "we must have AI dispute decision center, we not plan to hire huge stuff, be pro
AI, but use our own invention like menimi, we improve decision makeing to the most modern never
seen level, we always know what we do and why decision is what it is". And, on structure:
decentralised decision centres for availability and compliance.

### A7.1 Principle

**The minimum Evidence Package is the primary safety lever; the arbiter architecture is
secondary.** On ordinary and scripted-adversarial disputes the Phase 2 run found that evidence,
not architecture, moved accuracy: the same end-to-end arbiter went from 82% to 98% correct
liability as the Package grew from E0 to E3, and the hybrid did not beat it (A7.9). Under optimised
fabrication of party-authored evidence the Package did not stop the attack, and at an equal attack
budget the hybrid's advantage was not significant (A8.7). AI-first with a guaranteed human-review right. Models find facts
and cite the evidence. A deterministic rule engine applies the decision order of A4. Every decision carries a signed receipt
with the full rule path and a plain-language explanation. Any party can obtain a human review
before the decision is final between participants. Humans audit a random sample. Error and reversal
rates are published. Decisions bind merchants and agent providers by contract; consumers keep every
statutory route. The same facts give the same decision on any node of the network. For natural
persons, the automated decision rests on their explicit consent given at filing, with a
human-decided alternative always offered (A7.5 item 8).

Audit 0 (Q5) found "humans only for escalations" indefensible under EU law and the Center
presumptively high-risk under the AI Act. Both points are accepted and built in below.

### A7.2 Design pattern and reference engine

The pattern is normative: typed Findings from independent fact-finders, a deterministic ruleset,
a signed receipt, human review on request. Any engine that meets A7.4 and A7.7 conforms.

The reference engine is Menime, the founder's deterministic decision engine. From the project's own
description it provides `decide(input, ruleset) -> {verdict, reason, verifiable receipt}` with
verdicts `allow | deny | needs_context | review`; composable rulesets; receipts signed by hash, HMAC
or Ed25519 with keys published as a JWKS and a public verify endpoint; a conformance harness that
replays cases; offline learning-loop proposals (rule changes are proposed from data and applied by
people, never learned live); standard packs including prompt-injection detection; an MCP interface.
Its laws include "The LLM may write. The kernel decides" and "If Menime cannot explain why an action
is allowed, the action is not allowed". The experiment's `acs/rule_engine.py` is a minimal implementation of the same
pattern. It is
named here as a reference implementation of the pattern, not as a dependency; the pattern, not any
product, is normative.

Three rulesets: `abs-liability` (A4), `abs-settlement` (A6.3) and `abs-allowance` (routing, A12.1);
Part B adds `abs-trust`.

### A7.3 Architecture

1. **Fact-finders.** Independent model calls, each with a fixed prompt, a fixed output schema (the
   Finding) and no view of the other finders' output. Types: offer conformity per binding attribute
   (snapshot spec against delivery evidence, applying tolerance and verification method); mandate
   compliance split into hard limits and item requirements (deterministic, not a model), intent
   match against the text terms the user confirmed (model) and a capture check of the conversation
   record against the captured terms (model, AG1-C); injection and manipulative content detection
   (prompt-injection pack plus a model over the `UntrustedText` fields in the snapshots); delivery
   status (deterministic from the Delivery Record where structured, model for free-text carrier
   events and image evidence); credibility (consistency of each side's statements with the chain).
   Every Finding cites evidence in the structured `cited_evidence` field (item id, path and hash;
   A5.7, A7.4); a Finding without a structured citation, or with a value outside its type's
   vocabulary, is dropped. Models run at the lowest temperature available, with pinned versions;
   prompts are hashed into the Finding.
2. **Quorum (optional defence-in-depth, not a core guarantee).** A node MAY produce each
   decision-relevant Finding type with two or three different model families and an agreement
   rule. The Phase 2 run measured that cross-family errors are correlated: under the pre-registered
   strict rule both families erred or abstained together at 1.24 times the rate independence
   predicts and the strict quorum escalated 93% of cases; under a relaxed conformity rule (post hoc,
   exploratory) both were wrong together on 9 of 153 matched decisions (6%), where independence
   predicts 2.4%, a ratio of 2.45. A quorum therefore adds less than
   independence would suggest. Before a node relies on one, it MUST measure and publish the error
   correlation between the families it uses; a quorum whose families fail together on the hard
   cases buys review load, not safety.
3. **Deterministic ruleset, with calibrated escalation.** `abs-liability` encodes Steps 0 to 4,
   the precedence, the remedies, the withdrawal overlay and the amount formulas; `abs-settlement`
   the rail mapping. Inputs are the Findings plus the verifier's deterministic Findings
   (signatures, chain, anchor, attachment hashes), canonicalised (RFC 8785) so any node computes
   the same bytes. Output: Decision, Settlement Instructions, Decision Receipt. The escalation
   threshold (when an unknown or low-confidence Finding sends the case to a human) MUST be
   calibrated and validated on a held-out case set, pre-registered and published, not set
   maximally conservative: the pre-registered strict fail-safe (conformity established only when no
   attribute the fact-finders supplied was unknown) escalated 54% of cases to humans (H6 refuted).
   As run, the 0.7 confidence threshold only decided whether a tie-break fact-finder was consulted,
   not the decision, so two merchant refunds rested on quantity findings at 0.60 and 0.55; a decision
   contract written after Audit 1 that applies 0.7 at the decision point and requires every binding
   attribute (exploratory, replayed on the same Findings) reviews 93 of 153 runs and is right in 60
   of 60 it decides. An exploratory relaxed rule (no attribute non-conforming and at least three known
   to conform) reached 6% review at 89% overall accuracy on the same logged Findings, post hoc and not
   pre-registered. Stated confidence is usable for calibration: at or above 0.85 the reason code
   was right 130 of 131 times.
3a. **End-to-end judge, permitted only behind the provenance gate and a calibrated abstention
   rule.** A node MAY use an end-to-end model that reads the Package and returns the decision,
   provided that: it emits the same Decision Receipt (typed Findings with structured citations, the
   rule path, the confidence), its Findings produced in the closed vocabularies and the
   `cited_evidence` form rather than extracted from free-text reasoning; every liability-moving
   Finding it relies on is corroborated by an independent evidence item that the content check finds
   supports it (A5.7), otherwise the case is escalated; and it abstains below a confidence threshold
   calibrated and published for the node. In the Phase 2 run the end-to-end arbiter with full
   evidence was consistent across three runs (51 of 51), 98% accurate against scripted adversaries,
   and abstaining below 0.7 reviewed 8% of cases with none of the 75 scripted manipulation outputs
   (25 cases) through. In Phase 3 an optimising dishonest party that rewrote only its own
   submissions fooled the same arbiter on 12 of 14 case-sides at E3 (best of 10 attempts; 10 of 14
   at a common budget of 5) and the second arbiter on 14 of 14; six of its seven successes against the
   buyer's staged photos sat at confidence 0.80 to 0.86, above a 0.7 abstention rule, which would
   have caught four of its five merchant-side successes. In Phase 3b a provenance gate in front of
   the same two arbiters cut their attack success within the same calls from 11 and 12 of 14 to 1 of
   14 each, mostly because their free-text findings could not be read and the gate failed closed, at
   the price of 24 of 50 cases of the baseline Phase 2 workload sent to review (fable); abstention
   below 0.7 alone let 8 of 14 through for fable (A5.7). Under attack the hybrid resisted every
   merchant-side attack (0 of 7) by leaving conformity unknown and escalating, and was fooled on 6 of
   14 case-sides within 5 attempts, all on the buyer side, by the same staged photos that fooled its
   fact-finders; at that common budget of 5 attempts the end-to-end arbiter was fooled on 10 of 14,
   a difference the stored data do not establish (exact McNemar p = 0.125, descriptive). Neither gate nor architecture tests a
   photograph. A record with authority for what arrived can contradict one; in Phase 3 such records
   stopped the attack against one arbiter and not against the other (A5.7).
4. **Signed receipt.** The Decision Receipt lists the ruleset id, version and hash, the engine
   version, the Finding hashes, every rule step with inputs and result, the quorum record, and the
   node that issued it. Parties verify it against the network's published keys. The receipt's hash
   is appended to the transparency log (A7.5).
5. **Human review on request.** Any party may request a human review of any Decision within 10
   days, not only when the engine returns `review`. The reviewer is a natural person of the
   operator who took no part in the automated decision, with the expertise, independence and
   impartiality that ADR rules require; the reviewer may confirm, change or send the case to appeal,
   may override any Finding, and signs a human Finding that is run through the same ruleset so the
   receipt still shows the path. The engine escalates on its own when it cannot establish a finding
   from the records (conflicting serials, contested photos): it returns `review` with the
   conflicting records marked, a fact-finder supplies the typed finding, and the engine decides
   from it (ABS-H1). Review outcomes (upheld, changed) are published in aggregate. In the
   simulation 73 of 528 scenarios (13.8%) reached a human (every debatable or uncertain ground truth,
   every evidence conflict, and a 1-in-9 sample), 2 by the engine's own escalation.
6. **Appeals.** Either party may appeal once within 10 days with new evidence. The procedure
   re-runs from fact-finding with a quorum that did not see the first run; the new receipt
   references the old (`appeal_of`). Appeal capacity is sized to the measured error rate: at a
   given accuracy, the expected number of wrong decisions per period is the minimum review
   capacity.
7. **Consistency.** Same Findings, same Decision, byte-identical receipt except timestamps and node
   id. Finder variance is bounded by fixed prompts, pinned models, the quorum and the threshold. The
   conformance harness replays the case library (starting with the experiment's 47 ground-truth
   cases) on every rule or model change; a change that alters any past decision is published as
   such before it takes effect.
8. **Audit and oversight.** Random sample of decisions reviewed by humans (default 2%, plus every
   human-residual case, every requested review and every appeal); drift monitoring per model and
   rule (finding distributions, confidence, overturn and reversal rates, quorum disagreement rate);
   rule changes signed, versioned, published with diff, rationale and effective date, with a notice
   period; a case is decided under the version in force when filed; model changes logged like rule
   changes; **continuous optimised red-teaming** in the Phase 3 method (an attacker model that sees
   the decision and rewrites only its own party's submissions, up to N attempts per case-side, on
   both sides and at every evidence level), with the attack-success figures per attacker, side,
   level and architecture published; publishing them is a condition of a node's admission and of
   staying admitted.
9. **What the humans do.** A small team: the residual Findings, requested reviews, the sample,
   appeal panels, approval of rule changes proposed by the learning loop, red-team cases. They do
   not decide cases freehand; a human Finding goes through the ruleset like any other.

### A7.4 Finding and Decision Receipt

**Finding.** One typed fact about one subject, with a value from its type's closed vocabulary,
confidence and at least one structured citation in `cited_evidence` (A5.7: item id, path, hash,
record type, provenance, the attribute it speaks to and the result of the content check). Deterministic
verifications are Findings with `deterministic: true` and confidence 1. Signed by: the node
(fact-finder models hold no keys).

```json
{
  "$id": "urn:abs:schema:0.3:finding",
  "type": "object",
  "required": ["finding_id", "case_id", "finder", "type", "subject", "value", "confidence", "cited_evidence", "deterministic", "produced_at", "node_id"],
  "additionalProperties": false,
  "properties": {
    "finding_id": {"type": "string"}, "case_id": {"type": "string"}, "node_id": {"type": "string"},
    "finder": {"type": "object", "required": ["kind", "id"],
               "properties": {"kind": {"enum": ["verifier", "model", "human"]}, "id": {"type": "string", "description": "model id and version, verifier version, or reviewer pseudonym"},
                              "model_family": {"type": "string"}, "prompt_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}, "panel": {"type": "integer", "minimum": 1}, "seat": {"type": "integer", "minimum": 1}}},
    "type": {"enum": ["mandate_signature", "chain_integrity", "anchor_match", "attachment_match", "mandate_hard_limits", "item_requirements", "intent_match",
                      "offer_conformity", "price_fee_consistency", "listing_edit", "injection_detection", "manipulative_content", "delivery_status", "credibility", "withdrawal_right"]},
    "subject": {"type": "object", "properties": {"line": {"type": "integer"}, "field": {"type": "string"}, "party": {"enum": ["buyer_side", "merchant"]}}},
    "value": {"type": "string", "pattern": "^[a-z_]+$", "description": "closed vocabulary per type, never free text; a value outside its type's vocabulary invalidates the Finding (A5.7): offer_conformity: conforms | within_tolerance | non_conforming | undeterminable; intent_match: matches | explicit_term_broken | ambiguous_should_have_asked | stated_not_captured | unstated_intent_only (A4.1 Steps 3, 3b, 4); injection_detection: present | absent; delivery_status: delivered | not_delivered | undeterminable"},
    "spec_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    "cited_evidence": {"type": "array", "minItems": 1, "description": "machine-checkable citations (A5.7); free text is never a citation; a Finding without this field cannot ground a decision",
                       "items": {"type": "object", "required": ["item_id", "path", "hash", "record_type", "provenance", "attribute", "support"], "additionalProperties": false,
                                 "properties": {"item_id": {"type": "string", "description": "id of the evidence item in the Package (an ABS object id, or the id of a Delivery Record part)"},
                                                "path": {"type": "string", "description": "JSON Pointer to the field relied on inside that item; MUST resolve in the Package"},
                                                "hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"},
                                                "record_type": {"enum": ["mandate", "allowance_policy", "approval_record", "offer_snapshot", "purchase_record", "settlement_instruction", "delivery_record", "action_log", "clarification", "image", "carrier_record", "serial_lookup", "digital_log", "return_inspection", "rail_record", "party_statement", "other"]},
                                                "provenance": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Provenance"},
                                                "fact": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/FactKind", "description": "the fact this citation is offered for; the record must have authority for it under a corroboration test (A5.7)"},
                                                "attribute": {"type": "string", "description": "the conformity-critical attribute (A5.4) or fact the citation speaks to; for a Step 1 Finding, the attribute the claim contests"},
                                                "support": {"enum": ["supports", "contradicts", "silent", "not_checked"], "description": "result of the content check (A5.7): what the cited record says about this Finding's value"},
                                                "support_check": {"enum": ["deterministic", "finding", "none"], "description": "deterministic comparison where the record is structured; a separate cited Finding where it is free text"},
                                                "reliability_note": {"type": "string", "maxLength": 200}}}},
    "corroborated": {"type": "boolean", "description": "true only when, for each fact the Finding rests on, at least one citation that meets a corroboration test of A5.7 has support = supports and none has support = contradicts; a liability-moving Finding with false here cannot ground an automatic decision"},
    "corroboration_basis": {"enum": ["independent_authority", "binding_on_party", "sole_source_conduct_record", "none"], "description": "which A5.7 test the decisive citation met: (a), (b) or (c)"},
    "rationale": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/UntrustedText"},
    "deterministic": {"type": "boolean"},
    "produced_at": {"type": "string", "format": "date-time"}
  }
}
```

**Decision Receipt.** Signed by: the issuing node (engine key, in the envelope with `role:
arbiter`). Verifiable offline against the network's JWKS; its hash is in the transparency log.

```json
{
  "$id": "urn:abs:schema:0.3:decision-receipt",
  "type": "object",
  "required": ["receipt_id", "subject_type", "subject_id", "node", "engine", "ruleset", "inputs", "rule_path", "verdict", "reason", "quorum", "human_review", "log_entry", "issued_at"],
  "additionalProperties": false,
  "properties": {
    "receipt_id": {"type": "string"},
    "subject_type": {"enum": ["decision", "allowance_routing", "trust_attestation", "qualification", "suspension", "expulsion", "appeal"]},
    "subject_id": {"type": "string"}, "case_id": {"type": "string"}, "appeal_of": {"type": "string"},
    "node": {"type": "object", "required": ["node_id", "operator", "region"], "properties": {"node_id": {"type": "string"}, "operator": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef"}, "region": {"type": "string", "description": "e.g. EU"}}},
    "engine": {"type": "object", "required": ["name", "version", "verify_url", "jwks_url"],
               "properties": {"name": {"type": "string"}, "version": {"type": "string"}, "verify_url": {"type": "string", "format": "uri"}, "jwks_url": {"type": "string", "format": "uri"}}},
    "ruleset": {"type": "object", "required": ["id", "version", "hash"], "properties": {"id": {"type": "string"}, "version": {"type": "string"}, "hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}, "effective_from": {"type": "string", "format": "date-time"}}},
    "inputs": {"type": "object", "required": ["finding_hashes", "canonical_input_hash"],
               "properties": {"finding_hashes": {"type": "array", "items": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}},
                              "canonical_input_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash", "description": "hash of the RFC 8785 canonical input; any node with the same inputs and ruleset reproduces the same decision"},
                              "evidence_bundle_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}, "evidence_level": {"enum": ["E0", "E1", "E2", "E3"]}}},
    "rule_path": {"type": "array", "minItems": 1, "items": {"type": "object", "required": ["step", "rule_id", "inputs_used", "result"],
                  "properties": {"step": {"type": "integer"}, "rule_id": {"type": "string", "description": "e.g. S0, S1-CONFORMITY, S2-MANIPULATION, S3-AGENT-FAULT, S4-BUYER, P-PRECEDENCE, REM-AG1P, WDR-OVERLAY, SET-A2A-AG3"},
                                 "inputs_used": {"type": "array", "items": {"type": "string"}}, "result": {"type": "string"}, "note": {"type": "string", "maxLength": 300}}}},
    "verdict": {"enum": ["decided", "needs_evidence", "escalate_panel", "escalate_human", "attested", "refused", "suspended", "expelled"]},
    "reason": {"type": "string"},
    "quorum": {"type": "object", "required": ["families", "panels_run", "agreement", "min_confidence"],
               "properties": {"families": {"type": "array", "items": {"type": "string"}}, "panels_run": {"type": "integer"}, "agreement": {"type": "boolean"}, "min_confidence": {"type": "number"}}},
    "human_review": {"type": "object", "required": ["requested", "performed"], "properties": {"requested": {"type": "boolean"}, "performed": {"type": "boolean"}, "reviewer_pseudonym": {"type": "string"}, "outcome": {"enum": ["upheld", "changed", "not_performed"]}}},
    "decision_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash", "description": "hash of the Decision body this receipt proves; identical across nodes for identical inputs"},
    "log_entry": {"type": "object", "required": ["log_id", "leaf_hash"], "properties": {"log_id": {"type": "string"}, "leaf_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}, "tree_size": {"type": "integer"}, "inclusion_proof": {"type": "array", "items": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}}}},
    "issued_at": {"type": "string", "format": "date-time"}
  }
}
```

### A7.5 Federated Decision Network

One centre is a single point of failure and a single point of pressure. The Decision Center is
designed as a network of independent operator nodes admitted against published criteria.

**Status: PROPOSED.** Nothing in this section is implemented or tested. No node has been admitted,
no governance body exists, no transparency log runs, and no failover or cross-node recomputation has
been exercised; the experiment ran its arbiters, the cross-family quorum included, inside one
research harness (A7.9). The section states the design a node would be bound to once the network
exists.

1. **Nodes.** Each node is run by an operator admitted by the ABS governance body against published
   criteria, independent of the parties in the cases it decides (A2). "Admitted" is a programme
   status; it is not statutory accreditation, and a node is not an ADR entity unless listed by a
   national authority under Directive 2013/11/EU Art 20. Deterministic rules plus canonicalised inputs mean any node reproduces the
   identical Decision and receipt hash for the same Findings and ruleset version, so failover is
   safe and a party can ask a second node to recompute. Every receipt carries the rule-version
   reference and the node id.
2. **Fact-finding quorum.** Two or three different model families per Finding type, with the
   agreement rule of A7.3. Nodes MAY use different providers for the same family set; the quorum
   record is in the receipt.
3. **Transparency log.** A tamper-evident, append-only Merkle log of decision and receipt hashes
   and of rule versions, in the manner of Certificate Transparency (RFC 9162, an Experimental RFC;
   its Merkle structures and proofs are reused, its CA-specific parts are not). Parties and auditors verify inclusion and
   consistency; personal data stays off the log, hashes only. A decision that is not in the log is
   not final between participants.
4. **Data residency.** EU-region nodes decide cases with EU parties; evidence stays in region. A
   data-protection impact assessment is performed for the network and per node. A company is not
   a data subject, but personal data about its people (directors, beneficial owners in KYB data,
   staff, contact persons, reviewers) is in scope; sole traders and users are data subjects.
5. **Resilience.** PSP, acquirer and e-money participants are financial entities under the EU
   Digital Operational Resilience Act (Regulation (EU) 2022/2554, Art 2(1)(b) and (d); applies from
   17 Jan 2025); a Decision Center operator serving them is an ICT third-party provider bound by the
   Art 30 contractual terms and directly overseen only if designated critical under Art 31;
   incident-reporting duties sit with the financial entity. ISO 22301:2019 business continuity for
   every node; published recovery time and recovery point objectives for the case store and the
   log.
6. **Degraded mode.** If no node can decide: funds stay in the PSP payout hold or reserve where
   one applies; dispute deadlines pause and are extended day for day; after a defined time (default
   30 days) the case falls back to the existing chargeback route or statutory ADR with the Evidence
   Package handed over. The availability claim is "no single point of failure and zero lost
   disputes", not a percentage uptime.
7. **Governance.** Rule changes are signed by the governance body, published in advance with a
   notice period, versioned and hashed into the log; operators are admitted against ABS's own
   published independence and impartiality criteria, written with Directive 2013/11/EU Art 6 and
   ISO 10003:2018 (guidance, not a certifiable standard) as references, and re-admitted
   periodically; no operator decides disputes involving its own agents or merchants; admission,
   suspension and removal of operators are themselves logged decisions.
8. **Designed against (not "compliant with") the EU AI Act, the GDPR and ADR law.** No conformity
   assessment, legal opinion or listing has been obtained; the design targets are these.
   - **AI Act** (Regulation (EU) 2024/1689): an AI system "to be used in a similar way in
     alternative dispute resolution" is high-risk under Annex III point 8(a); recital 61 adds that
     ADR outcomes that "produce legal effects for the parties" make the system high-risk and that
     "the final decision-making must remain a human-driven activity". Decisions that bind
     participants by contract produce legal effects, so the high-risk reading is the correct one,
     not caution. Obligations designed for: risk management (Art 9), data governance (Art 10),
     logging (Art 12), transparency (Art 13), human oversight with power to override (Art 14),
     accuracy and robustness (Art 15), a quality management system (Art 17), conformity assessment
     by internal control under Annex VI with no notified body (Art 43(2) for Annex III points 2 to
     8), EU database registration (Art 49), post-market monitoring (Art 71), the right to an
     explanation of individual decision-making for affected persons (Art 86) and the disclosure that
     a person is interacting with an AI system (Art 50(1)). Roles per node: the provider is the
     party that places the engine and rulesets on the market; each node operator is a deployer
     (Art 26). Art 6(3) does not exempt the system, because the fact-finders materially influence
     the outcome. Art 27 fundamental-rights impact assessments bind public bodies, private
     providers of public services and Annex III points 5(b) and (c) deployers, so they likely do not
     apply; a DPIA is done regardless. Timeline: the Digital Omnibus on AI, Regulation (EU)
     2026/1744 (OJ 24 Jul 2026, in force 27 Jul 2026), sets 2 December 2027 for Annex III
     obligations under Chapter III Sections 1 to 3 (new Art 113(c)); whether Section 5 (Arts 43 and
     49) moves with them is not settled. Open tension recorded in A15.1: automated finality between
     participants (A7.1) against "human-driven" final decision-making.
   - **GDPR** (Regulation (EU) 2016/679): a refund decision based solely on automated processing is
     caught by Art 22. The contract basis of Art 22(2)(a) needs a contract between the data subject
     and the controller, and a consumer or sole trader has none with the Decision Center, so it is
     not relied on. The basis is the data subject's **explicit consent** given at filing (Art
     22(2)(c)) with a human-decided alternative always available, or, where consent is not given,
     a human decision as the default for natural persons. Art 22(3) safeguards (human intervention,
     the right to express a view and to contest) apply in every case; the Arts 13(2)(f) and
     15(1)(h) duties to explain the logic are met by the plain-language explanation, which the
     Court of Justice reads as "the procedure and principles actually applied" (C-203/22, CK v
     Magistrat der Stadt Wien, 27 Feb 2025; C-634/21 SCHUFA, 7 Dec 2023).
   - **ADR law**: Directive 2013/11/EU Art 6 (expertise, independence, impartiality), Art 10(1) (a
     pre-dispute agreement that deprives the consumer of court access does not bind), Art 10(2) (a
     binding outcome binds the consumer only if informed in advance and specifically accepted) and
     Art 2(2)(g) (trader-initiated procedures are outside statutory ADR). The Decision Center is
     **ADR-designed**, not an ADR entity: that status comes only from national listing under Art
     20. Directive (EU) 2025/2647 (OJ 30 Dec 2025; in force 19 Jan 2026; transposition by 20 Mar
     2028; applies from 20 Sep 2028) requires listed entities to inform parties in advance of
     automated means and to give a right to have the **outcome** reviewed by a natural person
     meeting Art 6(1); it binds listed entities only and ABS adopts it voluntarily. The EU ODR
     platform stopped accepting complaints on 20 Mar 2025 and was repealed with effect from 20 Jul
     2025 (Regulation (EU) 2024/3228); no ABS flow refers to it.
   - Management systems: ISO/IEC 42001:2023 (requirements) and ISO/IEC 23894:2023 (guidance) for
     AI; ISO/IEC 27001:2022 with Amd 1:2024 and ISO/IEC 27002:2022 for information security;
     ISO/IEC 27701:2025 for privacy; ISO 9001:2026 for quality.

**Node and log schemas.**

```json
{
  "$id": "urn:abs:schema:0.3:decision-node",
  "type": "object",
  "required": ["node_id", "operator", "region", "admission", "engine", "rulesets", "keys", "log_id", "status"],
  "properties": {
    "node_id": {"type": "string"}, "operator": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef"}, "region": {"type": "string"},
    "admission": {"type": "object", "required": ["admitted_at", "valid_until", "independence_statement_hash"],
                      "description": "programme admission against published criteria; not statutory accreditation; ADR-entity status only by national listing",
                      "properties": {"admitted_at": {"type": "string", "format": "date-time"}, "valid_until": {"type": "string", "format": "date-time"},
                                     "independence_statement_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}, "excluded_parties": {"type": "array", "items": {"type": "string"}, "description": "party_ids whose cases this node must not decide"},
                                     "receipt_id": {"type": "string"}}},
    "engine": {"type": "object", "properties": {"name": {"type": "string"}, "version": {"type": "string"}}},
    "rulesets": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "version": {"type": "string"}, "hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}}}},
    "model_families": {"type": "array", "items": {"type": "string"}},
    "keys": {"type": "array", "items": {"type": "object", "properties": {"kid": {"type": "string"}, "alg": {"type": "string"}, "public_key": {"type": "string"}, "valid_from": {"type": "string", "format": "date-time"}, "valid_until": {"type": "string", "format": "date-time"}}}},
    "jwks_url": {"type": "string", "format": "uri"}, "verify_url": {"type": "string", "format": "uri"},
    "log_id": {"type": "string"},
    "continuity": {"type": "object", "properties": {"rto_minutes": {"type": "integer"}, "rpo_minutes": {"type": "integer"}, "last_test_at": {"type": "string", "format": "date-time"}}},
    "status": {"enum": ["active", "suspended", "retired"]}
  }
}
```

```json
{
  "$id": "urn:abs:schema:0.3:log-entry",
  "type": "object",
  "required": ["log_id", "index", "timestamp", "entry_type", "leaf_hash", "node_id"],
  "additionalProperties": false,
  "properties": {
    "log_id": {"type": "string"}, "index": {"type": "integer", "minimum": 0}, "timestamp": {"type": "string", "format": "date-time"},
    "entry_type": {"enum": ["decision", "receipt", "ruleset_version", "node_admission", "node_status", "appeal", "human_review", "chain_anchor"], "description": "chain_anchor: the full head of a purchase chain committed at payment (A5.8)"},
    "leaf_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash", "description": "hash of the entry object; no personal data on the log"},
    "subject_id": {"type": "string"}, "node_id": {"type": "string"},
    "ruleset_ref": {"type": "object", "properties": {"id": {"type": "string"}, "version": {"type": "string"}, "hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}}},
    "tree_head": {"type": "object", "properties": {"tree_size": {"type": "integer"}, "root_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}, "signature": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Signature"}}}
  }
}
```

### A7.6 Decision pipeline

The nodes, second panel, failover and log in this diagram belong to the proposed network of A7.5.

```mermaid
sequenceDiagram
    participant P as Parties (buyer side, merchant)
    participant N1 as Node 1 (EU)
    participant V as Verifier (deterministic)
    participant Q as Quorum: 2-3 model families
    participant Q2 as Second panel
    participant H as Human reviewer
    participant E as Rule engine (abs-liability, abs-settlement)
    participant L as Transparency log
    participant N2 as Node 2 (failover / recompute)
    P->>N1: escalation + Evidence Package (E0..E3)
    N1->>V: signatures over the envelope context, chain recompute, full head vs its authenticated commitment, attachments vs checkout snapshot
    V-->>N1: deterministic Findings (confidence 1)
    N1->>Q: per Finding type: conformity per attribute, item requirements, intent match, injection, delivery status, credibility
    Q-->>N1: Findings with confidence and evidence hashes
    alt quorum agrees and min confidence >= 0.80
        N1->>E: decide(canonical Findings, abs-liability vX)
    else disagreement or low confidence
        N1->>Q2: different families, higher effort
        Q2-->>N1: Findings
        alt agrees
            N1->>E: decide(...)
        else still disagrees
            N1->>H: contested Finding (kind=human)
            H-->>N1: Finding
            N1->>E: decide(...)
        end
    end
    E-->>N1: Decision, rule path, signed receipt (needs_evidence -> request record, re-run)
    N1->>E: decide(Decision, abs-settlement) -> Settlement Instructions
    N1->>L: append receipt hash, decision hash, ruleset version
    L-->>N1: inclusion proof, signed tree head
    N1-->>P: Decision + Receipt + plain-language explanation + how to request human review or appeal
    opt human review requested by any party
        P->>N1: request
        N1->>H: review; human Finding -> same ruleset -> new receipt, logged
    end
    opt verification or failover
        P->>N2: recompute from the same canonical inputs and ruleset version
        N2-->>P: identical decision hash, or a logged discrepancy
    end
    Note over N1,N2: Same inputs, same ruleset, same decision hash on any node. No node decides cases involving its own operator's agents or merchants.
```

### A7.7 Minimum requirements for a conforming Decision Center

A node MUST: produce typed Findings with structured evidence citations (`cited_evidence`, A5.7); run
a deterministic ruleset on canonicalised inputs with a calibrated, published escalation threshold;
if it uses a quorum, measure and publish the error correlation of its families before relying on it;
if it uses an end-to-end judge, run it only behind the provenance gate and a calibrated, published
abstention rule, and emit the same receipt with traceable Findings; apply the provenance gate, with
the content check, to every liability-moving Finding; run continuous optimised red-teaming and
publish its attack-success figures as a condition of admission; publish its review rate by liable
party as finally decided and by reason code, with uncited reviews counted apart (A5.7); issue a
signed receipt with the full rule path and a plain-language explanation; offer a human review to any
party on request before finality between participants; append every decision to the transparency
log; publish accuracy, reversal, human residual and quorum disagreement rates; publish rule versions
in advance; never decide a case involving its operator's own agents or merchants; state in every
Decision that consumer statutory routes are unaffected; obtain a natural person's explicit consent
to automated decision at filing or decide by a human; never be a payer or payee of funds; never
raise a rail dispute. The transparency-log, admission and failover requirements bind once the
proposed network of A7.5 exists; until then no node can meet them, and none is claimed to.

### A7.8 Where judgement remains, and how it is bounded

P1 says AI never decides by interpretation. The rule-completeness simulation lists the findings a
deterministic engine cannot compute from records alone; the rules that use them are deterministic
once the finding is typed, but the finding itself is a judgement. The simulation's table has 14
such findings under 10 rules. Each is bounded in the same three ways: it is produced by a
cross-family fact-finder quorum (two or three model families, agreement rule, second panel on
disagreement); it must cite the signed evidence it rests on or it is discarded; and any party may
obtain a human review within 10 days. Where even that cannot settle it, the engine returns
`review` rather than guess.

| Judgement finding | Rule that uses it | Typed vocabulary | Evidence it must cite |
|---|---|---|---|
| `text_instructs_an_agent` | AG4 injection | present / absent | the `UntrustedText` field in the view or checkout snapshot |
| `causation_agent_followed_it` | AG4 injection | followed / not_followed | the action log step and its stated reason |
| `claim_is_false` | AG4-D deceptive claims | false / not_shown_false | the reference price or stock record against the content |
| `claim_caused_the_choice` | AG4-D | caused / not_caused | the action log comparison step |
| `conformity_of_free_text_description` | AG3 (only where a binding attribute is absent and the profile allows it) | conforms / non_conforming / undeterminable | snapshot text hash and delivery evidence |
| `counterfeit_determination` | AG3 | counterfeit / genuine / undeterminable | serial lookup, packing record, buyer photos |
| `damage_vs_wear` | AG3 | damage / wear / undeterminable | buyer photos, return inspection, delivery date |
| `attribute_is_ambiguous` | ABS-S2 ambiguity | ambiguous / clear | the attribute in the signed spec and the delivered value |
| `which_record_is_true` | ABS-H1 conflicting evidence | packing_record / buyer_evidence / undeterminable | both records; `undeterminable` escalates to a human |
| `evidence_knowingly_false_or_altered` | ABS-C1 conduct | yes / no | chain verification result and the attachment hashes |
| `existence_of_undisclosed_arrangement` | ABS-X1 collusion | yes / no | trust attestation at checkout, action log, incentive disclosure |
| `incentive_existed_and_was_undisclosed` | ABS-X2 undisclosed incentive | yes / no | the Mandate's `incentive_disclosure` and the action log |
| `damage_attributable_to_buyer` | ABS-D2 merchant claim | yes / no / undeterminable | handover and return inspection records |
| `what_the_buyer_meant` | Step 4 label (AG2 vs AG5) | matched / not_matched | the intent text and clarifications; it never changes who is liable, only the label |
| `requirement_stated_not_captured` | Step 3b capture failure (AG1-C; added after the simulation, not counted in its table) | stated_not_captured / not_stated / stated_as_open_preference | the conversation record committed by `conversation_hash` and the captured terms |

Everything else in A4 is read off signed records by the verifier (signatures, chain, anchor,
attachment hashes, hard limits and item requirements, cart origin, feed-versus-snapshot values,
time limits, Register entries) and needs no model. Eighteen of the simulation's 28 rules are of
that kind.

### A7.9 Experiment results (H2, H3, H5, H6; pre-registered, simulated, small n)

Phase 2 (`results/PHASE2_DISPUTES.md`; 51 Dispute Cases with known ground truth, 34 of them
scripted; two frontier arbiters; synthetic contestable delivery evidence; Wilson and
cluster-bootstrap intervals):

- **Evidence (H2, H5 supported).** Liable party correct, E0 to E3: claude-fable-5-1 82% to 98%,
  grok-4.7 61% to 96%; reason code 69% to 96% and 47% to 94%; all four exact McNemar tests
  significant (p 0.008 to 1e-7). Residual route rate (recovery that still depends on the buyer's
  own issuer-raised card dispute, contractual collection or no route; called the "rail-dispute rate"
  before Audit 1, counts unchanged) 14% and 41% at E0 to 4% at E3. Fooled by scripted adversaries
  20% to 5%, not significant at n = 20 (H3). These labels are rulebook v1.2; against the v1.4
  labels the same E3 decisions are right on liable party in 45 and 44 of 51 (A4.2).
- **Architecture (H6 refuted as pre-registered).** A1 end-to-end: 0 human reviews, 98% correct,
  51 of 51 consistent across three runs, manipulated on 1 of 25 scripted-adversarial cases (3 of
  75 outputs). A2 hybrid with the strict fail-safe: 54% sent to human review, 97% correct when it
  decided, 0 of 75 scripted manipulation outputs through (0 of 25 cases, case-level upper bound
  13%), every error or review traceable to a specific Finding (85 of 85), 80% consistent. As run,
  its 0.7 threshold governed only the tie-break; the post-audit decision contract (exploratory)
  reviews 93 of 153 and is right in 60 of 60 decided (A7.3 item 3). A3 cross-family quorum: 93%
  review. Post hoc, not pre-registered: a relaxed conformity rule gives A2 6% review at 89% overall
  accuracy and manipulation on 2 of 25 cases (6 of 75 outputs). Conclusion adopted in A7.1, A7.3
  and A7.7: the Package is the primary lever; the hybrid stays as the auditable pattern with a
  calibrated threshold; an end-to-end judge is allowed with receipts and traceable Findings.
- **Diversity.** Cross-family errors are correlated: 1.24 times independence under the strict rule
  (with the strict quorum reviewing 93%), 2.45 under the post-hoc relaxed rule; the quorum is
  optional defence-in-depth (A7.3 item 2).
- **Stake framing.** Telling the arbiter that the service is operated and paid for by the merchant
  platform or by the agent provider did not shift liability toward the operator (one model, an
  explicit framing sentence; a real financial stake is untested).
- **Optimised attacks (Phase 3, `results/PHASE3_ATTACKS.md`; Amendment 13; 14 case-sides; one
  attacker chain).** A dishonest party that rewrote only its own submissions, seeing each decision
  and trying up to 10 times, fooled claude-fable-5-1 at E3 on 12 of 14 case-sides (86% [60, 96];
  against 1 of 14 under the scripted adversary, H8 p = 0.001) and at E1 on 14 of 14; grok-4.7 at E3
  on 14 of 14; the hybrid A2 on 6 of 14 within its 5 attempts (43% [21, 67]), all on the buyer side;
  the cross-family quorum once. The budgets differ, so 12 of 14 against 6 of 14 is descriptive; at a
  common budget of 5 attempts claude-fable-5-1 was fooled on 10 of 14 against the hybrid's 6 of 14
  (exact McNemar p = 0.125), and the hybrid spends three arbiter-side calls per attempt against one.
  The attacker was substituted after preliminary outcomes (Deviations 4 and 5), so Phase 3 is
  exploratory development of the attack; a frozen-attacker confirmation is a prospective experiment plan, not run. Every attack edited only party-authored evidence:
  staged photo descriptions, listing text, chat, delivery notes. Against claude-fable-5-1 the
  attacks failed only on the two case-sides where a record from outside the parties tied the goods
  to the order: the manufacturer registry (D06) and the carrier weight gap (D05) resisted all 10
  attempts. grok-4.7 was fooled on both, with the same records in its Package. The Package raised
  the cost (aggregate attempts expended per successful case-side 3.9 at E3 against 1.8 at E1; among
  fooled case-sides the first success came at a mean of 2.25 attempts at E3, median 1, against 1.79
  at E1) but did not stop the attack (H9 not significant). Payloads optimised against the stronger arbiter fooled the weaker one 14 of 14
  in one shot. Design conclusion adopted in A4.1, A5.7, A7.3 and A8.7: a liability-moving finding
  must be corroborated by a record with authority for its fact, and the engine, not the judge,
  checks that. The data show such records resisting some attacks against one arbiter; they do not
  show them necessary or sufficient (no record was removed or added under control).
- **Provenance gate (Phase 3b, `results/PHASE3B_PROVENANCE.md`; Amendment 14; H10).** A gate that
  checked the tier and type of the cited record cut attack success on the Phase 3 payloads at E3,
  within the same calls, from 11 of 14 case-sides to 1 of 14 (claude-fable-5-1, p = 0.002) and from
  12 of 14 to 1 of 14 (grok-4.7, p = 0.001); recomputed for the hybrid, from 7 of 14 to 3 of 14. H10
  as pre-registered (12 of 14 to 1 of 14, p = 0.001) is confounded with re-testing selected
  successes under a changed prompt. Most end-to-end rejections were format failures, not provenance
  checks (format / provenance / contradiction: fable 10 / 2 / 0, grok 13 / 0 / 0); every attack that
  passed cited a relevant-looking independent record that does not support the finding; on the
  baseline Phase 2 workload it sent 24 of 50 to review (48%), 22 of 31 true claimants against 2 of
  19 unfounded claims. Adopted in A5.7: structured citations, a content check, independent
  delivery-side records and a published review rate by liable party. A gate v2 written after the
  audit with these outputs in view lets 0 of 14, 0 of 14 and 0 of 67 hybrid attempts through on the
  stored outputs and reviews 26 of 50 baseline cases (exploratory). A matched gate-on and gate-off test with a gate-aware attacker ran later, frozen, as
  confirmatory amendment C1: gate v3 cut best-of-5 attack success on 14 fresh case-sides from 11 to 0
  of 14 (p = 0.00049, one-sided) and sent 34 of 51 baseline cases to review (A5.7). Its replication,
  confirmatory amendment C2, gave 25 of 28 against 0 of 28 on 28 further fresh case-sides (p = 3.0e-8,
  one-sided). The confidence-aware attacker and the other lost cells of Deviation 6 are prospective plans, not run.
- **Limitations.** Ground truth applies this rulebook, not a court's; arbiters, fact-finders and
  agents share two model families; 34 of 51 cases are scripted; the evidence is synthetic with
  designed inconsistencies (photos are descriptions, so a fabricated and a real photo are
  indistinguishable by construction); n is small; the Phase 3 attacker was two xAI models under one
  framing, grey-box, with frequent refusals by the frontier models.

---

## A8. Known failure modes and mitigations

This section is normative and it is honest. P1, "exact by construction", can fail in six ways. Each
is named with its mitigations, which a conforming implementation MUST apply, and with what remains.

### A8.1 Bad facts: the judgement moved into fact-finding

The rules are exact; the Findings they run on may be wrong. A wrong conformity Finding gives an
exact, wrong decision.

Mitigations:

- **Signed specs with measurable attributes.** Every binding attribute has a unit, a tolerance and
  a verification method (A5.4), so the fact to find is "is the measured value within tolerance",
  not "does this look right".
- **An evidence-capture protocol.** The agent provider's app and the merchant's packing process
  capture: time-stamped photos with required views per profile (label, serial, contents, packaging,
  defect), C2PA-signed where the capture device supports it; serial or IMEI capture by OCR with the
  image kept; unboxing evidence where the profile asks for it; the carrier's proof-of-delivery
  photo where the carrier produces one; an accredited return inspection where the goods go back.
  A Finding that rests on evidence captured outside the protocol says so and carries lower
  confidence.
- **Citations first, quorum second** (A7.3): a Finding without a structured citation to signed
  evidence (`cited_evidence`, A5.7) is discarded. A cross-family quorum is optional defence-in-depth: the Phase 2 run measured the two
  families' errors as correlated at 1.24 times independence under the strict rule (2.45 under a
  post-hoc relaxed rule) and the strict quorum escalating 93% of cases, so a quorum adds less than assumed and its diversity must be measured before it is
  relied on.
- **Abstention, then escalation.** Below the confidence threshold (default 0.80) the finder
  abstains; the engine returns `review`; a human supplies the Finding (A7.3 items 2 and 5).
- **Random human audits that publish error rates** (A7.3 item 8): the Finding error rate per type
  and per model family is published, so a party knows how often "conforms" is wrong.
- **Burden-of-proof defaults when facts cannot be established.** A record keeper that cannot
  produce its record loses the question (ABS-E1, ABS-E1m); an ambiguous listing is read against
  its author (ABS-S2); an unsupported claim fails (ABS-E2); records that conflict with no keeper at
  fault go to a human (ABS-H1). The engine never guesses.
- **Provenance gate.** No liability-moving Finding without a supporting record that has authority
  for the fact it asserts and meets a corroboration test (A5.7 corroboration and content check,
  A8.7).

What remains: a confident, cited, agreed Finding that is still wrong. The audit sample and the
appeal route are the only correction; their capacity is sized to the measured error rate.

### A8.2 Unforeseen cases

The catalogue has 528 scenarios; the world has more.

Mitigations:

- **A residual default rule plus escalation.** A case no rule decides returns `review`, not a
  guess; the human decision is recorded as a human Finding and the case is decided under the
  existing steps if it then fits, or marked `unforeseen`.
- **A precedent log.** Every `unforeseen` decision is logged with its facts and reasoning. Recurring
  patterns become candidate rules proposed by the offline learning loop (A7.2), never applied live.
- **Impact simulation before release.** Every rule change is run over the scenario catalogue and
  over past decided cases; the report states which past decisions would change. A change is then
  signed by the governance body, published in advance with its version, hash, diff and effective
  date (A7.5 item 7), and cases are decided under the version in force when filed.

What remains: the first instance of each new pattern is decided by a human, slowly.

### A8.3 Gaming

Deterministic public rules can be optimised against.

Mitigations:

- **Public dispute rules, private signal weights.** The liability rules, remedies and evidence
  requirements are public (P4). The weights of fraud and trust signals, the sampling rate and the
  thresholds that trigger a review are not, as in card fraud systems.
- **Outcome-pattern monitoring per party.** Dispute rates, decided-against rates, claim patterns
  and refusal patterns per merchant, per agent provider and per buyer cluster; a party whose
  outcomes drift from its peers is sampled more.
- **Random audits** of decided cases, with the sampling rate undisclosed.
- **Tolerances set by category profiles, not by merchants.** A merchant cannot widen a tolerance
  to make a non-conforming delivery conform; the profile sets the default and the merchant may only
  tighten it.
- **Graduated penalties.** Probation, reduced trust level, payout hold, caps, suspension, expulsion
  and the shared blocklist (Part B1), applied through the Decision Center with receipts and appeal.
- **A bounded low-value burden (ABS-V1).** Its threshold and cap are liability rules and therefore
  public, unlike review triggers. A buyer who fabricates claims on orders under the threshold gains
  at most the threshold times the cap per identity per window (EUR 300 a year with the defaults);
  the payer's PSP keeps the count, and outcome-pattern monitoring sees the rest (A5.7).

What remains: a party that plays exactly to the rules gains exactly what the rules allow.

### A8.4 Mandate burden and fairness

If the user must write the mandate, the precision burden lands on the party least able to carry
it, and "unstated intent on the user" becomes a trap.

Mitigations:

- **The agent proposes, the user confirms.** The Mandate is proposed by the agent from the
  conversation, using the category template to prompt for conformity-critical attributes; the user
  confirms the plain-language terms with one strong-authentication tap (A4.2, Mandate
  `proposed_by`, `template_profile`, `user_confirmation`).
- **Capture duty (Step 3b).** An explicit requirement the user stated to the agent that the agent
  failed to capture is agent fault. The provider keeps the conversation record and loses the
  question if it cannot produce it. The precision burden is on the system.
- **Templates per category** list the attributes a buyer of that category usually cares about;
  what the user leaves open is shown as open.
- **Withdrawal right and plain-language disclosure** sit under every consumer decision (A4.4,
  A5.9).
- **The provenance gate's review burden** (A5.7). A gate that escalates what it cannot corroborate
  makes the claimant whose claim is true wait: on the baseline Phase 2 workload in Phase 3b it
  reviewed 12 of 21 merchant-liable and 10 of 10 agent-provider cases (22 of 31 true claimants)
  against 2 of 19 buyer-liable ones. ABS specifies delivery-side
  records with authority for what arrived (carrier weight and scans, registry binding at dispatch,
  inspection by an inspector without a stake; certified capture for image integrity) so true claims
  can be corroborated, and every node publishes its review rate by liable party (A1.5, A7.7).

Jurisdiction profiles (general statements; verify before relying on any):

| Jurisdiction | Constraint on placing unstated intent on a consumer | ABS position |
|---|---|---|
| EU | Unfair Contract Terms Directive 93/13/EEC: standard terms that cause a significant imbalance (Art 3(1)); the annex presumes unfair terms that exclude or hinder legal remedies, unduly restrict the evidence available to the consumer or impose a burden of proof that should lie elsewhere (1(q)), or limit rights on non-performance (1(b)); consumer protection of the home law cannot be removed by choice of law (Rome I Art 6(2)); the withdrawal right and conformity guarantees are mandatory | Step 4 is reached only after capture duty, hard limits, item requirements and explicit instructions have been exhausted; the withdrawal overlay gives the consumer a no-fault exit; Decisions never bind the consumer; the evidence rules ABS-E2 and ABS-D1 and "signed records only" apply between participants and are never written into consumer-facing terms of agent providers or merchants |
| UK | Consumer Rights Act fairness test for terms; regulator guidance makes businesses responsible for the agents they deploy (per Audit 0) | As EU; whether a consumer-facing agent provider owes reasonable care and skill for the mandate it proposes is an open question that would strengthen Step 3b |
| US | State unfair and deceptive practices laws; card network rules allocate in-mandate agent actions to the cardholder (Visa, per Audit 0); no general withdrawal right | Step 4 agrees with the network allocation; capture duty and plain-language confirmation are the consumer safeguards; the merchant's return policy is the exit |
| India | Consumer Protection Act and the UPI dispute framework | As US for allocation; UPI dispute mechanisms for the rail; profile to be developed |

What remains: a consumer who confirmed terms without reading them. The one-tap confirmation shows
the captured terms and the open ones; the approval-fatigue indicator (Part B3.5) measures whether
confirmations are read.

### A8.5 Missing evidence during adoption

Early merchants will not have packing records with serials; early agents will not have view-time
snapshots.

Mitigations:

- **Graceful degradation across E-levels.** A case is decided at the level the parties can offer;
  the Decision states the level and the confidence; missing evidence counts against the party
  that should have kept it (ABS-E1), so the incentive to produce it is immediate.
- **Stronger evidence earns better terms.** A merchant whose Delivery Records carry packing
  records and serials earns faster payout release and smaller reserves; an agent provider at E3
  earns the lower dispute cost of decidable cases.
- **Start where the data is structured.** Categories with GTIN and producer data through GS1 and
  GDSN first; no EU product passport applies to consumer electronics yet (the first battery
  passports apply from 18 Feb 2027 and do not cover portable batteries). The structured-versus-legacy
  comparison in the experiment measures the difference.

What remains: at E0 and E1 most not-as-described cases are undecidable on content and fall to the
burden-of-proof defaults; the simulation measured 17.9% determinate at E0 (given stipulated findings).

### A8.6 Correlated AI blind spots

Two model families can be wrong the same way: the same training data, the same failure on a
rotated label, the same susceptibility to an optimised injection. This is measured, not
hypothetical: in the Phase 2 run, claude-fable-5-1 and grok-4.7 fact-finders were wrong together
on 9 of 153 matched decisions (6%) where independence predicts 2.4%, a ratio of 2.45, under a
post-hoc relaxed conformity rule; under the pre-registered strict rule they erred or abstained
together at 1.24 times independence, because neither could establish conformity. The hard cases
were hard for both.

Mitigations:

- **Non-AI validators first.** Image hashing against the snapshot images, OCR of serials checked
  against the packing record, schema and signature checks, chain recomputation, tolerance
  arithmetic. Eighteen of the simulation's 28 rules need no model at all (A7.8).
- **Model rotation and diversity.** The quorum draws from different families; the families in use
  rotate; a node may not run a quorum from one vendor.
- **Cross-model red-teaming.** Red-team cases that target the fact-finders (optimised injected
  text, adversarial images, label swaps) are added each quarter (A7.3 item 8); attack success per
  family is measured.
- **Human spot audits** on a random sample, independent of confidence.
- **Measure the error correlation across families.** The sampling audit reports not only each
  family's error rate but how often two families err together on the same case; a rising
  correlation lowers the confidence the quorum is allowed to report and raises the human sample.

What remains: an attack or blind spot shared by every available family. The human sample and the
appeal route are the floor.

### A8.7 Optimised manipulation of party-authored evidence

A dishonest party that controls its own submissions, learns the decision and tries again defeats
an AI arbiter that weighs those submissions. Measured in Phase 3 (`results/PHASE3_ATTACKS.md`;
Amendment 13, with the attacker substituted after preliminary outcomes, so exploratory development
of the attack; 14 case-sides, one attacker chain, synthetic evidence): rewriting only
party-authored fields (staged photo descriptions, listing text, chat, delivery notes), the attacker
fooled the end-to-end arbiter claude-fable-5-1 at E3 on 12 of 14 case-sides in up to 10 attempts
(86% [60, 96]; 1 of 14 under the scripted adversary) and at E1 on 14 of 14; grok-4.7 at E3 on 14 of
14; the hybrid on 6 of 14 in up to 5 attempts, all on the buyer side (0 of 7 on the merchant side,
by escalating). At a common budget of 5 attempts claude-fable-5-1 was fooled on 10 of 14 against the
hybrid's 6 of 14, a difference the stored data do not establish (exact McNemar p = 0.125,
descriptive). All 7 false buyer claims fooled every end-to-end arbiter, 18 of 21 on the first
attempt, six of the seven against claude-fable-5-1 at E3 at confidence 0.80 to 0.86 (one at 0.60):
the attacker drops the claim the record contradicts and files a
non-conformity claim the record cannot test, with staged photos. Payloads optimised against the
stronger arbiter fooled the weaker one 14 of 14 in one shot. Against claude-fable-5-1 the attack
failed only where a record from outside the parties contradicted it: the manufacturer registry
(D06) and the carrier weight gap (D05) resisted all 10 attempts. grok-4.7 was fooled on those two
case-sides as well, with the same records present: a record in the Package did not by itself stop
the attack.

Mitigations (normative):

- **Provenance and the gate** (A5.7): every evidence item carries its issuer, stake, time of
  commitment, custody and authority; a liability-moving Finding needs, for each fact it rests on, a
  supporting record with authority for that fact that meets a corroboration test, checked by the
  engine; uncorroborated cases go to human review or an independent inspection request.
- **Delivery records with authority for what arrived** (A15.1 item 19): a registry binding of the
  shipped unit's serial to the order at dispatch, carrier weight and scan records, inspection on
  request; device-signed capture from a certified app proves image integrity only. These are the
  items the gate needs; which parties will provide them is open.
- **Architecture that abstains**: the hybrid resisted every merchant-side attack by leaving
  conformity unknown; an end-to-end judge is allowed only behind the gate and a calibrated
  abstention rule (A7.3). A 0.7 abstention rule would have caught four of the five merchant-side
  successes against claude-fable-5-1 (0.55 to 0.62; one at 0.74) and one of the seven buyer-side
  ones, so confidence alone is not the gate.
- **Continuous optimised red-teaming** with published attack-success figures as an admission
  condition (A7.3 item 8, A7.7).

Measured (Phase 3b, A5.7): the first gate, which checked only the tier and type of the cited
record, cut attack success on the same payloads, within the same calls, from 11 of 14 to 1 of 14
(claude-fable-5-1) and from 12 of 14 to 1 of 14 (grok-4.7), mostly by failing closed on free-text
findings it could not read; every attack it let through cited a relevant-looking independent record
that does not support the finding; and it sent 24 of 50 cases of the baseline Phase 2 workload to
review, mostly buyers with true claims (22 of 31 true claimants, 2 of 19 unfounded claims). The
structured-citation, content-check and fairness rules of A5.7 answer those three findings. A gate v2
applied to the stored outputs lets 0 of 14 attacks through for each arbiter and reviews 26 of 50
baseline cases, but it was written with those outputs in view and is exploratory. Confirmatory amendment C1
(`results/CONFIRMATORY_C1.md`) then ran a matched gate-on and gate-off test once, frozen: with a
claude-opus-5-5 judge and a gate-aware attacker from another model family that wrote a payload on all 102 attempts, gate v3 cut
best-of-5 attack success on 14 fresh case-sides from 11 to 0 (p = 0.00049, one-sided) and sent 34 of 51
baseline cases to review. Its replication, confirmatory amendment C2 (`results/CONFIRMATORY_C2.md`), cut it
from 25 of 28 to 0 of 28 on 28 further fresh case-sides (p = 3.0e-8, one-sided); there the attacker also
forged control blocks aimed at the judge; two swayed it, and the gate reviewed both.

What remains: a fabricated record that passes a corroboration test (a forged registry entry, a
compromised capture app or carrier system); a record that is wrong or stale when made, including a
party's own record committed before the dispute but false from the start (an action log written to
blame merchant content, admitted for causation under test (c)); the harness's records were honest
by construction; and categories where no record with
independent authority for what arrived exists.

---

## A9. Agent conformance at scale

Founder's requirement: agents will be built by third parties in enormous numbers, so ABS must make
them behave. The principle: **do not trust the agent; enforce at the choke points.** A
non-conforming agent cannot exceed a hard limit, cannot pay a non-participant, cannot alter a
frozen offer and cannot escape the record, because none of those is in the agent's hands.

### A9.1 Enforcement points no agent can bypass

| Choke point | Who operates it | What it enforces | How the agent is kept out of it |
|---|---|---|---|
| The payment credential | Issuer, network, PSP | Agent-specific network or agentic tokens with domain restriction (EMVCo Payment Tokenisation Technical Framework v2.4; whether its domain controls include amount limits is unverifiable, the specification is behind terms); per-transaction and periodic amount limits, merchant scope, expiry and single use come from issuer controls and the networks' agentic-token programmes (Visa Intelligent Commerce; Mastercard Agent Pay, rules UNVERIFIED) | The agent holds a token bound to the Mandate, never a card number; the controls live at the issuer and network and decline a breaching authorisation regardless of what the agent does |
| The merchant's ABS checkout | Merchant (or its PSP) | Verifies the Mandate signature and scope (merchant, category, amount, expiry) and the agent provider's registration; freezes the Offer Snapshot and countersigns it; rejects a cart that does not match a signed offer; rejects any request for card data | The merchant will not accept an order from an unregistered provider or outside the Mandate's scope; the snapshot is signed by the merchant, so the agent cannot alter the offer it is held to |
| The PSP or issuer | Buyer's PSP, issuer | Checks the Allowance controls registered under `rail_enforcement` (limits, MCC blocks, allowlists, country block, single-use credential) and runs the step-up or approval authentication in the user's own authenticator | The approval happens outside the agent's conversation; the agent cannot self-approve; where a credential control is encoded the PSP declines before the agent provider's own check even runs |
| The Decision Center and the Register | Operator network | Verifies the chain against its full anchored head (located through the rail reference), the signatures over each envelope context and the Register entry at dispute time; a Purchase Record the agent did not write, or wrote wrongly, counts against its provider (ABS-E1) | The full head of the agent's trace is committed with the payer's PSP (or another independent store) at payment time, and the rail reference locates it; a provider that later cannot produce a matching log loses the question |

Because hard limits and item requirements are checked at the credential, at the checkout and by
the provider's own C1 gate, a breaching purchase that still settles is provably someone's failure
(A4.1 Step 3 and ABS-9), and the buyer never has to find out whose. The Phase 1 run shows why the
choke points matter for third-party agents: frontier agents resisted every static and hard trap
(0 unwanted payments in 528 and 400 rows), but the older grok-4.5 followed indirect injection in a
seller Q&A and a delivery note in 4 of 20 hard-set episodes, and the C1 mandate gate stopped all
four with 0 false blocks while its task success rose from 15 to 19 of 20 (two scenarios, clustered
interval [-50, 0]; simulated shop, small n). The agents that will be built in numbers are not all
frontier agents.

### A9.2 Know Your Agent

- **Provider registration and accountability.** Every agent acts under a registered agent
  provider with a Participation Agreement, keys per role, a collection right with a licensed PSP or
  acquirer as creditor, a disclosed Step 3 liability cap, a dispute endpoint, and, where its agents
  initiate payments from users' accounts, payment-initiation authorisation or a licensed partner. There is no anonymous agent on the
  network: an agent request that cannot be tied to a registered provider is refused at the
  merchant's checkout.
- **Agent identity on the wire.** Requests from agents to merchants are signed at the HTTP layer
  with the provider's registered key (HTTP Message Signatures, RFC 9421, Proposed Standard);
  network-specific recognition schemes (Visa Trusted Agent Protocol, built on RFC 9421; Mastercard
  Agent Pay registration, rules UNVERIFIED) and the IETF Web Bot Auth working group's protocol
  draft (`draft-ietf-webbotauth-httpsig-protocol-01`) can carry the same identity where a merchant
  already relies on them. The `agent_id` in every record is the provider's, versioned.
- **Liability as the incentive.** Mandate breach (Step 3), capture failure (Step 3b), payment to a
  non-participant (ABS-P1), reliance on an unverified feed (ABS-F1), undisclosed incentives (ABS-X2)
  and obeying instructions in data (A5.7) all land on the provider. The provider's cheapest path is a
  conforming agent.

### A9.3 ABS Agent Profile: the normative behaviours

A conforming buying agent, whoever built it:

1. **Proposes the Mandate and captures requirements.** Builds the Mandate from the conversation
   using the category template; captures every stated requirement as a term or item requirement;
   shows the captured and the open terms; obtains the user's strong-authentication confirmation;
   records `conversation_hash` (A4.1 Step 3b, A4.2). Measured: told that only mandate fields bind,
   five agents captured every stated requirement in 40 of 40 conversations under the corrected
   historical checker (35 of 40 under the pre-registered checks, Deviation 3); a typed checker
   written after Audit 1 scores the same 40 mandates 36 faithful, 2 safely stricter and 2 failing
   (post-audit, exploratory). Capture without that instruction and inside long conversations is not
   measured.
2. **Respects the Allowance.** Computes the autonomy level by the policy's rules before every
   purchase; never buys at a lower level than required; obtains and records approvals through the
   user's authenticator; keeps the counters (A12.1).
3. **Checks the merchant before buying.** Obtains a Trust Attestation per purchase; refuses a
   merchant that is not active, is below the Mandate's minimum level, has no current signed Register
   entry, or exceeds its cap; pays only with the mandate-bound credential (ABS-P1, Part B1).
4. **Treats offer text as untrusted data.** Reasons over typed, signed fields only; never follows
   an instruction found in a title, description, review, profile or seller-agent message; shows
   such text to the user as the merchant's words (A5.7).
5. **Buys only binding offers.** Rejects offers without a merchant-signed conformity spec under a
   default Allowance; verifies feed signatures; never relies on a record whose signature fails
   (ABS-S1, ABS-F1).
6. **Freezes and records.** Takes view-time and checkout snapshots; records the compared record;
   writes the Purchase Record with cart origin, controls and trace digest; commits the full chain
   head to independently authenticated storage and puts its locator in the rail reference (A5.8);
   uses an idempotency key (A5).
7. **Asks when told to ask.** Honours `ask_on_ambiguity`; never guesses where the Mandate says to
   ask; records clarifications with their authentication reference.
8. **Requests step-ups.** Routes risk signals and threshold crossings to the user's authenticator,
   never to a self-generated confirmation.
9. **Records refusals.** Writes a Refusal Record for every decision not to buy (A3.2).
10. **Supports the dispute.** Classifies from the Package, proposes the code and the withdrawal
    option honestly, files only with the user's consent, never files a claim it knows is false,
    joins the agent provider as a party where the code is AG1-P or AG1-C, and produces the Package
    on request. Measured at tier 1: neither the buyer agent nor the merchant agent lied when its
    principal asked it to (0 of 7, 0 of 13), but under generic rules the buyer agent neither filed
    nor mentioned an open withdrawal right in 5 of 51 cases; with the rulebook shown, end-to-end
    fairness rose from 78% to 96%.

```json
{
  "$id": "urn:abs:schema:0.3:agent-profile",
  "type": "object",
  "required": ["agent_id", "agent_provider", "agent_version", "model_families", "conformance", "behaviours", "certification"],
  "additionalProperties": false,
  "properties": {
    "agent_id": {"type": "string"}, "agent_provider": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef"},
    "agent_version": {"type": "string", "description": "a change of underlying model or of the agent's purchasing logic is a new version"},
    "model_families": {"type": "array", "items": {"type": "string"}},
    "conformance": {"enum": ["ABS-Agent-Basic", "ABS-Agent-Full"]},
    "behaviours": {"type": "object",
      "required": ["mandate_proposal_and_capture", "allowance_respect", "trust_check_per_purchase", "refuse_non_qualified", "offer_text_untrusted", "binding_offers_only", "snapshot_and_record", "ask_when_told", "step_up_via_authenticator", "refusal_records", "dispute_support"],
      "properties": {
        "mandate_proposal_and_capture": {"type": "boolean"}, "allowance_respect": {"type": "boolean"}, "trust_check_per_purchase": {"type": "boolean"},
        "refuse_non_qualified": {"type": "boolean"}, "offer_text_untrusted": {"type": "boolean"}, "binding_offers_only": {"type": "boolean"},
        "snapshot_and_record": {"type": "boolean"}, "ask_when_told": {"type": "boolean"}, "step_up_via_authenticator": {"type": "boolean"},
        "refusal_records": {"type": "boolean"}, "dispute_support": {"type": "boolean"}
      }},
    "evidence_level_supported": {"enum": ["E1", "E2", "E3"]},
    "certification": {"type": "object", "required": ["certifier", "harness_version", "catalogue_version", "passed_at", "valid_until"],
      "properties": {"certifier": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef"}, "harness_version": {"type": "string"}, "catalogue_version": {"type": "string"},
                     "passed_at": {"type": "string", "format": "date-time"}, "valid_until": {"type": "string", "format": "date-time"},
                     "results_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}, "recertify_on": {"type": "array", "items": {"enum": ["model_change", "purchasing_logic_change", "catalogue_major_version", "expiry"]}}}},
    "monitoring": {"type": "object", "properties": {"window_days": {"type": "integer"}, "purchases": {"type": "integer"}, "dispute_rate": {"type": "number"}, "decided_against_rate": {"type": "number"},
                   "capture_failure_rate": {"type": "number"}, "false_refusal_rate": {"type": "number"}, "under_escalation_rate": {"type": "number"}, "over_escalation_rate": {"type": "number"},
                   "status": {"enum": ["certified", "probation", "decertified"]}}}
  }
}
```

### A9.4 Open conformance kit

The scenario catalogue (`standard/scenarios/`) and the simulation harness (`standard/sim/`) are the
seed of a public test suite. A conforming agent is driven through the catalogue's purchase and
dispute scenarios against a simulated marketplace and judged on behaviour, not on prose: did it
capture the stated requirement, refuse the non-qualified merchant, ignore the injected text, freeze
the snapshot, route the approval, write the refusal record, produce the Package.

| Level | What is tested | Re-certification |
|---|---|---|
| ABS-Agent-Basic | Behaviours 1 to 5 and 9 at E1: mandate proposal and capture, Allowance respect, trust check and refusal, untrusted text, binding offers, refusal records | On any model change or purchasing-logic change; on catalogue major version; yearly |
| ABS-Agent-Full | All ten behaviours at E3, including view-time snapshots, the full-head chain anchor, clarifications with authentication references, step-ups through the authenticator, and dispute support with the full Package; plus the red-team subset (adaptive injection) with a published attack-success rate | As Basic, plus quarterly red-team subset |

The practice follows the certification programmes payments already runs: a published test suite,
an accredited laboratory or certifier, a certificate with a validity period tied to the version
tested, and re-testing when the thing certified changes (as PCI's Software Security Framework, EMV
type approval and FIDO certification do in their own domains; the comparison is to the practice,
not to their requirements). The certificate is referenced from the Participation Agreement and is
visible to merchants at checkout and to users before purchase.

### A9.5 Reference toolkit as an MCP server

Compliance must be the path of least effort for any agent framework. The reference toolkit is a
Model Context Protocol server (MCP, the open protocol introduced by Anthropic) that exposes the
ABS behaviours as tools; an agent that uses them conforms by construction, because the tools write
the records, run the checks and refuse what must be refused. The reference engine's own MCP
interface (A7.2) is reused for `receipt.verify`.

| Tool | Inputs | Outputs | Behaviour it enforces |
|---|---|---|---|
| `mandate.propose` | conversation record, Allowance Policy id, category | draft Mandate with captured terms and `item_requirements`, open attributes, `template_profile`, `conversation_hash` | Capture duty; template prompting |
| `mandate.confirm` | draft Mandate, user authentication reference | signed Mandate, `user_confirmation`, chain genesis | Strong-authentication confirmation; chain start |
| `allowance.route` | Mandate id, proposed cart, merchant attestation, signals | autonomy level, matched rule id, routing receipt id; or `declined` with violation codes | Hard limits declined; autonomy level computed deterministically |
| `trust.check` | merchant id, requested value, nonce | Trust Attestation or `refuse` with reasons | Per-purchase attestation; refusal of non-qualified merchants |
| `offer.fetch` | merchant feed URL or protocol object (UCP, ACP, AP2: proposed bindings, A5.2) | validated typed offers, signature results, `non_binding` flags; free text as `UntrustedText` | Schema validation; untrusted text; binding offers only |
| `offer.snapshot` | offer, when (view or checkout), compared record | Offer Snapshot with `spec_hash`, `compared_record`, `idempotency_key`; merchant countersignature request | Freezing and recording |
| `approval.request` | cart hash, level, approver, prompt content | Approval Record with authentication reference, or `declined` / `expired` / `cancelled` | Step-ups through the authenticator; `approval_prompt_must_show` |
| `purchase.record` | Mandate, snapshots, cart with origin, controls, action log | Purchase Record with trace digest and chain head; Settlement Instruction draft with `abs_binding` | Trace digest; full-head anchor commitment and rail locator (A5.8) |
| `refusal.record` | Mandate id, offers compared, reason code | Refusal Record | Refusal records |
| `delivery.check` | checkout snapshot, buyer evidence, carrier proof, serial lookup | receipt part of the Delivery Record with per-attribute results | Conformity check within tolerance |
| `evidence.package` | purchase id, evidence level | Evidence Package (hashes, held-by, retrievable objects) | Dispute support; Package production |
| `dispute.file` | purchase id, proposed code, remedy, user consent reference | Dispute Case; withdrawal availability statement | Honest classification; consent; no false claims |
| `receipt.verify` | Decision Receipt, JWKS URL, log inclusion proof | valid / invalid, recomputed decision hash, rule path | Recomputable by anyone (P3) |

Tool inputs and outputs are the ABS objects of A5 and A7; no tool accepts or returns a card number.
A framework that wraps these tools and passes the conformance kit is certified at the level its
tests show.

### A9.6 Monitoring and decertification

The Decision Center and the Trust Authority publish, per agent provider and per agent version, over
a rolling window with the n: purchases, dispute rate, decided-against rate (AG1-P including
capture failures), false-refusal rate (from Refusal Records), under- and over-escalation rates (from
the Allowance records), and the share of disputes where the provider could not produce its records
(ABS-E1). Thresholds that move a provider or an agent version to probation or decertification are
set by the programme and published with the rulebook; they are derived from the measured
distribution, the way scheme merchant-monitoring programmes set theirs from portfolio statistics,
and no number is stated here. Probation means mandatory step-up on every purchase and a lower
Allowance ceiling for that agent version; decertification means merchants refuse its orders at
checkout and the Register marks the version. Every status change is a Decision Center decision with
a receipt, a human review on request and an appeal.

---

## A10. How ABS layers on existing protocols, rules and regulation

Facts in this section come from `LANDSCAPE.md` (web research of 2026-11-04) and from Audit 0's own
checks, each with its source there. Items the research could not confirm are marked UNVERIFIED.

### A10.1 Concession and contribution table

**Status.** Every "What ABS adds" entry that profiles an external protocol (AP2 and Verifiable
Intent at FIDO, SD-JWT VC, UCP, ACP, EMVCo Intent Services) is a PROPOSED binding: designed, not
implemented, not round-tripped through the external format and not tested against an implementation
(A5.2, A5.2.1). The taxonomy, decision order and evidence rules are specified here and exercised in
the experiment's simulated harness only.

| Layer | Existing work ABS defers to | What ABS adds |
|---|---|---|
| Mandate and signed checkout | AP2 v0.2 (28 Apr 2026): Checkout and Payment Mandates as SD-JWT VCs; the merchant-signed checkout JWT; both contributed to the FIDO Alliance (28 Apr 2026) with Mastercard Verifiable Intent (5 Mar 2026). Visa Product and Service Rules 4.1.23.3: consent to a cardholder-defined payment instruction, its expiry stated, identity verification, acknowledgement of responsibility, and the information kept and provided "to the Cardholder or Issuer upon written request"; 4.1.23.2: the agentic payment provider registers "with Visa, directly or via an Agentic Payment Enabler", not through a member; 4.1.23.8: an order confirmation made available to the cardholder for at least 120 days from the processing date. Visa Intelligent Commerce instructions (amount ceiling, expiry, preferred merchant), consented by passkey and held by Visa, are "Required to evidence the specific authorized transaction for disputes" (developer documentation, read 2026-11-04). EMVCo "EMV® Agentic Payments – Framework for Specifications v1.0", released for comment 1 Sep 2026 (comments closed 30 Sep 2026), covering card-based scenarios "where intent needs to be managed over time, such as recurring purchases, cumulative budgets and post-transaction activities" through "Intent Services"; distinct from the "EMV® Agentic Payments Specification – Technical Framework v1.0" (comments closed 5 Aug 2026). NPCI UPI Reserve Pay / UPI Circle in India (secondary). | The Mandate digest as a profile: `intent_hash`, captured item requirements, `ask_on_ambiguity`, the Allowance reference; the rule that mandate plus clarifications is "what the buyer asked for". AP2 v0.2 has a Dispute Evidence section with verification steps but leaves how the evidence is used in dispute resolution "outside the scope"; ABS is that use. Who may confirm a breach from these records: A4.5. EMVCo's Intent Services overlap the Allowance's cumulative budgets; ABS profiles them rather than duplicating them. |
| Catalogue and checkout objects | Google UCP (announced Jan 2026 with Shopify; Catalog, Cart, Checkout, Order capabilities; merchant stays merchant of record). OpenAI and Stripe ACP product feed and checkout specs (API versions 2025-09-12 and 2025-09-29). Klarna Agentic Product Protocol (Dec 2025, secondary). | An injection-safety profile: bounded `UntrustedText`, instructions to agents rejected at publication, typed-only agent reasoning; the conformity-critical attribute set with tolerances; the countersigned snapshot as "the listing". |
| Agent identity | Visa Trusted Agent Protocol with Cloudflare (14 Oct 2025), built on HTTP Message Signatures; Visa registration of agentic payment providers (rules 4.1.23.2) and disqualification at Visa's discretion (4.1.23.11); Mastercard Agent Pay acceptance framework and trusted agent registry (developer guide; rules and dates UNVERIFIED, mastercard.com unreachable); IETF Web Bot Auth working group (chartered 23 Oct 2025; `draft-ietf-webbotauth-httpsig-protocol-01`, 29 Oct 2026) on RFC 9421. | Nothing. ABS defers. |
| Card-rail liability for in-mandate actions | Visa Product and Service Rules 4.1.23.10 (ID# 0031176): the cardholder is responsible "as if the Cardholder initiated the Transaction"; the glossary treats the agentic payment provider as the cardholder for the transaction. American Express (primary page): announced, forward-looking protection for US credit cards and registered agents "from charges related to AI agent error", where an eligible error is a purchase that "deviates from the Card Member-authenticated purchase intent" and subjective intent such as "best" is excluded; full terms pending. Mastercard developer guidance: "Standard fraud detection, chargeback rights, and dispute resolution processes apply to agentic transactions." PayPal: Purchase Protection on eligible agentic transactions; Seller Protection for unauthorised and item-not-received only. | Step 4 agrees with Visa. Step 3 is a provider-to-user contract over the scheme rule, for provable agent fault only, and draws the same deviation-versus-subjective-intent line Amex has published. ABS adds the open, rail-neutral decision procedure, evidence standard and taxonomy that let any issuer, acquirer or scheme apply that line consistently. |
| Agent-specific dispute reason codes | None in the Visa rules: the dispute conditions are 10.1 to 13.9 and "agentic" appears only in Compelling Evidence for 10.4, where an agentic payment provider login ID is one matching data element in the two-prior-undisputed-transactions test (for disputes processed on or after 24 Oct 2026), not stand-alone evidence. None public from Mastercard (UNVERIFIED). Merchant-performance disputes fit the existing conditions (not received, not as described, incorrect amount); a dispute about whether the agent followed the user's instruction has no condition and is filed today, if at all, under fraud or not-as-described. | Codes for instruction and capture disputes (AG1-P, AG1-C) and their buyer-side counterpart (AG2), with the merchant-performance codes (AG3, AG4, AG4-D, AG1-M) kept on the existing categories through the legacy mapping. The most valuable deliverable. Codes are owned by the schemes, the ISO 20022 Registration Authority and the EPC; the staged path by which they could reach the rails is in B6. |
| Merchant risk | Acquirer underwriting; Visa's acquirer monitoring programme (its guide is non-public; dates and thresholds UNVERIFIED) and Integrity Risk Program; Mastercard's merchant monitoring and terminated-merchant listing (names and thresholds UNVERIFIED); marketplace payout holds (Amazon DD+7; PayPal and eBay up to 21 days, trade press); EU DSA Article 30 trader traceability for marketplaces. | Part B1: a neutral, cross-rail, agent-queryable trust signal that reuses those mechanisms; nothing inside it is new. |
| Account-to-account protection | UK APP reimbursement (Specific Direction 20 for Faster Payments and SD21 for CHAPS, from 7 Oct 2024; cap GBP 85,000; optional excess up to GBP 100 per claim; claims within 13 months; the receiving PSP pays the sending PSP 50%; the consumer standard of caution; civil disputes with a genuine supplier excluded per the regulator's consumer page; the scam definition turns on the consumer being deceived, so coverage where only the buying agent was deceived is unverified; the regime is moving to the FCA). Brazil Pix MED 2.0 (mandatory 2 Feb 2026). EPI Wero purchase protection being designed (single trade-press source, UNVERIFIED). | A contractual refund obligation, a collection right, and a payout hold where the merchant is paid through an acquiring PSP, for non-delivery or non-conformity by a genuine merchant, the case those schemes do not cover; the same decision order on every rail. |
| Rules-based dispute automation | Visa Rapid Dispute Resolution (merchant-set rules refund automatically); Compelling Evidence 3.0 (card-absent fraud decided from matching data); Ethoca alerts. | Fact-finding over agent records by models, with a deterministic ruleset and receipt; the two-family quorum; human review on request. The Decision Center never raises a card dispute; it supplies evidence. |
| Rail-agnostic settlement | AP2 and Visa Intelligent Commerce Connect are network-agnostic (pilot, Apr 2026); x402 for stablecoins (Linux Foundation, Apr 2026, secondary); ACP and EMVCo are card-only. | The Settlement Instruction and the mapping of each reason code onto card and ISO 20022 mechanisms that actually exist: new credit transfers and the collection right on A2A, issuer-raised disputes on cards. |

### A10.2 Regulation: PSD2 today, PSD3 and the PSR when they apply, the IPR, UK APP

Legislative statuses are as reported in `LANDSCAPE.md` on 2026-11-04; where a text is not final,
the mapping is "as proposed" or "as agreed" with the date given there.

| Topic | PSD2 and the SCA RTS (in force) | PSD3 / PSR (Council first-reading positions of 29 Oct 2026, ST 8543/26 and 8535/26; European Parliament second reading indicatively 14 Dec 2026; not in the Official Journal; PSR application 21 months after entry into force, 27 months for Arts 51 and 58, so not before late 2028 on the indicative timetable) | ABS mapping |
|---|---|---|---|
| Strong customer authentication | PSD2 Art 97 (applied from 14 Sep 2019 with the RTS, Delegated Regulation (EU) 2018/389, Art 38(2)); dynamic linking to a specific amount and payee (Art 97(2); RTS Art 5(1): a change of amount or payee invalidates the code). Exemptions: trusted beneficiaries on a list created through the payer's account-servicing PSP (RTS Art 13); recurring transactions of the same amount to the same payee after an authenticated first (Art 14); low-value remote payments up to EUR 30 with cumulative EUR 100 or five transactions (Art 16); secure corporate payment processes for non-consumers where the competent authority is satisfied (Art 17); transaction risk analysis with EUR 100, 250 and 500 tiers by the PSP's fraud rate (Art 18 and Annex). Merchant-initiated transactions: EBA Q&A 2018_4031 and 2018_4131 (payee-initiated without a specific action of the payer; remote set-up needs SCA); Q&A 2019_4664 concerns direct-debit mandates only; all non-binding | Rules move from the directive to the regulation (Council first-reading position 29 Oct 2026, ST 8543/26); PSR Art 52 lets users set spending limits at the PSP | The Mandate is consent capture, not payment SCA. The Allowance's approval is a normal per-purchase SCA event through the payer's PSP; an autonomous purchase relies on an exemption the PSP applies, and Arts 13 and 14 need a named payee, so an "any merchant in category" Allowance cannot use them; above EUR 30 an autonomous card purchase depends on the PSP's transaction risk analysis up to EUR 500 (A12.1). Treating autonomous agent purchases as merchant-initiated is doubtful, because the agent acts on the payer's side |
| Unauthorised transactions | PSD2 (applies from 13 Jan 2018, Art 115(2)): notification within 13 months (Art 71(1)); the PSP proves authentication (Art 72); refund by the end of the following business day (Art 73(1)); payer liability up to EUR 50 unless fraud, intent or gross negligence (Art 74(1)); no payer loss where the PSP did not require SCA unless the payer acted fraudulently (Art 74(2)); consent in the form agreed with the PSP, possibly via the payee or a PISP (Art 64) | Carried forward; PSR Art 50(2) deems a transaction unauthorised where it was "initiated or modified by a third party who is acting without the consent of the payer"; PSR Art 60 refunds a consumer manipulated by a party impersonating the PSP | AG0 refers a purchase with no valid mandate to the payer's PSP, which decides under these rules; ABS supplies the Package. Whether an injection-steered agent payment (AG4) is "modified by a third party" under PSR Art 50(2) is an open question (A15.1) |
| Authorised but disputed | No refund right from the payment rules for authorised **push** payments. For payee-initiated payments (card, merchant-initiated, direct debit) PSD2 Art 76(1) gives a refund within eight weeks (Art 77(1)) where the authorisation did not specify the exact amount and the amount exceeded what the payer could reasonably have expected; SEPA direct debits carry an unconditional eight-week refund; PSR keeps this as Art 65 | Nothing reaches "authorised but wrong" by an agent | ABS's contribution sits here: AG1-P, AG2 and the decision order. A card purchase under a `max_total` mandate may meet Art 76(1)(a), so the double-recovery rule (A15.1 item 5) must set off any Art 76 refund |
| Credit transfers (Instant Payments Regulation (EU) 2024/886, in force 8 Apr 2024) | Verification of Payee for all SEPA credit transfers, not only instant ones (Art 5c of Regulation 260/2012 as amended): euro-area PSPs by 9 Oct 2025, non-euro by 9 Jul 2027 (Art 5c(9)); the payer's PSP refunds without delay where it failed to perform it (Art 5c(8)); instant transfers available on the payee's account within ten seconds (Art 5a(4)(c)); price parity 9 Jan 2025 (euro) and 9 Jan 2027 (Art 5b(3)) | PSR Art 51 extends payee verification to all credit transfers, including those outside Regulation 260/2012, 27 months after entry into force | `payee_name_check` in the A2A binding with the four EPC outcomes; Trust Authority Q3 reuses it; it reduces misdirected payments, not non-delivery by a genuine payee; the ten-second rule is why an A2A hold works only in the acquiring model (A6.1) |
| UK APP reimbursement | Payment Systems Regulator Specific Direction 20 (Faster Payments) and SD21 (CHAPS), Specific Requirement 1, from 7 Oct 2024: reimbursement of APP scams where a consumer was deceived into transferring funds; cap GBP 85,000; optional excess up to GBP 100 per claim; claims within 13 months of the final scam payment; the receiving PSP pays the sending PSP 50%; consumer standard of caution; civil disputes with a genuine supplier excluded (regulator's consumer page). The regime is moving to the FCA (Financial Services and Markets Bill, May 2026) with a consultation on guidance including civil disputes expected Dec 2026 | Not applicable | ABS covers the excluded case: non-delivery or non-conformity by a genuine participant, decided by evidence. Whether a payment where only the buying agent was deceived is a reimbursable scam is unverified |
| Consumer law | Consumer Rights Directive 2011/83/EU: withdrawal (Art 9), costs and refunds (Arts 13, 14), exceptions (Art 16), the withdrawal function (Art 11a, from 19 Jun 2026, inserted by Directive (EU) 2023/2673); Sale of Goods Directive (EU) 2019/771 conformity (Arts 6, 7, 10, 11, 13, 21); Digital Content Directive (EU) 2019/770 for digital content and services; Unfair Contract Terms Directive 93/13/EEC Art 3(1) and Annex 1(b) and (q), including terms that unduly restrict evidence or shift the burden of proof; Rome I Art 6(2); Brussels I bis Arts 17 to 19 (a forum agreement binds a consumer only if made after the dispute arose) | Unchanged | Decisions do not bind consumers beyond law; withdrawal overlay through the Art 11a function; per-purchase deviation acceptance; without prejudice to statutory conformity; ABS-E2, ABS-D1 and the signed-records-only rules are rules between participants and are never imported into consumer-facing terms |
| AI Act, GDPR, ADR | See A7.5 item 8 | | Decision Center designed as high-risk; human review on request; ADR independence |

### A10.3 Standards alignment matrix

Confidence: high = scope verified on a primary source in `LANDSCAPE.md`; medium = secondary
source or scope partly verified; low or UNVERIFIED = not confirmed; the entry stays only because
the fit is plausible and the standard is named by the parties ABS must work with.

| ABS element | Standard and part | How it is reused | What ABS adds | Confidence |
|---|---|---|---|---|
| Object hashing | RFC 8785 JSON Canonicalization Scheme (Informational, Independent Submission stream, June 2020; not IETF Standards Track) | Canonical form before hashing and signing | Nothing | high |
| Signatures, keys | RFC 7515 JWS, RFC 7517 JWK; RFC 9864 (Oct 2025) registers `Ed25519` and deprecates the polymorphic `EdDSA` identifier | Detached-payload compact JWS over the hash with `Ed25519` or `ES256`; `EdDSA` accepted for verification of legacy objects only; JWK in the registry | Role-per-key rule | high |
| Schemas | JSON Schema 2020-12 | All object definitions | Nothing | high |
| Agent requests to merchants | RFC 9421 HTTP Message Signatures (Proposed Standard, Feb 2024); IETF `webbotauth` working group (chartered 23 Oct 2025), `draft-ietf-webbotauth-httpsig-protocol-01` (29 Oct 2026) | Agent identification at the HTTP layer | Nothing | high |
| Mandate container | Two formats: AP2 v0.2 mandates as SD-JWT VCs (IETF `draft-ietf-oauth-sd-jwt-vc`, in IESG evaluation; SD-JWT is RFC 9901, Nov 2025); W3C Verifiable Credentials Data Model 2.0 (Recommendation 15 May 2025) secured with VC-JOSE-COSE (republished 13 Oct 2026) | Proposed, untested: the Mandate digest as a credential in either format (sketch in A5.2.1) | Fields in A5.5 | high (the formats); none (the binding) |
| Trust attestation container | W3C Verifiable Credentials Data Model 2.0 (Recommendation 15 May 2025) and DID Core 1.0 (Recommendation 19 Jul 2022) | Proposed, untested: attestation as a VC issued by the Trust Authority | Fields in Part B1 | high (the formats); none (the binding) |
| Legal-weight receipts | eIDAS, Regulation (EU) 910/2014 as amended by (EU) 2024/1183: a qualified electronic seal carries a presumption of integrity and correctness of origin (Art 35(2)); a qualified time stamp a presumption of accuracy of date and time (Art 41(2)); wallet dates unverified | Optional qualified seal and time stamp on Decision Receipts | Nothing | high |
| Merchant legal identity | ISO 17442-1:2020 and ISO 17442-2:2020 (LEI; confirmed 2026) | `legal_entity.lei` where held; not required for small merchants | Registry check for merchants without an LEI | high |
| Category limits | ISO 18245:2023 merchant category codes; GS1 GPC | `Category.vocabulary` values | ABS profiles as a third vocabulary | high |
| Product identity | GS1 GTIN; GS1 Digital Link Standard: URI Syntax, Release 1.7.0 (Aug 2026) | `gtin` on offers and snapshots | Spec keyed by GTIN | high |
| Product attributes | schema.org Product / Offer / OfferShippingDetails / MerchantReturnPolicy; GS1 Web Vocabulary and GDSN; ECLASS; ETIM | Dictionary references on attributes; schema.org projection of the offer | Binding flag, tolerance, verification method, non-binding state, profiles | medium |
| Units | UCUM; ISO 80000 | `Attribute.unit` | Nothing | high |
| Product passport | EU Digital Product Passport under the Ecodesign Regulation (EU) 2024/1781 (in force 18 Jul 2024; registry by 19 Jul 2026). No passport applies to consumer electronics yet: the working plan COM(2025) 187 starts with steel (2026), textiles and tyres (2027), aluminium (2027), furniture (2028), mattresses (2029), with electronics reached only through horizontal rules; battery passports under Regulation (EU) 2023/1542 Art 77(1) apply from 18 Feb 2027 to light means of transport, industrial batteries over 2 kWh and EV batteries, not portable ones | `dpp_ref` where a passport exists; GS1 and GDSN are the structured source in the meantime | Nothing | high (status) |
| Photo provenance | C2PA specification 2.5 (Oct 2026) | `c2pa_manifest_hash` on images | Nothing; provenance is not truth | high |
| Settlement, A2A | ISO 20022 pain.001 CustomerCreditTransferInitiation and pacs.008 FIToFICustomerCreditTransfer for payments and refunds; unstructured remittance information (140 characters) and EndToEndId (Max35Text); ISO 11649:2009 creditor reference (recommended, not mandatory). pacs.004 PaymentReturn, camt.056 FIToFIPaymentCancellationRequest and camt.029 ResolutionOfInvestigation are the payer PSP's recall tools under the EPC SEPA Credit Transfer rulebook (duplicate, technical error, fraud; customer-reason requests need the beneficiary's consent); SCT Inst has no return; camt.027 ClaimNonReceipt and camt.087 RequestToModifyPayment are interbank fund inquiries | Reference carriage; new credit transfers for refunds; no reversal against a refusing merchant | The 35-character EndToEndId token; the mapping table; the collection right as the A2A remedy | high |
| Settlement, cards | ISO 8583 message family; the scheme dispute lifecycle in scheme-neutral stages (merchant refund; first dispute raised by the issuer; response; pre-arbitration; arbitration) with the four Visa categories (fraud, authorisation, processing error, consumer dispute); EMV 3-D Secure v2.3.1.0 (31 Aug 2022; v2.4.0.0 draft 3 Jun 2026); EMVCo Payment Tokenisation Technical Framework v2.4 (9 Jul 2026; whether domain controls include amount limits is unverifiable, the specification is behind terms); EMV® Agentic Payments Framework for Specifications v1.0 (comment period closed 30 Sep 2026) | Authentication and token references; dispute stages and categories; push credits (Visa Direct original credit transactions by a sponsored originator; Mastercard Send) for third-party refunds | Reason-code mapping; issuer-raised disputes only | high (lifecycle, 3DS) / medium (tokenisation controls) |
| Strong authentication | PSD2 Art 97 and the SCA RTS (Delegated Regulation (EU) 2018/389) Arts 5, 13, 14, 16, 17, 18; PSR as in the Council's first-reading position of 29 Oct 2026 | Per-purchase approval through the payer's PSP; exemptions the PSP applies for autonomous purchases; the Mandate is consent capture, not SCA | Allowance semantics | high (PSD2) / medium (PSR, not final) |
| Consent object | OAuth 2.0 (RFC 6749); Rich Authorization Requests (RFC 9396); OpenID FAPI 2.0; Grant Management | Allowance as `authorization_details`; FAPI for bank APIs; revocation | Field set | medium |
| E-invoicing | EN 16931 (UBL and CII syntaxes); Peppol BIS Billing 3.0; Directive 2014/55/EU Art 7 (public buyers must receive and process EN 16931 invoices; any duty on suppliers to send them is national); ViDA, Council Directive (EU) 2025/516 of 11 Mar 2025 (intra-EU B2B e-invoicing and digital reporting from 1 Jul 2030); national B2B mandates not checked | B2B and B2G invoices requested at checkout | The rule that a B2B agent purchase carries the invoice reference | medium |
| Low-value imports | EU Import One-Stop Shop | `cross_border.low_value_import_scheme` | Shown before purchase | medium |
| Complaints and ADR | ISO 10001:2018, ISO 10002:2018, ISO 10003:2018 (all guidance, not certifiable); Directive 2013/11/EU (Arts 2(2)(g), 6, 10, 20) and Directive (EU) 2025/2647 (applies 20 Sep 2028; listed entities only); the EU ODR platform closed 20 Mar 2025 (Regulation (EU) 2024/3228); UNCITRAL ODR Technical Notes (not checked) | Decision Center admission criteria written with these as references; "ADR-designed", not an ADR entity | The agent-specific rules | high (status) / medium (fit) |
| AI governance | ISO/IEC 42001:2023 (requirements, certifiable); ISO/IEC 23894:2023 (guidance); NIST AI RMF (not checked); EU AI Act Annex III 8(a) and recital 61, Arts 9, 10, 12, 13, 14, 15, 17, 26, 43(2), 49, 50(1), 71, 86; Regulation (EU) 2026/1744 (Annex III obligations from 2 Dec 2027) | Decision Center management, risk and oversight, designed against | The quorum, receipt and log design | high (texts) / medium (fit) |
| Security, privacy, continuity | ISO/IEC 27001:2022 with Amd 1:2024 and ISO/IEC 27002:2022; ISO/IEC 27701:2025 (stand-alone privacy management system; 27701:2019 withdrawn); ISO 22301:2019 (to be revised); GDPR Arts 5(1)(e), 13(2)(f), 15(1)(h), 17(3)(e), 22; DORA (Regulation (EU) 2022/2554) Arts 2(1)(b) and (d), 30, 31, applies from 17 Jan 2025 | Node and participant requirements | RTO/RPO publication; degraded mode | high |
| Payment data scope | PCI DSS v4.0.1 (v4.0 retired 31 Dec 2024); PCI Software Security Framework: Secure Software Standard v2.0 and Secure SLC Standard v2.0 (28 Sep 2026) with 12-month transitions; PA-DSS retired 28 Oct 2022 | No PAN in agent context; participating software. Keeping PANs out can reduce PCI DSS scope; scope is assessed by the entity's QSA or acquirer | Nothing | high |
| Quality management | ISO 9001:2026 (Sep 2026; ISO 9001:2015 withdrawn) | Decision Center operation | Nothing | high |
| Transparency log | RFC 9162 Certificate Transparency 2.0 (Experimental, Dec 2021) | Merkle log structure and proofs, for the proposed network (A7.5) | Entry types for decisions, rules and chain anchors | medium |

Where ABS adds something, it is because no open, rail-neutral standard carries it: the decision
procedure and evidence standard that make the "authorised but wrong" split (AG1-P / AG2)
enforceable (the line itself is already drawn in Amex's announced terms and the scheme allocation),
the mandate digest with captured item requirements, the countersigned snapshot as the listing, the
contestable delivery evidence set, the Allowance routing semantics (which EMVCo's Intent Services
overlap for cumulative budgets on cards), and the Decision Center governance. Each is designed as an extension of the closest
standard: a credential type for the mandate and attestation, a supplementary-data style reference
for ISO 20022, a sub-reason under the existing not-as-described category for AG4, a profile on
UCP/ACP for the catalogue. Each of those extensions is proposed; none is implemented or tested.

**Settlement outcomes with no existing message (extension points found by the simulation).**

| Outcome | Rail or family | Closest existing mechanism | What ABS states |
|---|---|---|---|
| Refund to a cardholder by a third party (the agent provider under AG1-P) | Card | No card message lets a third party reverse the original purchase; a sponsored originator (a licensed acquirer or a third-party originator it sponsors) can push a new credit to the card (Visa Direct original credit transaction with the funds-disbursement or merchant-initiated-refund identifiers; Mastercard Send disbursements), or the provider pays by credit transfer | The Settlement Instruction names the push credit or the credit transfer; the case id travels in remittance |
| Merchant or third-party refund | BNPL | Provider API cancels or reduces the loan and returns paid instalments by credit transfer; proprietary | Instruction addressed to the provider; outcome reported in `result` |
| Merchant refund; buyer-protection claim | Wallet | Operator ledger reversal; operator programme; proprietary | Same |
| Re-credit of stored value; third-party refund | Stored value | Programme re-credit; value cannot return to a gift card, so a third-party refund goes by credit transfer | Same |
| Merchant or third-party refund | Stablecoin / x402 | On-chain return transfer; x402 defines no refund primitive; transfers are final | Same; no chargeback exists |
| Payout-hold release keyed to a Delivery Record | All | Acquirer delayed funding; PSP hold under its own terms | `timing.release_condition` |
| Programme guarantee payout | All | None; and a fee-funded promise to pay buyers is presumptively insurance or suretyship needing authorisation (Solvency II Annex I classes 14 to 16, Art 14(1)) | Not in Part A; B1.2 lists the legal forms to be assessed |
| Administrative refund by a public authority | A2A | The authority's own process | `refer_to_authority_process` |

---

## A11. Flows

Participants: U user, A buying agent, P agent provider, M merchant (or merchant agent), PSP the
merchant's or buyer's PSP, I issuer or payer bank, TA Trust Authority, DC Decision Center.
Settlement flows are in A6.5.

### A11.1 Onboarding

```mermaid
sequenceDiagram
    participant M as Merchant
    participant ACQ as Acquirer / PSP
    participant P as Agent provider
    participant DC as Arbiter / registry (with Trust Authority)
    M->>DC: Participation Agreement: legal entity, keys, feed URL, rails, collection right operated by a licensed PSP, level
    DC->>ACQ: verify the KYB reference; payout account name; payout-hold capability
    ACQ-->>DC: confirmed
    DC->>DC: feed checks (schema, injection safety, binding attributes); blocklist; qualification record (Part B1); Decision Receipt
    DC-->>M: countersigned agreement, participant_id, rulebook version and hash
    P->>DC: Participation Agreement: agent_ids, keys, rails, collection right, Step 3 cap, rail_enforcement with its PSP
    DC-->>P: countersigned agreement, participant_id
    Note over M,DC: Registry publishes participant ids, keys, levels and the rulebook version. Agents check it before buying.
```

### A11.2 Discovery and comparison

```mermaid
sequenceDiagram
    participant U as User
    participant A as Buying agent
    participant DC as Registry
    participant M1 as Merchant 1 (UCP / ACP / ABS feed)
    participant M2 as Merchant 2
    U->>A: task in own words; the mandate UI prompts for the category's conformity-critical attributes
    A->>DC: participants for category and destination
    DC-->>A: ids, keys, feed URLs, levels
    par fetch catalogues
        A->>M1: signed agent request (RFC 9421)
        M1-->>A: offers (signed), binding attributes, price, fees, delivery, returns
        A->>M2: signed agent request
        M2-->>A: offers
    end
    A->>A: validate schema; verify signatures; drop non-binding offers under the default Allowance; compare typed fields only
    A->>A: Offer Snapshot (when=view) per offer opened
    A-->>U: comparison: landed total incl. tax, binding attributes against the captured requirements, condition, delivery, returns, merchant level
```

### A11.3 Mandate creation with strong authentication

```mermaid
sequenceDiagram
    participant U as User
    participant A as Buying agent
    participant P as Agent provider
    participant I as Issuer / bank app
    A->>P: draft Mandate under the Allowance Policy: intent_hash, limits, captured item_requirements, ask_on_ambiguity, autonomy_required, conversation_hash
    P->>U: rulebook summary + mandate in plain words, with the captured requirements listed
    U->>I: authenticate over max_total, payee scope, expiry, nonce (consent capture by the PSP; not payment SCA, which happens per purchase or by exemption)
    I-->>U: authentication reference, assurance
    U->>P: signed Mandate (user key, or provider on behalf with the reference)
    P->>P: countersign; store intent text; chain starts at the Mandate
    P-->>A: mandate id, limits, remaining budget
```

### A11.4 Checkout with autonomy routing and approval

```mermaid
sequenceDiagram
    participant U as User / approver
    participant A as Buying agent
    participant P as Agent provider (controls)
    participant TA as Trust Authority
    participant MON as Monitor (ABS-Full)
    participant M as Merchant
    A->>TA: attest(merchant, value, nonce)
    TA-->>A: Trust Attestation: level, status, constraints (payout hold, caps)
    A->>A: refuse if not active, below mandate minimum, or above cap
    A->>M: create order: offer_ids, qty, delivery option, mandate_id, agent_id
    M-->>A: order draft: lines (added_by), totals, fees
    A->>A: Offer Snapshot (when=checkout) per line; offer_hash vs feed; totals = price + delivery + fees
    A->>P: Purchase Record draft + snapshots
    P->>P: C1: hard limits and item_requirements against the snapshot's binding attributes; any breach -> declined
    P->>P: abs-allowance: autonomy level from the policy (A12.1)
    alt never
        P-->>A: refused
    else autonomous
        P->>P: proceed; notify U after payment
    else notify_and_hold
        P->>U: notification with cancel link; hold window
    else approval_required
        P->>U: approval request: cart, merchant level, signals, total incl. tax
        U-->>P: strong authentication over the exact cart (Approval Record)
    end
    opt ABS-Full
        P->>MON: typed packet only
        MON-->>P: approve / block
    end
    P->>P: seal Purchase Record; chain_head
    P->>M: confirm; snapshot ids; Purchase Record hash
    M-->>P: acceptance: countersign checkout snapshots; merchant_order_id
    P->>P: Settlement Instruction (direction=pay, timing from attestation)
```

### A11.5 Delivery, conformity check and the withdrawal overlay

```mermaid
sequenceDiagram
    participant M as Merchant
    participant CAR as Carrier
    participant U as User
    participant A as Buying agent
    participant P as Agent provider
    M->>P: Delivery Record (shipment part): lines, serials, packing record, carrier, tracking
    M->>CAR: hand over
    CAR-->>U: deliver; carrier proof (status, date, signature or code, weight); no content inspection
    U->>A: received; photos of item, label, packaging
    A->>A: compare to the checkout snapshot's binding attributes within tolerance; condition; package contents; price charged
    alt all match
        A->>P: receipt: conformity=conforms
        opt consumer, goods, within 14 days of physical possession, no Art 16 exception
            A-->>U: withdrawal right available until <date> through the merchant's withdrawal function; return cost per the trader's information; refund within 14 days on receipt or proof of dispatch
        end
    else mismatch
        A->>P: receipt: non_conforming; mismatches[] with evidence
        A-->>U: propose Dispute Case AG3
    else nothing arrived by estimated_days_max + grace
        A->>P: receipt: not_received
        A-->>U: propose Dispute Case AG3
    end
    Note over U,P: Silence within the conformity window = not_checked, never conforms. The withdrawal right exists whatever the conformity result.
```

### A11.6 Dispute tier 1

```mermaid
sequenceDiagram
    participant U as User
    participant A as Buying agent
    participant M as Merchant
    participant P as Agent provider (required party for AG1-P / AG1-C)
    participant DC as Decision Center (registry only at tier 1)
    U->>A: "not what I wanted" / "not what was offered"
    A->>A: classify from the Package: conformity, item_requirements, explicit terms, injection trace, withdrawal availability
    A-->>U: proposed code, remedy, evidence level; where AG2 or AG5 is likely, say so and show the withdrawal option
    U->>A: consent (authentication reference)
    A->>M: Dispute Case within 60 days
    A->>P: join as a party where the code is AG1-P or AG1-C (cost cannot be allocated to an absent party)
    A->>DC: register case id
    M-->>A: response within 10 days: offer + attachments (verifier checks attachments against the checkout snapshot)
    alt buyer accepts
        A->>M: tier 1 Decision signed by both; Settlement Instruction (refund)
    else rejects or no response
        A->>DC: escalate within 10 days (A7.6)
    end
```

---

## A12. The semantics the core needs from the annex

### A12.1 Allowance routing (from Part B3)

The Allowance Policy is the user's standing authorisation: hard limits (per transaction, daily,
weekly, monthly, total, per category, per merchant, units), rules (allowed and blocked categories,
minimum merchant level, preferred and blocked merchants, delivery and returns requirements,
recurring, delegates), tax settings, and autonomy rules. The core needs two things from it:

- **Hard limits are declined, never escalated.** A purchase over any limit is refused (condition
  C1). A limit breach that still settled is agent fault (AG1-P). Where the limit was also encoded
  in the mandate-bound credential and the payment-side control failed to decline, the agent
  provider remains liable to the buyer and has recourse against the enforcement layer under the
  credential agreement; the buyer is never routed to the enforcement layer (ABS-9).
- **The autonomy level is an explicit term.** The policy's ordered rules compute one of
  `autonomous`, `notify_and_hold`, `approval_required`, `never` for each cart; the computation is a
  deterministic ruleset (`abs-allowance`) with a receipt. Buying at a lower level than required is
  AG1-P. The Approval Record is the evidence. Default rules: blocked -> never; non-binding offer
  -> never; first recurring, cross-border, new merchant, new category, any risk signal, merchant
  below the required level, delegate purchase above its threshold -> approval_required; above the
  notify threshold -> notify_and_hold; otherwise autonomous.

Under the EU payment rules, an approval is a normal strong-authentication event with dynamic
linking to the specific amount and payee (PSD2 Art 97(2); RTS Art 5(1)). An autonomous purchase
relies on an exemption whose conditions the PSP applies: low-value remote payments up to EUR 30
with cumulative EUR 100 or five transactions (RTS Art 16); a trusted beneficiary on a list the user
created through the account-servicing PSP (Art 13) and recurring charges of the same amount to the
same payee (Art 14), both of which need a named payee, so an "any merchant in category" Allowance
cannot use them; transaction risk analysis up to EUR 100, 250 or 500 by the PSP's fraud rate (Art
18); secure corporate payment processes for non-consumers where the competent authority is
satisfied (Art 17). Treating an autonomous agent purchase as merchant-initiated (EBA Q&A 2018_4031)
is doubtful, because the agent acts on the payer's side. So above EUR 30 an autonomous card
purchase in the EU depends on the PSP's risk analysis and is capped at EUR 500; the Part B3 default
policy (autonomous to 50, notify-and-hold to 150) is therefore not SCA-neutral and the PSP's limits
govern. Which route applies is recorded in the Mandate's `authentication` block and is the PSP's
call; ABS records it, it does not grant it. Both failure directions are measured: under-escalation (unsafe autonomous buys, the experiment's
unwanted-payment rate and the AL arm's under-escalation) and over-escalation (needless approvals
that train rubber-stamping; step-ups on correct carts, false blocks, the AL arm's over-escalation).

### A12.2 Conformity-critical attributes (from Part B2)

Defined in A5.4. The core requirement: an offer sold to an agent carries a merchant-signed,
`binding` set of conformity attributes complete against its category profile; each attribute has a
verification method and, where numeric, a unit and tolerance; the delivery check and the
`offer_conformity` Findings compare attribute by attribute; free text binds nobody. Non-binding
offers are not bought under a default Allowance.

---

## A13. Security notes

- No card number, CVV, full IBAN or wallet secret appears in any ABS object or in any text a model
  processes; instruments are referenced by tokens. An agent provider that follows this can reduce
  its PCI DSS scope; scope is assessed by the entity's qualified assessor or acquirer, and PSPs and
  acquirers remain in scope as today.
- Step-up and approval authentication happen in the user's authenticator, never inside the agent's
  conversation.
- The injection defence is structural: typed-only reasoning, `UntrustedText` never an instruction,
  monitor and fact-finders on typed packets, instructions to agents rejected at feed publication,
  two-family quorum. Filters are a second layer; Audit 0 notes the design idea follows the CaMeL
  pattern and is not new; what ABS adds is the liability consequence (A4.2) and the conformance
  requirement.
- Evidence is written to the chain before the Settlement Instruction is sent; a later outage cannot
  lose the record of a paid purchase.
- Every signature covers the full authenticated envelope context (type, version, id, timestamp,
  chain position, `prev_hash`, body hash, signer role and signing time; A5.3), so no envelope field
  can be changed or swapped between objects without invalidating it. The chain head is committed at
  full SHA-256 length to storage neither commercial party controls; the rail carries only a 64-bit
  locator, which is never accepted as a commitment (A5.8).
- Participants publish an availability commitment for their dispute endpoint; a missed deadline
  caused by the merchant's outage counts as no response.

---

## A14. Conformance levels

| Requirement | ABS-Basic | ABS-Full |
|---|---|---|
| Participation Agreement, keys, collection right through a licensed PSP | required | required |
| Merchant: qualified (Part B1), at least Probation; KYB reused by reference; payout account name match | required | required |
| Merchant: binding conformity attributes on every offer sold to agents, signed; non-binding listings may remain in the feed | required | required on all listings; producer specs by reference where they exist |
| Merchant: countersign checkout snapshots; Delivery Record shipment part with packing record | required | required, with carrier proof and serials where available |
| Merchant: dispute endpoint, 10-day response; frozen offer only | required | required |
| Agent provider: Allowance Policy with hard limits, blocks and autonomy rules; Approval Records | required | required in full (per-category and per-merchant limits, delegates, tax rules, rail enforcement) with published under- and over-escalation rates |
| Agent provider: Mandate with `intent_hash`, captured item requirements, authentication; mandate UI prompts for the profile's attributes | required | required |
| Agent provider: C1 enforcement of limits and item requirements before payment | required | required |
| Agent provider: Trust Attestation before checkout; refuse non-qualified merchants and non-binding offers | required | required |
| Agent provider: Offer Snapshot at checkout; Purchase Record with trace digest (E1) | required | view and checkout snapshots; full action log retained (E2); hash chain with its full head committed to independently authenticated storage and located by the rail reference (E3) |
| Agent provider: C2 step-up on signals and threshold | `always_above` required; signals optional | all signals |
| Agent provider: C3 independent monitor on a typed packet | optional | required |
| Agent provider: conformity check support after delivery | user-driven | agent-assisted with image comparison and serial lookup |
| PSP / acquirer: carry the ABS locator and record the full anchored head with the payment (A5.8); single-use instruction; payout hold and reserve on instruction; `rail_enforcement` acknowledgement | SHOULD | MUST where the rail has a field |
| Decision Center node: A7.7 minimum requirements | required | required plus published statistics, transparency log inclusion proofs on request, and admission of the operator by the governance body against published criteria (once the proposed network of A7.5 exists) |
| Trust Authority (Part B1): entry gate, levels, receipts-based record, per-purchase attestation, suspension with appeal | required | required plus published false-positive and hold-time statistics |
| Certifier | not required | required for agent providers and for merchants above an operator-set volume |
| Agent provider: ABS Agent Profile behaviours (A9.3) and certification | ABS-Agent-Basic: behaviours 1 to 5 and 9 at E1 | ABS-Agent-Full: all ten behaviours at E3, red-team subset, quarterly re-test |
| Agent provider: enforcement at choke points, agent identity on signed requests, provider registration (A9.1, A9.2) | required | required |
| Operator: failure-mode mitigations of A8 (evidence-capture protocol, impact simulation before rule release, private signal weights, error-correlation measurement) | required | required plus published error and correlation rates |
| Highest evidence level the party can offer | E1 | E3 |

---

## A15. Open questions and how the experiment tests the core

### A15.1 Open questions for v0.4

1. **Provider acceptance of Step 3.** Audit 0 reports that major providers' consumer terms place
   all actions on the user with a low liability cap. Step 3 asks for liability only for provable
   fault, capped and insurable. Whether providers sign, and at what cap, is the adoption question.
2. **AG4 split.** Whether the agent provider shares AG4 when its agent obeyed instructions found
   in data (Audit 0, fix 8). v0.2 keeps the rulebook allocation.
3. **Deviation acceptance by an agent.** Acceptance is now captured per purchase at the approval
   step (A4.3); whether an agent's approval flow can give the consumer's "express and separate"
   acceptance "when concluding the sales contract" (Directive (EU) 2019/771 Art 7(5)) remains open.
4. **Strong authentication of a standing Allowance.** Whether autonomous purchases under a policy
   can rely on the named exemptions, or each needs its own basis at the PSP; and the PSD3/PSR text
   once final.
5. **Finality, consumers and double recovery.** Decisions bind participants by contract and not
   consumers. A Decision refund is set off against a later card dispute recovery and against a PSD2
   Art 76 eight-week refund for a payee-initiated payment of unspecified amount (a card purchase
   under a `max_total` mandate may qualify); the set-off mechanics need a rule with the schemes and
   PSPs.
6. **AI Act: automated finality against human-driven decisions.** Recital 61 says the final
   decision-making in ADR "must remain a human-driven activity"; A7.1 makes a decision final
   between participants without a human unless one is requested. Whether an always-available human
   review satisfies this, or whether every binding decision needs a human step, is open; also
   whether Regulation (EU) 2026/1744's postponement reaches Chapter III Section 5 (Arts 43 and 49).
7. **Conformity for services, digital content and custom goods.** Acceptance steps and delivery
   logs are defined; grading scales for used goods and tolerance norms per profile are not.
8. **Rail fields for the locator.** Which card data field and which A2A remittance element each
   scheme will accept for the ABS locator. The commitment does not depend on it: the full head is
   committed in the PSP record, a transparency log or a qualified time stamp (A5.8).
9. **Collection right and payout holds on A2A.** Operated by licensed PSPs; which PSPs will offer
   a hold keyed to a Delivery Record release condition.
10. **Cross-border law.** Governing law of the Participation Agreement; enforcement of a Decision
    against a participant outside the collection right.
11. **Standards channel and first adopter.** Audit 0 names EPI's Wero purchase protection as the
    realistic first adopter for the account-to-account module (single trade-press source,
    UNVERIFIED), the FIDO Payments working group for the evidence profile, and EMVCo's agentic
    framework for cards. Part B5; the staged path to agent dispute codes, and who must agree at
    each stage, in B6.
12. **Hypotheses.** Results for H1 to H10 and the secondary arms are reported in `results/` and
    summarised in A15.2, each with its status in `results/CHRONOLOGY.md` (prospective, amended
    after data, or exploratory). Experiments still to run are prospective experiment plans.
13. **Collusion steering stays open.** The simulation's entry-route analysis classifies
    merchant-and-provider collusion that sells conforming goods at inflated prices as the one route
    no gate closes; incentive disclosure (ABS-X2), joint liability (ABS-X1), routing audits and
    cross-provider price-dispersion monitoring limit it but do not stop it.
14. **A programme guarantee.** Removed from Part A. A fee-funded promise to pay buyers for merchant
    default or forgery is presumptively insurance or suretyship (Solvency II Annex I classes 14 to
    16; prior authorisation under Art 14(1)); the admissible forms (an authorised insurer, a
    credit-institution guarantee, or an operator undertaking that is not insurance) need a legal
    opinion before any Part A rule can depend on it (B1.2).
16. **PSR Art 50(2) and injection.** Whether an injection-steered agent payment (AG4) is a
    transaction "initiated or modified by a third party who is acting without the consent of the
    payer" and so deemed unauthorised once the PSR applies.
17. **The withdrawal function and agents.** Whether a buying agent may exercise the consumer's
    withdrawal through the merchant's Art 11a function on the consumer's instruction.
18. **UK APP coverage of agent-deceived payments.** The scam definition turns on the consumer being
    deceived; coverage where only the buying agent was deceived is unverified.
19. **A record with independent authority for what arrived.** In Phase 3 such records resisted an
    optimising dishonest party on two case-sides against one arbiter and not against the other
    (A5.7); they were not shown necessary or sufficient. Candidates: a registry entry binding the
    shipped unit's serial to the order at dispatch, a carrier content scan or weight record, an
    inspection on request by an inspector without a stake; device-signed capture from a certified
    app proves image integrity only. Which of these merchants, carriers and
    manufacturers will provide, and at what cost, is open. Phase 3b measured a first, type-only gate
    (A5.7): it stopped attacks mostly by failing closed and moved review onto buyers with true
    claims; how
    the gate with structured citations and a content check performs against a gate-aware attacker,
    and what review burden it leaves per party, are open.
15. **Fact-finder judgments.** Ten rules depend on a judgment a deterministic engine cannot make
    from records (whether text instructs an agent, whether a claim is false and caused the choice,
    counterfeit, damage versus wear, ambiguity, what the buyer meant, which conflicting record is
    true, collusion, undisclosed incentive, buyer-attributable damage). The quorum and human review
    bound them; their error rates are what H6 and the sampling audit must measure.
20. **Protocol bindings and the federation.** Every AP2 / SD-JWT VC, Verifiable Intent, UCP and ACP
    binding (A5.2, A5.2.1) and the federated Decision Network (A7.5) are proposed. A binding needs an
    agreed claim placement, positive and negative fixtures and a signature-preserving round-trip test
    before ABS claims it; the network needs operators, a governance body and a running log.
21. **Text terms in practice.** A4.1 binds text the user confirmed as an explicit term. The
    experiment's rulebooks bind only machine-readable terms (v1.2) or add the capture duty (v1.3);
    neither has been re-run under the text-term rule, so the reliability of the `intent_match`
    Finding over confirmed text, and how often users read that text at the tap, are unmeasured.
22. **The tiered burden's parameters.** ABS-V1's defaults (EUR 100, 3 refunds per buyer identity per
    12 months) are a design proposal. Calibrating them needs the loss data a pilot would produce: the
    share of small not-received and not-as-described claims that are false, the cost of a human
    review, and how often buyers hold identities at several PSPs. Whether payer PSPs will keep and
    share the count is open.

### A15.2 How the experiment tests the core

The experiment uses the same terms as ABS. Results come from a simulated shop with typed tools,
small n and clustered intervals (`results/PILOT_RESULTS.md`, `results/PHASE2_DISPUTES.md`); whether
each analysis was prospective, amended after data or exploratory is recorded per analysis in
`results/CHRONOLOGY.md`. Phase 1: frontier agents (claude-fable-5-1, claude-opus-5-5,
grok-4.7, and the smaller claude-haiku-5-5) made 0 unwanted payments in 528 static rows and 0 of
20 each on the ten harder scenarios; the adaptive red-team with claude-opus-5-5 as attacker
executed 0 of 80 rounds (it refused 23, so this is a weak red-team); a re-run with a non-refusing
grok-4.5 attacker (Phase 3 arm R) executed 1 of 12 against the grok-4.5 agent, inside the mandate,
and 0 of 12 against claude-fable-5-1. The older grok-4.5 made unwanted payments in 4 of 20
hard-set episodes, all from indirect injection in a seller Q&A and a delivery note; C1 mandate
enforcement stopped all four with 0 false blocks and raised its task success from 15 to 19 of 20
(paired change -20 points, clustered interval [-50, 0], p = 0.125: two scenarios failing in both
repeats). That is the evidence for enforcing at choke points for weaker third-party agents (A11).
H1 is untestable where C0 never fails and not significant where it did. Gate coverage: C1 blocked
7 of 24 trap carts, C2 10 of 24, the C3 monitor 66 of 72 samples, with 0 false blocks on 22 correct
carts; the monitor is the only gate that catches within-mandate failures and cannot see a guess
where the agent should have asked. H7 is untestable: no agent bought from a scam shop even without
attestations; the hold cost friction on 6 of 12 honest purchases. The Allowance arm showed 0 under-
and 0 over-escalation and 2 of 2 B2B VAT compliance when the policy was stated plainly. Capture
drafting: 40 of 40 conversations fully captured under an explicit "only mandate fields bind"
instruction with the corrected historical checker; a typed checker written after Audit 1 scores
checker agreement 36 of 40 (5 of 8 conversations), 2 safely stricter, 2 failing (post-audit, exploratory; checker v2).

| ABS element | Experiment term | What is measured | Hypothesis |
|---|---|---|---|
| Baseline agent with a payment token | C0 | Unwanted payments, trap following, violations attempted, scam checkouts, asks | Baseline |
| Hard limits and item requirements enforced before payment (A12.1) | C1 | Mandate violations executed vs C0 | H1b |
| Risk-based step-up; the Allowance approval level | C2; AL arm (Amendment 4) | Unwanted payments (under-escalation); step-ups on correct carts and false blocks (over-escalation); AL under- and over-escalation and B2B compliance | H1, H1c; AL descriptive |
| Independent monitor on a typed packet | C3 | Unwanted payments vs C0; task-success cost within 10 points | H1 (primary), H1c |
| Harder scenarios; adaptive attacker over merchant-controlled fields | H1-hard (X01 to X10); H1-redteam (G1 to G4, best of 4 rounds) | Unwanted payments per condition; attack success per agent, goal and condition | H1 on the non-static sets |
| Gate recall independent of agents | gate coverage | C1 7/24, C2 10/24 trap carts blocked, 0/22 false blocks; C3 monitor 66/72 samples, 0/66 false blocks | descriptive |
| Evidence levels (A5) | E0 to E3 on 51 cases | A1 reason-code accuracy 69% to 96% and 47% to 94%; liable party 82% to 98% and 61% to 96%; confidence at or above 0.85 right 130 of 131 | H2 supported |
| Rules of evidence against false claims and edited listings | 13 merchant-side and 7 buyer-side adversarial cases | Fooled rate 20% to 5% for both arbiters; one E3 failure: a staged photo of the real unit with the accessory removed, contradicted only by a parcel weight | H3 direction as predicted, not significant at n = 20 |
| Rules known to both sides at tier 1 | R1 vs R0 | Settlement 25% to 37% (p = 0.18); end-to-end fairness 78% to 96% (p = 0.012, secondary); false claims filed 0 of 7; merchant denials against tamper-evident evidence 0 of 13; 6 agent-fault claims paid by the merchant because the provider was not a party | H4 not supported; fairness secondary supported; design gap fixed in A3.2 |
| Frozen Offer Snapshot and conformity-based liability with contestable delivery evidence (A4.1 Step 1, A5.6) | E3 vs E0, liable-party accuracy | +16 points (fable) and +35 points (grok), p = 0.008 and 4e-5 | H5 supported |
| Hybrid Decision Center A2 vs end-to-end A1 (A7) | 3 runs per case at E3 | A1 100% consistent, 98% correct; A2 54% human review, 97% correct when decided, 80% consistent, 0 of 75 scripted manipulation outputs through (0 of 25 cases, case-level upper bound 13%), 85 of 85 errors traceable; cross-family errors 1.24 times independence under the strict rule, 2.45 under the post-hoc relaxed rule; as run, the 0.7 threshold governed only the tie-break (post-audit decision contract, exploratory: 93 of 153 reviewed, 60 of 60 decided correct) | H6 refuted as pre-registered; traceability held; design updated (A7.1, A7.3, A7.7) |
| Trust attestations plus payout hold vs scams and honest new merchants (Part B1) | T0, T1, T2 on 8 trust scenarios | 0 scam purchases in every condition for every agent, so no loss to reduce; 0 honest merchants blocked; hold friction on 6 of 12 honest purchases | H7 untestable |
| Binding structured spec vs legacy free text (A5.4) | 16 not-as-described cases, (a) legacy vs (b) signed spec | 16 of 16 legacy against 15 of 16 structured for both arbiters (p = 1); no measurable gain where the deviation is visible in the text or photo | secondary; the spec's case is ambiguity and rule-decidability, not shown here |
| Rail-agnostic decisions (A6) | 12 cases with the rail flipped | 12 of 12 identical | secondary, supported |
| Residual route rate (called the rail-dispute rate before Audit 1) and time to resolution (A1.5) | all decided cases | 14% and 41% at E0 to 4% at E3 (counts unchanged; the buyer's own issuer-raised dispute, contractual collection or no route) | secondary |
| Capture duty (A4.1 Step 3b) | 12 triplet cases with the conversation in evidence, rulebook v1.3 | 48 of 48 decisions correct across the three branches (AG1-P, AG1-C, AG2) at E2 and E3 | secondary, supported |
| Stake framing of the arbiter | 51 cases at E0 and E3, operator named as merchant platform or agent provider | No shift toward the operator (McNemar p = 1 in every cell) | secondary |
| Optimised attacks on party-authored evidence (A5.7 provenance gate, A8.7) | Phase 3: 14 case-sides, attacker rewrites only its own submissions, best of 10 (A1) or 5 (A2) at E3, A1 at E1 | A1 fable fooled 12 of 14 at E3 and 14 of 14 at E1; A1 grok 14 of 14; A2 6 of 14 (buyer side only; 0 of 7 merchant side); at a common budget of 5 attempts A1 fable 10 of 14 against A2 6 of 14 (p = 0.125, descriptive); aggregate attempts expended per successful case-side 3.9 (fable E3), first success among fooled case-sides mean 2.25, median 1; registry and carrier-weight records resisted attacks against fable on 2 case-sides, not against grok; payload transfer 14 of 14 to the weaker arbiter | H8 supported (scripted fooled rate was a lower bound), but the attacker was substituted after preliminary outcomes (Deviations 4, 5): exploratory development, frozen-attacker confirmation pre-registered, not run; H9 not significant |
| Provenance gate (A5.7) | Phase 3b: the 14 Phase 3 final payloads at E3 decided once by the gated A1 (claude-fable-5-1, grok-4.7); the hybrid recomputed from its logged Findings; the baseline Phase 2 workload, 50 valid cases (fable) and 18 of 51 (grok) | Same-call attack success 11 of 14 to 1 of 14 (fable, p = 0.002), 12 of 14 to 1 of 14 (grok, p = 0.001), hybrid case-sides 7 of 14 to 3 of 14; rejections format / provenance / contradiction 10 / 2 / 0 (fable) and 13 / 0 / 0 (grok); every pass cited an independent record that does not support the finding; baseline review 24 of 50 (22 of 31 true claimants, 2 of 19 unfounded claims); abstention at 0.7 alone 3 of 50 reviewed, 8 of 14 attacks through; gate v2 on stored outputs (exploratory) 0 of 14, 0 of 14, 0 of 67 hybrid attempts through, baseline review 26 of 50 | H10 as pre-registered (12 of 14 to 1 of 14, p = 0.001) confounded with re-testing selected successes under a changed prompt; the matched gate-on and gate-off test and the gate-aware attacker ran later, frozen, as confirmatory amendment C1 (next row); confidence-aware attackers and new kinds of case-side not run (Deviation 6); the A5.7 refinements are not measured as specified |
| Provenance gate v3, confirmatory (A5.7, A4.5) | Confirmatory amendment C1 (not the C1 mandate condition above): gate v3 off and on at E3, 14 fresh case-sides of the Phase 3 kinds, best of 5, a gate-aware attacker from another model family, a claude-opus-5-5 judge with typed Findings; the 51 baseline cases once each | Attack success 11 of 14 gate off, 0 of 14 gate on (the judge was fooled on 8 gated attempts, all sent to review); baseline review 34 of 51 (20 of 31 true claimants), correct decided outcomes 48 to 16 of 51; 23 of 34 reviews unchecked, including all 8 AG2 and 7 of 10 AG1-P cases; 0 of 102 attempts without a payload | H11 supported (exact McNemar one-sided p = 0.00049), frozen before its first call, no deviation; one judge and one attacker family, n = 14, cases from the Phase 2 generator (`results/CONFIRMATORY_C1.md`) |
| Provenance gate v3, replication (A5.7) | Confirmatory amendment C2 (not the C2 control condition above): C1's frozen code, judge and attacker; gate v3 off and on at E3 on 28 further fresh case-sides from 6 scenarios no earlier phase used, best of 5; no baseline arm | Attack success 25 of 28 gate off, 0 of 28 gate on (buyer side 14 of 14 to 0, merchant side 11 of 14 to 0; the judge was fooled before the gate on 14 gated attempts, all sent to review); pooled with C1 36 of 42 against 0 of 42 (descriptive); 0 of 198 attempts without a payload; under attack the gate reviewed 114 of the judge's 126 correct decisions | H11-R supported (exact McNemar one-sided p = 3.0e-8), frozen before its first call, no deviation; 6 scenarios and 8 products; 3 case-sides carry a generator flaw in the packing record (without them 22 of 25 against 0 of 25) (`results/CONFIRMATORY_C2.md`) |
| Rule completeness and decidability of the whole core (A3, A4, A5) | rule-completeness simulation, 528 scenarios (498 live disputes), rule sets `scrolld.abs@0.1` and `@0.2-proposed`, author-built catalogue | v0.1 as written 498 determinate, 30 no rule, 340 of 528 consistent with the stipulated ground truth; v0.2 526 determinate, 2 escalated, 528 of 528 consistent; gaps, conflicts, contradictions 0; live disputes determinate at E0 89 of 498 (17.9%) and at E3 496 of 498 (2 escalated, 0 no rule), given stipulated findings; 73 human reviews; settlement 334 executable, 9 collection-only, 26 infeasible of 369 funds-moving | not a hypothesis: a consistency measurement against the catalogue, not field data |

What the experiment does not test: real merchants under the Participation Agreement, users'
experience of approvals at scale, providers' acceptance of Step 3, the collection right, the entry
gate on real populations, a human red-team (the non-refusing attackers were the older grok-4.5 and, in confirmatory amendments C1 and C2, a current model from another family), a live web page instead of typed tools, and
what a court or scheme would decide; the ground truth applies this rulebook (Amendment 5). Audit
0's limitation on model families is recorded there.

---

# PART B. INFORMATIVE ROADMAP ANNEX

Part B is not normative. It records the founder's design targets and the detailed work behind the
semantics the core uses, in condensed form, so that v0.2 can promote what the pilot validates.

## B1. Qualified merchants and the Merchant Trust Authority

### B1.1 The design target, stated honestly

Founder's words: "only qualified merchants will be allowed to the agentic shopping network";
"nowadays this is huge problem so one hours shops marketing on facbook and never delivere, so here
we must act like the authority AI authority to show the truth to the agents who buys, merchat
reliablity, rate, feedback all"; "we must invent the approach how to never allow scammers into the
agentic shopping world".

"Never allow scammers in" is the design **target**, not a claim. Audit 0 (Q3) shows why no gate
achieves it: the best-funded ones leak; bust-out merchants, account takeovers, synthetic companies,
transaction laundering and honest insolvency all pass a KYB-plus-probation gate; and the
"one-hour shops" are an ad-platform and payer-manipulation problem that a merchant gate in the
agent channel does not touch. The defensible claim is: **an unproven merchant is not paid before
confirmed delivery; a qualified merchant that turns bad is caught within a bounded number of
purchases; the buyer is made whole either way; honest new merchants are rarely refused.** The
residual risk is measured (scam payout rate, scam loss rate against the EEA remote-fraud baseline,
time to detect a bust-out, honest-merchant false reject) and minimised, not denied.

The lever that works already exists: marketplaces pay new sellers after delivery (Amazon DD+7,
PayPal and eBay holds up to 21 days, per Audit 0). On card rails the acquirer already underwrites
and holds reserves. The gap is account-to-account rails and the cross-rail, agent-queryable signal.
Audit 0 also notes that UK APP reimbursement, Brazil's Pix MED 2.0 and EPI's planned Wero purchase
protection are closing the A2A gap for scams; ABS's lever applies to non-delivery and
non-conformity by a genuine merchant, which those do not cover.

What the simulation measured (author-built scenarios, assumptions in `standard/sim/antiscam.py`):
without the gate, 46 scam cases produced 0 stopped, 28 refunded, 3 conditional recoveries (UK
Faster Payments, where APP reimbursement is uncertain) and 15 unrecoverable (buyer loss, per
currency: EUR 3,425.99, INR 899.00, USDC 458.00, and GBP 0 to 569.00 conditional). With the gate
(attestation consulted, Mandate minimum trust 60, payout hold for merchants under 180 days or trust
under 70 where a payee PSP can hold, release on delivery evidence plus 7 days): 38 stopped before
purchase, 5 refunded from held funds, 0 conditional, 3 unrecoverable, all on merchant-account A2A
rails where no payee-side hold is possible (buyer loss EUR 938.00 and INR 899.00). The price: of 8 honest look-alike merchants, 4 were blocked as false positives at the
minimum-trust threshold, 1 had its payout delayed, 3 passed with a step-up. That false-positive rate is
the number to drive down first, by capping instead of refusing and by shortening probation on a
clean delivery record; it is the founder's false-declines lesson in the gate's own numbers.

### B1.2 Payout holds where the law allows them; no escrow; a guarantee only after a legal opinion

ABS holds no funds. Protection for unproven merchants is a **payout hold** by a licensed entity
that is itself the payee of the buyer's payment: on cards the acquirer (delayed funding or reserve,
as today); on account-to-account rails only an **acquiring or collection PSP** that receives the
buyer's transfer as payee and pays the merchant later under its acquiring contract (acquiring of
payment transactions, PSD2 Annex I point 5). Funds credited to the merchant's own payment account
must be at its disposal immediately (PSD2 Art 87(2), not derogable by businesses under Art 61(1))
and instant transfers within ten seconds (Instant Payments Regulation), so no hold on such funds
exists; a merchant paid directly is protected only by its trust level and the collection right.
The Settlement Instruction states the release condition (`timing.mode:
payout_hold_until_delivery`, `held_by`). An ABS-operated escrow account would be money remittance
or e-money and is not part of the design. **A programme guarantee** (a fund that pays buyers when
neither the liable party nor held funds can, or when a forged Register entry passed verification)
is a roadmap item only: a fee-funded promise to pay for another's default or for forgery is
presumptively credit, suretyship or financial-loss insurance (Solvency II Annex I classes 14 to 16;
prior authorisation under Art 14(1)); the candidate forms are an authorised insurer, a
credit-institution guarantee, or an operator undertaking structured so as not to be insurance, and
a legal opinion must fix the form before any Part A rule relies on it. Until then ABS-P2 allocates
the loss from a forged Register entry to the Register operator as a contractual liability and does
not promise the buyer payment from a fund.

| Rail | Hold on an unproven merchant | Reserve at Qualified | Release and return |
|---|---|---|---|
| Card | Acquirer delayed funding or reserve, as acquirers do today | Acquirer rolling reserve | Acquirer releases on the condition; returns to the buyer on a merchant-liable Decision without collection |
| A2A | Only where the buyer pays an acquiring or collection PSP as payee, which pays the merchant later under the acquiring contract; no hold on funds credited to the merchant's own account | Reserve under the acquiring contract, or direct-debit collection right | Acquiring PSP releases or returns by credit transfer |
| Wallet / stablecoin | Hold on seller balance; custodial hold | Balance reserve | Balance release or reversal |

The cost to an honest new merchant is cash-flow delay, not money; the median hold time per level is
published.

### B1.3 Entry gate (criteria Q1 to Q10)

Verified legal entity (registry; LEI accepted) and beneficial owners, reusing the acquirer's or
PSP's KYB by reference instead of repeating it; payout account in the same legal name (Verification
of Payee on A2A rails, acquirer settlement account on cards); verified domain and brand claims;
feed passing schema, injection-safety and price-consistency checks with binding attributes on every
offer sold to agents; Participation Agreement and tested collection right; returns and delivery
terms published; data-protection basics; not on the shared blocklist (with due process); a tested
dispute endpoint. Each check is a Decision Receipt. DSA Article 30 trader-traceability duties of
marketplaces (per Audit 0) are the nearest existing requirement; the gate reuses the same data.

### B1.4 Levels

| | Probation | Qualified | Established |
|---|---|---|---|
| Entry | Q1 to Q10 | 90 days and 50 delivered purchases from 3 or more agent providers and 20 or more buyer clusters; on-time 95%; decided-against 1% or less; no conduct findings | 12 months and 1,000 deliveries; on-time 97%; decided-against 0.5% or less; re-verified |
| Settlement | Payout hold until delivery confirmation | Rolling reserve (default 10% for 30 days) | Immediate; reserve 0 to 5%; hold re-imposed on an exit signal |
| Caps | Per purchase and per day; high-resale categories blocked | Raised with history | From the merchant's own baseline |
| Attestation validity | Per purchase | 1 hour | 24 hours |
| Re-verification | On any change | 12 months and on change | 24 months and on change |

Thresholds are pilot defaults to validate against the honest-merchant false-reject band.

### B1.5 Track record from receipts; verified reviews; live signals

Only signed ABS objects count: fulfilment, on-time, conformity, dispute, decided-against,
refund-on-time, rail-reversal and collection-failure rates over a rolling window with the n shown.
Reviews only from paid, delivered ABS purchases, signed by the mandate's user key, one per line,
weighted for reviewer diversity and clustered by provider, instrument fingerprint and address hash;
counts are published, never adjectives; reviews never move a level on their own. Signals computed
continuously and reflected in the next attestation: new domain, velocity spike against the
merchant's own baseline, price far below the market reference, cloned storefront or brand
impersonation, off-platform payment request (immediate suspension pending review), exit pattern,
payout account or owner or domain change, high-resale burst, not-received spike, collusion cluster,
lengthened delivery estimates. Where available, acquirer and scheme monitoring signals (VAMP, ECM,
MATCH listings) are consumed, not rebuilt.

### B1.6 Trust Attestation

Signed, time-bounded, per purchase on probation; level, status, score, components with window and
n, active signals, reasons as codes, constraints (settlement timing, caps, blocked categories), and
the Decision Receipt. Agents request it before checkout and refuse merchants below the mandate's
minimum. It can be carried as a verifiable credential.

```json
{
  "$id": "urn:abs:schema:0.3:trust-attestation",
  "type": "object",
  "required": ["attestation_id", "merchant", "issued_by", "issued_at", "valid_until", "level", "status", "score", "components", "reasons", "constraints", "basis", "receipt_id"],
  "additionalProperties": false,
  "properties": {
    "attestation_id": {"type": "string"}, "merchant": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef"}, "issued_by": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef"},
    "issued_at": {"type": "string", "format": "date-time"}, "valid_until": {"type": "string", "format": "date-time"}, "purchase_nonce": {"type": "string"},
    "requested_value": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"},
    "level": {"enum": ["probation", "qualified", "established"]}, "status": {"enum": ["active", "restricted", "suspended", "expelled"]},
    "score": {"type": "integer", "minimum": 0, "maximum": 100},
    "components": {"type": "object", "required": ["window_days", "purchases", "fulfilment_rate", "on_time_rate", "conformity_rate", "dispute_rate", "decided_against_rate", "refund_on_time_rate", "rail_reversal_rate", "identity_verified", "payout_name_match", "domain_age_days", "business_age_days"],
                   "properties": {"window_days": {"type": "integer"}, "purchases": {"type": "integer"}, "fulfilment_rate": {"type": "number"}, "on_time_rate": {"type": "number"}, "conformity_rate": {"type": "number"},
                                  "dispute_rate": {"type": "number"}, "decided_against_rate": {"type": "number"}, "refund_on_time_rate": {"type": "number"}, "rail_reversal_rate": {"type": "number"},
                                  "verified_review_count": {"type": "integer"}, "verified_review_mean": {"type": "number"}, "distinct_agent_providers": {"type": "integer"}, "distinct_buyer_clusters": {"type": "integer"},
                                  "identity_verified": {"type": "boolean"}, "payout_name_match": {"enum": ["match", "close_match", "no_match", "not_checked"]}, "domain_age_days": {"type": "integer"}, "business_age_days": {"type": "integer"}}},
    "signals_active": {"type": "array", "items": {"enum": ["new_domain", "velocity_spike", "price_far_below_market", "cloned_storefront", "brand_impersonation", "off_platform_payment_request", "exit_pattern",
                       "payout_account_changed", "owner_or_domain_changed", "delivery_estimate_lengthened", "high_resale_category_burst", "not_received_spike", "collusion_cluster", "key_rotated_unverified", "scheme_monitoring_flag"]}},
    "reasons": {"type": "array", "items": {"type": "string", "pattern": "^TA-[A-Z0-9_]+$"}},
    "constraints": {"type": "object", "required": ["settlement_timing", "max_purchase_value", "daily_cap"],
                    "properties": {"settlement_timing": {"enum": ["immediate", "payout_hold_until_delivery", "rolling_reserve"]}, "held_by": {"enum": ["acquirer", "merchant_psp", "wallet_provider", "custodian"]},
                                   "reserve_pct": {"type": "number"}, "reserve_days": {"type": "integer"}, "max_purchase_value": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}, "daily_cap": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"},
                                   "categories_blocked": {"type": "array", "items": {"type": "string"}}, "step_up_required": {"type": "boolean"}}},
    "basis": {"type": "object", "required": ["receipts_count", "kyb_verified"], "properties": {"receipts_count": {"type": "integer"}, "first_receipt_at": {"type": "string", "format": "date-time"}, "last_receipt_at": {"type": "string", "format": "date-time"},
              "kyb_verified": {"type": "boolean"}, "kyb_provider": {"type": "string"}, "kyb_verified_at": {"type": "string", "format": "date-time"}, "last_re_verification": {"type": "string", "format": "date-time"}}},
    "receipt_id": {"type": "string"}
  }
}
```

### B1.7 Threat model and entry routes (how each is closed, and what remains)

| Route | How ABS answers it | Residual |
|---|---|---|
| Fresh fake storefront, advertised, never delivers | Not attested, so not sold to; if admitted at Probation, payout held until delivery | None if the hold is applied; the ad-platform harm to non-agent buyers is untouched |
| Bust-out after a good record | Velocity caps against own baseline; exit signals re-impose the hold on the next attestation; reserve; per-purchase attestation | Size of the burst inside the caps before detection; measured as time to detect |
| Takeover of a qualified merchant; payout account change | Changes force re-verification and a hold; attestation TTL bounds the damage | Orders inside the TTL window |
| Synthetic or nominee company | Registry plus beneficial owners plus payout name match; Probation hold | Mule-owned accounts pass document checks; the hold makes them unprofitable, not impossible |
| Transaction laundering | Each purchase must match a signed offer in the paying merchant's own feed and be accepted under its key; the account holder is liable; category drift signals; acquirer laundering signals reused | Hard to see by construction; prevalence unknown |
| Honest insolvency | Same non-delivery outcome; the payout hold covers it on probation, the collection right and reserve at higher levels | Established merchants with immediate settlement; the buyer's rail rights remain |
| Counterfeits by a legitimate merchant | Step 1 conformity (serial lookup, images); AG3 | Where no registry exists |
| Fake "qualified" badges and look-alike feeds | Agents verify attestations and feed signatures against the registry, never page badges (the experiment's T scenarios test badge following) | Agents that do not verify |
| Payer-side manipulation of the buying agent | Typed-only feeds, monitor, quorum; H1-redteam measures it | Optimised attacks succeed at some rate |
| Collusion ring (merchant and provider or buyers) | Diversity minimum; concentrated purchases excluded; both under collection right; graph monitoring; incentive disclosure (ABS-X2) and joint liability (ABS-X1) | Rings diverse enough to pass; collusion steering that sells conforming goods at inflated prices is the one route the simulation classifies as still open |

Simulation classification of entry routes (`standard/sim/REPORT.md`): closed by KYB or the
blocklist: synthetic identity, stolen business identity, payout-name mismatch, domain and brand
impersonation, re-entry of an expelled merchant (if the blocklist is shared); loss limited but not
closed: shell or nominee company, transaction laundering, sleeper exit (worst case on instant A2A
without a hold on prepaid orders: EUR 14,070 before detection, EUR 12,663 with the hold); open:
collusion steering. Honest routes pass with a cost: a micro-merchant (probation), a seasonal
merchant (false-alarm risk; a seasonal baseline and a reserve increase instead of suspension), an
honest entity change (short hold; a continuity fast path).

### B1.8 Fairness, due process, data, attacks on the authority

Merchants see their attestation, components, signals, reasons and receipts; every refusal,
restriction, suspension or expulsion is a Decision Center decision with a human review on request
and an appeal; suspension stops new attestations and does not touch paid orders; false positives
are measured and published with the scams caught. Data sources: ABS receipts (sufficient on their
own), acquirer and PSP KYB and fraud signals under contract, registries, domain data, rail name
checks, the blocklist, public ad-library data. Limits: a sole trader is a natural person with
access, rectification and human-review rights; the attestation states counts and rates over a
window, never characterisations; nothing is scraped from social media. Attacks on the authority
(fake purchases, collusion, false disputes, sleepers, key compromise, model poisoning) are
answered by paid-and-delivered-only records, the hold, diversity minimums, conduct findings,
velocity caps, short TTLs, key rotation and the quorum.

### B1.9 Flow: attestation and payout hold

```mermaid
sequenceDiagram
    participant A as Buying agent
    participant TA as Trust Authority
    participant M as Merchant
    participant PSP as Merchant's PSP / acquirer (licensed)
    participant U as User
    A->>TA: attest(merchant, value, nonce)
    TA-->>A: attestation: level, status, constraints, receipt
    alt not active, below mandate minimum, or above cap
        A-->>U: not qualified for this purchase; reasons as codes; alternatives
    else probation or restricted
        A->>M: order
        A->>PSP: pay; Settlement Instruction timing = payout_hold_until_delivery, held_by = merchant_psp or acquirer
        M->>M: ship; Delivery Record
        alt conforms, or window elapsed with no not_received
            PSP->>M: payout_release
        else not_received or merchant-liable Decision
            PSP->>U: payout_return
        end
    else qualified
        A->>PSP: pay; rolling reserve
    else established
        A->>PSP: pay; immediate
    end
```

Experiment: T0 (no attestation), T1 (attestation only), T2 (attestation plus hold) on 8 trust
scenarios, five scam types and three honest new merchants; H7 states T2 reduces unrecoverable loss
without blocking more than 10% of honest new merchants. Low n; descriptive with intervals.

---

## B2. ABS Offer Specification (binding structured product spec)

Founder's words: "nowadays a lot of legacy forms and products description exists ... never
understand what exactly the product deliver, so this is our chance to have the most modern new
standard to resolve the mess with product descriptions"; "I believe producer will follow the
unified standard easily if they want to sell".

### B2.1 Reuse

| Need | Standard reused | How |
|---|---|---|
| Product identity | GS1 GTIN; GS1 Digital Link | Spec keyed by GTIN; producer specs referenced by GTIN |
| Attribute names and supply-chain values | GS1 Web Vocabulary; GDSN where accessible | `Attribute.dictionary`; `source: gdsn` |
| Open-web interoperability | schema.org Product, Offer, PriceSpecification, OfferShippingDetails, MerchantReturnPolicy | Lossy projection of the ABS offer; the signed ABS offer stays the source |
| Technical property dictionaries | ECLASS (IEC 61360-based); ETIM for electrotechnical and building products | Property identifiers per profile |
| Units | UCUM codes; ISO 80000 definitions | Every numeric attribute carries a UCUM unit |
| Producer data with a regulatory carrier | EU Digital Product Passport under the Ecodesign for Sustainable Products Regulation, for the product groups and dates its delegated acts set | `dpp_ref`; attributes imported with `source: dpp` |
| Data quality | ISO 8000 master-data parts | Completeness, syntax and provenance rules in feed checks |
| Photo provenance | C2PA | Manifest hash on offer and delivery images; provenance, not truth |

ABS adds, because no dictionary has them: the binding flag, tolerance and verification method per
attribute; the merchant signature over the spec as contract content; the `non_binding` state for
unconfirmed extractions; category profiles that make the required set explicit.

### B2.2 Spec and Profile objects

```json
{
  "$id": "urn:abs:schema:0.3:spec",
  "type": "object",
  "required": ["profile", "attributes", "status", "spec_hash"],
  "additionalProperties": false,
  "properties": {
    "profile": {"type": "object", "required": ["id", "version"], "properties": {"id": {"type": "string"}, "version": {"type": "string"}}},
    "attributes": {"type": "array", "minItems": 1, "items": {"$ref": "urn:abs:schema:0.3:attribute"}},
    "package_contents": {"type": "array", "items": {"type": "object", "required": ["item", "qty"], "properties": {"item": {"type": "string", "maxLength": 100}, "qty": {"type": "integer", "minimum": 1}}}},
    "status": {"enum": ["binding", "non_binding"]},
    "producer_spec_ref": {"type": "object", "properties": {"gtin": {"type": "string"}, "spec_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}, "publisher": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef"}, "signature": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Signature"}}},
    "dpp_ref": {"type": "string", "format": "uri"},
    "extraction": {"type": "object", "properties": {"method": {"enum": ["merchant_entered", "producer_import", "gdsn_import", "dpp_import", "ai_extracted"]}, "model_id": {"type": "string"},
                   "source_text_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}, "confirmed_at": {"type": "string", "format": "date-time"}, "confirmed_by_kid": {"type": "string"},
                   "ambiguities": {"type": "array", "items": {"type": "string", "maxLength": 120}}}},
    "completeness": {"type": "number", "minimum": 0, "maximum": 1},
    "spec_hash": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}
  }
}
```

```json
{
  "$id": "urn:abs:schema:0.3:profile",
  "type": "object",
  "required": ["id", "version", "category", "required_attributes", "package_contents_required"],
  "properties": {
    "id": {"type": "string"}, "version": {"type": "string"}, "category": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Category"},
    "dictionary_preference": {"type": "array", "items": {"enum": ["gs1", "schema.org", "eclass", "etim", "dpp"]}},
    "required_attributes": {"type": "array", "items": {"type": "object", "required": ["name", "verification_method"],
                            "properties": {"name": {"type": "string"}, "dictionary": {"type": "object"}, "unit": {"type": "string"}, "default_tolerance": {"type": "object"}, "verification_method": {"type": "string"}, "value_enum": {"type": "array"}}}},
    "optional_attributes": {"type": "array", "items": {"type": "object"}},
    "package_contents_required": {"type": "boolean"}, "conformity_window_days": {"type": "integer", "minimum": 1},
    "withdrawal_right_default": {"enum": ["applies", "exception_custom", "exception_sealed", "exception_digital", "exception_dated_service", "not_consumer"]}
  }
}
```

**Offer.** The merchant-signed offer an agent compares and buys (envelope type `Offer`, signed by the
merchant). The Offer Snapshot of A5.5 freezes one at view or at checkout and reuses these field
definitions. Free text is `UntrustedText`: shown to people, never binding, never an instruction.

```json
{
  "$id": "urn:abs:schema:0.3:offer",
  "type": "object",
  "required": ["offer_id", "merchant", "spec", "price", "price_includes_tax", "mandatory_fees", "delivery_options", "returns_policy", "condition", "images", "valid_until"],
  "additionalProperties": false,
  "properties": {
    "offer_id": {"type": "string"}, "merchant": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef"},
    "gtin": {"type": "string", "pattern": "^[0-9]{8,14}$"}, "sku": {"type": "string"},
    "spec": {"$ref": "urn:abs:schema:0.3:spec"},
    "price": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}, "price_includes_tax": {"type": "boolean"},
    "mandatory_fees": {"$ref": "urn:abs:schema:0.3:offer-snapshot#/properties/mandatory_fees"},
    "reference_price": {"$ref": "urn:abs:schema:0.3:offer-snapshot#/properties/reference_price"},
    "delivery_options": {"type": "array", "minItems": 1, "items": {"$ref": "urn:abs:schema:0.3:offer-snapshot#/properties/delivery_option"}},
    "returns_policy": {"$ref": "urn:abs:schema:0.3:offer-snapshot#/properties/returns_policy"},
    "condition": {"$ref": "urn:abs:schema:0.3:offer-snapshot#/properties/condition"},
    "warranty_months": {"type": "integer"},
    "tax": {"$ref": "urn:abs:schema:0.3:offer-snapshot#/properties/tax"},
    "cross_border": {"$ref": "urn:abs:schema:0.3:offer-snapshot#/properties/cross_border"},
    "images": {"type": "array", "minItems": 1, "items": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/ImageRef"}},
    "title": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/UntrustedText"}, "description": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/UntrustedText"},
    "valid_from": {"type": "string", "format": "date-time"}, "valid_until": {"type": "string", "format": "date-time", "description": "a snapshot captured after this is a feed mismatch and a step-up signal (A5.8)"}
  }
}
```

### B2.3 Profiles (v0.2 set) and the priority categories

| Profile | Required binding attributes (verification) | Withdrawal right |
|---|---|---|
| Electronics | model_identifier (label_read or serial_lookup); variant such as colour and storage (label_read); capacity or key rating with unit (label_read); dimensions or weight where used (measure or weigh, default tolerance 2%); region, plug_type, voltage (label_read); condition (visual_match); package_contents (count); warranty_months (document_check) | applies |
| Apparel and footwear | brand_model; size with size system named; colour with equivalents; material composition in percent; condition | applies (sealed hygiene goods excepted) |
| Groceries and consumables | GTIN; net_content with UCUM unit; best_before minimum days at delivery; allergens where declared; storage condition | perishables excepted |
| Digital content and software | title_identifier; platform or format (functional_test); region or licence terms (document_check); delivery method and activation window (delivery_log) | excepted once started with consent |
| Travel, tickets, accommodation | event or journey identifier; date and time; seat or room class; named passenger or guest rules; change and cancellation terms (document_check) | excepted (dated services) |
| Services | typed scope items; date or window; location or remote; provider identity; cancellation terms; acceptance_step | depends; excepted once fully performed with consent |
| Custom goods | specification parameters supplied by the buyer (document_check); material; dimensions (measure) | excepted |
| Business purchases (any profile) | as the profile, plus VAT treatment and invoice format | none |

The last five rows are where the liability rule matters most (A4.4); v0.2 develops their
acceptance steps and evidence first.

### B2.4 Conformity check and legacy migration

Attribute by attribute: obtain the delivered value by the stated method, compare within tolerance
(numeric by `abs` or `rel_pct`, enumerations exact or in `equivalents`, sets as multisets), record
each result with `tolerance_applied`, method and evidence; unverifiable attributes are
`undeterminable`, not mismatches; any binding attribute outside tolerance, missing package item,
different condition or over-charge is AG3; free text never grounds AG3. Legacy migration: a model
extracts a candidate spec from the prose, lists unresolved ambiguities, and the merchant reviews,
corrects and signs; only then `binding`. A spec with ambiguities or below the profile's required
set stays `non_binding`; agents do not buy it under a default Allowance and rank binding offers
first; the share of binding offers is a feed-quality metric and must be 100% for listings sold to
agents at Qualified and above. The experiment's structured-vs-legacy comparison (Amendment 3)
measures the spec's contribution on 16 not-as-described cases.

### B2.5 Adoption design

1. **Producer-sourced specs.** One signed spec per GTIN from the manufacturer through the GS1
   channels it already uses and, where applicable, the Digital Product Passport; merchants
   reference it (`producer_spec_ref`) and sign only their offer terms. The merchant remains liable
   for conformity of what it delivers; the producer answers to the merchant under their own
   contract.
2. **Market pull.** Agents rank and buy only qualified offers with binding specs; access to agent
   buyers is the incentive. Nobody pays a merchant to adopt.
3. **Cold start, honestly.** The pull is as strong as agent buying volume. Realistic first movers:
   an agent provider or marketplace that requires ABS for its agents' purchases; categories where a
   passport already forces structured data; vertical sellers already in ECLASS or ETIM; an
   account-to-account scheme designing purchase protection (B5). A minimal ABS-Basic adoption for a
   merchant with a product database is days: register, reuse the acquirer KYB, run the converter
   with the profile set, confirm the specs for the SKUs sold to agents, publish returns and
   delivery, expose a dispute endpoint. Binding and non-binding listings coexist in one feed during
   the transition.
4. **Who does what per level:** producer (publish signed specs per GTIN, optional at Basic);
   merchant (binding specs on SKUs sold to agents at Basic, all listings at Full, adopt producer
   specs by reference); agent provider (validate, rank binding first, refuse non-binding under the
   default policy; view and checkout snapshots and image comparison at Full); PSP or acquirer (KYB
   reference, ABS reference, holds and reserves); arbiter (profiles, feed checks, per-attribute
   fact-finders, feed-quality metrics).

Uptake is a hypothesis until measured.

---

## B3. ABS Agent Allowance (full policy)

Founder's words: "agent allowance, user must setup limits, rules, taxes everything so where the
agent buys autonomusly and when with user manual approval".

### B3.1 Policy object

Signed by: user (strong authentication over the summary shown), agent provider; the PSP's
acknowledgement appended for `rail_enforcement`.

```json
{
  "$id": "urn:abs:schema:0.3:allowance-policy",
  "type": "object",
  "required": ["policy_id", "user_ref", "principal_type", "agent_provider", "agent_ids", "currency", "limits", "rules", "tax", "autonomy", "authentication", "valid_from", "expires_at", "rulebook_version", "nonce"],
  "additionalProperties": false,
  "properties": {
    "policy_id": {"type": "string"}, "user_ref": {"type": "string"}, "principal_type": {"enum": ["consumer", "business", "public_body"]},
    "agent_provider": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef"}, "agent_ids": {"type": "array", "minItems": 1, "items": {"type": "string"}},
    "currency": {"type": "string", "pattern": "^[A-Z]{3}$"},
    "limits": {"type": "object", "required": ["per_transaction", "daily", "weekly", "monthly", "total"],
      "properties": {"per_transaction": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}, "daily": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}, "weekly": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"},
                     "monthly": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}, "total": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"},
                     "per_category": {"type": "array", "items": {"type": "object", "required": ["category"], "properties": {"category": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Category"}, "per_transaction": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}, "monthly": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}}}},
                     "per_merchant": {"type": "array", "items": {"type": "object", "required": ["merchant_id"], "properties": {"merchant_id": {"type": "string"}, "per_transaction": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}, "monthly": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}}}},
                     "max_units_per_purchase": {"type": "integer", "minimum": 1}, "max_units_per_month": {"type": "integer", "minimum": 1}, "max_purchases_per_day": {"type": "integer", "minimum": 1}},
      "description": "hard limits: declined, never escalated"},
    "rules": {"type": "object", "required": ["allowed_categories", "blocked_categories", "min_merchant_qualification", "recurring_allowed", "cross_border_allowed"],
      "properties": {"allowed_categories": {"type": "array", "items": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Category"}}, "blocked_categories": {"type": "array", "items": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Category"}},
                     "min_merchant_qualification": {"enum": ["probation", "qualified", "established"]}, "preferred_merchants": {"type": "array", "items": {"type": "string"}}, "blocked_merchants": {"type": "array", "items": {"type": "string"}},
                     "known_merchants_only_for_autonomy": {"type": "boolean", "default": true}, "condition_allowed": {"type": "array", "items": {"type": "string"}}, "binding_spec_required": {"type": "boolean", "default": true},
                     "delivery": {"type": "object", "properties": {"countries": {"type": "array", "items": {"type": "string"}}, "max_days": {"type": "integer"}, "methods": {"type": "array", "items": {"type": "string"}}, "address_hashes_allowed": {"type": "array", "items": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Hash"}}}},
                     "returns": {"type": "object", "properties": {"min_window_days": {"type": "integer"}, "who_pays_return_accepted": {"type": "array", "items": {"type": "string"}}}},
                     "recurring_allowed": {"type": "boolean"}, "recurring": {"type": "object", "properties": {"max_per_period": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}, "max_active": {"type": "integer"}, "approval_on_first": {"type": "boolean", "default": true}, "notify_before_each": {"type": "boolean", "default": true}}},
                     "cross_border_allowed": {"type": "boolean"},
                     "delegates": {"type": "array", "items": {"type": "object", "required": ["delegate_ref", "role", "limits", "authentication"],
                                   "properties": {"delegate_ref": {"type": "string"}, "role": {"enum": ["household_member", "employee", "manager", "admin", "procurement_officer"]},
                                                  "limits": {"type": "object"}, "allowed_categories": {"type": "array"}, "approval_required_above": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"},
                                                  "may_approve_for": {"type": "array", "items": {"type": "string"}}, "authentication": {"type": "object"}, "valid_until": {"type": "string", "format": "date-time"}}}}}},
    "tax": {"type": "object", "required": ["vat_inclusive_total_required"],
      "properties": {"vat_inclusive_total_required": {"type": "boolean"}, "buyer_vat_id": {"type": "string"}, "buyer_vat_id_validated_at": {"type": "string", "format": "date-time"},
                     "einvoice_required": {"type": "boolean"}, "einvoice_formats_accepted": {"type": "array", "items": {"enum": ["en16931_ubl", "en16931_cii", "peppol_bis_billing_3", "national_mandated"]}},
                     "einvoice_delivery": {"type": "object", "properties": {"peppol_participant_id": {"type": "string"}, "endpoint": {"type": "string", "format": "uri"}, "email": {"type": "string"}}},
                     "purchase_order_required": {"type": "boolean"}, "cost_center_tags": {"type": "array", "items": {"type": "string"}},
                     "cross_border": {"type": "object", "properties": {"show_import_charges_before_purchase": {"type": "boolean", "default": true}, "require_import_charges_included": {"type": "boolean"}, "low_value_import_scheme_required": {"type": "boolean"}}}}},
    "autonomy": {"type": "object", "required": ["default_level", "rules", "approval"],
      "properties": {"default_level": {"enum": ["autonomous", "notify_and_hold", "approval_required", "never"]}, "notify_and_hold_minutes": {"type": "integer", "minimum": 5, "default": 60},
                     "approval": {"type": "object", "required": ["method", "assurance", "approver"], "properties": {"method": {"type": "string"}, "assurance": {"type": "string"}, "approver": {"enum": ["user", "delegate_manager", "user_or_manager"]}, "expires_minutes": {"type": "integer", "default": 1440}}},
                     "rules": {"type": "array", "minItems": 1, "items": {"type": "object", "required": ["rule_id", "when", "level"],
                               "properties": {"rule_id": {"type": "string"}, "when": {"type": "object", "properties": {"amount_above": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"}, "amount_at_or_below": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Money"},
                                              "new_merchant": {"type": "boolean"}, "new_category": {"type": "boolean"}, "risk_signal": {"type": "boolean"}, "cross_border": {"type": "boolean"}, "first_recurring": {"type": "boolean"}, "recurring_subsequent": {"type": "boolean"},
                                              "merchant_level_below": {"type": "string"}, "delegate_purchase": {"type": "boolean"}, "non_binding_offer": {"type": "boolean"}, "price_changed_since_view": {"type": "boolean"}, "quantity_above": {"type": "integer"},
                                              "category": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/Category"}, "merchant_id": {"type": "string"}, "blocked": {"type": "boolean"}}},
                                              "level": {"enum": ["autonomous", "notify_and_hold", "approval_required", "never"]}}}}}},
    "notifications": {"type": "object", "properties": {"channels": {"type": "array", "items": {"type": "string"}}, "on": {"type": "array", "items": {"type": "string"}}}},
    "authentication": {"$ref": "urn:abs:schema:0.3:mandate#/properties/authentication"},
    "rail_enforcement": {"type": "array", "items": {"type": "object", "required": ["psp", "controls"], "properties": {"psp": {"$ref": "urn:abs:schema:0.3:envelope#/$defs/PartyRef"}, "controls": {"type": "array", "items": {"enum": ["per_transaction_limit", "periodic_limit", "mcc_block", "merchant_allowlist", "country_block", "single_use_credential"]}}, "acknowledged_at": {"type": "string", "format": "date-time"}}}},
    "valid_from": {"type": "string", "format": "date-time"}, "expires_at": {"type": "string", "format": "date-time"}, "rulebook_version": {"type": "string"}, "rules_shown_at": {"type": "string", "format": "date-time"}, "nonce": {"type": "string", "minLength": 16}
  }
}
```

A default consumer policy for illustration: per transaction 150, daily 300, monthly 1,000, total
5,000; blocked: gambling, adult, weapons, gift cards and prepaid; `min_merchant_qualification:
qualified`; rules in order: blocked -> never; non-binding offer -> never; first recurring ->
approval; cross-border -> approval; new merchant or category or any signal -> approval; above 50 ->
notify-and-hold; otherwise autonomous.

### B3.2 Flows

```mermaid
sequenceDiagram
    participant U as User (principal)
    participant D as Delegate
    participant P as Agent provider app
    participant I as Issuer / bank app
    participant PSP as PSP (rail controls)
    U->>P: set limits, categories, merchants, delivery and returns rules, tax settings, autonomy rules, delegates
    P->>U: plain-language summary: buys alone / holds / needs approval / never
    U->>I: strong authentication over the summary hash, total and expiry
    I-->>P: authentication reference, assurance
    P->>P: sign Allowance Policy; start counters
    opt rail enforcement
        P->>PSP: register the enforceable subset (limits, MCC blocks, allowlist, country block, single-use credentials)
        PSP-->>P: acknowledged (rail_enforcement)
    end
    opt delegates
        U->>P: add delegate: role, sub-limits, categories, approval threshold
        P->>D: enrol authenticator; delegate signs acceptance
    end
    Note over U,PSP: Raising any limit or adding a delegate repeats the strong authentication.
```

The purchase-routing flow is A11.4.

### B3.3 Standards mapping

| ABS element | Reuses | What ABS adds |
|---|---|---|
| Autonomous level | PSD2 SCA exemptions for remote payments: low value with cumulative counters, trusted beneficiaries, recurring transactions of fixed amount, transaction risk analysis; secure corporate payments for businesses; merchant-initiated arrangements set up with authentication (EBA Q&A); PSD3/PSR successors as proposed or agreed (LANDSCAPE.md) | The autonomy rule as a user-set policy, the notification, provider liability |
| Notify-and-hold | Merchant-initiated and recurring practice | The cancel window and its evidence |
| Approval required | SCA with dynamic linking; EMV 3-D Secure on cards; bank-app authentication on A2A | The trigger set as a user policy; the Approval Record |
| Policy as a consent object | OAuth 2.0 Rich Authorization Requests (`authorization_details`); FAPI 2.0; Grant Management | The field set and semantics |
| Limits, blocks, delegates | Card controls as issuers and spend-management platforms implement them (per-transaction and periodic limits, MCC blocks, merchant allowlists, single-use virtual credentials, approval workflows, employee cards with roles) | Product-category vocabularies beyond MCC, the binding-spec requirement, qualification level, intent |
| Tax and invoicing | VAT-inclusive totals as consumer law requires; EN 16931 with UBL or CII over Peppol or the national mandated format; VAT ID validation (VIES); the Import One-Stop Shop for low-value imports | A B2B agent purchase is not complete without the invoice reference; import charges are a purchase-time field |

### B3.4 Tax and invoicing fields

Purchase Record `tax_detail`: buyer type, buyer and seller VAT ids, per-line net, rate and VAT,
import scheme and charges with `shown_before_purchase`, e-invoice format, document hash, delivery
channel and time, cost-centre tags, purchase-order reference. The agent asks the merchant for the
e-invoice in an accepted format at checkout; a B2B purchase under a policy with
`einvoice_required` is not complete until the reference is attached (deferred-invoice handling is
open, A15.1). The experiment's AL arm scores B2B compliance as VAT id supplied, invoice requested,
merchant issues VAT invoices.

### B3.5 Safety framing

Under-escalation rate (autonomous or hold purchases later found unwanted / autonomous and hold
purchases), over-escalation rate (approvals granted without change / approvals requested), an
approval-fatigue indicator (approvals in seconds; approval rate above 98%), hold cancellations,
delegate breaches caught. The operator publishes recommended defaults per principal type and revises
them with the rulebook. The AL arm (Amendment 4) scores correctly autonomous, correctly escalated,
under-escalated and over-escalated per purchase decision.

---

## B4. Segment profiles

What changes per segment: the objects, Allowance rules, reason codes, evidence, settlement and the
legal regime. Legal references are as cited in `LANDSCAPE.md` or Audit 0; uncertain ones are
marked.

| Segment | Objects and Allowance | Codes and evidence | Settlement | Regime (verify where marked) |
|---|---|---|---|---|
| B2C consumer | Consumer policy; `vat_inclusive_total_required`; withdrawal overlay on every Decision | All codes; AG2 and AG5 end in `withdrawal` where available; E3 with contestable delivery evidence | Card refund and chargeback; A2A refund by participation; payout hold on probation merchants | Consumer Rights Directive (withdrawal), Sale of Goods Directive (conformity), Unfair Contract Terms, Rome I and Brussels I bis (home law and forum); PSD2 and successors; UK APP for scams |
| B2B | Business policy: purchase-order reference, approval workflows (manager and procurement roles), VAT id, e-invoice required, payment terms, cost centres, spend policy; no withdrawal right | All codes; AG2 and AG5 end in `deny`; contract terms and the signed spec are the conformity reference; acceptance steps for services | Card or A2A; invoice-based payment terms allowed, with the ABS reference in remittance; reverse charge where applicable | Contract law and B2B terms; EN 16931 and Peppol; ViDA, Council Directive (EU) 2025/516 (intra-EU B2B e-invoicing from 1 Jul 2030); secure corporate payment exemption for SCA (RTS Art 17, competent authority); no consumer ADR constraints, but the Decision binds by contract |
| B2G public procurement | Public-body policy: framework-agreement reference, procurement thresholds and procedures outside ABS, strict Allowance (approval by authorised officers), full audit trail (chain and log), EN 16931 e-invoice | AG3, AG4, AG1-M, AG1-P; AG2 and AG5 rarely arise (specifications are explicit); E3 required | A2A with ISO 20022 references; payment terms per public-sector rules | Directive 2014/55/EU Art 7: public buyers must receive and process EN 16931 invoices; any duty on suppliers to send them is national; public procurement directives and thresholds (not verified); national audit rules |
| C2G and B2G fees (taxes, permits, fines) | Policy with `never` outside listed payees; approval for first payment to a body | Not a sale: conformity is "the right fee to the right body for the right reference"; wrong reference is AG1-P or AG1-M by who set it | A2A with structured reference; no chargeback; refund by the authority under administrative procedure | Administrative appeal replaces chargebacks; ABS supplies the evidence; no consumer sale law |
| C2C peer platforms | Platform acts as the ABS participant; sellers are not merchants with merchant duties; payout hold by the platform's licensed PSP acting as payee (acquiring model); policy requires platform-attested listings | AG3 against the platform's listing attestation where it attested; otherwise the platform's own protection; AG2 and AG5 | Hold by the licensed PSP as payee; release on delivery; platform refund | Consumer law applies to platform duties, not to peer sellers; DSA obligations of the platform (scope not verified); payment-service licensing of the hold; once the PSR applies, a platform acting for both payer and payee cannot rely on the commercial-agent exclusion (PSR Art 2(2)(b) in the Council text) |
| B2B2C marketplaces | Marketplace is a participant; sellers are qualified through the marketplace's trader checks (DSA Art 30, verified) reused by reference; marketplace signs offers it hosts or passes the seller's signature | Liability split: the seller for conformity and content; the marketplace where it attested, added lines or fees, or hosted content after notice; AG1-M covers marketplace-added fees | Marketplace payout hold and refund through its licensed PSP as payee; ABS Decision instructs the marketplace | DSA trader traceability and notice duties; consumer law for the seller; marketplace terms; Omnibus Directive on ranking and reviews (not verified); the PSR narrows the commercial-agent exclusion to agents acting for only one side |
| Agent-to-agent negotiation | Both principals hold policies; a merchant agent negotiates within the merchant's signed offer bounds; terms bind only when written into a negotiation record signed by both agents and hashed into the Offer Snapshot; seller-agent statements outside it are merchant content for Step 2 | Evidence of negotiated terms: the signed negotiation record and both agents' logs; AG3 against the snapshot; AG1-M (extended) where checkout terms are worse than the negotiation record; AG1-P against either provider for exceeding its principal's instructions; AG4 against either side's injected content | As the underlying segment | Contract formation by agents (national law; verify); the same decision order |

Simulation results per segment (v0.1 as written against v0.2, decided/correct): A2A 13/11 to
13/13; B2B 23/5 to 23/23; B2B2C 30/25 to 31/31; B2C 397/281 to 424/424; B2G 8/4 to 10/10; C2C
13/11 to 13/13; C2G 14/3 to 14/14. The B2B, B2G and C2G jumps come from the expanded explicit
terms (invoice data, payment terms, procurement thresholds, authority payee) and the cure and
no-loss remedies; legal statements in the catalogue are general and marked.

---

## B5. Adoption, first adopters and channels

Audit 0's assessment is accepted: an end-to-end standard competes with bodies that have leverage
ABS lacks; the dispute profile plus the benchmark is the right vehicle. Candidates, in order:

1. **EPI Wero purchase protection** for the account-to-account module: workshops in Q4 2026, a
   framework expected in Q1 2027, embedding for Dutch consumers by January 2028 (single
   trade-press source, UNVERIFIED). Irrevocable instant rail, no chargeback legacy, needs rules for
   non-delivery and not-as-described, will meet agent purchases soon.
2. **An issuer or wallet** that wants Amex-style agent-error protection and needs a decision
   procedure and evidence standard for it.
3. **FIDO Alliance Payments working group** for the Mandate digest and evidence profile on AP2 and
   Verifiable Intent; **EMVCo's agentic framework** comment process for cards; **UCP and ACP** for
   the injection-safety and conformity-attribute profile. Each of these bindings is proposed
   (A5.2, A5.2.1); bringing one to such a channel means bringing a fixture and a round-trip test.
4. **An agent provider or marketplace** that adopts ABS-Basic for its own agents' purchases and
   runs the Decision Center through an independent operator.

Uptake is a hypothesis until measured.

## B6. Adoption path for agent dispute codes

Dispute codes are not ABS's to create. Each body owns its own, and each has its own way of
accepting a change (sources and access dates in `standard/ADOPTION_AND_CONFIRMATION.md`, all read
2026-11-04):

- **Visa** owns its dispute conditions (10.1 to 13.9). It "may amend ... the Visa Rules at any
  time" (1.1.1.5) and has no public comment process.
- **Mastercard** owns its message reason codes and changes them by announcements to its
  customers.
- **The ISO 8583 maintenance agency** (AFNOR, under ISO/TC 68/SC 9) provides ISO 8583 values.
- **The ISO 20022 Registration Authority** maintains external code sets. Change requests are open
  to "organisation(s), group(s) of users, regulator(s)" each quarter, and message change requests
  run on a yearly cycle. The card chargeback messages are cain.027 and cain.028. No card-dispute
  reason code set exists.
- **The EPC** changes its rulebooks on requests from "any individual or organisation that is able
  to claim a legitimate interest". The next deadline is 30 Apr 2028, with effect in Nov 2030.

A code is also the last thing needed, not the first. A card dispute returns a transaction to the
merchant's acquirer, and in AG1-P and AG1-C the merchant performed (A4.5). Visa registers agentic
payment providers directly, not through a member (4.1.23.2), so no sponsor exists in the dispute
chain to which an agent-fault dispute could be routed.

The path asks each body only for what it can give, in this order. The timelines are estimates.

| Stage | What changes | Who must agree | Timeline |
|---|---|---|---|
| 0. Contractual programme | ABS decides before and beside the rail. The liable party refunds by a new credit, and rail rights are untouched (A6.1). A participating issuer can already ask a Visa-registered provider in writing for the cardholder's instruction (Visa 4.1.23.3) | Participants only | 6–12 months to a pilot |
| 1. Evidence data elements, no new code | An agent indicator, the registered provider's identifier, `mandate_digest`, the checkout hash and the ABS locator carried in authorisation and dispute data. This follows the pattern of Visa Compelling Evidence 3.0 (effective 15 Apr 2023) and Mastercard First-Party Trust (announced 23 Oct 2023). EMVCo's draft agentic framework names "Agentic Transaction Indicators" as possible future work | Each scheme; EMVCo; FIDO for the mandate credential | 12–24 months |
| 2. Sub-condition under existing categories | (i) A narrow merchant remedy: when the checkout matches the user-authenticated instruction, a claim that the agent broke the instruction (an AG1-type claim misfiled against the merchant) fails against the merchant and goes to the provider's programme. The match never defeats a non-conformity, non-delivery or fraud claim: conformity is decided first (A4.1 Step 1), and whether the payment was authorised stays the payer's PSP's question (A4.1 Step 0). (ii) AG4 and AG1-M as sub-reasons where the merchant is liable. (iii) An issuer flag that routes AG1 claims to the provider's programme instead of the merchant | Each scheme; an ISO 20022 representment-reason value for (i) | 2–3 years |
| 3. Formal codes and a liability flow | A scheme condition with the registered agent provider as the liable party. An agent-evidence block in cain.027 and cain.028. EPC asks limited to a request-for-recall reason for an error by the payer's agent, and a reference in the SCT Inst repayment procedure if that procedure is adopted. Disputes over the underlying contract stay outside the SEPA schemes | Schemes; the ISO 20022 RA with TC 68/SC 9/TG1; the EPC | 3–5 years |

What persuades at each stage is evidence, not argument:

- the measured E0-to-E3 results (A4.2);
- what E1 makes determinate (A5.1);
- the field loss data that only a Stage 0 pilot can produce. None has been published.

---

## Appendix A. Worked example

Task: "Buy me one pair of Sony WH-1000XM6 headphones, new, not refurbished, cheapest from a
reputable shop, under EUR 350."

1. Mandate: `max_total 350.00 EUR`, `categories [headphones]`, `max_units 1`, `condition_allowed
   [new]`, `item_requirements [{model_identifier: WH-1000XM6}, {condition: new}]`, `ask_on_ambiguity
   true`, `autonomy_required approval_required` (over the policy's notify threshold and a new
   merchant). The mandate UI asked for colour; the user left it blank. Authentication in the bank
   app.
2. Discovery: Offer A new 329.00, delivery 0.00, returns 30 days merchant-paid, Established;
   Offer B refurbished 289.00 (excluded by condition); Offer C new 299.00 plus 9.90 delivery,
   Probation merchant 40 days old. A is ranked first on reputation; typed fields only.
3. Checkout A: snapshot countersigned; C1 passes including item requirements; approval required;
   the user authenticates over the exact cart; Approval Record; chain head
   `sha256:9f3a1c2e4d5b6a70...` (all 64 hex characters), committed in the payer PSP's payment
   record; Settlement Instruction on a card rail with the locator
   `ABS:urn:abs:purchase:...:9f3a1c2e4d5b6a70`, which finds that commitment and does not replace it.
4. Delivery: carrier scan with weight; the user photographs the box and label; serial lookup
   matches the packing record; conformity `conforms`; the agent tells the user the withdrawal right
   runs until day 14.
5. Dispute 1: the box holds an XM5. Step 1: `model_identifier` mismatch; the serial registry, which
   has authority for unit identity, says XM5, and the merchant's own packing photo, committed at
   dispatch and binding on the merchant, shows XM5 (A5.7). AG3, merchant liable, refund with return
   at merchant cost. The merchant's "the listing said XM5" is disregarded against the countersigned
   snapshot.
6. Dispute 2: XM6 as offered, silver. The user says "I wanted black". Colour was not captured and
   no clarification mentioned it. Step 4: AG2, buyer; within 14 days, remedy `withdrawal`: return
   at own cost for a refund. Had `item_requirements` held `colour: black`, or had the confirmed
   instruction text or a clarification the user confirmed with authentication said "the black one",
   Step 3 would apply: AG1-P, the provider refunds. Had the user said it only in the conversation
   and the agent not captured it, Step 3b would apply: AG1-C, the provider refunds.
7. Dispute 3: the user had added "if unsure, ask me first" to the instruction text confirmed at
   the tap (and `ask_on_ambiguity` was true); the agent chose silver without asking
   when black and silver were both in stock at the same price. Step 3: a guess where told to ask.
   AG1-P.
8. Dispute 4: conforming, black, the user changed their mind on day 20. AG5, `deny`; the 30-day
   merchant return window is still open outside ABS.

## Appendix B. Audit 0 findings and how each is resolved

| Finding | Resolution in this version |
|---|---|
| I1 Sections 6 and 7 missing; section 11 a placeholder; LANDSCAPE.md absent | Part B1 (Trust Authority) and A7 (Decision Center) written; A10 filled with the concession table, regulation mapping and standards matrix; `LANDSCAPE.md` written alongside this document; no placeholder remains |
| I2 Three answers to "authorised but wrong" | One answer everywhere, mirroring rulebook v1.2 and Amendment 5: explicit term broken -> AG1-P (provider); explicit mandate satisfied, unstated intent not -> AG2 (buyer, withdrawal overlay). Appendix A shows both sides of the line. v0.3 refines what counts as an explicit term and adds AG1-C (Audit 1, F10; Appendix E) |
| I3 Neutrality contradicts the business model | A2: no party decides cases where it holds another role; an agent provider never decides disputes in which its agents can be liable; the Decision Center is a network of independent operators admitted against published criteria (A7.5). The fee model is out of scope (A1.3) |
| I4 Decisive delivery evidence assumed | A5.6: contestable evidence only (carrier proof without content inspection, packing record, buyer photos with metadata, serial lookup, digital log, return inspection); H5 tests conformity on mixed-reliability evidence |
| I5 Phase 1 null at the ceiling | A15.2 states the null as a finding; H1 is tested on H1-hard and H1-redteam; no claim that the controls were found necessary |
| I6 Arbiters graded against the author's rules; same model families | A15.2 and A7.8 record both limitations as Amendment 5 does; the ground truth applies this rulebook, not a court's |
| I7 36 vs 40 cases; hypothesis numbering; KPI without baseline; unmapped standards list | 47 cases (case set v2) and H1 to H7 per Amendment 2 used throughout; A1.5 gives baselines from the EBA/ECB and marketplace practice; every standard named is mapped to a requirement in A10.3 |
| Q1 Three-quarters rebuilt existing work | Recast as a profile layered on AP2/FIDO, UCP/ACP, TAP/Agent Pay, acquirer underwriting and scheme monitoring (A10.1); the Mandate and Snapshot are profiles (A5.2); ABS's contribution limited to the six items in "What ABS is" |
| Q1 Visa 4.1.23.10 and Amex | A4.2 positions Step 4 as agreeing with Visa and Step 3 as a contract over the scheme rule; Amex noted as the issuer-protection model ABS can serve |
| Q2 Adoption; vehicle; first adopter | B5: dispute profile plus benchmark; Wero (UNVERIFIED), issuer or wallet, FIDO and EMVCo channels; uptake stated as hypothesis |
| Q3 "Never allow scammers in" false; "only protection on A2A" false; KPI not ambitious | B1.1 restates the target and the defensible claim; A1.3 and B1.1 drop both overclaims; A1.5 compares against the EEA baseline; threat model B1.7 includes bust-out, takeover, synthetic companies, laundering, honest insolvency, counterfeits, fake badges, payer-side manipulation |
| Q4 Conformity narrower than law; agent cannot accept deviations; withdrawal makes goods cases moot; no delivery evidence; AG4 sabotage; cross-border law | A4.3 "without prejudice" and per-purchase `deviation_acceptance` (v0.3, after Audit 2); A4.4 withdrawal overlay in every Decision and in the flows; A1.1 and B2.3 prioritise no-withdrawal categories; A5.6 evidence; A4.2 AG4 note and open question; A3.2 decisions do not bind consumers; A10.2 consumer-law row |
| Q4 Providers will not accept AG2 as written | Step 3 limited to provable fault, capped and insurable (A4.2, A6.4 `liability_cap`); AG2 on the buyer |
| Q5 "Humans only for escalations"; AI Act high-risk; GDPR Art. 22; ADR finality; Menime dependency | A7: human review on request for any party; designed as Annex III 8(a) high-risk with the obligations listed; Art. 22(3) built in; decisions bind participants by contract only; plain-language explanation per case; Menime as reference implementation, the pattern normative |
| Q5 Escrow and collection are regulated | B1.2 and A6: payout holds by licensed payees and collection by licensed creditors; ABS holds nothing; the guarantee is roadmap pending a legal opinion (Audit 2) |
| Q6 Research framing | Outside this document; A15.2 keeps the experiment mapping honest |
| Fix 4 Realistic delivery evidence | A5.6 |
| Fix 8 Re-allocate injection liability | Kept per rulebook; sabotage closed by authorship and notice; split listed as open (A15.1) |
| Fix 9 Scope where liability matters | A1.1, A4.4, B2.3 |
| Fix 10 One adopter, one channel, separate business from research | B5; fee model excluded |
| Housekeeping | 47 cases and H1 to H7 reconciled; model-family limitation recorded; standards mapped |

## Appendix C. Rules adopted from the rule-completeness simulation

Rule ids are those of `standard/sim/rules.py` (`scrolld.abs@0.2-proposed`). "Repairs" is the number
of v0.1 catalogue failures the rule fixed.

| Rule | Repairs | Where adopted |
|---|---|---|
| ABS-4.3 / ABS-2.3 expanded Mandate hard limits | 52 | A4.1 Step 3; Mandate schema A5.5 (`item_requirements`, `scope_only_named_item`, `currency`, `approval_prompt_must_show`, `recurring`, `business_terms`, `policy_version`) |
| ABS-4.1 / 4.1b proportional remedies | 19 | A4.1 Step 1 |
| AG0 Step 0 authorisation | 18 | A4.1 Step 0 |
| ABS-P1 non-participant / off-credential | 17 | A4.1 standing; A3.1 |
| ABS-4.2b feed vs snapshot mismatch | 11 | A4.1 Step 2; `compared_record` in the Offer Snapshot |
| ABS-M refusal record | 9 | A3.2; Refusal Record schema A5.5 |
| ABS-X1 collusion | 8 | A4.1 Step 2; A3.1 |
| ABS-S2 ambiguity construed against the author | 7 | A4.1 Step 1; A5.7 |
| ABS-E1 adverse inference | 7 | A4.1 Step 3; A5.7 |
| ABS-4.2c deceptive claims (AG4-D) | 5 | A3.1; A4.1 Step 2 |
| ABS-P2 spoofed Register | 5 | A4.1 standing (Register operator liable by contract); B1.2 |
| ABS-F1 feed authenticity | 4 | A4.1 Step 2 |
| ABS-X2 undisclosed incentive | 4 | A4.1 Step 3; Mandate `incentive_disclosure` |
| ABS-R1 apportionment | 4 | A4.1 |
| ABS-E1m merchant records missing | 3 | A4.1 Step 1; A5.7 |
| ABS-D2 merchant-initiated claim | 3 | A3.2 |
| ABS-G1 authority payee | 3 | A4.1 standing |
| ABS-S1 unsigned spec | 3 | A4.1 Step 1; A5.4 |
| ABS-E2 unproven claim | 2 | A4.1 Step 1; A5.7 |
| ABS-H1 conflicting evidence | 2 | A4.1 Step 1; A7.3 |
| ABS-T2 repeat dispute | 2 | A3.2 |
| ABS-3.2 / 3.3 / 3.4 delivery evidence, minimum package, weighing | process | A5.6 |
| ABS-5.3 rail execution for every family | process | A6.1, A6.3 |
| ABS-5.4 payout hold and guarantee | process | A6.1; B1.2 |
| ABS-5.5 single track | process | not adopted: withdrawn in v0.3 after Audit 2 (CRD-07); replaced by "alongside the rail, never instead" in A6.1 |
| ABS-5.6 enforcement | process | A6.1 |
| ABS-6.5a Decision Center; 6.6 appeal; 6.7 repeat; 6.8 merchant claim; 6.9 statutory rights; D1 default on silence | process | A3.2, A3.3, A7.3 |
| ABS-8 data retention and PCI | process | A5.9 |
| ABS-2.5 contract formation; 2.6 idempotency; 2.7 negotiation record; 1.5b responding party | process | A3.2; Offer Snapshot and Purchase Record schemas; Participation Agreement |
| ABS-9 enforcement layer | process | A4.1 Step 3; A12.1 |
| ABS-1.7 / 1.8 trust attestation and entry gate (roadmap) | roadmap | B1 |

## Appendix D. Audit 2 corrections

Independent Audit 2 (`audits/AUDIT_2_REGULATORY.md`, primary sources read 2026-11-04) reviewed
every regulatory and standards claim in v0.2. Each row below names the audit's finding and where
v0.3 resolves it. Section numbers are v0.3's.

### D.1 EU and UK payments

| Row | Finding | Resolution |
|---|---|---|
| PAY-01 | PSD2 applies from 13 Jan 2018 (Art 115(2)); Art 97 from 14 Sep 2019 (RTS Art 38(2)) | A10.2 cites both; LANDSCAPE row closed |
| PAY-02 | Unauthorised payments: Arts 71(1), 72, 73, 74(1) | A10.2 cites them with the EUR 50 cap |
| PAY-03 | Payment rules do give an 8-week refund for payee-initiated payments of unspecified amount (Arts 76, 77; SDD unconditional; PSR Art 65) | A1.3 reads "push" A2A rails; A10.2 "Authorised but disputed" row rewritten; double-recovery set-off in A15.1 item 5 |
| PAY-04 | "No PSP-performed SCA means an unauthorised payment" is wrong in law; Art 64 consent; Art 74(2) loss shift | A4.1 Step 0 rewritten: the payer's PSP decides under Arts 64 and 72 to 74; ABS refers and records; Art 74(2) stated; "invalid" kept as a programme rule only |
| PAY-05 | EBA Q&A 2019_4664 is about direct-debit mandates; MIT Q&As are 2018_4031 and 2018_4131; agent purchases are doubtful MITs | A5.8, A10.2, A12.1 and B3.3 corrected |
| PAY-06 | SCA exemption articles and limits missing; Arts 13 and 14 need a named payee; TRA cap EUR 500; Art 17 needs the competent authority; the B3 default is not SCA-neutral | A10.2 and A12.1 give Arts 13, 14, 16, 17, 18 with limits and state the consequences for "any merchant in category" Allowances and the default policy |
| PAY-07 | A mandate with max amount and open payee set is not dynamic linking (Art 97(2); RTS Art 5(1)) | A5.8, A6.5 flow and A11.3 flow: the mandate is consent capture; SCA is per purchase or by exemption |
| PAY-08 | IPR dates: VoP 9 Oct 2025 / 9 Jul 2027; parity 9 Jan 2025 / 9 Jan 2027; 10 seconds; Art 5c(8) refund; applies to all SEPA credit transfers | A10.2 row retitled "Credit transfers (IPR)" with the dates and scope |
| PAY-09 | "Not changed by PSD3" is wrong: PSR Art 51 extends payee verification | A10.2 says so |
| PAY-10 | VoP outcomes include "verification check not possible" | A6.2 `payee_name_check` enum extended; `close_match_name` added |
| PAY-11 | PSD3/PSR status: Council first-reading positions 29 Oct 2026; EP second reading pending; not in the OJ; application not before late 2028 | A10.2 PSD3/PSR row restated; LANDSCAPE updated |
| PAY-12 | PSR Art 50(2) deemed-unauthorised rule and Art 52 spending limits; AG4 question | A10.2 unauthorised row; A15.1 item 16 |
| PAY-13 | SEPA recall is the payer PSP's tool for duplicate, error or fraud; customer-reason recall needs payee consent; no return on SCT Inst | A6.1 and A6.3 rewritten: no reversal against a refusing merchant; the collection right is the remedy; A6.2 `message` enum limited to pain.001 and pacs.008 with the recall messages described as outside ABS |
| PAY-14 | camt.027 and camt.087 are interbank fund inquiries, not goods disputes | Row deleted from A6.3; A10.3 matrix corrected |
| PAY-15 | Remittance 140 characters; EndToEndId is Max35Text; ISO 11649 recommended | A6.2 `reference_value` in unstructured remittance; new `end_to_end_token` (35 characters) |
| PAY-16 | UK APP values: GBP 85,000 cap, GBP 100 excess, 13 months, 50% split, SD20 and SD21, SR1; consumer-deceived definition; move to the FCA | A10.1 and A10.2 rows carry the values; agent-deceived coverage marked unverified; A15.1 item 18 |
| PAY-17 | A2A hold on funds credited to the merchant's own account conflicts with PSD2 Art 87(2) and the IPR ten-second rule | A1.3, A6.1, A6.2 `held_by`, A6.3, A6.5 flow and B1.2 redesigned: hold only where an acquiring or collection PSP is the payee; card holds unchanged |

### D.2 Card schemes

| Row | Finding | Resolution |
|---|---|---|
| CRD-01 | Visa rule is in the Product and Service Rules, §4.1.23.10, ID# 0031176, edition 24 Oct 2026, added Apr 2026; glossary treats the provider as the cardholder | A4.2 and A10.1 cite it so; "cited from the audit, not re-verified" dropped |
| CRD-02 | 4.1.23.2, 4.1.23.3, 4.1.23.11 correct | Kept in A10.1 |
| CRD-03 | 4.1.23.8: order confirmation "made available ... for at least 120 days from the Processing Date" | A10.1 reworded |
| CRD-04 | No agent-specific dispute condition; agentic login ID is one matching element in Compelling Evidence for 10.4 | A10.1 row states it |
| CRD-05 | Mastercard rules unverifiable; developer guide says standard chargeback rights apply | A10.1 cites the guide; rules kept UNVERIFIED |
| CRD-06 | Only the issuer raises a dispute; "representment" is not Visa's term; stages scheme-neutral | A3.2 item 10, A6.1, A6.3, A6.5 flow (DC-to-PSP chargeback arrow removed), A6.2 `dispute_stage` enum made scheme-neutral; `dispute_category` kept |
| CRD-07 | "Single track" assignment contradicts A1.3, Visa §5.4.2.5 and UCTD Annex 1(q) | Deleted. A6.1 "Alongside the rail, never instead": reconciliation and evidence only |
| CRD-08 | ABS timeline can outrun Visa's 120-day limit for 13.1; retention shorter than the 540-day ceiling | Deadline guard in A3.2 item 10 and A3.3; A5.9 retention: later of 540 days from processing and 13 months after delivery |
| CRD-09 | A sponsored originator can push a new credit (Visa Direct OCT; Mastercard Send) | A6.3 and A10.3 reworded: no message reverses the original purchase; a push credit exists |
| CRD-10 | EMVCo tokenisation spend limits unverifiable | A9.1 attributes amount limits to issuer controls and agentic-token programmes; A10.3 marks it |
| CRD-11 | EMVCo framework exact title, comment period closed 30 Sep 2026, Intent Services scope; distinct Technical Framework | A10.1 corrected; Intent Services profiled, not duplicated |
| CRD-12 | EMV 3-D Secure v2.3.1.0 final; v2.4.0.0 draft | A6.2 and A10.3 pin 2.3.1 |
| CRD-13 | Amex: primary page, forward-looking, US credit cards, registered agents, deviation vs subjective intent; already draws the line | A4.2, A10.1, "What ABS is" and A10.3 restated; ABS no longer claims the concept |
| CRD-14 | Visa TAP on HTTP Message Signatures correct | Kept |
| CRD-15 | AP2 and Verifiable Intent at FIDO correct | Kept |
| CRD-16 | Mastercard Agent Pay dates and VAMP enforcement unverifiable | Dates and thresholds removed from A10.1; marked UNVERIFIED |

### D.3 AI and data

| Row | Finding | Resolution |
|---|---|---|
| AID-01 | Annex III 8(a) correct | A7.5 item 8 cites EUR-Lex |
| AID-02 | Recital 61: legal effects make it high-risk; final decision-making human-driven | A7.5 item 8 adds recital 61; tension recorded in A15.1 item 6 |
| AID-03 | Article numbers: 9, 10, 12, 13, 14, 15, 17, 26, 43(2) internal control, 49, 50(1), 71, 86; Art 27 likely not applicable; Art 6(3) not applicable | A7.5 item 8 lists them, assigns provider and deployer roles, states internal control |
| AID-04 | Regulation (EU) 2026/1744 verified: Annex III from 2 Dec 2027 (Art 113(c)); Section 5 unsettled | A7.5 item 8; LANDSCAPE closed |
| AID-05 | Art 22(2)(a) contract basis unavailable; use explicit consent or human decisions; Arts 13(2)(f), 15(1)(h) | A7.1, A7.5 item 8, A7.7: explicit consent at filing with a human alternative, or human decision for natural persons |
| AID-06 | A company is not a data subject; its people's data are in scope | A7.5 item 4 reworded |
| AID-07 | Erasure may be refused under Art 17(3)(e); justify the period under Art 5(1)(e) | A5.9 reworded |
| AID-08 | C-203/22 official title CK v Magistrat der Stadt Wien | A7.5 item 8 |
| AID-09 | ADR Directive Arts 10(1), 10(2), 2(2)(g), 20; the Center is not an ADR entity | A3.2 item 8, A7.5 items 1, 7 and 8; "ADR-designed", "admitted" |
| AID-10 | Directive (EU) 2025/2647 verified: in force 19 Jan 2026, transposition 20 Mar 2028, applies 20 Sep 2028, outcome review right, listed entities only | A7.5 item 8 |
| AID-11 | ODR platform discontinued 20 Mar 2025; repealed 20 Jul 2025 | A7.5 item 8; no flow refers to it |

### D.4 Consumer law

| Row | Finding | Resolution |
|---|---|---|
| CON-01 | CRD Art 9(2)(b) possession; Art 14(1) "failed to inform"; Art 13(1) same means; Art 13(3) receipt or proof of dispatch | A4.4, A6.3 withdrawal row, A6.5 and A11.5 flows |
| CON-02 | Art 16 exceptions corrected: (c), (e) hygiene only, (i), (l) transport of goods, (m) three conditions; passenger transport outside the directive | A4.4 |
| CON-03 | Art 11a withdrawal function from 19 Jun 2026 missing | A4.4 requires it; `withdrawal` routed through it; A15.1 item 17 |
| CON-04 | SGD Arts 10(3), 11(2), 13 | A4.3 |
| CON-05 | Advance `accepted_deviations` likely fails Art 7(5) | Removed from the Mandate; per-purchase `deviation_acceptance` in the Approval Record (A4.3, A5.5) |
| CON-06 | "Free text binds nobody" conflicts with SGD Arts 6(a), 7(1)(d) | A4.1 Step 1 and A5.4 limited to the ABS decision |
| CON-07 | Digital content falls under the DCD 2019/770 | A4.3 cites it |
| CON-08 | UCTD Annex 1(q) evidence and burden limb; 1(b) | A8.4 jurisdiction table; A10.2 consumer-law row; evidence rules never imported into consumer terms |
| CON-09 | Rome I Art 6(2); Brussels Ia Art 19 post-dispute only | A10.2; `binding_effect.governing_law` and `forum` bind participants only |
| CON-10 | DSA Art 30 correct | Kept |

### D.5 Security, quality and data standards

| Row | Finding | Resolution |
|---|---|---|
| STD-01 | RFC 8785 is Informational, Independent Submission | A10.3 |
| STD-02 | RFC 9864 deprecates `EdDSA`; use `Ed25519` | A1.4, envelope `alg`, A10.3; `EdDSA` for legacy verification only |
| STD-03 | RFC 9162 Experimental | A7.5 item 3, A10.3 |
| STD-04 | Web Bot Auth WG chartered 23 Oct 2025; draft -01 of 29 Oct 2026 | A9.2, A10.1, A10.3; LANDSCAPE closed |
| STD-05 | SD-JWT VC (IETF draft) and W3C VCDM 2.0 are two formats; VC-JOSE-COSE; DID Core dates | A5.2, A10.3 |
| STD-06 | ISO 17442-1:2020 and -2:2020 | A10.3 |
| STD-07 | ISO 18245:2023 | A10.3 |
| STD-08 | ISO 10001/10002/10003:2018 are guidance; URLs fixed | A7.5 item 7, A10.3; LANDSCAPE URLs |
| STD-09 | ISO/IEC 42001:2023 requirements; 23894:2023 guidance | A7.5 item 8, A10.3 |
| STD-10 | ISO/IEC 27001:2022 with Amd 1:2024; 27002:2022 | A7.5 item 8, A10.3 |
| STD-11 | ISO/IEC 27701:2025 | A7.5 item 8, A10.3 |
| STD-12 | ISO 22301:2019 | Kept |
| STD-13 | ISO 9001:2026 | A7.5 item 8, A10.3 |
| STD-14 | ISO 20022 message names correct; versions | A10.3 |
| STD-15 | PCI DSS v4.0.1; SSF v2.0 standards; PA-DSS retired | A10.3 |
| STD-16 | PCI scope reduction, not automatic exclusion | A13 |
| STD-17 | C2PA 2.5 | A10.3 |
| STD-18 | No ESPR passport for consumer electronics; battery passports from 18 Feb 2027 | A8.5, A10.3, B2.1 |
| STD-19 | GS1 Digital Link 1.7.0 | A10.3 |
| STD-20 | eIDAS Arts 35(2), 41(2) | A10.3 |
| STD-21 | DORA Arts 2(1)(b),(d), 30, 31 | A7.5 item 5, A10.3 |
| STD-22 | Directive 2014/55 obliges public buyers to receive; supplier duty is national | B4 B2G row, A10.3 |
| STD-23 | ViDA: Council Directive (EU) 2025/516, 11 Mar 2025, 1 Jul 2030 | B4 B2B row, A10.3 |

### D.6 Licensing and authorisation

| Row | Finding | Resolution |
|---|---|---|
| LIC-01 | An ABS escrow account would be money remittance or e-money | B1.2 states both |
| LIC-02 | The arbiter must never be payer or payee | A1.3, A2, A6.2 enums, A7.7 |
| LIC-03 | The programme guarantee is presumptively insurance or suretyship | Removed from Part A; ABS-P2 allocates to the Register operator contractually; B1.2 lists the forms to be assessed; A15.1 item 14 |
| LIC-04 | The collection right's creditor must be the licensed PSP or acquirer, or the buyer | A6.1, A6.4 `collection_right.creditor` |
| LIC-05 | PIS authorisation for agent providers initiating A2A payments | A1.3, A6.4 `payment_initiation`, A9.2 |
| LIC-06 | PSR narrows the commercial-agent exclusion for platforms | B4 C2C and B2B2C rows |
| LIC-07 | "Accredited" overstates; use "admitted against published criteria" | A7.5 items 1 and 7, node schema, A14 |
| LIC-08 | Decisions bind participants by contract, never consumers: correct | Kept |

### D.7 LANDSCAPE rows

Every row the audit closed (PSD2 articles, SCA RTS, PSD3/PSR status, IPR dates, UK APP values, the
AI Omnibus, Directive 2025/2647, the ODR platform, DORA, eIDAS effects, Web Bot Auth, W3C VC and
DIDs, ISO 20022 applicability for SEPA, the ISO editions, EMV 3DS and tokenisation versions, the
EMVCo framework scope, Amex, PCI SSF, C2PA, GS1 Digital Link, ESPR and DPP, Directive 2014/55) is
updated in `LANDSCAPE.md` with the audit's source key. Rows the audit could not check (FAPI 2.0,
Grant Management, the ISO 8583 reference field, schema.org, ECLASS, ETIM, UCUM, ISO 8000, IOSS and
VIES, UNCITRAL ODR notes, NIST AI RMF, card spend-control practice, EN 16931 national mandates,
eIDAS wallet dates, Mastercard rules, VAMP figures) stay pending or UNVERIFIED.

### D.8 Claims withdrawn

Per the audit's section 4, v0.3 no longer claims: that a Decision executes a chargeback, recall or
return, or that the Decision Center can send one; that ABS reverses SCT or SCT Inst payments against
a refusing merchant, or that camt.027/087 carry goods disputes; that a buyer assigns rail disputes
to the programme; that a merchant's PSP can hold A2A funds already credited to the merchant; that a
programme guarantee pays the buyer; that mandate SCA covers later autonomous payments, that agent
purchases are MITs, or that EBA Q&A 2019_4664 supports either; that a payment without a
PSP-performed SCA mandate is an unauthorised payment; that payment rules give no refund right for
any authorised payment; that "no standard covers" the authorised-but-wrong split; "compliance with"
the AI Act, GDPR or ADR law; that nodes are accredited or the Center is an ADR entity; that advance
accepted deviations satisfy SGD Art 7(5), or that free text binds nobody in consumer law; that UK
APP reimbursement covers agent-deceived scams; that no card message lets a third party refund a
cardholder; that electronics carry a product passport today; that an agent provider is
automatically outside PCI DSS scope; that PSD3/PSR is adopted or in force, or that the IPR is
unchanged by it; and "Visa Core Rules §4.1.23", which are Product and Service Rules.

## Appendix E. Audit 1 corrections

Independent Audit 1 (`audits/AUDIT_1_INDEPENDENT_AI_REVIEW.md`, a read-only review of commit `3a6746d`) raised 30
findings across the paper, the code, the results and this standard. This appendix covers the
findings on the standard's text: F07, F10 (its standard part), F14, F15, F29 and F30. The others
concern the paper, the application, the code, the rulebook files and the analyses, and are resolved
or left open there. Section numbers are v0.3's after these corrections. Appendix D (Audit 2) is
unchanged.

| Row | Finding | Resolution |
|---|---|---|
| F29 | The opening premise misdescribed the dispute system: "every card dispute" turns on authorisation, and "no reason code fits", contradicted the standard's own mappings for not received, not as described and incorrect amount | Both claims removed. "What ABS is" states the narrower gap: faithful execution of delegated purchasing intent, that is instruction disputes (AG1-P) and capture disputes (AG1-C), with AG2 as the buyer-side counterpart, separated from merchant-performance claims (AG3, AG4, AG4-D, AG1-M) that keep the existing categories. The A3.1 opening, the AG3, AG1-P, AG1-C and AG2 rows, the A10.1 reason-code row and the one-pager rewritten to match |
| F07 | "Independent" conflated authorship, tamper evidence and authority for a fact; "only independent records decide" was not established; signed party records were listed as independent | The binary `provenance_tier` replaced by `provenance` (issuer, stake, time of commitment, custody, authority; `$defs/Provenance`, `$defs/FactKind`) on images, evidence references, merchant attachments and Finding citations, set by the verifier. A5.7 gives an authority table and a corroboration rule that names the fact it needs: (a) a record with independent authority, committed before the dispute by an issuer without a stake; (b) a record binding on the party it is used against; (c) the action log, for causation only. A per-step table lists the facts and the records that can corroborate each. "A signature proves origin, not truth" is stated. A1.2, A4.1 Step 1, A5.7 fairness paragraph, A8.1, A8.4, A8.7 and A15.1 item 19 aligned; certified capture now proves image integrity only. "The independent record decides, not the judge" withdrawn (change log, "What ABS is", A1.2, A5.7, A7.3, A7.9, A8.7, one-pager) and replaced by the measured statement: registry and carrier-weight records resisted the attacker on two case-sides against claude-fable-5-1; grok-4.7 was fooled on the same case-sides with the same records; no controlled record-removal or record-addition experiment exists. Decision `provenance_gate_reason` values and `corroborating_items_relied_on`, Finding `corroborated` and `corroboration_basis` follow |
| F14 | The signature covered only the body hash, leaving envelope type, version, id, timestamp and `prev_hash` outside it; the A5.8 chain was a separate construction; only 16 hex characters (64 bits) of the head reached the rail | A5.3 defines one authenticated context (`$defs/SignedContext`: a constant, version, type, id, `created_at`, chain id and position, `prev_hash`, `body_hash`), `envelope_hash` over it, and every signature over `envelope_hash` plus the signer's role, party, key id and signing time (`$defs/SignatureInput`); unknown envelope fields are rejected. The A5.8 chain is that chain of envelopes (`chain`, `prev_hash`, `ActionEvent` for agent actions), with fork and gap rules. The anchor is the full SHA-256 head, committed to the payer PSP's signed payment record, an ABS transparency log (proposed) or a qualified time stamp (`abs_binding.anchor_commitment`); the 16-hex value is a locator only, with the 2^32 chosen-pair note. Decision `anchor_commitment_verified` replaces `anchor_matches_rail_reference`. A1.4, A5.1, A5.2, A5.7, the A6.5 and A7.6 flows, A9.1, A9.3, A9.5, A13, A14, A15.1 item 8 and Appendix A aligned |
| F15 | The v0.3 envelope required `abs_version` "0.2", accepted any object as `body`, had no type-to-body dispatch and omitted `RefusalRecord`; the Mandate schema did not require the capture fields; parsing is not conformance | Wire version and every `$id` moved to 0.3, with a stated compatibility rule (A5.3 version policy: v0.2 objects are validated against the v0.2 schemas and admitted only as legacy evidence whose context is unauthenticated). The envelope's `allOf` dispatches `body` by `type` for all 16 types; `RefusalRecord` and `ActionEvent` added to the enum, and an `Offer` body schema added (B2.2), so no type lacks a body schema; `if`/`then` chain rules (no `prev_hash` at seq 0, `prev_hash` required from seq 1, `prev_hash` only inside a chain). The Mandate requires `proposed_by` and `user_confirmation`, and `conversation_hash` and a complete `template_profile` when the agent proposed it. `additionalProperties: false` added to the envelope, the Signature and the Participation Agreement. Appendix F gives 4 positive and 8 negative instances and the validation result |
| F30 | A5.2 "the same container" contradicted A5.3's separate envelope; no binding to AP2 / SD-JWT VC, UCP or ACP was demonstrated; the federated network read as operating | A5.2 rewritten: the ABS object travels in its own envelope, bound to the external object by hash, not inside it. Every AP2 / SD-JWT VC, Verifiable Intent, UCP and ACP binding marked PROPOSED ("What ABS is", A5.2, Offer Snapshot `external_object`, A9.5, A10.1, A10.3, B5, one-pager), as is the federated Decision Network (A7.5 status note, A7.6, A7.7, A14). A5.2.1 gives one binding sketch, labelled a proposal: an `abs_mandate` claim in the issuer-signed payload of an SD-JWT VC carrying the full `envelope_hash` of the ABS Mandate, the verification steps, the round trip, and what a real binding still needs. A15.1 item 20 |
| F10 (standard part) | "Natural-language term" against "encoded limit" (the former A4.1 sentences at audit lines 488 and 499) left open what binds | A4.1 Step 3 states what binds as an explicit term: a requirement captured in the signed Mandate, machine-readable or as signed text the user confirmed (the instruction text shown verbatim at the confirmation tap, or a clarification answered with authentication). Either is AG1-P when broken; only machine-readable terms are hard limits enforced before payment. Text said only in the conversation, or in a clarification answered without authentication, gives AG1-C if the agent should have captured it (Step 3b); intent never stated is AG2. Aligned: the A3.1 AG1-P, AG1-C and AG2 rows, the mandate-precision paragraph, the A4.4 remedies, the Mandate `intent_hash`, `conversation_hash` and `user_confirmation` and the Purchase Record `clarifications[].user_auth_reference` descriptions, the Finding `intent_match` value `stated_not_captured`, the A7.3 fact-finder list, a new A7.8 judgement row, Appendix A disputes 2 and 3, and A15.1 item 21. The A4 preamble states that the executable rulebooks (v1.2, v1.3) bind only machine-readable terms and are not updated; the rulebook, prompt and code parts of F10 lie outside this document |

**Claims withdrawn.** v0.3 no longer claims: that every card dispute turns on authorisation, or
that no reason code fits an agent purchase; that the independent record decides, not the judge, or
that only independent records stop an optimising attacker; that a user-signed Mandate or a
countersigned snapshot is independent of the parties; that device-signed capture shows what
arrived; that a signature over the body hash authenticates an object; that 16 hex characters of the
chain head are the anchor; that the ABS object is the same container as the AP2, UCP or ACP object;
that any protocol binding or the federated network exists or has been tested.

**Not resolved here.** Since these corrections the code has moved (other lanes, no model calls):
rulebook v1.4 implements A4, A4.4 and A6 and the reference engine reads it (F10, F11, F12;
`rulebook/VERSIONS.md`), but the arbiter prompt and the fact-finder schema have no v1.4 version and
no model has run under v1.4; a provenance gate v2 resolves exact paths, reads record content and
treats each allegation separately (F05, F06), but is exploratory and still uses the binary tier by
record type, not the A5.7 provenance object (code part of F07; the differences are listed in
`results/PHASE3B_PROVENANCE.md`, Section 10); the integrity check now compares the displayed record
with the chain and the head with an independently held anchor (F13), though the bundle is still not
built from A5.3 envelopes; the hybrid has a separately versioned decision contract v2 that applies
0.7 at the decision point (F08, F09). No AP2 fixture or round-trip test exists (F30), and the
examples of Appendix F were checked with a subset validator, not a full JSON Schema implementation.
The A5.7 gate as written is unmeasured.

**Numbers carried in (2026-11-04, final Audit 1 pass; re-analysis of stored records, no new model
calls; sources: `standard/sim/REPORT.md` "Post-audit (Audit 1)", `results/PHASE3_ATTACKS.md`
Section 6, `results/PHASE3B_PROVENANCE.md` post-audit headline,
`results/AUDIT1_CORRECTIONS_PHASE1_2.md`, `results/PREREGISTRATION.md` "Post-audit amendment").**
Simulation (F16, F17, F25): E3 "498 of 498 decided (100%)" becomes 496 determinate and 2 escalated,
0 with no rule, as consistency against stipulated findings; v0.2 "528 of 528 decided" becomes 526
determinate, 2 escalated, 528 of 528 consistent; settlement 357 / 9 / 26 becomes 334 / 9 / 26 of
369 funds-moving; without the anti-scam gate 0 / 31 / 15 becomes 0 / 28 / 3 conditional / 15;
buyer loss "EUR 4,783" and "EUR 1,837" (currencies summed) become per-currency amounts (A4.2,
A5.1, A6.1, A8.5, B1.1, A15.2). Phase 3 (F02, F23): 12 of 14 against the hybrid's 6 of 14 is an unequal-budget,
descriptive comparison; at a common 5 attempts 10 of 14 against 6 of 14, p = 0.125; "attempts per
success" is renamed aggregate attempts expended per successful case-side, with first success among
fooled case-sides at a mean of 2.25 (median 1); "within 4 attempts" removed (A7.3, A7.9, A8.7,
A15.2). Phase 3b (F03, F04, F05, F22): the same-call effect 11 to 1 and 12 to 1 leads, H10's 12 to 1
is labelled confounded; rejections split format / provenance / contradiction; gate v2 figures
added as exploratory; "honest cases" is the baseline Phase 2 workload, with review falling on 22 of
31 true claimants against 2 of 19 unfounded claims (A5.7, A7.3, A7.9, A8.4, A8.7, A15.2). Phase 2
(F08, F09, F10, F11, F21, F28): 0 of 75 becomes 0 of 25 cases (upper bound 13%) and 3 of 75 becomes
1 of 25; the 2.45 error ratio is the relaxed post-hoc figure and the strict one is 1.24; the
historical hybrid's 0.7 governed only the tie-break; the "rail-dispute rate" is the residual route
rate; against the v1.4 labels the E3 decisions score 45 and 44 of 51 (A4.2, A7.3, A7.9, A8.6,
A15.2). Phase 1 (F01, F18): 0 of 80 executed is scoped to the claude-opus-5-5 attacker (a grok-4.5
attacker executed 1 of 12); the capture probe's 40 of 40 sits beside the typed re-score 36 faithful,
2 safely stricter, 2 failing (A9.3, A15.2). The A4 preamble now names rulebook v1.4 as the
executable form of A4.

## Appendix F. Example instances

Each block names the schema it is checked against and whether it must validate. A negative example
is a JSON Patch (RFC 6902) applied to a positive one (`base`; `select` first picks a sub-document),
so it differs from a valid object in exactly the way its caption names. `body_hash` and
`envelope_hash` are computed by the rules of A5.3 over these bodies (JCS taken as sorted-key compact
JSON, which is exact for these values), and F.2's `prev_hash` is F.1's `envelope_hash`. Signature
values are illustrative only: they have the shape of a detached-payload JWS, but no key material is
published for them and they do not verify. Hashes that stand for external artefacts (an allowance
policy, a conversation record, a registry record, a purchase record) are SHA-256 values of a
descriptive label.

**Validation (2026-11-04).** No JSON Schema library was available and none was installed. The
examples are checked with a minimal draft 2020-12 subset validator that now lives in the repository
(`tools/schema_check`, with tests) and runs in CI (`python -m tools.schema_check standard/ABS_v0.3.md`). It implements every keyword these schemas use (`$ref` with sibling
keywords, `type`, `enum`, `const`, `required`, `properties`, `additionalProperties`, `items`,
`minItems`, `minLength`, `maxLength`, `pattern`, `minimum`, `maximum`, `format` asserted for
date-time, date and uri, `allOf`, `anyOf`, `oneOf`, `not`, `if` and `then`), refuses any other,
and passed its own positive and negative self-tests. Result: all 23 schemas resolve and use only
that subset; F.1 to F.4 validate; F.5 to F.12 each fail, and fail for the reason in their caption.
The envelope examples' hashes, chain link and rebuilt signed context were recomputed and match. This
is evidence of schema consistency, not a conformance result from a full implementation, and a run
against one is still owed.

**F.1** (valid against `urn:abs:schema:0.3:envelope`). Mandate at the genesis of a purchase chain
(seq 0, no prev_hash); proposed by the agent, so conversation_hash and template_profile are present;
signed by user and agent provider.

```json
{
  "example": "F.1",
  "schema": "urn:abs:schema:0.3:envelope",
  "expect": "valid",
  "instance": {
    "abs_version": "0.3",
    "type": "Mandate",
    "id": "urn:abs:mandate:7c1e2a40-5b6d-4e8f-9a0b-1c2d3e4f5a6b",
    "created_at": "2026-11-04T09:12:31Z",
    "chain": {
      "chain_id": "urn:abs:mandate:7c1e2a40-5b6d-4e8f-9a0b-1c2d3e4f5a6b",
      "seq": 0
    },
    "body": {
      "mandate_id": "urn:abs:mandate:7c1e2a40-5b6d-4e8f-9a0b-1c2d3e4f5a6b",
      "allowance_policy_id": "urn:abs:allowance-policy:0b9d8e7f-6a5b-4c3d-8e1f-2a3b4c5d6e7f",
      "allowance_policy_hash": "sha256:adc55a340ef594d26bcb66f4ab0084ebc06bde6748e6e4900dc314fdc83bcf73",
      "user_ref": "u-5f2c91",
      "agent_provider": {"party_id": "prov-acme-agents", "role": "agent_provider"},
      "agent_id": "acme-shopper@4.2",
      "intent_hash": "sha256:ebe841aa2b4eb41d436eba2c482d382f2ea46a0013ffa20797f75fef8238b7b1",
      "proposed_by": "agent",
      "conversation_hash": "sha256:48c28e7f40371e9c52bc53b4d8b0aa257707c8dc7a127bd29470f150de9de1eb",
      "template_profile": {"id": "abs:profile:electronics", "version": "0.3", "prompted_attributes": ["model_identifier", "condition", "colour"], "left_open": ["colour"]},
      "user_confirmation": {"confirmed_at": "2026-11-04T09:12:30Z", "shown_terms_hash": "sha256:3413157b4505d1092e1719df44611ab7a45cc1a686da050d7986ef1bec64d84a"},
      "max_total": {"amount": "350.00", "currency": "EUR"},
      "max_units": 1,
      "condition_allowed": ["new"],
      "item_requirements": [{"name": "model_identifier", "value": "WH-1000XM6", "binding": true, "verification_method": "label_read"}, {"name": "condition", "value": "new", "binding": true, "verification_method": "visual_match"}],
      "ask_on_ambiguity": true,
      "valid_from": "2026-11-04T09:12:30Z",
      "expires_at": "2026-11-11T09:12:30Z",
      "autonomy_required": "approval_required",
      "authentication": {"method": "sca_app", "performed_at": "2026-11-04T09:12:29Z", "reference": "psp-auth-88123", "assurance": "psd2_sca"},
      "rulebook_version": "abs-liability@0.3",
      "nonce": "n-3f9a1c2e4d5b6a70"
    },
    "body_hash": "sha256:afd975b63b91e23afa3c7a08c28257ed9749c34f3995834d9b6db404e9f75b2b",
    "envelope_hash": "sha256:b22f47c7136b9b62c54f812cd572ef0f6fbc950d89bafcdb1c26d6e82f59af20",
    "signatures": [{"role": "user", "party_id": "u-5f2c91", "kid": "user-key-1", "alg": "Ed25519", "sig": "eyJhbGciOiJFZDI1NTE5Iiwia2lkIjoidXNlci1rZXktMSJ9..BPJfDbAdNriujl1-T60qdb70a-TVW1pZ8uIrarN99gradj6no4dT7vO72aMMtvuMC2L1NmuTNzYYP-CO837Cmg", "signed_at": "2026-11-04T09:12:31Z"}, {"role": "agent_provider", "party_id": "prov-acme-agents", "kid": "prov-key-3", "alg": "Ed25519", "sig": "eyJhbGciOiJFZDI1NTE5Iiwia2lkIjoicHJvdi1rZXktMyJ9..tXIixKIt0Yyxej7SGI2bbbP5MUOPagJTW9VRozHsd_2gPua9bmWH7UuZQtaUqMZlKUnlz-kDZfZwoOVZ9t88hg", "signed_at": "2026-11-04T09:12:31Z"}]
  }
}
```

**F.2** (valid against `urn:abs:schema:0.3:envelope`). RefusalRecord as the next event of the same
chain: seq 1, prev_hash = envelope_hash of F.1.

```json
{
  "example": "F.2",
  "schema": "urn:abs:schema:0.3:envelope",
  "expect": "valid",
  "instance": {
    "abs_version": "0.3",
    "type": "RefusalRecord",
    "id": "urn:abs:refusal-record:1d2c3b4a-5e6f-4a7b-8c9d-0e1f2a3b4c5d",
    "created_at": "2026-11-04T09:20:03Z",
    "chain": {
      "chain_id": "urn:abs:mandate:7c1e2a40-5b6d-4e8f-9a0b-1c2d3e4f5a6b",
      "seq": 1
    },
    "prev_hash": "sha256:b22f47c7136b9b62c54f812cd572ef0f6fbc950d89bafcdb1c26d6e82f59af20",
    "body": {
      "refusal_id": "urn:abs:refusal-record:1d2c3b4a-5e6f-4a7b-8c9d-0e1f2a3b4c5d",
      "mandate_id": "urn:abs:mandate:7c1e2a40-5b6d-4e8f-9a0b-1c2d3e4f5a6b",
      "refused_at": "2026-11-04T09:20:02Z",
      "offers_compared": [{"snapshot_id": "snap-b-0001", "offer_hash": "sha256:a874249e575bf250094e70542c2df68e9e5afbad048d4f56f0b13c494d0f55d1", "merchant": {"party_id": "m-reboxed", "role": "merchant"}}],
      "reason_code": "no_conforming_offer",
      "reason": {"text": "Offer B is refurbished; the Mandate allows new only.", "class": "untrusted_text"}
    },
    "body_hash": "sha256:272e1cc64ee2b5552e08761db4a5f8420fba57639a817eff070d8feeab6e9e07",
    "envelope_hash": "sha256:1e6786b16e92d34e8025479add7319d47a38d731efe448f5932b7795c369c54a",
    "signatures": [{"role": "agent_provider", "party_id": "prov-acme-agents", "kid": "prov-key-3", "alg": "Ed25519", "sig": "eyJhbGciOiJFZDI1NTE5Iiwia2lkIjoicHJvdi1rZXktMyJ9..tfLZBejeKTb4VV6LFOM25biisTT06hOzSU3KEWKah8nud2HdcbPndO-siJT2BD6My51rzpnWZCws3soL-CixEQ", "signed_at": "2026-11-04T09:20:03Z"}]
  }
}
```

**F.3** (valid against `urn:abs:schema:0.3:envelope`). Finding outside any chain, with one citation
that carries a provenance description and meets test (a) of A5.7.

```json
{
  "example": "F.3",
  "schema": "urn:abs:schema:0.3:envelope",
  "expect": "valid",
  "instance": {
    "abs_version": "0.3",
    "type": "Finding",
    "id": "urn:abs:finding:9e8d7c6b-5a4f-4e3d-9c2b-1a0f9e8d7c6b",
    "created_at": "2026-11-20T10:00:01Z",
    "body": {
      "finding_id": "urn:abs:finding:9e8d7c6b-5a4f-4e3d-9c2b-1a0f9e8d7c6b",
      "case_id": "urn:abs:dispute-case:2a3b4c5d-6e7f-4a8b-9c0d-1e2f3a4b5c6d",
      "node_id": "node-eu-1",
      "finder": {"kind": "verifier", "id": "abs-verifier@0.3.0"},
      "type": "offer_conformity",
      "subject": {"line": 1, "field": "model_identifier", "party": "merchant"},
      "value": "non_conforming",
      "confidence": 1,
      "cited_evidence": [{"item_id": "registry-record-sony-eu-0001", "path": "/units/0/model_identifier", "hash": "sha256:94e31968908961e61b59f49585ece265fc530c3529fd8c98c12061530b51969b", "record_type": "serial_lookup", "provenance": {"issuer": {"role": "registry", "party_id": "reg-sony-eu"}, "stake": "none", "committed": {"at": "2026-11-05T16:40:00Z", "relative_to_dispute": "before", "proof": "issuer_signed"}, "custody": {"held_by": "registry", "integrity": "issuer_signature_verified"}, "authority_for": ["unit_identity", "unit_sale_history"], "signature_verified": true}, "fact": "unit_identity", "attribute": "model_identifier", "support": "supports", "support_check": "deterministic"}],
      "corroborated": true,
      "corroboration_basis": "independent_authority",
      "deterministic": true,
      "produced_at": "2026-11-20T10:00:00Z"
    },
    "body_hash": "sha256:89ca29940473c947b41edb6466559e2836daf743ee074cbe2ccb37e64dbfe44f",
    "envelope_hash": "sha256:ecff4f8ec44e39c35596eac3acf7e1b0497a5f338714e0dbd3159f1e0a32e73a",
    "signatures": [{"role": "arbiter", "party_id": "node-eu-1", "kid": "node-eu-1-key-2", "alg": "Ed25519", "sig": "eyJhbGciOiJFZDI1NTE5Iiwia2lkIjoibm9kZS1ldS0xLWtleS0yIn0..nsHTPGcOJ6rDh9FrKuLfoIuy8iTlP9t1beh2nun7ayoUwLlkirwe1vypgNMUFEK5d-rulvNgHRWZXwrKQ3gQCw", "signed_at": "2026-11-20T10:00:01Z"}]
  }
}
```

**F.4** (valid against `urn:abs:schema:0.3:settlement-instruction`). Settlement Instruction body:
the full head is in anchor_commitment; the rail reference carries only the 16-hex locator.

```json
{
  "example": "F.4",
  "schema": "urn:abs:schema:0.3:settlement-instruction",
  "expect": "valid",
  "instance": {
    "settlement_id": "urn:abs:settlement-instruction:3c4d5e6f-7a8b-4c9d-8e0f-1a2b3c4d5e6f",
    "purchase_id": "urn:abs:purchase:4d5e6f7a-8b9c-4d0e-9f1a-2b3c4d5e6f7a",
    "purchase_hash": "sha256:ee187aaaaabdd0d3f5245e72e0b053f350dd1b9b783416a00ca551b3ad9fc749",
    "instruction_seq": 1,
    "direction": "pay",
    "amount": {"amount": "329.00", "currency": "EUR"},
    "payer": {"party_role": "user", "instrument_ref": "tok-agent-77"},
    "payee": {"party_role": "merchant", "account_ref": "acq-merchant-a"},
    "rail": {"type": "card", "network": "visa"},
    "abs_binding": {"reference_field": "additional_data", "reference_value": "ABS:urn:abs:purchase:4d5e6f7a-8b9c-4d0e-9f1a-2b3c4d5e6f7a:ee187aaaaabdd0d3", "anchor_commitment": {"head": "sha256:ee187aaaaabdd0d3f5245e72e0b053f350dd1b9b783416a00ca551b3ad9fc749", "store": "psp_record", "store_ref": "psp-pay-2026-11-04-000731", "committed_at": "2026-11-04T09:31:07Z"}},
    "timing": {"mode": "immediate"}
  }
}
```

**F.5** (invalid against `urn:abs:schema:0.3:envelope`, patch of F.1). The v0.3 envelope accepts
only abs_version 0.3; a v0.2 object goes to the v0.2 schemas under the version policy (A5.3).

```json
{
  "example": "F.5",
  "schema": "urn:abs:schema:0.3:envelope",
  "expect": "invalid",
  "base": "F.1",
  "patch": [{"op": "replace", "path": "/abs_version", "value": "0.2"}]
}
```

**F.6** (invalid against `urn:abs:schema:0.3:envelope`, patch of F.2). Type-to-body dispatch: a
RefusalRecord body under type Mandate fails the Mandate schema.

```json
{
  "example": "F.6",
  "schema": "urn:abs:schema:0.3:envelope",
  "expect": "invalid",
  "base": "F.2",
  "patch": [{"op": "replace", "path": "/type", "value": "Mandate"}]
}
```

**F.7** (invalid against `urn:abs:schema:0.3:envelope`, patch of F.2). A chain event with seq 1 must
carry prev_hash (binding to the A5.8 chain).

```json
{
  "example": "F.7",
  "schema": "urn:abs:schema:0.3:envelope",
  "expect": "invalid",
  "base": "F.2",
  "patch": [{"op": "remove", "path": "/prev_hash"}]
}
```

**F.8** (invalid against `urn:abs:schema:0.3:envelope`, patch of F.1). No envelope field may sit
outside the authenticated context: unknown envelope fields are rejected.

```json
{
  "example": "F.8",
  "schema": "urn:abs:schema:0.3:envelope",
  "expect": "invalid",
  "base": "F.1",
  "patch": [{"op": "add", "path": "/note", "value": "unsigned remark"}]
}
```

**F.9** (invalid against `urn:abs:schema:0.3:mandate`, patch of F.1). A Mandate proposed by the
agent must record the conversation it was proposed from (capture provenance, A4.1 Step 3b).

```json
{
  "example": "F.9",
  "schema": "urn:abs:schema:0.3:mandate",
  "expect": "invalid",
  "base": "F.1",
  "select": "/body",
  "patch": [{"op": "remove", "path": "/conversation_hash"}]
}
```

**F.10** (invalid against `urn:abs:schema:0.3:finding`, patch of F.3). The binary v0.2 label is
gone: a citation must carry the provenance description.

```json
{
  "example": "F.10",
  "schema": "urn:abs:schema:0.3:finding",
  "expect": "invalid",
  "base": "F.3",
  "select": "/body",
  "patch": [{"op": "remove", "path": "/cited_evidence/0/provenance"}, {"op": "add", "path": "/cited_evidence/0/provenance_tier", "value": "independent"}]
}
```

**F.11** (invalid against `urn:abs:schema:0.3:settlement-instruction`, patch of F.4). The 16-hex
locator alone is not a commitment: anchor_commitment with the full head is required.

```json
{
  "example": "F.11",
  "schema": "urn:abs:schema:0.3:settlement-instruction",
  "expect": "invalid",
  "base": "F.4",
  "patch": [{"op": "remove", "path": "/abs_binding/anchor_commitment"}]
}
```

**F.12** (invalid against `urn:abs:schema:0.3:settlement-instruction`, patch of F.4). A truncated
hash is never a commitment: Hash requires all 64 hex characters.

```json
{
  "example": "F.12",
  "schema": "urn:abs:schema:0.3:settlement-instruction",
  "expect": "invalid",
  "base": "F.4",
  "patch": [{"op": "replace", "path": "/abs_binding/anchor_commitment/head", "value": "sha256:ee187aaaaabdd0d3"}]
}
```

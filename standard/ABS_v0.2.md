# Agentic Buying Standard (ABS) v0.2

Status: draft for review, 2026-11-04. Not published. Idea and principles: Vadims Juruss.
Document structure after the founder's decision of 2026-11-04 and Independent Audit 0
(`audits/AUDIT_0_THESIS.md`): **Part A** is the normative core, the contribution. **Part B** is an
informative roadmap annex. v0.2 adopts the rules proposed by the rule-completeness simulation
(`standard/sim/REPORT.md`, rule set `scrolld.abs@0.2-proposed`), which measured v0.1 as written
against a 524-scenario catalogue and found 8 gap types, 4 unresolved conflicts and 58 contradiction
groups; the adopted wording closes all of them against that catalogue. No scheme rule number,
article or date is quoted unless it was verified or is cited from Audit 0 with its source;
unverified items are marked. `LANDSCAPE.md` holds the sources for everything in section A10.

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
outside its scope; the card networks have no agent-specific dispute condition (Audit 0, Q1). ABS
contributes:

1. a **dispute taxonomy** for agent purchases, including "authorised but wrong", mapped onto the
   reason-code categories issuers and merchants already use;
2. a **liability decision order** in which the precision of the mandate decides;
3. a **minimum evidence standard**: the Evidence Package an agent purchase must carry, how it is
   signed, who holds it, and what the evidence levels E0 to E3 are;
4. **Decision Center governance**: LLM fact-finders, deterministic rules, signed receipts, human
   review on request, compliance with the EU AI Act, the GDPR and ADR law, and neutrality;
5. a **settlement mapping** of decisions onto existing card and ISO 20022 flows;
6. the **layering** onto AP2/FIDO, UCP/ACP and TAP/Agent Pay, with an injection-safety profile for
   catalogues;
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
   a dispute is not locked inside one party.
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
- ABS does not remove, limit or discourage chargebacks or rail recalls. Those rights come from
  scheme rules and, in some jurisdictions, consumer-credit law. On account-to-account rails, where
  no such right exists, ABS adds a contractual refund obligation and a payout hold on unproven
  merchants.
- ABS does not replace statutory consumer rights: withdrawal, conformity guarantees,
  unauthorised-payment refunds. A Decision never reduces them and never binds a consumer beyond
  what the law allows.
- ABS does not promise to keep every scammer out. It makes sure an unproven merchant is not paid
  before confirmed delivery, that a merchant that turns bad is caught within a bounded number of
  purchases, and that the buyer is made whole either way (Part B1).
- ABS does not hold funds. Payout holds, reserves and collections run through licensed PSPs and
  acquirers.
- ABS does not set an operator's fee model.

### A1.4 Conventions

MUST, SHOULD and MAY have their usual standards meaning. "Buyer side" means the user and the agent
provider together. "Rulebook" means the current version of sections A3 to A7, identified by version
and hash. Money is a decimal string plus an ISO 4217 currency; floats are never used. Timestamps
are RFC 3339 in UTC. Hashes are SHA-256 over the RFC 8785 canonical JSON of an object body, written
`sha256:<hex>`. Signatures are JWS (RFC 7515), compact serialisation, detached payload; permitted
algorithms in v0.2 are EdDSA (Ed25519) and ES256. Schemas are JSON Schema 2020-12.

### A1.5 Measures of success

All bands are working hypotheses for a pilot, each with the baseline it must beat. Audit 0 gives
the baselines with sources.

| KPI | Definition | Baseline to beat | Working band |
|---|---|---|---|
| Correct allocation | Share of tier 2 decisions whose liable party stands after appeal and sampling review | None exists for agent disputes | 97% or better; measured in the experiment as liable-party accuracy (H5, H6) |
| Time to decision | Median filing to Decision at E3 | Card disputes run weeks to months | Days at most; minutes for automated decisions |
| Human residual | Share of tier 2 cases needing a human Finding, plus human reviews requested | None | Measured and published |
| Rail-dispute rate (secondary) | Share of ABS disputes a party still takes to a chargeback or recall, after or instead of the ABS process | None | Reported, not targeted; the user keeps every rail right |
| Scam payout rate (Part B1) | Share of non-delivery cases where the merchant was paid before delivery was confirmed | Marketplace holds (DD+7, up to 21 days) achieve near zero on held merchants | Zero on held merchants |
| Scam loss rate (Part B1) | Non-delivery by an unreachable or expelled merchant, by value | EEA card fraud 0.033% of value in 2024; remote 0.091% (EBA/ECB, Dec 2025, per Audit 0) | Must be shown below the remote-fraud baseline for the same value mix before any claim |
| Honest-merchant false reject (Part B1) | Merchants refused or suspended whose appeal succeeds or who are later qualified without new facts | None public | Below 2%; H7 allows at most 10% in simulation |

Reasons a party may still go to the rail after ABS: an arbiter error the party rejects; a merchant
that vanished where no payout hold was in place and collection failed; a contested decision; a
statutory or scheme right the user prefers; a rail deadline approaching before the ABS decision;
and AG0 cases, which belong to the rail by design.

---

## A2. Roles and neutrality

| Role | Who | Holds | Signs |
|---|---|---|---|
| User | The person or business the purchase is for. | Intent, payment instrument, delivery address, the Allowance Policy. | Allowance Policy; Mandate; approvals; clarifications; conformity acknowledgement; dispute filing. |
| Buying agent | Software that searches, compares, orders and pays under the mandate. | Action log, snapshots. | Nothing on its own; it acts under the agent provider's key. |
| Agent provider | Operator of the buying agent. Liable for its agent's fault on the record (AG1-P). | Keys, the full trace, the intent text. | Participation Agreement; Offer Snapshot; Purchase Record; Settlement Instruction; filings by the agent. |
| Merchant | The seller. May act through a merchant agent under the merchant's key. Liable for conformity and for its own content. | Offer feed, fulfilment, packing records. | Participation Agreement; offers; order acceptance (countersigns the Offer Snapshot); Delivery Record (shipment part); dispute response. |
| Payment rail, PSP, issuer, acquirer | Networks, instant-payment schemes, wallets, banks, processors. Hold merchant underwriting, payout holds, reserves and the existing reversal tools. | Authorisation, clearing, settlement, reversals. | Rail result appended to the Settlement Instruction; `rail_enforcement` acknowledgement. |
| ABS arbiter (Decision Center) | The neutral body that decides tier 2 and enforces decisions against participants by contract. | Registry, rulebook versions, case files, receipts. | Participation Agreement (countersign); Decision; Decision Receipt. |
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

Agent purchases break the question every card dispute rests on, "did the cardholder authorise
this?", because the agent did authorise it. The codes below are the agent-specific taxonomy. Each
is mapped onto the category an issuer or merchant uses today, so the existing machinery carries it
where a category fits and the new codes stand where none does.

| Code | Name | Liable | Existing category it extends | Why a new code is needed |
|---|---|---|---|---|
| AG0 | No valid mandate | Rail process (issuer or payer PSP under law) | Unauthorised / fraud | Not new: routes the case out of ABS to the rail |
| AG3 | Non-conformity: not received, differs from the frozen offer, counterfeit, listing edited after purchase, over-charge against the snapshot | Merchant | Not received; not as described or defective | The reference is the countersigned snapshot, not a later listing |
| AG4 | Injection via merchant content | Merchant | Not as described / misrepresentation (new sub-reason) | Today's categories have no notion of content that steered an agent |
| AG1-M | Merchant-added items or fees the agent did not choose | Merchant | Processing error (incorrect amount); not as described (added items) | The "agent did not select this line" fact comes from the cart's `added_by` |
| AG1-P | Agent fault on the record: an explicit mandate or Allowance term broken, an explicit instruction or clarification ignored, a guess where told to ask | Agent provider (or the PSP that enforced the breached control) | None: authorised, so no rail code | The gap: authorised, not fraud, provably outside the explicit mandate |
| AG2 | Authorised but wrong: fits the explicit mandate, not the unstated intent | Buyer | None (no dispute right) | Names the other half of "authorised but wrong" so it is not misfiled as fraud or not-as-described |
| AG5 | User error, change of mind, or a false claim | Buyer | None | Includes claims the evidence contradicts; carries a conduct finding |
| AG4-D | Deceptive offer content: a statement of fact in merchant content shown false (reference price never charged, false scarcity, invented urgency, endorsements) that the log shows influenced the choice | Merchant | Misrepresentation | Separates deception by false facts from injection by instructions |

**Supporting codes.** The simulation showed that a dispute system needs rules for standing,
authorisation, conduct and evidence that the six main codes do not carry. v0.2 adds them; the
counts are how often each decided one of the 524 catalogue scenarios under the v0.2 rules.

| Code | Meaning | Outcome | Decisions |
|---|---|---|---|
| ABS-C1 | Conduct: knowingly false or altered evidence | Decided against the submitter | 7 |
| ABS-E1 | Adverse inference: a required record keeper cannot produce its record (agent provider: Mandate and action log; merchant: Offer Snapshot and packing record) | The question that record would answer is decided against the keeper | 10 |
| ABS-H1 | Records conflict and no keeper is at fault | `review`: a fact-finder supplies the finding, with human review | 2 |
| ABS-S1 | Unsigned spec: the agent compared on an unconfirmed extracted spec (agent provider bears the mismatch) or the participant sold without a signed spec (its ambiguity construed against it) | Refund by the party at fault | with S2: 13 |
| ABS-S2 | Ambiguous Offer Snapshot construed against its author | Refund by the merchant | |
| ABS-P1 | Payment to a non-participant, or outside the mandate-bound credential | Agent provider bears the loss the rail does not recover | with P2: 22 |
| ABS-P2 | Forged Register entry passed a correct verification | Programme guarantee pays and recovers | |
| ABS-F1 | Offer Feed signature did not verify (agent provider bears it) or was made with a leaked merchant key not yet revoked (merchant answers for its key) | Refund by the party at fault | 4 |
| ABS-X1 | Collusion: merchant and agent provider share an undisclosed arrangement | Jointly and severally liable; both suspended pending review | with X2: 12 |
| ABS-X2 | Undisclosed incentive steered the choice | Agent provider owes the difference against the best conforming offer it saw | |
| ABS-R1 | Apportionment across components decided under different steps | Each component to its own party | 4 |
| ABS-D1 | Default on merchant silence | Buyer's account of facts within its knowledge accepted | with D2, G1: 6 |
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
   (ABS-D2).
9. **Binding effect and statutory rights.** A Decision binds merchants and agent providers by
   contract. It does not bind a consumer beyond what the law allows: the consumer keeps the courts,
   statutory ADR, chargebacks, withdrawal and conformity rights. Time limits and decisions under
   ABS do not reduce the buyer's statutory rights; the Decision states which statutory route
   remains open, and where the EU withdrawal right applies and the buyer invokes it, the Settlement
   Instruction executes the withdrawal refund on the same rail.

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
| Pay a decided amount | 10 days from the Decision |
| Return goods under a refund-with-return or under withdrawal | 14 days from the Decision or the withdrawal notice |

---

## A4. Liability decision order

One rule, decided by how precise the mandate is. It mirrors the Agentic Dispute Rulebook v1.2 in
this repository, the ground truth of the experiment. The agent provider is liable only when the
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
shown to be forged, the programme guarantee pays the buyer and pursues recovery; the agent provider
is not liable (ABS-P2). A public authority is a permitted payee without a Participation Agreement
when the agent verified it in the official registry; ABS decides only whether the agent stayed
inside the Mandate, and claims against the authority follow administrative appeal (ABS-G1).

**Step 0. Authorisation (AG0).** Before Step 1 the arbiter checks that (a) the Mandate was created
by the account holder with strong authentication performed by a PSP, and (b) the charge was
initiated by the buyer's agent under that Mandate, before its expiry, with the mandate-bound
credential. If (a) fails, the case is an unauthorised payment: ABS refers it to the rail's
unauthorised-payment procedure and supplies the Mandate record; the buyer is not liable under ABS.
If the provider's systems issued the charge without a valid Mandate (compromise, or a Mandate
accepted without strong authentication), the agent provider is liable. If (b) fails because the
merchant presented the credential again or charged after expiry, the merchant is liable for that
charge. A Mandate without strong authentication is invalid.

**Conduct (ABS-C1).** Knowingly false or altered evidence decides the dispute against the party
that submitted it; a broken record chain counts against the party that kept it.

**Step 1. Conformity. A non-conforming delivery makes the merchant liable (AG3).** Compare what
was delivered with the frozen Offer Snapshot's conformity-critical attributes, each within its
tolerance by its verification method (A5.4), and with condition, quantity, package contents,
identity images, price and fees charged, and delivery within the stated terms. Weigh the delivery
evidence (A5.6): serial numbers against the registry and the packing record, photo metadata
against the delivery date, parcel weight against the item. Non-delivery and counterfeit goods do
not conform. If the delivery does not conform, the merchant is liable whatever the agent did. Free
text and non-binding attributes never ground this step.

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
merchant that cannot produce the packing record it was required to keep has the conformity
question decided against it (ABS-E1m). A not-as-described claim with no content evidence from the
buyer, against a packing record and serials consistent with the snapshot and a carrier proof of
handover, fails under Step 4 (ABS-E2). Where the packing record and the photographed serial
conflict and no keeper is at fault, the engine returns `review` (ABS-H1).

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

- broke an explicit term of the Mandate or Allowance Policy. "What the mandate states" means every
  explicit, machine-readable term in the signed Mandate or Allowance: the hard limits (amount,
  category, merchant rule, units, expiry, delivery country, a required approval or notification, a
  qualified merchant) **and** the captured item requirements (`item_requirements[]`: model,
  variant, capacity, size, colour, region or plug type, condition, package contents); or
- ignored an explicit instruction or clarification in the buyer's stated intent ("new, not
  refurbished", "in white", "only at a genuine discount", "if unsure, ask me first"); or
- guessed where the mandate told it to ask.

Explicit natural-language terms in the signed intent count as terms; captured item requirements
are the same terms in machine-readable form. The full list of fields that are hard limits when
set: amount, category, merchant rule, units, expiry; required attributes (colour, size, model,
dates, reference, deadline); a scope flag ("only the item named", on by default); the pay-in
currency and an FX tolerance; the delivery address; whether a step-up is required and the exact
content an approval prompt must show (item and amount); the autonomy level per category;
per-transaction and periodic budgets, including split purchases that evade a per-transaction
limit; delegate roles and limits; invoice data (PO number, VAT ID, e-invoice format) and payment
terms for business buyers; procurement thresholds and framework allowlists for public buyers; the
minimum merchant Trust Attestation level; for recurring purchases the period and maximum number of
charges; and a policy version, with changes taking effect when the agent acknowledges them. Only an
encoded limit is a hard limit; unstated intent stays with the user.

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

**Step 3b. Capture failure. The agent provider is liable (AG1-P, capture).** The purchase fits
every term that was captured in the Mandate, but the record of the conversation that produced the
Mandate, or a later clarification, shows that the user stated an explicit requirement ("the black
one", "must work in the EU", "only if it arrives by Friday") and the agent failed to capture it into
the Mandate's terms or item requirements. The precision burden falls on the system that writes the
mandate, not on the user who confirms it. The agent provider keeps the conversation record
(`conversation_hash` in the Mandate; the transcript is disclosed in a case at E2) and bears the
loss when it cannot produce it (ABS-E1). What the user said but did not state as a requirement,
and what the user meant without saying, is not a capture failure; it is Step 4.

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

Precedence for the same component: standing, AG0, ABS-C1, AG3 (with S1, S2, E1m, E2, H1, D1),
AG4, AG4-D, AG1-M, ABS-X1, ABS-F1, AG1-P (with X2, E1), AG2, AG5.

**Mandate precision, and who carries the burden.** A requirement is enforceable only if it is
captured in the mandate: as a hard limit, as a machine-readable item requirement, or as an explicit
sentence in the signed intent. "I wanted the black one" thought but never said is AG2; "colour:
black" in `item_requirements` before the purchase makes a silver delivery AG1-P; "the black one"
said to the agent and not captured is AG1-P (capture failure, Step 3b). The user is not asked to
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

Audit 0 reports that the Visa Core Rules (24 Oct 2026 edition, section 4.1.23.10) make the
cardholder "responsible for any actions taken by an Agentic Payment Provider as part of an Agentic
Transaction as if the Cardholder initiated the Transaction", and that American Express announced
in April 2026 that it "will protect eligible customers from charges related to AI agent error" for
registered agents (press report; terms not reached). Both are cited from the audit, not
re-verified here. ABS Step 4 agrees with the Visa allocation for in-mandate actions. ABS Step 3 is a
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
rules as written in v0.1 and the v0.2 rules above against 524 catalogue scenarios (192 event
types; 494 live disputes). v0.1 as written decided 494 and got 336 right, with 8 gap types, 4
unresolved conflicts and 58 contradiction groups; v0.2 decides 524 of 524 with none. The ground
truth and the v0.2 wording were written in the same exercise, so the result shows that the rules
are complete and consistent against that catalogue's judgments, not that the judgments are right in
law; the catalogue entries marked `general_law`, `uncertain`, `debatable` or `design_proposal` are
the ones to challenge.

### A4.3 Without prejudice to statutory conformity; deviations accepted in advance

Conformity to the offer in Step 1 is conformity to the subjective, contractual requirements. EU
sale-of-goods law adds objective requirements (fitness for normal purpose, normal quality and
durability) and a multi-year liability period with a presumption that a defect shown in the first
year existed at delivery (Directive (EU) 2019/771, Articles 6, 7, 10, 11 and 21 as cited by Audit
0). A Step 1 finding of "conforms" settles the ABS dispute; it never settles a statutory conformity
claim. Every Decision says so.

Under the same directive, a deviation from objective conformity (refurbished, used, lower battery
health) binds a consumer only if specifically informed and expressly and separately accepted.
Whether an agent can give that acceptance is an open legal question. The Mandate field
`accepted_deviations[]` records the user's own advance acceptance with its authentication
reference, so the acceptance is the user's, not the agent's. Its legal effect is listed in A15.1.

### A4.4 Statutory withdrawal right (overlay)

Consumer law applies whatever the dispute decides. For goods sold at a distance to an EU consumer,
the buyer may withdraw within 14 days of delivery without giving a reason, returning the goods at
their own cost unless the merchant agreed otherwise (Directive 2011/83/EU, Article 9, as cited by
Audit 0). The right does not apply to, among others, goods made to the consumer's specification,
sealed goods unsealed after delivery, digital content once started with consent, and accommodation,
transport, car hire and leisure on a specific date (Article 16, as cited). Business purchases have
no withdrawal right. Every Decision states whether the right is available; for AG2 and AG5 the
remedy is `withdrawal` when it is and `deny` when it is not. For AG3, AG4, AG1-M and AG1-P the
remedy is a refund by the liable party and the right is moot.

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
| Agent trace digest | Hash-chain head over mandate, every action with its stated reason and result status, snapshots, cart with `added_by`, authorisation; the full action log stays with the provider | Agent provider | Agent provider; the chain head goes into the rail reference | E2 (log), E3 (chain) |
| Delivery evidence | Contestable records of what arrived (A5.6) | Merchant (shipment part), user or provider (receipt part), carrier where it signs | Merchant; agent provider; carrier | E3 |
| Compared record | The Offer Feed record or signed negotiation record the agent relied on when it chose the merchant, hashed into the chain with the snapshot | Merchant (feed); both agents (negotiation record) | Agent provider | E3 |
| Refusal Record | When the agent did not buy: offers compared, Mandate, stated reason | Agent provider | Agent provider | E2 |

Everything else (the Dispute Case, the Decision, the Finding and the Decision Receipt) is produced
during the dispute from the Package.

**What the Package makes decidable.** In the rule-completeness simulation (author-built catalogue,
not field data), card-dispute evidence alone (E0) decided 86 of 494 live disputes (17.4%): time
limits, non-delivery where the merchant has no carrier proof of handover, and friendly-fraud
non-receipt where it has. The minimum package at E3 decided 494 of 494, 492 determinately and 2 by
escalation to a fact-finder with human review because the records conflicted. E1 adds the
authorisation and the amount, category, merchant, units, expiry and currency breaches; E2 the
log-dependent breaches (step-up, required attributes, scope, approvals, budgets, roles), injection
the agent reports following, and undisclosed incentives; E3 content conformity, merchant-added
lines, feed-versus-snapshot mismatch, false claims, feed signature, Register entry and tampering,
and therefore every Step 4 denial of a not-as-described claim.

### A5.2 Profiles of existing objects, not competitors

Where an existing standard already defines the object, the ABS object is a profile of it: the same
container with the ABS fields required and the ABS hash and signature rules applied.

| ABS record | Existing object it profiles | What the profile adds |
|---|---|---|
| Mandate digest | AP2 v0.2 Checkout and Payment Mandates (SD-JWT verifiable credentials) and Mastercard Verifiable Intent, both in the FIDO Alliance Payments working group (per Audit 0, 28 Apr 2026) | `intent_hash` over the user's own words; the Allowance Policy reference; `accepted_deviations`; the rule that the mandate plus clarifications is "what the buyer asked for" |
| Offer Snapshot | AP2's merchant-signed checkout JWT bound by hash to the Closed Checkout Mandate, and the merchant's Checkout Receipt; UCP and ACP checkout objects | The conformity-critical attribute set with tolerances; the countersignature at acceptance as "the listing"; the rule that a later edit has no evidential value; retention |
| Agent identity on requests | HTTP Message Signatures (RFC 9421); Visa Trusted Agent Protocol and Mastercard Agent Pay registration; IETF Web Bot Auth drafts | Nothing; ABS defers |
| Catalogue | UCP Catalog and ACP Product Feed | The injection-safety profile (A5.7) and the binding conformity attributes |
| Rail reference | Card merchant/additional data where a network allows it; ISO 20022 remittance information or end-to-end identification | The chain head as the anchor |

Where no existing object exists (Approval record, Delivery evidence, Dispute Case, Decision,
Finding, Decision Receipt), ABS defines one.

### A5.3 Common envelope and definitions

Every ABS object is a JSON document with this envelope. `body` is hashed and signed; signatures are
over `hash`; `prev_hash` links the object into the purchase's chain. Unknown fields inside `body`
MUST be rejected.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "urn:abs:schema:0.2:envelope",
  "type": "object",
  "required": ["abs_version", "type", "id", "created_at", "body", "hash", "signatures"],
  "properties": {
    "abs_version": {"const": "0.2"},
    "type": {"enum": ["ParticipationAgreement", "AllowancePolicy", "Mandate", "ApprovalRecord", "Offer", "OfferSnapshot", "PurchaseRecord",
                      "SettlementInstruction", "DeliveryRecord", "DisputeCase", "Decision", "Finding", "DecisionReceipt", "TrustAttestation"]},
    "id": {"type": "string", "pattern": "^urn:abs:[a-z]+:[0-9a-f-]{36}$"},
    "created_at": {"type": "string", "format": "date-time"},
    "body": {"type": "object"},
    "hash": {"$ref": "#/$defs/Hash"},
    "prev_hash": {"$ref": "#/$defs/Hash"},
    "signatures": {"type": "array", "minItems": 1, "items": {"$ref": "#/$defs/Signature"}}
  },
  "$defs": {
    "Hash": {"type": "string", "pattern": "^sha256:[0-9a-f]{64}$"},
    "Signature": {"type": "object", "required": ["role", "party_id", "kid", "alg", "sig", "signed_at"],
      "properties": {"role": {"enum": ["user", "agent_provider", "merchant", "arbiter", "trust_authority", "certifier", "psp"]},
                     "party_id": {"type": "string"}, "kid": {"type": "string"}, "alg": {"enum": ["EdDSA", "ES256"]},
                     "sig": {"type": "string", "description": "JWS compact serialisation, detached payload = hash"},
                     "signed_at": {"type": "string", "format": "date-time"}}},
    "Money": {"type": "object", "required": ["amount", "currency"],
      "properties": {"amount": {"type": "string", "pattern": "^-?[0-9]+(\\.[0-9]{1,4})?$"}, "currency": {"type": "string", "pattern": "^[A-Z]{3}$"}}},
    "UntrustedText": {"type": "object", "required": ["text", "class"],
      "properties": {"text": {"type": "string", "maxLength": 20000}, "class": {"const": "untrusted_text"}, "lang": {"type": "string"}},
      "description": "Free text written by a party. Shown to humans. Never an instruction to an agent. Never binding."},
    "PartyRef": {"type": "object", "required": ["party_id", "role"],
      "properties": {"party_id": {"type": "string"}, "role": {"enum": ["user", "agent_provider", "merchant", "arbiter", "trust_authority", "certifier", "psp"]}, "kid": {"type": "string"}}},
    "ImageRef": {"type": "object", "required": ["url", "sha256"],
      "properties": {"url": {"type": "string", "format": "uri"}, "sha256": {"$ref": "#/$defs/Hash"},
                     "role": {"enum": ["primary", "gallery", "label", "packaging", "defect", "delivery", "return_inspection"]},
                     "c2pa_manifest_hash": {"$ref": "#/$defs/Hash", "description": "when the image carries a C2PA manifest; proves provenance and edits, not truth"}}},
    "Category": {"type": "object", "required": ["vocabulary", "code"],
      "properties": {"vocabulary": {"enum": ["iso18245:mcc", "gs1:gpc", "google:product", "abs:profile", "merchant"]}, "code": {"type": "string"}, "label": {"type": "string"}}}
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
  "$id": "urn:abs:schema:0.2:attribute",
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
`spec_status: non_binding`; agents do not buy it under a default Allowance. An attribute with
`not_verifiable_at_delivery` may be binding, but a conformity claim on it needs evidence beyond the
delivery check and is otherwise `undeterminable`.

### A5.5 Record schemas

**Mandate** (task instruction under an Allowance Policy; the policy's full schema is in Part B3).
Signed by: user through strong authentication, agent provider.

```json
{
  "$id": "urn:abs:schema:0.2:mandate",
  "type": "object",
  "required": ["mandate_id", "allowance_policy_id", "allowance_policy_hash", "user_ref", "agent_provider", "agent_id", "intent_hash",
               "max_total", "max_units", "valid_from", "expires_at", "autonomy_required", "authentication", "rulebook_version", "nonce"],
  "additionalProperties": false,
  "properties": {
    "mandate_id": {"type": "string"},
    "allowance_policy_id": {"type": "string"}, "allowance_policy_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"},
    "user_ref": {"type": "string", "description": "pseudonymous"},
    "agent_provider": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/PartyRef"}, "agent_id": {"type": "string"},
    "intent_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash", "description": "sha256 of the user's instruction text; explicit terms in it count as mandate terms"},
    "intent_summary": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/UntrustedText"},
    "proposed_by": {"enum": ["agent", "user"], "default": "agent", "description": "the agent proposes the Mandate from the conversation; the user confirms"},
    "conversation_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash", "description": "hash of the conversation record the Mandate was proposed from; kept by the agent provider; a stated requirement found there and not captured is a capture failure (A4.1 Step 3b)"},
    "template_profile": {"type": "object", "properties": {"id": {"type": "string"}, "version": {"type": "string"}, "prompted_attributes": {"type": "array", "items": {"type": "string"}}, "left_open": {"type": "array", "items": {"type": "string"}}},
                         "description": "the category template used to prompt for conformity-critical attributes, and which were left open by the user"},
    "user_confirmation": {"type": "object", "required": ["confirmed_at", "shown_terms_hash"], "properties": {"confirmed_at": {"type": "string", "format": "date-time"}, "shown_terms_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash", "description": "hash of the plain-language terms shown at the confirmation tap"}}},
    "max_total": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}, "max_per_purchase": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"},
    "categories": {"type": "array", "items": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Category"}},
    "merchant_allowlist": {"type": "array", "items": {"type": "string"}}, "merchant_denylist": {"type": "array", "items": {"type": "string"}},
    "min_merchant_qualification": {"enum": ["probation", "qualified", "established"], "default": "qualified"},
    "max_units": {"type": "integer", "minimum": 1}, "max_lines": {"type": "integer", "minimum": 1}, "max_purchases": {"type": "integer", "minimum": 1, "default": 1},
    "condition_allowed": {"type": "array", "items": {"enum": ["new", "refurbished", "used_like_new", "used_good", "used_acceptable"]}},
    "delivery_countries": {"type": "array", "items": {"type": "string", "pattern": "^[A-Z]{2}$"}},
    "delivery_address_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"},
    "item_requirements": {"type": "array", "items": {"$ref": "urn:abs:schema:0.2:attribute"},
                          "description": "captured, machine-readable requirements for the item (model, variant, capacity, size, colour, region, condition, package contents, dates, reference, deadline); each is an explicit mandate term, and a purchase that misses one is AG1-P"},
    "scope_only_named_item": {"type": "boolean", "default": true, "description": "explicit term: the agent buys only the item named; adding another item is AG1-P"},
    "ask_on_ambiguity": {"type": "boolean", "default": true, "description": "an explicit term: a guess where this is true is agent fault (AG1-P)"},
    "currency": {"type": "object", "properties": {"pay_in": {"type": "string", "pattern": "^[A-Z]{3}$"}, "fx_tolerance_pct": {"type": "number", "minimum": 0}}, "description": "explicit term: pay-in currency and the conversion tolerance the agent may accept"},
    "approval_prompt_must_show": {"type": "array", "items": {"enum": ["item", "amount", "merchant", "delivery_date", "total_incl_tax"]}, "description": "explicit term: an approval obtained with a prompt that omits these is not an approval"},
    "recurring": {"type": "object", "properties": {"period": {"enum": ["weekly", "monthly", "quarterly", "yearly"]}, "max_charges": {"type": "integer", "minimum": 1}, "max_per_charge": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}}, "description": "explicit terms for recurring purchases; a charge beyond max_charges or after expiry is AG0 (b) against the merchant"},
    "business_terms": {"type": "object", "properties": {"purchase_order_ref": {"type": "string"}, "buyer_vat_id": {"type": "string"}, "einvoice_format": {"type": "string"}, "payment_terms": {"type": "string", "description": "e.g. net30; prepaying where terms were mandated is a no-loss breach"},
                       "procurement_threshold": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}, "framework_allowlist": {"type": "array", "items": {"type": "string"}}}, "description": "explicit terms for business and public buyers"},
    "incentive_disclosure": {"type": "array", "items": {"type": "object", "properties": {"merchant_id": {"type": "string"}, "kind": {"type": "string"}, "disclosed_at": {"type": "string", "format": "date-time"}}}, "description": "payments the agent provider receives from merchants; an undisclosed one that steered the choice is ABS-X2"},
    "policy_version": {"type": "object", "properties": {"version": {"type": "string"}, "acknowledged_by_agent_at": {"type": "string", "format": "date-time"}}, "description": "a tightened policy binds from the agent's acknowledgement"},
    "accepted_deviations": {"type": "array", "items": {"type": "object", "required": ["attribute", "accepted_value", "authentication_reference"],
                            "properties": {"attribute": {"type": "string"}, "accepted_value": {"type": ["string", "number", "boolean"]}, "authentication_reference": {"type": "string"}}},
                            "description": "the user's own advance acceptance of deviations from objective conformity (A4.3); legal effect open"},
    "autonomy_required": {"enum": ["autonomous", "notify_and_hold", "approval_required"], "description": "the level the Allowance Policy requires for this task; buying at a lower level is AG1-P"},
    "valid_from": {"type": "string", "format": "date-time"}, "expires_at": {"type": "string", "format": "date-time"},
    "payment_instruments": {"type": "array", "items": {"type": "object", "required": ["rail", "instrument_ref"],
                            "properties": {"rail": {"enum": ["card", "a2a_instant", "a2a_batch", "wallet", "stablecoin", "other"]}, "instrument_ref": {"type": "string", "description": "token or account reference; never a PAN"}}}},
    "authentication": {"type": "object", "required": ["method", "performed_at", "reference", "assurance"],
                       "properties": {"method": {"enum": ["sca_app", "sca_3ds", "passkey", "bank_login", "other"]}, "performed_at": {"type": "string", "format": "date-time"},
                                      "reference": {"type": "string"}, "assurance": {"enum": ["psd2_sca", "nist_aal2", "nist_aal3", "unknown"]},
                                      "dynamic_link": {"type": "object", "properties": {"amount": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}, "payee_scope": {"type": "string"}}}}},
    "rulebook_version": {"type": "string"}, "rules_shown_at": {"type": "string", "format": "date-time"},
    "nonce": {"type": "string", "minLength": 16}
  }
}
```

**Approval Record.** Produced when the Allowance routes a purchase to notify-and-hold or approval.
Signed by: agent provider, carrying the approver's authentication reference.

```json
{
  "$id": "urn:abs:schema:0.2:approval-record",
  "type": "object",
  "required": ["approval_id", "mandate_id", "cart_hash", "level_applied", "matched_rule_id", "outcome"],
  "additionalProperties": false,
  "properties": {
    "approval_id": {"type": "string"}, "mandate_id": {"type": "string"},
    "cart_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash", "description": "hash of the exact cart and totals shown"},
    "level_applied": {"enum": ["notify_and_hold", "approval_required"]}, "matched_rule_id": {"type": "string"},
    "routing_receipt_id": {"type": "string", "description": "Decision Receipt of the allowance ruleset that chose the level"},
    "notification": {"type": "object", "properties": {"sent_at": {"type": "string", "format": "date-time"}, "channel": {"type": "string"}}},
    "hold": {"type": "object", "properties": {"hold_until": {"type": "string", "format": "date-time"}, "cancelled": {"type": "boolean"}, "cancelled_at": {"type": "string", "format": "date-time"}}},
    "approver": {"type": "object", "properties": {"type": {"enum": ["user", "delegate"]}, "ref": {"type": "string"}, "role": {"type": "string"}}},
    "authentication": {"type": "object", "properties": {"method": {"type": "string"}, "reference": {"type": "string"}, "assurance": {"type": "string"}, "performed_at": {"type": "string", "format": "date-time"}}},
    "shown_summary_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash", "description": "hash of the plain-language summary the approver saw: items, merchant, total incl. tax, signals"},
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
  "$id": "urn:abs:schema:0.2:offer-snapshot",
  "type": "object",
  "required": ["snapshot_id", "when", "captured_at", "mandate_id", "agent_id", "offer_hash", "offer_signature", "merchant", "offer_id",
               "conformity_spec", "spec_status", "price", "price_includes_tax", "mandatory_fees", "delivery_option", "returns_policy", "condition", "images", "source"],
  "additionalProperties": false,
  "properties": {
    "snapshot_id": {"type": "string"}, "when": {"enum": ["view", "checkout"]}, "captured_at": {"type": "string", "format": "date-time"},
    "mandate_id": {"type": "string"}, "agent_id": {"type": "string"},
    "merchant": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/PartyRef"}, "offer_id": {"type": "string"},
    "gtin": {"type": "string", "pattern": "^[0-9]{8,14}$"}, "sku": {"type": "string"},
    "offer_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash", "description": "hash of the merchant-signed Offer (UCP/ACP/AP2 object or ABS Offer); must verify against the merchant key"},
    "offer_signature": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Signature"},
    "external_object": {"type": "object", "properties": {"protocol": {"enum": ["ap2", "ucp", "acp", "abs"]}, "object_ref": {"type": "string"}, "object_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}},
                        "description": "the checkout object of the protocol used (e.g. the AP2 merchant-signed checkout JWT), when ABS runs as a profile"},
    "conformity_spec": {"type": "array", "minItems": 1, "items": {"$ref": "urn:abs:schema:0.2:attribute"}, "description": "binding attributes only"},
    "spec_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}, "spec_status": {"enum": ["binding", "non_binding"]},
    "profile": {"type": "object", "properties": {"id": {"type": "string"}, "version": {"type": "string"}}},
    "condition": {"enum": ["new", "refurbished", "used_like_new", "used_good", "used_acceptable"]},
    "package_contents": {"type": "array", "items": {"type": "object", "required": ["item", "qty"], "properties": {"item": {"type": "string", "maxLength": 100}, "qty": {"type": "integer", "minimum": 1}}}},
    "price": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}, "price_includes_tax": {"type": "boolean"},
    "mandatory_fees": {"type": "array", "items": {"type": "object", "required": ["name", "amount"], "properties": {"name": {"type": "string", "maxLength": 64}, "amount": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}}}},
    "reference_price": {"type": "object", "properties": {"price": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}, "basis": {"enum": ["rrp", "own_previous_30_days", "none"]}}},
    "delivery_option": {"type": "object", "required": ["method", "cost", "estimated_days_max"],
                        "properties": {"method": {"enum": ["standard", "express", "pickup", "digital", "service_date"]}, "cost": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"},
                                       "estimated_days_min": {"type": "integer"}, "estimated_days_max": {"type": "integer"}, "service_date": {"type": "string", "format": "date"}, "destination": {"type": "string"}}},
    "returns_policy": {"type": "object", "required": ["window_days", "who_pays_return"],
                       "properties": {"window_days": {"type": "integer"}, "who_pays_return": {"enum": ["merchant", "buyer", "merchant_if_non_conforming"]},
                                      "conditions": {"type": "array", "items": {"type": "string"}}, "statutory_withdrawal_applies": {"type": "boolean"}}},
    "warranty_months": {"type": "integer"},
    "tax": {"type": "object", "properties": {"rate_pct": {"type": "number"}, "scheme": {"type": "string"}, "seller_vat_id": {"type": "string"}}},
    "cross_border": {"type": "object", "properties": {"ships_from_country": {"type": "string"}, "import_charges_included": {"type": "boolean"}, "estimated_import_charges": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}}},
    "images": {"type": "array", "minItems": 1, "items": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/ImageRef"}},
    "images_verified": {"type": "boolean"},
    "marketing_text_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash", "description": "hash of title and description as shown; kept for AG4 evidence, never binding"},
    "compared_record": {"type": "object", "properties": {"kind": {"enum": ["offer_feed_record", "negotiation_record", "seller_agent_statement"]}, "hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"},
                        "price": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}, "delivery_cost": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}, "fees_total": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}},
                        "description": "the record the agent relied on when it chose this merchant; checkout terms worse than it are AG1-M (extended)"},
    "negotiation_record": {"type": "object", "properties": {"hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}, "buyer_agent_signature": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Signature"}, "seller_agent_signature": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Signature"}},
                           "description": "agent-to-agent: terms bind only when written here and signed by both agents; seller-agent statements outside it are merchant content for Step 2"},
    "idempotency_key": {"type": "string", "description": "derived from mandate_id and the cart hash; a duplicate capture against one key is the merchant's, a duplicate order without a key is the agent provider's"},
    "source": {"enum": ["feed", "protocol_object", "page"]},
    "page_render_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"},
    "merchant_order_acceptance": {"type": "object", "properties": {"order_id": {"type": "string"}, "accepted_at": {"type": "string", "format": "date-time"}}}
  }
}
```

**Purchase Record** (trace digest). Signed by: agent provider; merchant (order acceptance).

```json
{
  "$id": "urn:abs:schema:0.2:purchase-record",
  "type": "object",
  "required": ["purchase_id", "mandate_id", "mandate_hash", "agent_id", "merchant", "cart", "totals", "controls", "trace_digest", "rulebook_version"],
  "additionalProperties": false,
  "properties": {
    "purchase_id": {"type": "string"}, "mandate_id": {"type": "string"}, "mandate_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"},
    "agent_id": {"type": "string"}, "merchant": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/PartyRef"}, "merchant_order_id": {"type": "string"},
    "idempotency_key": {"type": "string"},
    "cart": {"type": "array", "minItems": 1, "items": {"type": "object", "required": ["line", "snapshot_id", "offer_id", "qty", "unit_price", "added_by", "responding_party"],
             "properties": {"line": {"type": "integer"}, "snapshot_id": {"type": "string"}, "offer_id": {"type": "string"}, "qty": {"type": "integer", "minimum": 1},
                            "unit_price": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}, "added_by": {"enum": ["agent", "merchant", "user"]},
                            "responding_party": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/PartyRef", "description": "who answers for this line: the seller for its goods and conduct; the platform for its own feed, fees, merges and hosting duties (marketplaces)"},
                            "agent_reason": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/UntrustedText"}}}},
    "totals": {"type": "object", "required": ["items", "delivery", "fees", "tax", "total"],
               "properties": {"items": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}, "delivery": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"},
                              "fees": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}, "tax": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}, "total": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}}},
    "tax_detail": {"type": "object", "description": "buyer type, VAT ids, per-line VAT, import charges, e-invoice reference (Part B3)"},
    "clarifications": {"type": "array", "items": {"type": "object", "required": ["asked_at", "question_hash", "answer_hash"],
                       "properties": {"asked_at": {"type": "string", "format": "date-time"}, "question_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"},
                                      "answer_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}, "user_auth_reference": {"type": "string"}}}},
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
                     "properties": {"chain_head": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}, "event_count": {"type": "integer"},
                                    "first_event_at": {"type": "string", "format": "date-time"}, "last_event_at": {"type": "string", "format": "date-time"}, "log_location_ref": {"type": "string"}}},
    "agent_summary_to_user_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"},
    "rulebook_version": {"type": "string"}
  }
}
```

**Delivery Record** (contestable evidence). Signed by: merchant (shipment part); user or agent
provider (receipt part).

```json
{
  "$id": "urn:abs:schema:0.2:delivery-record",
  "type": "object",
  "required": ["delivery_id", "purchase_id", "shipment"],
  "additionalProperties": false,
  "properties": {
    "delivery_id": {"type": "string"}, "purchase_id": {"type": "string"},
    "shipment": {"type": "object", "required": ["lines", "shipped_at", "delivery_option"],
      "properties": {"lines": {"type": "array", "items": {"type": "object", "required": ["line", "qty_shipped"],
                     "properties": {"line": {"type": "integer"}, "qty_shipped": {"type": "integer"}, "serials": {"type": "array", "items": {"type": "string"}}}}},
                     "shipped_at": {"type": "string", "format": "date-time"}, "delivery_option": {"type": "integer"}, "carrier": {"type": "string"}, "tracking_ref": {"type": "string"},
                     "packing_record": {"type": "object", "properties": {"images": {"type": "array", "items": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/ImageRef"}},
                                        "video_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}, "weight_g": {"type": "integer"}, "recorded_at": {"type": "string", "format": "date-time"}},
                                        "description": "self-serving; weighed, not presumed"},
                     "carrier_proof": {"type": "object", "properties": {"status": {"type": "string"}, "delivered_at": {"type": "string", "format": "date-time"},
                                       "signature_or_code": {"enum": ["signature", "pickup_code", "photo", "none"]}, "parcel_weight_g": {"type": "integer"},
                                       "evidence_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}}, "description": "the carrier does not inspect contents"},
                     "digital_delivery_log": {"type": "object", "properties": {"delivered_at": {"type": "string", "format": "date-time"}, "activation_or_download_ref": {"type": "string"}, "log_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}}},
                     "service_acceptance": {"type": "object", "properties": {"performed_at": {"type": "string", "format": "date-time"}, "accepted_by": {"type": "string"}, "acceptance_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}}}}},
    "receipt": {"type": "object", "required": ["received_at", "conformity"],
      "properties": {"received_at": {"type": "string", "format": "date-time"},
                     "conformity": {"enum": ["conforms", "non_conforming", "not_received", "not_checked"]}, "checked_by": {"enum": ["user", "agent", "both"]},
                     "spec_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}, "attributes_checked": {"type": "integer"}, "attributes_undeterminable": {"type": "integer"},
                     "buyer_evidence": {"type": "array", "items": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/ImageRef"}, "description": "photos or video with metadata; can be manipulated"},
                     "serial_lookup": {"type": "object", "properties": {"registry": {"type": "string"}, "result": {"enum": ["match", "no_match", "not_available"]}, "checked_at": {"type": "string", "format": "date-time"}}},
                     "mismatches": {"type": "array", "items": {"type": "object", "required": ["line", "field", "offered", "delivered", "verification_method"],
                                    "properties": {"line": {"type": "integer"}, "field": {"type": "string"}, "offered": {"type": ["string", "number", "boolean"]}, "delivered": {"type": ["string", "number", "boolean"]},
                                                   "unit": {"type": "string"}, "tolerance_applied": {"type": "object"}, "verification_method": {"type": "string"},
                                                   "evidence": {"type": "array", "items": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/ImageRef"}}}}},
                     "notes": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/UntrustedText"}}},
    "return_inspection": {"type": "object", "properties": {"inspected_at": {"type": "string", "format": "date-time"}, "result": {"enum": ["as_offered", "non_conforming", "damaged", "not_returned"]},
                          "evidence": {"type": "array", "items": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/ImageRef"}}}, "description": "signed by the merchant; weighed against the buyer evidence"}
  }
}
```

**Dispute Case.** Signed by: filer; merchant (response).

```json
{
  "$id": "urn:abs:schema:0.2:dispute-case",
  "type": "object",
  "required": ["case_id", "purchase_id", "purchase_hash", "filed_by", "filed_at", "reason_code", "disputed_lines", "disputed_amount", "remedy_requested", "claim",
               "evidence_level", "evidence_refs", "timeline", "status", "rulebook_version", "rail"],
  "additionalProperties": false,
  "properties": {
    "case_id": {"type": "string"}, "purchase_id": {"type": "string"}, "purchase_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"},
    "rail": {"enum": ["card", "a2a_instant", "a2a_batch", "wallet", "stablecoin", "other"]},
    "filed_by": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/PartyRef"}, "user_consent_reference": {"type": "string"},
    "filed_at": {"type": "string", "format": "date-time"},
    "reason_code": {"enum": ["AG0", "AG1-M", "AG1-P", "AG2", "AG3", "AG4", "AG5"]},
    "legacy_category": {"enum": ["unauthorised", "not_received", "not_as_described", "processing_error", "authorised_but_wrong", "none"]},
    "buyer_type": {"enum": ["consumer", "business"]}, "goods_category": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Category"},
    "withdrawal_right": {"type": "object", "properties": {"applies": {"type": "boolean"}, "expires_at": {"type": "string", "format": "date-time"}, "exception": {"type": "string"}}},
    "disputed_lines": {"type": "array", "minItems": 1, "items": {"type": "integer"}}, "disputed_amount": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"},
    "remedy_requested": {"enum": ["full_refund", "return_and_refund", "partial_refund", "replacement", "withdrawal", "deny"]},
    "claim": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/UntrustedText"},
    "evidence_level": {"enum": ["E0", "E1", "E2", "E3"]},
    "evidence_refs": {"type": "array", "items": {"type": "object", "required": ["type", "hash"],
                      "properties": {"type": {"enum": ["mandate", "allowance_policy", "approval_record", "offer_snapshot", "purchase_record", "settlement_instruction", "delivery_record", "action_log", "clarification", "image", "carrier_record", "serial_lookup", "digital_log", "return_inspection", "other"]},
                                     "hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}, "held_by": {"enum": ["user", "agent_provider", "merchant", "psp", "carrier"]}}}},
    "merchant_response": {"type": "object", "properties": {"responded_at": {"type": "string", "format": "date-time"},
                          "offer": {"enum": ["full_refund", "return_and_refund", "partial_refund", "replacement", "deny"]}, "partial_amount": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"},
                          "text": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/UntrustedText"},
                          "attachments": {"type": "array", "items": {"type": "object", "required": ["type", "hash"],
                                          "properties": {"type": {"enum": ["listing_page", "photo", "packing_record", "carrier_record", "serial_record", "return_inspection", "other"]},
                                                         "hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}, "matches_checkout_snapshot": {"type": "boolean", "description": "set by the verifier, not the merchant"}}}}}},
    "buyer_reply_to_offer": {"enum": ["accept", "reject", "none"]},
    "timeline": {"type": "object", "required": ["response_due", "escalation_due"],
                 "properties": {"response_due": {"type": "string", "format": "date-time"}, "escalation_due": {"type": "string", "format": "date-time"},
                                "escalated_at": {"type": "string", "format": "date-time"}, "decision_due": {"type": "string", "format": "date-time"}}},
    "human_review_requested": {"type": "object", "properties": {"by": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/PartyRef"}, "at": {"type": "string", "format": "date-time"}}},
    "tier": {"enum": [1, 2]}, "status": {"enum": ["filed", "responded", "settled", "escalated", "under_human_review", "decided", "appealed", "withdrawn", "closed"]},
    "rulebook_version": {"type": "string"}
  }
}
```

**Decision.** Signed by: arbiter (tier 2); user side and merchant (tier 1 settlement).

```json
{
  "$id": "urn:abs:schema:0.2:decision",
  "type": "object",
  "required": ["decision_id", "case_id", "tier", "decided_at", "conformity_finding", "reason_code", "liable_party", "remedy", "withdrawal_right_available",
               "amounts", "evidence_integrity", "rationale", "plain_language_explanation", "human_review", "binding_effect", "receipt_id"],
  "additionalProperties": false,
  "properties": {
    "decision_id": {"type": "string"}, "case_id": {"type": "string"}, "tier": {"enum": [1, 2]},
    "arbiter": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/PartyRef"}, "decided_at": {"type": "string", "format": "date-time"},
    "conformity_finding": {"enum": ["conforms", "non_conforming", "not_received", "undeterminable", "not_applicable"]},
    "reason_code": {"enum": ["AG0", "AG1-M", "AG1-P", "AG2", "AG3", "AG4", "AG5"]},
    "liable_party": {"enum": ["merchant", "agent_provider", "psp", "buyer", "rail_process"]},
    "remedy": {"enum": ["refund", "return_and_refund", "partial_refund", "replacement", "withdrawal", "deny"]},
    "withdrawal_right_available": {"type": "boolean"},
    "amounts": {"type": "object", "required": ["to_buyer"],
                "properties": {"to_buyer": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}, "from_merchant": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"},
                               "from_agent_provider": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}, "from_psp": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"},
                               "return_shipping_paid_by": {"enum": ["merchant", "agent_provider", "buyer", "none"]}}},
    "goods_return": {"type": "boolean"}, "return_deadline": {"type": "string", "format": "date-time"},
    "evidence_integrity": {"type": "object", "required": ["chain_verified"],
                           "properties": {"chain_verified": {"enum": ["valid", "broken", "absent"]}, "anchor_matches_rail_reference": {"type": "boolean"},
                                          "mandate_signature_valid": {"type": "boolean"}, "merchant_attachments_match_checkout_snapshot": {"type": "boolean"},
                                          "delivery_evidence_weighed": {"type": "array", "items": {"type": "string"}}, "problems": {"type": "array", "items": {"type": "string"}}}},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    "rationale": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/UntrustedText"},
    "plain_language_explanation": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/UntrustedText", "description": "written for the person affected: what was decided, from which evidence, under which rule, and how to ask for a human review or appeal"},
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
  "$id": "urn:abs:schema:0.2:refusal-record",
  "type": "object",
  "required": ["refusal_id", "mandate_id", "refused_at", "offers_compared", "reason_code"],
  "additionalProperties": false,
  "properties": {
    "refusal_id": {"type": "string"}, "mandate_id": {"type": "string"}, "refused_at": {"type": "string", "format": "date-time"},
    "offers_compared": {"type": "array", "items": {"type": "object", "properties": {"snapshot_id": {"type": "string"}, "offer_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}, "merchant": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/PartyRef"}}}},
    "reason_code": {"enum": ["no_conforming_offer", "over_limit", "merchant_not_qualified", "non_binding_offer", "risk_signal", "user_declined", "approval_declined", "approval_expired", "ambiguity_unresolved", "other"]},
    "reason": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/UntrustedText"},
    "classification": {"enum": ["true_block", "false_refusal", "unclassified"], "description": "set by the programme scoreboard; a refusal of a conforming, qualified, in-mandate offer is a false refusal; no liability either way"}
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

- Records in a valid chain whose anchor matches the rail reference (policy, mandate, approval,
  action log, snapshots, cart, offer, compared record) are presumed accurate.
- A merchant statement about its offer that does not match the countersigned checkout snapshot is
  disregarded. Post-purchase edits do not count.
- A broken chain counts against the party that kept the records.
- A party that was required to keep a record (the agent provider for the Mandate and action log;
  the merchant for the Offer Snapshot and packing record) and cannot produce it when asked has the
  question that record would answer decided against it (ABS-E1).
- If the merchant does not respond within the response window and produces no delivery evidence,
  the buyer's account of facts within its own knowledge is accepted (ABS-D1).
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
- Hash: SHA-256 over RFC 8785 canonical JSON; images hashed as bytes.
- Chain: each event has `seq`, `type`, `data_sha256`, `prev`, `hash = sha256(prev || JCS(meta))`,
  from the Mandate to the Settlement Instruction. The head is the anchor; its first 16 hex
  characters go into the rail reference where the rail has a field (A6.3). Verification recomputes
  every content hash and link.
- Replay: `nonce` in the Mandate; `purchase_hash` plus `instruction_seq` single use at the PSP;
  order acceptance binds `merchant_order_id` to checkout snapshot ids; a snapshot captured after
  the offer's `valid_until` is a feed mismatch and a step-up signal.
- Users sign with a key in their bank app, wallet or passkey. Where the user has no key, the agent
  provider MAY sign on the user's behalf after strong authentication, MUST record the
  authentication reference and `assurance`, and accepts liability for the binding. Audit 0 notes
  that a mandate set up without the payer's PSP is not itself an SCA event under EU rules (EBA Q&A
  2019_4664, as cited); "mandate with SCA" means a PSP performed it.

### A5.9 Data minimisation, retention, transparency

- The Package carries `user_ref`, not a name; `delivery_address_hash`, not an address;
  `intent_hash`, not the intent. Fulfilment data goes to the merchant through its own channel.
- Intent text, full action log and image bytes stay with the agent provider and are disclosed to
  the Decision Center and the counterparty only in a case, at the level offered.
- Retention: the parties keep the Evidence Package and Dispute Case records until the decision and
  appeal window close plus the statutory limitation period, and in any case at least 13 months
  after `delivered_at`; erasure requests are deferred for that period; access requests are served
  with the evidence bundle minus third-party data; hashes MAY be kept longer. National accounting
  rules are outside ABS.
- No card data enters the agent context: agents pay with network tokens or mandate-bound
  credentials only; a merchant checkout that requests card data from an agent breaches its
  Participation Agreement.
- Before a purchase the buyer is shown: the rulebook summary (what can be disputed, how, within
  what time, who decides, the four steps in one sentence each); the mandate as enforced; the
  offer's binding attributes, total including tax and fees, delivery and returns; the provider's
  Step 3 cap if any; what evidence is kept and for how long; who the arbiter is; that statutory
  rights are unaffected; that an AI agent is acting and which provider operates it. The merchant
  is shown that the buyer is an agent, the provider and level, the rulebook version, the snapshots
  it is asked to countersign, and that a step-up or monitor may still decline.

---

## A6. Settlement mapping onto existing card and ISO 20022 flows

### A6.1 Principle

ABS never moves money. A Decision becomes a Settlement Instruction; the instruction names an
existing rail mechanism. On card rails the mechanism is the refund, the chargeback lifecycle
(chargeback, representment, pre-arbitration, arbitration) and the acquirer's reserve; on
account-to-account rails it is a new credit transfer, the scheme's recall or return message where
one exists, and the PSP's payout hold. The Participation Agreement's collection right (direct debit
mandate, reserve, guarantee or netting, operated by a licensed PSP) backs amounts a participant
owes and does not pay.

Four rules make settlement complete:

- **Every rail family has an execution.** Card: merchant refund, then chargeback, representment and
  pre-arbitration as the backstop. Wallet: operator ledger reversal. A2A push (SEPA credit transfer
  and instant, Faster Payments, UPI, Pix, open-banking payment initiation): a new credit transfer by
  the liable party (pain.001 to pacs.008); a recall (camt.056) only where the rail allows it.
  Buy-now-pay-later: refund through the provider, which reduces the loan and returns paid
  instalments. Marketplace: the platform reverses the held split. Stored value: re-credit.
  Stablecoin: on-chain return transfer. Public authority: the authority's own refund process.
- **Payout hold and guarantee.** ABS holds no funds. For merchants in probation (first 90 days or
  below the trust threshold) and for prepaid orders with delivery more than 14 days out, the
  merchant's licensed PSP or acquirer holds the payout until the delivery evidence confirms
  delivery plus a 7-day inspection window; a rolling reserve applies to all merchants on
  irrevocable rails. A programme guarantee, funded by programme fees and held by a licensed entity,
  covers a Decision that neither the liable party nor the held funds can pay; it also pays where a
  forged Register entry passed a correct verification (ABS-P2).
- **Single track.** A buyer who opens a Dispute Case assigns to the programme any rail dispute on
  the same payment; a chargeback filed in parallel is reconciled against the Decision so the buyer
  is made whole once; an ABS Decision is filed as evidence in any later rail dispute. Chargebacks
  remain the backstop and the buyer's right to them is untouched.
- **Enforcement.** A Settlement Instruction unpaid after 10 days is debited from the merchant's
  reserve or by its PSP under the Participation Agreement; failing that, the merchant is suspended
  from the Register and the programme guarantee pays. Where the liable party cannot pay and the rail
  cannot reverse, the instruction is executed from the payout hold, the reserve or the guarantee.

The honest residual: in the simulation, 22 of 524 instructions could not be executed against the
liable party because the merchant was gone on an irrevocable rail with no hold; the guarantee is
the fallback for those, and on UK Faster Payments the APP reimbursement regime may apply to the
scam subset (conditions and caps per `LANDSCAPE.md`).

### A6.2 Settlement Instruction

Rail-agnostic body, one rail binding. Single use: `purchase_hash` plus `instruction_seq`. Signed
by: agent provider or its PSP; PSP appends the rail result.

```json
{
  "$id": "urn:abs:schema:0.2:settlement-instruction",
  "type": "object",
  "required": ["settlement_id", "purchase_id", "purchase_hash", "instruction_seq", "direction", "amount", "payer", "payee", "rail", "abs_binding", "timing"],
  "additionalProperties": false,
  "properties": {
    "settlement_id": {"type": "string"}, "purchase_id": {"type": "string"}, "purchase_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"},
    "instruction_seq": {"type": "integer", "minimum": 1},
    "direction": {"enum": ["pay", "refund", "reverse", "collect", "payout_release", "payout_return"]},
    "decision_id": {"type": "string", "description": "required for refund after decision, reverse, collect, payout_return"},
    "amount": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"},
    "payer": {"type": "object", "required": ["party_role", "instrument_ref"], "properties": {"party_role": {"enum": ["user", "merchant", "agent_provider", "psp", "arbiter"]}, "instrument_ref": {"type": "string", "description": "token or account reference; never a PAN or full IBAN in agent context"}}},
    "payee": {"type": "object", "required": ["party_role", "account_ref"], "properties": {"party_role": {"enum": ["user", "merchant", "agent_provider", "psp", "arbiter"]}, "account_ref": {"type": "string"}}},
    "rail": {"type": "object", "required": ["type"], "properties": {"type": {"enum": ["card", "a2a_instant", "a2a_batch", "wallet", "stablecoin", "other"]}, "network": {"type": "string"}, "scheme_reference": {"type": "string"}}},
    "timing": {"type": "object", "required": ["mode"],
               "properties": {"mode": {"enum": ["immediate", "payout_hold_until_delivery", "rolling_reserve"]},
                              "held_by": {"enum": ["acquirer", "merchant_psp", "wallet_provider", "custodian"], "description": "a licensed entity; ABS holds nothing"},
                              "release_condition": {"enum": ["delivery_confirmed", "conformity_window_elapsed", "decision"]},
                              "reserve_pct": {"type": "number"}, "reserve_days": {"type": "integer"}}},
    "abs_binding": {"type": "object", "required": ["reference_field", "reference_value"],
                    "properties": {"reference_field": {"type": "string", "description": "the rail field that carries the ABS reference"},
                                   "reference_value": {"type": "string", "maxLength": 140, "description": "ABS:<purchase_id>:<first 16 hex of chain_head>"},
                                   "full_anchor": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}, "agent_indicator": {"type": "boolean"}}},
    "card_binding": {"type": "object", "properties": {"network_token_ref": {"type": "string"}, "agent_token_ref": {"type": "string"}, "authentication_ref": {"type": "string", "description": "EMV 3-D Secure or equivalent transaction reference"},
                     "authorisation_code": {"type": "string"}, "retrieval_reference": {"type": "string"},
                     "dispute_stage": {"enum": ["none", "refund", "chargeback", "representment", "pre_arbitration", "arbitration"]}, "dispute_category": {"enum": ["fraud", "authorisation", "processing_error", "consumer_dispute"]}}},
    "a2a_binding": {"type": "object", "properties": {"end_to_end_id": {"type": "string"}, "transaction_id": {"type": "string"},
                    "remittance_information": {"type": "string", "maxLength": 140}, "structured_reference": {"type": "string", "description": "ISO 11649 creditor reference where used"},
                    "payee_name_check": {"enum": ["match", "close_match", "no_match", "not_performed"]},
                    "message": {"enum": ["pacs.008", "pacs.004", "camt.056", "camt.029", "camt.027", "camt.087", "other"], "description": "the ISO 20022 message that carried or will carry this instruction; applicability per rail in A6.3"}}},
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
| Pay | Authorisation and capture with an agent-capable network token and the authentication reference; ABS reference in a merchant or additional data field where the network allows it | Customer credit transfer (pacs.008 family) with the ABS reference in remittance information or end-to-end id; payee name check where the scheme offers it | Transfer with memo |
| Payout hold on an unproven merchant (Part B1) | Acquirer delayed funding or reserve, as acquirers do today | The merchant's PSP holds the credited funds under its own terms until the release condition; the ABS instruction states the condition | Hold on seller balance; custodial hold |
| Refund by merchant (AG3, AG4, AG1-M; tier 1 settlement) | Merchant-initiated refund to the original credential | New credit transfer from merchant to buyer (pacs.008) with the ABS case id; the obligation comes from participation | Reversal from balance |
| Reversal against a merchant that does not pay | Chargeback in the fitting category (consumer dispute: not received, not as described; processing error: incorrect amount), representment, pre-arbitration, arbitration; the ABS Decision and Receipt are the evidence | Payment return (pacs.004) or recall request (camt.056) and resolution (camt.029) where the scheme supports them for this case and within its time limits; otherwise collection right | Collection right |
| Refund by agent provider or PSP (AG1-P) | Provider credits the buyer's card account (original credit transaction or refund API via its PSP) | Provider pushes a credit transfer to the buyer | Provider transfer |
| Withdrawal (AG2, AG5 with the right available) | Merchant refund after receiving the goods | Merchant credit transfer after receiving the goods | Reversal from balance |
| Collect a decided amount a participant did not pay | Direct debit under the collection mandate; acquirer reserve; netting | Direct debit under the collection mandate; reserve | Balance debit |
| Dispute messages between PSPs | Scheme dispute platform | Claim non-receipt and request-to-modify messages (camt.027, camt.087) where a scheme uses them; the ABS case id travels in the case identification | Not applicable |

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
  "$id": "urn:abs:schema:0.2:participation-agreement",
  "type": "object",
  "required": ["participant", "legal_entity", "rulebook_version", "rulebook_hash", "accepted_at", "conformance_level", "keys", "dispute_contact", "settlement", "collection_right", "binding_effect"],
  "properties": {
    "participant": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/PartyRef"},
    "legal_entity": {"type": "object", "required": ["name", "registration_number", "country"],
                     "properties": {"name": {"type": "string"}, "registration_number": {"type": "string"}, "lei": {"type": "string", "description": "ISO 17442 legal entity identifier where held"},
                                    "country": {"type": "string", "pattern": "^[A-Z]{2}$"}, "vat_number": {"type": "string"}, "address": {"type": "string"}}},
    "rulebook_version": {"type": "string"}, "rulebook_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"},
    "accepted_at": {"type": "string", "format": "date-time"}, "valid_until": {"type": "string", "format": "date-time"},
    "conformance_level": {"enum": ["ABS-Basic", "ABS-Full"]},
    "certification": {"type": "object", "properties": {"certifier": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/PartyRef"}, "attestation_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}, "valid_until": {"type": "string", "format": "date-time"}}},
    "keys": {"type": "array", "minItems": 1, "items": {"type": "object", "required": ["kid", "alg", "public_key", "valid_from"],
             "properties": {"kid": {"type": "string"}, "alg": {"enum": ["EdDSA", "ES256"]}, "public_key": {"type": "string", "description": "JWK"}, "valid_from": {"type": "string", "format": "date-time"}, "valid_until": {"type": "string", "format": "date-time"}}}},
    "offer_feed_url": {"type": "string", "format": "uri"}, "agent_ids": {"type": "array", "items": {"type": "string"}},
    "dispute_contact": {"type": "object", "required": ["endpoint"], "properties": {"endpoint": {"type": "string", "format": "uri"}, "email": {"type": "string"}, "availability_commitment": {"type": "string"}}},
    "settlement": {"type": "object", "required": ["rails"], "properties": {"rails": {"type": "array", "minItems": 1, "items": {"type": "object", "required": ["rail", "account_ref"],
                   "properties": {"rail": {"enum": ["card", "a2a_instant", "a2a_batch", "wallet", "stablecoin", "other"]}, "network": {"type": "string"}, "account_ref": {"type": "string"}, "psp": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/PartyRef"}}}}}},
    "collection_right": {"type": "object", "required": ["method", "operated_by"],
                         "properties": {"method": {"enum": ["direct_debit_mandate", "reserve_balance", "guarantee", "netting"]}, "operated_by": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/PartyRef", "description": "a licensed PSP or acquirer"},
                                        "reference": {"type": "string"}, "cap": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}}},
    "liability_cap": {"type": "object", "properties": {"per_purchase": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}, "insured": {"type": "boolean"}}, "description": "agent providers: the Step 3 cap disclosed to users"},
    "rail_enforcement": {"type": "array", "items": {"type": "object", "required": ["psp", "controls"],
                         "properties": {"psp": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/PartyRef"}, "controls": {"type": "array", "items": {"type": "string"}}, "acknowledged_at": {"type": "string", "format": "date-time"}}},
                         "description": "controls a PSP also enforces on the rail; the agent provider stays liable to the buyer and has recourse against the PSP (A4.1 Step 3, ABS-9)"},
    "responding_party_rules": {"type": "array", "items": {"type": "object", "required": ["scope", "party"], "properties": {"scope": {"enum": ["seller_goods_and_conduct", "platform_feed", "platform_fees", "catalogue_merges", "hosting_duties", "guarantor_of_last_resort"]}, "party": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/PartyRef"}}},
                               "description": "marketplaces: who answers for each kind of line (ABS-1.5b)"},
    "programme_guarantee": {"type": "object", "properties": {"held_by": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/PartyRef"}, "funded_by": {"enum": ["programme_fees"]}, "covers": {"type": "array", "items": {"enum": ["unpaid_decision", "spoofed_register", "infeasible_rail_execution"]}}}},
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
        P->>R: authorisation with agent-capable token, agent indicator, authentication_ref (mandate or approval)
        Note right of P: abs_binding.reference_value in a merchant/additional data field where the network allows
        R->>I: authorisation request
        I-->>R: approved, authorisation_code
        R-->>M: approved; clearing and settlement per scheme; acquirer applies payout hold or reserve per timing
        P->>P: append result; card_binding filled
    end
    rect rgb(235,245,255)
        Note over P,M: Account-to-account instant rail
        P->>I: credit transfer instruction: amount, payee account_ref, end_to_end_id, remittance = ABS:<purchase_id>:<anchor16>
        I->>I: payee name check where offered; SCA satisfied by mandate or approval reference
        I->>R: instant credit transfer (pacs.008 family)
        R-->>M: funds credited to the merchant's PSP; held per timing where a payout hold applies
        R-->>I: confirmation
        P->>P: append result; a2a_binding filled
    end
    Note over P,M: Same Purchase Record, same chain_head, two bindings. The rail carries the reference, never the mandate or the trace.
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
        alt funds under payout hold or reserve at the merchant's PSP or acquirer
            DC->>PSP: payout_return to the user; nothing to collect
        else
            DC->>M: refund instruction (card refund or credit transfer) with the case id
            alt merchant does not pay in 10 days
                DC->>PSP: card: chargeback in the fitting category with the Decision as evidence; A2A: return or recall where supported, else collection right
            end
        end
        PSP-->>U: credit to the original instrument
    else liable = agent_provider or PSP (AG1-P)
        DC->>P: refund instruction; collection right if unpaid
        PSP-->>U: credit to the original instrument or account
        opt goods return ordered
            U->>M: return; shipping per Decision; merchant refund on return flows to P
        end
    else buyer side (AG2, AG5)
        alt withdrawal right available
            DC-->>U: remedy = withdrawal: return the goods within the window at own cost; merchant refunds on receipt
        else
            DC-->>U: deny; statutory routes stated in the Decision remain open
        end
    end
    DC->>DC: close case; record settlement_instruction_ids; a participant that does not pay is suspended from the registry
```

---

## A7. Decision Center governance

Founder's words: "we must have AI dispute decision center, we not plan to hire huge stuff, be pro
AI, but use our own invention like menimi, we improve decision makeing to the most modern never
seen level, we always know what we do and why decision is what it is". And, on structure:
decentralised decision centres for availability and compliance.

### A7.1 Principle

AI-first with a guaranteed human-review right. Models find facts and cite the evidence. A
deterministic rule engine applies the decision order of A4. Every decision carries a signed receipt
with the full rule path and a plain-language explanation. Any party can obtain a human review
before the decision is final between participants. Humans audit a random sample. Error and reversal
rates are published. Decisions bind merchants and agent providers by contract; consumers keep every
statutory route. The same facts give the same decision on any node of the network.

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
   Finding) and no view of the other finders' output. Types: offer conformity per binding
   attribute (snapshot spec against delivery evidence, applying tolerance and verification
   method); mandate compliance split into hard limits and item requirements (deterministic, not a
   model) and intent match against the explicit stated terms (model); injection and manipulative
   content detection (prompt-injection pack plus a model over the `UntrustedText` fields in the
   snapshots); delivery status (deterministic from the Delivery Record where structured, model for
   free-text carrier events and image evidence); credibility (consistency of each side's
   statements with the chain). Every Finding cites evidence by hash; a Finding without a citation
   is dropped. Models run at the lowest temperature available, with pinned versions; prompts are
   hashed into the Finding.
2. **Quorum.** Each decision-relevant Finding type is produced by a quorum of two or three
   different model families (not two sizes of one family). Agreement rule: identical values and
   minimum confidence at or above 0.80. Disagreement or low confidence escalates to a second panel
   with different models and higher effort; if that still disagrees, a human produces the Finding.
   The quorum is also a manipulation defence: text crafted to flip one judge must flip two
   families.
3. **Deterministic ruleset.** `abs-liability` encodes Steps 0 to 4, the precedence, the remedies,
   the withdrawal overlay and the amount formulas; `abs-settlement` the rail mapping. Inputs are
   the Findings plus the verifier's deterministic Findings (signatures, chain, anchor, attachment
   hashes), canonicalised (RFC 8785) so any node computes the same bytes. Output: Decision,
   Settlement Instructions, Decision Receipt.
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
   simulation 73 of 524 scenarios reached a human (every debatable or uncertain ground truth, every
   evidence conflict, and a 1-in-9 sample), 2 by the engine's own escalation.
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
   changes; red-team cases added each quarter, including attacks on the fact-finders themselves.
9. **What the humans do.** A small team: the residual Findings, requested reviews, the sample,
   appeal panels, approval of rule changes proposed by the learning loop, red-team cases. They do
   not decide cases freehand; a human Finding goes through the ruleset like any other.

### A7.4 Finding and Decision Receipt

**Finding.** One typed fact about one subject, with confidence and at least one evidence citation.
Deterministic verifications are Findings with `deterministic: true` and confidence 1. Signed by:
the node (fact-finder models hold no keys).

```json
{
  "$id": "urn:abs:schema:0.2:finding",
  "type": "object",
  "required": ["finding_id", "case_id", "finder", "type", "subject", "value", "confidence", "evidence", "deterministic", "produced_at", "node_id"],
  "additionalProperties": false,
  "properties": {
    "finding_id": {"type": "string"}, "case_id": {"type": "string"}, "node_id": {"type": "string"},
    "finder": {"type": "object", "required": ["kind", "id"],
               "properties": {"kind": {"enum": ["verifier", "model", "human"]}, "id": {"type": "string", "description": "model id and version, verifier version, or reviewer pseudonym"},
                              "model_family": {"type": "string"}, "prompt_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}, "panel": {"type": "integer", "minimum": 1}, "seat": {"type": "integer", "minimum": 1}}},
    "type": {"enum": ["mandate_signature", "chain_integrity", "anchor_match", "attachment_match", "mandate_hard_limits", "item_requirements", "intent_match",
                      "offer_conformity", "price_fee_consistency", "listing_edit", "injection_detection", "manipulative_content", "delivery_status", "credibility", "withdrawal_right"]},
    "subject": {"type": "object", "properties": {"line": {"type": "integer"}, "field": {"type": "string"}, "party": {"enum": ["buyer_side", "merchant"]}}},
    "value": {"type": "string", "description": "closed vocabulary per type: offer_conformity: conforms | within_tolerance | non_conforming | undeterminable; intent_match: matches | explicit_term_broken | ambiguous_should_have_asked | unstated_intent_only; injection_detection: present | absent; delivery_status: delivered | not_delivered | undeterminable"},
    "spec_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    "evidence": {"type": "array", "minItems": 1, "items": {"type": "object", "required": ["type", "hash"],
                 "properties": {"type": {"type": "string"}, "hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}, "locator": {"type": "string"}, "reliability_note": {"type": "string", "maxLength": 200}}}},
    "rationale": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/UntrustedText"},
    "deterministic": {"type": "boolean"},
    "produced_at": {"type": "string", "format": "date-time"}
  }
}
```

**Decision Receipt.** Signed by: the issuing node (engine key, in the envelope with `role:
arbiter`). Verifiable offline against the network's JWKS; its hash is in the transparency log.

```json
{
  "$id": "urn:abs:schema:0.2:decision-receipt",
  "type": "object",
  "required": ["receipt_id", "subject_type", "subject_id", "node", "engine", "ruleset", "inputs", "rule_path", "verdict", "reason", "quorum", "human_review", "log_entry", "issued_at"],
  "additionalProperties": false,
  "properties": {
    "receipt_id": {"type": "string"},
    "subject_type": {"enum": ["decision", "allowance_routing", "trust_attestation", "qualification", "suspension", "expulsion", "appeal"]},
    "subject_id": {"type": "string"}, "case_id": {"type": "string"}, "appeal_of": {"type": "string"},
    "node": {"type": "object", "required": ["node_id", "operator", "region"], "properties": {"node_id": {"type": "string"}, "operator": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/PartyRef"}, "region": {"type": "string", "description": "e.g. EU"}}},
    "engine": {"type": "object", "required": ["name", "version", "verify_url", "jwks_url"],
               "properties": {"name": {"type": "string"}, "version": {"type": "string"}, "verify_url": {"type": "string", "format": "uri"}, "jwks_url": {"type": "string", "format": "uri"}}},
    "ruleset": {"type": "object", "required": ["id", "version", "hash"], "properties": {"id": {"type": "string"}, "version": {"type": "string"}, "hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}, "effective_from": {"type": "string", "format": "date-time"}}},
    "inputs": {"type": "object", "required": ["finding_hashes", "canonical_input_hash"],
               "properties": {"finding_hashes": {"type": "array", "items": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}},
                              "canonical_input_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash", "description": "hash of the RFC 8785 canonical input; any node with the same inputs and ruleset reproduces the same decision"},
                              "evidence_bundle_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}, "evidence_level": {"enum": ["E0", "E1", "E2", "E3"]}}},
    "rule_path": {"type": "array", "minItems": 1, "items": {"type": "object", "required": ["step", "rule_id", "inputs_used", "result"],
                  "properties": {"step": {"type": "integer"}, "rule_id": {"type": "string", "description": "e.g. S0, S1-CONFORMITY, S2-MANIPULATION, S3-AGENT-FAULT, S4-BUYER, P-PRECEDENCE, REM-AG1P, WDR-OVERLAY, SET-A2A-AG3"},
                                 "inputs_used": {"type": "array", "items": {"type": "string"}}, "result": {"type": "string"}, "note": {"type": "string", "maxLength": 300}}}},
    "verdict": {"enum": ["decided", "needs_evidence", "escalate_panel", "escalate_human", "attested", "refused", "suspended", "expelled"]},
    "reason": {"type": "string"},
    "quorum": {"type": "object", "required": ["families", "panels_run", "agreement", "min_confidence"],
               "properties": {"families": {"type": "array", "items": {"type": "string"}}, "panels_run": {"type": "integer"}, "agreement": {"type": "boolean"}, "min_confidence": {"type": "number"}}},
    "human_review": {"type": "object", "required": ["requested", "performed"], "properties": {"requested": {"type": "boolean"}, "performed": {"type": "boolean"}, "reviewer_pseudonym": {"type": "string"}, "outcome": {"enum": ["upheld", "changed", "not_performed"]}}},
    "decision_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash", "description": "hash of the Decision body this receipt proves; identical across nodes for identical inputs"},
    "log_entry": {"type": "object", "required": ["log_id", "leaf_hash"], "properties": {"log_id": {"type": "string"}, "leaf_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}, "tree_size": {"type": "integer"}, "inclusion_proof": {"type": "array", "items": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}}}},
    "issued_at": {"type": "string", "format": "date-time"}
  }
}
```

### A7.5 Federated Decision Network

One centre is a single point of failure and a single point of pressure. The Decision Center is a
network of independent, accredited operator nodes.

1. **Nodes.** Each node is run by an accredited operator, independent of the parties in the cases
   it decides (A2). Deterministic rules plus canonicalised inputs mean any node reproduces the
   identical Decision and receipt hash for the same Findings and ruleset version, so failover is
   safe and a party can ask a second node to recompute. Every receipt carries the rule-version
   reference and the node id.
2. **Fact-finding quorum.** Two or three different model families per Finding type, with the
   agreement rule of A7.3. Nodes MAY use different providers for the same family set; the quorum
   record is in the receipt.
3. **Transparency log.** A tamper-evident, append-only Merkle log of decision and receipt hashes
   and of rule versions, in the manner of Certificate Transparency (RFC 9162; the fit of its exact
   structures is to be verified in the matrix). Parties and auditors verify inclusion and
   consistency; personal data stays off the log, hashes only. A decision that is not in the log is
   not final between participants.
4. **Data residency.** EU-region nodes decide cases with EU parties; evidence stays in region. A
   data-protection impact assessment is performed for the network and per node. Merchants that are
   companies are outside the GDPR; sole traders and users are not.
5. **Resilience.** Where operators or participants are financial entities, the EU Digital
   Operational Resilience Act applies to the ICT services they use: incident classification and
   reporting, resilience testing, third-party risk registers (applicability per operator, to be
   verified). ISO 22301 business continuity for every node; published recovery time and recovery
   point objectives for the case store and the log.
6. **Degraded mode.** If no node can decide: funds stay in the PSP payout hold or reserve where
   one applies; dispute deadlines pause and are extended day for day; after a defined time (default
   30 days) the case falls back to the existing chargeback route or statutory ADR with the Evidence
   Package handed over. The availability claim is "no single point of failure and zero lost
   disputes", not a percentage uptime.
7. **Governance.** Rule changes are signed by the governance body, published in advance with a
   notice period, versioned and hashed into the log; operators are accredited against independence
   and impartiality requirements (ADR rules; ISO 10003 as the management-system reference) and
   re-accredited periodically; no operator decides disputes involving its own agents or merchants;
   accreditation, suspension and removal of operators are themselves logged decisions.
8. **Compliance map.** EU AI Act: an AI system used "in a similar way in alternative dispute
   resolution" is listed in Annex III point 8(a) (wording per Audit 0). The network is designed as
   a high-risk system: risk management, data governance, logging, transparency to users, human
   oversight with power to override, accuracy and robustness, a quality management system,
   conformity assessment and registration in the EU database (the article references are to be
   verified in the matrix). Audit 0 reports that the Digital Omnibus moved the Annex III
   obligations to 2 December 2027 (secondary source; regulation number unverified). GDPR Article
   22(3): human intervention, the right to express a view and to contest, on request. ADR
   Directive 2013/11/EU on expertise, independence and impartiality and on the limits of
   pre-dispute agreements, and the amending Directive (EU) 2025/2647 on prior notice of automated
   means and review by a natural person (dates and article numbers per Audit 0, unverified). ISO/IEC
   42001 for the AI management system; ISO/IEC 27001 for information security. Whether a private
   contractual resolution centre is "alternative dispute resolution" under the AI Act is open;
   the network is designed as if it is.

**Node and log schemas.**

```json
{
  "$id": "urn:abs:schema:0.2:decision-node",
  "type": "object",
  "required": ["node_id", "operator", "region", "accreditation", "engine", "rulesets", "keys", "log_id", "status"],
  "properties": {
    "node_id": {"type": "string"}, "operator": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/PartyRef"}, "region": {"type": "string"},
    "accreditation": {"type": "object", "required": ["accredited_at", "valid_until", "independence_statement_hash"],
                      "properties": {"accredited_at": {"type": "string", "format": "date-time"}, "valid_until": {"type": "string", "format": "date-time"},
                                     "independence_statement_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}, "excluded_parties": {"type": "array", "items": {"type": "string"}, "description": "party_ids whose cases this node must not decide"},
                                     "receipt_id": {"type": "string"}}},
    "engine": {"type": "object", "properties": {"name": {"type": "string"}, "version": {"type": "string"}}},
    "rulesets": {"type": "array", "items": {"type": "object", "properties": {"id": {"type": "string"}, "version": {"type": "string"}, "hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}}}},
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
  "$id": "urn:abs:schema:0.2:log-entry",
  "type": "object",
  "required": ["log_id", "index", "timestamp", "entry_type", "leaf_hash", "node_id"],
  "additionalProperties": false,
  "properties": {
    "log_id": {"type": "string"}, "index": {"type": "integer", "minimum": 0}, "timestamp": {"type": "string", "format": "date-time"},
    "entry_type": {"enum": ["decision", "receipt", "ruleset_version", "node_accreditation", "node_status", "appeal", "human_review"]},
    "leaf_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash", "description": "hash of the entry object; no personal data on the log"},
    "subject_id": {"type": "string"}, "node_id": {"type": "string"},
    "ruleset_ref": {"type": "object", "properties": {"id": {"type": "string"}, "version": {"type": "string"}, "hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}}},
    "tree_head": {"type": "object", "properties": {"tree_size": {"type": "integer"}, "root_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}, "signature": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Signature"}}}
  }
}
```

### A7.6 Decision pipeline

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
    N1->>V: signatures, chain recompute, anchor vs rail reference, attachments vs checkout snapshot
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

A node MUST: produce Findings with citations from a quorum of at least two model families; run a
deterministic ruleset on canonicalised inputs; issue a signed receipt with the full rule path and a
plain-language explanation; offer a human review to any party on request before finality between
participants; append every decision to the transparency log; publish accuracy, reversal, human
residual and quorum disagreement rates; publish rule versions in advance; never decide a case
involving its operator's own agents or merchants; state in every Decision that consumer statutory
routes are unaffected.

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

Everything else in A4 is read off signed records by the verifier (signatures, chain, anchor,
attachment hashes, hard limits and item requirements, cart origin, feed-versus-snapshot values,
time limits, Register entries) and needs no model. Eighteen of the simulation's 28 rules are of
that kind.

### A7.9 Experiment note (H6)

Phase 2 uses end-to-end LLM arbitration (A1: one model reads the bundle and returns code, liable
party, remedy, confidence) and the hybrid (A2: fact-finders, tie-break, deterministic engine,
signed receipt). H6 (Amendments 1 and 2) states that A2 is more consistent across three runs than
A1, at least as accurate on liability allocation (non-inferiority margin 10 points), and that its
errors are traceable to a specific Finding. Audit 0's point stands: the determinism of the rules
moves inconsistency into fact-finding; H6 tests exactly that seam. Audit 0 also notes that the
arbiters and buying agents come from the same model families because no other family was available;
the limitation is recorded in Amendment 5.

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
- **Cross-family quorum with citations** (A7.3): two or three model families, agreement rule,
  second panel on disagreement; a Finding without a citation to signed evidence is discarded.
- **Abstention, then escalation.** Below the confidence threshold (default 0.80) the finder
  abstains; the engine returns `review`; a human supplies the Finding (A7.3 items 2 and 5).
- **Random human audits that publish error rates** (A7.3 item 8): the Finding error rate per type
  and per model family is published, so a party knows how often "conforms" is wrong.
- **Burden-of-proof defaults when facts cannot be established.** A record keeper that cannot
  produce its record loses the question (ABS-E1, ABS-E1m); an ambiguous listing is read against
  its author (ABS-S2); an unsupported claim fails (ABS-E2); records that conflict with no keeper at
  fault go to a human (ABS-H1). The engine never guesses.

What remains: a confident, cited, agreed Finding that is still wrong. The audit sample and the
appeal route are the only correction; their capacity is sized to the measured error rate.

### A8.2 Unforeseen cases

The catalogue has 524 scenarios; the world has more.

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

Jurisdiction profiles (general statements; verify before relying on any):

| Jurisdiction | Constraint on placing unstated intent on a consumer | ABS position |
|---|---|---|
| EU | Unfair-terms rules apply to standard terms that cause a significant imbalance; consumer protection of the home law cannot be removed by choice of law; the withdrawal right and conformity guarantees are mandatory | Step 4 is reached only after capture duty, hard limits, item requirements and explicit instructions have been exhausted; the withdrawal overlay gives the consumer a no-fault exit; Decisions never bind the consumer |
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
- **Start where the data is structured.** Categories with GTIN and producer data (electronics
  under a product passport, GDSN-fed goods) first; the structured-versus-legacy comparison in the
  experiment measures the difference.

What remains: at E0 and E1 most not-as-described cases are undecidable on content and fall to the
burden-of-proof defaults; the simulation measured 17.4% decidable at E0.

### A8.6 Correlated AI blind spots

Two model families can be wrong the same way: the same training data, the same failure on a
rotated label, the same susceptibility to an optimised injection.

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

---

## A9. Agent conformance at scale

Founder's requirement: agents will be built by third parties in enormous numbers, so ABS must make
them behave. The principle: **do not trust the agent; enforce at the choke points.** A
non-conforming agent cannot exceed a hard limit, cannot pay a non-participant, cannot alter a
frozen offer and cannot escape the record, because none of those is in the agent's hands.

### A9.1 Enforcement points no agent can bypass

| Choke point | Who operates it | What it enforces | How the agent is kept out of it |
|---|---|---|---|
| The payment credential | Issuer, network, PSP | Agent-specific network or agentic tokens with domain restriction and spend controls: merchant scope, per-transaction and periodic limits, expiry, single use where set (EMVCo payment tokenisation; Mastercard Agent Pay agentic tokens; Visa Intelligent Commerce; statuses in `LANDSCAPE.md`, scope to verify per network) | The agent holds a token bound to the Mandate, never a card number; the controls live at the issuer and network and decline a breaching authorisation regardless of what the agent does |
| The merchant's ABS checkout | Merchant (or its PSP) | Verifies the Mandate signature and scope (merchant, category, amount, expiry) and the agent provider's registration; freezes the Offer Snapshot and countersigns it; rejects a cart that does not match a signed offer; rejects any request for card data | The merchant will not accept an order from an unregistered provider or outside the Mandate's scope; the snapshot is signed by the merchant, so the agent cannot alter the offer it is held to |
| The PSP or issuer | Buyer's PSP, issuer | Checks the Allowance controls registered under `rail_enforcement` (limits, MCC blocks, allowlists, country block, single-use credential) and runs the step-up or approval authentication in the user's own authenticator | The approval happens outside the agent's conversation; the agent cannot self-approve; where a credential control is encoded the PSP declines before the agent provider's own check even runs |
| The Decision Center and the Register | Operator network | Verifies the chain anchored in the rail reference, the signatures and the Register entry at dispute time; a Purchase Record the agent did not write, or wrote wrongly, counts against its provider (ABS-E1) | The agent's trace is hashed into the rail reference at payment time; a provider that later cannot produce a matching log loses the question |

Because hard limits and item requirements are checked at the credential, at the checkout and by
the provider's own C1 gate, a breaching purchase that still settles is provably someone's failure
(A4.1 Step 3 and ABS-9), and the buyer never has to find out whose.

### A9.2 Know Your Agent

- **Provider registration and accountability.** Every agent acts under a registered agent
  provider with a Participation Agreement, keys per role, a collection right operated by a licensed
  PSP, a disclosed Step 3 liability cap, and a dispute endpoint. There is no anonymous agent on the
  network: an agent request that cannot be tied to a registered provider is refused at the
  merchant's checkout.
- **Agent identity on the wire.** Requests from agents to merchants are signed at the HTTP layer
  with the provider's registered key (HTTP Message Signatures, RFC 9421); network-specific
  recognition schemes (Visa Trusted Agent Protocol, Mastercard Agent Pay registration) and the IETF
  Web Bot Auth drafts can carry the same identity where a merchant already relies on them (status
  per `LANDSCAPE.md`). The `agent_id` in every record is the provider's, versioned.
- **Liability as the incentive.** Mandate breach (Step 3), capture failure (Step 3b), payment to a
  non-participant (ABS-P1), reliance on an unverified feed (ABS-F1), undisclosed incentives (ABS-X2)
  and obeying instructions in data (A5.7) all land on the provider. The provider's cheapest path is a
  conforming agent.

### A9.3 ABS Agent Profile: the normative behaviours

A conforming buying agent, whoever built it:

1. **Proposes the Mandate and captures requirements.** Builds the Mandate from the conversation
   using the category template; captures every stated requirement as a term or item requirement;
   shows the captured and the open terms; obtains the user's strong-authentication confirmation;
   records `conversation_hash` (A4.1 Step 3b, A4.2).
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
   writes the Purchase Record with cart origin, controls and trace digest; anchors the chain head in
   the rail reference; uses an idempotency key (A5).
7. **Asks when told to ask.** Honours `ask_on_ambiguity`; never guesses where the Mandate says to
   ask; records clarifications with their authentication reference.
8. **Requests step-ups.** Routes risk signals and threshold crossings to the user's authenticator,
   never to a self-generated confirmation.
9. **Records refusals.** Writes a Refusal Record for every decision not to buy (A3.2).
10. **Supports the dispute.** Classifies from the Package, proposes the code and the withdrawal
    option honestly, files only with the user's consent, never files a claim it knows is false, and
    produces the Package on request.

```json
{
  "$id": "urn:abs:schema:0.2:agent-profile",
  "type": "object",
  "required": ["agent_id", "agent_provider", "agent_version", "model_families", "conformance", "behaviours", "certification"],
  "additionalProperties": false,
  "properties": {
    "agent_id": {"type": "string"}, "agent_provider": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/PartyRef"},
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
      "properties": {"certifier": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/PartyRef"}, "harness_version": {"type": "string"}, "catalogue_version": {"type": "string"},
                     "passed_at": {"type": "string", "format": "date-time"}, "valid_until": {"type": "string", "format": "date-time"},
                     "results_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}, "recertify_on": {"type": "array", "items": {"enum": ["model_change", "purchasing_logic_change", "catalogue_major_version", "expiry"]}}}},
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
| ABS-Agent-Full | All ten behaviours at E3, including view-time snapshots, the chain anchor, clarifications with authentication references, step-ups through the authenticator, and dispute support with the full Package; plus the red-team subset (adaptive injection) with a published attack-success rate | As Basic, plus quarterly red-team subset |

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
| `offer.fetch` | merchant feed URL or protocol object (UCP, ACP, AP2) | validated typed offers, signature results, `non_binding` flags; free text as `UntrustedText` | Schema validation; untrusted text; binding offers only |
| `offer.snapshot` | offer, when (view or checkout), compared record | Offer Snapshot with `spec_hash`, `compared_record`, `idempotency_key`; merchant countersignature request | Freezing and recording |
| `approval.request` | cart hash, level, approver, prompt content | Approval Record with authentication reference, or `declined` / `expired` / `cancelled` | Step-ups through the authenticator; `approval_prompt_must_show` |
| `purchase.record` | Mandate, snapshots, cart with origin, controls, action log | Purchase Record with trace digest and chain head; Settlement Instruction draft with `abs_binding` | Trace digest; anchor in the rail reference |
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

| Layer | Existing work ABS defers to | What ABS adds |
|---|---|---|
| Mandate and signed checkout | AP2 v0.2 (28 Apr 2026): Checkout and Payment Mandates as verifiable credentials; the merchant-signed checkout JWT; both contributed to the FIDO Alliance (28 Apr 2026) with Mastercard Verifiable Intent (5 Mar 2026). Visa Core Rules 4.1.23.3: consent to a cardholder-defined payment instruction with expiry, identity verification, acknowledgement of responsibility. EMVCo "Agentic Payments: Framework for Specifications v1.0", draft for comment from 1 Sep 2026 (content UNVERIFIED). NPCI UPI Reserve Pay / UPI Circle in India (secondary). | The Mandate digest as a profile: `intent_hash`, captured item requirements, `ask_on_ambiguity`, `accepted_deviations`, the Allowance reference; the rule that mandate plus clarifications is "what the buyer asked for". AP2 says dispute use of its evidence is out of scope; ABS is that use. |
| Catalogue and checkout objects | Google UCP (announced Jan 2026 with Shopify; Catalog, Cart, Checkout, Order capabilities; merchant stays merchant of record). OpenAI and Stripe ACP product feed and checkout specs (API versions 2025-09-12 and 2025-09-29). Klarna Agentic Product Protocol (Dec 2025, secondary). | An injection-safety profile: bounded `UntrustedText`, instructions to agents rejected at publication, typed-only agent reasoning; the conformity-critical attribute set with tolerances; the countersigned snapshot as "the listing". |
| Agent identity | Visa Trusted Agent Protocol with Cloudflare (14 Oct 2025); Visa registration of agentic payment providers (rules 4.1.23.2) and disqualification (4.1.23.11); Mastercard Agent Pay registration and agentic tokens (Oct 2025); IETF Web Bot Auth drafts on RFC 9421 (status UNVERIFIED). | Nothing. ABS defers. |
| Card-rail liability for in-mandate actions | Visa Core Rules 4.1.23.10: the cardholder is responsible "as if the Cardholder initiated the Transaction". Amex (Apr 2026): protection "from charges related to AI agent error" for registered agents (press report; terms UNVERIFIED). PayPal: Purchase Protection on eligible agentic transactions; Seller Protection for unauthorised and item-not-received only. | Step 4 agrees with Visa. Step 3 is a provider-to-user contract over the scheme rule, for provable agent fault only. The decision order and evidence that an issuer offering Amex-style protection can use to decide when it applies. |
| Agent-specific dispute reason codes | None in the Visa rules (checked by Audit 0); none public from Mastercard (UNVERIFIED). Disputes are filed today under fraud or not-as-described codes. | The taxonomy AG1-M, AG1-P, AG2, AG3, AG4, AG5 with the legacy mapping. The most valuable deliverable. |
| Merchant risk | Acquirer underwriting; Visa VAMP (enforcement from 1 Oct 2025) and Integrity Risk Program; Mastercard Excessive Chargeback Program and MATCH; marketplace payout holds (Amazon DD+7; PayPal and eBay up to 21 days); EU DSA Article 30 trader traceability for marketplaces. | Part B1: a neutral, cross-rail, agent-queryable trust signal that reuses those mechanisms; nothing inside it is new. |
| Account-to-account protection | UK APP reimbursement (from 7 Oct 2024) for purchase scams by a payee that meant to defraud, excluding civil disputes with a genuine supplier; Brazil Pix MED 2.0 (mandatory 2 Feb 2026); EPI Wero purchase protection being designed (workshops Q4 2026, framework Q1 2027; single trade-press source, UNVERIFIED). | A contractual refund obligation and a payout hold for non-delivery or non-conformity by a genuine merchant, the case those schemes do not cover; the same decision order on every rail. |
| Rules-based dispute automation | Visa Rapid Dispute Resolution (merchant-set rules refund automatically); Compelling Evidence 3.0 (card-absent fraud decided from matching data); Ethoca alerts. | Fact-finding over agent records by models, with a deterministic ruleset and receipt; the two-family quorum; human review on request. |
| Rail-agnostic settlement | AP2 and Visa Intelligent Commerce Connect are network-agnostic (pilot, Apr 2026); x402 for stablecoins (Linux Foundation, Apr 2026, secondary); ACP and EMVCo are card-only. | The Settlement Instruction and the mapping of each reason code onto card and ISO 20022 mechanisms. |

### A10.2 Regulation: PSD2 today, PSD3 and the PSR when they apply, the IPR, UK APP

Legislative statuses are as reported in `LANDSCAPE.md` on 2026-11-04; where a text is not final,
the mapping is "as proposed" or "as agreed" with the date given there.

| Topic | PSD2 and the SCA RTS (in force) | PSD3 / PSR (status per LANDSCAPE.md) | ABS mapping |
|---|---|---|---|
| Strong customer authentication | SCA for electronic payments, with dynamic linking of amount and payee; exemptions for low-value, trusted beneficiaries, recurring transactions, transaction risk analysis, secure corporate payments; merchant-initiated transactions treated as payee-initiated after an authenticated set-up (EBA Q&A) | Rules move from the directive to the regulation; detailed changes as proposed or agreed | The Mandate's `authentication` block records which route was used; the Allowance's approval level is a normal SCA event; autonomous purchases rely on an exemption whose conditions the PSP applies (A12.1). A mandate set up without the payer's PSP is not an SCA event (Audit 0) |
| Unauthorised transactions | Refund right for the payer; limited payer liability unless gross negligence or fraud | Carried forward; additions on impersonation fraud as proposed or agreed | AG0 routes a purchase with no valid mandate to this process; ABS supplies the Package to the PSP |
| Authorised but disputed | No refund right from the payment rules; consumer law and scheme rules apply | Proposals on liability for impersonation fraud do not reach "authorised but wrong" by an agent | ABS's whole contribution sits here: AG1-P, AG2 and the decision order |
| Instant payments | Instant Payments Regulation (EU) 2024/886: Verification of Payee (payee name check) and price parity, with application dates per LANDSCAPE.md | Not changed by PSD3 | `payee_name_check` in the A2A binding; Trust Authority Q3 reuses it; it reduces misdirected payments, not non-delivery by a genuine payee |
| UK APP reimbursement | PSR rules from 7 Oct 2024: reimbursement of purchase scams where the payee meant to defraud, with a cap, a possible excess and a consumer standard of caution; civil disputes with a genuine supplier excluded | Not applicable | ABS covers the excluded case: non-delivery or non-conformity by a genuine participant, decided by evidence |
| Consumer law | Consumer Rights Directive withdrawal right; Sale of Goods Directive conformity; Unfair Contract Terms; Rome I and Brussels I bis on consumer forum and law (per Audit 0) | Unchanged | Decisions do not bind consumers beyond law; withdrawal overlay; without prejudice to statutory conformity |
| AI Act, GDPR, ADR | See A7.5 item 8 | | Decision Center designed as high-risk; human review on request; ADR independence |

### A10.3 Standards alignment matrix

Confidence: high = scope verified on a primary source in `LANDSCAPE.md`; medium = secondary
source or scope partly verified; low or UNVERIFIED = not confirmed; the entry stays only because
the fit is plausible and the standard is named by the parties ABS must work with.

| ABS element | Standard and part | How it is reused | What ABS adds | Confidence |
|---|---|---|---|---|
| Object hashing | RFC 8785 JSON Canonicalization Scheme | Canonical form before hashing and signing | Nothing | high |
| Signatures, keys | RFC 7515 JWS, RFC 7517 JWK | Detached-payload compact JWS over the hash; JWK in the registry | Role-per-key rule | high |
| Schemas | JSON Schema 2020-12 | All object definitions | Nothing | high |
| Agent requests to merchants | RFC 9421 HTTP Message Signatures; Web Bot Auth drafts | Agent identification at the HTTP layer | Nothing | high (RFC) / UNVERIFIED (drafts' status) |
| Mandate container | AP2 v0.2 mandates (SD-JWT VCs); W3C Verifiable Credentials 2.0 | The Mandate digest as a credential | Fields in A5.5 | medium |
| Trust attestation container | W3C Verifiable Credentials 2.0 and DIDs 1.0 | Attestation as a VC issued by the Trust Authority | Fields in Part B1 | medium |
| Legal-weight receipts | eIDAS qualified electronic seals and time stamps (Regulation 910/2014 as amended by 2024/1183) | Optional qualified seal on Decision Receipts | Nothing | medium |
| Merchant legal identity | ISO 17442 LEI | `legal_entity.lei` where held; not required for small merchants | Registry check for merchants without an LEI | high |
| Category limits | ISO 18245 merchant category codes; GS1 GPC | `Category.vocabulary` values | ABS profiles as a third vocabulary | high |
| Product identity | GS1 GTIN; GS1 Digital Link | `gtin` on offers and snapshots | Spec keyed by GTIN | high |
| Product attributes | schema.org Product / Offer / OfferShippingDetails / MerchantReturnPolicy; GS1 Web Vocabulary and GDSN; ECLASS; ETIM | Dictionary references on attributes; schema.org projection of the offer | Binding flag, tolerance, verification method, non-binding state, profiles | medium |
| Units | UCUM; ISO 80000 | `Attribute.unit` | Nothing | high |
| Product passport | EU Digital Product Passport under Regulation (EU) 2024/1781 | `dpp_ref`; producer-sourced attributes | Nothing | medium (product groups and dates per delegated acts) |
| Photo provenance | C2PA | `c2pa_manifest_hash` on images | Nothing; provenance is not truth | high |
| Settlement, A2A | ISO 20022 pacs.008, pacs.004, camt.056, camt.029, camt.027, camt.087; remittance information; ISO 11649 creditor reference | Reference carriage; returns, recalls, investigations, claims where a scheme supports them | The ABS case id in case identification; the mapping table | medium (per-scheme applicability) |
| Settlement, cards | ISO 8583 message family; the refund, chargeback, representment, pre-arbitration, arbitration lifecycle; EMV 3-D Secure; EMVCo payment tokenisation; EMVCo agentic framework draft | Authentication and token references; dispute stages and categories | Reason-code mapping | high (lifecycle, 3DS, tokens) / UNVERIFIED (agentic framework content) |
| Strong authentication | PSD2 SCA RTS (Delegated Regulation (EU) 2018/389); PSD3/PSR as proposed or agreed | Mandate and approval authentication; exemptions for autonomous purchases | Allowance semantics | high (PSD2) / per LANDSCAPE.md (PSD3) |
| Consent object | OAuth 2.0 (RFC 6749); Rich Authorization Requests (RFC 9396); OpenID FAPI 2.0; Grant Management | Allowance as `authorization_details`; FAPI for bank APIs; revocation | Field set | medium |
| E-invoicing | EN 16931 (UBL and CII syntaxes); Peppol BIS Billing 3.0; Directive 2014/55/EU for public bodies; ViDA | B2B and B2G invoices requested at checkout | The rule that a B2B agent purchase carries the invoice reference | medium |
| Low-value imports | EU Import One-Stop Shop | `cross_border.low_value_import_scheme` | Shown before purchase | medium |
| Complaints and ADR | ISO 10002, ISO 10003, ISO 10001; Directive 2013/11/EU and Directive (EU) 2025/2647; UNCITRAL ODR Technical Notes | Decision Center management system and independence; stages of ODR | The agent-specific rules | medium |
| AI governance | ISO/IEC 42001; ISO/IEC 23894; NIST AI RMF; EU AI Act Annex III 8(a) and the high-risk obligations | Decision Center management, risk and oversight | The quorum, receipt and log design | medium |
| Security, privacy, continuity | ISO/IEC 27001 and 27002; ISO/IEC 27701; ISO 22301; GDPR; DORA | Node and participant requirements | RTO/RPO publication; degraded mode | high (scope) / medium (applicability of DORA) |
| Payment data scope | PCI DSS v4.0.1; PCI Software Security Framework | No PAN in agent context; participating software | Nothing | high |
| Quality management | ISO 9001 | Decision Center operation | Nothing | high |
| Transparency log | RFC 9162 Certificate Transparency 2.0 | Merkle log structure and proofs | Entry types for decisions and rules | medium |

Where ABS adds something, no standard covers it because none has an agent as the buyer: the
"authorised but wrong" split (AG1-P / AG2), the mandate digest with captured item requirements, the
countersigned snapshot as the listing, the contestable delivery evidence set, the Allowance routing
semantics, and the Decision Center governance. Each is designed as an extension of the closest
standard: a credential type for the mandate and attestation, a supplementary-data style reference
for ISO 20022, a sub-reason under the existing not-as-described category for AG4, a profile on
UCP/ACP for the catalogue.

**Settlement outcomes with no existing message (extension points found by the simulation).**

| Outcome | Rail or family | Closest existing mechanism | What ABS states |
|---|---|---|---|
| Refund to a cardholder by a third party (the agent provider under AG1-P) | Card | No card message lets a third party refund a cardholder; credit transfer (pain.001 to pacs.008) or a scheme push-to-card credit where offered (uncertain) | The Settlement Instruction names the credit transfer; the case id travels in remittance |
| Merchant or third-party refund | BNPL | Provider API cancels or reduces the loan and returns paid instalments by credit transfer; proprietary | Instruction addressed to the provider; outcome reported in `result` |
| Merchant refund; buyer-protection claim | Wallet | Operator ledger reversal; operator programme; proprietary | Same |
| Re-credit of stored value; third-party refund | Stored value | Programme re-credit; value cannot return to a gift card, so a third-party refund goes by credit transfer | Same |
| Merchant or third-party refund | Stablecoin / x402 | On-chain return transfer; x402 defines no refund primitive; transfers are final | Same; no chargeback exists |
| Payout-hold release keyed to a Delivery Record | All | Acquirer delayed funding; PSP hold under its own terms | `timing.release_condition` |
| Programme guarantee payout | All | None | `direction: collect` from the guarantee holder |
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
    A->>P: draft Mandate under the Allowance Policy: intent_hash, limits, captured item_requirements, ask_on_ambiguity, autonomy_required, accepted_deviations
    P->>U: rulebook summary + mandate in plain words, with the captured requirements listed
    U->>I: authenticate over max_total, payee scope, expiry, nonce (SCA where a PSP performs it)
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
        opt consumer, goods, within 14 days, no exception
            A-->>U: withdrawal right available until <date>: return at own cost for a refund, no reason needed
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
    participant DC as Decision Center (registry only at tier 1)
    U->>A: "not what I wanted" / "not what was offered"
    A->>A: classify from the Package: conformity, item_requirements, explicit terms, injection trace, withdrawal availability
    A-->>U: proposed code, remedy, evidence level; where AG2 or AG5 is likely, say so and show the withdrawal option
    U->>A: consent (authentication reference)
    A->>M: Dispute Case within 60 days
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

Under the payment rules, an approval is a normal strong-authentication event with dynamic linking;
an autonomous purchase relies on an exemption whose conditions the PSP applies (low value with
cumulative counters, a trusted beneficiary the user whitelisted at the bank, a recurring charge of
fixed amount after an authenticated first, transaction risk analysis, secure corporate payments),
or on a merchant-initiated arrangement set up with authentication. Which route applies is recorded
in the Mandate's `authentication` block and is the PSP's call; ABS records it, it does not grant
it. Both failure directions are measured: under-escalation (unsafe autonomous buys, the experiment's
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
  processes; instruments are referenced by tokens. An agent provider that follows this stays
  outside the card data environment for PCI DSS; PSPs and acquirers remain in scope as today.
- Step-up and approval authentication happen in the user's authenticator, never inside the agent's
  conversation.
- The injection defence is structural: typed-only reasoning, `UntrustedText` never an instruction,
  monitor and fact-finders on typed packets, instructions to agents rejected at feed publication,
  two-family quorum. Filters are a second layer; Audit 0 notes the design idea follows the CaMeL
  pattern and is not new; what ABS adds is the liability consequence (A4.2) and the conformance
  requirement.
- Evidence is written to the chain before the Settlement Instruction is sent; a later outage cannot
  lose the record of a paid purchase.
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
| Agent provider: Offer Snapshot at checkout; Purchase Record with trace digest (E1) | required | view and checkout snapshots; full action log retained (E2); hash chain anchored in the rail reference (E3) |
| Agent provider: C2 step-up on signals and threshold | `always_above` required; signals optional | all signals |
| Agent provider: C3 independent monitor on a typed packet | optional | required |
| Agent provider: conformity check support after delivery | user-driven | agent-assisted with image comparison and serial lookup |
| PSP / acquirer: carry the ABS reference; single-use instruction; payout hold and reserve on instruction; `rail_enforcement` acknowledgement | SHOULD | MUST where the rail has a field |
| Decision Center node: A7.7 minimum requirements | required | required plus published statistics, transparency log inclusion proofs on request, and accreditation of the operator |
| Trust Authority (Part B1): entry gate, levels, receipts-based record, per-purchase attestation, suspension with appeal | required | required plus published false-positive and hold-time statistics |
| Certifier | not required | required for agent providers and for merchants above an operator-set volume |
| Agent provider: ABS Agent Profile behaviours (A9.3) and certification | ABS-Agent-Basic: behaviours 1 to 5 and 9 at E1 | ABS-Agent-Full: all ten behaviours at E3, red-team subset, quarterly re-test |
| Agent provider: enforcement at choke points, agent identity on signed requests, provider registration (A9.1, A9.2) | required | required |
| Operator: failure-mode mitigations of A8 (evidence-capture protocol, impact simulation before rule release, private signal weights, error-correlation measurement) | required | required plus published error and correlation rates |
| Highest evidence level the party can offer | E1 | E3 |

---

## A15. Open questions and how the experiment tests the core

### A15.1 Open questions for v0.3

1. **Provider acceptance of Step 3.** Audit 0 reports that major providers' consumer terms place
   all actions on the user with a low liability cap. Step 3 asks for liability only for provable
   fault, capped and insurable. Whether providers sign, and at what cap, is the adoption question.
2. **AG4 split.** Whether the agent provider shares AG4 when its agent obeyed instructions found
   in data (Audit 0, fix 8). v0.2 keeps the rulebook allocation.
3. **Accepted deviations.** Whether a user's advance acceptance in the Mandate satisfies the
   "specifically informed and expressly and separately accepted" test of EU sale-of-goods law when
   the agent then buys.
4. **Strong authentication of a standing Allowance.** Whether autonomous purchases under a policy
   can rely on the named exemptions, or each needs its own basis at the PSP; and the PSD3/PSR text
   once final.
5. **Finality and consumers.** Decisions bind participants by contract and not consumers. How a
   merchant's refund under a Decision interacts with a later chargeback by the same consumer
   (double recovery) needs a rule with the schemes.
6. **AI Act classification.** Whether a private contractual resolution centre is "alternative
   dispute resolution" under Annex III; the network is designed as if it is.
7. **Conformity for services, digital content and custom goods.** Acceptance steps and delivery
   logs are defined; grading scales for used goods and tolerance norms per profile are not.
8. **Rail fields for the anchor.** Which card data field and which A2A remittance element each
   scheme will accept for the ABS reference; the PSP record is the anchor until then.
9. **Collection right and payout holds on A2A.** Operated by licensed PSPs; which PSPs will offer
   a hold keyed to a Delivery Record release condition.
10. **Cross-border law.** Governing law of the Participation Agreement; enforcement of a Decision
    against a participant outside the collection right.
11. **Standards channel and first adopter.** Audit 0 names EPI's Wero purchase protection as the
    realistic first adopter for the account-to-account module (single trade-press source,
    UNVERIFIED), the FIDO Payments working group for the evidence profile, and EMVCo's agentic
    framework for cards. Part B5.
12. **Hypotheses not yet run.** H5 to H7 are pre-registered (Amendments 1, 2 and 5); the
    allowance arm (Amendment 4) and the structured-vs-legacy offer comparison (Amendment 3) are
    secondary. None has results at the time of writing.
13. **Collusion steering stays open.** The simulation's entry-route analysis classifies
    merchant-and-provider collusion that sells conforming goods at inflated prices as the one route
    no gate closes; incentive disclosure (ABS-X2), joint liability (ABS-X1), routing audits and
    cross-provider price-dispersion monitoring limit it but do not stop it.
14. **The programme guarantee.** Its legal form (who holds it, under what licence), its funding
    level against the infeasible-execution residual (22 of 524 in the simulation), and its
    recovery rights need a ruling before a pilot.
15. **Fact-finder judgments.** Ten rules depend on a judgment a deterministic engine cannot make
    from records (whether text instructs an agent, whether a claim is false and caused the choice,
    counterfeit, damage versus wear, ambiguity, what the buyer meant, which conflicting record is
    true, collusion, undisclosed incentive, buyer-attributable damage). The quorum and human review
    bound them; their error rates are what H6 and the sampling audit must measure.

### A15.2 How the experiment tests the core

The experiment uses the same terms as ABS. Phase 1 on the static trap set found 0 unwanted
payments in 528 rows across four agents and four conditions (Amendment 3): a null at the ceiling,
reported as a finding. H1 is therefore tested on the harder set and the adaptive red-team arm. No
claim that the controls "were tested and found needed" is made from the static set.

| ABS element | Experiment term | What is measured | Hypothesis |
|---|---|---|---|
| Baseline agent with a payment token | C0 | Unwanted payments, trap following, violations attempted, scam checkouts, asks | Baseline |
| Hard limits and item requirements enforced before payment (A12.1) | C1 | Mandate violations executed vs C0 | H1b |
| Risk-based step-up; the Allowance approval level | C2; AL arm (Amendment 4) | Unwanted payments (under-escalation); step-ups on correct carts and false blocks (over-escalation); AL under- and over-escalation and B2B compliance | H1, H1c; AL descriptive |
| Independent monitor on a typed packet | C3 | Unwanted payments vs C0; task-success cost within 10 points | H1 (primary), H1c |
| Harder scenarios; adaptive attacker over merchant-controlled fields | H1-hard (X01 to X10); H1-redteam (G1 to G4, best of 4 rounds) | Unwanted payments per condition; attack success per agent, goal and condition | H1 on the non-static sets |
| Gate recall independent of agents | gate coverage | C1 7/24, C2 10/24 trap carts blocked, 0/22 false blocks; C3 monitor 66/72 samples, 0/66 false blocks | descriptive |
| Evidence levels (A5) | E0 to E3 on 47 cases | A1 reason-code accuracy; liable-party and remedy accuracy; calibration | H2 |
| Rules of evidence against false claims and edited listings | 13 merchant-side and 7 buyer-side adversarial cases | Fooled rate E0 vs E3 | H3 |
| Rules known to both sides at tier 1 | R1 vs R0 | Tier 1 settlement rate; fairness; false-claim filing when asked; reliance on altered evidence | H4 |
| Frozen Offer Snapshot and conformity-based liability with contestable delivery evidence (A4.1 Step 1, A5.6) | E3 vs E0, liable-party accuracy; conformity accuracy by deviation severity | Whether the frozen offer plus mixed-reliability delivery evidence lets an arbiter allocate liability correctly | H5 |
| Hybrid Decision Center A2 vs end-to-end A1 (A7) | 3 runs per case at E3 | Identical decisions across runs; liable-party accuracy (non-inferiority 10 points); errors traceable to a Finding; review rate | H6 |
| Trust attestations plus payout hold vs scams and honest new merchants (Part B1) | T0, T1, T2 on 8 trust scenarios | Scam purchases; unrecoverable loss; honest merchants avoided or blocked (10% or less); fake-badge following | H7 |
| Binding structured spec vs legacy free text (A5.4) | 16 not-as-described cases, (a) legacy vs (b) signed spec | Conformity and liable-party accuracy | secondary |
| Rail-agnostic decisions (A6) | 12 cases with the rail flipped | Share of identical decisions | secondary |
| Rail-dispute rate and time to resolution (A1.5) | all decided cases | Share that would still go to the rail; lifecycle steps | secondary |
| Rule completeness and decidability of the whole core (A3, A4, A5) | rule-completeness simulation, 524 scenarios, rule sets `scrolld.abs@0.1` and `@0.2-proposed`, author-built catalogue | Decided and correct per rule set; gaps, conflicts, contradictions; decidable share at E0 (17.4%) and E3 (100%, 2 escalations); 73 human reviews; 22 infeasible executions | not a hypothesis: a consistency measurement against the catalogue, not field data |

What the experiment does not test: real merchants under the Participation Agreement, users'
experience of approvals at scale, providers' acceptance of Step 3, the collection right, the entry
gate on real populations, and what a court or scheme would decide; the ground truth applies this
rulebook (Amendment 5). Audit 0's limitation on model families is recorded there.

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
without the gate, 45 scam cases produced 0 stopped, 31 refunded by rail reversal and 14
unrecoverable (buyer loss EUR 4,314; loss moved to acquirers, operator or provider EUR 6,139). With
the gate (attestation consulted, Mandate minimum trust 60, payout hold for merchants under 180
days or trust under 70, release on delivery evidence plus 7 days): 38 stopped before purchase, 5
refunded from held funds, 2 unrecoverable, both on instant A2A rails (buyer loss EUR 1,368). The
price: of 8 honest look-alike merchants, 4 were blocked as false positives at the minimum-trust
threshold, 1 had its payout delayed 12 days, 3 passed with a step-up. That false-positive rate is
the number to drive down first, by capping instead of refusing and by shortening probation on a
clean delivery record; it is the founder's false-declines lesson in the gate's own numbers.

### B1.2 Payout holds, not escrow

ABS holds no funds. Protection for unproven merchants is a **payout hold** by a licensed acquirer
or the merchant's PSP: the payment is authorised and captured or credited as normal; settlement to
the merchant waits for the release condition (delivery confirmed, or the conformity window elapsed
with no `not_received`, or a Decision). The Settlement Instruction states the condition
(`timing.mode: payout_hold_until_delivery`, `held_by`). An ABS-operated escrow account would be a
regulated payment service and is not part of the design.

| Rail | Hold on an unproven merchant | Reserve at Qualified | Release and return |
|---|---|---|---|
| Card | Acquirer delayed funding or reserve, as acquirers do today | Acquirer rolling reserve | Acquirer releases on the condition; returns to the buyer on a merchant-liable Decision without collection |
| A2A | The merchant's PSP holds the credited funds under its contract with the merchant and the ABS instruction | PSP reserve or direct-debit collection | PSP releases or returns by credit transfer |
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
  "$id": "urn:abs:schema:0.2:trust-attestation",
  "type": "object",
  "required": ["attestation_id", "merchant", "issued_by", "issued_at", "valid_until", "level", "status", "score", "components", "reasons", "constraints", "basis", "receipt_id"],
  "additionalProperties": false,
  "properties": {
    "attestation_id": {"type": "string"}, "merchant": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/PartyRef"}, "issued_by": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/PartyRef"},
    "issued_at": {"type": "string", "format": "date-time"}, "valid_until": {"type": "string", "format": "date-time"}, "purchase_nonce": {"type": "string"},
    "requested_value": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"},
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
                                   "reserve_pct": {"type": "number"}, "reserve_days": {"type": "integer"}, "max_purchase_value": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}, "daily_cap": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"},
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
  "$id": "urn:abs:schema:0.2:spec",
  "type": "object",
  "required": ["profile", "attributes", "status", "spec_hash"],
  "additionalProperties": false,
  "properties": {
    "profile": {"type": "object", "required": ["id", "version"], "properties": {"id": {"type": "string"}, "version": {"type": "string"}}},
    "attributes": {"type": "array", "minItems": 1, "items": {"$ref": "urn:abs:schema:0.2:attribute"}},
    "package_contents": {"type": "array", "items": {"type": "object", "required": ["item", "qty"], "properties": {"item": {"type": "string", "maxLength": 100}, "qty": {"type": "integer", "minimum": 1}}}},
    "status": {"enum": ["binding", "non_binding"]},
    "producer_spec_ref": {"type": "object", "properties": {"gtin": {"type": "string"}, "spec_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}, "publisher": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/PartyRef"}, "signature": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Signature"}}},
    "dpp_ref": {"type": "string", "format": "uri"},
    "extraction": {"type": "object", "properties": {"method": {"enum": ["merchant_entered", "producer_import", "gdsn_import", "dpp_import", "ai_extracted"]}, "model_id": {"type": "string"},
                   "source_text_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}, "confirmed_at": {"type": "string", "format": "date-time"}, "confirmed_by_kid": {"type": "string"},
                   "ambiguities": {"type": "array", "items": {"type": "string", "maxLength": 120}}}},
    "completeness": {"type": "number", "minimum": 0, "maximum": 1},
    "spec_hash": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}
  }
}
```

```json
{
  "$id": "urn:abs:schema:0.2:profile",
  "type": "object",
  "required": ["id", "version", "category", "required_attributes", "package_contents_required"],
  "properties": {
    "id": {"type": "string"}, "version": {"type": "string"}, "category": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Category"},
    "dictionary_preference": {"type": "array", "items": {"enum": ["gs1", "schema.org", "eclass", "etim", "dpp"]}},
    "required_attributes": {"type": "array", "items": {"type": "object", "required": ["name", "verification_method"],
                            "properties": {"name": {"type": "string"}, "dictionary": {"type": "object"}, "unit": {"type": "string"}, "default_tolerance": {"type": "object"}, "verification_method": {"type": "string"}, "value_enum": {"type": "array"}}}},
    "optional_attributes": {"type": "array", "items": {"type": "object"}},
    "package_contents_required": {"type": "boolean"}, "conformity_window_days": {"type": "integer", "minimum": 1},
    "withdrawal_right_default": {"enum": ["applies", "exception_custom", "exception_sealed", "exception_digital", "exception_dated_service", "not_consumer"]}
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
  "$id": "urn:abs:schema:0.2:allowance-policy",
  "type": "object",
  "required": ["policy_id", "user_ref", "principal_type", "agent_provider", "agent_ids", "currency", "limits", "rules", "tax", "autonomy", "authentication", "valid_from", "expires_at", "rulebook_version", "nonce"],
  "additionalProperties": false,
  "properties": {
    "policy_id": {"type": "string"}, "user_ref": {"type": "string"}, "principal_type": {"enum": ["consumer", "business", "public_body"]},
    "agent_provider": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/PartyRef"}, "agent_ids": {"type": "array", "minItems": 1, "items": {"type": "string"}},
    "currency": {"type": "string", "pattern": "^[A-Z]{3}$"},
    "limits": {"type": "object", "required": ["per_transaction", "daily", "weekly", "monthly", "total"],
      "properties": {"per_transaction": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}, "daily": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}, "weekly": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"},
                     "monthly": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}, "total": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"},
                     "per_category": {"type": "array", "items": {"type": "object", "required": ["category"], "properties": {"category": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Category"}, "per_transaction": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}, "monthly": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}}}},
                     "per_merchant": {"type": "array", "items": {"type": "object", "required": ["merchant_id"], "properties": {"merchant_id": {"type": "string"}, "per_transaction": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}, "monthly": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}}}},
                     "max_units_per_purchase": {"type": "integer", "minimum": 1}, "max_units_per_month": {"type": "integer", "minimum": 1}, "max_purchases_per_day": {"type": "integer", "minimum": 1}},
      "description": "hard limits: declined, never escalated"},
    "rules": {"type": "object", "required": ["allowed_categories", "blocked_categories", "min_merchant_qualification", "recurring_allowed", "cross_border_allowed"],
      "properties": {"allowed_categories": {"type": "array", "items": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Category"}}, "blocked_categories": {"type": "array", "items": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Category"}},
                     "min_merchant_qualification": {"enum": ["probation", "qualified", "established"]}, "preferred_merchants": {"type": "array", "items": {"type": "string"}}, "blocked_merchants": {"type": "array", "items": {"type": "string"}},
                     "known_merchants_only_for_autonomy": {"type": "boolean", "default": true}, "condition_allowed": {"type": "array", "items": {"type": "string"}}, "binding_spec_required": {"type": "boolean", "default": true},
                     "delivery": {"type": "object", "properties": {"countries": {"type": "array", "items": {"type": "string"}}, "max_days": {"type": "integer"}, "methods": {"type": "array", "items": {"type": "string"}}, "address_hashes_allowed": {"type": "array", "items": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Hash"}}}},
                     "returns": {"type": "object", "properties": {"min_window_days": {"type": "integer"}, "who_pays_return_accepted": {"type": "array", "items": {"type": "string"}}}},
                     "recurring_allowed": {"type": "boolean"}, "recurring": {"type": "object", "properties": {"max_per_period": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}, "max_active": {"type": "integer"}, "approval_on_first": {"type": "boolean", "default": true}, "notify_before_each": {"type": "boolean", "default": true}}},
                     "cross_border_allowed": {"type": "boolean"},
                     "delegates": {"type": "array", "items": {"type": "object", "required": ["delegate_ref", "role", "limits", "authentication"],
                                   "properties": {"delegate_ref": {"type": "string"}, "role": {"enum": ["household_member", "employee", "manager", "admin", "procurement_officer"]},
                                                  "limits": {"type": "object"}, "allowed_categories": {"type": "array"}, "approval_required_above": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"},
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
                               "properties": {"rule_id": {"type": "string"}, "when": {"type": "object", "properties": {"amount_above": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"}, "amount_at_or_below": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Money"},
                                              "new_merchant": {"type": "boolean"}, "new_category": {"type": "boolean"}, "risk_signal": {"type": "boolean"}, "cross_border": {"type": "boolean"}, "first_recurring": {"type": "boolean"}, "recurring_subsequent": {"type": "boolean"},
                                              "merchant_level_below": {"type": "string"}, "delegate_purchase": {"type": "boolean"}, "non_binding_offer": {"type": "boolean"}, "price_changed_since_view": {"type": "boolean"}, "quantity_above": {"type": "integer"},
                                              "category": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/Category"}, "merchant_id": {"type": "string"}, "blocked": {"type": "boolean"}}},
                                              "level": {"enum": ["autonomous", "notify_and_hold", "approval_required", "never"]}}}}}},
    "notifications": {"type": "object", "properties": {"channels": {"type": "array", "items": {"type": "string"}}, "on": {"type": "array", "items": {"type": "string"}}}},
    "authentication": {"$ref": "urn:abs:schema:0.2:mandate#/properties/authentication"},
    "rail_enforcement": {"type": "array", "items": {"type": "object", "required": ["psp", "controls"], "properties": {"psp": {"$ref": "urn:abs:schema:0.2:envelope#/$defs/PartyRef"}, "controls": {"type": "array", "items": {"enum": ["per_transaction_limit", "periodic_limit", "mcc_block", "merchant_allowlist", "country_block", "single_use_credential"]}}, "acknowledged_at": {"type": "string", "format": "date-time"}}}},
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
| B2B | Business policy: purchase-order reference, approval workflows (manager and procurement roles), VAT id, e-invoice required, payment terms, cost centres, spend policy; no withdrawal right | All codes; AG2 and AG5 end in `deny`; contract terms and the signed spec are the conformity reference; acceptance steps for services | Card or A2A; invoice-based payment terms allowed, with the ABS reference in remittance; reverse charge where applicable | Contract law and B2B terms; EN 16931 and Peppol; ViDA as adopted; secure corporate payment exemption for SCA; no consumer ADR constraints, but the Decision binds by contract |
| B2G public procurement | Public-body policy: framework-agreement reference, procurement thresholds and procedures outside ABS, strict Allowance (approval by authorised officers), full audit trail (chain and log), mandatory e-invoice to public bodies | AG3, AG4, AG1-M, AG1-P; AG2 and AG5 rarely arise (specifications are explicit); E3 required | A2A with ISO 20022 references; payment terms per public-sector rules | Directive 2014/55/EU on e-invoicing in public procurement (verify current status); public procurement directives and thresholds (verify); national audit rules |
| C2G and B2G fees (taxes, permits, fines) | Policy with `never` outside listed payees; approval for first payment to a body | Not a sale: conformity is "the right fee to the right body for the right reference"; wrong reference is AG1-P or AG1-M by who set it | A2A with structured reference; no chargeback; refund by the authority under administrative procedure | Administrative appeal replaces chargebacks; ABS supplies the evidence; no consumer sale law |
| C2C peer platforms | Platform acts as the ABS participant; sellers are not merchants with merchant duties; payout hold by the platform's licensed PSP; policy requires platform-attested listings | AG3 against the platform's listing attestation where it attested; otherwise the platform's own protection; AG2 and AG5 | Escrow-like hold by the licensed PSP; release on delivery; platform refund | Consumer law applies to platform duties, not to peer sellers; DSA obligations of the platform (verify scope); payment-service licensing of the hold |
| B2B2C marketplaces | Marketplace is a participant; sellers are qualified through the marketplace's trader checks (DSA Article 30 per Audit 0) reused by reference; marketplace signs offers it hosts or passes the seller's signature | Liability split: the seller for conformity and content; the marketplace where it attested, added lines or fees, or hosted content after notice; AG1-M covers marketplace-added fees | Marketplace payout hold and refund (existing holds); ABS Decision instructs the marketplace | DSA trader traceability and notice duties; consumer law for the seller; marketplace terms; Omnibus Directive on ranking and reviews (verify) |
| Agent-to-agent negotiation | Both principals hold policies; a merchant agent negotiates within the merchant's signed offer bounds; terms bind only when written into a negotiation record signed by both agents and hashed into the Offer Snapshot; seller-agent statements outside it are merchant content for Step 2 | Evidence of negotiated terms: the signed negotiation record and both agents' logs; AG3 against the snapshot; AG1-M (extended) where checkout terms are worse than the negotiation record; AG1-P against either provider for exceeding its principal's instructions; AG4 against either side's injected content | As the underlying segment | Contract formation by agents (national law; verify); the same decision order |

Simulation results per segment (v0.1 as written against v0.2, decided/correct): A2A 13/11 to
13/13; B2B 23/5 to 23/23; B2B2C 30/25 to 31/31; B2C 393/277 to 420/420; B2G 8/4 to 10/10; C2C
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
   the injection-safety and conformity-attribute profile.
4. **An agent provider or marketplace** that adopts ABS-Basic for its own agents' purchases and
   runs the Decision Center through an independent operator.

Uptake is a hypothesis until measured.

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
   the user authenticates over the exact cart; Approval Record; chain head `sha256:9f3a...`;
   Settlement Instruction on a card rail, reference `ABS:urn:abs:purchase:...:9f3a1c2e4d5b6a70`.
4. Delivery: carrier scan with weight; the user photographs the box and label; serial lookup
   matches the packing record; conformity `conforms`; the agent tells the user the withdrawal right
   runs until day 14.
5. Dispute 1: the box holds an XM5. Step 1: `model_identifier` mismatch, serial registry says XM5,
   packing photo shows XM5. AG3, merchant liable, refund with return at merchant cost. The
   merchant's "the listing said XM5" is disregarded against the countersigned snapshot.
6. Dispute 2: XM6 as offered, silver. The user says "I wanted black". Colour was not captured and
   no clarification mentioned it. Step 4: AG2, buyer; within 14 days, remedy `withdrawal`: return
   at own cost for a refund. Had `item_requirements` held `colour: black`, or had the user said
   "the black one" in a clarification, Step 3 would apply: AG1-P, the provider refunds.
7. Dispute 3: the user had added "if unsure, ask me first"; the agent chose silver without asking
   when black and silver were both in stock at the same price. Step 3: a guess where told to ask.
   AG1-P.
8. Dispute 4: conforming, black, the user changed their mind on day 20. AG5, `deny`; the 30-day
   merchant return window is still open outside ABS.

## Appendix B. Audit 0 findings and how each is resolved

| Finding | Resolution in this version |
|---|---|
| I1 Sections 6 and 7 missing; section 11 a placeholder; LANDSCAPE.md absent | Part B1 (Trust Authority) and A7 (Decision Center) written; A10 filled with the concession table, regulation mapping and standards matrix; `LANDSCAPE.md` written alongside this document; no placeholder remains |
| I2 Three answers to "authorised but wrong" | One answer everywhere, mirroring rulebook v1.2 and Amendment 5: explicit term broken -> AG1-P (provider); explicit mandate satisfied, unstated intent not -> AG2 (buyer, withdrawal overlay). Appendix A shows both sides of the line |
| I3 Neutrality contradicts the business model | A2: no party decides cases where it holds another role; an agent provider never decides disputes in which its agents can be liable; the Decision Center is an independent, accredited operator network (A7.5). The fee model is out of scope (A1.3) |
| I4 Decisive delivery evidence assumed | A5.6: contestable evidence only (carrier proof without content inspection, packing record, buyer photos with metadata, serial lookup, digital log, return inspection); H5 tests conformity on mixed-reliability evidence |
| I5 Phase 1 null at the ceiling | A15.2 states the null as a finding; H1 is tested on H1-hard and H1-redteam; no claim that the controls were found necessary |
| I6 Arbiters graded against the author's rules; same model families | A15.2 and A7.8 record both limitations as Amendment 5 does; the ground truth applies this rulebook, not a court's |
| I7 36 vs 40 cases; hypothesis numbering; KPI without baseline; unmapped standards list | 47 cases (case set v2) and H1 to H7 per Amendment 2 used throughout; A1.5 gives baselines from the EBA/ECB and marketplace practice; every standard named is mapped to a requirement in A10.3 |
| Q1 Three-quarters rebuilt existing work | Recast as a profile layered on AP2/FIDO, UCP/ACP, TAP/Agent Pay, acquirer underwriting and scheme monitoring (A10.1); the Mandate and Snapshot are profiles (A5.2); ABS's contribution limited to the six items in "What ABS is" |
| Q1 Visa 4.1.23.10 and Amex | A4.2 positions Step 4 as agreeing with Visa and Step 3 as a contract over the scheme rule; Amex noted as the issuer-protection model ABS can serve |
| Q2 Adoption; vehicle; first adopter | B5: dispute profile plus benchmark; Wero (UNVERIFIED), issuer or wallet, FIDO and EMVCo channels; uptake stated as hypothesis |
| Q3 "Never allow scammers in" false; "only protection on A2A" false; KPI not ambitious | B1.1 restates the target and the defensible claim; A1.3 and B1.1 drop both overclaims; A1.5 compares against the EEA baseline; threat model B1.7 includes bust-out, takeover, synthetic companies, laundering, honest insolvency, counterfeits, fake badges, payer-side manipulation |
| Q4 Conformity narrower than law; agent cannot accept deviations; withdrawal makes goods cases moot; no delivery evidence; AG4 sabotage; cross-border law | A4.3 "without prejudice" and `accepted_deviations`; A4.4 withdrawal overlay in every Decision and in the flows; A1.1 and B2.3 prioritise no-withdrawal categories; A5.6 evidence; A4.2 AG4 note and open question; A3.2 decisions do not bind consumers; A10.2 consumer-law row |
| Q4 Providers will not accept AG2 as written | Step 3 limited to provable fault, capped and insurable (A4.2, A6.4 `liability_cap`); AG2 on the buyer |
| Q5 "Humans only for escalations"; AI Act high-risk; GDPR Art. 22; ADR finality; Menime dependency | A7: human review on request for any party; designed as Annex III 8(a) high-risk with the obligations listed; Art. 22(3) built in; decisions bind participants by contract only; plain-language explanation per case; Menime as reference implementation, the pattern normative |
| Q5 Escrow and collection are regulated | B1.2 and A6: payout holds and collection through licensed PSPs and acquirers; ABS holds nothing |
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
| ABS-P2 spoofed Register | 5 | A4.1 standing; A6.1 guarantee |
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
| ABS-5.5 single track | process | A6.1 |
| ABS-5.6 enforcement | process | A6.1 |
| ABS-6.5a Decision Center; 6.6 appeal; 6.7 repeat; 6.8 merchant claim; 6.9 statutory rights; D1 default on silence | process | A3.2, A3.3, A7.3 |
| ABS-8 data retention and PCI | process | A5.9 |
| ABS-2.5 contract formation; 2.6 idempotency; 2.7 negotiation record; 1.5b responding party | process | A3.2; Offer Snapshot and Purchase Record schemas; Participation Agreement |
| ABS-9 enforcement layer | process | A4.1 Step 3; A12.1 |
| ABS-1.7 / 1.8 trust attestation and entry gate (roadmap) | roadmap | B1 |

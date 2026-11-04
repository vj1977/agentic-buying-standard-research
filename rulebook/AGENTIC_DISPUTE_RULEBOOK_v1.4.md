# Agentic Dispute Rulebook v1.4 (current core, research simulation)

Frozen 2026-11-04 after Audit 1 (findings F10, F11, F12). The machine-readable form is
`AGENTIC_DISPUTE_RULEBOOK_v1.4.json`; the reference engine `acs/rule_engine.py` applies it with
`decide(..., rulebook="1.4")`. It matches ABS v0.3: A4 (liability order), A4.4 (withdrawal
overlay) and A6 (settlement), with the reading of A4.1 Step 3 given in section 3 below.

**No model has been run under v1.4.** Every Phase 1-3 result was produced under v1.2 (and v1.3
for the capture-duty arm) and stays reported under that rulebook. `rulebook/VERSIONS.md` maps each
result to the rulebook it used. v1.2 (`AGENTIC_DISPUTE_RULEBOOK.md`/`.json`) and v1.3
(`AGENTIC_DISPUTE_RULEBOOK_v1.3.json`) are kept unchanged as history.

## Changes from v1.2 and v1.3

| Topic | v1.2 (and v1.3) | v1.4 |
|---|---|---|
| What binds the agent | Only encoded, machine-readable fields; "free-text intent is context, not a term"; a wish said only in chat binds nobody | A term captured in the signed Mandate, machine-readable or as signed text the user confirmed (the instruction text shown at the confirmation tap, or a clarification answered with authentication): AG1-P when broken. Only a machine-readable term is a *hard limit* |
| Stated but not captured | v1.2: AG2 (buyer). v1.3: AG1-C (agent provider) | A requirement about the purchase said only in the conversation, or in a clarification answered without authentication: AG1-C (agent provider), Step 3b, after AG1-P; the provider bears the loss when it cannot produce the conversation record (ABS-E1) |
| Never stated | AG2 (buyer) | AG2 (buyer) |
| Authorisation | not modelled | Step 0, AG0: referred to the payer's PSP; a provider-issued charge without a valid Mandate is the provider's; a merchant re-presenting the credential or charging after expiry is the merchant's |
| Deceptive offer content | not modelled | AG4-D (merchant), between AG4 and AG1-M |
| Withdrawal: digital content | always excluded once delivered | excluded only where prior express consent, acknowledgement of the loss of the right and the trader's confirmation are all recorded (CRD Art 16(m)); missing = unresolved |
| Withdrawal: scope and dates | not checked; a negative delivery-to-dispute interval counted as "within 14 days" | consumer, EU distance contract; valid dates with the dispute not before delivery; business buyer: no right; anything missing: unresolved |
| Missing prerequisite | treated as "not available" (deny) | `undetermined`: liability decided, remedy escalated to a human; never deny |
| Card settlement | "reversal against the merchant through the card network's chargeback mechanism" | merchant refund to the card; if unpaid, contractual collection and the buyer's own issuer-raised dispute (ABS cannot raise one) |
| A2A settlement | merchant pushes a refund; recall implied as the rail route | new credit transfer by the liable party; no recall or return as an ABS mechanism; a refusing merchant is reached only by contractual collection |
| Tier 1 | buyer and merchant only | the agent provider is a required party whenever AG1-P or AG1-C is alleged |

## 1. Participation

Merchants and agent providers accept the rules by taking part; buyers and their agents see them
before buying. A participant cannot opt out of a single dispute. Offers to agents are structured
records; text that instructs an agent is rejected at publication. The agent provider is a party,
and a required party at tier 1 whenever the dispute alleges an agent error (AG1-P or AG1-C).

## 2. Evidence

| Level | Contents |
|---|---|
| E0 | Card-dispute data: amount, merchant name and descriptor, date, item titles, the buyer's claim, the merchant's reply. |
| E1 | E0 plus the signed Mandate. |
| E2 | E1 plus the agent's action log, the buyer's clarifications and the user-agent conversation that produced the Mandate. |
| E3 | E2 plus the frozen Offer Snapshot, page snapshots, the cart with who added each line, the hash-chain check against an independently held payment anchor, and contestable delivery evidence. |

Delivery evidence is contestable and weighed. A non-conformity finding must not rest only on
party-authored evidence that no independent record corroborates (provenance gate); otherwise the
case goes to review. A broken chain, or a displayed record that differs from the chained one,
counts against the party that kept the records.

## 3. What binds: terms, hard limits, stated and unstated intent

As in ABS v0.3 A4.1 Step 3 ("What binds as an explicit term", normative):

- **Terms (Step 3, AG1-P).** A requirement binds only if it is captured in the signed Mandate or
  the Allowance Policy, in one of two forms: (1) machine-readable, a hard limit or other Mandate
  field, or a captured item requirement; (2) signed text the user confirmed, the instruction text
  shown verbatim at the confirmation tap (the Mandate's `intent_hash`), or a clarification the user
  answered with an authentication reference, which amends the Mandate ("new, not refurbished",
  "in white", "only at a genuine discount", "if unsure, ask me first" bind in this form when they
  appear in that text). Breaking either form is AG1-P.
- **Hard limits.** Only a machine-readable term is a hard limit, checked deterministically before
  payment. A signed text term binds equally for liability and is checked after the fact.
- **Stated but not captured (Step 3b, AG1-C).** Text said only in the conversation, or in a
  clarification answered without authentication, is not a term. If it stated a requirement about
  the purchase (what, from whom, at what price, by when, in what condition) that the agent should
  have captured, and the purchase misses it, the failure is AG1-C. A preference the user left open
  ("ideally black, any colour is fine") is not such a requirement.
- **Never stated (Step 4, AG2).** What the user meant without saying stays with the user.

The audit found the earlier A4.1 wording ambiguous ("natural-language term" against "encoded
limit"); `results/AUDIT1_CORRECTIONS_PHASE1_2.md` (F10) records the ambiguity and how it was
resolved.

## 4. Decision order (first rule that fires decides the component)

Precedence: AG0, ABS-C1, AG3, AG4, AG4-D, AG1-M, ABS-X1, ABS-F1, AG1-P, AG1-C, AG2, AG5.

| Step | Code | Liable | Remedy | Test |
|---|---|---|---|---|
| 0 | AG0 | payer's PSP process (rail); provider if its systems charged without a valid Mandate; merchant if it re-presented the credential or charged after expiry | refer to the payer's PSP, or refund by the liable participant | The Mandate was not created by the account holder with PSP-performed strong authentication, or the charge was not initiated under it. Unauthorised-in-law is the PSP's question (PSD2 Arts 64, 72-74). |
| 1 | AG3 | merchant | refund | Delivery does not conform to the frozen offer (model, specs, colour, condition, quantity, accessories, images, price or fees, delivery terms), including non-delivery and counterfeits. |
| 2 | AG4 | merchant | refund | The agent followed instructions in merchant-controlled or hosted content. |
| 2 | AG4-D | merchant | refund of the difference against the best conforming offer seen, or of the affected item | A statement of fact in merchant content is shown false (reference price never charged, false scarcity, invented urgency, endorsements) and the log shows it influenced the choice. |
| 2 | AG1-M | merchant | refund | The merchant added or pre-selected items or fees, or the snapshot is worse than the signed feed record the agent relied on. |
| 3 | AG1-P | agent provider | refund | The agent broke an explicit term (section 3), or guessed where told to ask. |
| 3b | AG1-C | agent provider | refund | Capture failure: a stated requirement was not captured and the purchase misses it; no conversation record produced: decided against the provider (ABS-E1). |
| 4 | AG2 | buyer | withdrawal / deny / undetermined | Fits every explicit term, no stated requirement uncaptured, not what the buyer meant and never said. |
| 4 | AG5 | buyer | withdrawal / deny / undetermined | User error, change of mind, or a claim the evidence contradicts. |

The reference engine fails safe: any finding a step needs that is unknown gives `review`. It does
not execute standing, conduct, construction, collusion, feed-signature or apportionment rules
(listed in the JSON under `not_executed_by_the_reference_engine`).

## 4a. Statutory withdrawal right (overlay)

For goods sold at a distance to an EU consumer, the buyer may withdraw within 14 days from the
day the consumer acquires physical possession (Directive 2011/83/EU, Art 9(2)(b)). The overlay is
**available** only when every prerequisite is established and no exception applies, **not
available** when an exception applies, the buyer is a business, or the window has passed, and
**unresolved** otherwise:

- **Scope.** The buyer is a consumer and the contract an EU distance contract. A business buyer
  has no right. Another jurisdiction is unresolved (national law).
- **Dates.** `delivered_on` and the dispute date are valid ISO dates and the dispute is not before
  delivery. A missing or invalid date, or a negative interval, is unresolved.
- **Exceptions.** Custom goods (Art 16(c)); sealed hygiene goods unsealed after delivery (16(e));
  sealed audio, video or software unsealed after delivery (16(i)); date-specific accommodation,
  transport of goods, car rental, catering or leisure (16(l)); and digital content not on a
  tangible medium once performance has begun **only where** the consumer gave prior express
  consent, acknowledged the loss of the right **and** the trader provided the confirmation
  (16(m)). If any of the three is recorded false the exception does not apply; if any is missing
  the overlay is unresolved. Passenger transport is outside the directive (Art 3(3)(k)).
- **Missing prerequisite.** Remedy `undetermined`: liability is decided, the remedy goes to a human
  before any Settlement Instruction issues. It is never converted to `deny`.

For AG2 and AG5 the remedy is `withdrawal` when the right is available, `deny` when it is not, and
`undetermined` when it is unresolved. For AG0 (participant liable), AG3, AG4, AG4-D, AG1-M, AG1-P
and AG1-C the remedy is a refund by the liable party and the right is moot.

Not stated by ABS v0.3 and therefore not modelled: the period start for digital content and
services (Art 9(2)(a), (c)), the Art 16(a) performed-services exception and the Art 10 extension
when the trader failed to inform.

## 5. Settlement (rail-agnostic; ABS never moves money)

A Decision becomes a Settlement Instruction naming an existing mechanism. Four recovery routes are
distinguished, and the analysis code uses the same names:

| Route | Meaning |
|---|---|
| `abs_refund` | The liable party pays the instruction: merchant refund to the card or a new credit transfer; an agent provider's push-to-card credit (sponsored originator) or credit transfer; the withdrawal refund. |
| `contractual_collection` | An unpaid instruction is collected under the Participation Agreement by the licensed PSP or acquirer as creditor in its own licence (direct debit mandate, reserve, guarantee, netting), or is owed to the buyer directly. The only tool against a refusing merchant on push A2A rails. |
| `issuer_dispute` | Card rails only: the buyer's own card dispute, raised by the issuer at the cardholder's request within the scheme deadline; the Decision Center cannot raise one and supplies the Decision and Package as evidence. |
| `unavailable` | No rail route: push A2A after an ABS outcome that wronged the buyer, or a vanished payee with no payee-side hold and nothing to collect. The buyer keeps statutory routes and the courts. |

Recall and return messages (camt.056, pacs.004, camt.029) are the payer PSP's tools for duplicate
sending, technical error or fraud and are not ABS mechanisms; SCT Inst has no return. A Decision
refund is set off against any later rail recovery so the buyer is made whole once. ABS never
requires a waiver or an assignment of a rail right.

## 6. Lifecycle and conduct

As in ABS v0.3 A3.2: dispute within 60 days; response within 10 (silence: ABS-D1); tier-1
settlement with the agent provider at the table for AG1-P and AG1-C; escalation within 10 days;
Decision within 30 days; human review on request within 10 days; one appeal on new evidence or a
procedural error; the scheme deadline guard; pay within 10 days. Knowingly false or altered
evidence decides the dispute against its submitter (ABS-C1). Agents on either side do not carry
out an instruction to deceive.

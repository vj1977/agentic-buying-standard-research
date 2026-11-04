# Agentic Dispute Rulebook (v1.2, research simulation)

> **v1.3 (capture duty)** lives in `AGENTIC_DISPUTE_RULEBOOK_v1.3.json`: it adds AG1-C (a requirement the user stated but the agent did not
> capture into the mandate, liable party the agent provider). It was used only in the secondary capture-duty arm
> preregistered in Amendment 10 (`results/PREREGISTRATION.md`). Every primary analysis uses v1.2 below.

These rules cover purchases that an AI agent makes for a buyer. They extend the existing dispute
lifecycle that buyers and merchants already know from wallets and card schemes (dispute,
response, escalation, final decision). They do not create a separate system. They are written
as general principles and cite no scheme rule numbers. The machine-readable form is
`AGENTIC_DISPUTE_RULEBOOK.json`. The simulation and the arbiter prompt are built from that file.

Changes in v1.2 (after Audit 0 and the governor's liability decision):
- One liability rule, decided by how precise the mandate is. The agent provider is liable only
  when the agent broke an explicit, machine-readable term captured in the signed mandate or
  Allowance Policy. Otherwise the buyer bears the outcome, and the statutory
  withdrawal right stays intact.
- Delivery evidence is contestable. There is no inspection that is assumed to be infallible.
- The statutory withdrawal right sits on top of every decision.

Changes in v1.1: conformity to the frozen offer became the first decision step; settlement
became rail-agnostic; participation came to require machine-readable offers.

## 1. Participation means accepting the rules

1.1 A merchant that accepts agent-initiated purchases agrees to these rules before it sells
anything. This works the way accepting a wallet or card brand binds a merchant to that
programme's dispute rules today. A merchant cannot opt out for one dispute.

1.2 Before any purchase, the buyer and the buyer's agent are shown these rules: what can be
disputed, how, within which time limits, and who decides. The merchant and any agent acting
for the merchant are shown the same rules.

1.3 **Machine-readable offers.** A participating merchant publishes every offer to agents as a
structured record. The record holds the price, delivery cost, total landed cost (every
mandatory fee included), stock, delivery terms, return terms, structured product attributes,
image descriptors, and a flag that the merchant accepts these rules. The record follows a
validated schema: free-text fields are bounded, and text that instructs an agent is rejected
at publication. Agents compare merchants on these records. The record shown at checkout is
the offer.

1.4 The agent provider is the operator of the buyer's agent. It takes part as the party liable
for its agent acting outside the mandate.

## 2. The mandate and the frozen offer

2.1 Every agent purchase is paid with a credential bound to a mandate that the buyer signed. The
mandate holds the buyer's intent in their own words, the maximum total, the permitted
categories, any merchant rules, the maximum units, and an expiry. Clarifications the buyer gave
the agent during the task are part of the record.

2.2 At checkout the exact offer is frozen and kept in the hash-chained record:
- structured attributes (brand, model, condition, colour, key specifications, included
  accessories, quantity);
- the description;
- image descriptors;
- the price charged;
- delivery terms and return terms.

## 3. Evidence

| Level | Contents |
|---|---|
| E0 | What a card dispute has today: amount, merchant name and statement descriptor, date, item titles, the buyer's claim, and the merchant's reply with any attachments. |
| E1 | E0 plus the signed mandate. |
| E2 | E1 plus the agent's action log: every action, the agent's stated reason, and the result status. |
| E3 | E2 plus the frozen offer snapshot at checkout, page snapshots at view time, the cart at checkout with who added each line, a hash chain over these records anchored in the payment authorisation, and the delivery evidence (see 3.2). |

3.2 Delivery evidence is contestable and is weighed, not presumed. It can include:
- the carrier's proof of delivery (status, date, signature, parcel weight; the carrier does not
  inspect the contents);
- the merchant's packing record (self-serving);
- the buyer's photos with metadata (these can be manipulated);
- a manufacturer serial-number registry lookup, where one exists;
- a digital delivery log for digital goods;
- a return inspection.

Any of these can be missing or can conflict with another.

Records in a valid hash chain (mandate, action log, snapshots, cart, offer) are presumed accurate. A merchant statement about its offer that
does not match the frozen offer is disregarded, because post-purchase edits do not count. A
broken chain counts against the party that kept the records. Where evidence is missing, the
decision rests on the balance of probabilities and states its confidence.

## 4. Decision order (applied by the arbiter, in this order)

**Step 1. Conformity.** Compare what was delivered with the frozen offer: model, specifications,
colour, condition, quantity, included accessories, appearance against the image descriptors,
price charged, and delivery within the stated terms. Weigh the delivery evidence for
consistency: serial numbers against the registry and the packing record, photo metadata against
the delivery date, parcel weight against the item. Non-delivery and counterfeit goods do not
conform. If the delivery does not conform, the **merchant** is liable, whatever the agent did.
Reason code **AG3, Non-conformity**. Remedy: refund; non-conforming goods are returned at the
merchant's cost.

**Step 2. Manipulative offer.** The delivery conforms, but the purchase was caused by the
merchant's own offer. Either the agent followed instructions embedded in content the merchant
controls or hosts (listing text, reviews it hosts, merchant profile), or the merchant added or
pre-selected items or fees the agent did not choose. The **merchant** is liable.
- **AG4, Injection via merchant content.**
- **AG1-M, Merchant-added items.**

Remedy: refund of the affected items.

**Step 3. Agent breach of an explicit mandate term.** The delivery conforms and the offer was not
manipulative, but the agent broke an explicit, machine-readable term of the signed mandate or
the Allowance Policy:
- a hard limit: amount, category, merchant rule, units, expiry, or a required approval or
  notification;
- an item requirement captured in the mandate: condition, colour, model, capacity or spec,
  size, region or plug, minimum discount;
- a captured "clarify if ambiguous" flag.

The **agent provider** is liable. Reason code **AG1-P**. Remedy: refund by the agent provider.
Free-text intent is context, not a term. A wish the buyer said only in chat and that was not
captured in the mandate does not bind the agent provider. The precision of the mandate
decides.

**Step 4. Buyer side.** The delivery conforms, the offer was not manipulative, and the agent
followed every explicit term. The **buyer** bears the outcome, and the dispute gives no remedy:
- **AG2, Authorised but wrong**: the purchase meets every explicit mandate term but not what the
  buyer wanted and did not capture (said only in chat, or never said);
- **AG5, User error, change of mind, or friendly fraud**: including claims the evidence
  contradicts.

The statutory withdrawal right still applies (section 4a).

## 4a. Statutory withdrawal right (overlay)

Consumer law applies whatever the dispute decides. For goods sold at a distance to a consumer
in the EU, the buyer may withdraw within 14 days of delivery without giving a reason, returning
the goods at their own cost unless the merchant agreed otherwise. Exceptions modelled here:
- digital content (for example gift card codes) once delivery has started with the consumer's
  consent;
- goods made to the consumer's specification (custom goods).

The decision states whether the withdrawal right is available. For a buyer-side outcome (AG2,
AG5), the remedy is "withdrawal" when the right is available and has not expired, and "deny"
otherwise. For AG3, AG4, AG1-M and AG1-P the remedy is a refund by the liable party.

## 5. Settlement is rail-agnostic

5.1 These rules sit above the payment rail. A decision produces a settlement instruction: the
type (refund, refund on withdrawal, or no refund), the amount, who bears the cost, and whether
goods go back. The instruction is executed on whatever rail carried the payment.

5.2 On card rails the instruction can use the existing reversal (chargeback) mechanism against
the merchant's acquirer. On account-to-account and instant payment rails (instant credit
transfers and similar), a push payment is generally final and the rail offers no chargeback.
There, the merchant (or the agent provider) executes the refund as a new push payment, as it
undertook to do when it joined the programme. Participation (1.1) is what makes the
instruction enforceable on these rails. The decision itself does not depend on the rail.

## 6. Lifecycle

6.1 **Dispute.** The buyer, or the buyer's agent with the buyer's consent, files within 60 days of
the transaction (or of the latest promised delivery date). The filing names a reason code, the
disputed items and amount, the remedy requested, and the evidence relied on. A buyer's agent
must not file a claim it knows is false.

6.2 **Response.** Within 10 days the merchant answers with its evidence and one offer: full refund,
return and refund, partial refund, or deny. A merchant must not present an offer other than the
frozen one.

6.3 **Settlement (tier 1).** If the buyer accepts the offer, the dispute closes with a settlement
instruction on the payment's rail. A settlement obtained by a false claim or false evidence can
be reopened.

6.4 **Escalation (tier 2).** Either party may escalate to the neutral arbiter within 10 days of
the response, or when no response arrives.

6.5 **Final decision.** The arbiter applies the decision order in section 4 to the evidence
package. It records its conformity finding, reason code, liable party, remedy, confidence and a
short rationale, states whether the withdrawal right is available, and issues the settlement
instruction. The decision is final within the
programme.

## 7. Conduct

7.1 Neither side may submit evidence it knows is false or altered. Doing so decides the dispute
against that side.

7.2 Agents on either side represent their principal. They do not carry out a principal's
instruction to deceive.

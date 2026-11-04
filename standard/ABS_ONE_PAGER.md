# Agentic Buying Standard (ABS). One page.

Vadims Juruss. Draft v0.3, 4 November 2026. Not published.

## The problem

Most of what goes wrong in an agent purchase already has a card dispute code: the goods did not
arrive, were not as described, or the amount was wrong. No code covers a purchase that was
authorised and delivered as offered but is not what the user asked the agent to buy, because the
agent broke an instruction the user confirmed or never recorded a requirement the user stated. That is the gap:
faithful execution of delegated purchasing intent. The card networks put an in-mandate agent
action on the cardholder, and the key evidence, the user's instruction to the agent, sits with the
AI provider, outside the scheme rules. One issuer has announced protection for agent error on US
cards. Nobody offers an open, rail-neutral way to decide that line from evidence, across issuers,
acquirers and bank rails. That is what ABS is.

## What ABS is

The dispute, evidence and liability profile for agentic commerce. It is designed to sit on what
exists: AP2 mandates (now at FIDO), UCP and ACP catalogues, Visa and Mastercard agent identity,
acquirer underwriting, the card dispute lifecycle and ISO 20022 bank messages. It adds the part they
leave open. The bindings to those protocols are proposed, not yet implemented or tested.

## The core

1. **A dispute taxonomy for agent purchases.** Non-conformity. Injection or deception in merchant
   content. Merchant-added items. Agent fault on the record. Capture failure. Authorised but wrong.
   User error or false claim. Merchant-performance claims keep the categories issuers and
   merchants use today; only the instruction and capture disputes get codes of their own.
2. **One liability rule: the precision of the mandate decides.** Delivery did not match the frozen
   offer: the merchant pays. The merchant steered the agent: the merchant pays. The agent broke a
   term captured in the signed mandate (a limit, a requirement such as colour or capacity, or an
   instruction the user confirmed), or guessed where told to ask: the agent provider pays. The user
   said it and the agent failed to capture it: the agent provider pays. The agent did exactly what
   was said but not what was meant and never said: the user bears it and keeps the 14-day
   withdrawal right. The agent proposes the mandate from the conversation; the user confirms with
   one tap. The burden of precision is on the system.
3. **A minimum evidence standard.** Every purchase carries a signed package: the mandate digest, the
   approval record, the offer frozen at checkout with its binding attributes and countersigned by
   the merchant, the agent's signed trace chain, whose full hash is committed with the payment and
   located by the payment reference, and contestable delivery evidence. Four levels, E0 to E3. The
   snapshot outranks a later edit; a missing record counts against whoever had to keep it; false
   evidence loses. Every item records who issued it, their stake, when it was committed, who has
   held it and which facts it can prove. A finding that moves liability needs a record with
   authority for that fact; one party's own photos or text never suffice, and a signature proves
   who signed, not that it is true. An optimising liar fooled the AI arbiters in 12 and 14 of 14
   cases with staged photos; a registry record and a carrier weight held out against one arbiter on
   two cases, and the other arbiter was fooled even with them in front of it. A gate built on that
   finding, compared within the same calls, cut the liar's success from 11 and 12 of 14 to 1 of 14,
   mostly by refusing decisions it could not check, and sent almost half of the ordinary caseload to
   a human, mostly buyers who were right; so findings must now cite records in a structured form,
   the cited record must say what the finding says, and review rates are published per party. A
   gate that reads the cited record let 0 of 14 through on the stored attacks, but it was written
   after seeing them and has not met a fresh attacker.
4. **Decision Center governance.** Models find facts and cite the evidence. Deterministic,
   versioned rules decide. Every decision carries a signed receipt with the rule path and a plain
   explanation; anyone can recompute it. Any party can get a human review; a person decides for
   anyone who does not consent to an automated one. Decisions bind merchants and agent providers by
   contract; consumers keep every statutory route and every card dispute right, which ABS never
   asks them to waive. A network of independent nodes and a transparency log is proposed, not
   built. Designed against the EU AI Act's high-risk rules, the GDPR and ADR law; not certified
   against them.
5. **Settlement on existing rails, nothing invented.** A merchant refund, a new credit transfer
   with the case reference, a payout release or return. No bank message reverses a transfer against
   a merchant that refuses; the remedy is the collection right it signed, run by a licensed bank or
   acquirer. On cards the cardholder may still ask the issuer for a chargeback; ABS supplies the
   evidence and guards the deadline. Unproven merchants are paid after delivery where a licensed
   acquirer or collecting PSP is the payee. ABS holds no money and never pays or collects.
6. **Agent conformance at scale.** We do not trust the agent. We enforce at the credential, the
   checkout and the bank, where no agent can reach. Registered providers, signed requests, an open
   test suite with certification levels, a reference MCP toolkit, and monitoring per agent version.

## What the experiment found

A simulated shop, small n; which analyses were pre-registered and which are exploratory is
recorded per analysis. On ordinary and scripted-adversarial disputes evidence is the lever: with
card-dispute data alone, two frontier arbiters allocated liability correctly in 82 and 61 percent
of 51 cases; with the full package, 98 and 96 percent (scored against the experiment's rulebook,
not yet the current one). Disputes whose recovery would still depend on the buyer's own card
dispute or a collection fell from 14 and 41 percent to 4. Optimised fabrication of a party's own
evidence then defeated both arbiters even with the full package, and at an equal attack budget the
hybrid arbiter was not significantly harder to fool (10 of 14 against 6 of 14). The hybrid was more
auditable, not more accurate, and a strict fail-safe sent half the cases to humans: thresholds must
be calibrated. Two model families erred together more often than independence predicts (1.24 times
under the strict rule, 2.45 under a relaxed rule chosen afterwards): a quorum is defence in depth,
not a guarantee. Frontier
agents resisted every trap; an older agent followed planted text in 4 of 20 cases and the mandate
gate stopped all four with no false block. Negotiating agents did not lie; showing them the rulebook
raised fairness from 78 to 96 percent. One gap found and fixed: the agent provider must be a party
when its agent is blamed. Against a 528-scenario catalogue the rules reach a determinate outcome
in 526 cases and send 2 to a human, consistent with the catalogue's stipulated judgements in all
528; that is a consistency check on our own catalogue and its stipulated facts, not field data.

## What we ask of each party

Merchant: accept the rules, sign the binding attributes of each offer, countersign the snapshot,
answer in ten days. Agent provider: register, propose and capture the mandate, enforce it, freeze
the offer, keep the trace, carry liability for provable fault, certify the agent. Bank or acquirer:
carry a reference and keep the full hash it points to, hold a payout where you are the payee,
collect under the mandate you hold. Rail:
nothing new.

Roadmap, informative only: qualified merchants and a trust authority, a full product-data
standard, tax and segment profiles, and an adoption path through an instant-payment scheme's
purchase protection.

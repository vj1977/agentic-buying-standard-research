# Agent dispute codes: how they become possible, and who confirms the agent broke the instruction

Status: design note for ABS v0.3, 2026-11-04. Informative. Its normative part is ABS v0.3 A4.5,
and its adoption part is B6. It answers two questions the founder asked on 2026-11-04
(the author's private notes). Every fact about a scheme, ISO or EPC process is cited in
section 10 with its access date. Anything not confirmed on a primary source is marked UNVERIFIED.
Nothing here has been discussed with a scheme, an issuer or a standards body. Timelines are
estimates.

## For the founder: five lines

1. The code comes last. In an instruction dispute the merchant performed, so a chargeback would
   hit the wrong party. The evidence must travel first, then claims are routed, then a code with
   a liability flow to the agent provider.
2. The stages:
   - Stage 0: a contractual programme, now.
   - Stage 1: the mandate digest and agent ID in card data, on the Compelling Evidence pattern.
   - Stage 2: a narrow merchant remedy and sub-reasons.
   - Stage 3: formal codes through the schemes, ISO 20022 and the EPC (effect 2030 at the
     earliest).
3. Yours to start: pilot terms; a free EMVCo comment; an ISO 20022 code request (any
   organisation, quarterly, next by 31 Dec 2026); an EPC change request (by 30 Apr 2028). The
   schemes' rules move only through their clients: your issuer network.
4. Who confirms machine-readable terms: nobody needs to be trusted. A public rule compares the
   user-signed mandate with the merchant-signed cart and the authorisation, and the issuer can run
   it at intake. Visa already obliges the provider to hand the issuer the instruction on request.
5. Text terms and chat-only requirements: the records are committed before the dispute, and a
   neutral Decision Center reads them, with typed citations and human review. The provider can
   lose by not producing records but never wins on its own word, with one narrow exception: its
   anchored action log can show that its agent followed injected or deceptive content the merchant
   signed, which moves the loss to the merchant, and only if no other record contradicts it (ABS
   A4.5, A5.7 test (c), B6).

## 1. The two questions

The first question is about governance: who owns dispute codes, and what sequence of asks could
bring agent disputes into them. The second is about evidence: for each kind of agent dispute,
which fact decides it, which record proves that fact, and who can check the record without being
trusted. The two depend on each other. A scheme will adopt a code only if the deciding fact can be
established cheaply, without a judgement the scheme then has to defend.

## 2. Why the code is the last step, not the first

Visa defines a dispute as "A Transaction that an Issuer returns to an Acquirer". Every existing
condition names a failure on the merchant's side of that return: no authorisation, a bad
authorisation, a processing error, or a merchant that did not perform (Visa 10.1–13.9;
Mastercard 4837, 4834, 4853; Amex C08, C31, C32, F29). An instruction dispute (AG1-P) or a capture
dispute (AG1-C) fits none of them. The payment was authorised under a mandate, and the merchant
delivered the cart the agent ordered. The fault is the agent provider's, and the provider is not
on the acquiring side. Visa makes the cardholder "responsible for any actions taken by an Agentic
Payment Provider ... as if the Cardholder initiated the Transaction" (4.1.23.10).

A new code alone would return to the merchant's acquirer a loss the merchant did not cause. The
honest order is:

1. **Carry the evidence.** The issuer sees that an agent bought, under which mandate, for which
   cart.
2. **Route.** Agent-fault claims stop being misfiled against a merchant that performed.
3. **Add a code only with a liability flow to the agent provider.** That flow is the hard part.

Visa has the hook for step 3 but not the flow. An agentic payment provider registers "with Visa,
directly or via an Agentic Payment Enabler" (4.1.23.2). It is not a member-sponsored agent, Visa
issues its identifier and may disqualify it (4.1.23.11), and no acquirer or issuer stands behind it
in the dispute chain. American Express can move first because it is issuer and acquirer for its own
US cards. It has announced protection from "AI agent error" for registered agents, with terms
pending.

On account-to-account rails the rulebooks leave disputes over the underlying contract outside the
scheme. A recall covers only a duplicate, a technical error or fraud. A customer-reason recall
needs the beneficiary's consent, and SCT Inst has no return. An "agent dispute" R-code has nothing
to attach to there. A data element and a recall reason can attach.

## 3. Who owns dispute codes today, and how they change

| Body | What it owns | How it changes | Who may propose | Pace observed | Agent content today |
|---|---|---|---|---|---|
| **Visa** | Conditions 10.1–13.9 in four categories (fraud, authorisation, processing errors, consumer disputes); Compelling Evidence | "Visa may amend ... the Visa Rules at any time" (1.1.1.5). Each edition lists a Summary of Changes, effective on publication unless dated (ID# 0020315). Editions of 18 Apr and 24 Oct 2026 | Visa alone; no public comment process found | Compelling Evidence 3.0: FAQ March 2023, effective 15 Apr 2023. Agentic rules (4.1.23) added Apr 2026; agentic login ID in Compelling Evidence for disputes from 24 Oct 2026 | No agent condition. A provider login ID is one matching element for 10.4. The provider keeps the instruction and must "provide it to the Cardholder or Issuer upon written request" (4.1.23.3) |
| **Mastercard** | Message reason codes in the Chargeback Guide | Bulletins and announcements to customers, not public | Mastercard and its customers | First-Party Trust announced 23 Oct 2023, US rollout 2024, with reject code 5002 | Guidance: "Standard ... chargeback rights ... apply to agentic transactions". Agent metadata and "consumer intent data" travel with agentic tokens |
| **American Express** | Its own codes | Amex alone, as issuer and acquirer | Amex | Protection announced; terms pending | Covers a purchase that "deviates from the Card Member-authenticated purchase intent" |
| **ISO 8583** | ISO 8583:2023, replacing parts 1 to 3; ISO/TC 68/SC 9. Values "are provided by the ISO 8583 maintenance agency" (AFNOR) | No public code-request procedure found. The 1998 procedure ran through a national member body as sponsor | A national standards body | Not known | None. Schemes define dispute codes themselves (UNVERIFIED on a primary source) |
| **ISO 20022** | Chargeback messages cain.027 and cain.028 (V04) and retrieval messages, from TC 68/SC 9/TG1. The reason is a 4-digit ISO 8583 code; the condition is free text. No card-dispute code set exists; ExternalRePresentmentReason1Code covers the acquirer side | Messages: yearly cycle, requests by 1 June, publication April/May of the next year. Code sets: quarterly, requests by end Dec/Mar/Jun/Sep, publication end Feb/May/Aug/Nov | Messages: "Actual or potential users". Code sets: "organisation(s), group(s) of users, regulator(s)", with a Cards domain | About three months for a code value; about two years for a message change | None |
| **EPC** | SCT, SCT Inst and SDD rulebooks and their R-transactions | Change request, a 90-day public consultation, then a decision by the Payment Scheme Management Board; a cycle at least every two years | "any individual or organisation that is able to claim a legitimate interest", on template EPC064-24 by email; every request is published | 2026-cycle rulebooks published Q2 2027. Next deadline 30 Apr 2028; consultation Sep–Dec 2028; effect Nov 2030 | None. An SCT Inst beneficiary-initiated repayment was recommended in 2026 (final decision UNVERIFIED) |

## 4. What the agent frameworks already carry

| Framework | What the user authorises | What reaches the network or issuer | Dispute use stated |
|---|---|---|---|
| **Google AP2 v0.2** (at FIDO) | Checkout Mandate (open: constraints; closed: the merchant-signed `checkout_jwt`) and Payment Mandate. v0.1 named them Intent, Cart and Payment mandates | Payment Mandate (`transaction_id` = hash of the merchant-signed checkout; payee; amount; instrument; risk data), verified by the credential provider, the network and the merchant's processor | A "Dispute Evidence" section with verification steps; how it is used in dispute resolution is "outside the scope" |
| **Mastercard Verifiable Intent** (draft v0.1, at FIDO) | Layers from credential provider to user, user to agent, agent to network or merchant | `transaction_id` equals `checkout_hash` | "Out of scope: ... dispute resolution" |
| **Mastercard Agent Pay** | Agentic token, Payment Passkeys | "metadata identifying the certified agent"; "Consumer intent data flows alongside payment credentials" | Standard chargeback rights |
| **Visa Intelligent Commerce** | A passkey-consented instruction: `declineThreshold`, `effectiveUntilTime`, preferred merchant | Instructions held by Visa; agent order data sent to Visa by API, not in the authorisation | Instructions are "Required to evidence the specific authorized transaction for disputes" |
| **Visa Trusted Agent Protocol** | None (agent identity only) | Signatures from agent to merchant; nothing reaches the issuer | None |
| **EMVCo Agentic Payments Framework** (draft, Sep 2026) | "Intent Services" to "register, reference, retrieve and manage consumer-authorised intent before, during and after a transaction" | "data fields for registering intent"; Know Your Agent and "Agentic Transaction Indicators" named as possible future work | Not addressed |

The evidence is being built, and each scheme keeps it in its own system. Visa's instruction holds
no item attributes, and those decide most instruction disputes. What is missing is an
interoperable reference an issuer can use at intake. AP2's `transaction_id` and Verifiable Intent's
`checkout_hash` already hash the merchant-signed checkout. ABS's proposed `mandate_digest` adds the
user-side hash.

## 5. The staged adoption path

| Stage | What changes | Who must agree | Route | Timeline (estimate) | What persuades |
|---|---|---|---|---|---|
| **0. Contractual programme** | ABS decides before and beside the rail. The liable party refunds by a new credit; rail rights are untouched (no waiver, Visa ID# 0008771) | Participants only: merchants, agent providers, optionally an issuer or wallet | Participation Agreement (ABS A6.4) | 6–12 months to a pilot | The measured E0-to-E3 results. The pilot must produce the loss data no one has published: dispute rate, share misfiled as fraud or not-as-described, cost per case |
| **1. Evidence data elements, no new code** | An agent indicator, the registered provider's ID, the mandate digest, the checkout hash and the ABS locator in authorisation and dispute data, on the Compelling Evidence 3.0 and First-Party Trust pattern | Each scheme; EMVCo for a common definition; FIDO for the mandate credential | EMVCo comment and membership; the FIDO Payments working group; scheme teams via issuer and acquirer clients | 12–24 months. Past dispute-data changes took effect about six months to a year after a scheme decided | In the rule simulation (stipulated findings), E1 makes the amount, merchant, units, expiry and currency breaches determinate (A5.1). Without the mandate, arbiters put agent breaches on the buyer in 13 of 20 decisions. Liable-party accuracy rose from 82% and 61% at E0 to 98% and 96% at E3 (A4.2) |
| **2. Sub-condition under existing categories** | (i) A narrow merchant remedy: when the checkout matches the user-authenticated instruction, a claim that the agent broke the instruction (an AG1-type claim misfiled against the merchant) fails against the merchant and goes to the provider's programme. The match never defeats a non-conformity, non-delivery or fraud claim: conformity is decided first (ABS A4.1 Step 1), and whether the payment was authorised stays the payer's PSP's question (Step 0; Audit 2 PAY-04). (ii) AG4 and AG1-M as sub-reasons where the merchant is liable. (iii) An issuer flag that routes AG1 claims to the provider's programme | Each scheme | Scheme rules; for (i), an ISO 20022 representment-reason value | 2–3 years | Stage 1 data; Stage 0 misfiling and loss rates |
| **3. Formal codes and a liability flow** | A scheme condition with the registered agent provider as the liable party; an agent-evidence block in cain.027 and cain.028; EPC recall reasons and references, not a dispute process | Schemes; the ISO 20022 RA with TC 68/SC 9/TG1; the EPC | Scheme rules; an RA change request; EPC change management | 3–5 years; EPC effect Nov 2030 at the earliest | Stage 2 volumes; a scheme's decision to make registered providers financially answerable |

Stage 0 can already use Visa 4.1.23.3: a participating issuer can ask the provider in writing for
the cardholder's instruction. Stage 1 fits EMVCo's Intent Services, which "reference" and
"retrieve" intent after the transaction; its release names "Agentic Transaction Indicators" as
possible future work. Stage 3 is the first stage that needs a new liability flow. In cards that is
plausible because Visa already registers and can disqualify providers directly. In SEPA the
realistic asks are narrow: a request-for-recall reason meaning "error by the payer's agent" (the
beneficiary's consent is still required), and the ABS case reference in the SCT Inst repayment
procedure, if that procedure is adopted.

**What the founder can start personally.**

1. **Now:** Stage 0 pilot terms, for one agent provider and a few merchants, or for an issuer or
   wallet that wants Amex-style protection.
2. **Now:** an open data-element proposal with test fixtures (A5.2.1 item 5), filed as a public
   comment on EMVCo's next agentic draft. Review is free. The "New Initiative" associate tier
   costs USD 15,000 a year and lists Agentic Commerce.
3. **By 31 Dec 2026:** a request to the ISO 20022 Registration Authority for an
   ExternalRePresentmentReason1Code value, "purchase matched the user-authenticated agent
   instruction". If approved it is published end Feb 2027. Its value depends on schemes using
   cain.027 (UNVERIFIED).
4. **By 1 Jun 2027:** a message change request for an agent-evidence block in cain.027 and
   cain.028, developed with TC 68/SC 9/TG1, for publication in April or May 2028.
5. **By 30 Apr 2028:** an EPC change request (EPC064-24) for the recall reason and the repayment
   reference.
6. **TC 68:** Latvia was not a member in the last readable list (2023). Ask LVS to take part, or
   work through another national body.
7. **Visa and Mastercard:** there is no public route. Go through issuer and acquirer clients.

## 6. Who confirms: the principle

A dispute turns on one deciding fact. "Who confirms" therefore depends on three things:

- which fact decides the case;
- which record has authority for that fact (ABS A5.7);
- whether that record was committed before the dispute arose.

Phase 3 set the constraint. An optimising dishonest party that rewrote only its own submissions
fooled one AI judge on 12 of 14 case-sides and the other on 14 of 14, and signed records did not
stop the second (`results/PHASE3_ATTACKS.md`). Reading two stories and choosing can be optimised
against. ABS therefore confirms in this order:

1. **Recompute.** A fact that is a comparison of signed, structured records is computed by a
   public rule. Every verifier gets the same answer.
2. **Read a committed record.** A fact that needs a reading of words is read only from records
   committed before the dispute, by a party with no stake. The reading is a typed Finding with a
   machine-checkable citation, and any party may ask for a human review.
3. **Infer against the keeper.** A party that had to keep a record and cannot produce it has the
   question decided against it (ABS-E1).

A narrative states what is contested. It is never evidence of the deciding fact.

### 6.1 Confirmation matrix, part 1: the record

| Dispute type | Deciding fact | Record that proves it | Issuer and stake | Committed | Held by |
|---|---|---|---|---|---|
| **AG1-P, machine-readable term** (model, colour, condition, price cap, merchant rule, autonomy level) | A captured term is outside what was bought | User-signed Mandate; merchant-signed cart (countersigned Offer Snapshot); the authorisation; the Approval Record if autonomy is at issue | The user and the provider co-sign the Mandate, which binds both to what was asked. The merchant's signature binds it to what it sold. The issuer has no stake between user and provider | Mandate before checkout; cart at checkout; both under the head anchored at payment (A5.8) | Provider (chain); user (Mandate); merchant (cart); payer's PSP (authorisation, anchored head, the digest once carried) |
| **AG1-P, signed text term** ("new, not refurbished" in the confirmed text; an authenticated clarification) | The purchase contradicts text the user confirmed | Text matching `intent_hash` inside `shown_terms_hash`; clarifications with `user_auth_reference`; the cart | The user's words, signed by the user and co-signed by the provider, which has a stake | At the confirmation tap | Provider; a user-side copy (proposed, 7.1) |
| **AG1-C, said in chat, not captured** | Before signing, the user stated an explicit requirement that the Mandate omits | The conversation record whose `conversation_hash` the user signed inside the Mandate; `template_profile` | The user's words, recorded by the liable provider: the record binds the provider and never helps it | At Mandate signing; anchored at payment | Provider; a user-side copy (proposed) |
| **AG2, intent never stated** | An absence: every term met, nothing stated left uncaptured | All of the above | As above | As above | As above |
| **AG1-M, AG4, AG4-D: merchant manipulation, injection or deceptive content** | The merchant added a line or a fee; the terms are worse than the record compared on; merchant text instructed the agent and the agent obeyed; a statement of fact in merchant content (reference price, stock, time limit, endorsement) was false and influenced the choice | Merchant-signed cart (`added_by`), feed record and snapshot with its `UntrustedText`; for AG4-D, the reference price or stock record against the content; the anchored action log for causation | The merchant (the record binds it). The provider for causation, with a stake: AG4 and AG4-D move the loss to the merchant | At checkout; the log anchored at payment | Merchant; provider |
| **AG3: non-conformity, including non-delivery** | What arrived, against the snapshot; handover | Carrier scans and weight; a registry binding of the serial at dispatch; an independent inspection; the packing record, used against the merchant | Carrier, registry and inspector: no stake. Merchant: stake | Dispatch and scans before the dispute; the inspection commissioned after it | Carrier; registry; inspector; merchant |

### 6.2 Confirmation matrix, part 2: who confirms

| Dispute type | Who verifies or recomputes | Who decides | If the record is missing | Attack surface (Phase 3 lessons) |
|---|---|---|---|---|
| **AG1-P, machine-readable** | Anyone with the records and the registered keys. An issuer can already get the instruction from a Visa-registered provider on written request (4.1.23.3) and recompute at intake once it holds the records. Once the digest travels (Stage 1), it can check that the records it obtains are the ones committed at purchase; the digest does not supply them. Before payment, the provider's own check (C1) | Nobody: a published rule (A4.1 Step 3). The Center records the result; a human review checks the computation | The provider cannot produce the Mandate or the chain: decided against it (ABS-E1) | A swapped Mandate fails the signature and the anchored head. "Midnight" for "black" needs dictionary-coded attributes, else `review`. No narrative enters, so optimised prose has nothing to act on |
| **AG1-P, text** | Anyone can check the text against its hash. Whether the cart breaks the text is a reading | The Decision Center: a typed `intent_match` Finding citing the text span and the cart field, content-checked; human review | No text matching `intent_hash`: ABS-E1 | A substituted text fails the hash. The fooled judges read party prose, so the reading is confined to the committed text and signed cart fields. Capture shrinks this row: a term that maps to an attribute becomes an item requirement |
| **AG1-C** | Anyone can check the transcript against `conversation_hash`. Whether a turn is a requirement or an open preference is a reading | The Decision Center: `requirement_stated_not_captured`, citing the turn; human review | Not produced, or not matching: ABS-E1, so AG1-C | Later edits fail the hash. Omissions before commitment, where the provider records both ends, are caught only by an independent user-side copy. An invented turn cannot be cited. Phase 2: 48 of 48 on typed capture cases; no optimised attack run here |
| **AG2** | The terms by recomputation; the transcript by the reading above | The issuer can close a claim at intake when only a captured term is alleged and none is broken. Otherwise the Center | No transcript: AG2 cannot be shown, so the case is AG1-C | In Phase 3 false buyer claims moved to non-conformity with staged photos; that claim goes to the AG3 row |
| **AG1-M, AG4, AG4-D** | Added lines and prices: anyone, by rule. Injection and deceptive content: the text is in the merchant-signed snapshot; for AG4-D its falsity is read against the reference price or stock record; causation rests on the provider's log | A rule for lines and prices. The Center for "this text instructs an agent", for "this claim is false" and for causation | No snapshot: against the merchant (ABS-E1m). No log: no causation, so the case is AG1-P | A provider may cry "injection" to escape AG1-P: its log counts only if nothing contradicts it (A5.7 test (c)) and the text is in what the merchant signed |
| **AG3** | Weight and registry: by rule. Inspection: a reader without a stake | The rail process (the issuer's consumer dispute) or the Center behind the A5.7 gate | ABS-E1m; no handover proof means not received | Staged photos and serial-mismatch reversals fooled end-to-end judges; registry and weight records resisted one judge, not the other. An independent record must support the contested attribute itself |

AG0 (no valid mandate) is not in the matrix. Whether a payment is unauthorised is decided by the
payer's PSP under PSD2 Arts 64 and 72 to 74 and the scheme rules; ABS supplies records.

## 7. The candidate mechanisms

| Mechanism | Confirms | Confirmer's stake | For | Against | Regulatory fit | Maps to |
|---|---|---|---|---|---|---|
| **(a) Deterministic recomputation by anyone** | AG1-P machine terms; AG1-M; the term half of AG2 | None: arithmetic over signatures | No trust; same answer everywhere; no AI to persuade; cheap at intake | Only structured captured terms; needs shared dictionaries; the issuer holds no mandate today (Stage 1) | Existing intake practice; hashes until a dispute; the Compelling Evidence pattern | AP2 checkout and payment mandates; Verifiable Intent; network instructions; EMVCo Intent Services |
| **(b) Issuer as mandate holder** | What the user authenticated, independently of the provider | None between user and provider. Adverse to the provider where the issuer insures agent error (the Amex model) | Independent custody; SCA and an app that shows terms before signing already exist | Set-up SCA is not dynamic linking for later purchases (PSD2 Art 97(2); RTS Art 5(1)); an issuer screen shows terms, not a conversation; agents may hold several issuers' cards | Fits as SCA for a remote action that carries a risk of abuse (Art 97(1)(c)). EBA Q&A 2018_4031 subjects a remote mandate set-up to SCA. PSR Art 52 spending limits at the PSP, as proposed. Does not fit as SCA for each autonomous purchase, and treating those purchases as merchant-initiated is doubtful | Agentic tokens with issuer controls; EMV 3-D Secure. A network-held variant exists: Visa Intelligent Commerce keeps passkey-consented instructions, holding only an amount ceiling, an expiry and a merchant |
| **(c) Conversation commitment** | Whether a requirement was stated in the chat | The record is the liable party's own: it binds the provider and never helps it | Makes AG1-C decidable; later edits fail the hash; withholding loses the case | The provider controls recording before commitment; private content; still needs a reading | Disclosed only in a case, and only to those who need it (GDPR minimisation, A5.9) | None today; ABS's `conversation_hash` |
| **(d) Neutral Decision Center, for interpretive cases only** | Text terms; requirement against preference; injection | None (A2 neutrality) | Handles the residue rules cannot: typed Findings, citations, content check, human review | Judgement remains, and Phase 3 shows submissions steer judges, so inputs are confined to committed records; cost; governance | Designed against the AI Act as high-risk, with human review and GDPR Art 22 safeguards (A7) | ADR; scheme arbitration as the analogue |
| **(e) Must not confirm alone** | — | The agent provider (liable in AG1); the merchant; either side's narrative; an AI judge reading party submissions; the issuer on interpretive questions (no transcript, and a stake where it insures agent error) | — | — | A party's own record binds it and never proves a fact in its favour (A5.7), with one exception: the provider's anchored action log may prove causation in Step 2, that its agent followed injected text or relied on a deceptive claim in content the merchant signed, which moves the loss to the merchant (AG4, AG4-D; A5.7 test (c)). The log then counts only for what the agent did, only if no signed or independent record contradicts it, and never for what the user asked or what arrived | — |

### 7.1 Two details that make (a) and (c) work

- **The digest must travel.** The issuer can recompute only if the transaction carries two
  hashes: one of the user-signed Mandate (or of the credential that commits to it, A5.2.1), and
  one of the merchant-signed cart. ABS already commits the chain head in the payer's PSP record
  (A5.8). The proposed `mandate_digest` names the Mandate directly, so the issuer does not need
  the chain. The hashes authenticate the records; they do not supply them. The issuer still has to
  obtain the Mandate and the cart and hold the registered keys (A4.5).
- **A user-side copy, disclosed by parts (proposed).** The conversation is committed turn by turn:
  a salted hash per turn, a root over the turns, and the turn count. One turn can then be
  disclosed with proof that it belongs to the whole, and the whole goes only to the Center. The
  user's client keeps the shown terms and the transcript. That copy is independent only where the
  client is not the provider's software, for example a wallet, a browser or an operating-system
  agent.

## 8. The cleanest answer, and its limits

**Nobody needs to be trusted for machine-readable terms.** The user's signed mandate, the
merchant's signed cart and the issuer's authorisation are compared by a public rule. Whoever holds
the three records gets the same answer, first of all the issuer at dispute intake. For text terms
and requirements said only in chat, the records are fixed by commitment before the dispute, and
only their reading goes to a neutral Decision Center. The agent provider can lose by failing to
produce its records, but it never wins on its own word. The one exception is narrow: its anchored
action log can establish that its agent followed injected or deceptive content the merchant signed
(A5.7 test (c)), and only when no signed or independent record contradicts it.

Its limits:

1. **Only what was captured can be recomputed.** The burden moves to capture (A4.1). A vague
   mandate leaves the loss with its author: the provider for what was said in chat and not
   captured, the user for what was never said.
2. **The issuer sees no mandate today.** Until Stage 1, recomputation runs at the Center or at a
   participating wallet.
3. **Confirmation is not recovery.** An issuer that confirms AG1-P cannot charge it back to a
   merchant that performed. The loss reaches the provider by contract until a scheme builds a
   liability flow (Stage 3).
4. **A signature proves display, not understanding.** A browser-rendered confirmation such as W3C
   Secure Payment Confirmation guarantees that the payee, amount and instrument were displayed. It
   does not guarantee the item terms. Consumer law may also limit how far a one-tap confirmation
   binds a consumer (A8.4).
5. **Capture before commitment is the provider's,** unless the user-side copy is independent.
6. **Collusion before the dispute passes recomputation.** A merchant and a provider that sign a
   consistent false cart produce a clean comparison. The case then turns on delivery evidence
   (AG3) and the collusion rule (ABS-X1).
7. **The interpretive residue is real.** Its bounds are designed. The refined gate is not yet
   measured (A5.7).
8. **SCA is separate.** An issuer-held mandate authenticates the set-up, not each purchase.

## 9. What changed in ABS v0.3

- **A4.5 (normative), "Who confirms the deciding fact".** It sets four routes: recomputed, read
  from a committed record, adverse inference, and rail process. It names who never confirms alone
  and gives the short-form matrix.
- **The Decision's `confirmation_route`** records the route used.
- **The Settlement Instruction's `abs_binding.mandate_digest` (PROPOSED)** carries the Mandate's
  full hash, optionally the snapshot hash, and where the digest travels. It stays `not_carried`
  until a scheme or rail defines a field.
- **B6 (informative)** gives the adoption path in short form.
- **A10.1** records Visa 4.1.23.2 and 4.1.23.3 and AP2 v0.2's Dispute Evidence section. A10.1
  and A15.1 item 11 point to B6, and the change log has an entry.

No experiment was run. The numbers quoted are ABS's existing results, within their stated limits.

## 10. Sources

All sources were read on 2026-11-04. Where a live site refused scripted access (HTTP 401 or 403),
the page was read from a web.archive.org capture of the live page, with the capture date in the
URL.

| Source | URL | Status |
|---|---|---|
| Visa Core Rules and Visa Product and Service Rules, 24 Oct 2026: conditions; Compelling Evidence for 10.4; 1.1.1.5; 4.1.23.2, .3, .8, .10, .11; ID# 0008771, 0020315, 0025920 | https://usa.visa.com/dam/VCOM/download/about-visa/visa-rules-public.pdf | Verified |
| Visa Dispute Management Guide for Merchants (the four categories) | https://usa.visa.com/dam/VCOM/global/support-legal/documents/merchants-dispute-management-guidelines.pdf | Verified |
| Visa Compelling Evidence 3.0 acquirer FAQ, March 2023 | https://usa.visa.com/content/dam/VCOM/regional/na/us/Solutions/pps/evolution-of-compelling-evidence-acquirer-faq.pdf | Verified |
| Visa Claims Resolution: the name and the April 2018 launch | The Visa brochure URL returned HTTP 404 | UNVERIFIED (the categories are verified above) |
| Visa Intelligent Commerce: concepts, capability page, press release of 30 Apr 2025 | https://developer.visa.com/docs/visa-intelligent-commerce/concepts ; https://developer.visa.com/capabilities/visa-intelligent-commerce ; https://usa.visa.com/about-visa/newsroom/press-releases.releaseId.21361.html | Verified |
| Visa Trusted Agent Protocol | https://github.com/visa/trusted-agent-protocol ; https://developer.visa.com/docs/trusted-agent-protocol/trusted-agent-protocol-specifications | Verified |
| Mastercard Chargeback Guide, Merchant Edition, 13 May 2025 | https://www.mastercard.us/content/dam/public/mastercardcom/na/global-site/documents/chargeback-guide.pdf | Verified (plain fetch returned HTTP 403; read with browser headers). The rules page returned HTTP 403 |
| Mastercard First-Party Trust press release, 23 Oct 2023 | https://newsroom.mastercard.com/news/press/2023/october/mastercard-targets-friendly-fraud-to-protect-small-businesses-and-merchants | Verified |
| Mastercard agentic commerce guide (developer guidance, not rules) | https://developer.mastercard.com/merchant-cloud/documentation/tutorials-and-guides/agentic-commerce-guide/21/index.md (the original URL returned HTTP 401) | Partly verified; no data-element numbers |
| Mastercard Verifiable Intent, draft v0.1 | https://github.com/agent-intent/verifiable-intent | Verified |
| American Express agentic commerce page; dispute reference guide (2019) | https://www.americanexpress.com/en-us/company/agentic-commerce/ ; https://www.americanexpress.com/content/dam/amex/us/merchant/pdf/US-Disputes-Reference-Guide-Updated.pdf | Page verified, terms pending; guide partly verified (it is not the Merchant Regulations) |
| Google AP2 specification v0.2 | https://raw.githubusercontent.com/google-agentic-commerce/AP2/main/docs/ap2/specification.md | Verified |
| EMVCo framework release, 1 Sep 2026; Q3 2026 newsletter; participation costs | https://www.emvco.com/news-publications/emvco-requests-feedback-on-framework-for-secure-interoperable-and-scalable-card-based-agentic-payments/ ; https://www.emvco.com/news-publications/emvco-newsletter-q3-2026/ ; https://www.emvco.com/join-us/participation-agreements-costs/ | Verified; no final framework yet |
| FIDO Alliance announcement, 28 Apr 2026; membership levels | https://fidoalliance.org/fido-alliance-to-develop-standards-for-trusted-ai-agent-interactions/ ; https://fidoalliance.org/members/membership-benefits/ | Verified; working-group rights per level are inferred |
| ISO 8583:2023; ISO/TC 68/SC 9; ISO maintenance agencies | https://web.archive.org/web/20261026174638/https://www.iso.org/standard/79451.html ; https://web.archive.org/web/20260308022116/https://www.iso.org/committee/6534831.html ; https://web.archive.org/web/20261025162003/https://www.iso.org/maintenance_agencies.html | Verified (archived; the live site returned HTTP 403) |
| ISO 20022 message catalogue (cain.027, cain.028) | https://web.archive.org/web/20261001070437/https://www.iso20022.org/iso-20022-message-definitions | Verified (archived). Production use by schemes is UNVERIFIED |
| ISO 20022 external code sets; request form; maintenance process | https://web.archive.org/web/20261003094352/https://www.iso20022.org/catalogue/additional-content-messages/external-code-sets ; https://web.archive.org/web/20260308072105/https://www.iso20022.org/iso-20022-request-updates-external-code-sets ; https://web.archive.org/web/20260113161508/https://www.iso20022.org/iso-20022-standard-maintenance-process | Verified (archived) |
| EPC SCT Rulebook 2025 v1.2, with the Payment Scheme Management Rules | https://www.europeanpaymentscouncil.eu/sites/default/files/kb/file/2026-09/EPC125-05%202025%20SCT%20Rulebook%20version%201.2.pdf | Verified |
| EPC SCT Inst and SDD Core rulebooks 2025 v1.2; the 2026 consultation EPC009-26 | https://www.europeanpaymentscouncil.eu/sites/default/files/kb/file/2026-09/EPC004-16%202025%20SCT%20Instant%20Rulebook%20v1.2.pdf ; https://www.europeanpaymentscouncil.eu/sites/default/files/kb/file/2026-09/EPC016-06%202025%20SDD%20Core%20Rulebook%20version%201.2.pdf ; https://www.europeanpaymentscouncil.eu/sites/default/files/kb/file/2026-03/EPC009-26%20SCT%20Inst%20Scheme%20Rulebook%20-%20Public%20Consultation%20Document%20on%202026%20Change%20Requests.pdf | Verified. The final decision on the SCT Inst repayment is UNVERIFIED |
| EPC evolution of the schemes (cycle dates); change request template EPC064-24 | https://web.archive.org/web/20261006185330/https://www.europeanpaymentscouncil.eu/what-we-do/epc-payment-scheme-management/evolution-schemes ; https://web.archive.org/web/20250803044444/https://www.europeanpaymentscouncil.eu/document-library/other/template-propose-change-epc-payment-scheme-rulebooks | Verified (archived) |
| ISO TC 68 participants; the LVS register entry for ISO/TC 68/SC 9 | https://web.archive.org/web/20230416080340/https://www.iso.org/committee/49650.html?view=participation ; https://www.lvs.lv/lv/committees/13548 | Partly verified; Latvia's current status in TC 68 is UNVERIFIED |
| PSD2, the SCA RTS, EBA Q&A 2018_4031 | Audit 2 sources S1, S2 and S4 (`audits/AUDIT_2_REGULATORY.md`) | Verified by Audit 2 the same day; EUR-Lex refused scripted access for this note |
| W3C Secure Payment Confirmation | https://www.w3.org/TR/secure-payment-confirmation/ | Verified: Candidate Recommendation Draft, 13 Oct 2026; the browser must show payee, amount and instrument |

Also UNVERIFIED:

- any public channel through which Visa or Mastercard take outside proposals;
- the announcement date of Compelling Evidence 3.0;
- the meaning of field 25 in the 1993 and 2003 editions of ISO 8583;
- published loss data on agent disputes (none found);
- any EPC, EBA or ECB publication on agentic payments (none found in one search).

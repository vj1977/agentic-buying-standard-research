# Audit 0: the thesis of the Agentic Buying Standard (ABS)

Independent audit, 2026-11-04. The auditor wrote none of the ABS documents and did not take part in the
experiment. Read-only: no file was changed except this one, and nobody was contacted.

**What was read:** four private documents of the author (notes, a research-proposal draft, an application draft and a
business note; not in this repository and redacted below where quoted),
`standard/ABS_v0.1.md` (all 1,378 lines), `rulebook/AGENTIC_DISPUTE_RULEBOOK.md` and `.json` (v1.1),
`results/PREREGISTRATION.md` (with Amendment 1 and Deviation 1), `results/pilot_summary.md`,
`results/main_summary.md`, `results/gate_coverage.md`, and samples of `data/heldout/`.
`standard/LANDSCAPE.md` does not exist; `standard/scenarios/` and `standard/sim/` are empty.

**How external claims are marked:** every external claim has a URL and a date. "Accessed 2026-11-04"
means the page was read on that date. **UNVERIFIED** means it could not be confirmed from a primary or
reputable source.

## Verdict

1. As a whole standard, ABS will not be adopted. About three-quarters of it rebuilds what AP2 (now at FIDO), UCP and ACP, Visa TAP, Mastercard Agent Pay and acquirer underwriting already provide.
2. The one valuable part nobody else has is the dispute layer: agent reason codes, the decision order, rules of evidence and a measured minimum evidence standard. Put everything there.
3. "Never allow scammers in" is false. Withdraw it, and claim instead that unproven merchants are not paid before delivery and the buyer is made whole.
4. "Conformity decides" is the right instinct but incomplete. It has no delivery evidence, it is narrower than consumer law, it is aimed at goods the 14-day withdrawal already covers, and the documents give three answers on "authorised but wrong", where Visa says cardholder and Amex says issuer.
5. [redacted: private application material]

## Scorecard

| Dimension | Score (1–5) | One-line reason |
|---|---|---|
| Novelty | 2 | Mandates, signed checkouts, agent identity, merchant KYB, holds and two-tier resolution all exist. New: agent dispute codes, the four-way decision order, and measuring which evidence decides. |
| Feasibility | 2 (standard) / 4 (research) | The standard needs participation agreements from every party, licensed escrow and a carrier inspection that does not exist. The benchmark is doable now. |
| Adoption likelihood | 1 (whole standard) / 3 (dispute module via an existing body) | Nobody gains enough from the whole. Wero, FIDO and EMVCo are open to a well-evidenced dispute module now. |
| Safety-research relevance | 2 as framed / 4 if refocused | KYB, escrow and rails are not safety. An AI arbiter judging an AI agent under adversarial evidence is unstudied scalable oversight. |
| Regulatory risk (5 = highest) | 4 | AI Act high-risk (Annex III 8(a)); GDPR Art. 22; ADR finality; a payment licence for escrow and collection; consumer law overriding the conformity and liability rules. |

---

## 0. Findings inside the documents (before any outside comparison)

These need no web source; each can be checked in the repository.

**I1. The normative core of the headline goal is missing.** ABS v0.1 sends the reader to section 6
(Merchant Trust Authority, qualification, attestation, expulsion) and section 7 (Decision Center) at
least ten times, for example lines 18–19, 44, 56–58, 98, 116–119, 278, 550 and 602. Neither section
exists: the file goes from 5.4 straight to 8. Section 11 ("How ABS relates to existing protocols") holds
only the literal string `ABS_SECTION_9_PLACEHOLDER`, and the `LANDSCAPE.md` it cites does not exist. So
the stated first goal of the standard ("only qualified merchants"), its anti-scam claim and its decision
centre have no normative text. A reviewer will see this at once.

**I2. The central question has three different answers.** The question that motivates the whole project
is the founder's own: "Who pays when the agent is wrong? Not fraudulent. Wrong. The agent had
permission. It stayed inside the spending limit." That is reason code AG2, "authorised but wrong".

| Document | Who bears AG2 (conforming delivery, inside the hard limits, not what the user meant) |
|---|---|
| Rulebook v1.1, `.md` section 4 step 4 and `.json` `reason_codes.AG2` | **Buyer.** Remedy: deny. |
| ABS v0.1 section 5.1 Rule 3 and the 5.2 table | **Agent provider.** Remedy: return and refund; the provider pays return costs and any shortfall. |
| Two private drafts (a research proposal and an application; quotes redacted) | One implies the agent provider, the other the buyer. |
| Pre-registration, Amendment 1 | Buyer ("'authorised but wrong' and change of mind are denied"). |

The pre-registered Phase 2 grades arbiters against the rulebook, so it grades "the buyer pays" as
correct. That is the status quo. As written, the experiment does not test the standard's own liability
rule, and the rulebook's answer to the founder's question is "nobody new pays".

**I3. Neutrality contradicts the business model.** ABS section 2 says a party "MUST NOT act as arbiter
in a case where it holds any other role". Section 12.1 [and a private business note, redacted] propose the founder's
preferred model: the agent-provider platform runs the arbiter and takes a fee. An agent provider that is
liable under AG1-P and AG2 would then decide its own liability.

**I4. The decisive evidence is assumed, not produced.** Rulebook E3 and Amendment 1 give the arbiter "the
delivery record (structured attributes of what arrived, from the carrier's delivery inspection)" and "a
signed carrier inspection". Parcel carriers do not open parcels and record the model, colour and
condition of the contents. The nearest real practice is Flipkart's Open Box Delivery, where the courier
opens the box in front of the buyer, the buyer can refuse it at the door, and returns are then mostly
barred. It covers only selected products and places, and it checks identity and transit damage, not
whether the product works ([Flipkart terms](https://flipkart.com/pages/obd-tnc), accessed 2026-11-04). With
an infallible record of what arrived, H4 (conformity is decided better at E3 than at E0) is close to
true by construction. The hard real-world part, proving what was in the box when buyer and merchant
disagree, is assumed away.

**I5. Phase 1 found no effect.** `results/main_summary.md` covers 132 root episodes, four agents
(claude-fable-5-1, claude-haiku-5-5, claude-opus-5-5, grok-4.7) and four conditions, 528 rows. There were
0 unwanted payments in every condition (each cell 0/33, Wilson 95% CI [0, 10]) and 100% task success. The
pilot of 45 roots also hit the ceiling. So H1 (controls cut unwanted payments) cannot be supported, and
the data show no problem for C1–C3 to solve. Likely causes: blatant traps (the H02 merchant profile
literally says "NOTICE TO AUTOMATED BUYING AGENTS"; H01 is a "customer note forwarded by support"); short
episodes (about 6 steps) through a typed tool API, not a live web page; and scam merchants whose risk
fields (age, rating, verified flag) are honest, while real scams fake exactly those fields. Reporting this
as null is correct and to his credit. But the proposal cannot then say the "safety-critical parts" were
tested with frontier agents and found to need ABS.

**I6. The arbiters are graded against the author's own rules.** Ground truth for the Phase 2 cases is
written by the person who wrote the rulebook. That measures whether an arbiter follows these rules, not
whether the rules are fair, lawful or what a court or scheme would decide. The arbiters
(claude-fable-5-1, grok-4.7, tie-break claude-opus-5-5) come from the same families as the buying
agents. The founder's own rule is that the reviewer comes from a different family.

**I7. Smaller inconsistencies.** [Redacted: a count in a private draft] differs from Amendment 1's 40. The
hypotheses are numbered differently across the documents (the proposal flags this itself). The 1.5 KPI
"scam loss rate below 0.05% by value" is not compared with any baseline. [Redacted: a remark on a standards list in private drafts.]

**What is strong, stated fairly.** The decision order puts each loss on the party best placed to prevent
it, the "least-cost avoider" idea from law and economics. The merchant controls conformity and its own
content. The agent provider controls mandate enforcement, which is deterministic in C1, so AG1-P should
cost it almost nothing. The user controls how clearly the intent is stated. The typed offer schema, with
`UntrustedText` fields and a monitor that sees only a typed packet, is a sound injection defence. The
research hygiene is the best asset in the folder: pre-registration, k/n with intervals, a harness defect
logged as Deviation 1 and re-run, and a null result reported as null. Measuring honest merchants wrongly
refused, not only scammers caught, is the right instinct from false declines.

---

## Q1. Prior art and overlap

**Most load-bearing fact (primary text, checked by the auditor).** The Visa Core Rules, 24 October 2026
edition, section 4.1.23.10 "Agentic Payment Provider – Cardholder Responsibility" (ID# 0031176, last
updated Apr 2026), says: *"A Cardholder is responsible for any actions taken by an Agentic Payment
Provider as part of an Agentic Transaction as if the Cardholder initiated the Transaction."*

Before any agentic transaction, section 4.1.23.3 requires the provider to:
- obtain consent to a "Cardholder-defined payment instruction";
- state its expiry;
- verify the cardholder's identity;
- "obtain Cardholder acknowledgement that they are responsible for actions taken by the Agentic Payment
  Provider".

Section 4.1.23.4 requires the provider to "use only the Cardholder-defined criteria". Section 4.1.23.6
lets the provider accept a merchant's limited refund policy on the cardholder's behalf. Section 4.1.23.8
requires an order confirmation for 120 days. A merchant "must not require a Cardholder to waive the right
to dispute a Transaction, including an Agentic Transaction" (ID# 0008771). In the dispute chapter,
"agentic" appears only where an agentic login ID counts as Compelling Evidence; there is no agent dispute
condition
([visa-rules-public.pdf](https://usa.visa.com/dam/VCOM/download/about-visa/visa-rules-public.pdf),
downloaded and searched 2026-11-04). **The largest network has therefore already answered "who pays for
an in-mandate agent action": the cardholder, as far as the network is concerned.** ABS has to argue
against this, not ignore it.

| ABS component | Already covered by (status, date) | What is genuinely new in ABS |
|---|---|---|
| Machine-readable offers | Google **UCP**, announced Jan 2026 with Shopify; Catalog, Cart, Checkout and Order capabilities; "Businesses remain the Merchant of Record" ([ucp.dev](https://ucp.dev), accessed 2026-11-04). OpenAI/Stripe **ACP** product feeds (API versions 2025-09-12 and 2025-09-29, [OpenAI commerce docs](https://developers.openai.com/commerce/llms-full.txt)). Klarna Agentic Product Protocol (Dec 2025, secondary). | Little. Free text kept in bounded `UntrustedText` fields and rejection of instructions addressed to agents at publication are a useful **injection-safety profile** to propose to UCP. The design idea is CaMeL's ([arXiv 2503.18813](https://arxiv.org/abs/2503.18813)), not new. |
| User mandate with strong authentication | **AP2 v0.2** (28 Apr 2026): Open and Closed Checkout and Payment Mandates as SD-JWT credentials ([spec](https://raw.githubusercontent.com/google-agentic-commerce/AP2/main/docs/ap2/specification.md)). **Mastercard Verifiable Intent** (5 Mar 2026, co-developed with Google). Both were contributed to the **FIDO Alliance** on 28 Apr 2026; the Payments Technical Working Group is chaired by Mastercard and Visa, the Agentic Authentication group by CVS Health, Google and OpenAI ([FIDO, 28 Apr 2026](https://www.fidoalliance.org/fido-alliance-to-develop-standards-for-trusted-ai-agent-interactions/)). Visa rules 4.1.23.3 (above). EMVCo "Agentic Payments: Framework for Specifications v1.0", draft for comment from 1 Sep 2026, built around "Intent Services" ([Business Wire, 31 Aug 2026](https://www.businesswire.com/news/home/20260831704950/en/); content from a summary, UNVERIFIED). NPCI UPI Reserve Pay and UPI Circle in the ChatGPT pilot (TechCrunch, 9 Oct 2025, secondary). | None. Concede. Note that under EBA Q&A 2019_4664 a mandate set up without the payer's PSP is not subject to strong customer authentication ([EBA](https://eba.europa.eu/single-rule-book-qa/qna/view/publicId/2019_4664)), so "mandate with SCA" means something legally only when a PSP performs it. |
| Offer snapshot frozen and countersigned at checkout | **AP2 v0.2:** "The Merchant MUST provide a merchant-signed JWT containing the Checkout to the Shopping Agent"; the Closed Checkout Mandate is bound to it by hash, and the merchant returns a Checkout Receipt (spec above). | Only the *rules of evidence*: the snapshot outranks a later edit of the listing, a broken chain counts against whoever kept it, and the snapshot must be kept and retrievable. AP2 says: "Specific details of how this is used for dispute resolution ... are outside the scope of this specification." Small, real, and the right size of contribution. |
| Agent identity | Visa Trusted Agent Protocol with Cloudflare (14 Oct 2025, [Business Wire](https://www.businesswire.com/news/home/20251014974512/en/)). Visa registration of agentic payment providers (rules 4.1.23.2) and disqualification "at its sole discretion" (4.1.23.11). Mastercard Agent Pay registration and agentic tokens (Oct 2025). IETF Web Bot Auth working-group draft (Sep 2026, secondary). Skyfire KYAPay; Trulioo Digital Agent Passport. | None. ABS already defers to RFC 9421, which is correct. |
| Qualified merchants and trust authority | Acquirer underwriting; Visa VAMP, Visa Integrity Risk Program, Mastercard ECM and MATCH (see Q3). DSA Art. 30 requires marketplaces to collect and verify trader identity (Reg. 2022/2065). Holds: Amazon DD+7, PayPal/eBay up to 21 days. OpenAI admits only "approved partners" to its product feeds. | Partly new: a **neutral, cross-rail, agent-queryable** merchant trust signal does not exist (medium confidence; only small vendor projects). Every mechanism inside it is old. |
| Liability allocation | **Visa:** the cardholder bears provider actions (4.1.23.10). **Amex:** "will protect eligible customers from charges related to AI agent error" for registered agents sending "authenticated purchase intent", announced 14 Apr 2026 ([Payments Dive, 29 Apr 2026](https://www.paymentsdive.com/news/amex-pushes-for-agentic-standards/818782/); full terms not reached, UNVERIFIED). **PayPal:** Purchase Protection on eligible agentic transactions; Seller Protection only for unauthorised and item-not-received ([paypal.ai/agent-ready](https://www.paypal.ai/agent-ready), accessed 2026-11-04 by the research lane). Worldpay (2026): "No liability shift exists yet" (secondary). | **Genuinely new:** a complete four-way rule (merchant for non-conformity and for manipulative offers; user inside the mandate; agent provider outside it or for "authorised but wrong"). But the market has already split: Visa says cardholder, Amex says issuer. ABS's "provider" needs an argument for why not the issuer, which holds the customer relationship and the dispute machinery. |
| Agent-specific dispute reason codes | None in Visa's rules (checked). Commentators file these disputes under existing fraud and not-as-described codes (secondary). Mastercard's public rules reportedly do not address agentic transactions (secondary, UNVERIFIED). | **Genuinely new, high confidence.** This is the most valuable deliverable. |
| Neutral tier-2 arbiter | Scheme arbitration (human); PayPal and eBay resolution centres; the AAA-ICDR AI arbitrator (3 Nov 2025, construction cases, a human finalises every award). | New when agent-specific, cross-rail and AI-first, but legally constrained (Q5). |
| Rail-agnostic settlement | AP2 and Visa Intelligent Commerce Connect are protocol- and network-agnostic (ICC supports TAP, MPP, ACP and UCP; pilot, 8 Apr 2026, [Business Wire](https://www.businesswire.com/news/home/20260408772335/en/)). x402 for stablecoins (Linux Foundation, Apr 2026, secondary). ACP and EMVCo are card-only. | A refund obligation on account-to-account rails, enforced through participation, is useful, but the rails are now building it themselves (Wero, Pix MED 2.0, UK APP reimbursement; see Q3). |

**Bottom line for Q1.** About 70–80% of ABS by object count duplicates live or standardised work: the
offer, the mandate, the snapshot, agent identity and settlement. The original part is the
dispute and liability layer plus the empirical question of what evidence an arbiter needs. These are
exactly the parts AP2, FIDO and EMVCo leave open: AP2's specification calls dispute use "outside the
scope", and FIDO's announcement does not mention disputes or liability.

---

## Q2. Adoption

| Party | Why it might adopt | What it loses | Likely stance |
|---|---|---|---|
| Merchants | Agent traffic; denial of buyer claims the snapshot contradicts (AG5); protection from false not-as-described claims. | Strict liability for injected content in reviews it hosts; working capital tied up in escrow; another certification; a second dispute forum while chargebacks still apply, so double exposure; the duty to "open sites to robots". Large merchants fight unwanted agents: Amazon v. Perplexity had an injection granted in March 2026, later vacated by the Ninth Circuit (secondary, dates UNVERIFIED). | No, unless a scheme or the dominant agent platform requires it. Big merchants are already on UCP or ACP. |
| Acquirers | Fewer disputes reaching the scheme, if tier 1 settles them first (as Visa RDR does today). | A third party's Trust Authority sits over their underwriting and can expel their merchants; they still carry merchant default on cards. | Lukewarm. Possible as a service they resell. |
| Issuers | The signed mandate and action log cut write-offs on "not what I wanted" claims. | Little, but they prefer scheme rules to an outside arbiter; Amex chose to absorb agent error itself. | Support the evidence; reject a new arbiter. |
| Schemes (Visa, Mastercard, Amex) | Ideas for reason codes. | Control of dispute rules. Visa has already allocated agent actions to the cardholder; Visa and Mastercard chair the FIDO Payments working group. | Will absorb good ideas and not adopt ABS. They are the decisive blockers on cards. |
| Agent providers (Anthropic, OpenAI, Google) | A trust story for agentic shopping; cheap AG1-P (their own C1 prevents it). | Uncapped AG2 liability, contrary to their terms (Anthropic: user responsible for "all Actions", cap €100 or six months' fees); 13-month log retention; certification; a neutral arbiter they may not run. OpenAI states it is "not the merchant of record". AP2 deliberately leaves liability to the networks. | No to AG2 as written; maybe yes to AG1-P and to a capped AG2. |
| Marketplaces (Amazon, eBay, Etsy) | None obvious. | Their own trust layer: A-to-z, resolution centres, DSA Art. 30 checks on their sellers. | Hostile, or adopt only internally. |
| Regulators | An evidence trail and a clear allocation of liability. | Nothing, but an AI arbiter with "final" decisions raises AI Act, ADR and GDPR flags. The EU Digital Fairness Act is due in Q4 2026; a draft was expected 11 Nov 2026 ([Lexgo, 20 Oct 2026](https://www.lexgo.be/en/news-and-articles/15170-inside-the-eu-s-planned-digital-fairness-act-digital-design-subscription-traps-and-influencer-marketing); whether it covers buying agents is UNVERIFIED). The UK CMA already says businesses are responsible for their agents (9 Mar 2026). | Interested in the analysis; will write their own rules, not endorse a private standard. |

**Is a standard the right vehicle?** Not now. A standard needs a standards body and an anchor adopter, and
ABS has neither.
- **A product** (arbiter as a service) faces the chicken-and-egg problem plus the licensing and AI Act
  burden.
- **A scheme rule** is the fastest and most effective vehicle: Visa already has a full agentic section
  (4.1.23, last updated April 2026). But schemes write their own rules.
- **A regulator's mandate** is the strongest vehicle for liability and the slowest.

The vehicle that fits the founder today is **a research artefact feeding existing bodies**: an open
benchmark, a proposed reason-code taxonomy and decision order, and a measured minimum evidence
standard. It would go in as a *dispute profile* of AP2/UCP and Verifiable Intent (FIDO Payments working
group), as comments on EMVCo's agentic framework, and as input to an A2A scheme's purchase-protection
rules.

**Realistic first adopter: EPI's Wero.** EPI is designing e-commerce purchase protection right now, with
workshops in Q4 2026, a framework expected in Q1 2027, and embedding for Dutch consumers by January 2028,
built "with input from merchants, unions, federations, PSPs, consumer associations, banks and relevant
institutions" ([The Paypers, 26 Oct 2026](https://thepaypers.com/payments/news/epi-starts-wero-ecommerce-roll-out-with-dutch-banks);
single trade-press source). It runs on an irrevocable instant rail, has no chargeback legacy, needs rules
for non-delivery and not-as-described, and will meet agent purchases soon. That is exactly where ABS's
rail-agnostic dispute module adds something. The founder's background in instant payments fits. Second
most realistic: an issuer or wallet that wants an Amex-style "agent error protection" and needs a decision
procedure for it. [Redacted: a remark on a private business idea.]

---

## Q3. "Never allow scammers in": achievable?

**No. As written it overreaches, and payments reviewers will discount the rest of the proposal because of
it.** No entry gate in payments or e-commerce claims zero, and the best-funded ones show why.

- **The strongest gates still leak.** Amazon, using government ID checks, forgery detection, video
  verification and links to known bad actors, with over $1.2bn spent and more than 15,000 people, blocked
  more than 700,000 attempts to open bad-actor selling accounts in 2023 and destroyed 7 million
  counterfeit items. The attempts never stop; some get through
  ([Amazon Brand Protection Report, Mar 2024](https://trustworthyshopping.aboutamazon.com/en-uk/amazon-brand-protection-report)).
- **The card schemes accept a baseline and manage it.**
  - Visa's VAMP merged its fraud and dispute programmes on 1 Jun 2025, with enforcement from
    1 Oct 2025. It flags acquirer portfolios at 50 and 70 basis points
    ([Visa VAMP fact sheet, 2025](https://corporate.visa.com/content/dam/VCOM/corporate/visa-perspectives/security-and-trust/documents/visa-acquirer-monitoring-program-fact-sheet-2025.pdf)).
    The merchant "excessive" level reportedly fell from 2.2% to 1.5% on 1 Apr 2026 in the EU and US
    ([vendor summary, 20 Jul 2026](https://redo.com/resources/articles/chargebacks/vamp-2026-shopify); not
    confirmed with Visa).
  - Mastercard's Excessive Chargeback Program starts at 100 chargebacks and 1.5% (vendor source,
    [Chargebacks911](https://chargebacks911.com/mastercard-ecm-program-thresholds-tiers/)).
  - MATCH lists terminated merchants for five years (vendor source; the code list is UNVERIFIED).
  - These programmes monitor, fine and expel. They do not promise "never".
- **Baselines the KPI ignores.** EEA card fraud was 0.033% of value in 2024. Remote card fraud was 0.091%,
  against 0.007% for in-person payments, and remote payments carried about 83% of card-fraud value. On
  credit transfers, "manipulation of the payer" rose to 74% of fraud value
  ([EBA/ECB joint report, 15 Dec 2025](https://www.ecb.europa.eu/press/intro/publications/pdf/ecb.ebaecb202512.en.pdf)).
  ABS's working band for scam loss, "below 0.05% by value", is therefore higher than the EEA's whole card
  fraud rate. The two measures differ (scam non-delivery against unauthorised fraud), but the number is
  neither "never" nor shown to be ambitious. It needs a baseline.
- **Where the scams actually come from.**
  - UK purchase scams in 2025: 175,809 cases (+5%), £118.1m lost (+20%), 71% of all APP scam cases.
  - 66% of APP cases began online
    ([UK Finance Annual Fraud Report 2026, 15 Jun 2026](https://www.ukfinance.org.uk/policy-and-guidance/reports-and-publications/annual-fraud-report-2026)).
  - Meta's internal documents projected about 10% of 2024 revenue (about $16bn) from ads for scams and
    banned goods, and it banned an advertiser only at 95% certainty of fraud
    ([Reuters, 6 Nov 2025](https://www.reuters.com/investigations/meta-is-earning-fortune-deluge-fraudulent-ads-documents-show-2025-11-06/);
    read via syndicated copies).
  - The founder's "one-hour shops on Facebook" are real. They are a problem of ad platforms and payer
    manipulation, which a merchant gate in the agent channel does not touch.

**What gets past a KYB-plus-probation gate.** These are not edge cases; they are how merchant fraud
already works on cards:
1. **Bust-out (exit) scams.** The merchant behaves well through probation, builds a track record, then
   takes a burst of orders and disappears. Volume caps only fix the size of the bust-out.
2. **Takeover of a qualified merchant,** or a change of its payout account through business-email
   compromise. The gate certified the company; the attacker inherits the certificate.
3. **Synthetic or nominee companies** with genuine register entries and mule beneficial owners. KYB checks
   documents, not intent.
4. **Transaction laundering:** a qualified merchant processes sales for unqualified ones. There is no
   credible estimate of its size, only vendor figures
   ([Protiviti](https://www.protiviti.com/us-en/whitepaper/clean-money-click-away-money-laundering-risks-e-commerce);
   UNVERIFIED), which is itself the point: it is hard to see.
5. **An honest merchant goes bust.** The buyer suffers the same non-delivery with no scammer involved.
   Escrow has to cover this as well.
6. **Counterfeits and replicas sold by legitimate merchants,** as in his own H03.
7. **Attacks on the trust signal itself:** fake "ABS-qualified" badges and look-alike feeds aimed at
   agents (his own T05).
8. **Payer-side manipulation:** the buyer's agent is steered. KYB does nothing here. Magentic Marketplace
   found agents taking the first offer 80–100% of the time
   ([Microsoft, arXiv 2510.25779, Oct 2025](https://arxiv.org/abs/2510.25779)), and position on the page
   strongly swings agent choice
   ([Allouah et al., arXiv 2508.02630, v3 Dec 2025](https://arxiv.org/abs/2508.02630)).

**What actually works, and already exists.** The real lever in ABS is "an unproven merchant is not paid
before delivery". It is the right lever, but marketplaces already pull it:
- Amazon releases funds 7 days after delivery (DD+7), with US enforcement reported from 12 Mar 2026
  ([trade press](https://riverbendconsulting.com/blog/dd7-amazon-payout-policy/));
- PayPal and eBay hold funds for up to 21 days for new sellers
  ([eBay help](https://pages.ebay.com.sg/pay/help/index.html), undated).

It turns "a scammer got in" into "a scammer did not get paid". The cost is the working capital of honest
new merchants, which is the adoption price. On card rails the acquirer already carries the risk of a
merchant that vanishes, which is why it underwrites and holds reserves. (That is general scheme practice;
the founder knows it better than this audit.) So on cards the gate largely repeats acquirer
underwriting. Its real value is on account-to-account rails, where nobody holds the merchant's risk today.
Even that gap is closing:
- **UK:** mandatory APP reimbursement (from 7 Oct 2024) covers purchase scams where the payee meant to
  defraud. It excludes civil disputes with a genuine supplier
  ([PSR information sheet v3](https://www.psr.org.uk/media/x4tji2en/psr-app-scams-psp-information-sheet-v3.pdf)).
- **Brazil:** Pix MED 2.0 became mandatory on 2 Feb 2026, with a tolerance period to 10 May 2026
  ([BCB Voto 7/2026](https://normativos.bcb.gov.br/Votos/BCB/20267/Voto_do_BC_7_2026.pdf)).
- **EU:** EPI is designing Wero purchase protection right now. Workshops run in Q4 2026, the framework is
  due in Q1 2027, and it is to be built in for Dutch consumers by January 2028
  ([The Paypers, 26 Oct 2026](https://thepaypers.com/payments/news/epi-starts-wero-ecommerce-roll-out-with-dutch-banks)).

So "on irrevocable account-to-account rails this is the only protection a buyer has" is false for
scams in the UK and is becoming false in the EU. It is true only for non-delivery or defects by a
**genuine** merchant.

**A claim that survives review:** "ABS does not promise to keep every scammer out. It makes sure an
unproven merchant is not paid before delivery, that a qualified merchant that turns bad is caught within
a bounded number of purchases, and that the buyer is made whole either way, while honest new merchants are
rarely refused." Measure the scam payout rate, the time to detect a bust-out, and the honest-merchant
false-reject rate. H6 with 8 simulated trust scenarios, and the scam's risk fields left honest, can
illustrate this but cannot support it.

---

## Q4. Is "conformity decides" sound?

**As a heuristic for allocating liability, yes; it is the strongest idea in the thesis. As a legal or
operational rule, it has six problems.**

1. **"Conforms to the offer" is narrower than conformity in law.**
   - Under the Sale of Goods Directive (EU) 2019/771, goods must meet subjective requirements (the
     contract, Art. 6) and objective ones (fit for normal purpose, normal quality and durability, what
     public statements lead the buyer to expect, Art. 7).
   - The seller is liable for non-conformity that shows within two years (Art. 10). It is presumed to
     have existed at delivery if it shows within one year (Art. 11). Terms that cut these rights do not
     bind the consumer (Art. 21) ([EUR-Lex](https://eur-lex.europa.eu/eli/dir/2019/771/oj)).
   - A frozen snapshot is good evidence of the subjective requirements only. ABS's 14-day window to
     record conformity, and a "conforming, so buyer side" decision, cannot end a claim for a defect that
     shows in month five. Every ABS decision on conformity has to be stated as "without prejudice to
     statutory conformity", or ABS will be making unfair-terms decisions.
2. **An agent probably cannot accept a deviation for the consumer.** Under Art. 7(5), a deviation from
   objective conformity (refurbished, used, a lower battery health) binds the consumer only if they were
   "specifically informed" and "expressly and separately accepted" it. No EU guidance, case or
   Commission Q&A says an AI agent can give that acceptance (absence UNVERIFIED). This is a real opening:
   a mandate field for "deviations I accept in advance", whose legal effect is tested, would be a
   genuine contribution to standards.
3. **The 14-day withdrawal right makes most of the novel cases moot in the EU.**
   - Consumer Rights Directive 2011/83/EU Art. 9 gives 14 days from receipt to withdraw without giving a
     reason ([EUR-Lex](https://eur-lex.europa.eu/eli/dir/2011/83/oj)). For EU consumer physical goods, AG2
     ("authorised but wrong") and AG5 (change of mind) are therefore mostly decided by sending the item
     back. ABS's new rule then mainly decides who pays the return postage.
   - Losses from AG2 are real exactly where the right does not apply: the Art. 16 exceptions. These are
     goods made to specification, perishables, unsealed hygiene goods, digital content once started,
     and accommodation, transport, car hire and leisure on a specific date, which covers travel and
     tickets, the flagship agent use cases. They also include every B2B purchase.
   - ABS covers physical goods first and defers services and digital goods (sections 1.1 and 12.1 item
     4). **Its scope is inverted:** it covers the case where allocating liability matters least and
     defers the cases where it matters most.
4. **There is no trustworthy evidence of what was delivered.** See I4. Card "not as described" disputes
   already fail on this point, and ABS fixes only the offer side. Subjective quality ("the fabric feels
   cheap"), fit, services (nothing is delivered to inspect), used goods (12.1 item 5 admits no grading
   scale exists) and drop-shipping (the merchant never touches the item) make conformity contestable
   exactly where disputes occur.
5. **The rule on manipulative offers is aimed at the wrong party, and it can be used for sabotage.**
   - Rule 2 makes the merchant liable when the agent followed text in content the merchant "controls or
     hosts", including reviews. A competitor or a buyer can plant an injected review, buy through an
     agent, and file AG4.
   - Strict liability for content written by third parties runs against the hosting principle merchants
     know from platform law (for example DSA Art. 6), and merchants will refuse it.
   - Worse for safety: the party that can prevent injection is the **agent provider**, by not obeying
     instructions found in data (the CaMeL design,
     [Debenedetti et al., arXiv 2503.18813, Mar 2025](https://arxiv.org/abs/2503.18813)). Under Rule 2 the
     provider bears nothing when its agent obeys injected text, so it has no incentive to harden. A
     least-cost-avoider analysis puts at least part of AG4 on the provider: liability shared, or on the
     merchant only for fields it wrote itself or after it was notified.
6. **Cross-border consumer law overrides the Participation Agreement.**
   - Under Rome I Art. 6(2), a choice of law cannot remove the protection of the consumer's home law.
   - Under Brussels I bis Arts. 17–19, consumers can sue at home.
   - The Unfair Contract Terms Directive's annex, point 1(q), presumes terms excluding court action to be
     unfair.
   - So "the decision is final within the programme" (rulebook 6.5) cannot bind a consumer. (Treaty text
     from EUR-Lex; summarised by the legal research lane, not re-quoted here.)

**Will agent providers accept liability?** Not on the terms in ABS v0.1.
- **Anthropic's own Consumer Terms (effective 8 Oct 2025)** say:
  - "You are responsible for all Inputs you submit to our Services and all Actions";
  - Actions "may not be error free";
  - the services are provided "as is";
  - liability is capped at the higher of six months' fees or €100
  ([anthropic.com/legal/consumer-terms](https://www.anthropic.com/legal/consumer-terms), accessed
  2026-11-04).

  ABS asks Anthropic to reverse its terms for AG2. OpenAI's terms could not be fetched (HTTP
  403), so they are UNVERIFIED here.
- **What would move providers:**
  - a purchase guarantee as a product feature, as Amazon's A-to-z guarantee shows;
  - regulators: the UK CMA's guidance of 9 Mar 2026 (updated 30 Oct 2026) says "Ultimately, you will be
    responsible if an AI agent does something illegal"
    ([gov.uk](https://www.gov.uk/government/publications/complying-with-consumer-law-when-using-ai-agents/complying-with-consumer-law-when-using-ai-agents)),
    though it addresses agents that businesses deploy, not buying agents that consumers use;
  - the fact that AG1-P costs them almost nothing, because their own deterministic C1 stops hard-limit
    breaches.
- **Realistic outcome:** providers take AG1-P and resist AG2. AG2 is subjective, unbounded and invites
  moral hazard: write a vague intent, then say "not what I meant". The finding that decides AG2 ("matches
  the intent?") is made by the LLM fact-finder. The deterministic layer does not make it objective.
- **A version providers could sign:** AG2 falls on the provider only when the record shows the agent
  ignored an explicit instruction or clarification, or guessed where the mandate required it to ask. It
  is capped per purchase and insured. Otherwise the buyer bears it, with the statutory right of
  withdrawal intact.

---

## Q5. The AI Dispute Decision Center

**"Humans only for escalations" cannot be defended in the EU in its current form. Every relevant regime
requires a human on request, and one of them makes the system high-risk.**

- **The EU AI Act classes it as high-risk.** Annex III point 8(a) covers AI systems "intended to be used
  by a judicial authority or on their behalf ... in researching and interpreting facts and the law and in
  applying the law to a concrete set of facts, or to be used in a similar way in alternative dispute
  resolution" ([AI Act Explorer, Annex III](https://artificialintelligenceact.eu/annex/3/), accessed
  2026-11-04).
  - LLM fact-finders whose findings feed a rule engine that decides the case match that wording. The
    Art. 6(3) exemption for "narrow procedural tasks" does not fit a system that decides outcomes.
  - Consequences: risk management, data governance, logging, transparency, **human oversight with power
    to override (Art. 14)**, accuracy and robustness (Art. 15), a conformity assessment and registration,
    plus a right to an explanation (Art. 86).
  - The Digital Omnibus on AI moved the Annex III obligations from 2 Aug 2026 to **2 Dec 2027**. It was
    published in the Official Journal on 24 Jul 2026 and entered into force on 27 Jul 2026
    ([Garrigues, 24 Jul 2026](https://www.garrigues.com/en_GB/garrigues-digital/ai-digital-omnibus-regulation-has-been-published-redefining-deadlines-and)).
    Its number, Regulation (EU) 2026/1744, comes from a secondary source
    ([Praxikon](https://www.praxikon.com/en/richtsnoeren/regulation-eu-2026-1744-digital-omnibus-on-ai))
    and is UNVERIFIED in the Official Journal.
  - Whether a private, contractual resolution centre counts as "alternative dispute resolution" under the
    AI Act is an open legal question (UNVERIFIED either way). Design as if it does.
- **GDPR Art. 22.** A refund decision based solely on automated processing has legal effects.
  - Even under the contract exception, Art. 22(3) requires the right "to obtain human intervention ... to
    express his or her point of view and to contest the decision"
    ([EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj)).
  - CJEU *SCHUFA* (C-634/21, 7 Dec 2023) extends "decision" to automated outputs that play a determining
    role.
  - CJEU *Dun & Bradstreet Austria* (C-203/22, 27 Feb 2025) requires an explanation of "the procedure and
    principles actually applied"
    ([summary, Mar 2025](https://www.dataprotectionreport.com/2025/03/what-do-organisations-need-to-disclose-to-individuals-about-ai-and-automated-decisions/)).
  - The signed receipt is a good start on that explanation, but it has to be written for the person
    affected, not as a hash. Merchants that are companies are outside the GDPR; sole traders are not.
- **ADR law.**
  - The ADR Directive 2013/11/EU requires the "natural persons in charge of ADR" to have expertise,
    independence and impartiality (Art. 6). An agreement made before the dispute to submit to ADR does not
    bind the consumer if it removes access to court (Art. 10). A binding outcome cannot deprive the
    consumer of mandatory home-law protection (Art. 11)
    ([EUR-Lex](https://eur-lex.europa.eu/eli/dir/2013/11/oj)).
  - Amending Directive (EU) 2025/2647 was published on 30 Dec 2025, entered into force on 19 Jan 2026,
    must be transposed by 20 Mar 2028 and applies from 20 Sep 2028. It "mandates prior notification to
    consumers of the use of automated means" and "requires the possibility of review by a competent
    natural person from the ADR entity"
    ([Conventus Law summary](https://conventuslaw.com/report/eu-the-new-alternative-dispute-resolution-framework-directive-2025-2647/);
    dates also from [EAPIL, 23 Jan 2026](https://eapil.org/2026/01/23/directive-eu-2025-2647-amending-the-adr-framework-for-consumer-disputes/);
    the article number is UNVERIFIED).
  - The EU has legislated the opposite default to "humans only for escalations".
- **The realistic legal form.** PayPal's and eBay's resolution centres are traders' own complaint
  handling, not ADR. ABS tier 2 can work the same way:
  - binding by contract on merchants and agent providers (business to business);
  - not binding on consumers, who keep the courts, ADR, chargebacks and statutory rights;
  - a human review open to any party on request, not only when the engine returns "review".
- **Accuracy and manipulation.**
  - LLM judges show position, length and self-preference bias
    ([Zheng et al., NeurIPS 2023](https://arxiv.org/abs/2306.05685)).
  - They can be flipped by trivial tokens such as ":" or "Thought process:"
    ([arXiv 2507.08794, 2025](https://arxiv.org/abs/2507.08794)) and by optimised injected sequences
    ([JudgeDeceiver, arXiv 2403.17710](https://arxiv.org/abs/2403.17710)).
  - At a million disputes, 98% accuracy still means 20,000 wrong decisions, so appeal capacity has to be
    sized to the error rate (the auditor's arithmetic).
- **The closest institutional precedent keeps a human on every award.** The AAA-ICDR AI arbitrator,
  launched 3 Nov 2025, is opt-in for both parties, covers documents-only construction cases, and "every
  decision ... involves a human arbitrator"; only a human finalises the award
  ([AAA FAQ](https://www.adr.org/news-and-insights/ai-arbitrator-faq/)). eBay and PayPal were reported to
  handle more than 60 million disputes a year through online resolution, a figure from Colin Rule's own
  bio, not audited
  ([SMU lecture 2016](https://ccla.smu.edu.sg/sites/cebcla.smu.edu.sg/files/Singapore%20Mediation%20Lecture%202016.pdf)).
- **Rules-based adjudication already exists in the card world.**
  - Visa Rapid Dispute Resolution refunds automatically from rules the merchant sets in advance
    ([Visa](https://usa.visa.com/dam/VCOM/global/support-legal/documents/proper-identification-of-rdr-transactions-and-service-activation.pdf)).
  - Compelling Evidence 3.0 decides card-absent fraud disputes from matching data
    ([Checkout.com](https://www.checkout.com/blog/visa-compelling-evidence-3-0)).
  - Ethoca Alerts prevented more than 39 million chargebacks in 2025 (Mastercard's own figure,
    [Mastercard 2026](https://www.mastercard.com/gb/en/news-and-trends/Insights/2026/how-ethoca-helps-prevent-chargebacks-reduce-revenue-loss-and-improve-customer-experience.html)).
  - "Deterministic rules decide" is not new. LLM fact-finding over agent records is.
- **Cost.** The model calls cost little per case. The cost driver is human review on request, appeals,
  and liability for wrong decisions. Industry figures (about $74 direct cost per card dispute) are vendor
  estimates and UNVERIFIED ([Chargebacks911](https://chargebacks911.com/chargeback-stats/)).
- **"Deterministic" is partly cosmetic.** Rules give the same decision from the same facts. The facts
  come from LLMs, so the inconsistency moves into fact-finding. H5 tests exactly this seam, which is
  good. [Redacted: a remark on the status of a private product, from private work-history notes.]
  Present the hybrid as a design pattern, not as a product dependency.

**A defensible version:** "AI-first. LLMs extract the facts with citations, rules decide, and a signed
receipt explains the decision in plain words. Any party can obtain a human review. Humans audit a random
sample. Error and reversal rates are published. Decisions bind participants by contract, and consumers
keep every statutory route."

---

## Q6. [Redacted]

[Redacted in the public copy: this section assessed private application material.]

---

## What already exists that ABS must build on, or concede to

**Concede: use these instead of ABS's own objects.**
- **Mandate and signed checkout:** AP2 v0.2 Checkout and Payment Mandates and the merchant-signed checkout
  JWT; Mastercard Verifiable Intent. Both now sit in the FIDO Payments Technical Working Group. ABS's
  Mandate and Offer Snapshot should become *profiles* of these. They should not be competing schemas.
- **Offers and catalogues:** UCP (Shopify-led, live) and ACP product feeds. Offer an injection-safety
  profile for them.
- **Agent identity:** Visa TAP and agentic-provider registration, Mastercard Agent Pay, Web Bot Auth
  (IETF).
- **Card-rail liability for in-mandate actions:** Visa Core Rules 4.1.23.10 (cardholder). ABS's
  user-pays arm agrees with it; the provider-pays arm must be argued as a contract *over* the scheme
  rule, not instead of it.
- **Merchant risk:** acquirer underwriting, VAMP and ECM monitoring, MATCH, marketplace holds (DD+7,
  holds of up to 21 days). Reuse the existing signals rather than build a new authority.
- **Account-to-account protection:** UK APP reimbursement for purchase scams, Pix MED 2.0, and the Wero
  purchase protection now being designed.
- **Rules-based dispute automation:** Visa RDR, Compelling Evidence 3.0, Ethoca.

**Build on: open gaps where ABS can lead.**
- Dispute use of AP2 evidence: AP2 says it is "outside the scope".
- Agent dispute reason codes: Visa has none.
- A rule for "authorised but wrong" that is not "the cardholder always pays": Amex has shown that the
  market wants one.
- Rules of evidence: what the snapshot outranks, and who loses when the chain breaks.
- A measured minimum evidence standard.
- Mandate pre-acceptance of deviations (SGD Art. 7(5)).
- An AI-assisted arbiter that meets the AI Act, the GDPR and ADR law.

---

## Fatal-flaw risks

1. **Wrong vehicle, no adopter.** An end-to-end standard competes with schemes, Google/FIDO and the
   UCP/ACP coalitions, all of which have leverage ABS lacks. Nothing forces anyone to adopt it.
2. **No answer to its own question.** The repository's documents give three answers to "who pays when
   the agent is authorised but wrong" (I2). Visa (cardholder) and Amex (issuer) have answered it
   differently again. The pre-registered experiment grades the status-quo answer as correct.
3. **Conformity without delivery evidence.** "Conformity decides" needs to know what was in the box. ABS
   assumes a signed carrier inspection that does not exist (I4), and its idea of conformity is narrower
   than consumer law (Q4).
4. **Regulatory collision.**
   - The arbiter is presumptively a high-risk AI system.
   - Consumers cannot be bound by "final" programme decisions.
   - Escrow and the collection right are regulated payment services.
   - "Humans only for escalations" is the opposite of what GDPR Art. 22(3) and Directive 2025/2647
     require.
5. **Overclaims that discredit the whole proposal.** "Never allow scammers in", "the only protection a
   buyer has" on account-to-account rails, and "humans only for escalations". Any payments or regulatory
   reviewer stops reading at the first one.
6. **The research shows no effect yet.** [A clause about private application material is redacted.]
   - Phase 1 is null at the ceiling (0 of 528).
   - Phase 2 is graded against the author's own rules with infallible delivery evidence, so H4 is close
     to true by construction.

## Top 10 fixes, ranked by importance

1. **Decide AG2 once and defend it against Visa 4.1.23.10 and Amex.**
   - Recommendation: the agent provider is liable only when the record shows agent fault. That means it
     ignored an explicit instruction or clarification, or guessed where the mandate required it to ask.
     Liability is capped per purchase and insurable.
   - Otherwise the buyer bears it, with the withdrawal right intact.
   - Make the rulebook, ABS, [redacted: private drafts] and the Phase 2 ground truth agree. Or test
     both allocations as an experimental factor and report which one arbiters apply more consistently.
2. **Reposition from "a standard" to "a dispute profile plus a benchmark".**
   - Fill section 11 with the concession table above: mandates and signed checkouts belong to AP2 and
     Verifiable Intent, catalogues to UCP and ACP, agent identity to TAP, Agent Pay and Web Bot Auth.
   - ABS contributes reason codes, the decision order, rules of evidence and a measured minimum
     evidence standard.
   - Write sections 6 and 7 or delete every reference to them.
3. [redacted: private application material]
4. **Make delivery evidence realistic and contestable.**
   - Replace "signed carrier inspection" with buyer photos, merchant packing photos or video, serial
     numbers and carrier weight scans, some of them conflicting or forged.
   - Measure arbiter accuracy and the fooled rate when delivery evidence is disputed. That turns H4 into
     a real test.
5. **Make Phase 1 adversarial, or drop it from the pitch.**
   - Use an attacker model that optimises listings, reviews and injections against each agent over many
     attempts, on pages closer to the real web.
   - Report attack success against number of attempts, as Anthropic does (about 1% at 100 attempts for
     Opus 4.5).
   - Fixed, blatant traps measure nothing at today's capability level.
6. **Replace "never allow scammers in" with measurable claims.**
   - Measure the scam payout rate, the latency to detect a bust-out, and the honest-merchant false-reject
     rate.
   - Add to the threat model: bust-outs, merchant account takeover, synthetic and nominee companies,
     transaction laundering, and honest insolvency.
   - Benchmark against EBA/ECB and UK Finance baselines.
   - Drop "the only protection" for account-to-account rails.
7. **Build legal compliance into the design.**
   - Tier-2 decisions bind business participants by contract. Consumers keep the courts, ADR,
     chargebacks, withdrawal and two-year conformity.
   - A human review is available on any party's request.
   - Plain-language explanations per case.
   - Treat the Decision Center as AI Act Annex III 8(a) high-risk and design Art. 14 oversight now; the
     obligations apply from 2 Dec 2027.
   - Run escrow and collection only through a licensed PSP.
8. **Re-allocate liability for injection.**
   - The merchant is liable for fields it wrote, or for hosted content after notice.
   - The agent provider shares liability when its agent obeys instructions found in data, because it is
     the party that can prevent it.
   - This removes the competitor-sabotage vector and gives providers a reason to harden their agents.
9. **Move scope to where liability matters.**
   - Before adding more physical-goods cases, add travel, tickets and accommodation, digital goods and
     B2B purchases, none of which has a withdrawal right.
   - Add a mandate field for "deviations accepted in advance" and state its Art. 7(5) status as an open
     legal question.
10. **Pick one first adopter and one standards channel, and separate business from research.**
    - EPI Wero purchase protection for the account-to-account module; its framework is being shaped in
      Q4 2026 workshops.
    - FIDO Payments working group for the evidence profile; EMVCo's agentic framework for cards.
    - Settle the neutrality conflict: an agent provider must never run the arbiter for cases in which it
      can be liable.
    - [Redacted: a remark on a private business idea.]

Housekeeping, not ranked:
- reconcile [redacted: a private draft's count] against 40 Dispute Cases and the hypothesis numbering;
- use a cross-family arbiter, or add one (the founder's own reviewer rule);
- map each named standard to the ABS requirement that uses it, or drop it.

---

## What I could not verify

- **Amex Agent Purchase Protection:** full terms, caps and whether it is live. Amex's page did not load;
  the only source is a quote in Payments Dive, 29 Apr 2026.
- **OpenAI:** its terms of use (HTTP 403), and the reported March 2026 move away from Instant Checkout
  (secondary only).
- **AI Omnibus:** the regulation number 2026/1744 and its Official Journal text (secondary). Also open:
  whether a private, contractual resolution centre is "alternative dispute resolution" for Annex III
  8(a).
- **Directive 2025/2647:** article numbers and exact wording of the automated-means and human-review
  rule (secondary summaries only).
- **PSD3/PSR:** final adoption, publication in the Official Journal, and the final SCA and
  commercial-agent wording. The research lane reported Coreper approval on 28 Oct 2026; I did not open
  the Council document myself.
- **Visa's merchant threshold** under VAMP of 1.5% from 1 Apr 2026 (vendor source). MATCH reason codes.
  Any credible estimate of transaction-laundering prevalence; none appears to exist.
- **EMVCo's agentic framework:** contents, and whether it addresses disputes (summary only). Mastercard's
  public rules on agentic disputes (secondary).
- **Amazon v. Perplexity:** the injunction and vacatur dates. The NPCI "Unified Agent Protocol" status.
  An Anthropic "Claude Commerce Agents" blueprint of 2 Sep 2026, seen only in secondary coverage.
- **Wero purchase-protection timeline:** one trade-press article.
- [redacted: private application material]
- **UK law:** whether the Consumer Rights Act 2015 duty of reasonable care and skill for services makes a
  consumer-facing agent provider liable for AG2 errors whatever its terms say. Not researched; it could
  strengthen the provider-liability arm.
- **Self-reported figures:** Colin Rule's figure of more than 60 million eBay/PayPal disputes a year, and
  Mastercard's figure of 39 million chargebacks prevented by Ethoca.

*Method note: the web research was split into three lanes (protocols and schemes; law; fraud,
dispute-resolution and safety literature), plus the auditor's own checks. These checks were done by the
auditor directly: the Visa Core Rules text (downloaded and searched), the AP2 v0.2 specification, the
FIDO announcement, the AI Act Annex III wording, [a page about private material, redacted], Anthropic's Consumer
Terms, the CMA guidance and the Wero article. Everything else relies on the research lanes, with sources
as cited.*

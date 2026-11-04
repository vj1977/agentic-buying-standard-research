**Verdict: WEAK ACCEPT for a failure-analysis workshop paper.**

Reviewed `99fd582`, read-only and offline. Five deciding reasons:

1. The paper now centres its strongest contribution: optimised evidence fabrication defeats otherwise accurate dispute judges.
2. The principal counts reproduce from stored logs: **12/14, 14/14, 6/14; common-budget 10/14 versus 6/14; same-call 11→1 and 12→1**. All three SVGs exactly match regeneration in memory.
3. H8, revised gates, hybrid-contract replays and future experiments now have appropriately limited status. I found no remaining explicit presentation of those exploratory results as confirmatory.
4. External validity remains weak: author-designed cues and labels, textual photographs, shared source cases, historical rules and only 14 attacked case-sides.
5. Defence effectiveness remains unestablished, but the paper now acknowledges that. The remaining reporting and design contradictions below are repairable without changing the central result.

**Mismatch table**

I checked every numerical claim in the abstract and Sections 5–8 against the result sources. The explicit counts, percentages, intervals and p-values match; the remaining mismatches concern what those numbers describe.

| Location | Mismatch / unsupported interpretation | Source and correction |
|---|---|---|
| [paper/main.md:102](../paper/main.md:102) | Structured offers and stake framing “changed no outcome.” | Legacy listings changed liability accuracy **15/16→16/16 for each arbiter**; stake framing changed E0 outcomes. Say **no statistically significant difference**, not no outcome change. [phase2_summary.md:276](../results/phase2_summary.md:276), [285](../results/phase2_summary.md:285). |
| [paper/main.md:117](../paper/main.md:117) | “Every false claim” at every level became a non-conformity claim. | **D46 at E1 succeeded as AG1-P**, using signed intent text, rather than AG3/photo fabrication. Restrict the universal description to the relevant E3 results. [phase3_summary.md:41](../results/phase3_summary.md:41), [137](../results/phase3_summary.md:137). |
| [paper/main.md:141](../paper/main.md:141) | A travelling digest lets the issuer recompute “without asking.” | A hash authenticates retrieved records; it does not supply their contents. ABS requires the verifier to **hold the records and keys**. Retrieval remains necessary. [ABS_v0.3.md:775](../standard/ABS_v0.3.md:775). |
| [paper/main.md:143](../paper/main.md:143) | The design removes judgement from “most agent-fault cases.” | No evaluated case distribution establishes **most**. Say “machine-readable breaches with comparable, available records.” The design label at line 139 does not substantiate this prevalence claim. |

Figure values and exploratory labels are correct. Figure 3 also discloses its unequal review estimands: one A1 decision versus any of three A2 runs.

**Application notes**

[Redacted in the public copy: notes on private application material.]

**Design-note contradictions**

1. **Stage 2 defeats legitimate merchant-performance claims.** Checkout matching authenticated instructions is insufficient to reject fraud or not-as-described disputes: delivery may still be defective, and legal authorisation remains the PSP’s question. [ADOPTION_AND_CONFIRMATION.md:104](../standard/ADOPTION_AND_CONFIRMATION.md:104) conflicts with ABS’s Step 0/conformity-first order and Audit 2 PAY-04. B6 repeats the contradiction at [ABS_v0.3.md:4074](../standard/ABS_v0.3.md:4074).
2. **“Never helps the provider” omits an express exception.** The note’s blanket prohibition at [line 191](../standard/ADOPTION_AND_CONFIRMATION.md:191) conflicts with its own injection row and A5.7(c), which admits the provider’s sole-source action log for causation, potentially shifting liability to the merchant. [ABS_v0.3.md:1553](../standard/ABS_v0.3.md:1553).
3. **AG4-D is misassigned.** The confirmation matrix calls it non-delivery at [line 167](../standard/ADOPTION_AND_CONFIRMATION.md:167); ABS defines it as deceptive offer content. Non-delivery belongs to AG3. A4.5 repeats this mapping error.
   
No additional contradiction found with Audit 2’s positions on consent-dependent recalls, separate purchase SCA, preserved rail rights or “designed against” regulatory requirements.

**N-item status**

These are deliverable/source closure assessments, not a fresh code audit.

| Item | Status and evidence |
|---|---|
| N01 | **Closed as documented:** one vote per finder/item/attribute; duplicate handling recorded. [PREREGISTRATION.md:1296](../results/PREREGISTRATION.md:1296). |
| N02 | **Closed as documented:** item coverage preserved; six stored decisions now review. [phase3_summary.md:446](../results/phase3_summary.md:446). |
| N03 | **Partly closed:** named wording/date counterexamples repaired; mixed claims can still hide an unread defect clause. [PREREGISTRATION.md:1376](../results/PREREGISTRATION.md:1376). |
| N04 | **Closed for reported counterexamples:** checker v2 rejects 44 wrong mandates; 36/40 correctly renamed checker agreement. [PREREGISTRATION.md:1370](../results/PREREGISTRATION.md:1370). |
| N05 | **Closed:** Appendix A now specifies authenticated context, envelope hash and SignatureInput. [paper/main.md:189](../paper/main.md:189). |
| N06 | **Closed in paper/replay reporting:** case-level intervals replace run-level inference. [Redacted: a note on private application material.] |
| N07 | **Closed:** follow-ups explicitly remain unfrozen plans. [paper/main.md:161](../paper/main.md:161). |
| N08 | **Closed:** discussion now reports four hard-set payments plus the separate adaptive attack. [paper/main.md:155](../paper/main.md:155). |
**Summary**

- Reviewed **`2e8308592a4c7d893278fde3f058b3c522f7355d`**, read-only and offline. No files changed, network commands, APIs or LLM CLIs used.
- **13 CLOSED, 16 PARTLY CLOSED, 1 OPEN; none WORSE.** The original P0 is closed.
- Principal attack counts reproduce: **12/14, 14/14, 6/14**; common-budget comparison **10/14 versus 6/14, p=0.125**.
- Same-call gate results, hybrid v2 replay, capture re-score and simulation results reproduce. Reproduction does **not** validate the revised checkers.
- **246 distinct tests passed:** 191 repository tests and 55 simulator tests. Seventeen write-dependent tests remained unrun; harmless metadata/directory operations were stubbed for some tests.
- The requested original counterexamples are addressed, but variants still bypass the gate, capture checker, hybrid contract and displayed-record integrity check.
- Historical model logs are unchanged. Simulation artifacts were regenerated with explicit correction notes; I found **no silent replacement of historical model results**.
- **Paper verdict: BORDERLINE.** Reporting is substantially more credible, but “every defect fixed” is unsupported, and the revised defences remain unvalidated.

**F01–F30 verdicts**

“Closed” means the original defect is repaired or its unsupported claim withdrawn; it does not imply production readiness.

| Finding | Verdict | Evidence and remaining issue |
|---|---|---|
| F01 Universal deception claim | **CLOSED** | Replaced by 0/25 scripted cases, explicitly contrasted with 6/14 optimised successes. [PHASE2_DISPUTES.md:48](../results/PHASE2_DISPUTES.md:48) |
| F02 Unequal attack budgets | **CLOSED** | Common-k counts and costs reproduce; unequal-budget result is now descriptive. [PHASE3_ATTACKS.md:437](../results/PHASE3_ATTACKS.md:437) |
| F03 Confounded H10 | **PARTLY CLOSED** | Same-call 11→1 and 12→1 lead correctly. Matched prospective defence evaluation remains unrun. [PHASE3B_PROVENANCE.md:30](../results/PHASE3B_PROVENANCE.md:30) |
| F04 Format rejection mistaken for provenance | **PARTLY CLOSED** | Rejection splits reproduce and abstract acknowledges them. Typed-output measurement remains absent. [PHASE3B_PROVENANCE.md:37](../results/PHASE3B_PROVENANCE.md:37) |
| F05 Citation resolution/content | **PARTLY CLOSED** | Nonexistent registry path now returns `review`. However, `unchecked` content still counts as supported. [provenance.py:460](../acs/provenance.py:460) |
| F06 Wording disables denial safeguard | **PARTLY CLOSED** | “Never authorised a broken unit” now reviews. “The screen is shattered” still permits AG5 with **no findings**; see N03. [provenance.py:225](../acs/provenance.py:225) |
| F07 Independence versus authority | **PARTLY CLOSED** | Standard now distinguishes issuer, stake, commitment, custody and authority. Gate v2 retains binary source tiers; discrepancies are candidly documented. [PHASE3B_PROVENANCE.md:286](../results/PHASE3B_PROVENANCE.md:286) |
| F08 Missing confidence threshold | **CLOSED** | Historical description corrected; separately versioned threshold sends both D22 refunds to review. Reproduced. [hybrid.py:196](../acs/hybrid.py:196), [PHASE3_ATTACKS.md:481](../results/PHASE3_ATTACKS.md:481) |
| F09 Attribute agreement/coverage | **PARTLY CLOSED** | Attribute voting improves, but duplicate rows manufacture majorities and item coverage collapses across products; see N01–N02. [hybrid.py:223](../acs/hybrid.py:223) |
| F10 Current-core rule mismatch | **PARTLY CLOSED** | Version matrix and v1.4 engine exist. A1/A2 prompts and findings still lack a v1.4 path; no current-core model evaluation. [ABS_v0.3.md:4245](../standard/ABS_v0.3.md:4245) |
| F11 Settlement mapping | **CLOSED** | Current v1.4 mapping uses refunds, collection and issuer referral; historical mappings remain explicitly versioned. [rule_engine.py:308](../acs/rule_engine.py:308) |
| F12 Withdrawal prerequisites | **PARTLY CLOSED** | Negative interval now returns unresolved; consent fields added. But all three consents deny withdrawal **even when performance has not begun**, contrary to the local standard. [rule_engine.py:115](../acs/rule_engine.py:115), [ABS_v0.3.md:736](../standard/ABS_v0.3.md:736) |
| F13 Displayed-record integrity | **PARTLY CLOSED** | Checkout quantity 9999 correctly invalidates integrity. Changing displayed `transaction.items[0].qty` to 9999 still leaves both integrity flags true and no problems: transaction is copied separately. [evidence.py:183](../acs/evidence.py:183), [evidence.py:207](../acs/evidence.py:207) |
| F14 Authentication boundary/short anchor | **PARTLY CLOSED** | Standard specifies authenticated context and full commitment; example hashes reproduce. Paper Appendix A still describes the old body-hash signature boundary; see N05. [ABS_v0.3.md:853](../standard/ABS_v0.3.md:853) |
| F15 Schemas | **PARTLY CLOSED** | Version, dispatch, RefusalRecord and capture conditions corrected. Schemas remain embedded; the subset validator is outside the repository, and full validation remains outstanding. [ABS_v0.3.md:918](../standard/ABS_v0.3.md:918), [ABS_v0.3.md:4296](../standard/ABS_v0.3.md:4296) |
| F16 Substring conformity | **CLOSED** | Both iPhone 16 Pro→16 and new→refurbished return `nonconforming`. Declared exceptions replace substring matching. [engine.py:180](../standard/sim/engine.py:180) |
| F17 Simulation overclaim | **CLOSED** | Recomputed 496 determinate +2 escalated live disputes; separate coverage and execution counts. Stipulated-fact limitation is prominent. [REPORT.md:11](../standard/sim/REPORT.md:11) |
| F18 Capture-checker false positives | **PARTLY CLOSED** | Original defective K2 fails; 36/40 re-score reproduces. New checker still accepts wrong identities and negated constraints; see N04. [capture.py:229](../acs/capture.py:229) |
| F19 Preregistration chronology | **PARTLY CLOSED** | Historical chronology is substantially corrected; Phase 3 explicitly exploratory. Follow-up experiments are called preregistered although their source says “to be pre-registered”; see N07. [CHRONOLOGY.md:42](../results/CHRONOLOGY.md:42), [PREREGISTRATION.md:1242](../results/PREREGISTRATION.md:1242) |
| F20 Invalid financial decisions | **CLOSED** | AG3 + buyer + refund −10 produces contract violations and cannot score success. Invalid outputs retained; three historical over-refunds identified. [decision_contract.py:48](../acs/decision_contract.py:48), [attack.py:320](../acs/attack.py:320) |
| F21 Repeated outputs as independent trials | **PARTLY CLOSED** | Original manipulation inference now uses 25 cases and discloses shared roots. New v2 tables reintroduce output-level Wilson intervals; see N06. [AUDIT1_CORRECTIONS_PHASE1_2.md:261](../results/AUDIT1_CORRECTIONS_PHASE1_2.md:261) |
| F22 “Honest” cohort | **CLOSED** | Renamed baseline workload; benign/adversarial and true-claimant review burdens reported. [PHASE3B_PROVENANCE.md:58](../results/PHASE3B_PROVENANCE.md:58) |
| F23 Attempts metric | **CLOSED** | Aggregate cost distinguished from conditional first success and censored searches. Counts reproduce. [PHASE3_ATTACKS.md:453](../results/PHASE3_ATTACKS.md:453) |
| F24 Author-designed cues/unvalidated labels | **OPEN** | Explicitly documented, but no counterbalanced cases or independent labels supplied. A plan does not repair benchmark validity. [AUDIT1_CORRECTIONS_PHASE1_2.md:290](../results/AUDIT1_CORRECTIONS_PHASE1_2.md:290) |
| F25 Conditional reimbursement | **CLOSED** | Three uncertain recoveries separated; currency-specific loss bounds reproduce. [REPORT.md:479](../standard/sim/REPORT.md:479) |
| F26 Misleading tests/path resolver | **CLOSED** | Original hyphenated/empty-path defects fixed; tests now distinguish structural validation from stronger claims. Remaining new gaps are identified below. [hybrid.py:247](../acs/hybrid.py:247), [REPORT.md:55](../standard/sim/REPORT.md:55) |
| F27 Isolation/ledger | **CLOSED** | Missing init raises `IsolationError`; five mocked Claude isolation tests pass. Future ledger records hashes/configuration; historical metadata gap is disclosed. [backends.py:240](../acs/backends.py:240), [PHASE3_ATTACKS.md:500](../results/PHASE3_ATTACKS.md:500) |
| F28 Application honesty | **PARTLY CLOSED** | [redacted: private application material] |
| F29 Dispute-system premise | **CLOSED** | Opening now separates existing merchant-performance disputes from instruction/capture disputes. External novelty claims remain unverified. [main.md:16](../paper/main.md:16) |
| F30 Executable protocol binding | **PARTLY CLOSED** | Bindings/federation honestly marked proposed; no executable fixture or signature-preserving round trip exists. [ABS_v0.3.md:787](../standard/ABS_v0.3.md:787) |

**New findings**

These distinguish defects in new code from incomplete propagation or surviving failure modes. No new P0 found.

| ID | Severity | Finding, reproduction and evidence |
|---|---|---|
| N01 | **P1** | **Hybrid v2 counts rows rather than distinct finder votes.** One finder repeating `model=false` three times beats two finders reporting true and refunds the merchant. With two duplicated opposing votes per finder, reversing finder order changes AG3/refund into AG5/withdrawal. Deduplicate or reject duplicate `(finder,item,attribute)` rows. [hybrid.py:196](../acs/hybrid.py:196), [hybrid.py:226](../acs/hybrid.py:226) |
| N02 | **P1** | **“Every binding attribute per item” is not implemented.** Binding requirements are a flat attribute set; agreed model conformity for item A satisfies a two-item A/B purchase with nothing for B. The parser also drops supplied item IDs. Preserve identities and require `(item,attribute)` coverage. [hybrid.py:178](../acs/hybrid.py:178), [hybrid.py:112](../acs/hybrid.py:112), [hybrid.py:234](../acs/hybrid.py:234) |
| N03 | **P1** | **Gate v2 retains an easy denial bypass and adds an invalid temporal inference.** “The screen is shattered” and “The laptop will not turn on” yield no allegations, allowing AG5 with empty findings. Its delivery reader also treats delivery **before ordering** as supporting on-time delivery. Unknown claim meaning must not imply no contest; validate date intervals. [provenance.py:225](../acs/provenance.py:225), [provenance.py:407](../acs/provenance.py:407), [provenance.py:529](../acs/provenance.py:529) |
| N04 | **P1** | **New “typed” capture checker still rewards substrings.** Otherwise-valid K2 mandates specifying `XPS 140`, `brand="not Dell"` or `plug_type="not EU"` each score **faithful**. Explicit JPY currency also passes. The 36/40 number is checker agreement, not established faithful capture. [capture.py:209](../acs/capture.py:209), [capture.py:229](../acs/capture.py:229), [capture.py:253](../acs/capture.py:253) |
| N05 | **P1** | **Paper’s schema summary contradicts the repaired standard.** Appendix A still specifies `hash` over the body and signatures over that hash; standard now requires `body_hash`, `envelope_hash` and `SignatureInput`. This preserves the insecure specification in a current deliverable. [main.md:218](../paper/main.md:218), [ABS_v0.3.md:853](../standard/ABS_v0.3.md:853) |
| N06 | **P2** | **New replay intervals repeat F21.** Contract v2’s 60/60 interval `[94,100]` treats repeated outputs independently; those decisions cover **22 cases**. Even a simple 22/22 case-level Wilson interval is approximately `[85,100]`. Use a declared case/root-level estimand. [phase3_summary.md:361](../results/phase3_summary.md:361) |
| N07 | **P2** | **Follow-up preregistration is overstated.** Paper says five experiments “are pre-registered”; source heading says “to be pre-registered,” with gate implementation and frozen artifacts still undecided. Call these prospective experiment plans until frozen. [main.md:182](../paper/main.md:182), [PREREGISTRATION.md:1242](../results/PREREGISTRATION.md:1242) |
| N08 | **P2** | **Fresh numerical prose error:** discussion says “the one injection-driven unwanted payment under C0”; hard-set results report **four**, plus the separate adaptive success. [main.md:194](../paper/main.md:194), [main.md:108](../paper/main.md:108) |

I found no duplicated finder attributes in the stored Phase 2/3 logs checked, so N01 does not currently alter their replay totals. The F13 transaction mutation is outside the historical attacker whitelist; it demonstrates incomplete integrity assurance, not inflated historical attack success.

**Paper verdict: BORDERLINE**

I would not yet recommend acceptance. Five deciding reasons:

1. **Useful, reproducible failure evidence:** optimised party-authored evidence defeats otherwise accurate judges.
2. **Much better research honesty:** budget mismatch, attacker changes, historical rules and post-hoc replays are now disclosed.
3. **Weak external validity:** 14 attacked case-sides, label-derived cues, textual photos and no independent labels.
4. **Defence evidence remains insufficient:** gate v2 is evaluated on development data, has fresh bypasses and lacks adaptive evaluation.
5. **Claims exceed the artifact:** hybrid item/majority guarantees and the paper’s cryptographic summary remain wrong; the broad standards contribution obscures the stronger failure-analysis result.

The five cheapest changes likely to move it toward **weak accept**:

1. Centre the paper on the reproducible failure analysis; move most normative standard material to an appendix.
2. Fix N01–N04 or withdraw their corresponding guarantees, then rerun the offline replays.
3. Reconcile Appendix A, counts, preregistration status and case-level intervals.
4. Obtain a small genuinely independent blind label/ambiguity audit, including counterbalanced metadata cues.
5. Run one small, frozen held-out typed gate-on/off experiment with a gate-aware attacker before attempting the entire proposed programme.

**Application notes**

[Redacted in the public copy: notes on private application material.]

**What I could not verify**

- External citations and current law/protocols: no network used. [Items about private material are redacted.]
- Actual served-model identities, reviewer-family independence, or isolation of historical calls lacking metadata.
- Fresh model performance, adaptive gate robustness or independent human accuracy.
- Full JSON Schema/signature conformance: relevant libraries and verification keys were unavailable. All 36 embedded JSON blocks parsed; F.1–F.3 body/context hashes recomputed correctly.
- Seventeen write-dependent tests, publication builds and production payment/protocol operation.
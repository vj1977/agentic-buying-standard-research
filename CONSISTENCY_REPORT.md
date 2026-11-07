# Consistency report: ABS research package, 2026-11-04

Scope: every quantitative claim and every defined term in `paper/main.md`, `standard/ABS_v0.3.md`,
`standard/ABS_ONE_PAGER.md` and three private application documents (redacted in the public copy), checked against the canonical sources:

- `results/PILOT_RESULTS.md` (Phase 1), `results/PHASE2_DISPUTES.md` and `results/phase2_summary.md`
  (Phase 2), `results/PREREGISTRATION.md` (12 amendments, 3 deviations);
- `standard/sim/REPORT.md` and `standard/sim/results.json`, the current post-Audit-2 run: 528 scenarios,
  498 live disputes, E0 89/498 = 17.9%, minimum package 498/498 with 2 escalations, settlement 357
  executable / 9 collection-only / 26 infeasible (v0.1 224 / 4 / 40), anti-scam 33 stopped / 5 refunded /
  3 unrecoverable of 41 (0 / 28 / 13 without the gate), 4 of 8 honest look-alikes blocked;
- `audits/AUDIT_2_REGULATORY.md` for the Audit 2 positions.

Status values: **ok** (matches canon), **stale** (an earlier run or draft; superseded), **wrong** (does not
follow from any source), **unsupported** (no source in the repository). "Fixed" means corrected in this
pass. Files owned by other lanes (`standard/**` and one private document) were not edited; their
rows are for the owners.

Nothing was pushed, published, submitted or committed.

## Summary

| Document | ok | stale | wrong | unsupported | Action |
|---|---|---|---|---|---|
| `paper/main.md` | 52 | 18 | 2 | 2 | all stale and wrong fixed; unsupported clauses removed; body trimmed to 8,999 words |
| `standard/ABS_v0.3.md` | 14 | 11 | 0 | 0 | not edited (standards lane); 13 lines still carry the pre-Audit-2 catalogue numbers |
| `standard/ABS_ONE_PAGER.md` | 4 | 1 | 0 | 0 | not edited; one stale number |
| Three private application documents (redacted) | 7 | 23 | 2 | 5 | redacted in the public copy |
| **Total** | 77 | 53 | 4 | 7 | |

Paper: author's draft about 13,100 body words (15,098 including front matter and appendices); now
8,999 body words (sections 1 to 7), 10,941 in total with abstract and appendices. One `[CHECK]`
remains (PSD3/PSR status at submission). Every entry in `refs.bib` is cited and every citation resolves.
No `[RESULT]` marker remains anywhere.

## 1. `paper/main.md`

Location refers to the author's draft before this pass; the fix column states what the paper now says.

| Location | Claim as stated | Canonical | Status | Fix |
|---|---|---|---|---|
| Abstract | catalogue of 524 scenarios | 528 (`REPORT.md` line 3) | stale | 528 |
| Abstract | E0 decides 17.4% of 494 live disputes | 89/498 = 17.9% | stale | 17.9% of 498 |
| Abstract | 0 unwanted payments in 528 static rows, 400 hard rows, 80 red-team rounds | PILOT_RESULTS 1, 3.3, 3.4 | ok | |
| Abstract | older model 4 of 20; C1 stopped all four | PILOT_RESULTS 3.3 | ok | |
| Abstract | 51 cases, 20 adversarial; 82% and 61% to 98% and 96%; p = 0.008 and 4e-5 | phase2_summary A1 table and paired tests | ok | |
| Abstract | 13 of 20 agent-fault cases charged to the buyer at E0 | E0 confusion matrix, AG1-P row, AG2 column = 13 | ok | |
| Abstract | hybrid 54% to human review; less consistent; every error traced; never deceived | A2: 83/153; 41/51 vs 51/51; 85/85; 0/75 | ok | |
| Abstract | agents refused to lie in 20 of 20 instructions | 0/7 buyer + 0/13 merchant | ok | |
| 1 Contributions | catalogue of 524 scenarios | 528 | stale | 528 |
| 1 | Visa "as if the Cardholder initiated the Transaction"; Amex "deviates from the Card Member-authenticated purchase intent", full terms to follow | `refs.bib` visarules2026, amex2026 (verified; Amex forward-looking) | ok | |
| 2 | Magentic Marketplace: first proposal selected in 60 to 100% of cases | `refs.bib` magentic2025 note (section 5.4) | ok | kept |
| 2 | Khan et al. debate result | `refs.bib` khan2024, ICML 2024 (PMLR 235) | ok | now states the consultancy baseline |
| 2 | Visa Rapid Dispute Resolution and Compelling Evidence 3.0 clauses | no primary source verified (`[CHECK]` C2) | unsupported | clause removed; Ethoca 39 million (ethoca2026) kept |
| 2 | Ethoca alerts prevented more than 39 million chargebacks in 2025 | ethoca2026 | ok | |
| 2 | Directive (EU) 2025/2647 from 20 September 2028; Omnibus Regulation (EU) 2026/1744, 2 December 2027 | adr2025, omnibus2026 | ok | |
| 3 (intro) | "ABS v0.2 has a normative core (Part A)" | current standard is v0.3 | stale | v0.3 |
| 3.5 draft | Flipkart Open Box Delivery as nearest real practice | no source verified (`[CHECK]` C5) | unsupported | sentence made generic (carriers do not open parcels) |
| 3.6 draft | 14 judgement findings used by 10 of the 28 rules; 18 deterministic | REPORT.md judgment-finding table; line 418 | ok | |
| 3.6 draft | quorum confidence 0.80 (standard) | ABS_v0.3 lines 1788, 1919; experiment A3 used 0.7 (Amendment 8), stated in 5.4 | ok | both stated |
| 3.7 draft | no single track; issuer-only card disputes; A2A contractual collection; payout hold only where PSP is payee; guarantee moved to roadmap | AUDIT_2 items 4, 5, 7, CRD-07, PAY-17, LIC-03 | ok | kept |
| 4.1 | 524 scenarios; 494 live; 297 core | 528; 498; 299 | stale | corrected |
| 4.1 | 192 event types; twelve families; seven rail families | REPORT.md line 3; rail table | ok | |
| 4.1 | 5 forged-register scenarios whose payer was the guarantee | results.json by_reason_code ABS-P2 = 5 | ok | |
| 4.2 table | E0 decidable 86/494 (17.4%) | 89/498 (17.9%) | stale | corrected |
| 4.2 table | E3 494/494, 492 determinate, 2 escalated | 498/498, 496, 2 | stale | corrected |
| 4.2 table | v0.1 decidable 86 / 473 / 21 | 89 / 477 / 21 | stale | corrected |
| 4.2 table | core v0.1 gaps / conflicts / contradictions 23 / 4 / 91; v0.2 0 / 0 / 0 | REPORT.md headline | ok | |
| 4.2 table | all families v0.1 decided / correct 494 / 336 of 524 | 498 / 340 of 528 | stale | corrected |
| 4.2 table | all families v0.2 524 / 524 | 528 / 528 | stale | corrected |
| 4.2 table | human review 73 / 2 / 13.9% | 73 / 2 / 73/528 = 13.8% | stale | 13.8% |
| 4.2 table | settlement not executable 22 (v0.2) / 36 (v0.1) | executable 357 / collection-only 9 / infeasible 26 (v0.1 224 / 4 / 40) | wrong (conflated two classes; counts from an earlier run) | corrected to three classes |
| 4.2 table | withdrawal overlay resolves 50 | REPORT.md | ok | |
| 4.2 text | E0 decidability 0 of 30 agent-failure, 0 of 27 user-side, 22 of 26 entry-route | 0/30, 0/27, 23/27 | stale | 23 of 27 |
| 4.2 text | v0.1: 205 scenario-gaps across 8 types (81 rail, 73 human review); 4 unresolved conflicts; 158 contradictions in 58 groups | REPORT.md v0.1 section | ok | |
| 4.2 text | repairs ranked 52 / 19 / 18 / 17 / 11 / 9 / 8 | REPORT.md proposed fixes | ok | |
| 4.2 residuals | 2 undecidable at E3 (serial A vs B) | REPORT.md | ok | |
| 4.2 residuals | 22 instructions not executable | 26 infeasible and 9 contractual-collection-only | stale | corrected |
| 4.2 residuals | eight outcomes have no existing settlement message | 15 rail-and-outcome pairs (results.json standards_gap_table) | wrong | fifteen pairs |
| 4.2 residuals | anti-scam 38 of 45 stopped, 5 refunded, 2 unrecoverable vs 0, 31, 14; 4 honest blocked | 33 of 41, 5, 3 vs 0, 28, 13; 4 of 8 honest blocked | stale | corrected |
| 4.2 residuals | entry routes 5 closed, 3 limit loss, 1 open | results.json entry_gate | ok | |
| 4.2 residuals | signed spec 38 of 47 decidable vs 0 legacy | REPORT.md product spec | ok | |
| 5.1 | pre-registered 4 Nov 2026; 12 amendments; 3 deviations | PREREGISTRATION.md | ok | |
| 5.1 | 7 merchants, about 55 products; models and effort levels; isolation checks; Codex and Gemini unavailable | PILOT_RESULTS 2 | ok | |
| 5.2 | 15 dev, 9 held-out, 10 hard, 8 trust, 8 allowance scenarios; 33 / 20 / 8 / 8 roots | PILOT_RESULTS 2 | ok | |
| 5.2 | H1, H1b, H1c, H7 definitions; red-team 5 x 4 x 4 = 80 rounds | PREREGISTRATION, Amendments 1 to 3 | ok | |
| 5.3 static | 33/33 [90, 100]; 0 in 528 rows; 0/33 [0, 10]; 132 C0 roots; pilot 45 roots; Deviation 1 (H05) | PILOT_RESULTS 1, 3.1 | ok | |
| 5.3 gates | C1 7/24 29% [15, 49]; C2 10/24 42% [24, 61]; monitor 66/72 92% [83, 96]; 0/22 [0, 15]; 0/66 [0, 6] | PILOT_RESULTS 3.2 | ok | |
| 5.3 hard | frontier and haiku 0/20 [0, 16]; grok-4.5 4/20 [8, 42]; X05 and X07 both repeats; C1 stopped 4, 0 false blocks; 15/20 to 19/20; -20 pp [-40, -5]; p = 0.125; clustered [-50, +0] | PILOT_RESULTS 3.3 | ok | |
| 5.3 red-team | 0/20 pairs [0, 16]; 0/80 [0, 5]; 23 refusals (14 of 20 G4); 57 effective, 0/57 [0, 6], 1/57 [0, 9]; EUR 50 more (1,449 vs 1,399); about 1,100 characters; EUR 7 to 15 | PILOT_RESULTS 3.4, 4.4 | ok | |
| 5.3 trust etc. | 0/5 scams all conditions; 6 of 12 escrow; allowance 3 agents 0/8, 0/8 [0, 32], 2/2; audit 40/40, 39/40, kappa 1.00 and 0.94; 528 / 400 / 64 / 48 rows; about 3 s | PILOT_RESULTS 3.5 to 3.8, 4, 5 | ok | |
| 5.4 | case mix 13 / 5 / 3 / 10 / 8 / 12; 4 twin pairs; 13 + 7 adversarial; 8 of 20 withdrawal; 27 card / 24 A2A; 17 real / 34 scripted | PHASE2_DISPUTES 1.2 | ok | |
| 5.4 | A1 408 decisions; A2 3 runs (153); A3 unanimity of two at 0.7; tie-break below 0.7 | PHASE2_DISPUTES 1.4; Amendment 8 | ok | |
| 5.5 table | A1 by level, 8 rows (reason code, liable, remedy, fooled, rail, Brier) | phase2_summary A1 table | ok | |
| 5.5 | H5 0/8 p = 0.008 +16 [+6, +25]; 1/19 p = 4e-5 +35 [+22, +49]; H2 0/14 p = 1.2e-4 +27 [+16, +39]; 0/24 p = 1.2e-7 +47 [+33, +61] | phase2_summary paired tests | ok | |
| 5.5 | rail-dispute rate 14% and 41% to 4% | A1 table | ok | |
| 5.5 | AG1-P to AG2 13 of 20; AG4 0/10 at E0 and E1, 8/10 at E2, 10/10 at E3; AG5 6/12 and 5/12 to 10/12 | confusion matrix; per-code table | ok | |
| 5.5 | E3 residual errors: one AG1-P as AG3, four AG5 as AG3 or AG2 | E3 confusion matrix | ok | |
| 5.5 | twins 2/4 and 0/4 at E0, 4/4 from E2; uncaptured 4/4 at every level; subtle 3/4 to 4/4; remedy 9/11 to 10/11 and 10/11 to 11/11 | twin, severity and remedy tables | ok | |
| 5.5 H3 | 4/20 to 1/20 both; 3/0 p = 0.25 -15 [-30, +0]; 4/1 p = 0.375 -15 [-35, +5]; false claims 3/7 to 1/7 and 1/7; merchant false conformity 3/10, 5/10, 0/10; edited listing 0/3; D46 | fooled tables | ok | |
| 5.5 calibration | 0/6; 91/155; 100/116; 109/110; 21/21; 130/131 at or above 0.85 | calibration table | ok | |
| 5.5 table | architectures, 5 rows | phase2_summary architectures table | ok | |
| 5.5 H6 | 10 vs 0 p = 0.002 -20 [-31, -10]; -53.6 [-66.0, -40.5] vs margin -10; 85/85; 51/70 73%; 149/153; 0/75 vs 3/75; H6b 0/75, quorum escalated 66/75; 80/153 52% vs 42%, ratio 1.24; 0/30 | phase2_summary | ok | |
| 5.5 relaxed | 9/153; 136/144; 136/153; 6/75; 142/150; 3/153; 102/115; 13/75; 100/106; 47/153; 9/153 6% vs 2.4%, ratio 2.45 | post-hoc table | ok | |
| 5.5 stake | 42/51 vs 43/51; 50/51 vs 50/51; 49/50 vs 49/50; p = 1; 0/1 and 1/3 moves | stake-framing table | ok | |
| 5.5 tier 1 | 22/51; 13/51 25% [16, 39]; 9/13; 16/51; 40/51 78% [65, 88]; 4/51; 17/51; 19/51 37% [25, 51]; 17/19; 15/51; 49/51 96% [87, 99]; 2/51; 10 vs 4 p = 0.18; 10 vs 1 p = 0.012; 0/7; 0/13; 2.20 / 2.02; 6 settlements (4 + 2) | tier-1 tables | ok | |
| 5.5 secondary | 15/16 vs 16/16 p = 1; 12/12 [76, 100]; 48/48 and 8/8; 35/40 to 40/40 (Deviation 3); expert kit 40 cases, not labelled; cost 416 / 104 / 475 / 212 / 229 / 32 / 12 / 51, about 1,530; 250 superseded | PHASE2_DISPUTES 2.3 to 2.7; Amendments 10, 11 | ok | |
| 6.1 | E0 decides 17.4% | 17.9% | stale | corrected |
| 6.1 | 205 gaps, 4 conflicts, 158 contradictions | REPORT.md | ok | |
| 6.4 draft | 524 scenarios | 528 | stale | corrected |
| 7 | 524 scenarios; "about a sixth" | 528; 17.9% is under a fifth | stale | corrected |
| Appendix B | AG3 decisions v0.1 206 / v0.2 173 | 210 / 177 | stale | corrected |
| Appendix B | AG4 16/16; AG4-D 5; AG1-M 6/17; AG1-P 31/83; AG2 53/14; AG5 147/79; AG0 18; ABS-C1 7/7; E1 10; H1 2; S1/S2 13; P1/P2 22 | REPORT.md Core 1 | ok | |
| Appendix D | hypotheses H1 to H7, H6b; amendments 1 to 12; deviations 1 to 3; superseded 203, 34 and 3 | PREREGISTRATION.md | ok | |
| refs.bib | 53 entries, all cited; `research/RELATED_WORK.md` does not exist | repo | ok | note for the governor |

## 2. `standard/ABS_v0.3.md` (not edited; standards lane)

| Line | Claim as stated | Canonical | Status |
|---|---|---|---|
| 8 | 524-scenario catalogue; 8 gap types, 4 unresolved conflicts, 58 contradiction groups | 528; 8 / 4 / 58 are right | stale (524 only) |
| 187 | rail-dispute rate 14% and 41% to 4% (51 cases) | ok | ok |
| 245 | 524 catalogue scenarios | 528 | stale |
| 555 to 557 | 524 scenarios; 494 live; v0.1 decided 494, 336 right; v0.2 524 of 524 | 528; 498; 498 and 340; 528 of 528 | stale |
| 565 to 568 | 82% and 61% to 98% and 96%; p from 0.008; 13 of 20; no injection seen at E0 | ok | ok |
| 641 | E0 decided 86 of 494 (17.4%) | 89 of 498 (17.9%) | stale |
| 643 | E3 494 of 494, 492 determinately, 2 escalated | 498 of 498, 496, 2 | stale |
| 1189 | fairness 78% to 96%, p = 0.012 | ok | ok |
| 1259 | 22 of 524 instructions could not be executed | 26 infeasible and 9 collection-only of 528 | stale |
| 1460, 1869 | 82% to 98% | ok | ok |
| 1509, 1881, 1916, 2028 | 9 of 153 (6%) vs 2.4%, ratio 2.45; quorum escalated 93% | ok | ok |
| 1522, 1873 | A2 54% human review; 0 reviews and 98% for A1 | ok | ok |
| 1547 | 73 of 524 scenarios reached a human | 73 of 528 (13.8%) | stale |
| 1788, 1919 | quorum threshold 0.80 (design) | design value; experiment used 0.7, disclosed | ok |
| 1887 | 34 of 51 cases scripted | ok | ok |
| 1933 | "The catalogue has 524 scenarios" | 528 | stale |
| 2021 | 17.4% decidable at E0 | 17.9% | stale |
| 2071, 2072, 2645, 2647 | 0 in 528 and 400 rows; grok-4.5 4 of 20; C1 stopped all four; attacker refused 23 | ok | ok |
| 2131, 2132 | withdrawal right not mentioned in 5 of 51 R0 cases; 78% to 96% | ok (PHASE2_DISPUTES 2.4) | ok |
| 2655 | H7 untestable | ok | ok |
| 2669 to 2678 | 69% to 96%, 47% to 94%; 82% to 98%, 61% to 96%; 130 of 131; 25% to 37% p = 0.18; 0 of 7; 0 of 13; 6 agent-fault claims paid by the merchant; A2 54% / 97% / 80% / 0 of 75 / 85 of 85; 48 of 48 | ok | ok |
| 2680 | 524 scenarios; 17.4% at E0; 22 infeasible executions | 528; 17.9%; 26 infeasible and 9 collection-only | stale |
| 2723 | without the gate, 45 scam cases: 0 stopped, 31 refunded, 14 unrecoverable | 41 cases: 0 / 28 / 13; with the gate 33 / 5 / 3 | stale |
| 989 | reason-code enum includes AG0, AG1-M, AG1-P, AG1-C, AG2, AG3, AG4, AG4-D, AG5 | matches paper and rulebook v1.3 | ok |
| 2615 | H5 to H7 pre-registered (Amendments 1, 2, 5) | PREREGISTRATION | ok |

Thirteen lines carry the pre-Audit-2 catalogue (524 / 494 / 336 / 86 / 492 / 22 / 17.4% / 45-31-14). The
owner should re-run `standard/sim/run.py` numbers into the text or cite `REPORT.md` directly.

## 3. `standard/ABS_ONE_PAGER.md` (not edited)

| Line | Claim | Canonical | Status |
|---|---|---|---|
| 57 to 60 | 82 and 61 percent to 98 and 96 of 51 cases; rail 14 and 41 to 4; half the cases to humans | ok | ok |
| 61 to 65 | 2.45 times; 4 of 20, mandate gate stopped all four, no false block; agents did not lie; 78 to 96 percent; provider must be a party | ok | ok |
| 66 | "Against a 524-scenario catalogue the rules decide every case" | 528 | stale |
| 23 to 32 | liability rule: non-conformity or steering to merchant; explicit term incl. captured requirement or guess where told to ask to provider; capture failure to provider; did what was said not what was meant to user with withdrawal right | matches Amendment 7, rulebook v1.3, paper 3 | ok |
| 38 to 50 | Decision Center: models find facts, deterministic rules decide, human review; no waiver of card rights; settlement on existing rails, no reversal against a refusing merchant, chargeback via issuer, hold only where licensed PSP is payee, ABS holds no money; "designed against ... not certified" | Audit 2 positions | ok |

## 4 to 6. Private application material (redacted)

Sections 4 to 6 checked three private documents against the same sources. They are omitted from the public copy.

## 7. Terms

| Term | Canon | Paper | ABS v0.3 | One-pager |
|---|---|---|---|---|
| Hypotheses H1 to H7, H6b (Amendment 2 numbering) | PREREGISTRATION | ok | ok (L2615) | n/a |
| Evidence levels E0 to E3 (E3 includes contestable delivery evidence) | Amendment 5 | ok | ok | ok |
| Arbiters A1 end-to-end, A2 hybrid, A3 cross-family quorum | Amendments 1, 8 | ok | ok (also uses A1 to A15 as section labels) | described, not named |
| Reason codes AG0 to AG5, AG1-M, AG1-P, AG1-C, AG4-D | rulebook v1.3; v0.3 enum | ok | ok | names only |
| Liability rule wording | Amendment 7 + v1.3 capture duty | ok | ok | ok |
| Audit 2 positions | AUDIT_2 | ok | ok (PLACEHOLDERS confirms applied) | ok |
| "designed against", never "compliant" | AUDIT_2 | ok | ok | ok |
| Amex draws the line; ABS contributes procedure, evidence, taxonomy | AUDIT_2 | ok | ok (L2299) | ok |

## 8. Notes for other lanes

- `standard/sim/results.json`: inside `antiscam.summary.B_abs_gate.results` the counter
  `scam_stopped_before_purchase` is 38 while `stopped` is 33 (and the per-result counters sum to 46 for 41
  scams). The headline 33 / 5 / 3 is used everywhere; the sub-counter looks like a double count and should
  be checked by the sim lane.
- `research/RELATED_WORK.md` does not exist. The paper's related-work section was aligned to the two
  corrections named in the brief (Magentic 60 to 100%; Khan et al. ICML 2024 with consultancy baselines)
  and to `refs.bib`. Reconcile again if that file appears.
- `README.md` title still says "ABS v0.1 safety controls"; the Phase 1 controls were designed against v0.1
  and the write-ups say so, so it is historical rather than wrong, but the README could point to v0.3.

## 9. Items only the founder can resolve

[Items about private application material are redacted in the public copy.]

1. **Label the expert baseline.** `expert/cases.html`, 40 cases; export labels; run `expert/score_expert.py`;
   do not open the answer key first. The paper says "built, not labelled". If labelled before submission, add
   the result by dated amendment.
2. **Paper:** one `[CHECK]`, the PSD3/PSR status at submission (Council documents ST 8543/26 and 8535/26).
3. **Owned by other lanes, not his:** the 11 stale rows (13 lines) in `standard/ABS_v0.3.md`, one in
   `standard/ABS_ONE_PAGER.md`, and the anti-scam sub-counter in `results.json`.

## Correction 2026-11-04 (after this report)
The sim lane found and fixed an anti-scam counter bug (X07 forged-register scams were counted as neither scam nor honest after
Audit 2). Canonical anti-scam headline is now **38 stopped / 5 refunded / 3 unrecoverable of 46 scams** (without the gate
0 / 31 / 15; buyer loss EUR 1,837 vs EUR 4,783); honest look-alikes 4 of 8 blocked. Every "33 of 41" above is superseded;
the paper was updated to the new figures.


## Audit 1 (2026-11-04, final consistency and claims pass)

Scope: `paper/main.md` (and its figures), `standard/ABS_v0.3.md`, `standard/ABS_ONE_PAGER.md`,
three private application documents (redacted) and
`expert/score_expert.py`, after Audit 1 (`audits/AUDIT_1_INDEPENDENT_AI_REVIEW.md`, 30 findings, read-only review of commit
3a6746d) and the four fix lanes. No model was called. Sources of truth: `standard/sim/REPORT.md` ("Post-audit
(Audit 1)"); `results/AUDIT1_CORRECTIONS_PHASE1_2.md`; `results/CHRONOLOGY.md`; `rulebook/VERSIONS.md`;
`results/PHASE2_DISPUTES.md` section 3 and `results/phase2_summary.md`; `results/PHASE3_ATTACKS.md` section 6
and `results/phase3_summary.md` ("Post-audit (Audit 1)"); `results/PHASE3B_PROVENANCE.md` (post-audit headline,
section 10) and `results/phase3b_summary.md` ("Post-audit (Audit 1)"); `results/PREREGISTRATION.md` ("Post-audit
amendment (Audit 1)"). Labels: *correction* (a reporting, inference or code defect fixed), *relabel* (counts
unchanged, name corrected), *descriptive* (a recount of stored records), *exploratory* (code or labels written
after the audit, applied to stored outputs). Historical numbers stay in the results files beside the new ones.

### Changed numbers (old -> new -> source)

| # | Quantity | Old | New | Label | Source |
|---|---|---|---|---|---|
| 1 | Simulation, E3, v0.2 | 498/498 decided (100%) | 496 determinate + 2 escalated of 498, 0 with no rule; consistency against stipulated facts, not evidence sufficiency | correction (F17) | sim REPORT post-audit |
| 2 | Simulation, undecidable at E3 | 0 | 2 escalated (ABS-H1, ABS-S0073/74) + 0 with no rule | correction (F17) | same |
| 3 | Simulation, E0 | 89/498 decidable | 89/498 (17.9%) determinate | relabel (F17) | same |
| 4 | Simulation, all scenarios, v0.2 | 528 decided / 528 correct | 526 determinate, 2 escalated; 528/528 consistent with stipulated ground truth | correction (F17) | same |
| 5 | Simulation, all scenarios, v0.1 | 498 decided / 340 correct | 498 determinate, 30 no rule; 340/528 consistent | relabel (F17) | same |
| 6 | Settlement, v0.2 (v0.1) | 357 / 9 / 26 (224 / 4 / 40) | 334 / 9 / 26 of 369 funds-moving (224 / 4 / 40 of 268) | correction (F17) | same |
| 7 | Anti-scam with the gate | 38 / 5 / 3 | 38 stopped / 5 refunded / 0 conditional / 3 unrecoverable | correction (F25) | same |
| 8 | Anti-scam without the gate | 0 / 31 / 15 | 0 / 28 / 3 conditional (UK push-payment reimbursement uncertain) / 15 | correction (F25) | same |
| 9 | Buyer loss with the gate | EUR 1,837 | EUR 938.00 and INR 899.00 (the old total added currencies) | correction (F25) | same |
| 10 | Buyer loss without the gate | EUR 4,783 | EUR 3,425.99, INR 899.00, USDC 458.00, GBP 0 to 569.00 conditional | correction (F25) | same |
| 11 | Simulation conformity matching | substring | exact identifiers with declared equivalents and tolerances; no outcome changed | correction (F16) | same |
| 12 | Phase 1 red-team, executed attacks | 0 (unscoped) | 0/80 with the claude-opus-5-5 attacker; with a grok-4.5 attacker (arm R) the grok-4.5 agent executed 1/12, claude-fable-5-1 0/12 | correction (F01) | `PILOT_RESULTS.md`; `AUDIT1_CORRECTIONS_PHASE1_2.md` F01 |
| 13 | Capture probe | 40/40 (35/40 under the pre-registered checks) | typed checker: 36/40 faithful [77, 96], 2 safely stricter, 2 fail; lenient 37 / 3 / 0 | exploratory (F18) | `AUDIT1_CORRECTIONS_PHASE1_2.md` F18 |
| 14 | A2 scripted manipulation | 0/75 [0, 5] | 0/25 cases [0, 13]; 0/75 outputs kept as description | correction (F21) | same, F21 |
| 15 | A1 fable scripted manipulation | 3/75 [1, 11] | 1/25 cases [1, 20] | correction (F21) | same |
| 16 | A3 quorum and single-finder hybrids | 0/75 each | 0/25 cases [0, 13] each | correction (F21) | same |
| 17 | Relaxed rule, scripted manipulation | 6/75 [4, 16] (grok-only 13/75) | 2/25 cases [2, 25] (grok-only 5/25 [9, 39]) | correction (F21) | same |
| 18 | Case independence | 51 cases | 44 source references in 27 scenarios; 13 cases share a root | disclosure (F21) | same |
| 19 | grok-4.7 liable party, E1 / E2 | 37/51 / 46/51 | 36/51 / 45/51 (three refunds above the disputed amount are invalid outputs); E0, E3, H2, H3, H5 unchanged | exploratory (F20) | `PHASE3_ATTACKS.md` 6.4; `PHASE2_DISPUTES.md` 3 |
| 20 | Liable party at E3 against the current v1.4 labels | 50/51 (fable), 49/51 (grok), v1.2 labels | 45/51 and 44/51: benchmark-vs-current-rule distance, not arbiter error (D31 AG1-P -> AG4-D; D32 to D35 AG2 -> AG1-C; D43 deny -> undetermined) | exploratory (F10) | `AUDIT1_CORRECTIONS_PHASE1_2.md` F10; `rulebook/VERSIONS.md` |
| 21 | Residual route (was "rail-dispute rate") | 14% / 41% -> 4%, chargeback / recall / unrecoverable | same rates; issuer dispute / contractual collection / unavailable | relabel (F11) | same, F11 |
| 22 | Historical hybrid decision rule | conformity only when every binding attribute is known at >= 0.7 | 0.7 governed only the tie-break; two D22 merchant refunds rest on quantity findings at 0.60 and 0.55 | correction (F08) | `PHASE3_ATTACKS.md` 6.3 |
| 23 | A2, Phase 2, decision contract v2 | review 83/153, 68/70 correct when decided | 93/153, 60/60 | exploratory (F08, F09) | same |
| 24 | Cross-family error ratio quoted with the 93% quorum review | 2.45 | 1.24 under the strict rule (with A3 reviewing 143/153 = 93%); 2.45 belongs to the post-hoc relaxed rule (A2 9/153 reviews) | correction (F28) | `PHASE2_DISPUTES.md` 2.2; `phase2_summary.md` |
| 25 | Architecture comparison under attack | A1 fable 12/14 vs A2 6/14, p = 0.031, as an architecture result | unequal budgets (10 vs 5), descriptive; at k = 5: 10/14 vs 6/14, 4 / 0 discordant, p = 0.125, -29 pp [-50, -7]; A2 spends 3.0 arbiter-side calls per attempt against 1.0 | correction (F02) | `PHASE3_ATTACKS.md` 6.1 |
| 26 | Fooled within 5 attempts, other arms | - | grok E3 14/14 (vs A2 p = 0.008), fable E1 13/14 (p = 0.016) | descriptive (F02) | same |
| 27 | "Attempts per success" | 3.9 / 1.5 / 1.8 / 8.8 | renamed aggregate attempts expended per successful case-side; first success among fooled case-sides: mean 2.25 (median 1) fable E3, 1.50 grok E3, 1.79 fable E1, 2.17 A2; D05 and D06 censored at 10, 8 A2 case-sides censored at 5 | relabel (F23) | `PHASE3_ATTACKS.md` 6.2 |
| 28 | "Within about four attempts" | in the paper and [redacted: private material] | withdrawn: describes neither quantity | correction (F23) | same |
| 29 | H8 status | supported (confirmatory) | as computed (12/14 vs 1/14, p = 0.001); the attacker was substituted after outcomes were seen, so exploratory development; a frozen-attacker confirmation is pre-registered, not run | correction (F19) | `CHRONOLOGY.md` row 22; `PREREGISTRATION.md` post-audit amendment |
| 30 | A2 under attack, decision contract v2 | 10/67 attempts, 7/14 case-sides | 5/67, 5/14; with gate v2 0/67 | exploratory (F08) | `PHASE3_ATTACKS.md` 6.3 |
| 31 | H10 | 12/14 -> 1/14, p = 0.00098, supported | kept as computed, labelled confounded; same-call effect leads: fable 11/14 -> 1/14 (10 / 0, p = 0.002), grok 12/14 -> 1/14 (11 / 0, p = 0.001) | correction (F03) | `PHASE3B_PROVENANCE.md` post-audit headline 1 |
| 32 | What the gate's rejections were | "uncited" 10 of 12, 13 of 13 | format / provenance / contradiction: fable attacks 10 / 2 / 0; grok attacks 13 / 0 / 0; fable baseline 21 / 3 / 0; grok baseline 16 / 0 / 0; A2 attacked 0 / 7 / 0; A2 baseline 0 / 8 / 0 | descriptive (F04) | same, headline 2 |
| 33 | Gate v2 on stored outputs | - | attacks through 0/14 (fable), 0/14 (grok), 0/67 (A2); baseline decided wrongly 3 -> 0; review fable 24/50 -> 26/50, grok 16/18 -> 17/18, A2 91/153 -> 110/153; 31 baseline passes rest on content v2 cannot read | exploratory (F05) | same, headline 3 |
| 34 | Cohort name | "honest cases" | baseline Phase 2 workload (25 of 51 cases carry a scripted adversary; 24 of the 50 valid GB rows) | relabel (F22) | same, headline 4 |
| 35 | Who carries the review (gated fable) | 12/21 merchant-liable, 10/10 provider, 2/19 buyer | by claimant truth: 22 of 31 true claimants vs 2 of 19 unfounded claims; benign stratum 12/13 vs 0/13 | descriptive (F22) | same |
| 36 | Integrity flag shown to the arbiters | `hash_chain_valid` checked a parallel chain against its own anchor | displayed record compared with the chain, head with an independent anchor; all 228 stored packages byte-identical, no number changes | correction (F13) | `AUDIT1_CORRECTIONS_PHASE1_2.md` F13 |
| 37 | Isolation | "checked on every request" | fails closed now; 866 stored A1 Claude calls with metadata carry the init event; 672 A2 fact-finder calls kept none and cannot be checked | correction (F27) | `PHASE3_ATTACKS.md` 6.5 |
| 38 | Catalogue chronology ([redacted: private material]) | [quote from private material redacted] | first catalogue commit 62ec0eb at 00:55:45Z on 4 November, after the first model runs (from 23:39Z on 3 November); no catalogue scenario was sent to a model (Amendment 9) | correction (F28) | `git log -- standard/scenarios/catalogue.json`; `CHRONOLOGY.md` table 2 |
| 39 | Pre-registration status | blanket "pre-registered", "every amendment committed before the runs it governs" | per-analysis statuses: prospective (Phase 1 confirmatory, gate coverage, Phase 2 H2/H5, capture-duty arm, stake framing), design informed by earlier data (hard set, red-team, Phase 3b), amended after data (H05 re-run, Phase 1 clustered intervals, capture checker, tier-1 scoring, Phase 3), exploratory (pilot, post-hoc analyses, every Audit 1 re-analysis) | correction (F19) | `CHRONOLOGY.md` |

### Claims withdrawn from every deliverable

"Never deceived"; "evidence beats architecture" and "architecture matters under attack" as findings; "the
independent record decides, not the judge" and "only records the parties cannot author decide"; "every card
dispute rests on authorisation" and "no reason code fits" (replaced by the narrower gap: faithful execution of
delegated intent, i.e. instruction disputes AG1-P and capture disputes AG1-C, with AG2 the buyer-side
counterpart); "within about four attempts"; "honest cases"; "the hybrid halved attack success" as a controlled
result; "every binding attribute known at 0.7" for the historical hybrid; the blanket "pre-registered" (the
paper's title no longer carries it). Remaining mentions are only in explicit withdrawn-claim lists, old -> new
notes, "Do not say" lists and [redacted: private material] that explain the withdrawal.

### Where each deliverable stands

- `paper/main.md`: abstract, Sections 1 to 7 and Appendix D revised to the claim above; new Section 5.7
  "Post-audit corrections" citing the audit as an internal review (`refs.bib` entry `audit1`); the v1.2
  benchmark separated from the v1.4 rules; Phase 3b leads with the same-call effect; body 8,969 words
  (limit 9,000). Figures: Fig. 1 labelled as the v1.2 benchmark; Fig. 2 shows the same-call comparison with
  gate v2 labelled exploratory; Fig. 3 uses the baseline Phase 2 workload and adds the gate v2 point (hollow,
  exploratory). `paper/build.sh` passes and `build/main.pdf` renders (24 pages). Details:
  `paper/PLACEHOLDERS.md`, "Post-audit pass (Audit 1)".
- `standard/ABS_v0.3.md`: every number above that it quoted, the stale A4 preamble sentence (rulebook v1.4
  now implements the binding-term rule; no model has run under it) and the closing sentences of Appendix E,
  with a dated "Numbers carried in" note. `standard/ABS_ONE_PAGER.md`: the same numbers and claims.
- [redacted: private application material]
- `expert/score_expert.py`: every agreement measure is reported against both the v1.2 (historical) and the
  v1.4 labels; a relabel check compares the key's changed ids with the documented list (X89C5F/D31,
  X9FC6C/D43). Tested with synthetic label files (`tests/test_expert_score.py`).

### Checks run (2026-11-04)

- Stale-token and withdrawn-phrase sweep over the six deliverables (never deceived; evidence beats
  architecture; independent record decides; only independent records; no reason code fits; every card
  dispute; rests on one question; within about four / 4 attempts; honest cases; halved; every binding
  attribute; 0.031; 357; 1,837; 4,782/4,783; 498/498; 498 of 498; 100% decided; 40/40 and 40 of 40; 0/75 and
  0 of 75; 2.45; attempts per success; architecture matters): every remaining hit is a withdrawn-claim list,
  an old -> new note, case-level or re-score scoped, labelled as the relaxed or unequal-budget figure, or an
  unrelated use (the scoring audit's 40/40; "every card dispute right"; "every binding attribute has a unit").
- `python3 -m unittest discover -s tests -t .`: 208 tests OK. `python3 -m unittest discover -s standard/sim
  -t .`: 55 tests OK.
- `standard/ABS_v0.3.md`: 36 of 36 JSON blocks parse; every section reference (A1 to A15, B1 to B5 and
  their subsections) resolves to a heading or its parent; Appendix A to F all present. Every `*.json` in
  the repository parses.
- `paper/build.sh`: figures regenerated with every plotted number parsed from `results/` and asserted
  against `main.md`; pandoc without warnings; 3 figures, 50 internal links, 47 references, 1 `[CHECK]`
  (PSD3/PSR); body 8,969 words.

### Unresolved

- Needs new model calls: the five pre-registered follow-up experiments (about 1,800 calls); any v1.4 run.
- Needs a person: the blind expert labels; the F24 counterbalanced case set; [redacted: three items about private application
  material; the reviewer is described publicly only as an independent AI reviewer (another model family)].
- Outside these files: the protocol binding fixture (F30) and the A1/A2 prompts for v1.4 (F10, future runs);
  the paper's `[CHECK]` C6; the first pdflatex run of `paper/build/main.tex`.

## Audit 3 re-check (2026-11-04, paper restructure and [redacted] pass)

Scope: `paper/main.md` and its figures, `standard/ABS_v0.3.md` (Appendix F, one sentence),
`expert/answer_key.json` (D43's reason text) and three private application documents (redacted), after the independent re-check `audits/AUDIT_3_INDEPENDENT_AI_RECHECK.md` (13 of 30
findings closed, 16 partly closed, 1 open; new findings N01-N08; paper verdict borderline). No model was
called. Sources of truth: `results/phase3_summary.md` and `results/phase3b_summary.md` ("Post-audit (Audit
3)"); `results/PHASE3_ATTACKS.md` Section 7; `results/PHASE3B_PROVENANCE.md` Section 11 and the Audit 3 note
under its post-audit headline; `results/AUDIT1_CORRECTIONS_PHASE1_2.md` ("Audit 3 re-check");
`results/PREREGISTRATION.md` ("Post-audit amendment (Audit 3 re-check)"); `results/CHRONOLOGY.md` rows 25 and
26; `results/PILOT_RESULTS.md` and `results/gate_coverage.md` (Phase 1 units); ABS v0.3 A4.5, A5.3, A5.8 and
B6; `standard/ADOPTION_AND_CONFIRMATION.md`. Labels as in the Audit 1 section, plus *unit* (the same count
with its interval moved to the independent unit).

### Changed numbers (old -> new -> source)

| # | Quantity | Old | New | Label | Source |
|---|---|---|---|---|---|
| 1 | A2 Phase 2, hybrid decision contract | v2: review 93/153 runs, decided 60, correct 60/60 = 100% [94, 100] (runs) | v3: review 99/153 runs, correct 54/54 of decided (counts only); cases decided correctly 20/20 [84, 100]; cases with a run sent to review 35/51 [55, 80] (v2 at case level: 22/22 [85, 100], 33/51 [51, 76]) | exploratory (N01, N02); unit (N06) | `phase3_summary.md` "Post-audit (Audit 3), N01, N02 and N06"; `PHASE3_ATTACKS.md` 7.1 |
| 2 | A2 attacked, decision contract | v2: 5/67 attempts, 5/14 case-sides | v3: 5/67 attempts, 5/14 case-sides [16, 61]; with gate v3 0/14 [0, 22] | exploratory (N01, N02) | same |
| 3 | A2 Phase 2 as run, review and correct of decided | 83/153 = 54% [46, 62]; 68/70 = 97% [90, 99] (runs) | 83/153 and 68/70 as counts; cases with a run sent to review 33/51 = 65% [51, 76]; cases decided correctly 27/28 [82, 99] | unit (N06) | `phase3_summary.md` "Post-audit (Audit 3), N06" |
| 4 | Paper architecture table (A1, A2, A3, single-finder hybrids) | review and correct-of-decided with Wilson intervals over 153 runs (e.g. 150/153 [94, 99], 143/153 [88, 96]) | run counts without intervals; intervals only on case-level columns (scripted manipulation of 25 cases; consistency over 51 cases); a contract v3 row added | unit (N06) | `phase2_summary.md` architecture table |
| 5 | Gate on the stored outputs | v2: attacks let through 0/14, 0/14, 0/67; baseline decided wrongly 0; fable baseline review 26/50; true claimants 22/31, unfounded claims 4/19; A2 cases with a run reviewed 41/51 | v3: 0/14, 0/14, 0/67; 0; review 40/50 = 80% [67, 89]; true claimants 25/31, unfounded claims 15/19; A2 as run + gate v3 43/51 [72, 92]; contract v3 + gate v3 44/51 [74, 93] | exploratory (N03, F05) | `phase3b_summary.md` "Post-audit (Audit 3)"; `PHASE3B_PROVENANCE.md` 11 |
| 6 | Passes on content no reader checks | v2: 33 (31 baseline, 2 attacked A2); 14 of them fable baseline | v3: all 33 go to review (fable's 14 account for 26/50 -> 40/50) | exploratory (F05) | same |
| 7 | Capture probe | typed checker "36/40 faithful [77, 96]" | checker agreement 36/40 strict, 37/40 lenient (checker v2, same class for all 40 mandates); case level 5/8 conversations [31, 86]; the interval over 40 mandates is withdrawn | unit and name (N04); checker v2 exploratory | `AUDIT1_CORRECTIONS_PHASE1_2.md` "Audit 3 re-check"; `PREREGISTRATION.md` Audit 3 section 2 |
| 8 | Follow-up experiments (about 1,800 calls) | "are pre-registered and not run" | prospective experiment plans (not yet frozen preregistrations) | correction (N07) | `PREREGISTRATION.md` Audit 3 section 3; `CHRONOLOGY.md` row 26 |
| 9 | Injection-driven unwanted payments (paper discussion) | "the one injection-driven unwanted payment under C0" | four on the hard set (grok-4.5, 4 of 20 C0 episodes from two scenarios), plus the separate executed adaptive attack | correction (N08) | `PILOT_RESULTS.md` headline 2 and 3 |
| 10 | Paper Appendix A envelope | `hash` over the body; signatures over that hash; EdDSA or ES256 | `body_hash`, `envelope_hash` over the rebuilt signed context, JWS payload = SignatureInput, full 64-hex anchor (16-hex locator only finds it); Ed25519 or ES256, EdDSA for legacy verification only | correction (N05) | ABS v0.3 A5.3, A5.8, `$defs/Signature` |
| 11 | Phase 1 monitor coverage | 66/72 samples = 92% [83, 96] | 22 of 24 trap carts blocked in all three samples, 92% [74, 98] (Wilson over carts, computed from the per-cart table); 66/72 samples as a count | unit | `gate_coverage.md` |
| 12 | Phase 1 hard set | grok-4.5 4/20 [8, 42]; frontier 0/20 [0, 16]; C1 - C0 -20 points [-40, -5] (episode bootstrap) | 4 of 20 C0 episodes from two of ten scenarios, scenario-clustered interval [0, 50]; frontier 0 of 20 episodes, no interval; -20 points, scenario-clustered [-50, +0] | unit | `PILOT_RESULTS.md` headline 2 |
| 13 | Phase 1 red-team | 0/20 pairs [0, 16], 0/80 rounds [0, 5] | 0/20 target-goal pairs [0, 16] over 80 rounds | unit | `PILOT_RESULTS.md` headline 3 |
| 14 | Phase 1 static set | 33/33 [90, 100], 0/33 [0, 10] per agent and condition | 33 roots (24 scenarios, the 9 held-out at two seeds), no interval | unit | `PILOT_RESULTS.md` sample sizes |
| 15 | D43 reason under v1.4 (`expert/answer_key.json`) | prerequisites missing: prior_express_consent, acknowledged_loss_of_right, trader_confirmation | performance_begun listed first, as the engine and `phase2_summary.md` give it; label unchanged (AG5 / buyer / undetermined) | correction (F12 remainder) | `phase2_summary.md` v1.4 section; `acs/rule_engine.withdrawal_status` |
| 16 | Standard Appendix F, validator | "written for this correction outside the repository" | in the repository (`tools/schema_check`, with tests) and run in CI | correction (F15 remainder) | `.github/workflows/ci.yml` |

### Claims withdrawn or tightened in this pass

"Every defect fixed" or "I reproduced every one and fixed it" (now the closure state: 13 closed, 16 partly
closed, 1 open, 8 new; the counterexamples reproduced and repaired; experimental gaps named); "only records
the parties did not write" for the gate (its independent tier holds signed party records; v3 also needs the
record's content to support the finding); "H8 supported" (exploratory); "Phase 1 found nothing" unscoped
(the static and frontier null only); "faithful capture" without "checker agreement"; "are pre-registered" for
the follow-ups; any interval over runs or attempts.

### Where each deliverable stands

- `paper/main.md`: retitled "Who pays when the agent is wrong? Evidence, adjudication and optimised evidence
  fabrication in agentic commerce" and restructured around the failure analysis (Phase 2 evidence, Phase 3
  fabrication, Phase 3b and the v3 replays as a safety-usefulness result); the standard's normative detail
  moved to Appendices A and B or left to the standard by reference; a short design section on who confirms
  the deciding fact and the staged adoption path, marked design, not evaluated; closure state in 9.5. Body
  8,105 words. Figures 2 and 3 show gate v3; Figure 3 plots A2 review at case level. An independent
  read-only review of the restructured text against the sources found one schema-field error (Appendix A's
  Mandate listed `accepted_deviations`, removed in v0.3), one closure overclaim and ten wording items; all
  fixed in commit 105e451. Details: `paper/PLACEHOLDERS.md`, "Audit 3 re-check pass".
- [redacted: private application material]
- `standard/ABS_v0.3.md`: Appendix F's validator sentence only. Still stale elsewhere (left for the
  standards lane): "pre-registered, not run" for the follow-ups at about lines 1627, 2554, 2579 and 2806, and
  "36 of 40 faithful" at about line 3465.
- `expert/answer_key.json`: D43's reason text; labels unchanged.

### Checks run (2026-11-04)

- Withdrawn-phrase and stale-number sweep over `paper/main.md` and three private files, redacted ("every
  defect", "never deceived", "independent record decides", "within about four", "honest cases", "faithful"
  without "checker agreement", "H8 supported", "are/is pre-registered" for the follow-ups, "one
  injection-driven", "a year of", "money gives", "did not write", "found nothing", run-level intervals such
  as [94, 100], [0, 5], [46, 62], [90, 99], [83, 96], [8, 42]): every remaining hit is a never-say list, a
  change log, an old -> new note, a negation ("not established faithful capture"; "do not support the claim
  that independent records decide") or an unrelated use ("faithful execution of delegated intent"; an agent
  that "did not write down" a requirement).
- `python3 -m unittest discover -s tests -t .`: 267 tests OK. `python3 -m unittest discover -s standard/sim
  -t .`: 55 tests OK. `python3 -m tools.schema_check standard/ABS_v0.3.md` (the CI step): all checks passed
  (4 positive examples valid, 8 negative invalid, 4/4 integrity checks). `python3
  tools/schema_check/check_doc.py standard/ABS_v0.3.md`: 0 errors.
- `paper/build.sh`: every plotted number parsed from `results/` and asserted against `main.md`; pandoc
  without warnings; 3 figures, 51 internal links, 48 references, 1 `[CHECK]` (PSD3/PSR); body 8,105 words;
  `build/main.pdf` 27 pages, figures rendered and inspected.

### Unresolved

- Needs new model calls: the five prospective experiment plans (about 1,800 calls); a v1.4 arbiter run.
- Needs a person: independent blind labels and the counterbalanced case set (F24, the one open finding);
  [redacted: items about private application material]; the paper's PSD3/PSR `[CHECK]`.
- Outside these files: the standard's stale follow-up and capture wording listed above; gate convergence on
  the A5.7 provenance description; the transaction header (date, rail, currency, descriptor, buyer) not
  committed in the chain; `results/PILOT_RESULTS.md` says "only the monitor catches within-mandate failures"
  although C2 blocks three trap carts with no mandate violation on risk signals (the paper now says "that
  carry no risk signal").

## Label adjudication (2026-11-04, founder's partial labels and two model runs)

Scope: the founder's blind labels on 8 of the 40 kit cases, two web-UI model label runs on all 40, and every
disagreement with the v1.4 key, adjudicated by the author side (not independent); no model calls. Sources of truth:
`results/expert_baseline_partial.md` (`expert/score_expert.py`), `results/LABEL_ADJUDICATION_2026-11-04.md` and
`expert/answer_key_v1.4_adjudicated.json` (both generated by `python3 -m acs.label_adjudication`),
`results/PREREGISTRATION.md` "Post-audit amendment (label adjudication)". `expert/answer_key.json`,
`data/disputes/cases.json` and `results/phase2_summary.md` are unchanged. Labels as in the sections above;
*exploratory* = written after the data were seen.

### Changed numbers (old -> new -> source)

| # | Quantity | Old | New | Label | Source |
|---|---|---|---|---|---|
| 1 | Expert baseline | "still to be labelled" (paper 9.1); "not yet labelled" ([redacted: private material]) | partial, author-labelled, not independent: founder 8 of 40, liable party 5/8 = 62% [31, 86] against the v1.4 and historical keys (kappa 0.40), remedy 6/8 (kappa 0.00, not meaningful: no variance) | exploratory | `results/expert_baseline_partial.md` |
| 2 | Model labels at E3, liable party (not expert labels) | - | 12/12 and 11/12 against the v1.4 key (one run is Grok; batch mode; run 2 leaked facts across cases) | descriptive | `expert/model_labels/score_run*_unnamed.md` |
| 3 | v1.4 ground-truth labels that differ from v1.2 | six (D31, D32-D35, D43) | seven: D37 AG2 / buyer / deny -> AG1-P / agent provider / refund (signed "my usual printer ink" binds under v1.4); D37's v1.2 label unchanged | exploratory (ground-truth error) | `results/LABEL_ADJUDICATION_2026-11-04.md`; `PREREGISTRATION.md` label adjudication section 1 |
| 4 | Phase 2 A1 liable party against v1.4 labels, E3 (paper Section 5 and Appendix G) | 45/51 and 44/51 | 44/51 and 43/51 (every level drops by one: fable 37, 37, 40, 44; grok 26, 31, 39, 43); old figure kept beside it | exploratory (corrects an Audit 1 exploratory figure) | same, "Phase 2 re-score" |
| 5 | Phase 2 A1 liable party, v1.2 headline (42 -> 50, 31 -> 49 of 51) | as reported | unchanged | as run | `results/phase2_summary.md` |
| 6 | Same, on the kit cells the shown evidence can decide | - | fable 31/45 = 69% [54, 80] -> 44/51 = 86% [74, 93]; grok 22/45 = 49% [35, 63] -> 43/51 = 84% [72, 92]; only the 40 kit cells read, so not an estimate over all decidable cells | exploratory | `results/LABEL_ADJUDICATION_2026-11-04.md` |
| 7 | Model runs, liable party (not expert labels) | 26/40 and 32/40 against the v1.4 key | unchanged; 35/40 and 24/40 against the adjudicated key | exploratory | same; `expert/model_labels/README.md` |
| 8 | Post-audit amendments | two (paper Section 4; [redacted: private material]) | three | correction (count) | `results/PREREGISTRATION.md` |

### Claims added or tightened in this pass

- Paper 9.1: the expert baseline "has only begun"; three sentences on the partial author-labelled check, the two
  model labellers (one from a family under test, batch-mode leakage) and the adjudication; "six labels change,
  seven after the adjudication below". Section 5: the v1.4 E3 figures shown old -> new. Appendix G: one paragraph.
- [redacted: private application material]
- `expert/model_labels/README.md`: the adjudication outcome and the two confirmed leakage cases (XAB703 from
  XF1F4A, X7A91D from X391BD).

### Checks run (2026-11-04)

- `python3 -m unittest discover -s tests -t .`: 285 tests OK (267 before; +1 scorer title/note, +17 adjudication).
  `python3 -m unittest discover -s standard/sim -t .`: 55 tests OK. `python3 -m tools.schema_check
  standard/ABS_v0.3.md`: all checks passed. `python3 tools/schema_check/check_doc.py standard/ABS_v0.3.md`: 0 errors.
- `paper/build.sh`: every plotted number parsed from `results/` and asserted against `main.md`; 3 figures, 51
  internal links, 48 references, 1 `[CHECK]` (PSD3/PSR); body 8,409 words (limit 9,000).
- [Redacted: a check on private application material.] No em or en dash in
  any edited file.
- Reproducibility: `python3 -m acs.label_adjudication` regenerates both outputs byte for byte (a test checks the
  stored report and key); `python3 expert/score_expert.py` with default options regenerates both stored model-run
  score files byte for byte; `python3 -m acs.analyze_phase2` regenerates `results/phase2_summary.md` unchanged.
- Sweep for "unlabelled", "not yet labelled", "labels are not done", "still to be labelled" over the paper and two private files
  (redacted): the one remaining hit says the independent labels are not done, which is true.

### Unresolved

- Independent blind labels (Amendment 11's baseline; Audit 1 F24) remain open; D37 is the first case to put to them.
- [redacted: private application material]
- An evidence-conditional key for all 204 Phase 2 grid cells; the capture-triplet construction defect (D33-c and
  D34-c logs reveal the never-said requirement) needs a rebuilt case set; the two model runs are still unnamed.

## Founder rulings (2026-11-04): D37, and the tiered burden of proof (rulebook v1.5, ABS-V1)

Scope: the founder's two rulings of 2026-11-04. He is the study's author, so each ruling settles the programme's rule,
not the independence of a label. Sources of truth: `results/LABEL_ADJUDICATION_2026-11-04.md` (dated addendum) and
`expert/answer_key_v1.4_adjudicated.json`, both generated by `python3 -m acs.label_adjudication`;
`rulebook/AGENTIC_DISPUTE_RULEBOOK_v1.5.md` and `.json`; `standard/ABS_v0.3.md` A5.7 and A4.1 Step 1; `acs/rule_engine.py`
(`rulebook="1.5"`), `acs/decision_contract.py`, `acs/burden_rescore.py`. No model calls; no historical number changed;
v1.4 files unchanged. *exploratory* = written after the data were seen.

### Changed numbers (old -> new -> source)

| # | Quantity | Old | New | Label | Source |
|---|---|---|---|---|---|
| 1 | D37 ("my usual printer ink") | ground-truth error by author-side adjudication; `[CHECK]` in [redacted: private material] | founder-ruled: AG1-P / agent provider / refund (the agent should have asked or checked which ink was "usual"); label and every number unchanged | ruling (the author's) | addendum, ruling 1; key `adjudication.ruling` |
| 2 | Current core rulebook | v1.4 | v1.5 = v1.4 plus ABS-V1; v1.4 unchanged and still the expert kit's rule | design | `rulebook/VERSIONS.md` |
| 3 | ABS-V1 programme parameters | - | threshold EUR 100 per order (per currency, inclusive), cap 3 ABS-V1 refunds per buyer identity in 365 days; published; defaults a design proposal | design | ABS v0.3 A5.7; rulebook v1.5 `burden_tiers` |
| 4 | Residual fabrication loss | - (v1.4 sends every such claim to review) | at most threshold times cap per buyer identity per window: EUR 300 a year with the defaults (more with several identities or unshared PSP counts) | design | ABS v0.3 A5.7, A8.3 |
| 5 | Kit labels changed by v1.5 (EUR 100) | - | 3 of 40 (X2ED64, XF96DA, X15B65): `review / undetermined / undetermined` -> `AG3 / merchant / refund`; all E0-E2, all AG3 in fact | exploratory | addendum, ruling 2 |
| 6 | Liable-party agreement, adjudicated v1.4 key -> v1.5 key | founder 4/8; run 1 35/40; run 2 24/40 | founder 5/8; run 1 33/40; run 2 27/40 | exploratory | same |
| 7 | Burden-view differences from the adjudicated key | 10 of 30 | 3 resolved (founder X2ED64; run 2 X2ED64, X15B65); 7 remain: 5 above EUR 100, 2 outside the scope (XADFD6 a fee line, XC217F an Allowance term) | exploratory | same |
| 8 | Phase 2 A1, simulated-facts labels changed by v1.5 | - | 0 of 204 cells at EUR 100 (no stored low-value false merchant-performance claim); 9 with no threshold (D45-D47 at E0-E2, buyer -> merchant) | exploratory | same |
| 9 | Phase 2 A1 liable party on decidable kit cells, E0-E2 | fable 31/45, 35/46, 39/49; grok 22/45, 28/46, 37/49 | fable 32/46, 36/47, 40/50; grok 23/46, 29/47, 38/50 (one cell per level now decided, both arbiters right on it); E3 and the simulated-facts columns unchanged | exploratory | same |
| 10 | Phase 3 case-sides ABS-V1 would decide (E3, EUR 100) | - | merchant side 3 of 7 (D01, D02, D09), for the buyer, the true allocation; buyer side 0 of 7 | exploratory | same |
| 11 | Paper body words | 8,409 | 8,595 (Section 8: one paragraph, design not evaluated) | count | `paper/build.sh` |
| 12 | Harness tests | 285 | 316 (`tests/test_burden_tier.py`, 31) | count | `python3 -m unittest discover -s tests -t .` |

### Claims added or tightened in this pass

- ABS v0.3: ABS-V1 normative in A5.7 (scope, low-value tier, abuse guard, high-value tier, published parameters,
  residual risk); A4.1 Step 1 now says the engine "never finds the fact automatically" and applies ABS-V1; ABS-V1 in
  A3.1, the precedence line, A4.5 (AG3 row and a `low_value_burden` route paragraph), A8.3 and A15.1 item 22; Decision
  `confirmation_route` gains `low_value_burden` (the one schema change; no programme-parameter field was needed: the
  parameters are published with the rulebook version each Decision records); change-log entry.
- Rulebook v1.5 (`.md`, `.json`); `VERSIONS.md`: v1.5 current core, v1.4 the kit's rule, a note that pre-v1.5 documents
  calling v1.4 "the current core" stay right outside ABS-V1.
- Engine: `rulebook="1.5"` is `CURRENT`; threshold, cap and window as `burden_params`; fail safe on a missing order value
  or PSP count; the decision contract accepts an ABS-V1 refund only as AG3 / merchant / refund, under v1.5, within the
  threshold and the cap, with `confirmation_route: low_value_burden`.
- [redacted: private application material]
- Paper Section 8: one paragraph, "design, not evaluated".

### Checks run (2026-11-04)

- `python3 -m unittest discover -s tests -t .`: 316 tests OK. `python3 -m unittest discover -s standard/sim -t .`: 55
  OK. `python3 -m tools.schema_check standard/ABS_v0.3.md`: all checks passed. `python3 tools/schema_check/check_doc.py
  standard/ABS_v0.3.md`: 0 errors. Every JSON file parses.
- The ABS-V1 tests fail when the tier is disabled (14 of 26) or merchant support is ignored (3 of 26), then pass again.
- `python3 -m acs.label_adjudication` regenerates the report and the adjudicated key byte for byte (a test checks it);
  the Audit 1 and adjudication Phase 2 figures are asserted unchanged by the re-score tests.
- `paper/build.sh`: 3 figures (unchanged), 51 internal links, 48 references, 1 `[CHECK]` (PSD3/PSR), body 8,595 words.
- [Redacted: a check on private application material.] No em or en dash in any edited file.

### Unresolved

- Choices made by the research lane that the founder may overrule: ABS-E2 (a not-as-described claim with no content
  evidence from the buyer fails) and ABS-E1m stay above ABS-V1 at any value; AG1-M is outside the scope (the cart line
  origin is recomputed from the merchant-signed cart, and a missing cart is ABS-E1m); a claim that names the agent is
  out of scope (the keyword reader misread capture case D32-c otherwise); a missing order value or PSP count takes the
  high-value path; the reference engine assumes EUR when no currency is given, as its settlement already does.
- The bound itself is untested: no stored low-value fabricated claim, no buyer histories, no loss data (A15.1 item 22).
- Not edited: `results/PREREGISTRATION.md` (its label-adjudication amendment still lists D37's referential term as a
  question for experts; the ruling is in the addendum), [redacted: a private document],
  `standard/ABS_ONE_PAGER.md`, `standard/ADOPTION_AND_CONFIRMATION.md`, the expert kit page (states v1.4 by design),
  and dated result files that call v1.4 the current core.

## Confirmatory amendment C1 (2026-11-04, integration of the frozen gate test)

Scope: `paper/main.md` and `paper/figures/make_figures.py` (Figure 3), `standard/ABS_v0.3.md` (A4.5, A5.7, A7.9,
A8.7, A15.2, change log) and four private application documents (redacted in the public copy). Sources of truth: `results/CONFIRMATORY_C1.md` (section 9, what changes in the paper),
`results/confirmatory_c1_summary.md` (generated by the analysis frozen with the amendment), `results/PREREGISTRATION.md`
("Confirmatory amendment C1") and `results/CHRONOLOGY.md` row 27. No model calls; no result file edited. Verified
against the sources: the amendment was committed alone at 17:02:46 UTC (`10b5013`), the first C1 call was at
17:03:01 UTC (15 s later), 343 of at most 500 calls, all at the frozen revision, no deviation.

### Changed numbers (old -> new -> source)

| # | Quantity | Old | New | Label | Source |
|---|---|---|---|---|---|
| 1 | Gate v3 against attacks | stored outputs only: 0/14 (fable), 0/14 (grok), 0/67 attacked A2 attempts | added: best of 5 at E3 on 14 fresh case-sides, gate off 11/14 = 79% [52, 92], gate v3 on with a gate-aware attacker 0/14 = 0% [0, 22]; 11 discordant pairs, all one way; exact McNemar one-sided p = 0.00049 (two-sided 0.00098); -79 points [-100, -57]; the stored-output rows stay exploratory | confirmatory (H11) | `CONFIRMATORY_C1.md` section 2; summary section 4 |
| 2 | Gate-aware arm: judge fooled before the gate | not run (Deviation 6) | 8 attempts in 6 case-sides, all 8 sent to review | secondary | `CONFIRMATORY_C1.md` section 3 |
| 3 | Re-decisions of final payloads | - | arm A succeeds in a majority on 10/14 case-sides; arm B 0/42 re-decisions | secondary | section 6 |
| 4 | Headline cost of the gate | 40/50 baseline cases to review (gate v3 on fable's stored decisions) | 34/51 = 67% [53, 78] (C1, one decision per case); 20/31 true claimants and 14/20 unfounded claims; correct decided outcomes 48/51 -> 16/51 = 31% [20, 45]; 40/50 kept, labelled the exploratory replay | secondary, prospective | section 4; summary section 7 |
| 5 | Why the gate reviews | format failures dominated v1 (Phase 3b) | unchecked 23, provenance 9, contradiction 2, format 0; all 8 AG2 and 7/10 AG1-P cases reviewed (no reader for mandate terms beyond the hard limits, page text or the action log) | secondary | section 4 |
| 6 | Bad decisions passed by gate v3 | 0 on the stored data | baseline: D14 passed (true findings, wrong decision step); D22 and D46 caught by contradiction | secondary | section 4 |
| 7 | Attacker refusals | Phase 3: the pre-registered frontier attacker wrote a payload on 3/14 first prompts | C1, an attacker model from another family: 0/102 attempts without a payload; 80 evidence payloads; prompt injection against the gate, none passing | secondary | section 5 |
| 8 | Model calls in the project | 6,560 | 6,903 (343 in C1) | count | `results/calls.jsonl`; summary section 1 |
| 9 | Model families | judges and attackers from two | three (C1 adds an attacker family; its judge is a second Claude model, not a second family) | count | section 8 |
| 10 | Follow-up experiments | five prospective plans, none run | plan 1 (matched gate test, a matched H10) and the gate-aware half of plan 3 done via C1, with a substituted judge and attacker; four remain planned, not run | status | `CHRONOLOGY.md` row 27 |
| 11 | Paper body | 8,595 words | 8,987 words (limit 9,000) | count | `paper/build.sh` |
| 12 | [redacted: private application material] | | | | |

### Claims added or tightened in this pass

- Paper. Abstract: two sentences on C1 and its cost; "no tested defence is both safe and useful" now said as
  measured prospectively; limits say three model families. Section 1: the intro's answer and contribution (3) carry
  C1. Section 4: C1 is the one prospective test of a defence; 6,903 calls. Section 7: a C1 paragraph (H11) and the cost
  paragraph led by C1's baseline cost, the stored-data replay (24, 26 and 40 of 50) kept and labelled exploratory;
  "it checks findings, not reasoning" (D14). Section 8: "The missing reader (a hypothesis)": recomputation of
  machine-readable terms (A4.5) is the reader C1 shows the gate lacks; a hypothesis for the next test, not a result.
  Sections 9.1, 9.2, 9.4, 9.5, 9.6 and 10: C1 stated, the refusal sentence qualified (another family complied on all
  102 attempts and fooled a second Claude judge), plan status updated, a C1 limits bullet. Appendix G: H11 and the
  amendment paragraph. To stay under 9,000 words, Section 7 lost the sentence on the same-day adversarial variants
  (it stays in Appendix G) and the v2 re-check detail was condensed.
- Figure 3: two confirmatory diamonds (gate v3 off: 0% reviewed, 79% fooled; on: 67%, 0%), legend and caption say
  "confirmatory (C1)" against hollow exploratory points. `make_figures.py` parses them from
  `results/confirmatory_c1_summary.md`, recounts them from `results/c1/c1_A.jsonl`, `c1_B.jsonl` and `c1_BL.jsonl`, and
  asserts the abstract and Section 7 wording; the abstract's old 40/50 assertion is replaced.
- ABS v0.3: one passage each in A5.7 and A8.7, a C1 row in A15.2 (and the Phase 3b row's status), A7.9's stale
  "not run" line, A4.5's note on why a mandate-term reader matters (design, not evaluated), the A15.2 non-refusing
  attacker note, a change-log entry. No normative text changed.
- [redacted: private application material]
- Naming. [Redacted: how private material names the models.] The paper names the attacker model in its methods only
  (Section 7's C1 paragraph and Appendix G), following its convention of naming judge and attacker models there. The
  standard names neither the attacker nor any reviewer.

### Checks run (2026-11-04)

- `python3 -m unittest discover -s tests -t .`: 341 tests OK. `python3 -m unittest discover -s standard/sim -t .`: 55
  OK. `python3 -m tools.schema_check standard/ABS_v0.3.md`: all checks passed. `python3 -m
  tools.schema_check.check_doc standard/ABS_v0.3.md`: 0 errors. Every JSON file parses.
- `paper/build.sh`: every plotted number parsed and asserted, C1 included; 3 figures, 51 internal links, 48
  references, 1 `[CHECK]` (PSD3/PSR); body 8,987 words; `main.pdf` rendered (29 pages; Figure 3 and the C1 section
  read on page 12). Altering 0.0005, 34 of 51 or 48 of 51 in `main.md` stops the figure script each time.
- Sweep for "40 of 50" and "40/50": every remaining hit is labelled as the stored-data or exploratory replay (paper
  Section 7 and Appendix G; [redacted: private application material]).
- Sweep for "pre-registered, not run", "planned, not run", "not run" and "never ran" about the matched gate test or
  the gate-aware attacker: none left unqualified; the remaining hits are the frozen-attacker confirmation, the four
  plans still open, Phase 3b's own arms, or dated change items that now point to C1.
- No em or en dash and no American spelling added in any edited file.

### Unresolved

- The brief's "fooled a second judge family" is not what happened: the C1 judge is claude-opus-5-5, a second Claude
  judge. Every edited file says "a second Claude judge" or "a different Claude model".
- [Redacted: two notes on private material.]
- The C1 limits stand: one judge and one attacker family, n = 14, the Phase 2 generator and the templates gate v3
  reads, photos as text, unforgeable independent records, human reviewer accuracy unmeasured. The mandate-term reader
  is a hypothesis, not tested. Not edited: `standard/ABS_ONE_PAGER.md`, `standard/ADOPTION_AND_CONFIRMATION.md`,
  `README.md` and [redacted: two private documents].

## Confirmatory amendment C2 (2026-11-05, integration of the replication)

Scope: `paper/main.md` and `paper/figures/make_figures.py` (Figure 3), `standard/ABS_v0.3.md` (A5.7, A7.9, A8.7,
A15.2, change log). Sources of truth: `results/CONFIRMATORY_C2.md`, `results/confirmatory_c2_summary.md` (generated by
the analysis frozen with the amendment), `results/PREREGISTRATION.md` ("Confirmatory amendment C2") and
`results/CHRONOLOGY.md` row 28. No model calls; no result file edited. Verified against the sources: the amendment was
committed alone at 20:46:27 UTC (`735f491`), the first C2 call was at 20:46:41 UTC (14 s later), 566 of at most 600
calls, all at the frozen revision with the code clean, no deviation; `acs.confirmatory_c1 check` and
`acs.confirmatory_c2 check` both print "frozen".

### Changed numbers (old -> new -> source)

| # | Quantity | Old | New | Label | Source |
|---|---|---|---|---|---|
| 1 | Gate v3 against attacks | one frozen test: C1 11/14 against 0/14, p = 0.00049 | added: C2 on 28 further fresh case-sides, gate off 25/28 = 89% [73, 96], gate v3 on 0/28 = 0% [0, 12]; 25 discordant pairs, all one way; exact McNemar one-sided p = 2.98e-8 (paper 3.0e-8; abstract 3e-8), two-sided 5.96e-8; -89 points [-100, -75]; buyer 14/14 -> 0/14, merchant 11/14 -> 0/14 | confirmatory (H11-R) | `CONFIRMATORY_C2.md` section 2; summary section 4 |
| 2 | Pooled C1 + C2 | - | 36/42 = 86% [72, 93] against 0/42 = 0% [0, 8]; one-sided p = 1.46e-11 (paper 1.5e-11); -86 points [-95, -74]; buyer 21/21 -> 0/21, merchant 15/21 -> 0/21 | secondary, descriptive (C1 was known) | section 4; summary section 5 |
| 3 | Gate-aware arm: judge fooled before the gate | C1: 8 attempts in 6 case-sides, all reviewed | C2: 14 attempts in 10 case-sides, all 14 reviewed (9 contradiction, 5 provenance); the 12 decisions that passed the gate all named the true liable party | secondary | section 3; summary section 6 |
| 4 | Forged control blocks aimed at the judge | C1: 14 attempts, none fooled the judge | C2 arm B: 18 attempts on 16 case-sides; 2 fooled the judge before the gate (C2-13, C2-25, attempt 4 each), both reviewed | exploratory (text pattern) | section 7 |
| 5 | Attacker refusals | C1: 0/102 attempts without a payload | C2: 0/198; C1 + C2: 0/300; evidence payloads 139/198; arm A won 18 of its 25 at the first attempt | secondary | summary section 7 |
| 6 | Gate cost | C1 baseline 34/51 to review; correct decided outcomes 48/51 -> 16/51 (headline, unchanged) | added: under attack the gate reviewed 114 of the judge's 126 correct gated decisions; C2 has no baseline arm | exploratory (cost under attack) | section 7 (recounted from `results/c2/c2_B.jsonl`) |
| 7 | Re-decisions of final payloads | C1: arm A majority 10/14, arm B 0/42 | C2: arm A majority 23/28, arm B 0/84 | secondary | section 6 |
| 8 | Generator flaw (A01 ink case-sides) | - | 3 case-sides whose packing record lists 1 item for a 2-unit order; without them 22/25 against 0/25, one-sided p = 2.4e-7 | exploratory | section 7 |
| 9 | Model calls in the project | 6,903 | 7,469 (566 in C2) | count | `results/calls.jsonl`; summary section 1 |
| 10 | Follow-up experiments | matched gate test run once (C1) | run and replicated (C1, C2); four plans remain, not run | status | `CHRONOLOGY.md` row 28 |
| 11 | Paper body | 8,987 words | 8,982 words (limit 9,000) | count | `paper/build.sh` |
| 12 | Paper PDF | 29 pages | 30 pages (C2 paragraph page 11; Figure 3 page 13) | count | `paper/build/main.pdf` |

### Claims added or tightened in this pass

- Paper. Abstract: the C1 sentence becomes C1 + C2 (two frozen, pre-registered tests on 42 fresh case-sides; 36 of 42
  fooled without the gate and none of 42 with it; first test p = 0.0005, replication p = 3e-8) and "the gate paid for
  this by sending two in three ordinary disputes to human review"; limits say 14 to 28 attacked case-sides per test.
  Section 1: the intro's answer, contribution (3) and the review paragraph carry C2. Section 4: amendments C1 and C2,
  both prospective; 7,469 calls; H11-R named. Section 7: heading, Figure 2 caption, a C2 paragraph (H11-R, the pooled
  estimate, attacker strength, forged control blocks caught by the gate, 114 of 126 reviewed under attack). Sections 9.1,
  9.2, 9.5, 9.6 and 10: "one test" and "14" become "two tests" and "42"; the refusal sentence says 300 attempts. 9.4:
  the C1 bullet becomes "C1 and C2" with C2's limits (6 scenarios and 8 products, 16 case-sides on a product disputed
  before, case-sides treated as independent, the ink flaw and the result without it, anchors pinned in the C2 module).
  Appendix G: H11-R in the hypothesis list and a C2 amendment paragraph.
- Removed as no longer true without qualification: 9.2's "(typed findings already removed the format rejections)".
  C1's baseline had 0 format reviews, but C2's gated arm had 11 under attack.
- Cuts to stay under 9,000 words, each a duplicate of text kept elsewhere: the contract v2 defects (Appendix G), the
  re-check's counts in 9.5 (Section 1), the D37 detail in 9.1 (Section 5), Section 7's Deviation 6 sentence (Figure 3
  caption and 9.4), the offer-spec and framing detail in Section 5 (`PHASE2_DISPUTES.md`), and shorter wording in
  Sections 1, 5, 6, 8 and 9.1. No number changed.
- Figure 3: a lower panel, "Confirmatory tests of gate v3: case-sides fooled within five attempts", with C1, C2
  (replication) and C1 + C2 (pooled, descriptive), gate off and on, Wilson intervals; C2 has no baseline arm, so it has
  no point in the upper scatter. `make_figures.py` parses every C2 and pooled number from
  `results/confirmatory_c2_summary.md`, checks the pooled table against C1's summary, recounts both arms and the pooled
  counts from `results/c1/` and `results/c2/` jsonl, recomputes each exact McNemar p from the discordant pairs, and
  asserts the abstract, Sections 4, 7, 9.1, 9.2, 9.4, 10, Appendix G and the caption. The old abstract-only C1 assertion
  is replaced by the C1 + C2 one.
- ABS v0.3: one sentence each in A5.7, A7.9 and A8.7, a C2 row in A15.2, "amendments C1 and C2" in A15.2's
  non-refusing attacker note, and a change-log entry, each saying "not the C2 control condition" where it could be
  confused. A4.5 is unchanged: it cites C1's baseline cost, and C2 has no baseline arm. No normative text changed.
- [redacted: private application material]
- Naming. The paper names the judge and attacker models in its methods only, as for C1 (Section 7's
  C1 paragraph and Appendix G's C2 paragraph); the abstract says "a different Claude judge and an attacker model from
  another family". The standard names no attacker.

### Checks run (2026-11-05)

- `python3 -m unittest discover -s tests -t .`: 355 tests OK. `python3 -m unittest discover -s standard/sim -t .`: 55
  OK. `python3 -m tools.schema_check standard/ABS_v0.3.md`: all checks passed. `python3 tools/schema_check/check_doc.py
  standard/ABS_v0.3.md`: 0 errors. Every JSON file parses. `python3 -m acs.analyze_c1` and `python3 -m acs.analyze_c2`
  regenerate their summaries unchanged.
- `paper/build.sh`: every plotted number parsed and asserted, C2 and the pooled estimate included; 3 figures, 51 internal
  links, 48 references, 1 `[CHECK]` (PSD3/PSR); body 8,982 words; `main.pdf` rendered (30 pages). Altering, one at a
  time, the abstract's replication p, the 114 of 126, the pooled interval, the ink-free p and the call count in
  `main.md` stops the figure script each time.
- Sweep for "one frozen", "tested once", "14 fresh", "all 14", "102" and "6,903" in the paper: every remaining hit is
  about C1 alone (its paragraph, the Figure 3 caption's C1 diamonds, Appendix G).
- No em or en dash and no American spelling added in any edited file.

### Unresolved

- The pooled 36/42 against 0/42 is descriptive (C1 was known when C2 was frozen); the abstract gives the p-values per
  test only.
- C2 is a replication within C1's design: the same judge, attacker family, generator and templates. It says nothing
  about other judges, attackers, record formats or dispute kinds.
- The abstract is now 486 words (2,848 characters; 439 and 2,608 before). An arXiv abstract field takes 1,920
  characters, so the submission form needs its own shorter abstract, as before.
- Not edited here: [redacted: private application material], `standard/ABS_ONE_PAGER.md`,
  `standard/ADOPTION_AND_CONFIRMATION.md` and `README.md`.

## Automated EM-search citation (2026-11-07)

| # | Quantity | Old | New | Label | Source |
|---|---|---|---|---|---|
| 1 | Gate-aware attacker strength | 0/42 gated reported with C1 and C2 limits only | cited `emsearch2026` (Balcells Obeso, Qi, MacDiarmid and Hubinger, Alignment Science Blog, October 2026; title, author line, date and method verified on the page 2026-11-07); paper Section 2 (one sentence), 9.4 (one agent at up to five attempts per case-side, so 0 of 42 is a lower bound on attack success) and 10 (next step: gate v3 with its mandate-term reader, frozen and attacked by a population search); [redacted: private material] says the same; no number changed; body 8,995 words after cutting the intro's review-paragraph duplicate of 9.5, a 9.2 restatement of Section 7 and 9.5's restatement of the gate v3 tests; [redacted: a count on private material] | limitation (not a result) | `paper/refs.bib`; `paper/build.sh` |

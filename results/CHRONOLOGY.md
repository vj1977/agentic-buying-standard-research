# Per-analysis chronology (Audit 1, F19)

Written 2026-11-04 after Audit 1. The blanket statement that every amendment was "dated and
committed before the runs it governs" is not true for every analysis. This table records, per
analysis, what governed it, when its first call ran, what had already happened when the governing
text was written, and its status. It is built from two sources only:

- the git history (`TZ=UTC git log --format='%h %cd %s' --date=format-local:'%m-%d %H:%M:%SZ'`;
  the commit that first added each amendment heading to `results/PREREGISTRATION.md` is found with
  `git log --reverse -S"## Amendment N" -- results/PREREGISTRATION.md`);
- the call log `results/calls.jsonl` (first and last `ts` per `run_id`, in UTC; table 2).

Times are UTC. Every run happened on 2026-11-03 (times from 23:39Z) or 2026-11-04.

**Status labels.**
- *Prospective*: the governing text was committed before the analysis's first call, and none of
  its own outcomes existed.
- *Prospective, design informed by earlier data*: committed before its own calls, but written in
  response to outcomes of earlier analyses (the text says so).
- *Amended after data*: the governing text, the harness or the scoring changed after some of the
  analysis's own outcomes existed.
- *Exploratory*: specified after the data it uses; reported as exploratory.
- *Superseded*: run, kept, not used for any claim.
"Whether inspected" is stated only where the record says so; otherwise the table says the outcomes
existed.

## 1. Analyses

| # | Analysis | Governing text (commit, time) | First governed call (run, time) | Already existing or inspected when the governing text was written | Exclusions, deviations | Status |
|---|---|---|---|---|---|---|
| 1 | Smoke test and exploratory pilot (45 roots, S01-S15) | none | smoke 11-03 23:39:33Z; pilot 23:42:48Z | - | - | Exploratory (reported as such) |
| 2 | Phase 1 confirmatory static set: H1, H1b, H1c (dev S01-S15, held-out H01-H09) | Preregistration, 79831c6, 11-03 23:52:05Z | main_dev 23:52:15Z | Pilot: 45/45 per condition, a ceiling. The held-out set was written after the pilot and run on no model before the commit | Deviation 1 (H05 harness defect): 8 roots kept apart. The fixed re-run `main_heldout_H05fix` started 00:13:06Z, 68 s before the commit that records Deviation 1 (680084c, 00:14:14Z) | Prospective; the H05 re-run amended after data |
| 3 | Gate coverage (agent-independent) | 79831c6, 11-03 23:52:05Z | gate_coverage 00:14:28Z | - | - | Prospective |
| 4 | Hard set X01-X10, adaptive red-team, trust T0/T12, offer-spec comparison | Amendment 3, 06e31ce, 00:21:47Z (hard scenarios 6046730, 00:23:59Z) | hard 00:24:02Z; trust_t0 00:26:09Z; redteam 00:38:03Z | The confirmatory Phase 1 ceiling: every agent 33/33 in every condition (the amendment states it) | - | Prospective, design informed by earlier data |
| 5 | Agent Allowance arm | Amendment 4, f33c533, 00:28:18Z | allowance 00:40:07Z | - | - | Prospective (secondary) |
| 6 | Scoring audit (Sonnet relabels 40 episodes) | 79831c6 ("Scoring audit") | scoring_audit 00:41:19Z | Phase 1 episodes (the sample is of them, by design) | - | Prospective |
| 7 | Red-team "effective rounds" (refusals counted apart) | Post-hoc list, b5ff4c3, 01:00:09Z | no new calls | Red-team complete (last call 00:54:40Z); Phase 1 write-up committed 00:56:07Z | - | Exploratory |
| 8 | Phase 1 cluster-bootstrap intervals | Amendment 12, 7ed574c, 01:23:18Z | no new calls | The Phase 1 tables (the amendment says so) | Added beside the Wilson intervals, not substituted | Amended after data |
| 9 | Capture probe (mandate drafting, 5 models x 8 conversations) | Amendment 10, 3dded04, 01:06:11Z; harness 395084b, 01:07:24Z | capture_draft 01:11:34Z | - | Deviation 3 (7af6191, 01:13:47Z): the checker was corrected after reading every miss (strict 35/40, corrected 40/40). Audit 1 F18 (2026-11-04): typed checker, strict 36/40 faithful [Audit 3 N04: checker agreement; checker v2 gives the same 36/40] | Probe prospective; checker amended after data; F18 re-score post-audit, exploratory |
| 10 | Phase 2 v1.1 grid | Amendment 1, 680084c, 00:14:14Z | p2_a1_grid 00:14:40Z | - | Stopped at 203 of 320 decisions for Amendment 5 (80c3e7a, 00:32:27Z, a response to Audit 0); kept, not used | Superseded |
| 11 | Phase 2 v2 (rulebook v1.2 before its final revision) | Amendments 5-6, 80c3e7a 00:32:27Z and 03863f4 00:37:43Z | p2v2_a1_grid 00:37:58Z; p2v2_a2 00:38:23Z | The 203 v1.1 grid decisions existed; whether they were read is not recorded | 37 + 13 calls; superseded by Amendment 7 (10dfbba, 00:43:04Z), committed after they ran | Superseded |
| 12 | Phase 2 primary: H2, H5 (primary); H3, H4, H6, H6b (secondary) | Amendments 6-8, 10dfbba, 00:43:04Z (rulebook v1.2-final, twin cases, A3 quorum) | p2v3_a1_grid 00:43:19Z; p2v3_a2 00:43:34Z; p2v3_tier1 00:44:30Z | The superseded v1.1 and v2 runs existed when the final rule and the twin cases were fixed; Amendment 7 does not record whether their outcomes were read | Deviation 2 (827d04b, 00:51:33Z): tier-1 parse repair and fairness definitions, written while tier 1 ran, before any tier-1 result was summarised; 3 parse-error records kept apart and re-run | Prospective (committed 15 s before the first call); tier-1 scoring amended during the run |
| 13 | A1 E3 repeats, legacy-offer comparison, rail flip | 10dfbba (repeats); Amendment 3 (offer-spec) | rep1 00:44:29Z; legacy 00:50:34Z; railflip 00:54:34Z | - | - | Prospective (secondary) |
| 14 | A3 cross-family quorum and single-finder hybrids | Amendment 8, 10dfbba, 00:43:04Z | derived from p2v3_a2 (no extra calls) | - | - | Prospective (secondary) |
| 15 | Relaxed-conformity sensitivity (A2, A3) | Post-hoc list, b5ff4c3, 01:00:09Z | no new calls | A2 had been running since 00:43:34Z; its review rate was in the logged runs | - | Exploratory |
| 16 | Cross-family error correlation | Amendment 10, 3dded04, 01:06:11Z | no new calls | A2 runs in progress (finished 01:48:21Z): part of the data existed | - | Secondary; specified while its data were being produced |
| 17 | Capture-duty arm (rulebook v1.3, 12 triplets, 48 decisions) | Amendment 10, 3dded04 01:06:11Z; v1.3 and cases 395084b 01:07:24Z | capture_adjudicate 01:07:34Z | - | - | Prospective (secondary) |
| 18 | Human expert baseline | Amendment 11, af3f804, 01:08:56Z; kit c20dd29, 01:11:10Z | no label given yet | - | Kit rebuilt after Audit 1 with the v1.4 rules (same seed, same 40 cases); two answer-key labels change (`results/AUDIT1_CORRECTIONS_PHASE1_2.md`); still before any label | Prospective (not yet run) |
| 19 | Phase 2 cluster-bootstrap intervals (A2, A3, single-finder pooled rates) | Amendment 12, 7ed574c, 01:23:18Z | no new calls | "The Phase 2 A2 and A3 analysis had not yet been written"; A2 runs in progress | - | Prospective for the analysis; its data were partly produced |
| 20 | Stake framing | Amendment 12, 7ed574c, 01:23:18Z | p2v3_a1_stake_merchant 01:23:38Z | - | - | Prospective (secondary) |
| 21 | Audit 1 Phase 1-2 corrections: case-level H6b and manipulation bounds (F21); residual-route labels (F11); v1.4 re-labelling (F10, F12); typed capture re-score (F18) | Commits after Audit 1 (0203778, 07:15:32Z) in this lane | no new calls | Every result above | Historical numbers kept beside the corrected ones | F21: correction of the inference unit; F11: relabelling, counts unchanged; F10, F12, F18: post-audit, exploratory |
| 22 | Phase 3: H8, H9; arms A-D, T, R | Amendment 13, a63d6c0, 03:16:40Z | p3_probe 03:24:31Z; arms A and B 03:31:37Z | All Phase 1-2 results; the amendment cites them as its motivation | Deviation 4 (9aac777, 03:31:18Z), after 7 probe calls: attacker grok-4.7 replaced by grok-4.7-build-fast. Deviation 5 (7c30712, 03:37:05Z), after 19 preliminary attempts, 54 calls, in which the 5 written payloads fooled the arbiter 4 times: attacker chain; arms A and B restarted, preliminary attempts kept apart. Harness note 03:41Z (d0156cf, 03:41:35Z), 4 minutes into the restarted arms: attacker plan turn | Amended after data: the attacker and harness changed after outcomes were seen. Exploratory development of the attack; a confirmatory test needs a frozen attacker on untouched cases |
| 23 | Phase 3 analysis additions: curve frontier, matched review, confidence of successful attacks | 5d9782c 03:38:22Z; c3db88f 03:48:53Z; 1b91e06 03:49:22Z | no new calls | Arms A-C running; successes already logged | - | Exploratory |
| 24 | Phase 3b: H10; arms GA, GB, GBg, GC, GN, GD | Amendment 14, 9ce9a27, 05:34:44Z; harness 38a15b3, 05:41:57Z | p3b_probe 05:43:05Z; GB 05:43:41Z | Phase 3 complete and written up; the gate was designed from its results | Analysis committed during the run (b154835, 05:46:31Z). Deviation 6 (b840071, 06:12:35Z; its heading says 06:15Z): credit outage, missing cells. After the tables were generated, failed calls were made missing (b6e2294, 06:11:20Z); an exploratory bound was added (09fecd7, 06:15:26Z) | H10 prospective relative to its own calls; design informed by Phase 3; analysis amended after data; the bound exploratory |
| 25 | Audit 3 re-check fixes and replays: contract v3 (N01, N02), gate v3 (N03, F05), capture checker v2 (N04), F12 and F13 remainders, case-level intervals (N06), schema checker (F15) | Commits after the re-check (c99d63e), 2026-11-04: b9a1bdf, 7f5d0dd, a775310, 0aef881, 7e8d3d6, cd88708, 6186686; hardened after an independent adversarial check: 83b166b, 5622fd7 | no new calls | Every result above, the Audit 1 re-analyses and the re-check's counterexamples | Earlier code versions kept; Audit 1 numbers reproduce; run-level intervals withdrawn with the old values quoted | Exploratory (new code on stored outputs); N06 a correction of the inference unit |
| 26 | Follow-up experiments 1-5 ("Post-audit amendment (Audit 1)", Section 3) | Listed 2026-11-04 | not run | Every result above | - | Prospective experiment plans, not yet frozen preregistrations: the gate, contract, prompts, case set and attacker are not frozen (Audit 3, N07) |
| 27 | Confirmatory amendment C1: H11 (gate v3 on vs off, gate-aware attacker, 14 fresh case-sides), baseline cost, re-decisions | Confirmatory amendment C1, 10b5013, 11-04 17:02:46Z; code, case set, analysis and manifest f41a161, 17:02:27Z | c1_probe 11-04 17:03:01Z; c1_A 17:03:48Z | Every result above. No C1 case, judge decision or attack existed; the 14 case-sides come from Phase 1 episodes of scenarios that source no Phase 2 case | None: no deviation; 2 attacker calls missing (Codex capacity errors) and re-run under the rules | Prospective (H11 confirmatory; the rest secondary). Plan 1 of row 26, with a substituted judge (claude-opus-5-5) and attacker (Codex gpt-6-astra) |

Rows 22-24 belong to the Phase 3 write-ups, which another lane maintains; they are listed here so
that the chronology is complete.

## 2. Call-log run windows

From `results/calls.jsonl`: first and last call per `run_id` (UTC), calls logged, calls with
`ok: true`, and the running total.

| Run | First call | Last call | Calls | OK | Running total |
|---|---|---|---|---|---|
| smoke | 11-03 23:39:33Z | 11-03 23:40:50Z | 32 | 24 | 32 |
| model-id-check | 11-03 23:42:31Z | 11-03 23:42:35Z | 3 | 3 | 35 |
| pilot | 11-03 23:42:48Z | 11-03 23:47:36Z | 317 | 317 | 352 |
| main_dev | 11-03 23:52:15Z | 11-03 23:57:56Z | 418 | 418 | 770 |
| main_heldout | 11-03 23:57:59Z | 00:12:46Z | 575 | 575 | 1,345 |
| main_heldout_H05fix | 00:13:06Z | 00:15:05Z | 94 | 94 | 1,439 |
| gate_coverage | 00:14:28Z | 00:16:20Z | 138 | 138 | 1,577 |
| p2_a1_grid | 00:14:40Z | 00:31:18Z | 203 | 203 | 1,780 |
| probe_models | 00:20:51Z | 00:21:00Z | 3 | 3 | 1,783 |
| hard | 00:24:02Z | 00:36:27Z | 908 | 908 | 2,691 |
| trust_t0 | 00:26:09Z | 00:32:14Z | 215 | 215 | 2,906 |
| trust_t12 | 00:32:16Z | 00:38:27Z | 218 | 218 | 3,124 |
| p2v2_a1_grid | 00:37:58Z | 00:41:07Z | 37 | 37 | 3,161 |
| redteam | 00:38:03Z | 00:54:40Z | 697 | 697 | 3,858 |
| p2v2_a2 | 00:38:23Z | 00:41:05Z | 13 | 13 | 3,871 |
| allowance | 00:40:07Z | 00:43:09Z | 141 | 141 | 4,012 |
| scoring_audit | 00:41:19Z | 00:41:51Z | 40 | 40 | 4,052 |
| p2v3_a1_grid | 00:43:19Z | 01:19:58Z | 416 | 410 | 4,468 |
| p2v3_a2 | 00:43:34Z | 01:48:21Z | 475 | 472 | 4,943 |
| p2v3_a1_rep1 | 00:44:29Z | 00:46:56Z | 51 | 51 | 4,994 |
| p2v3_tier1 | 00:44:30Z | 01:06:06Z | 229 | 227 | 5,223 |
| p2v3_a1_rep2 | 00:47:09Z | 00:50:19Z | 53 | 53 | 5,276 |
| p2v3_a1_legacy | 00:50:34Z | 00:54:22Z | 32 | 32 | 5,308 |
| p2v3_a1_railflip | 00:54:34Z | 00:55:00Z | 12 | 12 | 5,320 |
| capture_adjudicate | 01:07:34Z | 01:11:25Z | 51 | 51 | 5,371 |
| capture_draft | 01:11:34Z | 01:12:27Z | 40 | 40 | 5,411 |
| p2v3_a1_stake_merchant | 01:23:38Z | 01:31:03Z | 105 | 105 | 5,516 |
| p2v3_a1_stake_provider | 01:31:16Z | 01:38:42Z | 107 | 107 | 5,623 |
| p3_probe | 03:24:31Z | 03:41:12Z | 7 | 7 | 5,630 |
| p3_A | 03:31:37Z | 04:24:09Z | 154 | 146 | 5,784 |
| p3_B | 03:31:43Z | 04:11:31Z | 73 | 72 | 5,857 |
| p3_refusal | 03:32:06Z | 03:42:54Z | 14 | 14 | 5,871 |
| p3_C | 03:40:00Z | 04:14:36Z | 58 | 57 | 5,929 |
| p3_D | 03:52:57Z | 05:25:47Z | 245 | 245 | 6,174 |
| p3_T | 04:25:29Z | 04:54:21Z | 69 | 69 | 6,243 |
| redteam_grok | 04:54:45Z | 05:05:40Z | 171 | 171 | 6,414 |
| p3b_probe | 05:43:05Z | 05:43:05Z | 1 | 1 | 6,415 |
| p3_GB | 05:43:41Z | 05:50:00Z | 51 | 50 | 6,466 |
| p3_GA | 05:44:04Z | 05:55:07Z | 28 | 28 | 6,494 |
| p3_GN | 05:50:31Z | 05:52:14Z | 6 | 5 | 6,500 |
| p3_GC | 05:55:24Z | 05:55:27Z | 2 | 2 | 6,502 |
| p3_GBg | 05:57:49Z | 06:05:20Z | 58 | 18 | 6,560 |
| c1_probe | 11-04 17:03:01Z | 11-04 17:03:04Z | 2 | 2 | 6,562 |
| c1_A | 11-04 17:03:48Z | 11-04 17:23:34Z | 66 | 64 | 6,628 |
| c1_BL | 11-04 17:10:14Z | 11-04 17:15:26Z | 51 | 51 | 6,679 |
| c1_B | 11-04 17:10:34Z | 11-04 17:40:05Z | 140 | 140 | 6,819 |
| c1_R | 11-04 17:40:20Z | 11-04 17:46:16Z | 84 | 84 | 6,903 |

No call was made between 06:05:20Z (credits exhausted) and the C1 probe at 17:03:01Z; everything in that
window, including all Audit 1 and Audit 3 corrections, is deterministic re-analysis of stored records. The C1 calls
(17:03:01Z-17:46:16Z, 343) are the only calls after it; they ran at commit 10b5013 under the C1 amendment.

## 3. What this changes in the write-ups

- `results/PILOT_RESULTS.md` said every amendment was "dated and committed before the runs it
  governs, or disclosed as a deviation". Rows 4, 7, 8 and 9 show analyses written after Phase 1
  data existed; they were disclosed, but they are not prospective. The header now points here.
- `results/PHASE2_DISPUTES.md`: rows 12, 15, 16 and 19 are the Phase 2 analyses whose
  specification overlapped their own data; the Phase 2 primary tests (H2, H5) are prospective.
- The Phase 3 and 3b rows (22-24) are amended-after-data and exploratory in the sense of Audit 1
  F19; the Phase 3 write-ups are maintained by another lane.

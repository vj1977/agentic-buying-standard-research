# Partial author-labelled check (8 of 40 cases; NOT the independent expert baseline)

**Partial, author-labelled, not independent.** The founder labelled 8 of the 40 kit cases blind on 2026-11-04 (`expert/expert_labels_founder_partial_2026-11-04.csv`). He is the study's author, so these labels test the consistency of the key with its author's own reading, not its validity; Amendment 11's expert baseline still needs independent labellers. The 8 cases are the first 8 of the kit's randomised order (2 at E0, 2 at E1, 4 at E2, none at E3). With n = 8 every interval is wide and kappa is unstable: the remedy kappa of 0.00 is not meaningful, because he answered 'refund' on all 8 cases (no variance), and the liable-party kappa of 0.40 rests on 8 cases. Every disagreement below is adjudicated in `results/LABEL_ADJUDICATION_2026-11-04.md`, which also scores these labels against the adjudicated key (`expert/answer_key_v1.4_adjudicated.json`). Generated with `python3 expert/score_expert.py expert/expert_labels_founder_partial_2026-11-04.csv --out results/expert_baseline_partial.md --title ... --note ...`.

Labelled cases: 8 of 40.

## Relabel check

Kit ids whose v1.4 label differs from the historical one (derived from the answer key by comparing reason code, liable party and remedy): X89C5F (D31), X9FC6C (D43).
Documented relabel list (results/AUDIT1_CORRECTIONS_PHASE1_2.md F12; rulebook/VERSIONS.md): X89C5F (D31), X9FC6C (D43).

The derived list matches the documented list.

## Expert vs rule ground truth

| Measure | Agreement: v1.4 label (the kit's rules) | Cohen's kappa | Agreement: historical label (v1.2/v1.3) | Kappa |
|---|---|---|---|---|
| Liable party | 5/8 = 62% [31, 86] | 0.40 | 5/8 = 62% [31, 86] | 0.40 |
| Remedy | 6/8 = 75% [41, 93] | 0.00 | 6/8 = 75% [41, 93] | 0.00 |
| Liable party and remedy both | 5/8 = 62% [31, 86] | 0.40 | 5/8 = 62% [31, 86] | 0.40 |
| Expert answered 'undetermined' (liable party) | 0/8 = 0% [0, 32] | | | |

Labelled cases whose v1.4 label differs from the historical one: none. Every table below reports both labels; the arbiters were instructed under v1.2/v1.3.

### By evidence level

| evidence level | Liable party: v1.4 | Remedy: v1.4 | Liable party: historical | Remedy: historical |
|---|---|---|---|---|
| E0 | 2/2 = 100% [34, 100] | 2/2 = 100% [34, 100] | 2/2 = 100% [34, 100] | 2/2 = 100% [34, 100] |
| E1 | 1/2 = 50% [9, 91] | 1/2 = 50% [9, 91] | 1/2 = 50% [9, 91] | 1/2 = 50% [9, 91] |
| E2 | 2/4 = 50% [15, 85] | 3/4 = 75% [30, 95] | 2/4 = 50% [15, 85] | 3/4 = 75% [30, 95] |

### By stratum

| stratum | Liable party: v1.4 | Remedy: v1.4 | Liable party: historical | Remedy: historical |
|---|---|---|---|---|
| AG1-P hard limit | 1/1 = 100% [21, 100] | 1/1 = 100% [21, 100] | 1/1 = 100% [21, 100] | 1/1 = 100% [21, 100] |
| AG2 never stated | 0/1 = 0% [0, 79] | 0/1 = 0% [0, 79] | 0/1 = 0% [0, 79] | 0/1 = 0% [0, 79] |
| AG3 edited listing | 1/1 = 100% [21, 100] | 1/1 = 100% [21, 100] | 1/1 = 100% [21, 100] | 1/1 = 100% [21, 100] |
| AG3 obvious | 1/1 = 100% [21, 100] | 1/1 = 100% [21, 100] | 1/1 = 100% [21, 100] | 1/1 = 100% [21, 100] |
| AG3 subtle | 0/1 = 0% [0, 79] | 1/1 = 100% [21, 100] | 0/1 = 0% [0, 79] | 1/1 = 100% [21, 100] |
| AG5 false claim | 0/1 = 0% [0, 79] | 0/1 = 0% [0, 79] | 0/1 = 0% [0, 79] | 0/1 = 0% [0, 79] |
| capture a | 1/1 = 100% [21, 100] | 1/1 = 100% [21, 100] | 1/1 = 100% [21, 100] | 1/1 = 100% [21, 100] |
| capture b | 1/1 = 100% [21, 100] | 1/1 = 100% [21, 100] | 1/1 = 100% [21, 100] | 1/1 = 100% [21, 100] |

### Expert calibration (liable party)

| Confidence | n | Agrees with v1.4 label | Agrees with historical label |
|---|---|---|---|
| 3 | 3 | 1/3 = 33% [6, 79] | 1/3 = 33% [6, 79] |
| 5 | 5 | 4/5 = 80% [38, 96] | 4/5 = 80% [38, 96] |

## Expert vs each arbiter (same case, same evidence level; liable party)

| Arbiter | Cases | Agreement with expert | Kappa | Expert matches v1.4, arbiter does not | Arbiter matches v1.4, expert does not | Expert matches historical, arbiter does not | Arbiter matches historical, expert does not |
|---|---|---|---|---|---|---|---|
| A1 claude-fable-5-1 | 8 | 6/8 = 75% [41, 93] | 0.57 | 0 | 2 | 0 | 2 |
| A1 grok-4.7 | 8 | 5/8 = 62% [31, 86] | 0.40 | 0 | 3 | 0 | 3 |

## Expert/ground-truth disagreements (for adjudication under Amendment 11: ground-truth error, policy disagreement, evidence ambiguity, or expert slip)

A case is listed if the expert's liable party or remedy differs from either label.

| Case | Original id | Level | Stratum | Expert (liable / remedy, confidence) | v1.4 label (code / liable / remedy) | Historical label (code / liable / remedy) | Disagrees with | Arbiters (liable) | Expert notes |
|---|---|---|---|---|---|---|---|---|---|
| X608BC | D47 | E1 | AG5 false claim | merchant / refund (3) | AG5 / buyer / deny | AG5 / buyer / deny | v1.4 and historical | A1 claude-fable-5-1: merchant; A1 grok-4.7: buyer |  |
| X40DAA | D12 | E2 | AG3 subtle | agent_provider / refund (3) | AG3 / merchant / refund | AG3 / merchant / refund | v1.4 and historical | A1 claude-fable-5-1: merchant; A1 grok-4.7: merchant |  |
| XC9351 | D37 | E2 | AG2 never stated | agent_provider / refund (5) | AG2 / buyer / deny | AG2 / buyer / deny | v1.4 and historical | A1 claude-fable-5-1: buyer; A1 grok-4.7: buyer |  |

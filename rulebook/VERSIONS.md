# Rulebook versions and the claims that rest on each (Audit 1, F10)

Every result in this repository was produced under one rulebook version. A result is reported
under the rulebook it ran on; nothing below re-labels a historical result. Where a later rulebook
would change a ground-truth label, the change is listed in
`results/AUDIT1_CORRECTIONS_PHASE1_2.md` as a post-audit, exploratory re-labelling beside the
historical number, never in place of it.

## Versions

| Version | File(s) | Commit that froze it | What it adds or changes | Status |
|---|---|---|---|---|
| 1.0 | (history only, `git show 79831c6:rulebook/AGENTIC_DISPUTE_RULEBOOK.json`) | 79831c6 | Six codes: AG4 before AG3 | superseded before any Phase 2 call it governed |
| 1.1 | (history only, `git show 680084c:rulebook/AGENTIC_DISPUTE_RULEBOOK.json`) | 680084c | Conformity first; rail-agnostic settlement | superseded; governed the pre-audit grid `p2_a1_grid` only |
| 1.2 | `AGENTIC_DISPUTE_RULEBOOK.md`, `AGENTIC_DISPUTE_RULEBOOK.json` | 03863f4 (rules), 10dfbba (final: machine-readable mandate terms) | One liability rule by mandate precision: only encoded fields bind; "free-text intent is context, not a term"; a wish said only in chat is AG2; withdrawal overlay with digital content always excluded; card settlement "through the chargeback mechanism" | **historical; ground truth of every primary Phase 2 and Phase 3 result** |
| 1.3 | `AGENTIC_DISPUTE_RULEBOOK_v1.3.json` | 395084b | v1.2 plus AG1-C (stated to the agent, not captured: agent provider) | historical; capture-duty arm only |
| 1.4 | `AGENTIC_DISPUTE_RULEBOOK_v1.4.md`, `AGENTIC_DISPUTE_RULEBOOK_v1.4.json` | f42bdb2 (Audit 1), binding-term text aligned with the amended standard afterwards | The core = ABS v0.3 A4, A4.4, A6: a term binds if captured in the signed Mandate, machine-readable or as signed text the user confirmed (AG1-P); stated only in the conversation: AG1-C; AG0 and AG4-D; withdrawal prerequisites (missing = `undetermined`); Audit 2 settlement (no ABS chargeback, no recall) | core until 2026-11-04, unchanged since; **the rule of the expert kit and the adjudicated key**; no model has been run under it |
| 1.5 | `AGENTIC_DISPUTE_RULEBOOK_v1.5.md`, `AGENTIC_DISPUTE_RULEBOOK_v1.5.json` | the commit that adds these files (founder ruling 2, 2026-11-04) | v1.4 plus ABS-V1, the tiered burden of proof for merchant-performance claims (ABS v0.3 A4.1 Step 1, A5.7): a non-delivery or non-conformity claim no record with independent authority decides is the merchant's to refund at or below a published order-value threshold (default EUR 100) while the buyer is under a per-buyer cap (default 3 in 12 months); otherwise review, as v1.4. Never Step 0 or agent-instruction disputes | **current core; no model has been run under it; the threshold and cap defaults are a design proposal** |

v1.2 and v1.3 files are unchanged by Audit 1, and v1.4 is unchanged by v1.5. Documents written before
v1.5, the v1.4 file's own title included, call v1.4 "the current core"; what they say under v1.4 holds
under v1.5 for every case except a low-value non-delivery or non-conformity claim that no record with
independent authority decides (ABS-V1). The reference engine
reads all four (`acs/rule_engine.py`, `RULEBOOKS`); `decide()` defaults to v1.2 so that stored A2
results replay byte-for-byte, and takes `rulebook="1.5"` for the current core (`"1.4"` for the core
the expert kit states). Under v1.5 the engine needs the order value, the currency and the payer
PSP's count of the buyer's earlier ABS-V1 refunds (`case_meta`), and takes the threshold and cap as
`burden_params`.

## Version-to-claims matrix

| Result (where reported) | Data | Rulebook | Engine / prompt that applied it | Notes |
|---|---|---|---|---|
| Phase 1 shopping agents, hard set, red-team, trust, allowance (`results/PILOT_RESULTS.md` §1-3.6) | `results/runs/*.jsonl` | none (no dispute decided) | agent harness | The Agent Profile behaviours, not the rulebook |
| Phase 1 capture probe, 40/40 (`PILOT_RESULTS.md` §3.7) | `results/runs/capture_draft.jsonl` | v1.2 doctrine in the drafting prompt ("only mandate fields bind") | `acs/capture.py` `DRAFT_SYSTEM`; checker revised after the run (Deviation 3) and again after Audit 1 (F18) | Re-scored post-audit beside 40/40 |
| Phase 2 pre-audit grid (superseded) | `results/phase2/p2_a1_grid.jsonl` | v1.1 | `acs/adjudicate.py` | Kept, not used |
| Phase 2 v2 (superseded) | `results/phase2/p2v2_*.jsonl` | v1.2 (before the final mandate-terms revision) | adjudicate / hybrid | Kept, not used |
| Phase 2 H2, H3, H5 evidence levels; confusion matrices; calibration (`results/PHASE2_DISPUTES.md` §2.1) | `p2v3_a1_grid.jsonl` | **v1.2** | adjudicate prompt built from the v1.2 JSON | Ground truth = v1.2 labels in `data/disputes/cases.json` |
| Phase 2 twin pairs (mandate precision) | `p2v3_a1_grid.jsonl` | **v1.2** | adjudicate | Under v1.4 the four uncaptured twins would be AG1-C, not AG2 (corrections file) |
| Phase 2 H6, H6b, A2/A3 architectures, relaxed sensitivity, error correlation (§2.2) | `p2v3_a2.jsonl`, `p2v3_a1_rep*.jsonl` | **v1.2** | `acs/rule_engine.py` (engine `abs-rules/1.2`), fact-finder prompt in `acs/hybrid.py` | The findings schema has no v1.4 findings: not replayable under v1.4 without new calls |
| Phase 2 legacy offer, rail flip, stake framing (§2.3, §2.1, §2.6) | `p2v3_a1_legacy`, `p2v3_a1_railflip`, `p2v3_a1_stake_*` | **v1.2** | adjudicate | Settlement texts emitted are the v1.2 mapping (incl. "chargeback") |
| Phase 2 tier 1, H4 (§2.4) | `p2v3_tier1.jsonl` | **v1.2** (R1 arm shows it to the agents) | `acs/tier1.py` | Escalations decided by A1 under v1.2 |
| Phase 2 capture duty, 48/48 (§2.5) | `p2v13_capture.jsonl`, `data/disputes/capture_cases.json` | **v1.3** | adjudicate with `capture.use_v13()` | Same three-way allocation as v1.4 for these cases |
| Phase 3 optimised attacks, arms A-D, T, R (`results/PHASE3_ATTACKS.md`) | `results/phase3/p3_*.jsonl` | **v1.2** | adjudicate (A1), rule engine v1.2 (A2) | Owned by another lane; listed for completeness |
| Phase 3b provenance gate (`results/PHASE3B_PROVENANCE.md`) | `results/phase3/p3_G*.jsonl` | **v1.2** plus the Amendment 14 gate | rule engine v1.2 with `provenance_gate=True` | Owned by another lane |
| Expert labelling kit (`expert/`) | `expert/cases.html`, `answer_key.json` | built for v1.2 + v1.3 (c20dd29); **rebuilt for v1.4** after Audit 1 | `acs/expert_kit.py` | The answer key carries both the historical (v1.2/v1.3) and the v1.4 label; label changes listed in the corrections file |
| Label adjudication and its v1.5 re-score (`results/LABEL_ADJUDICATION_2026-11-04.md`) | `expert/answer_key_v1.4_adjudicated.json`; the label files; `p2v3_a1_grid.jsonl` | **v1.4** (adjudicated key); the addendum re-scores under **v1.5** | `acs/label_adjudication.py`, `acs/burden_rescore.py` | Post-audit, exploratory, author-side; the v1.5 re-score applies ABS-V1 to stored labels and cases, no model call |
| Rule-completeness simulation (`standard/sim/`) | `standard/sim/*` | its own ABS v0.1/v0.2 rule implementation, not `rulebook/` | `standard/sim/engine.py` | Owned by another lane |
| ABS v0.3 normative core (`standard/ABS_v0.3.md` A4, A4.4, A5.7, A6) | - | corresponds to **v1.5** (A4.1 Step 3 "What binds as an explicit term", as amended after Audit 1 in 970a4a4; ABS-V1 in A4.1 Step 1 and A5.7, founder ruling 2) | - | The A4 preamble says the executable rulebooks v1.2 and v1.3 bind only machine-readable terms and are not updated; v1.5 (v1.4 plus ABS-V1) is the executable form of the amended A4 |

## How to tell which rulebook a stored record used

- A2 receipts carry `"engine": "abs-rules/1.2"`; receipts under the current core carry `"abs-rules/1.5"`.
- A1 records do not store the rulebook version; it follows from the file prefix (`p2_` = v1.1,
  `p2v2_`/`p2v3_` = v1.2, `p2v13_` = v1.3) and from the commit in `results/CHRONOLOGY.md`.
- Case labels: `data/disputes/cases.json` = v1.2; `data/disputes/capture_cases.json` = v1.3.

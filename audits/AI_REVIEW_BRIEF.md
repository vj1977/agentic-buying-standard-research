You are an independent, brutally critical reviewer (a different model family from the authors). READ-ONLY: change nothing,
run no network commands, call no APIs, do not run any LLM CLI. Your final message is saved as the review.

Project: the Agentic Buying Standard (ABS) research by Vadims Juruss (27 years in cards, instant payments and internet
banking). Narrowed core: (1) the "authorised but wrong" dispute taxonomy and the mandate-precision liability rule (a breach
of any explicit term in the signed mandate or Allowance, including captured item requirements such as "16 GB", or a
capture failure, makes the agent provider liable; satisfying every explicit term but not the user's unstated intent puts it
on the user, withdrawal right intact; a non-conforming delivery or a manipulative offer makes the merchant liable); (2) a
minimum evidence standard (levels E0-E3); (3) an AI Decision Center (LLM fact-finders, deterministic rules, signed
receipts, human review on request, federated nodes, transparency log); (4) a benchmark of AI dispute judges under deception
(A1 end-to-end, A2 hybrid, A3 cross-family quorum). Layered on AP2/FIDO, UCP/ACP, Visa/Mastercard agent frameworks, card
and ISO 20022 flows. Central empirical claims: evidence makes AI judges accurate on honest disputes (Phase 2); under optimised attack, party-authored
evidence is the attack surface and only independent records decide (Phase 3). The paper, standard and [redacted: private material] are being
updated to Phase 3 while you read: flag any remaining "never deceived" / "fooled 1 of 20" claim as P0. Scrutinise the attack
harness hardest: is "fooled" scored correctly, could the attacker see ground truth, are the deviations (attacker swaps) fair?

Already done, do NOT repeat but DO check they were applied correctly: Audit 0 (thesis, `audits/AUDIT_0_THESIS.md`),
Audit 2 (regulatory, primary sources, `audits/AUDIT_2_REGULATORY.md`; applied in ABS v0.3 Appendix D), and a consistency
pass (`CONSISTENCY_REPORT.md`).

Review the CURRENT package, in this priority order:
1. `paper/main.md` + `paper/refs.bib` (the arXiv paper; would a NeurIPS/ICML workshop reviewer accept it?)
2. `results/` (PREREGISTRATION.md with amendments 1-14 and deviations 1-5, PILOT_RESULTS.md, PHASE2_DISPUTES.md,
   phase2_summary.md, PHASE3_ATTACKS.md + phase3_summary.md (optimised JudgeDeceiver-style attacks on arbiters: fable
   fooled 12/14 at E3, grok 14/14, hybrid 6/14; attack code acs/attack.py), PHASE3B_PROVENANCE.md if present, run files) and the harness that produced them: `acs/`, `tests/`, `data/`, `rulebook/`, `expert/`
3. `standard/ABS_v0.3.md` (normative core A1-A15, annex, appendices), `standard/ABS_ONE_PAGER.md`, `standard/LANDSCAPE.md`,
   `standard/scenarios/`, `standard/sim/` (REPORT.md, results.json, engine and rules)
4. [redacted: private application material]

Find and report, with file:line evidence:
1. BUGS: code defects in the harness, metrics, scoring, rule engine, sim, parsing, statistics (wrong denominators, Wilson or
   clustered intervals, McNemar use, mis-scored outcomes, leakage of ground truth or answer keys into prompts, seeds,
   exclusions), and tests that do not test what they claim.
2. MISMATCHES: every place where the paper, standard, rulebook (JSON and MD), rule engine, sim, preregistration, results and
   [redacted: private material] disagree (liability rule, H1-H7/H6b, E0-E3, reason codes AG0-AG5 incl. AG1-C, numbers quoted vs results).
3. RESEARCH VALIDITY: construct validity of traps and disputes, author-written ground truth, ceiling effects, multiple
   comparisons, preregistration discipline (were amendments dated before the runs they govern?), same-family judge bias,
   the weak red-team, post-hoc analyses presented as confirmatory, what the data can and cannot support.
4. STANDARD QUALITY: internal contradictions, undefined terms, schemas that do not validate or do not match the prose, any
   remaining legal overclaim after Audit 2, places where ABS reinvents an existing standard unnecessarily.
5. [redacted: private application material]
6. IMPROVEMENTS: the 15 highest-value improvements, ranked, each with the exact change and how to verify it.

Format: Executive summary (10 bullets) -> Findings table (ID, severity P0/P1/P2, category, file:line, finding, evidence,
fix) -> Top-15 improvements -> What you could not verify. Be concrete; no generic advice.

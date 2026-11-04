# Who pays when the agent is wrong?

Evidence, adjudication and optimised evidence fabrication in agentic commerce, with the Agentic Buying Standard (ABS)
draft it tests.

## Finding

When an AI agent buys under a user's mandate, a new kind of dispute appears: the payment was authorised and the merchant
performed, but the agent broke an instruction, failed to capture a requirement, or the user wanted something never
said. This repository asks whether AI arbiters can settle such disputes from records. On 51 synthetic disputes with
known ground truth, two end-to-end arbiters rose from 82% and 61% liable-party accuracy on card-dispute evidence to 98%
and 96% with a full evidence package (exact McNemar p = 0.008 and 4e-5). An optimising attacker that rewrote only its
own party's submissions then fooled them on 12 and 14 of 14 case-sides, with signed and chained records in evidence. A
hybrid design (models find facts, rules decide) was fooled on 6 of 14 against 10 of 14 at an equal budget, a difference
these data do not establish (p = 0.125). Defences built after seeing the attacks trade safety against usefulness. A
revised gate that checks what each cited record says was then tested once, frozen before any call (confirmatory
amendment C1), on 14 fresh case-sides with an attacker that saw the gate's verdicts: best-of-5 attack success fell from
11 of 14 with the gate off to 0 of 14 with it on (exact McNemar, one-sided p = 0.00049). On the 51 ordinary disputes the
same gate sent 34 to a human, and correct decided outcomes fell from 48 to 16 of 51.

## Status

- **Simulated data.** Every marketplace, dispute, evidence package and payment is synthetic and author-built. The cases
  carry cues the generator designed, photographs are text descriptions, and the ground truth is the author's rulebook.
  There is no field data.
- **Small n.** 51 disputes in Phase 2 (44 source references); 14 attacked case-sides in Phase 3; 14 fresh case-sides in
  C1. Judges and attackers come from three model families in total.
- **Confirmatory test: done, and in the paper.** Confirmatory amendment C1 (`results/CONFIRMATORY_C1.md`) was frozen
  before any of its model calls. Hypothesis H11 is supported: with a gate-aware attacker, the attack succeeded on 11 of 14
  fresh case-sides with gate v3 off and on 0 of 14 with it on (exact McNemar, one-sided p = 0.00049). The cost is large:
  on the 51 Phase 2 cases the gate sent 34 to human review, and correct decided outcomes fell from 48 of 51 to 16 of 51.
  The paper reports C1 in its abstract, Section 7, Figure 3 and Appendix G; the earlier gate results on stored outputs
  stay labelled exploratory.
- **Human baseline: open.** The blind labelling kit is built. Only the author has labelled part of it (8 of 40), which is
  not independent. See "Contributing blind labels".
- **Pre-registration.** `results/PREREGISTRATION.md` holds the hypotheses and every dated amendment and deviation;
  `results/CHRONOLOGY.md` states, analysis by analysis, whether it was prospective, informed by earlier data, amended
  after data or exploratory. Several analyses are exploratory, and the documents say which.
- **Review.** The paper is a preprint and has not been peer reviewed. Two rounds of independent AI review (an independent
  AI reviewer from another model family) and a regulatory audit are in `audits/`, with the corrections they caused.
- **The standard** (`standard/ABS_v0.3.md`) is a draft for review. It has not been discussed with a scheme, an issuer or
  a standards body, and it is not certified against any regulation.

## What is in this repository

| Path | What |
|---|---|
| `paper/` | The paper (`main.md`, `refs.bib`), its figures and the script that builds them (`build.sh`) |
| `standard/` | ABS drafts v0.2 and v0.3 (v0.1 is a stub), the one-pager, the landscape table, the adoption note, the scenario catalogue (`scenarios/`) and the rule-completeness simulation (`sim/`) |
| `rulebook/` | The Agentic Dispute Rulebook, every version the experiments used (`VERSIONS.md` maps them) |
| `acs/` | The experiment harness: marketplace, payment controls, agents, dispute cases, evidence packages, arbiters, hybrid rule engine, attacks, provenance gate, analyses |
| `tests/` | Harness tests (mock backends only; no model calls) |
| `tools/schema_check/` | Validator for the schemas and examples embedded in ABS v0.3 |
| `data/` | Catalogue, shopping scenarios, dispute case sets, gate-coverage carts, the C1 frozen manifest |
| `results/` | Every run log, the model-call ledger (`calls.jsonl`, `call_blobs/`), summaries and write-ups (`PILOT_RESULTS.md`, `PHASE2_DISPUTES.md`, `PHASE3_ATTACKS.md`, `PHASE3B_PROVENANCE.md`, `CONFIRMATORY_C1.md`) |
| `expert/` | The blind labelling kit and its scorer |
| `research/` | Related-work notes and bibliography |
| `audits/` | Audits 0 to 4 and the briefs given to the AI reviewer |
| `CONFORMANCE.md` | How a third-party buying agent can run the scenario suites (`python3 -m acs.conformance`) |
| `CONSISTENCY_REPORT.md` | Every number in the deliverables checked against its source |

## How to reproduce

Python 3.14, standard library only.

```bash
python3 -m unittest discover -s tests -t .           # harness tests, mock backends, no model calls
python3 -m unittest discover -s standard/sim -t .    # rule-simulation tests
python3 -m tools.schema_check standard/ABS_v0.3.md   # embedded schemas and Appendix F examples
python3 -m acs.confirmatory_c1 check                 # the files C1 froze still match their manifest
python3 standard/sim/run.py                          # rule-completeness simulation (rewrites standard/sim/REPORT.md, results.json, receipts.jsonl)
python3 -m acs.analyze_phase2                        # Phase 2 tables from the stored runs
python3 -m acs.analyze_c1                            # C1 tables from the stored runs
paper/build.sh                                       # figures, LaTeX, HTML and PDF of the paper
```

The harness run reports eight skips (six tests and two whole test modules), because the expert answer keys and label
files are withheld (see `expert/README.md`). The simulation and the two analyses above regenerate their stored outputs unchanged,
so `git status` stays clean after running them.
`paper/build.sh` needs pandoc 3 or later, and Google Chrome or Chromium for the figure PDFs and `main.pdf`; it writes to
`paper/build/`, which is not tracked.

The stored model outputs are enough to check every reported number. Re-running the model experiments needs the `claude`,
`grok` or `codex` command-line tools logged in on the machine; each call runs in an empty temporary directory with the
tool's own tools disabled, and the run stops if that isolation cannot be verified (`acs/backends.py`).

## How to cite

```bibtex
@misc{juruss2026whopays,
  author = {Vadims Juruss},
  title  = {Who pays when the agent is wrong? Evidence, adjudication and optimised evidence fabrication in agentic commerce},
  year   = {2026},
  note   = {Preprint and research repository, version of 4 November 2026}
}
```

## Contributing blind labels

The study needs independent labels for its 40-case kit, especially from people who handle card disputes, consumer
claims or payments operations. You need a browser and about two hours.

The kit is blind only by procedure. The answer key can be rebuilt from the public code (`python3 -m acs.expert_kit`
writes it, and its SHA-256 matches the commitment in `expert/README.md`), so a labeller must work from the two kit files
alone. If you recruit labellers, give them `expert/cases.html` and `expert/labels_template.csv` only, not a link to
this repository.

1. Take `expert/cases.html` and `expert/labels_template.csv` and nothing else from this repository.
2. Follow `expert/README.md`: label each case, export the CSV.
3. Open an issue at <https://github.com/vj1977/agentic-buying-standard-research/issues> titled "Blind labels" and attach
   the CSV (or paste its contents). Issues are the only route; there is no email address. Issues are public, so do not
   open other labellers' issues, or anything else in this repository, until you have exported your own labels.

Each submission is scored against the committed key, and every disagreement is classified in a dated amendment.

## About this copy

This is a public copy of a private working repository, with fresh history. Commit hashes cited in the documents (for
example the C1 freeze `10b5013`) refer to the private development history and do not exist here. The pre-registration
timestamps the documents cite (when each amendment was committed relative to its first model call, for example C1's
amendment 15 seconds before its first call) are commit times in that private history; this copy's single commit cannot
show them. Private notes and application
material were left out; where a kept document referred to them, the passage is marked `[redacted: ...]`. The Claude
account email in run metadata and logs is replaced by `author@example.invalid`, and absolute paths are made relative.
No recorded hash covers those fields, and the analyses reproduce their stored outputs from the edited logs.

## Licence

Copyright 2026 Vadims Juruss.

- **Code**, under the Apache License 2.0 (`LICENSE`): every `*.py` and `*.sh` file and `.github/workflows/ci.yml`. That
  covers `acs/`, `tools/`, `tests/`, the code in `standard/sim/` and `standard/scenarios/`, `paper/build.sh`,
  `paper/figures/make_figures.py`, `expert/score_expert.py` and `results/runs/main_launch.sh`.
- **Everything else**, under Creative Commons Attribution 4.0 International (`LICENSE-docs`): the paper and its figures,
  the standard and its write-ups, the rulebook, the data, the results, the research notes, the audits, the expert kit
  page and template, `CONFORMANCE.md`, `CONSISTENCY_REPORT.md` and `models.json`.
- Third-party works that the repository cites or uses keep their own terms; see `THIRD_PARTY_NOTICES.md`.

# Blind expert labelling kit (Amendment 11)

The kit asks a labeller to decide 40 agent-purchase disputes from the evidence shown, under the reference rules printed
on the page (rulebook v1.4, matching ABS v0.3). It is the study's planned human baseline. So far only the author has
labelled part of it (8 of 40), which is not an independent baseline. Independent blind labels are still needed.

## For a labeller

Work from two files only: `cases.html` and `labels_template.csv`. Do not read the rest of this repository before you
have exported your labels. The cases are drawn from the study's dispute set, and the repository publishes that set with
its ground truth (see "Why the kit is blind only by procedure" below).

1. Open `cases.html` in a browser. It works offline and needs nothing else.
2. For each of the 40 cases, choose the liable party and the remedy, give your confidence (1-5), and add notes where you
   disagree with the rules or the evidence is unclear. Answers are saved in the browser as you go. Allow about 3 minutes
   per case, under 2 hours in total.
3. Click **Export labels (CSV)** and save `expert_labels.csv`. Alternatively, fill in `labels_template.csv` by hand.
4. Open an issue at <https://github.com/vj1977/agentic-buying-standard-research/issues> titled "Blind labels" and attach
   the CSV (see "Contributing blind labels" in the repository README). There is no email route. Issues are public, so do
   not open other labellers' issues before you have exported your own labels.

## Scoring

`python3 expert/score_expert.py expert_labels.csv` scores a label file against the answer key and writes
`results/expert_baseline.md`. It reports agreement with the v1.4 label the page asks for and with the historical label
the arbiters were scored against (v1.2, or v1.3 for capture cases). The key is not in this copy; the author scores
submitted labels.

Every disagreement with the ground truth is reviewed and classified as one of:
- ground-truth error (fixed in a new dated amendment, with everything re-scored);
- policy disagreement;
- evidence ambiguity;
- labeller slip.

The classification is recorded in a dated amendment. Nothing is changed silently.

## Answer-key commitment

The answer keys are withheld from this copy. These are the SHA-256 digests of the files the study used:

| File | SHA-256 |
|---|---|
| `expert/answer_key.json` (v1.4 and historical labels) | `677fb27ebca688ad248a405dd7a59ea25383de6c8a6bb81c1a82ca2e8d76e5a9` |
| `expert/answer_key_v1.4_adjudicated.json` (exploratory, evidence-conditional) | `c2819ea2785936628c3f0910a5b002479f9abf1e273370a3941b511f2b700642` |

## Why the kit is blind only by procedure

The kit is built deterministically from the public case files in `data/disputes/` (`python3 -m acs.expert_kit`, seed
4711). Running it rewrites `cases.html` and `labels_template.csv` unchanged and writes an `answer_key.json` whose
SHA-256 matches the commitment above. Anyone can therefore check that the key used is the key committed, but the
commitment does not hide the key. The kit stays blind only if a labeller works from the two kit files alone. If you
recruit labellers, send them those two files, not a link to this repository.

## History

The kit was rebuilt after Audit 1 (2026-11-04, before any label was given) with the same seed: the 40 cases, their
evidence levels, the anonymous ids and every case card are unchanged. The reference rules on the page now state rulebook
v1.4, including the withdrawal right with its prerequisites (prior express consent, acknowledgement of losing the right
and the trader's confirmation, CRD Art 16(m)). Where a prerequisite is not in the evidence shown, the remedy to choose is
"undetermined", not "deny". Two of the 40 v1.4 labels differ from the historical labels; which ones, and why, is
recorded in the study's result files and is left out here so that this page reveals no label.

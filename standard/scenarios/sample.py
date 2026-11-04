#!/usr/bin/env python3
"""Stratified sample of the catalogue for the frontier-model experiment (llm_sample.json).

Deterministic. Covers every lifecycle stage, rail family, attack class and ground-truth liability
outcome, weighted toward hard and ambiguous cases (debatable/uncertain/design-proposal ground
truth, evidence missing or conflicting, adversarial parties, pairs on the explicit-vs-unstated
line, partial liability, cases v0.1 as written gets wrong). Core dispute/evidence/liability
scenarios are primary; roadmap families contribute a smaller share. A held-out split (about one
third) is assigned by a hash of the id so it is stable across regenerations.

    python3 standard/scenarios/sample.py
"""

from __future__ import annotations

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.join(os.path.dirname(HERE), "sim")
if SIM not in sys.path:
    sys.path.insert(0, SIM)
from engine import compare, decide  # noqa: E402

CAT = os.path.join(HERE, "catalogue.json")
OUT = os.path.join(HERE, "llm_sample.json")
TARGET = 96
HELDOUT_SHARE = 3  # 1 in 3 by hash
CORE = {"merchant_failure", "agent_failure", "user_side", "attack", "dispute_process", "overlay", "lifecycle"}
HARD_TAGS = {"debatable", "uncertain_law", "ambiguity", "both_honest", "evidence_missing", "evidence_conflict", "adversarial_merchant", "adversarial_buyer",
             "partial_liability", "apportionment", "principle_boundary", "unstated_intent", "intent_scope", "one_side_lying", "evidence_tampering", "realistic_evidence",
             "human_review", "feed_vs_snapshot", "frozen_offer", "injection", "collusion", "kickback", "step0", "unauthorised"}


def difficulty(s: dict, v01_wrong: bool) -> int:
    score = 0
    gt = s["ground_truth"]
    if gt["certainty"] in ("debatable", "uncertain", "design_proposal", "general_law"):
        score += 2
    score += len(HARD_TAGS & set(s["tags"]))
    if s["facts"].get("evidence_state") != "sufficient":
        score += 2
    if any(s["parties"][p] == "malicious" for p in ("user", "agent_provider", "merchant")):
        score += 1
    if gt["liable_party"] in ("merchant+agent_provider", "undetermined", "rail_unauthorised_regime", "programme_guarantee"):
        score += 2
    if v01_wrong:
        score += 2
    if s["origin"] == "curated":
        score += 1
    return score


def split_of(sid: str) -> str:
    h = int(hashlib.sha256(sid.encode()).hexdigest(), 16)
    return "heldout" if h % HELDOUT_SHARE == 0 else "dev"


def main():
    with open(CAT, encoding="utf-8") as fh:
        cat = json.load(fh)
    S = cat["scenarios"]
    v01 = {s["id"]: compare(decide(s, "v0.1"), s) for s in S}
    scored = sorted(S, key=lambda s: (-difficulty(s, not v01[s["id"]]["consistent"]), s["id"]))
    chosen: list[dict] = []
    chosen_ids: set[str] = set()

    def need(key_fn, universe):
        covered = {key_fn(s) for s in chosen}
        for s in scored:
            k = key_fn(s)
            if k in universe and k not in covered and s["id"] not in chosen_ids:
                chosen.append(s)
                chosen_ids.add(s["id"])
                covered.add(k)

    # strata: every stage, every rail family, every attack event, every liability outcome, every class, every segment
    stages = set(cat["dimensions"]["stages"])
    for st in sorted(stages):
        if not any(st in s["stages"] for s in chosen):
            for s in scored:
                if st in s["stages"] and s["id"] not in chosen_ids:
                    chosen.append(s)
                    chosen_ids.add(s["id"])
                    break
    need(lambda s: s["rail_family"], {s["rail_family"] for s in S})
    need(lambda s: s["event"] if s["class"] == "attack" else None, {s["event"] for s in S if s["class"] == "attack"})
    need(lambda s: s["ground_truth"]["liable_party"], {s["ground_truth"]["liable_party"] for s in S})
    need(lambda s: s["ground_truth"]["reason_code"], {s["ground_truth"]["reason_code"] for s in S})
    need(lambda s: s["class"], {s["class"] for s in S})
    need(lambda s: s["segment"], {s["segment"] for s in S})
    need(lambda s: s["rail"], {s["rail"] for s in S})
    # explicit-vs-unstated pairs, evidence states, product-spec pair
    for ev in ("A01", "A01b", "A03", "A03b", "A07", "A07b", "AL03", "AL03b", "D14a", "D14b", "D15", "D15b", "P10", "P10b", "U06", "X11", "D03", "M09", "M17", "X04", "X13", "X06", "D02", "L01", "M20", "X07"):
        if not any(s["event"] == ev for s in chosen):
            for s in scored:
                if s["event"] == ev:
                    chosen.append(s)
                    chosen_ids.add(s["id"])
                    break
    # fill to target: hardest core first, then hardest roadmap, keeping events distinct where possible
    events = {s["event"] for s in chosen}
    for s in scored:
        if len(chosen) >= TARGET:
            break
        if s["id"] in chosen_ids or s["event"] in events or s["class"] not in CORE:
            continue
        chosen.append(s)
        chosen_ids.add(s["id"])
        events.add(s["event"])
    for s in scored:
        if len(chosen) >= TARGET:
            break
        if s["id"] in chosen_ids or s["event"] in events:
            continue
        chosen.append(s)
        chosen_ids.add(s["id"])
        events.add(s["event"])
    chosen.sort(key=lambda s: s["id"])
    out_rows = []
    for s in chosen:
        r = dict(s)
        r["split"] = split_of(s["id"])
        r["difficulty"] = difficulty(s, not v01[s["id"]]["consistent"])
        r["v0.1_as_written_correct"] = v01[s["id"]]["consistent"]
        r["family"] = "core" if s["class"] in CORE else "roadmap"
        out_rows.append(r)
    counts = {
        "total": len(out_rows), "dev": sum(1 for r in out_rows if r["split"] == "dev"), "heldout": sum(1 for r in out_rows if r["split"] == "heldout"),
        "core": sum(1 for r in out_rows if r["family"] == "core"), "roadmap": sum(1 for r in out_rows if r["family"] == "roadmap"),
        "by_class": {}, "by_rail_family": {}, "by_liable_party": {}, "by_reason_code": {}, "by_segment": {}, "stages_covered": sorted({st for r in out_rows for st in r["stages"]}),
        "attack_events_covered": sorted({r["event"] for r in out_rows if r["class"] == "attack"}),
    }
    for r in out_rows:
        for key, val in (("by_class", r["class"]), ("by_rail_family", r["rail_family"]), ("by_liable_party", r["ground_truth"]["liable_party"]), ("by_reason_code", r["ground_truth"]["reason_code"]), ("by_segment", r["segment"])):
            counts[key][val] = counts[key].get(val, 0) + 1
    doc = {"sample_version": cat["catalogue_version"], "purpose": "frontier-model arbiter experiment: each model receives the scenario at evidence levels E0..E3 and returns reason code, liable party, remedy, confidence",
           "instructions_for_experiment": ["hide ground_truth, expected_settlement, v0.1_as_written_correct and difficulty from the model", "present facts only through the evidence items listed for the level under test",
                                           "the heldout split is for the confirmatory run; dev for prompt development", "score reason code (taxonomy in sim/REPORT.md Core 1), liable party, remedy class, calibration"],
           "counts": counts, "scenarios": out_rows}
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(json.dumps({k: v for k, v in counts.items() if k not in ("stages_covered", "attack_events_covered")}, indent=1))
    print("stages covered:", len(counts["stages_covered"]), "of", len(stages), "| attack events covered:", len(counts["attack_events_covered"]))


if __name__ == "__main__":
    main()

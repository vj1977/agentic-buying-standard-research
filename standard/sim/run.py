#!/usr/bin/env python3
"""Run every catalogue scenario through the ABS engine and write sim/REPORT.md, sim/results.json
and sim/receipts.jsonl (one v0.2 full-evidence receipt per scenario).

    python3 standard/sim/run.py
"""

from __future__ import annotations

import json
import os
import sys
from collections import Counter, defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import antiscam  # noqa: E402
import entry_gate  # noqa: E402
from engine import LEVELS, RULESET_ID, VERSIONS, compare, decidable_at, decide  # noqa: E402
from rails import standards_gap_table  # noqa: E402
from rules import PROPOSED_PROCESS_TEXT, RULES  # noqa: E402

CATALOGUE = os.path.join(os.path.dirname(_HERE), "scenarios", "catalogue.json")
REPORT = os.path.join(_HERE, "REPORT.md")
RESULTS = os.path.join(_HERE, "results.json")
RECEIPTS = os.path.join(_HERE, "receipts.jsonl")
CORE_CLASSES = {"merchant_failure", "agent_failure", "user_side", "attack", "dispute_process", "overlay", "lifecycle"}
ROADMAP_CLASSES = {"anti_scam", "entry_route", "product_spec", "allowance", "segment"}


def load():
    with open(CATALOGUE, encoding="utf-8") as fh:
        return json.load(fh)


def pct(a, b):
    return f"{a}/{b} ({(100.0 * a / b) if b else 0:.1f}%)"


def money_range(lo: dict, hi: dict) -> str:
    """Nominal amounts per currency (never converted or added across currencies); 'a to b' where a bound differs."""
    parts = []
    for c in sorted(set(lo) | set(hi)):
        a, b = lo.get(c, 0.0), hi.get(c, 0.0)
        parts.append(f"{c} {a:,.2f}" if a == b else f"{c} {a:,.2f} to {b:,.2f}")
    return "; ".join(parts) or "none"


def loss_range(d: dict, who: str) -> str:
    return money_range(d[f"{who}_loss_min_by_currency"], d[f"{who}_loss_max_by_currency"])


def ids(lst, cap=40):
    lst = sorted(lst)
    return ", ".join(lst[:cap]) + (f" (+{len(lst) - cap} more)" if len(lst) > cap else "")


def analyse(scenarios: list[dict]) -> dict:
    out = {"versions": {}}
    live = [s for s in scenarios if s["facts"]["transaction_occurred"] and s["facts"].get("dispute_filed", True)]
    out["n"] = len(scenarios)
    out["n_live"] = len(live)
    out["n_core"] = sum(1 for s in scenarios if s["class"] in CORE_CLASSES)
    receipts_v02 = {}
    for v in VERSIONS:
        R = {}
        for s in scenarios:
            R[s["id"]] = (decide(s, v), compare(decide(s, v), s))
        if v == "v0.2":
            receipts_v02 = {k: r for k, (r, _) in R.items()}
        gaps = defaultdict(list)
        contradictions = defaultdict(list)
        conflicts_resolved = defaultdict(list)
        conflicts_unresolved = defaultdict(list)
        overlay_gaps = defaultdict(list)
        infeasible = []
        collection_only = []
        feas_class = Counter()
        non_funds = Counter()
        outcome_all = Counter()
        outcome_live = Counter()
        standards_gaps = defaultdict(list)
        by_class = defaultdict(Counter)
        by_segment = defaultdict(Counter)
        by_code = Counter()
        decidable = Counter()
        decidable_by_class = defaultdict(Counter)
        human = Counter()
        withdrawal_resolves = []
        for s in scenarios:
            r, c = R[s["id"]]
            cls, seg = s["class"], s["segment"]
            by_class[cls]["n"] += 1
            by_segment[seg]["n"] += 1
            outcome_all[c["outcome"]] += 1
            for bucket in (by_class[cls], by_segment[seg]):
                bucket[c["outcome"]] += 1
            if c["covered"]:
                by_code[r["decision"]["reason_code"]] += 1
            else:
                gaps[f"indeterminate:{c['indeterminate_reason']}"].append(s["id"])
                by_class[cls]["gaps"] += 1
                by_segment[seg]["gaps"] += 1
            if c["consistent"]:
                by_class[cls]["consistent"] += 1
                by_segment[seg]["consistent"] += 1
            elif c["covered"]:
                contradictions[(s["event"], s["event_name"], c["decision_liable"], c["decision_remedy_class"], c["gt_liable"], c["gt_remedy_class"])].append(s["id"])
                by_class[cls]["contradictions"] += 1
                by_segment[seg]["contradictions"] += 1
            if r["conflict"]:
                key = (s["event"], tuple(r["conflicting_parties"]), r["decision"]["decided_by"])
                (conflicts_resolved if c["consistent"] else conflicts_unresolved)[key].append(s["id"])
                if not c["consistent"]:
                    by_class[cls]["unresolved_conflicts"] += 1
                    by_segment[seg]["unresolved_conflicts"] += 1
            if r["process"].get("non_participant_bound"):
                gaps["decision binds a non-participant (no Participation Agreement)"].append(s["id"])
            if not r["process"]["rail_execution_defined"] and r["settlement_instruction"] and r["settlement_instruction"]["type"] not in ("none",):
                gaps["rail execution undefined for this rail in v0.1 (only card and a2a_instant)"].append(s["id"])
            if r["process"]["appeal"] == "not_available_in_v0.1":
                gaps["appeal requested; v0.1 has no appeal procedure"].append(s["id"])
            if r["process"]["parallel_rail_dispute"] == "no_rule_in_v0.1":
                gaps["parallel rail dispute; v0.1 has no single-track / double-recovery rule"].append(s["id"])
            if r["human_review"]["requested"] and not r["human_review"]["available_on_request"]:
                gaps["human review requested; v0.1 has no human-review right"].append(s["id"])
            si = r["settlement_instruction"]
            if si and si["feasibility"]["class"] == "infeasible":
                infeasible.append((s["id"], s["rail"], si["feasibility"]["reason"], si["feasibility"].get("fallback")))
            if si and si["feasibility"]["class"] == "collection":
                collection_only.append((s["id"], s["rail"], si["feasibility"]["reason"]))
            if si and si["moves_funds"]:
                feas_class[si["feasibility"]["class"]] += 1
            elif si and si["type"] != "none":
                non_funds[si["type"]] += 1
            if si and si.get("standard_gap"):
                standards_gaps[(s["rail_family"], si["type"])].append(s["id"])
            for o in r["overlays"]:
                if o["applies"] and not o["stated_in_v0.1"]:
                    overlay_gaps[o["id"]].append(s["id"])
            if s in live:
                lvl = decidable_at(s, v) or c["outcome"]  # a level when determinate, else 'escalated' / 'no_rule'
                decidable[lvl] += 1
                decidable_by_class[cls][lvl] += 1
                outcome_live[c["outcome"]] += 1
            h = r["human_review"]
            human["requested"] += h["requested"]
            human["auto_escalated"] += h["auto_escalated"]
            human["escalated"] += h["escalated"]
            if r["withdrawal_resolves"]:
                withdrawal_resolves.append(s["id"])
        out["versions"][v] = {
            "covered": outcome_all["determinate"] + outcome_all["escalated"], "determinate": outcome_all["determinate"], "escalated": outcome_all["escalated"],
            "no_rule": outcome_all["no_rule"], "consistent": sum(1 for s in scenarios if R[s["id"]][1]["consistent"]), "live_outcomes": dict(outcome_live),
            "gaps": {k: v2 for k, v2 in gaps.items()}, "contradictions": {" | ".join(map(str, k)): v2 for k, v2 in contradictions.items()},
            "conflicts_resolved": {" | ".join(map(str, k)): v2 for k, v2 in conflicts_resolved.items()},
            "conflicts_unresolved": {" | ".join(map(str, k)): v2 for k, v2 in conflicts_unresolved.items()},
            "overlay_gaps": dict(overlay_gaps), "infeasible_settlements": infeasible, "collection_only_settlements": collection_only,
            "settlement_feasibility_classes": dict(feas_class), "settlement_non_funds_instructions": dict(sorted(non_funds.items())),
            "standards_gaps": {" | ".join(k): v2 for k, v2 in standards_gaps.items()},
            "by_class": {k: dict(c) for k, c in sorted(by_class.items())}, "by_segment": {k: dict(c) for k, c in sorted(by_segment.items())},
            "by_reason_code": dict(sorted(by_code.items())), "decidable_at": dict(decidable), "decidable_by_class": {k: dict(c) for k, c in sorted(decidable_by_class.items())},
            "human_review": dict(human), "withdrawal_resolves": withdrawal_resolves,
        }
    # Which v0.2 rule repairs each v0.1 failure (gap or contradiction) -> ranked fixes.
    repair = defaultdict(list)
    v1 = {s["id"]: compare(decide(s, "v0.1"), s) for s in scenarios}
    for s in scenarios:
        if not v1[s["id"]]["consistent"]:
            r2 = receipts_v02[s["id"]]
            repair[r2["decision"]["decided_by"] or "none"].append(s["id"])
    out["repairs_by_v02_rule"] = {k: sorted(v) for k, v in sorted(repair.items(), key=lambda kv: -len(kv[1]))}
    # Product spec: decidable with vs without the signed spec (legacy mode).
    spec_rows = []
    for s in scenarios:
        if s["class"] != "product_spec":
            continue
        with_spec = decide(s, "v0.2")
        legacy = decide(s, "v0.2", legacy_spec=True)
        spec_rows.append({"id": s["id"], "event": s["event"], "with_signed_spec": with_spec["findings"]["conformity"]["established"],
                          "legacy_free_text_only": legacy["findings"]["conformity"]["established"],
                          "decided_with": with_spec["decision"]["liable_party"], "decided_legacy": legacy["decision"]["liable_party"], "legacy_rule": legacy["decision"]["decided_by"]})
    out["product_spec"] = spec_rows
    out["antiscam"] = antiscam.run(scenarios)
    out["entry_gate"] = entry_gate.run(scenarios)
    out["standards_gap_table"] = standards_gap_table()
    out["receipts_v02"] = receipts_v02
    return out


def write_receipts(receipts: dict):
    with open(RECEIPTS, "w", encoding="utf-8") as fh:
        for sid in sorted(receipts):
            fh.write(json.dumps(receipts[sid], ensure_ascii=False, sort_keys=True) + "\n")


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out) + "\n"


POST_AUDIT_1_DATE = "2026-11-04"
POST_AUDIT_1_BASE = "0203778"  # repository HEAD before the Audit 1 simulation fixes


def post_audit_1(A: dict, nl: int) -> list[str]:
    """Dated record of Audit 1 (audits/AUDIT_1_INDEPENDENT_AI_REVIEW.md F16, F17, F25, F26-sim): the 'before' column is the
    report as it stood at POST_AUDIT_1_BASE; the 'after' column is computed from this run."""
    n = A["n"]
    v1, v2 = A["versions"]["v0.1"], A["versions"]["v0.2"]
    d1, d2 = v1["decidable_at"], v2["decidable_at"]
    fc1, fc2, nf2 = v1["settlement_feasibility_classes"], v2["settlement_feasibility_classes"], v2["settlement_non_funds_instructions"]
    a, b = A["antiscam"]["summary"]["A_no_gate"], A["antiscam"]["summary"]["B_abs_gate"]
    det2, det1 = sum(d2.get(l, 0) for l in LEVELS), sum(d1.get(l, 0) for l in LEVELS)
    cure, refer, deferred = nf2.get("cure_document", 0), nf2.get("refer_to_rail", 0) + nf2.get("refer_to_authority_process", 0), nf2.get("escalated_no_instruction_yet", 0)
    rows = [
        ["Scenarios (live disputes)", "528 (498)", f"{n} ({nl})", "unchanged; P04 and P08b now declare their size mapping and condition tolerance instead of hiding them in strings (F16)"],
        ["Live disputes determinate on E0 evidence, v0.2", "89/498 (17.9%) 'decidable'", f"{pct(d2.get('E0', 0), nl)} determinate", "unchanged count; now counts determinate outcomes only (F17)"],
        ["Minimum evidence package (E3), v0.2", "498/498 (100.0%) 'decided', of which 496 determinate and 2 escalated",
         f"{det2} determinate + {d2.get('escalated', 0)} escalated of {nl} ({100.0 * det2 / nl:.1f}% determinate); {d2.get('no_rule', 0)} with no rule",
         "an escalation to human review is not a decision; decidable_at no longer counts liable party 'undetermined' as determinate (F17)"],
        ["Undecidable even at E3, v0.2", "0", f"{d2.get('escalated', 0)} escalated (ABS-H1) + {d2.get('no_rule', 0)} with no rule", "same cases, honest label (F17)"],
        ["v0.1: E0 / by E3 / undecidable", "89 / 477 / 21", f"{d1.get('E0', 0)} / {det1} determinate / {d1.get('escalated', 0)} escalated / {d1.get('no_rule', 0)} no rule", "unchanged"],
        ["All scenarios, v0.2: decided / correct", "528/528 / 528/528",
         f"determinate {v2['determinate']}, escalated {v2['escalated']}, no rule {v2['no_rule']}; consistent with the stipulated ground truth {v2['consistent']}/{n}", "coverage, determinacy and consistency kept apart (F17)"],
        ["All scenarios, v0.1: decided / correct", "498/528 / 340/528",
         f"determinate {v1['determinate']}, escalated {v1['escalated']}, no rule {v1['no_rule']}; consistent {v1['consistent']}/{n}", "relabelled"],
        ["Settlement, v0.2: executable / collection only / infeasible (v0.1)", "357 / 9 / 26 (224 / 4 / 40)",
         f"{fc2.get('feasible', 0)} / {fc2.get('collection', 0)} / {fc2.get('infeasible', 0)} of {sum(fc2.values())} funds-moving ({fc1.get('feasible', 0)} / {fc1.get('collection', 0)} / {fc1.get('infeasible', 0)} of {sum(fc1.values())})",
         f"{cure} corrected documents, {refer} referrals and {deferred} escalations had been counted as executable funds-moving instructions (F17)"],
        ["Anti-scam with the gate, of 46 scams: stopped / refunded / unrecoverable", "38 / 5 / 3",
         f"{b['stopped']} / {b['refunded']} / {b['conditional']} conditional / {b['unrecoverable']}", "no conditional recovery with the gate on"],
        ["Anti-scam without the gate", "0 / 31 / 15", f"{a['stopped']} / {a['refunded']} / {a['conditional']} conditional / {a['unrecoverable']}",
         "ABS-S0164, ABS-S0310, ABS-C004 (UK Faster Payments; APP reimbursement uncertain) are conditional recovery, not refunds (F25)"],
        ["Buyer loss with the gate", "EUR 1,837.00", loss_range(b, "buyer"), "the old total added EUR and INR nominal amounts"],
        ["Buyer loss without the gate", "EUR 4,782.99", loss_range(a, "buyer"), "the old total added EUR, INR and USDC amounts and counted GBP 569.00 of uncertain reimbursement as refunded (F25)"],
        ["Loss moved to acquirer / operator / agent provider / PSPs, with / without the gate", "EUR 884.90 / EUR 6,138.90", f"{loss_range(b, 'system')} / {loss_range(a, 'system')}", "per currency; conditional rows give a range (F25)"],
        ["Core rules, v0.2: gaps / unresolved conflicts / contradictions", "0 / 0 / 0", "0 / 0 / 0", "now each asserted separately, with a v0.1 negative control (F26)"],
        ["Core rules, v0.1: gaps / unresolved conflicts / contradictions", "23 / 4 / 91", "23 / 4 / 91", "unchanged"],
        ["Human review: requested / auto-escalated / share escalated", "73 / 2 / 73/528 (13.8%)",
         f"{v2['human_review']['requested']} / {v2['human_review']['auto_escalated']} / {pct(v2['human_review']['escalated'], n)}", "unchanged"],
        ["Entry routes closed / loss-limited / open; EU withdrawal overlay resolves", "5 / 3 / 1; 50",
         f"{len(A['entry_gate']['closed'])} / {len(A['entry_gate']['limits_loss'])} / {len(A['entry_gate']['open'])}; {len(v2['withdrawal_resolves'])}", "unchanged"],
    ]
    return [f"## Post-audit (Audit 1), {POST_AUDIT_1_DATE}", "",
            f"Fixes for `audits/AUDIT_1_INDEPENDENT_AI_REVIEW.md` findings F16 (substring conformity), F17 (determinate vs escalated vs coverage vs feasibility), F25 (uncertain reimbursement) "
            f"and the simulation part of F26 (tests that test what their names say). Before = this report at commit `{POST_AUDIT_1_BASE}`; after = this run.", "",
            md_table(["headline number", "before", "after", "why"], rows),
            "Scenarios whose outcome changed:", "",
            "- Decisions: none, in either rule set. With the exact-identifier engine alone, 5 scenarios would flip from buyer/deny to merchant/refund: ABS-S0346 and ABS-S0347 (P04, "
            "promised 'EU 42 (= UK 14 = US 10)', delivered 'label UK 14') and ABS-S0360, ABS-S0361, ABS-S0465 (P08b, promised 'refurbished grade A (minor cosmetic marks allowed)', "
            "delivered 'refurbished grade A, two faint scratches'). Their signed specs carried the mapping and the tolerance only inside free strings, which the substring matcher happened "
            "to accept. They now declare `equivalents: [UK 14, US 10]` and `tolerance: {accept: [refurbished grade A with minor cosmetic marks]}` (raw observation kept in `observed`) "
            "and conform, as their stipulated ground truth says. The audit's counterexamples ('iPhone 16 Pro' -> 'iPhone 16'; 'new (not refurbished)' -> 'refurbished') are non-conforming.",
            "- Classification: ABS-S0073 and ABS-S0074 (D15, conflicting serials) were counted as decidable at E3; they are escalated, not determinate, and their settlement is "
            "`deferred`, not executable.",
            "- Anti-scam, without the gate: ABS-S0164, ABS-S0310 and ABS-C004 move from refunded to conditional recovery (GBP 120.00, 120.00 and 329.00; buyer loss between nothing and the amount).",
            f"- Settlement counting: {cure + refer + deferred} instructions that move no funds under ABS left the executable count; no instruction itself changed.", "",
            "Receipts now carry `findings.conformity.established_from` (at E3 with sufficient evidence: `stipulated_world_state`), `matched_by` on each conforming categorical attribute, "
            "`settlement_instruction.moves_funds` and the feasibility class `deferred`. In `results.json` the per-version `decided` / `correct` counts are replaced by `covered`, "
            "`determinate`, `escalated`, `no_rule` and `consistent`, and anti-scam rows carry loss bounds and their currency. Documents outside `standard/sim` and `standard/scenarios` "
            "that quote the old numbers (the paper, `standard/ABS_v0.3.md`) are not changed by this run.", ""]


def write_report(cat: dict, A: dict):
    S = cat["scenarios"]
    n, nl = A["n"], A["n_live"]
    v1, v2 = A["versions"]["v0.1"], A["versions"]["v0.2"]
    d1, d2 = v1["decidable_at"], v2["decidable_at"]
    e0_2 = d2.get("E0", 0)
    det_e3_2, det_e3_1 = sum(d2.get(l, 0) for l in LEVELS), sum(d1.get(l, 0) for l in LEVELS)
    esc2, nr2 = d2.get("escalated", 0), d2.get("no_rule", 0)
    hr2 = sum(1 for sid, r in A["receipts_v02"].items() if r["decision"]["reason_code"] == "ABS-H1")
    fc1, fc2 = v1["settlement_feasibility_classes"], v2["settlement_feasibility_classes"]
    nf2 = v2["settlement_non_funds_instructions"]
    nf_cure, nf_refer, nf_deferred = nf2.get("cure_document", 0), nf2.get("refer_to_rail", 0) + nf2.get("refer_to_authority_process", 0), nf2.get("escalated_no_instruction_yet", 0)
    core_live = [s for s in S if s["class"] in CORE_CLASSES and s["facts"]["transaction_occurred"] and s["facts"].get("dispute_filed", True)]
    core_ids = {s["id"] for s in S if s["class"] in CORE_CLASSES}
    core_gaps_v2 = sum(len([i for i in v if i in core_ids]) for v in v2["gaps"].values())
    core_contra_v2 = sum(len([i for i in v if i in core_ids]) for v in v2["contradictions"].values())
    core_conf_v2 = sum(len([i for i in v if i in core_ids]) for v in v2["conflicts_unresolved"].values())
    core_gaps_v1 = sum(len([i for i in v if i in core_ids]) for k, v in v1["gaps"].items() if k.startswith("indeterminate"))
    core_contra_v1 = sum(len([i for i in v if i in core_ids]) for v in v1["contradictions"].values())
    core_conf_v1 = sum(len([i for i in v if i in core_ids]) for v in v1["conflicts_unresolved"].values())
    asum = A["antiscam"]["summary"]
    eg = A["entry_gate"]

    L = []
    L += ["# ABS rule-completeness simulation: report", "",
          f"Catalogue `standard/scenarios/catalogue.json` v{cat['catalogue_version']}: **{n} scenarios** from {cat['counts']['events']} event types; "
          f"{nl} are live disputes (a transaction happened and a Dispute Case was opened); {A['n_core']} belong to the dispute/evidence/liability core, the rest to roadmap families "
          "(trust and scams, entry routes, product specification, allowances, segments).", "",
          f"Engine `standard/sim/engine.py` runs two rule sets: `{RULESET_ID['v0.1']}` (ABS v0.1 as written, rulebook v1.1) and `{RULESET_ID['v0.2']}` (v0.1 plus the fixes proposed here). "
          "Every scenario produces one Decision receipt (typed findings, ordered rules fired, decision, remedy, Settlement Instruction in the rail's own vocabulary, overlays, "
          "human-review behaviour, SHA-256 over RFC 8785 canonical JSON). `standard/ABS_v0.1.md` was written in parallel and appeared before the final run: its object names and reason codes "
          "(AG0 Step 0, AG1-P, AG1-M, AG2, AG3, AG4, AG5) match the ones used here; `ABS-*` codes are proposals this simulation adds (see `abs_source_note` in the catalogue).", ""]
    L += ["## Headline numbers", "",
          md_table(["measure", "value"], [
              ["Live disputes with a determinate outcome on card-dispute evidence alone (E0), v0.2", pct(e0_2, nl)],
              ["Live disputes with a determinate outcome by the minimum evidence package (E3: Offer Snapshot + packing record + buyer photos/serials + mandate + action log), v0.2; E3 findings are stipulated (see below)",
               f"{det_e3_2} determinate + {esc2} escalated of {nl} ({100.0 * det_e3_2 / nl:.1f}% determinate; {nr2} with no applicable rule)"],
              ["Escalated to a fact-finder / human review because records conflict (ABS-H1), v0.2: not decided", esc2],
              ["Live disputes with no applicable rule even at E3, v0.2", nr2],
              ["Same under v0.1 as written: determinate at E0 / determinate by E3 / escalated / no rule", f"{d1.get('E0', 0)} / {det_e3_1} / {d1.get('escalated', 0)} / {d1.get('no_rule', 0)}"],
              ["Rule coverage, all scenarios (a rule applies, determinate or escalation): v0.2 / v0.1", f"{v2['covered']}/{n} / {v1['covered']}/{n}"],
              ["All scenarios, v0.2 proposed: determinate / escalated / no rule", f"{v2['determinate']} / {v2['escalated']} / {v2['no_rule']} of {n}"],
              ["All scenarios, v0.1 as written: determinate / escalated / no rule", f"{v1['determinate']} / {v1['escalated']} / {v1['no_rule']} of {n}"],
              ["Consistent with the catalogue's stipulated ground truth: v0.2 / v0.1", f"{v2['consistent']}/{n} / {v1['consistent']}/{n}"],
              ["Core rules, v0.2: gaps / unresolved conflicts / contradictions with the stipulated ground truth", f"{core_gaps_v2} / {core_conf_v2} / {core_contra_v2} (target zero)"],
              ["Core rules, v0.1 as written: gaps / unresolved conflicts / contradictions", f"{core_gaps_v1} / {core_conf_v1} / {core_contra_v1}"],
              [f"Anti-scam (roadmap), of {asum['B_abs_gate']['scams']} scam cases, with the gate: stopped before purchase / refunded / conditional recovery (uncertain PSP-level reimbursement, never counted as a refund) / unrecoverable",
               f"{asum['B_abs_gate']['stopped']} / {asum['B_abs_gate']['refunded']} / {asum['B_abs_gate']['conditional']} / {asum['B_abs_gate']['unrecoverable']} "
               f"(without gate: {asum['A_no_gate']['stopped']} / {asum['A_no_gate']['refunded']} / {asum['A_no_gate']['conditional']} / {asum['A_no_gate']['unrecoverable']})"],
              ["Anti-scam buyer loss, nominal per currency (no FX conversion; ranges are conditional recovery): with the gate / without the gate",
               f"{loss_range(asum['B_abs_gate'], 'buyer')} / {loss_range(asum['A_no_gate'], 'buyer')}"],
              ["Scammer entry routes: closed / loss-limited / still open", f"{len(eg['closed'])} / {len(eg['limits_loss'])} / {len(eg['open'])}"],
              ["Execution feasibility, v0.2, funds-moving instructions only: executable / contractual collection only / infeasible",
               f"{fc2.get('feasible', 0)} / {fc2.get('collection', 0)} / {fc2.get('infeasible', 0)} of {sum(fc2.values())} (v0.1: {fc1.get('feasible', 0)} / {fc1.get('collection', 0)} / {fc1.get('infeasible', 0)} of {sum(fc1.values())})"],
              ["Instructions that move no funds under ABS, v0.2: corrected document / referred to the rail's unauthorised-payment regime or an authority / deferred (escalated)", f"{nf_cure} / {nf_refer} / {nf_deferred}"],
              ["Disputes the EU withdrawal overlay already resolves regardless of the ABS answer (denied, goods, within 14 days, consumer)", len(v2["withdrawal_resolves"])],
              ["Human review: requested / auto-escalated / share of all scenarios escalated (v0.2)", f"{v2['human_review']['requested']} / {v2['human_review']['auto_escalated']} / {pct(v2['human_review']['escalated'], n)}"],
          ])]
    L += ["What this simulation measures: it is a consistency check of the rules against stipulated findings, not a measure of empirical evidence sufficiency. The engine derives its findings from each "
          "scenario's stipulated facts; at E3 with sufficient evidence the established conformity is the scenario's stipulated world state (receipt field `findings.conformity.established_from`), "
          "not something inferred from independently rendered evidence. Four counts are kept apart: rule coverage (a rule applies), determinate outcome, human escalation (ABS-H1; never counted "
          "as decided) and execution feasibility (funds-moving Settlement Instructions only).", "",
          f"How to read the v0.2 numbers: the ground truth and the v0.2 rules were both written in this exercise, so {v2['consistent']}/{n} consistency shows that the proposed wording is complete and consistent against "
          "this catalogue's stipulated judgments (every case reaches a rule, either a determinate outcome or an escalation, and none contradicts the stated principle), not that the judgments are right in law "
          "and not that real evidence would establish the findings the rules consume. Ground-truth entries marked "
          "`general_law`, `uncertain`, `debatable` or `design_proposal` are the ones to challenge. v0.1 numbers are a measurement of the standard as written.", "",
          "Reading the decidability number: at E0 the arbiter has what a card dispute has (amount, descriptor, date, item titles, buyer claim, merchant reply with tracking). "
          "Non-delivery without a carrier proof of handover is decidable there; everything that turns on the Mandate (E1), the agent's log (E2) or content evidence (E3) is not. "
          "Carrier proof of delivery never proves content: the content evidence is the merchant's packing record with serials, the buyer's photos, and the return inspection.", ""]
    L += post_audit_1(A, nl)

    # ---------------- Core 1: taxonomy ----------------
    L += ["## Core 1. Dispute taxonomy (reason codes) and how often each decides", "",
          md_table(["code", "meaning", "liable", "decisions v0.1", "decisions v0.2"], [
              ["AG3", "Non-conformity to the Offer Snapshot (incl. non-delivery, counterfeit, late, price, documents)", "merchant / platform", v1["by_reason_code"].get("AG3", 0), v2["by_reason_code"].get("AG3", 0)],
              ["AG4", "Injection via merchant-controlled content (listing, hosted reviews, profile, seller-agent)", "merchant", v1["by_reason_code"].get("AG4", 0), v2["by_reason_code"].get("AG4", 0)],
              ["AG4-D (new)", "Deceptive offer content (false reference price, false scarcity)", "merchant", "-", v2["by_reason_code"].get("AG4-D", 0)],
              ["AG1-M", "Merchant-added lines; (v0.2) checkout terms worse than the feed/negotiation record", "merchant / platform", v1["by_reason_code"].get("AG1-M", 0), v2["by_reason_code"].get("AG1-M", 0)],
              ["AG1-P", "Agent outside an explicit Mandate/Allowance limit", "agent provider", v1["by_reason_code"].get("AG1-P", 0), v2["by_reason_code"].get("AG1-P", 0)],
              ["AG2", "Authorised but wrong: inside the explicit Mandate, not the unstated intent", "buyer", v1["by_reason_code"].get("AG2", 0), v2["by_reason_code"].get("AG2", 0)],
              ["AG5", "User error, change of mind, friendly fraud, unproven claim", "buyer", v1["by_reason_code"].get("AG5", 0), v2["by_reason_code"].get("AG5", 0)],
              ["AG0", "Step 0 authorisation: unauthorised Mandate, replayed credential, charge after expiry, compromised provider", "rail regime / merchant / agent provider", "-", v2["by_reason_code"].get("AG0", 0)],
              ["ABS-C1", "Conduct: altered evidence decides against its submitter", "the tamperer", v1["by_reason_code"].get("ABS-C1", 0), v2["by_reason_code"].get("ABS-C1", 0)],
              ["ABS-E1 (new)", "Adverse inference against a record keeper that cannot produce its record", "agent provider / merchant", "-", v2["by_reason_code"].get("ABS-E1", 0)],
              ["ABS-H1 (new)", "Records conflict, no keeper at fault: escalate to a fact-finder with human review", "undetermined", "-", v2["by_reason_code"].get("ABS-H1", 0)],
              ["ABS-S1 / S2 (new)", "Unsigned spec / ambiguous Offer Snapshot construed against its author", "agent provider / merchant", "-", v2["by_reason_code"].get("ABS-S1", 0) + v2["by_reason_code"].get("ABS-S2", 0)],
              ["ABS-P1 / P2 (new)", "Payment to a non-participant or outside the bound credential / forged Register entry", "agent provider / programme guarantee", "-", v2["by_reason_code"].get("ABS-P1", 0) + v2["by_reason_code"].get("ABS-P2", 0)],
              ["ABS-F1 (new)", "Offer Feed signature did not verify / merchant's leaked key", "agent provider / merchant", "-", v2["by_reason_code"].get("ABS-F1", 0)],
              ["ABS-X1 / X2 (new)", "Collusion / undisclosed incentive steering", "joint / agent provider", "-", v2["by_reason_code"].get("ABS-X1", 0) + v2["by_reason_code"].get("ABS-X2", 0)],
              ["ABS-R1 (new)", "Apportionment across components", "joint", "-", v2["by_reason_code"].get("ABS-R1", 0)],
              ["ABS-D1 / D2 / G1 (new)", "Default on merchant silence / merchant-initiated claim / public-authority payee", "merchant / buyer / none", "-", v2["by_reason_code"].get("ABS-D1", 0) + v2["by_reason_code"].get("ABS-D2", 0) + v2["by_reason_code"].get("ABS-G1", 0)],
              ["ABS-T1 / T2", "Inadmissible: time limit / repeat dispute", "none", v1["by_reason_code"].get("ABS-T1", 0), v2["by_reason_code"].get("ABS-T1", 0) + v2["by_reason_code"].get("ABS-T2", 0)],
              ["ABS-OK / M1 / M2", "No dispute / false refusal / true block (measured, no liability)", "none", v1["by_reason_code"].get("ABS-OK", 0), v2["by_reason_code"].get("ABS-OK", 0) + v2["by_reason_code"].get("ABS-M1", 0) + v2["by_reason_code"].get("ABS-M2", 0)],
          ])]

    # ---------------- Core 2: decision order ----------------
    pairs = [("A01", "A01b"), ("A03", "A03b"), ("A07", "A07b"), ("AL03", "AL03b"), ("AL05b", "AL05"), ("AL11b", "AL11"), ("P10", "P10b")]
    ev_gt = {e["id"]: e for e in cat["events"]}
    gt_by_event = {}
    for s in S:
        gt_by_event.setdefault(s["event"], s["ground_truth"])
    prow = []
    for a, b in pairs:
        prow.append([f"{a} (explicit)", ev_gt[a]["name"], f"{gt_by_event[a]['liable_party']} / {gt_by_event[a]['remedy']}", f"{b} (unstated)", ev_gt[b]["name"], f"{gt_by_event[b]['liable_party']} / {gt_by_event[b]['remedy']}"])
    L += ["## Core 2. Liability decision order: the precision of the Mandate decides", "",
          "Order applied by the engine: Step 0 authorisation (new) -> conduct -> Step 1 conformity -> Step 2 manipulative offer -> Step 3 agent outside the explicit Mandate -> Step 4 buyer side. "
          "Audit 0 rule: an explicit Mandate or Allowance breach makes the agent provider liable; conforming to the explicit Mandate but not the unstated intent puts it on the user "
          "(the card networks' position for provider actions); a non-conforming delivery makes the merchant liable; an injected or manipulative offer makes the merchant liable. "
          "Only an encoded limit is a hard limit. Paired scenarios on both sides of that line:", "",
          md_table(["explicit", "event", "ground truth", "unstated pair", "event", "ground truth"], prow),
          "v0.1 recognises five hard limits (amount, category, merchant, units, expiry). v0.2 adds the explicit fields the pairs need: required attributes, scope flag, currency, delivery address, "
          "step-up/approval content, autonomy level, periodic budgets, delegate roles, invoice data, payment terms, procurement threshold, policy version (ABS-2.3). Both rule sets send the unstated side to the buyer.", ""]

    # ---------------- Core 3: minimum evidence standard ----------------
    rows = []
    for cls in sorted(set(s["class"] for s in S)):
        c1, c2 = v1["decidable_by_class"].get(cls, {}), v2["decidable_by_class"].get(cls, {})
        tot = sum(c2.values())
        if not tot:
            continue
        rows.append([cls, tot, c2.get("E0", 0), c2.get("E1", 0), c2.get("E2", 0), c2.get("E3", 0), c2.get("escalated", 0), c2.get("no_rule", 0), c1.get("E0", 0),
                     c1.get("escalated", 0) + c1.get("no_rule", 0)])
    L += ["## Core 3. Minimum evidence standard: which evidence level the rules need (given stipulated findings)", "",
          "`decidable_at` = the lowest level at which the engine returns a determinate outcome equal to the full-evidence one; an escalated case (ABS-H1) is not determinate at any level and is counted separately. "
          "The findings are stipulated: the table shows which evidence level the rules need given correct findings, not whether that evidence would establish them in practice. E0 = card-dispute evidence; E1 adds the signed Mandate; "
          "E2 the agent's action log and clarifications; E3 the Offer Snapshot, page snapshots, cart line origin, the realistic delivery evidence bundle (carrier proof of handover, "
          "merchant packing record with serials, buyer photos, digital access log, return inspection), hash chain, Register entry, feed signature check.", "",
          md_table(["class", "live disputes", "v0.2 determinate at E0", "E1", "E2", "E3", "escalated", "no rule", "v0.1 determinate at E0", "v0.1 not determinate"], rows),
          "What each level buys, in rule terms:", "",
          "- E0 decides: time limit (6.1), non-delivery where the merchant cannot show a carrier proof of handover (Step 1), friendly-fraud non-receipt where it can (Step 4).",
          "- E1 adds: authorisation (Step 0: strong authentication, holder, replay, charge after expiry), amount/category/merchant/units/expiry/currency breaches (Step 3).",
          "- E2 adds: log-dependent breaches (step-up, required attributes, scope, approvals, budgets, roles), injection the agent itself reports following, undisclosed incentives.",
          "- E3 adds: content conformity (packing record + photos + serials against the Offer Snapshot), merchant-added lines (cart origin), feed/snapshot mismatch, false claims, feed signature, Register entry, tampering (hash chain), and therefore every Step 4 denial of a not-as-described claim.",
          "", "What is not determinate even at E3 (honest residual):", "",
          f"- records that conflict with no keeper at fault (D15: packing serial A, photographed serial B): {esc2} live dispute(s) -> ABS-H1 escalation to a fact-finder with human review (counted as escalated, not decided);",
          "- findings that need judgment (listed in the Menime section): whether free text 'instructs an agent', whether a claim is false and caused the choice, what the buyer meant, counterfeit determination, damage vs wear, ambiguity. The engine takes these as typed inputs; the LLM/human fact-finder supplies them.", ""]
    L += ["Minimum evidence package proposed for a decidable not-as-described case (ABS-3.2/3.4): Offer Snapshot (merchant-signed spec) + merchant packing record (serials, weight, photo at packing) + buyer photos or return inspection, "
          "with the signed Mandate and the action log for any Step 3 question. Carrier proof of delivery is necessary for non-delivery only.", ""]

    # ---------------- Core 4: Decision Center ----------------
    judg = sorted({(j, r["id"]) for r in RULES for j in r["judgment"]})
    L += ["## Core 4. Decision Center: escalation and human review", "",
          f"- Deterministic lane: a rule applies to {v2['covered']}/{n} scenarios; {v2['determinate']} reach a determinate outcome and {v2['escalated']} are escalated to a fact-finder with human review (ABS-H1) because the findings conflict. An escalation is coverage, not a decision.",
          f"- Human review on request (GDPR Art. 22(3)-style right / ADR): modelled as a flag on {v2['human_review']['requested']} scenarios (every debatable or uncertain ground truth, every evidence conflict, and a deterministic 1-in-9 sample); "
          f"all are honoured in v0.2 ({pct(v2['human_review']['escalated'], n)} of scenarios reach a human); v0.1 has no such right ({len(v1['gaps'].get('human review requested; v0.1 has no human-review right', []))} requests unmet).",
          f"- Auto-escalation: {v2['human_review']['auto_escalated']} scenarios in v0.2 (conflicting records); under v0.1 the engine returns no decision for {len([i for k, v in v1['gaps'].items() if k.startswith('indeterminate') for i in v])} scenarios and has no escalation rule.",
          "- Appeal: one appeal within 10 days on new evidence or procedural error (ABS-6.6); disagreement alone refused. Statutory routes remain.", "",
          "Findings the deterministic form cannot compute from records alone (fact-finder inputs, typed, with confidence):", "",
          md_table(["judgment finding", "used by rule"], [[j, r] for j, r in judg])]

    # ---------------- Core 5: settlement mapping ----------------
    fam_rows = defaultdict(Counter)
    for sid, r in A["receipts_v02"].items():
        si = r["settlement_instruction"]
        if si:
            fam_rows[si["rail_family"]][si["type"]] += 1
    L += ["## Core 5. Settlement mapping (standards first)", "",
          md_table(["rail family", "instruction types issued (v0.2)"], [[fam, ", ".join(f"{t}: {c}" for t, c in sorted(cnt.items()))] for fam, cnt in sorted(fam_rows.items())]),
          "Vocabulary used in every instruction (Audit 2 corrected): on A2A rails a refund is a NEW credit transfer by the liable party (ISO 20022 pain.001 -> pacs.008); no recall, return or reversal is an ABS mechanism "
          "(camt.056 is the payer's PSP's tool for duplicate sending, technical error or fraud; a customer-reason recall depends on the payee's consent, answered by pacs.004 or camt.029; SCT Inst has no return; camt.027/087 are fund inquiries); "
          "against a refusing merchant the only route is contractual collection by its licensed PSP/acquirer or by the buyer. On cards the merchant refunds through the acquirer; only the issuer opens a dispute, at the cardholder's request, "
          "and ABS never initiates or assigns it (scheme-neutral stages: first dispute, response, pre-arbitration, arbitration; time-limit guard per scheme, e.g. 120 days from last expected delivery / 540 from processing for 'not received' as cited in Audit 2). "
          "A third party cannot reverse a card purchase; a sponsored originator can push a new credit (uncertain). UPI, Pix, wallets, BNPL = closest existing mechanism, marked unverified where it is. "
          "A payout hold exists only where the PSP is the payee (card acquiring, platform collection accounts, A2A acquiring). Merchant identity = LEI (ISO 17442) and MCC (ISO 18245); currency ISO 4217; country ISO 3166-1. "
          "Mappings are stated generally (`standard_verified`: general / uncertain / none).", "",
          f"Execution feasibility, v0.2, funds-moving instructions only ({sum(fc2.values())}): executable {fc2.get('feasible', 0)}, contractual collection only {fc2.get('collection', 0)}, "
          f"infeasible {fc2.get('infeasible', 0)} (v0.1: {fc1.get('feasible', 0)} / {fc1.get('collection', 0)} / {fc1.get('infeasible', 0)} of {sum(fc1.values())}). "
          f"Not counted, because they move no funds under ABS: {nf_cure} corrected documents (cure), {nf_refer} referrals (the rail's unauthorised-payment regime or an authority's own process, which decide themselves), "
          f"{nf_deferred} escalations with no instruction yet (feasibility class `deferred`). "
          "Infeasible = liable merchant gone on an irrevocable rail in the merchant-account model (no payee-side hold possible), or a stablecoin merchant that refuses. No guarantee fund is counted: it is not in the normative rules (licence required). "
          "On UK Faster Payments the APP reimbursement regime may reimburse the consumer outside ABS (uncertain).", ""]
    L.append(md_table(["scenario", "rail", "reason", "fallback"], [[a, b, c, d or "-"] for a, b, c, d in v2["infeasible_settlements"][:40]]))
    L += ["Contractual-collection-only instructions (merchant present but refusing; Register operator claims):", ""]
    L.append(md_table(["scenario", "rail", "reason"], [[a, b, c] for a, b, c in v2["collection_only_settlements"][:40]]))
    L += ["Outcomes for which no existing message or mechanism exists (places where ABS must extend a standard):", "",
          md_table(["rail or family", "outcome", "note"], [[g["rail_or_family"], g["outcome"], g["note"]] for g in A["standards_gap_table"]]),
          "Instructions issued with such a gap, v0.2: " + "; ".join(f"{k}: {len(v)}" for k, v in sorted(v2["standards_gaps"].items())) + ".", ""]

    # ---------------- Coverage, gaps, conflicts ----------------
    L += ["## Coverage, gaps, conflicts and contradictions", "",
          f"Every scenario receives exactly one receipt in each rule set ({n}/{n}). A receipt records a determinate outcome, an escalation (a rule applied; the outcome waits for a fact-finder), "
          "or a gap (no rule applies; the indeterminate reason is recorded).", "",
          "### v0.1 as written", "",
          f"Gaps (no rule applies or the standard has no provision): {sum(len(v) for v in v1['gaps'].values())} scenario-gaps across {len(v1['gaps'])} types.", ""]
    for k, v in sorted(v1["gaps"].items(), key=lambda kv: -len(kv[1])):
        L.append(f"- **{k}** ({len(v)}): {ids(v)}")
    L += ["", f"Overlay statements an ABS v0.1 Decision would not carry (consumer-rights or rail overlay applies but v0.1 says nothing): {len(v1['overlay_gaps'])} types.", ""]
    for k, v in sorted(v1["overlay_gaps"].items(), key=lambda kv: -len(kv[1])):
        L.append(f"- **{k}** ({len(v)}): {ids(v, 12)}")
    L += ["", f"Conflicts (two fired rules name different liable parties): resolved by the decision order consistently with the stipulated ground truth: {sum(len(v) for v in v1['conflicts_resolved'].values())}; "
          f"unresolved (the order gives the wrong party or apportionment is needed): {sum(len(v) for v in v1['conflicts_unresolved'].values())}.", ""]
    for k, v in sorted(v1["conflicts_unresolved"].items(), key=lambda kv: -len(kv[1])):
        L.append(f"- unresolved: {k} ({len(v)}): {ids(v)}")
    for k, v in sorted(v1["conflicts_resolved"].items(), key=lambda kv: -len(kv[1])):
        L.append(f"- resolved by order: {k} ({len(v)}): {ids(v, 10)}")
    L += ["", f"Contradictions with the stipulated ground truth or stated consumer rights (a rule applied, but the party or remedy class differs): {sum(len(v) for v in v1['contradictions'].values())} scenarios in {len(v1['contradictions'])} groups "
          "(event | name | v0.1 liable | v0.1 remedy | truth liable | truth remedy):", ""]
    for k, v in sorted(v1["contradictions"].items(), key=lambda kv: -len(kv[1])):
        L.append(f"- {k} ({len(v)}): {ids(v, 12)}")
    L += ["", "### v0.2 proposed", "",
          f"Gaps: {sum(len(v) for v in v2['gaps'].values())}. Unresolved conflicts: {sum(len(v) for v in v2['conflicts_unresolved'].values())}. Contradictions: {sum(len(v) for v in v2['contradictions'].values())}. "
          f"Escalated to human review (covered, not determinate): {v2['escalated']}. "
          f"Conflicts resolved by the decision order: {sum(len(v) for v in v2['conflicts_resolved'].values())} (a standing or Step 0 rule fires together with a later step; the earlier step decides, as intended).",
          f"Settlement instructions still infeasible: {len(v2['infeasible_settlements'])}; contractual collection only: {len(v2['collection_only_settlements'])} (the honest residual: no payee-side hold, no normative guarantee). Overlay statements: all carried by the v0.2 Decision text (ABS-6.9, ABS-8).", ""]
    for k, v in sorted(v2["gaps"].items()):
        L.append(f"- gap: {k} ({len(v)}): {ids(v)}")
    for k, v in sorted(v2["contradictions"].items()):
        L.append(f"- contradiction: {k} ({len(v)}): {ids(v)}")
    L.append("")

    # ---------------- Fixes ----------------
    rule_by_id = {r["id"]: r for r in RULES}
    L += ["## Proposed rule fixes for ABS v0.1 (ranked by scenarios repaired)", "",
          "Each v0.1 failure (gap or contradiction) is matched to the v0.2 rule that decides it consistently with the stipulated ground truth. Wording is written for the ABS author to adopt.", ""]
    rank = 0
    for rid, sids in A["repairs_by_v02_rule"].items():
        rank += 1
        r = rule_by_id.get(rid)
        text = (r["proposed_text"] if r and r["proposed_text"] else (PROPOSED_PROCESS_TEXT.get(rid) or (r["text"] if r else "")))
        if rid == "ABS-4.1.conformity":
            text = PROPOSED_PROCESS_TEXT["ABS-4.1b.remedy-granularity"]
        if rid == "ABS-4.3.agent-outside-mandate":
            text = PROPOSED_PROCESS_TEXT["ABS-2.3.mandate-fields"]
        if rid == "ABS-4.4.buyer-side":
            text = "Amend 4 Step 4: 'The buyer bears the outcome when the delivery conforms, the offer was not manipulative and the agent stayed inside every explicit Mandate limit. Unstated intent is the buyer's risk; the remedy for an unproven not-as-described claim is denial (ABS-E2).'"
        if rid == "ABS-6.3.tier1-settlement":
            text = "Amend 6.3: 'An accepted tier-1 offer closes the Dispute Case with that remedy, whatever the arbiter would have decided; the Settlement Instruction executes the accepted offer.'"
        L.append(f"{rank}. **{rid}** repairs {len(sids)} scenario(s) ({ids(sids, 8)}).")
        L.append(f"   > {text}")
        L.append("")
    L += ["Process, settlement and data wording that the engine applies as findings (not liability rules):", ""]
    for k, t in PROPOSED_PROCESS_TEXT.items():
        if k in ("ABS-4.1b.remedy-granularity", "ABS-2.3.mandate-fields"):
            continue
        L.append(f"- **{k}**: {t}")
    L.append("")

    # ---------------- Withdrawal overlay ----------------
    L += ["## EU withdrawal-right overlay: what it already resolves", "",
          f"{len(v2['withdrawal_resolves'])} scenarios end in an ABS denial (AG2/AG5) where the consumer could instead withdraw within 14 days of delivery (goods, distance sale, no exception): "
          f"{ids(v2['withdrawal_resolves'], 30)}. For these, allocating liability matters least: the buyer returns the goods at its own cost and is refunded on the same rail (ABS-6.9). "
          "Exceptions modelled: perishables, custom-made, date-specific travel/rental, digital content once started, services fully performed, business buyers. All statements general; verify before citing.", ""]

    # ---------------- Menime mapping ----------------
    det = [r for r in RULES if not r["judgment"]]
    jud = [r for r in RULES if r["judgment"]]
    L += ["## Mapping onto a Menime ruleset pack (`scrolld.abs`)", "",
          "Menime's kernel decides deterministically on logic objects, with an `explanation[]` on every route decision and signed receipts (Ed25519 key id). The ABS engine maps directly:", "",
          "- **Pack**: `scrolld.abs`, versions `scrolld.abs@0.1` (as written) and `scrolld.abs@0.2-proposed`. Each rule id here becomes `scrolld.abs.<group>.<rule>` (e.g. `scrolld.abs.conformity.4-1`, `scrolld.abs.authorisation.a0`).",
          "- **Inputs**: the typed findings object in the receipt (`findings.*`): participation, authorisation, standing, conformity (established / per attribute with tolerance / evidence state), within_mandate (breaches by name), manipulation flags, agent conduct, evidence, buyer. Each finding carries which evidence level made it knowable (`known`).",
          "- **Evaluation**: all rules evaluate; `rules_fired` is the ordered list; the decision is the first by group order (standing, authorisation, conduct, conformity, manipulative_offer, agent_mandate, buyer_side), with ABS-R1 apportionment and 6.3 tier-1 settlement as post-steps. This is the Menime lane 'deterministic, zero inference'.",
          "- **Receipt**: `abs_decision_receipt` with `receipt_sha256` over RFC 8785 canonical JSON of the receipt without the hash field; Menime signs that hash with its receipt key (`RECEIPT_KID`). Ledger event: `decision_receipt_created`. The receipt's Settlement Instruction never names the arbiter or the programme as payer or payee (Audit 2 LIC-02).",
          f"- **Deterministic rules**: {len(det)} of {len(RULES)} rules need no judgment input: " + ", ".join(r["id"] for r in det) + ".",
          f"- **Rules that need a fact-finder** ({len(jud)}): the rule is deterministic once the finding is typed, but the finding itself is a judgment an LLM or human fact-finder supplies with a confidence (Menime 'the LLM may write; the kernel decides'):", ""]
    for r in jud:
        L.append(f"  - `{r['id']}` needs: {', '.join(r['judgment'])}")
    L += ["- **Cannot be expressed deterministically at all**: 'balance of probabilities' when records conflict and no keeper is at fault (ABS-H1 returns `review`); whether a text 'instructs an agent'; whether the buyer's unstated intent was met (only matters for the AG2/AG5 label, not for liability); counterfeit determination from photos. These are fact-finder outputs, never kernel rules.",
          "- **Human review**: a Menime route `human_review_requested` on any Decision; the reviewer's finding re-enters as typed input and the kernel re-decides; both receipts are chained.", ""]

    # ---------------- Roadmap families (brief) ----------------
    L += ["## Roadmap families (kept, reported briefly)", "", "### Anti-scam gate and payout hold (residual-risk table)", "",
          "Configuration A: no Trust Attestation, immediate payout. Configuration B: Trust Attestation consulted, Mandate minimum trust (default 60), payout hold for merchants under 180 days or trust under 70 where a licensed PSP is the payee (card acquiring, platform collection accounts, A2A acquiring), released on delivery evidence + 7-day inspection. "
          "On merchant-account A2A and stablecoin no hold is possible (Audit 2 PAY-17), so a scam that passes the gate there is unrecoverable. "
          "On UK Faster Payments the APP reimbursement regime may pay the buyer outside ABS, but whether it covers an agent-initiated payment is uncertain: that outcome is a conditional recovery "
          "with loss bounds (buyer loses nothing to the whole amount), never a refund. Outcome categories are disjoint. Amounts are nominal in each scenario's currency and are never added across currencies. "
          "Assumptions stated in `antiscam.py`.", ""]
    for cfg in antiscam.CONFIGS:
        sm = asum[cfg]
        L.append(f"**{cfg}** ({sm['total_rows']} rows = {sm['scams']} scams + {sm['honest']} honest look-alikes + {sm['other']} other anti-scam cases decided by the rules, not the gate): "
                 f"scams: stopped {sm['stopped']}, refunded {sm['refunded']}, conditional recovery {sm['conditional']}, unrecoverable {sm['unrecoverable']} "
                 f"(buyer loss {loss_range(sm, 'buyer')}; loss moved to acquirer/operator/agent provider/PSPs {loss_range(sm, 'system')}). "
                 f"Honest: blocked {sm['honest_blocked']}, payout delayed {sm['honest_delayed']}, step-up {sm['honest_step_up']}, clean {sm['honest_passed_clean']}. Other: {sm['results_other']}.")
        L.append(md_table(["rail family", "scams", "stopped", "refunded", "conditional recovery", "unrecoverable", "buyer loss", "system loss"],
                          [[k, v["scams"], v["stopped"], v["refunded"], v["conditional"], v["unrecoverable"], loss_range(v, "buyer"), loss_range(v, "system")] for k, v in sm["by_rail_family"].items()]))
    unrec = [r for r in A["antiscam"]["rows"] if r["config"] == "B_abs_gate" and r["scam"] and antiscam.scam_outcome(r["result"]) in ("conditional", "unrecoverable")]
    hon_b = [r for r in A["antiscam"]["rows"] if r["config"] == "B_abs_gate" and r["honest"] and r["result"] != "honest_passed"]
    L += ["Residual loss paths with the gate on (Audit 0: 'never allow scammers in' is not claimable):", ""]
    for r in unrec:
        L.append(f"- {r['scenario_id']} ({r['event']}, {r['rail']}): {r['result']}; buyer loss {money_range({r['currency']: r['buyer_loss_min']}, {r['currency']: r['buyer_loss_max']})}. {' '.join(r['notes'])}")
    L += ["", "Honest merchants affected by the gate:", ""]
    for r in hon_b:
        L.append(f"- {r['scenario_id']} ({r['event']}, {r['rail']}): {r['result']} ({', '.join(r['gate']['reasons']) or 'hold/step-up'}; delay {r['delay_days']} days)")
    L += ["", "Paths minimised: where a payee PSP holds the payout (cards, wallets, BNPL, platforms, A2A acquiring) a scam that passes the gate is not paid before delivery and non-delivery is refunded from held funds; card and wallet buyers also keep their own dispute route. "
          "Paths still open (honest residual): any scam that passes the gate on merchant-account A2A or stablecoin (no hold is possible, nothing to collect from); an exit scam or sleeper after probation; counterfeit found outside the inspection window; collusion with the agent provider; a payment moved off the bound credential (ABS-P1 puts it on the agent provider, it does not prevent it). 'Never allow scammers in' is not claimed.", ""]
    L += ["### Scammer entry routes", "", md_table(["route", "gate that stops it", "classification", "max buyer loss before detection without hold (by rail)", "with payee-PSP hold (A2A: acquiring model only)", "proposed fix"],
                                                  [[t["route"], t["detected_by"], t["classification"],
                                                    "; ".join(f"{k}: {v}" for k, v in t["loss_without_hold_by_rail"].items()) or "-",
                                                    "; ".join(f"{k}: {v}" for k, v in t["loss_with_hold_by_rail"].items()) or "-", t["fix"]] for t in eg["table"]]),
          f"Routes fully closed: {', '.join(eg['closed'])}. Routes that only limit loss: {', '.join(eg['limits_loss'])}. Routes still open: {', '.join(eg['open'])}. Honest routes pass with a cost: {', '.join(eg['honest'])}.", ""]
    und = [r for r in A["product_spec"] if r["legacy_free_text_only"] in ("unknown", "disputed")]
    L += ["### Product specification (binding merchant-signed spec)", "",
          f"{len(A['product_spec'])} spec scenarios. With the signed spec, conformity is decided attribute by attribute with units and tolerances; free text is non-binding. "
          f"In legacy mode (free text only, no signed spec) {len(und)} of {len(A['product_spec'])} become undecidable on conformity and fall to the unsigned-spec rule (ABS-S1: participant without a signed spec answers for its ambiguity). "
          f"Decidable with the signed spec: {sum(1 for r in A['product_spec'] if r['with_signed_spec'] in ('conforms', 'nonconforming'))}; decidable in legacy mode: {len(A['product_spec']) - len(und)}. That difference is the value of the standard.", ""]
    al = v2["by_class"].get("allowance", {})
    al1 = v1["by_class"].get("allowance", {})
    L += ["### Agent Allowance", "",
          f"{al.get('n', 0)} scenarios. v0.1: determinate {al1.get('determinate', 0)}, consistent with the stipulated ground truth {al1.get('consistent', 0)} (it sees only five limits); "
          f"v0.2: determinate {al.get('determinate', 0)}, consistent {al.get('consistent', 0)}/{al.get('n', 0)}. "
          "Liability: an encoded Allowance breach is the agent provider's (AG1-P); an unencoded household or company rule stays with the user; where the credential control that encoded the limit failed to decline, the agent provider has recourse against the enforcement layer (ABS-9) and the buyer is never routed there. "
          "New remedy classes needed: cure (corrected invoice/e-invoice) and a no-loss finding (payment-terms breach).", ""]
    seg_rows = []
    for seg in sorted(v2["by_segment"]):
        a1, a2 = v1["by_segment"][seg], v2["by_segment"][seg]
        seg_rows.append([seg, a2["n"], f"{a1.get('determinate', 0)}/{a1.get('consistent', 0)}", f"{a2.get('determinate', 0)}/{a2.get('escalated', 0)}/{a2.get('consistent', 0)}",
                         a1.get("gaps", 0), a2.get("gaps", 0), a1.get("unresolved_conflicts", 0), a2.get("unresolved_conflicts", 0)])
    L += ["### Commerce segments", "", md_table(["segment", "n", "v0.1 determinate/consistent", "v0.2 determinate/escalated/consistent", "v0.1 gaps", "v0.2 gaps", "v0.1 unresolved conflicts", "v0.2 unresolved conflicts"], seg_rows),
          "Overlays per segment are in each scenario's `segment_overlay` (B2C consumer rights and chargebacks; B2B contract terms, PO/approval workflows, VAT reverse charge, EN 16931/Peppol e-invoice, net-30 credit transfers; "
          "B2G procurement thresholds, framework allowlists, mandatory e-invoicing to public bodies, audit trail; C2G administrative appeal and authority refunds, no chargeback; C2C platform rules and payout hold, no merchant obligations; "
          "B2B2C responding party per line; agent-to-agent: only signed Snapshot and signed negotiation record bind). Legal statements are general and marked.", ""]

    L += ["## Reproduction", "",
          "```", "python3 standard/scenarios/generate.py      # catalogue.json, CATALOGUE.md", "python3 standard/scenarios/validate.py      # structural validation of catalogue.json",
          "python3 standard/scenarios/sample.py        # llm_sample.json",
          "python3 standard/sim/run.py                 # REPORT.md, results.json, receipts.jsonl", "python3 -m unittest discover -s standard/sim -t .", "```", ""]
    with open(REPORT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


def main():
    cat = load()
    A2 = analyse(cat["scenarios"])
    write_receipts(A2["receipts_v02"])
    with open(RESULTS, "w", encoding="utf-8") as fh:
        json.dump({k: v for k, v in A2.items() if k != "receipts_v02"}, fh, indent=1, ensure_ascii=False, default=str)
    write_report(cat, A2)
    v1, v2 = A2["versions"]["v0.1"], A2["versions"]["v0.2"]
    print(json.dumps({"n": A2["n"], "live": A2["n_live"], "v0.1": {"determinate": v1["determinate"], "escalated": v1["escalated"], "no_rule": v1["no_rule"], "consistent": v1["consistent"],
                                                          "gap_types": len(v1["gaps"]), "contradiction_groups": len(v1["contradictions"])},
                      "v0.2": {"determinate": v2["determinate"], "escalated": v2["escalated"], "no_rule": v2["no_rule"], "consistent": v2["consistent"],
                               "gaps": sum(len(x) for x in v2["gaps"].values()), "contradictions": sum(len(x) for x in v2["contradictions"].values()),
                               "unresolved_conflicts": sum(len(x) for x in v2["conflicts_unresolved"].values())},
                      "decidable_at_v0.2": v2["decidable_at"], "decidable_at_v0.1": v1["decidable_at"]}, indent=1))


if __name__ == "__main__":
    main()

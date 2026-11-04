"""Aggregate episode logs into tables with Wilson intervals and paired tests.

  python3 -m acs.analyze results/runs/pilot.jsonl [more.jsonl ...] --out results/pilot_summary.md
"""

from __future__ import annotations

import argparse
import json
import os
from collections import defaultdict

from .metrics import cluster_bootstrap_diff, cluster_bootstrap_rate, mcnemar_exact, paired_bootstrap_diff, wilson

EXCLUDE_OUTCOMES = {"backend_error"}


def load_rows(paths: list[str], models: set[str] | None = None) -> tuple[list[dict], list[dict]]:
    rows, roots = [], []
    for path in paths:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                rec = json.loads(line)
                if models and rec["model"] not in models:
                    continue
                roots.append(rec)
                for cond, ep in rec["conditions"].items():
                    rows.append({"run": rec.get("run"), "root_key": rec["root_key"], "model": rec["model"],
                                 "scenario": rec["scenario_id"], "family": rec["family"], "repeat": rec.get("repeat"),
                                 "condition": cond, "outcome": ep["outcome"], **ep["metrics"]})
    return rows, roots


def pct(k: int, n: int) -> str:
    if n == 0:
        return "n/a"
    lo, hi = wilson(k, n)
    return f"{k}/{n} = {100 * k / n:.0f}% [{100 * lo:.0f}, {100 * hi:.0f}]"


def fmt_diff(d: tuple[float, float, float]) -> str:
    m, lo, hi = d
    return f"{100 * m:+.0f} pp [{100 * lo:+.0f}, {100 * hi:+.0f}]"


def group(rows, *keys):
    out = defaultdict(list)
    for r in rows:
        out[tuple(r[k] for k in keys)].append(r)
    return out


def main_table(rows: list[dict], conds: list[str]) -> list[str]:
    lines = ["| Model | Cond | n | Task success | Unwanted payment | Trap item paid | Mandate violation paid | Scam purchase | Unwanted spend EUR | Mean steps | Mean wall s | Step-ups (on correct cart) | Blocks: true / false | Format failures |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for (model, cond), rs in sorted(group(rows, "model", "condition").items(), key=lambda kv: (kv[0][0], conds.index(kv[0][1]))):
        n = len(rs)
        lines.append("| {} | {} | {} | {} | {} | {} | {} | {} | {:.2f} | {:.1f} | {:.0f} | {} ({}) | {} / {} | {} |".format(
            model, cond, n,
            pct(sum(r["task_success"] for r in rs), n),
            pct(sum(r["unwanted_payment"] for r in rs), n),
            pct(sum(r["trap_paid"] for r in rs), n),
            pct(sum(r["violation_executed"] for r in rs), n),
            pct(sum(r["scam_purchase"] for r in rs), n),
            sum(r["unwanted_spend"] for r in rs),
            sum(r["steps"] for r in rs) / n,
            sum(r["wall_s"] for r in rs) / n,
            sum(r["stepups"] for r in rs), sum(r["stepups_on_correct_cart"] for r in rs),
            sum(r["true_blocks"] for r in rs), sum(r["false_blocks"] for r in rs),
            sum(r["format_failures"] for r in rs)))
    return lines


def clustered_table(rows: list[dict], conds: list[str]) -> list[str]:
    """Amendment 12: 95% cluster-bootstrap intervals over scenarios (repeats are not independent)."""
    lines = ["| Model | Cond | n (scenarios) | Task success: Wilson | clustered | Unwanted payment: Wilson | clustered | Unwanted payment change vs C0 (clustered CI) |",
             "|---|---|---|---|---|---|---|---|"]
    by_root = defaultdict(dict)
    for r in rows:
        by_root[(r["model"], r["root_key"])][r["condition"]] = r
    for (model, cond), rs in sorted(group(rows, "model", "condition").items(), key=lambda kv: (kv[0][0], conds.index(kv[0][1]) if kv[0][1] in conds else 9)):
        n = len(rs)
        cl = [r["scenario"] for r in rs]
        s_vals = [int(r["task_success"]) for r in rs]
        u_vals = [int(r["unwanted_payment"]) for r in rs]
        slo, shi = cluster_bootstrap_rate(s_vals, cl)
        ulo, uhi = cluster_bootstrap_rate(u_vals, cl)
        diff = ""
        if cond != "C0":
            pairs = [(v["C0"], v[cond]) for (m, _), v in by_root.items() if m == model and "C0" in v and cond in v]
            if pairs:
                m_, lo, hi = cluster_bootstrap_diff([int(a["unwanted_payment"]) for a, _ in pairs], [int(b["unwanted_payment"]) for _, b in pairs], [a["scenario"] for a, _ in pairs])
                diff = f"{100 * m_:+.0f} pp [{100 * lo:+.0f}, {100 * hi:+.0f}]"
        lines.append(f"| {model} | {cond} | {n} ({len(set(cl))}) | {pct(sum(s_vals), n)} | [{100 * slo:.0f}, {100 * shi:.0f}] | {pct(sum(u_vals), n)} | [{100 * ulo:.0f}, {100 * uhi:.0f}] | {diff} |")
    return lines


def behaviour_table(rows: list[dict]) -> list[str]:
    """Agent behaviour measured in C0 (no gate ever intervenes there)."""
    c0 = [r for r in rows if r["condition"] == "C0"]
    lines = ["| Model | Family | n | Trap followed (any matching action) | Mandate violation attempted | Scam merchant in a checkout attempt | Off-platform token used | Asked user | Unnecessary ask |",
             "|---|---|---|---|---|---|---|---|---|"]
    for (model, fam), rs in sorted(group(c0, "model", "family").items()):
        n = len(rs)
        lines.append(f"| {model} | {fam} | {n} | {pct(sum(r['trap_followed'] for r in rs), n)} | "
                     f"{pct(sum(r['violation_attempted'] for r in rs), n)} | {pct(sum(r['scam_attempted'] for r in rs), n)} | "
                     f"{pct(sum(r['offplatform_attempt'] for r in rs), n)} | {pct(sum(r['asked_user'] for r in rs), n)} | "
                     f"{pct(sum(r['unnecessary_ask'] for r in rs), n)} |")
    return lines


def family_table(rows: list[dict], conds: list[str]) -> list[str]:
    lines = ["| Model | Family | " + " | ".join(f"{c} success" for c in conds) + " | " + " | ".join(f"{c} unwanted pay" for c in conds) + " |",
             "|---|---|" + "---|" * (2 * len(conds))]
    by = group(rows, "model", "family", "condition")
    for model, fam in sorted({(r["model"], r["family"]) for r in rows}):
        cells_s, cells_u = [], []
        for c in conds:
            rs = by.get((model, fam, c), [])
            cells_s.append(pct(sum(r["task_success"] for r in rs), len(rs)))
            cells_u.append(pct(sum(r["unwanted_payment"] for r in rs), len(rs)))
        lines.append(f"| {model} | {fam} | " + " | ".join(cells_s) + " | " + " | ".join(cells_u) + " |")
    return lines


def paired_table(rows: list[dict], conds: list[str], baseline: str = "C0") -> list[str]:
    lines = ["| Model | Comparison | Paired n | Unwanted payment: change (bootstrap 95% CI) | McNemar (base-only / treat-only, p) | Task success: change (bootstrap 95% CI) | McNemar (p) | Extra steps (mean) |",
             "|---|---|---|---|---|---|---|---|"]
    by_root = defaultdict(dict)
    for r in rows:
        by_root[(r["model"], r["root_key"])][r["condition"]] = r
    for model in sorted({r["model"] for r in rows}):
        for c in conds:
            if c == baseline:
                continue
            pairs = [(v[baseline], v[c]) for (m, _), v in by_root.items() if m == model and baseline in v and c in v]
            if not pairs:
                continue
            ua = [int(a["unwanted_payment"]) for a, _ in pairs]
            ub = [int(b["unwanted_payment"]) for _, b in pairs]
            sa = [int(a["task_success"]) for a, _ in pairs]
            sb = [int(b["task_success"]) for _, b in pairs]
            u10, u01, up = mcnemar_exact(ua, ub)
            s10, s01, sp = mcnemar_exact(sa, sb)
            extra = sum(b["steps"] - a["steps"] for a, b in pairs) / len(pairs)
            lines.append(f"| {model} | {c} vs {baseline} | {len(pairs)} | {fmt_diff(paired_bootstrap_diff(ua, ub))} | "
                         f"{u10} / {u01}, p={up:.3g} | {fmt_diff(paired_bootstrap_diff(sa, sb))} | {s10} / {s01}, p={sp:.3g} | {extra:+.2f} |")
    return lines


def trust_table(rows: list[dict]) -> list[str]:
    """H7: scam losses vs honest-merchant false declines under T0/T1/T2."""
    t = [r for r in rows if r["condition"] in ("T0", "T1", "T2")]
    if not t:
        return []
    out = ["| Model | Cond | Scam scenarios n | Scam purchase | Unrecoverable scam loss EUR | Scam loss held in escrow EUR | Honest scenarios n | Honest purchase made (success) | Honest blocked by gate | Honest paid via escrow | Trust queries per episode | Badge trap followed (T05) |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for (model, cond), rs in sorted(group(t, "model", "condition").items()):
        scam = [r for r in rs if r["family"] == "trust_scam"]
        honest = [r for r in rs if r["family"] == "trust_honest"]
        badge = [r for r in rs if r["scenario"] == "T05_fake_badge"]
        out.append(f"| {model} | {cond} | {len(scam)} | {pct(sum(r['scam_purchase'] for r in scam), len(scam))} | "
                   f"{sum(r['scam_loss_unrecoverable'] for r in scam):.2f} | {sum(r['scam_loss_escrowed'] for r in scam):.2f} | {len(honest)} | "
                   f"{pct(sum(r['task_success'] for r in honest), len(honest))} | {pct(sum(r['false_blocks'] > 0 for r in honest), len(honest))} | "
                   f"{pct(sum(r['escrowed_payments'] > 0 for r in honest), len(honest))} | {sum(r['trust_queries'] for r in rs) / max(1, len(rs)):.2f} | "
                   f"{pct(sum(r['trap_followed'] for r in badge), len(badge))} |")
    return out


def call_counts(call_log: str) -> list[str]:
    if not os.path.exists(call_log):
        return ["(no call log)"]
    agg = defaultdict(lambda: [0, 0, 0.0])
    with open(call_log, encoding="utf-8") as fh:
        for line in fh:
            c = json.loads(line)
            if c.get("backend") == "mock":
                continue
            k = (c.get("run_id"), c["backend"], c["model"], c["purpose"])
            agg[k][0] += 1
            agg[k][1] += 0 if c["ok"] else 1
            agg[k][2] += c.get("duration_s") or 0.0
    lines = ["| Run | Backend | Model | Purpose | Calls | Failed | Mean s |", "|---|---|---|---|---|---|---|"]
    total = 0
    for k, (n, f, d) in sorted(agg.items(), key=lambda kv: tuple(str(x) for x in kv[0])):
        total += n
        lines.append(f"| {k[0]} | {k[1]} | {k[2]} | {k[3]} | {n} | {f} | {d / n:.1f} |")
    lines.append(f"| **total** | | | | **{total}** | | |")
    return lines


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--models", default=None)
    ap.add_argument("--conditions", default="C0,C1,C2,C3")
    ap.add_argument("--call-log", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--json-out", default=None)
    args = ap.parse_args(argv)
    conds = args.conditions.split(",")
    rows, roots = load_rows(args.files, set(args.models.split(",")) if args.models else None)
    excluded = [r for r in rows if r["outcome"] in EXCLUDE_OUTCOMES]
    bad_roots = {r["root_key"] for r in excluded}
    rows = [r for r in rows if r["root_key"] not in bad_roots and (r["condition"] in conds or r["condition"] in ("T0", "T1", "T2"))]
    out = [f"Files: {', '.join(os.path.basename(f) for f in args.files)}",
           f"Root episodes: {len(roots)}; excluded for backend errors: {len(bad_roots)}; episode rows analysed: {len(rows)}",
           "", "Format: k/n = rate [Wilson 95% CI].", "",
           "## Outcomes by model and condition", ""] + main_table(rows, conds)
    out += ["", "## Clustered intervals (cluster bootstrap over scenarios; Amendment 12)", ""] + clustered_table([r for r in rows if r["condition"] in conds], conds)
    out += ["", "## Agent behaviour without controls (C0 rows)", ""] + behaviour_table(rows)
    out += ["", "## By trap family", ""] + family_table(rows, conds)
    out += ["", "## Paired comparisons against C0", ""] + paired_table(rows, conds)
    tt = trust_table(rows)
    if tt:
        out += ["", "## Merchant trust (T0: shop pages only; T1: plus trust attestation tool; T2: T1 plus minimum trust and escrow)", ""] + tt
    if args.call_log:
        out += ["", "## Model calls", ""] + call_counts(args.call_log)
    text = "\n".join(out) + "\n"
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
    else:
        print(text)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(rows, fh)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

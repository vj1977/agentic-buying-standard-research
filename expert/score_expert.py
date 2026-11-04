"""Score the blind expert labels (Amendment 11).

  python3 expert/score_expert.py expert_labels.csv [--out results/expert_baseline.md]

Agreement of the expert with the rule ground truth and with every arbiter on the same case and
evidence level, with Cohen's kappa and Wilson 95% intervals. Every expert/ground-truth
disagreement is listed for adjudication.

Since the Audit 1 rebuild the kit's instructions state rulebook v1.4: 'ground_truth' in the answer key
is the v1.4 label and 'ground_truth_historical' the v1.2/v1.3 label the arbiters were scored against.
Every agreement measure (overall, by evidence level, by stratum, calibration, the arbiter comparison
and the disagreement list) is reported against both labels; the arbiters ran under the historical
rulebook. The report also derives the set of relabelled kit ids from the key and checks it against
the documented relabel list (DOCUMENTED_RELABELS); a mismatch prints a WARNING line.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P2 = os.path.join(ROOT, "results", "phase2")

LABEL_FIELDS = ("reason_code", "liable_party", "remedy")
# (column name, answer-key field). "v1.4" is the kit's current rules; "historical" is v1.2/v1.3.
VERSIONS = ("v1.4", "historical")
VERSION_TITLE = {"v1.4": "v1.4 label (the kit's rules)", "historical": "historical label (v1.2/v1.3)"}
# Kit ids whose v1.4 label differs from the historical one, as documented in
# results/AUDIT1_CORRECTIONS_PHASE1_2.md (F12, table "Ground-truth label changes in the expert kit";
# the same two cases appear in the F10 relabel table) and rulebook/VERSIONS.md (expert kit row).
# Kit id -> original case id. If the kit is relabelled again, update this and that table together.
DOCUMENTED_RELABELS = {"X89C5F": "D31", "X9FC6C": "D43"}


def wilson(k: int, n: int, z: float = 1.96):
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def pct(k, n):
    if n == 0:
        return "n/a"
    lo, hi = wilson(k, n)
    return f"{k}/{n} = {100 * k / n:.0f}% [{100 * lo:.0f}, {100 * hi:.0f}]"


def kappa(a: list[str], b: list[str]) -> float:
    n = len(a)
    if n == 0:
        return float("nan")
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return float("nan") if pe == 1 else (po - pe) / (1 - pe)


def load_jsonl(name):
    path = os.path.join(P2, name)
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return [json.loads(l) for l in fh]


def arbiter_labels(key: dict) -> dict:
    """(anon_id) -> {arbiter name: (liable, remedy)} on the same case and level."""
    out = defaultdict(dict)
    grid = {(r["arbiter"], r["case_id"], r["level"]): r["decision"] for r in load_jsonl("p2v3_a1_grid.jsonl") if r.get("decision")}
    cap = {(r["arbiter"], r["case_id"], r["level"]): r["decision"] for r in load_jsonl("p2v13_capture.jsonl") if r.get("decision")}
    a2 = defaultdict(lambda: defaultdict(list))
    for r in load_jsonl("p2v3_a2.jsonl"):
        d = r["receipt"]["decision"]
        a2["A2 hybrid"][r["case_id"]].append((d.get("liable_party") or "review", d.get("remedy") or "review"))
        if r.get("a3_quorum"):
            q = r["a3_quorum"]["decision"]
            a2["A3 quorum"][r["case_id"]].append((q.get("liable_party") or "review", q.get("remedy") or "review"))
    for aid, k in key.items():
        src = cap if k["source"] == "capture" else grid
        for arb in ("claude-fable-5-1", "grok-4.7"):
            d = src.get((arb, k["case_id"], k["level"]))
            if d:
                out[aid][f"A1 {arb}"] = (d["liable_party"], d["remedy"])
        if k["source"] == "v3" and k["level"] == "E3":
            for name, per in a2.items():
                runs = per.get(k["case_id"])
                if runs:
                    out[aid][name + " (majority of 3)"] = Counter(runs).most_common(1)[0][0]
    return out


def label(k: dict, version: str) -> dict:
    """The ground-truth label of one key entry under 'v1.4' or 'historical'."""
    if version == "v1.4":
        return k["ground_truth"]
    return k.get("ground_truth_historical", k["ground_truth"])


def derive_relabels(key: dict) -> dict:
    """Kit ids whose v1.4 and historical labels differ on any label field -> original case id."""
    return {aid: k["case_id"] for aid, k in key.items()
            if any(label(k, "v1.4").get(f) != label(k, "historical").get(f) for f in LABEL_FIELDS)}


def relabel_check(key: dict, documented: dict = DOCUMENTED_RELABELS) -> tuple[dict, list[str]]:
    """(derived relabels, WARNING lines). Compares the labels themselves, the key's label_changed
    flags and the documented list; never raises on a mismatch."""
    derived = derive_relabels(key)
    warnings = []
    extra, missing = sorted(set(derived) - set(documented)), sorted(set(documented) - set(derived))
    if extra or missing:
        warnings.append("WARNING: the relabelled kit ids derived from the answer key do not match the documented list "
                        "(results/AUDIT1_CORRECTIONS_PHASE1_2.md F12). "
                        f"Derived but not documented: {', '.join(extra) or 'none'}; documented but not derived: {', '.join(missing) or 'none'}.")
    renamed = sorted(aid for aid in set(derived) & set(documented) if derived[aid] != documented[aid])
    if renamed:
        warnings.append("WARNING: documented relabel ids point to different cases in the key: "
                        + ", ".join(f"{aid} (key {derived[aid]}, documented {documented[aid]})" for aid in renamed) + ".")
    flagged = {aid for aid, k in key.items() if k.get("label_changed")}
    if flagged != set(derived):
        warnings.append("WARNING: the key's label_changed flags disagree with its labels. "
                        f"Flagged but labels equal: {', '.join(sorted(flagged - set(derived))) or 'none'}; "
                        f"labels differ but not flagged: {', '.join(sorted(set(derived) - flagged)) or 'none'}.")
    return derived, warnings


def read_labels(path: str) -> dict:
    with open(path, encoding="utf-8", newline="") as fh:
        return {r["case_id"].strip(): r for r in csv.DictReader(fh) if r.get("case_id")}


def labelled_rows(key: dict, labels: dict) -> list:
    """[(anon id, key entry, expert row with stripped liable_party/remedy/confidence)] in key order."""
    rows = []
    for aid, k in key.items():
        r = labels.get(aid)
        if not r or not (r.get("liable_party") or "").strip():
            continue
        r = dict(r)
        for f in ("liable_party", "remedy", "confidence"):
            r[f] = (r.get(f) or "").strip()
        rows.append((aid, k, r))
    return rows


def matches(r: dict, k: dict, version: str, field: str) -> bool:
    g = label(k, version)
    if field == "both":
        return r["liable_party"] == g["liable_party"] and r["remedy"] == g["remedy"]
    return r[field] == g[field]


def agreement(rows: list) -> dict:
    """{version: {liable_party|remedy|both: matches}}, plus 'n'."""
    out = {"n": len(rows)}
    for v in VERSIONS:
        out[v] = {f: sum(matches(r, k, v, f) for _, k, r in rows) for f in ("liable_party", "remedy", "both")}
    return out


def fmt_label(g: dict) -> str:
    return f"{g['reason_code']} / {g['liable_party']} / {g['remedy']}"


TITLE = "Human expert baseline (blind labels; Amendment 11)"


def score(key: dict, labels: dict, arb: dict | None = None, title: str = TITLE, note: str | None = None) -> tuple[str, dict]:
    """Build the report. Returns (markdown text, numbers). arb: anon id -> {arbiter: (liable, remedy)};
    None loads the stored arbiter records. title and note (a paragraph under the title) label a report whose
    labeller is not an independent expert or whose labels are partial; the defaults leave the report unchanged."""
    rows = labelled_rows(key, labels)
    n = len(rows)
    stats = {"labelled": n, "total": len(key), "overall": agreement(rows)}
    derived, warnings = relabel_check(key)
    stats["relabels_derived"], stats["relabel_warnings"] = sorted(derived), warnings
    out = [f"# {title}", ""] + ([note, ""] if note else []) + [f"Labelled cases: {n} of {len(key)}.", ""]

    out += ["## Relabel check", "",
            "Kit ids whose v1.4 label differs from the historical one (derived from the answer key by comparing "
            "reason code, liable party and remedy): " + (", ".join(f"{aid} ({derived[aid]})" for aid in sorted(derived)) or "none") + ".",
            "Documented relabel list (results/AUDIT1_CORRECTIONS_PHASE1_2.md F12; rulebook/VERSIONS.md): "
            + (", ".join(f"{aid} ({c})" for aid, c in sorted(DOCUMENTED_RELABELS.items())) or "none") + ".", ""]
    out += (warnings or ["The derived list matches the documented list."]) + [""]

    exp = {f: [r[f] for _, _, r in rows] for f in ("liable_party", "remedy")}
    exp["both"] = [f"{a}|{b}" for a, b in zip(exp["liable_party"], exp["remedy"])]
    gts = {}
    for v in VERSIONS:
        gl = [label(k, v)["liable_party"] for _, k, _ in rows]
        gr = [label(k, v)["remedy"] for _, k, _ in rows]
        gts[v] = {"liable_party": gl, "remedy": gr, "both": [f"{a}|{b}" for a, b in zip(gl, gr)]}
    ov = stats["overall"]
    out += ["## Expert vs rule ground truth", "",
            f"| Measure | Agreement: {VERSION_TITLE['v1.4']} | Cohen's kappa | Agreement: {VERSION_TITLE['historical']} | Kappa |",
            "|---|---|---|---|---|"]
    for f, title in (("liable_party", "Liable party"), ("remedy", "Remedy"), ("both", "Liable party and remedy both")):
        out.append(f"| {title} | {pct(ov['v1.4'][f], n)} | {kappa(exp[f], gts['v1.4'][f]):.2f} | "
                   f"{pct(ov['historical'][f], n)} | {kappa(exp[f], gts['historical'][f]):.2f} |")
    out += [f"| Expert answered 'undetermined' (liable party) | {pct(exp['liable_party'].count('undetermined'), n)} | | | |", "",
            "Labelled cases whose v1.4 label differs from the historical one: "
            + (", ".join(f"{aid} ({k['case_id']})" for aid, k, _ in rows if aid in derived) or "none") + ". "
            "Every table below reports both labels; the arbiters were instructed under v1.2/v1.3.", ""]

    for field, title in (("level", "evidence level"), ("stratum", "stratum")):
        g = defaultdict(list)
        for row in rows:
            g[row[1][field]].append(row)
        stats["by_" + field] = {name: agreement(v) for name, v in g.items()}
        out += [f"### By {title}", "",
                f"| {title} | Liable party: v1.4 | Remedy: v1.4 | Liable party: historical | Remedy: historical |",
                "|---|---|---|---|---|"]
        for name in sorted(g):
            a, m = stats["by_" + field][name], len(g[name])
            out.append(f"| {name} | {pct(a['v1.4']['liable_party'], m)} | {pct(a['v1.4']['remedy'], m)} | "
                       f"{pct(a['historical']['liable_party'], m)} | {pct(a['historical']['remedy'], m)} |")
        out.append("")

    conf = defaultdict(list)
    for row in rows:
        if row[2]["confidence"]:
            conf[row[2]["confidence"]].append(row)
    stats["calibration"] = {c: {"n": len(v), **{ver: sum(matches(r, k, ver, "liable_party") for _, k, r in v) for ver in VERSIONS}}
                            for c, v in conf.items()}
    out += ["### Expert calibration (liable party)", "",
            "| Confidence | n | Agrees with v1.4 label | Agrees with historical label |", "|---|---|---|---|"]
    out += [f"| {c} | {s['n']} | {pct(s['v1.4'], s['n'])} | {pct(s['historical'], s['n'])} |" for c, s in sorted(stats["calibration"].items())]
    out.append("")

    arb = arbiter_labels(key) if arb is None else arb
    names = sorted({name for d in arb.values() for name in d})
    stats["arbiters"] = {}
    out += ["## Expert vs each arbiter (same case, same evidence level; liable party)", "",
            "| Arbiter | Cases | Agreement with expert | Kappa | Expert matches v1.4, arbiter does not | Arbiter matches v1.4, expert does not "
            "| Expert matches historical, arbiter does not | Arbiter matches historical, expert does not |",
            "|---|---|---|---|---|---|---|---|"]
    for name in names:
        xs = [(r["liable_party"], arb[aid][name][0], label(k, "v1.4")["liable_party"], label(k, "historical")["liable_party"])
              for aid, k, r in rows if name in arb.get(aid, {})]
        if not xs:
            continue
        e, a = [x[0] for x in xs], [x[1] for x in xs]
        s = {"n": len(xs), "agree": sum(x == y for x, y in zip(e, a))}
        for i, ver in ((2, "v1.4"), (3, "historical")):
            s[ver] = {"expert_only": sum(x[0] == x[i] and x[1] != x[i] for x in xs),
                      "arbiter_only": sum(x[1] == x[i] and x[0] != x[i] for x in xs)}
        stats["arbiters"][name] = s
        out.append(f"| {name} | {len(xs)} | {pct(s['agree'], len(xs))} | {kappa(e, a):.2f} | "
                   f"{s['v1.4']['expert_only']} | {s['v1.4']['arbiter_only']} | {s['historical']['expert_only']} | {s['historical']['arbiter_only']} |")

    out += ["", "## Expert/ground-truth disagreements (for adjudication under Amendment 11: ground-truth error, policy disagreement, evidence ambiguity, or expert slip)", "",
            "A case is listed if the expert's liable party or remedy differs from either label.", "",
            "| Case | Original id | Level | Stratum | Expert (liable / remedy, confidence) | v1.4 label (code / liable / remedy) "
            "| Historical label (code / liable / remedy) | Disagrees with | Arbiters (liable) | Expert notes |",
            "|---|---|---|---|---|---|---|---|---|---|"]
    stats["disagreements"] = {}
    for aid, k, r in rows:
        off = [v for v in VERSIONS if not matches(r, k, v, "both")]
        if not off:
            continue
        stats["disagreements"][aid] = off
        arbs = "; ".join(f"{name}: {v[0]}" for name, v in arb.get(aid, {}).items())
        out.append(f"| {aid} | {k['case_id']} | {k['level']} | {k['stratum']} | {r['liable_party']} / {r['remedy']} ({r['confidence']}) | "
                   f"{fmt_label(label(k, 'v1.4'))} | {fmt_label(label(k, 'historical'))} | {' and '.join(off)} | {arbs} | "
                   f"{(r.get('notes') or '').replace('|', '/')} |")
    return "\n".join(out) + "\n", stats


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("labels")
    ap.add_argument("--key", default=os.path.join(ROOT, "expert", "answer_key.json"))
    ap.add_argument("--out", default=os.path.join(ROOT, "results", "expert_baseline.md"))
    ap.add_argument("--title", default=TITLE, help="report title (e.g. to mark partial or non-independent labels)")
    ap.add_argument("--note", default=None, help="paragraph printed under the title")
    args = ap.parse_args(argv)
    with open(args.key, encoding="utf-8") as fh:
        key = json.load(fh)["cases"]
    text, _ = score(key, read_labels(args.labels), title=args.title, note=args.note)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

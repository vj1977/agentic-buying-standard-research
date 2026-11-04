#!/usr/bin/env python3
"""Draw the paper's three figures as SVG from the result files.

Standard library only. Every plotted number is parsed from `results/` (the Markdown
summaries and write-ups, and the Phase 3b jsonl logs where a summary does not state
the number), cross-checked between sources, and asserted against the text of
`paper/main.md`. Nothing is typed by hand; a mismatch stops the script.

    python3 paper/figures/make_figures.py      # writes paper/figures/fig*.svg
"""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
ROOT = PAPER.parent
RES = ROOT / "results"

FABLE, GROK = "claude-fable-5-1", "grok-4.7"

# Okabe-Ito hues (three, one per arbiter) and neutral inks on a white surface.
C_FABLE, C_GROK, C_A2, C_C1 = "#0072B2", "#D55E00", "#009E73", "#CC79A7"
INK, INK2, MUTED, GRID, AXIS = "#1f1f1f", "#454545", "#666666", "#e6e6e6", "#8c8c8c"
FONT = "'Helvetica Neue', Helvetica, Arial, 'Liberation Sans', sans-serif"
W, H = 600, 380
H3 = 576  # Figure 3 carries a second panel


# --------------------------------------------------------------------------- reading


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s)


KN = re.compile(r"(\d+)/(\d+)(?: = (\d+)% \[(\d+), (\d+)\])?")


class Rate:
    """k/n with the percentage and interval as printed in the source (if printed)."""

    def __init__(self, k: int, n: int, pct=None, lo=None, hi=None, src=""):
        self.k, self.n, self.src = k, n, src
        self.pct = pct if pct is not None else round_pct(k / n)
        w = wilson(k, n)
        self.lo = lo if lo is not None else round_pct(w[0])
        self.hi = hi if hi is not None else round_pct(w[1])
        self.printed_ci = lo is not None

    @property
    def p(self) -> float:
        return 100.0 * self.k / self.n

    def kn(self) -> str:
        return f"{self.k}/{self.n}"

    def full(self) -> str:
        return f"{self.k}/{self.n} = {self.pct}% [{self.lo}, {self.hi}]"

    def __repr__(self):
        return self.full()


def round_pct(x: float) -> int:
    return int(math.floor(100.0 * x + 0.5))


def wilson(k: int, n: int, z: float = 1.959963984540054):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def parse_rate(cell: str, src: str) -> Rate:
    m = KN.search(cell.replace("*", ""))
    if not m:
        raise SystemExit(f"no k/n in {cell!r} ({src})")
    k, n = int(m.group(1)), int(m.group(2))
    if m.group(3) is None:
        return Rate(k, n, src=src)
    return Rate(k, n, int(m.group(3)), int(m.group(4)), int(m.group(5)), src=src)


def table_after(text: str, heading: str, src: str):
    """First Markdown pipe table after the line starting with `heading`: list of dicts."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith(heading):
            break
    else:
        raise SystemExit(f"heading {heading!r} not found in {src}")
    j = i + 1
    while j < len(lines) and not lines[j].startswith("|"):
        j += 1
    rows = []
    while j < len(lines) and lines[j].startswith("|"):
        rows.append([c.strip().replace("**", "") for c in lines[j].strip().strip("|").split("|")])
        j += 1
    header, body = rows[0], [r for r in rows[2:]]
    return [dict(zip(header, r)) for r in body]


def table_at(text: str, header_start: str, src: str):
    """The Markdown pipe table whose header row starts with `header_start`: list of dicts."""
    lines = text.splitlines()
    starts = [i for i, ln in enumerate(lines) if ln.startswith(header_start)]
    if len(starts) != 1:
        raise SystemExit(f"{src}: expected one table header {header_start!r}, found {len(starts)}")
    j, rows = starts[0], []
    while j < len(lines) and lines[j].startswith("|"):
        rows.append([c.strip().replace("**", "") for c in lines[j].strip().strip("|").split("|")])
        j += 1
    return [dict(zip(rows[0], r)) for r in rows[2:]]


def pick(rows, src, **match):
    hits = [r for r in rows if all(r.get(k) == v for k, v in match.items())]
    if len(hits) != 1:
        raise SystemExit(f"{src}: expected one row for {match}, found {len(hits)}")
    return hits[0]


def check(cond: bool, what: str):
    if not cond:
        raise SystemExit(f"CHECK FAILED: {what}")


def must_contain(text: str, needle: str, where: str):
    check(norm(needle) in norm(text), f"{where} does not contain {needle!r}")


def check_ci(r: Rate, what: str):
    """A printed Wilson interval must equal the one recomputed from k/n."""
    if r.printed_ci:
        lo, hi = wilson(r.k, r.n)
        check((round_pct(lo), round_pct(hi)) == (r.lo, r.hi),
              f"{what}: printed interval [{r.lo}, {r.hi}] != Wilson of {r.kn()}")
    check(r.pct == round_pct(r.k / r.n), f"{what}: printed {r.pct}% != {r.kn()}")


def section(text: str, heading: str, src: str) -> str:
    """The text from the line starting with `heading` up to the next level-2 heading."""
    i = text.find("\n" + heading)
    check(i >= 0, f"{src}: heading {heading!r} not found")
    j = text.find("\n## ", i + 1)
    return text[i:] if j < 0 else text[i:j]


def mcnemar_one_sided(b: int, c: int) -> float:
    """Exact McNemar, one-sided (c < b): P(X <= c) for X ~ Binomial(b + c, 1/2)."""
    n = b + c
    return sum(math.comb(n, i) for i in range(c + 1)) / 2 ** n


def sci(p: float, sig: int) -> str:
    """p in the paper's e-notation with `sig` significant digits: 3e-8, 3.0e-8, 1.5e-11."""
    m, e = f"{p:.{sig - 1}e}".split("e")
    return f"{m}e{int(e)}"


def sup(p: float, sig: int) -> str:
    """p as the write-ups print it: 3.0 × 10⁻⁸."""
    m, e = f"{p:.{sig - 1}e}".split("e")
    return f"{m} × 10" + str(int(e)).translate(str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹"))


def paper_row(paper: str, first_cells: list[str]):
    """Cells of the pipe-table row in main.md whose leading cells equal `first_cells`."""
    for line in paper.splitlines():
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells[: len(first_cells)] == first_cells:
                return cells
    raise SystemExit(f"main.md: no table row starting {first_cells}")


def paper_header(paper: str, first_cell: str, must: str):
    for line in paper.splitlines():
        if line.startswith(f"| {first_cell} |") and must in line:
            return [c.strip() for c in line.strip().strip("|").split("|")]
    raise SystemExit(f"main.md: no header row {first_cell!r} with {must!r}")


# --------------------------------------------------------------------------- data


def load():
    paper = read(PAPER / "main.md")
    p2 = read(RES / "phase2_summary.md")
    p2w = read(RES / "PHASE2_DISPUTES.md")
    p3 = read(RES / "phase3_summary.md")
    p3w = read(RES / "PHASE3_ATTACKS.md")
    p3b = read(RES / "phase3b_summary.md")
    p3bw = read(RES / "PHASE3B_PROVENANCE.md")
    d = {}

    # ---- Figure 1: A1 liable-party accuracy by evidence level (Phase 2, historical v1.2 labels)
    src = "phase2_summary.md"
    rows = table_after(p2, "## A1 (end-to-end LLM arbiter): accuracy by evidence level", src)
    col = "Liable party correct (as reported)"  # v1.2 labels, as reported; post-audit columns sit beside it
    levels = ["E0", "E1", "E2", "E3"]
    acc = {}
    ph = paper_header(paper, "Arbiter", "Liable party correct")
    li = ph.index("Liable party correct")
    for arb in (FABLE, GROK):
        for lv in levels:
            r = parse_rate(pick(rows, src, Arbiter=arb, Level=lv)[col], src)
            check_ci(r, f"{src} {arb} {lv} liable party")
            # The write-up's table carries the same k/n.
            wl = [ln for ln in p2w.splitlines() if ln.startswith(f"| {arb} | {lv} |")]
            check(len(wl) >= 1, f"PHASE2_DISPUTES.md has a row for {arb} {lv}")
            wcell = [c.strip().replace("**", "") for c in wl[0].strip().strip("|").split("|")][3]
            check(wcell.startswith(r.kn()), f"PHASE2_DISPUTES.md {arb} {lv}: {wcell} vs {r.kn()}")
            # The paper's Section 5.5 table quotes it (interval at E0 and E3 only).
            cell = paper_row(paper, [arb, lv])[li]
            check(cell.startswith(f"{r.kn()} = {r.pct}%"), f"main.md {arb} {lv}: {cell!r} vs {r.full()}")
            if "[" in cell:
                check(cell == r.full(), f"main.md {arb} {lv}: {cell!r} vs {r.full()}")
            acc[(arb, lv)] = r
    must_contain(paper, f"from {acc[(GROK, 'E0')].pct}% and {acc[(FABLE, 'E0')].pct}% to "
                        f"{acc[(GROK, 'E3')].pct}% and {acc[(FABLE, 'E3')].pct}% liability accuracy",
                 "main.md Section 7")
    must_contain(paper, "scored against the historical rulebook v1.2 labels", "main.md Figure 1 caption")
    d["fig1"] = {"levels": levels, "acc": acc, "n": acc[(FABLE, "E0")].n}

    # ---- Figure 2: attack success at E3 within the same calls: before the gate, gate v1 (as run),
    #      gate v2 (post-audit, exploratory). Phase 3b, arm GA; A2 recomputed from its logged findings.
    src = "phase3b_summary.md section 2"
    g = table_after(p3b, "## 2. Attack success with and without the gate", src)
    a1 = {}
    for arb in (FABLE, GROK):
        for side in ("buyer", "merchant", "all"):
            row = pick(g, src, Arbiter=f"A1 {arb}", Side=side)
            p3r = parse_rate(row["Fooled without the gate (Phase 3)"], src)   # selected Phase 3 final (H10)
            pre = parse_rate(row["Fooled pre-gate (same call)"], src)
            wi = parse_rate(row["Fooled with the gate"], src)
            ab = parse_rate(row["Abstention only"], src)
            rv = parse_rate(row["Sent to review by the gate"], src)
            for r, nm in ((p3r, "phase3"), (pre, "pre-gate"), (wi, "with"), (ab, "abstention"), (rv, "review")):
                check_ci(r, f"{src} {arb} {side} {nm}")
            a1[(arb, side)] = {"phase3": p3r, "before": pre, "with": wi, "abst": ab, "review": rv}
    # Phase 3 arm table: the same selected Phase 3 counts by side.
    arms = table_after(p3, "## Optimised evidence attacks (Amendment 13)", "phase3_summary.md")
    for arm, arb in (("A: A1 claude-fable-5-1 at E3, N=10", FABLE), ("B: A1 grok-4.7 at E3, N=10", GROK)):
        row = pick(arms, "phase3_summary.md", Arm=arm)
        for side, c in (("buyer", "buyer side"), ("merchant", "merchant side"), ("all", "Fooled (best-of-N)")):
            r = parse_rate(row[c], "phase3_summary.md")
            check(r.kn() == a1[(arb, side)]["phase3"].kn(),
                  f"Phase 3 {arb} {side} {r.kn()} vs Phase 3b {a1[(arb, side)]['phase3'].kn()}")
    # Phase 3b jsonl (arm GA): recount fooled with the gate and in Phase 3 per side.
    ga = [json.loads(x) for x in read(RES / "phase3" / "p3_GA.jsonl").splitlines() if x.strip()]
    for arb in (FABLE, GROK):
        for side in ("buyer", "merchant"):
            recs = [x for x in ga if x["target"] == arb and x["side"] == side]
            check(len(recs) == a1[(arb, side)]["with"].n, f"p3_GA.jsonl n for {arb} {side}")
            check(sum(bool(x["success"]) for x in recs) == a1[(arb, side)]["with"].k,
                  f"p3_GA.jsonl gated successes for {arb} {side}")
            check(sum(bool(x["source_success"]) for x in recs) == a1[(arb, side)]["phase3"].k,
                  f"p3_GA.jsonl Phase 3 successes for {arb} {side}")
    # Post-audit F03: the same-call comparison and its exact McNemar p, cross-checked with section 2.
    src3 = "phase3b_summary.md post-audit F03"
    f03 = table_after(p3b, "## Post-audit (Audit 1), F03", src3)
    same_p = {}
    for arb in (FABLE, GROK):
        row = pick(f03, src3, Arbiter=f"A1 {arb}")
        check(row["Fresh call, same payload, before the gate"] == a1[(arb, "all")]["before"].kn(), f"{src3} {arb} before")
        check(row["After the gate, same call"] == a1[(arb, "all")]["with"].kn(), f"{src3} {arb} after")
        check(row["Phase 3 final (selected; as in H10)"] == a1[(arb, "all")]["phase3"].kn(), f"{src3} {arb} phase 3")
        same_p[arb] = float(row["Same-call exact McNemar p"])
        disc = [int(x) for x in row["Same-call discordant (only before / only after)"].split(" / ")]
        a1[(arb, "all")]["disc"] = disc
    # Post-audit F04: what the v1 rejections on the attacks were (format / provenance / contradiction).
    src4 = "phase3b_summary.md post-audit F04"
    f04 = table_after(p3b, "## Post-audit (Audit 1), F04", src4)
    split = {}
    for arb in (FABLE, GROK):
        cell = pick(f04, src4, Data=f"A1 {arb}, Phase 3 final payloads (GA)")["v1 rejections: format / provenance / contradiction"]
        split[arb] = [int(x) for x in cell.split(" / ")]
        check(sum(split[arb]) == a1[(arb, "all")]["review"].k, f"{src4} {arb}: rejections sum to the gate's reviews")
    # Post-audit F05: gate v2 on the stored outputs (exploratory). Reported pooled over sides: a zero
    # pooled count is zero on each side; any other count would need the per-side records.
    src5 = "phase3b_summary.md post-audit F05"
    f05 = table_after(p3b, "## Post-audit (Audit 1), F05", src5)
    V2 = "v2, stored values: bad / review / decided correctly"
    def v2_parts(data):
        parts = [parse_rate(x, src5) for x in pick(f05, src5, Data=data)[V2].split(" / ")]
        check(len(parts) == 3, f"{src5} {data}: three parts")
        return parts
    for arb in (FABLE, GROK):
        bad, _, _ = v2_parts(f"A1 {arb}, Phase 3 final payloads (GA)")
        check(bad.n == a1[(arb, "all")]["with"].n, f"{src5} {arb} n")
        check(bad.k == 0, f"{src5} {arb}: v2 lets {bad.kn()} through; per-side split needs the records")
        a1[(arb, "all")]["v2"] = bad
        for side in ("buyer", "merchant"):
            a1[(arb, side)]["v2"] = Rate(0, a1[(arb, side)]["with"].n, src=src5 + " (zero pooled)")
    a2_v2_bad, _, _ = v2_parts("A2 hybrid, attacked (arm D + transfers), attempts")
    check(a2_v2_bad.k == 0, f"{src5} A2: v2 lets {a2_v2_bad.kn()} attempts through")
    _, fable_v2_review, _ = v2_parts(f"A1 {FABLE}, baseline Phase 2 workload (GB)")
    # Post-audit (Audit 3) N03 and F05: gate v3 on the stored outputs (exploratory). The paper's Figure 2
    # plots v3 and states that v2 gives the same counts; both must be zero on every attacked row.
    src6 = "phase3b_summary.md post-audit (Audit 3) N03 and F05"
    f3g = table_after(p3b, "## Post-audit (Audit 3), N03 and F05", src6)
    V3 = "v3: bad / review / decided correctly"
    def v3_parts(data):
        parts = [parse_rate(x, src6) for x in pick(f3g, src6, Data=data)[V3].split(" / ")]
        check(len(parts) == 3, f"{src6} {data}: three parts")
        return parts
    for arb in (FABLE, GROK):
        bad3, _, _ = v3_parts(f"A1 {arb}, Phase 3 final payloads (GA)")
        check(bad3.n == a1[(arb, "all")]["with"].n, f"{src6} {arb} n")
        check(bad3.k == 0 and a1[(arb, "all")]["v2"].k == 0,
              f"{src6} {arb}: v3 lets {bad3.kn()} through; per-side split needs the records")
        a1[(arb, "all")]["v3"] = bad3
        for side in ("buyer", "merchant"):
            a1[(arb, side)]["v3"] = Rate(0, a1[(arb, side)]["with"].n, src=src6 + " (zero pooled)")
    a2_v3_bad, _, _ = v3_parts("A2 hybrid, attacked (arm D + transfers), attempts")
    check(a2_v3_bad.k == 0, f"{src6} A2: v3 lets {a2_v3_bad.kn()} attempts through")
    _, fable_v3_review, _ = v3_parts(f"A1 {FABLE}, baseline Phase 2 workload (GB)")
    # A2: deterministic recomputation, strict (pre-registered) engine rule, case-sides.
    src = "phase3b_summary.md section 3"
    g3 = table_after(p3b, "## 3. Attack success with and without the gate: A2 hybrid", src)
    a2 = {}
    for side in ("buyer", "merchant", "all"):
        cell = pick(g3, src, Side=side, Rule="strict")["Case-sides fooled without / with"]
        m = re.fullmatch(r"(\d+)/(\d+) / (\d+)/(\d+)", cell)
        check(m is not None, f"{src}: case-sides cell {cell!r}")
        a2[side] = {"before": Rate(int(m.group(1)), int(m.group(2)), src=src),
                    "with": Rate(int(m.group(3)), int(m.group(4)), src=src),
                    "v2": Rate(0, int(m.group(2)), src=src5 + " (zero attempts fooled)"),
                    "v3": Rate(0, int(m.group(2)), src=src6 + " (zero attempts fooled)")}
    # The paper's wording, rebuilt from the parsed numbers.
    fa, gr = a1[(FABLE, "all")], a1[(GROK, "all")]
    must_contain(paper, f"Within the same calls, the gate cut fable's attack success at E3 from {fa['before'].kn()} to "
                        f"{fa['with'].kn()} ({fa['disc'][0]} discordant case-sides, exact McNemar p = {same_p[FABLE]:.3f}) "
                        f"and grok's from {gr['before'].kn()} to {gr['with'].kn()} (p = {same_p[GROK]:.3f}); "
                        f"A2's attacked case-sides fell from {a2['all']['before'].kn()} to {a2['all']['with'].kn()}", "main.md 5.6")
    check(fa["disc"][1] == 0 and gr["disc"][1] == 0, "no case-side fooled only with the gate")
    must_contain(paper, f"{fa['phase3'].kn()} to {fa['with'].kn()}, p = 0.001, supported as computed but confounded", "main.md 5.6 (H10)")
    split_sentence = (f"fable's split {split[FABLE][0]} format, {split[FABLE][1]} provenance and {split[FABLE][2]} "
                      f"contradiction, and grok's {split[GROK][0]}, {split[GROK][1]} and {split[GROK][2]}")
    must_contain(paper, "Most of the A1 effect is a format failure: the gate reads only true or false values and both "
                        "arbiters mostly wrote free text, so of the gate's rejections on the attacks " + split_sentence, "main.md 5.6")
    must_contain(paper, f"both revisions let {fa['v3'].kn()} attacks through for fable, {gr['v3'].kn()} for grok and "
                        f"{a2_v3_bad.kn()} attacked A2 attempts", "main.md 7 (gates v2 and v3)")
    must_contain(paper, "Both are exploratory: written after the reviews with these outputs in view", "main.md 7 (gates v2, v3)")
    must_contain(paper, "after the revised gate (v3, exploratory: written after the reviews with these outputs in view; "
                        "v2 gives the same counts)", "main.md Figure 2 caption")
    for arb, label in ((FABLE, "A1 claude-fable-5-1, E3, N = 10"), (GROK, "A1 grok-4.7, E3, N = 10")):
        cells = paper_row(paper, [label])
        check(cells[2] == a1[(arb, "buyer")]["phase3"].kn() and cells[3] == a1[(arb, "merchant")]["phase3"].kn(),
              f"main.md Phase 3 table sides for {arb}")
    must_contain(p3bw, f"fooled case-sides from {a2['all']['before'].kn()} to {a2['all']['with'].kn()} (all buyer side",
                 "PHASE3B_PROVENANCE.md")
    must_contain(p3bw, "fable 11/14 -> 1/14, grok 12/14 -> 1/14", "PHASE3B_PROVENANCE.md post-audit headline")
    must_contain(p3w, f"| **{fa['phase3'].full()}** | {a1[(FABLE, 'buyer')]['phase3'].kn()} | "
                      f"{a1[(FABLE, 'merchant')]['phase3'].kn()} |", "PHASE3_ATTACKS.md")
    d["fig2"] = {"a1": a1, "a2": a2, "split": split}

    # ---- Figure 3: baseline Phase 2 workload sent to review against attack success (Phase 3b)
    src = "phase3b_summary.md section 4"
    g4 = table_after(p3b, "## 4. What the gate costs on the baseline Phase 2 workload", src)
    fr = pick(g4, src, Arbiter=f"A1 {FABLE}")
    f_gate = parse_rate(fr["Review with the gate"], src)
    f_abst = parse_rate(fr["Abstention only: review / accuracy when decided"].split(" / ")[0], src)
    a2_plain = parse_rate(pick(g4, src, Arbiter="A2 hybrid, strict, no gate")["Review with the gate"], src)
    a2_gate = parse_rate(pick(g4, src, Arbiter="A2 hybrid, strict, gate")["Review with the gate"], src)
    for r, nm in ((f_gate, "fable gate"), (f_abst, "fable abstention")):
        check_ci(r, f"{src} {nm}")
    check(fable_v2_review.n == f_gate.n, "gate v2 baseline n matches gate v1")
    # Who carries the review (post-audit F22): true claimants against unfounded claims, gated fable.
    src22 = "phase3b_summary.md post-audit F22"
    f22 = pick(table_after(p3b, "## Post-audit (Audit 1), F22", src22), src22,
               Arbiter=f"A1 {FABLE}", Stratum="all")
    tc, uf = f22["Review on true claimants (v1)"], f22["Review on unfounded claims (v1)"]
    check(f22["Review with gate v2"] == fable_v2_review.kn(), f"{src22}: v2 review matches F05")
    # The A2 review intervals are clustered by case (not Wilson): keep them as printed.
    # The plain A1 arbiter never sends a case to review: recount it, with the other two
    # A1 operating points, from the arm GB log.
    gb = [json.loads(x) for x in read(RES / "phase3" / "p3_GB.jsonl").splitlines() if x.strip()]
    gb = [x for x in gb if x["arbiter"] == FABLE and x["level"] == "E3" and x.get("pre_gate")]
    check(len(gb) == f_gate.n, f"p3_GB.jsonl valid records {len(gb)} vs {f_gate.n}")
    check(sum(x["verdict"] == "review" for x in gb) == f_gate.k, "p3_GB.jsonl gate reviews")
    check(sum(x["pre_gate"]["confidence"] < 0.7 for x in gb) == f_abst.k, "p3_GB.jsonl abstentions")
    f_plain = Rate(sum(x["pre_gate"].get("liable_party") == "review" for x in gb), len(gb), src="p3_GB.jsonl")
    # The A2 rates agree with Phase 2.
    p2a = table_after(p2, "## Arbiter architectures at E3", "phase2_summary.md")
    r = parse_rate(pick(p2a, "phase2_summary.md", Architecture="A2 fable+grok finders, opus tie-break")["Human review"],
                   "phase2_summary.md")
    check(r.kn() == a2_plain.kn(), "A2 review, Phase 2 vs Phase 3b")
    # Paper wording.
    must_contain(paper, f"Gated fable (v1) sent {f_gate.k} of {f_gate.n} cases to review ({f_gate.pct}% [{f_gate.lo}, "
                        f"{f_gate.hi}]): {tc.split('/')[0]} of {tc.split('/')[1]} true claimants against "
                        f"{uf.split('/')[0]} of {uf.split('/')[1]} unfounded claims", "main.md 7")
    must_contain(paper, f"Gate v2 sent {fable_v2_review.k} of {fable_v2_review.n}.", "main.md 7")
    # Audit 3: the review burden at case level, gate v1 -> v2 -> v3 (fable one decision per case; A2 any run).
    src33 = "phase3b_summary.md post-audit (Audit 3) review burden"
    rb = table_after(p3b, "## Post-audit (Audit 3): the review burden by stratum", src33)
    fb = pick(rb, src33, Arbiter=f"A1 {FABLE}", Stratum="all")
    f_v3 = parse_rate(fb["Review, gate v3"], src33)
    check_ci(f_v3, f"{src33} fable v3")
    check(f_v3.kn() == fable_v3_review.kn(), f"{src33}: v3 review {f_v3.kn()} vs {fable_v3_review.kn()}")
    check(parse_rate(fb["Review, gate v1 (as run)"], src33).kn() == f_gate.kn(), f"{src33}: v1 review matches")
    tc3 = re.fullmatch(r"(\d+) -> (\d+) -> (\d+) of (\d+)", fb["True claimants reviewed, v1 -> v2 -> v3"])
    uf3 = re.fullmatch(r"(\d+) -> (\d+) -> (\d+) of (\d+)", fb["Unfounded claims reviewed, v1 -> v2 -> v3"])
    check(tc3 is not None and uf3 is not None, f"{src33}: claimant cells")
    check(f"{tc3.group(1)}/{tc3.group(4)}" == tc and f"{uf3.group(1)}/{uf3.group(4)}" == uf, f"{src33}: v1 claimants match F22")
    must_contain(paper, f"Gate v3 sends {f_v3.k} of {f_v3.n} ({f_v3.pct}% [{f_v3.lo}, {f_v3.hi}]): {tc3.group(3)} of "
                        f"{tc3.group(4)} true claimants and {uf3.group(3)} of {uf3.group(4)} unfounded claims", "main.md 7")
    a2b = pick(rb, src33, Arbiter="A2 hybrid (strict)", Stratum="all")
    a2_gate_cases = parse_rate(a2b["Review, gate v1 (as run)"], src33)
    # A2 case level: a case counts as reviewed if any of its three runs was (Audit 3, N06).
    src3c = "phase3_summary.md post-audit (Audit 3) N01, N02 and N06"
    c3 = table_after(p3, "## Post-audit (Audit 3), N01, N02 and N06", src3c)
    P2 = "Phase 2, 153 runs at E3 (51 cases, 44 roots)"
    ATT = "Phase 3 attacked: arm D + A2 transfers (14 case-sides)"
    a2_plain_cases = parse_rate(pick(c3, src3c, Data=P2, Rule="as run (recomputed)")["Cases with a run sent to review"], src3c)
    a2_v3_cases = parse_rate(pick(c3, src3c, Data=P2, Rule="contract v3 + gate v3")["Cases with a run sent to review"], src3c)
    def fooled_cases(rule):
        cell = pick(c3, src3c, Data=ATT, Rule=rule)["Manipulated / fooled"]
        m = re.search(r"case-sides (\d+)/(\d+)", cell)
        check(m is not None, f"{src3c} {rule}: fooled cell {cell!r}")
        return Rate(int(m.group(1)), int(m.group(2)), src=src3c)
    a2_plain_att = fooled_cases("as run (recomputed)")
    a2_v3_att = fooled_cases("contract v3 + gate v3")
    for r, nm in ((a2_plain_cases, "A2 as run"), (a2_v3_cases, "A2 v3"), (a2_gate_cases, "A2 gate v1")):
        check_ci(r, f"{src3c} {nm} cases reviewed")
    check(a2_plain_att.kn() == a2["all"]["before"].kn(), f"{src3c}: A2 attacked as run {a2_plain_att.kn()} vs Phase 3b")
    check(a2_v3_att.k == 0, f"{src3c}: A2 contract v3 + gate v3 fooled {a2_v3_att.kn()}")
    must_contain(paper, f"the hybrid sent {a2_plain_cases.k} of {a2_plain_cases.n} cases to review at least once "
                        f"({a2_plain_cases.pct}% [{a2_plain_cases.lo}, {a2_plain_cases.hi}])", "main.md 5")
    must_contain(paper, f"For the hybrid with contract v3 and gate v3, {a2_v3_cases.k} of {a2_v3_cases.n} cases have a run "
                        f"sent to review ({a2_v3_cases.pct}% [{a2_v3_cases.lo}, {a2_v3_cases.hi}]) and none of the "
                        f"{a2_v3_att.n} attacked case-sides is fooled", "main.md 7")
    must_contain(paper, f"Abstention below 0.7 alone reviewed {f_abst.kn()} but let "
                        f"{fa['abst'].kn()} attacks through", "main.md 5.6")
    must_contain(paper, f"| {a2_plain.kn()} | 68/70 |", "main.md 5 table (A2 runs sent to review, descriptive)")
    must_contain(paper, "| A1 claude-fable-5-1 | 0/153 |", "main.md 5 table (A1 never reviews)")
    must_contain(paper, "the share of the baseline Phase 2 workload sent to human review", "main.md Figure 3 caption")
    must_contain(p3bw, f"{a2_plain.kn()} -> {a2_gate.kn()} runs", "PHASE3B_PROVENANCE.md")
    must_contain(p3bw, f"({a2_plain.pct}% -> {a2_gate.pct}%, clustered)", "PHASE3B_PROVENANCE.md")
    # ---- Confirmatory amendment C1: gate v3 off and on with a gate-aware attacker on 14 fresh case-sides,
    #      and the baseline cost on the 51 Phase 2 cases (results/confirmatory_c1_summary.md, frozen analysis).
    c1s = read(RES / "confirmatory_c1_summary.md")
    c1w = read(RES / "CONFIRMATORY_C1.md")
    srcc = "confirmatory_c1_summary.md section 4"
    h11 = pick(table_after(c1s, "## 4. H11 (primary, confirmatory)", srcc), srcc, **{"": "case-sides fooled, best of 5"})
    c1_off, c1_on = parse_rate(h11["Arm A (gate off)"], srcc), parse_rate(h11["Arm B (gate v3 on)"], srcc)
    srcb = "confirmatory_c1_summary.md section 7"
    blt = table_after(c1s, "## 7. Baseline cost", srcb)
    rv = pick(blt, srcb, **{"": "sent to review"})
    c1_rev_off, c1_rev_on = parse_rate(rv["Gate off"], srcb), parse_rate(rv["Gate v3 on"], srcb)
    okr = pick(blt, srcb, **{"": "liable party correct, review and invalid counted as not correct"})
    c1_ok_off, c1_ok_on = parse_rate(okr["Gate off"], srcb), parse_rate(okr["Gate v3 on"], srcb)
    for r, nm in ((c1_off, "arm A fooled"), (c1_on, "arm B fooled"), (c1_rev_on, "baseline review"),
                  (c1_ok_off, "correct, gate off"), (c1_ok_on, "correct, gate on")):
        check_ci(r, f"C1 {nm}")
    byp = {}
    for party in ("merchant", "agent_provider", "buyer"):
        byp[party] = parse_rate(pick(table_at(c1s, "| True liable party |", srcb), srcb,
                                     **{"True liable party": party})["Gate on: review"], srcb)
    tc_c1 = Rate(byp["merchant"].k + byp["agent_provider"].k, byp["merchant"].n + byp["agent_provider"].n)
    uf_c1 = byp["buyer"]
    check(tc_c1.k + uf_c1.k == c1_rev_on.k and tc_c1.n + uf_c1.n == c1_rev_on.n, "C1 review split by true liable party")
    m = re.search(r"Exact McNemar, one-sided \(B < A\): p = ([0-9.]+)", c1s)
    check(m is not None, "C1 one-sided McNemar p")
    p_c1 = float(m.group(1))
    m = re.search(r"Discordant case-sides: fooled in A only (\d+), in B only (\d+)\.", c1s)
    check(m is not None and int(m.group(2)) == 0 and int(m.group(1)) == c1_off.k - c1_on.k, "C1 discordant pairs")
    m = re.search(r"Paired difference B - A: (-?\d+) pp \[(-?\d+), (-?\d+)\]", c1s)
    check(m is not None, "C1 paired difference")
    diff_c1 = f"{m.group(1)} points [{m.group(2)}, {m.group(3)}]"
    # Recount from the frozen run's records.
    c1rec = {arm: [json.loads(x) for x in read(RES / "c1" / f"c1_{arm}.jsonl").splitlines() if x.strip()] for arm in "AB"}
    for arm, rate in (("A", c1_off), ("B", c1_on)):
        ids = sorted({x["case_id"] for x in c1rec[arm]})
        fooled = sum(any(x["success"] for x in c1rec[arm] if x["case_id"] == c) for c in ids)
        check((fooled, len(ids)) == (rate.k, rate.n), f"c1_{arm}.jsonl: {fooled}/{len(ids)} vs {rate.kn()}")
    blr = [json.loads(x) for x in read(RES / "c1" / "c1_BL.jsonl").splitlines() if x.strip()]
    check(len(blr) == c1_rev_on.n and sum(x["verdict"] == "review" for x in blr) == c1_rev_on.k, "c1_BL.jsonl reviews")
    check(c1_rev_off.k == 0 and c1_rev_off.n == len(blr), "C1 gate off reviews nothing")
    check(sum(x["pre_gate"]["liable_party"] == x["ground_truth"]["liable_party"] for x in blr) == c1_ok_off.k,
          "c1_BL.jsonl correct with the gate off")
    check(sum(x["verdict"] == "decided" and x["decision"]["liable_party"] == x["ground_truth"]["liable_party"]
              for x in blr) == c1_ok_on.k, "c1_BL.jsonl correct with the gate on")
    n_dec = c1_rev_on.n - c1_rev_on.k
    # The write-up and the paper's wording.
    must_contain(c1w, f"exact McNemar one-sided **p = {p_c1:.2g}**", "CONFIRMATORY_C1.md headline")
    must_contain(paper, f"the same gate sent {c1_rev_on.k} to a human, {tc_c1.k} of {tc_c1.n} true claimants among them, "
                        f"and correct decided outcomes fell from {c1_ok_off.k} to {c1_ok_on.k} of {c1_ok_on.n}",
                 "main.md abstract (C1 cost)")
    must_contain(paper, f"H11 is supported: {c1_off.k} of {c1_off.n} case-sides fooled with the gate off ({c1_off.pct}% "
                        f"[{c1_off.lo}, {c1_off.hi}]), {c1_on.k} of {c1_on.n} with it on ({c1_on.pct}% [{c1_on.lo}, "
                        f"{c1_on.hi}]); all {c1_off.k - c1_on.k} discordant pairs go one way, exact McNemar one-sided "
                        f"p = {p_c1:.2g}, {diff_c1}", "main.md 7 (C1)")
    must_contain(paper, f"Gate v3 sent {c1_rev_on.k} of {c1_rev_on.n} to review ({c1_rev_on.pct}% [{c1_rev_on.lo}, "
                        f"{c1_rev_on.hi}]), {tc_c1.k} of {tc_c1.n} true claimants and {uf_c1.k} of {uf_c1.n} unfounded "
                        f"claims, and decided {c1_ok_on.k} of the other {n_dec} correctly: correct decided outcomes fell "
                        f"from {c1_ok_off.k} of {c1_ok_off.n} with the gate off to {c1_ok_on.k} of {c1_ok_on.n}",
                 "main.md 7 (C1 cost)")
    must_contain(paper, "Diamonds are confirmatory (C1)", "main.md Figure 3 caption")

    # ---- Confirmatory amendment C2: H11 replicated (H11-R) on 28 further fresh case-sides with C1's frozen code,
    #      judge and attacker, and the pooled C1 + C2 estimate (results/confirmatory_c2_summary.md, written by the
    #      analysis frozen with the amendment). C2 has no baseline arm, so it has no point in the upper panel.
    c2s = read(RES / "confirmatory_c2_summary.md")
    c2w = read(RES / "CONFIRMATORY_C2.md")
    src4 = "confirmatory_c2_summary.md section 4"
    sec4 = section(c2s, "## 4. H11-R (primary, confirmatory)", src4)
    h11r = pick(table_after(c2s, "## 4. H11-R (primary, confirmatory)", src4), src4,
                **{"": "case-sides fooled, best of 5"})
    c2_off, c2_on = parse_rate(h11r["Arm A (gate off)"], src4), parse_rate(h11r["Arm B (gate v3 on)"], src4)
    m = re.search(r"Discordant case-sides: fooled in A only (\d+), in B only (\d+)\.", sec4)
    check(m is not None, "C2 discordant pairs")
    disc_a, disc_b = int(m.group(1)), int(m.group(2))
    check(disc_b == 0 and disc_a == c2_off.k - c2_on.k, "C2 discordant pairs all one way")
    m = re.search(r"Exact McNemar, one-sided \(B < A\): p = ([0-9.]+(?:e-?\d+)?)", sec4)
    check(m is not None, "C2 one-sided McNemar p")
    p_c2 = mcnemar_one_sided(disc_a, disc_b)
    check(math.isclose(p_c2, float(m.group(1)), rel_tol=5e-3), f"C2 p {m.group(1)} != exact {p_c2:.4g}")
    m = re.search(r"Paired difference B - A: (-?\d+) pp \[(-?\d+), (-?\d+)\]", sec4)
    check(m is not None, "C2 paired difference")
    diff_c2 = f"{m.group(1)} points [{m.group(2)}, {m.group(3)}]"
    c2_side = {}
    for sd in ("buyer", "merchant"):
        m = re.search(rf"- side {sd}: A (\d+/\d+ = \d+% \[\d+, \d+\]), B (\d+/\d+ = \d+% \[\d+, \d+\])", sec4)
        check(m is not None, f"C2 side {sd}")
        c2_side[sd] = (parse_rate(m.group(1), src4), parse_rate(m.group(2), src4))
    check(sum(a.k for a, _ in c2_side.values()) == c2_off.k and sum(b.k for _, b in c2_side.values()) == c2_on.k
          and sum(a.n for a, _ in c2_side.values()) == c2_off.n, "C2 sides add up")
    m = re.search(r"\| A \| (\d+) \|", sec4)
    check(m is not None, "C2 best-of-k, k = 1")
    first_c2 = int(m.group(1))
    # Pooled C1 + C2 (secondary, descriptive: C1's case-sides were known when C2 was frozen).
    src5 = "confirmatory_c2_summary.md section 5"
    sec5 = section(c2s, "## 5. Pooled C1 + C2 (secondary)", src5)
    pt = table_after(c2s, "## 5. Pooled C1 + C2 (secondary)", src5)
    for study, off, on in (("C1", c1_off, c1_on), ("C2", c2_off, c2_on)):
        row = pick(pt, src5, Study=study)
        for col, r in (("Arm A fooled", off), ("Arm B fooled", on)):
            check(parse_rate(row[col], src5).full() == r.full(), f"C2 pooled table, {study} {col}")
    row = pick(pt, src5, Study="C1 + C2")
    pool_off, pool_on = parse_rate(row["Arm A fooled"], src5), parse_rate(row["Arm B fooled"], src5)
    check((pool_off.k, pool_off.n, pool_on.k, pool_on.n) == (c1_off.k + c2_off.k, c1_off.n + c2_off.n,
                                                           c1_on.k + c2_on.k, c1_on.n + c2_on.n), "pooled = C1 + C2")
    m = re.search(r"Pooled: Discordant case-sides: fooled in A only (\d+), in B only (\d+)\. Exact McNemar, one-sided "
                  r"\(B < A\): p = ([0-9.]+(?:e-?\d+)?)", sec5)
    check(m is not None, "pooled McNemar")
    p_pool = mcnemar_one_sided(int(m.group(1)), int(m.group(2)))
    check(int(m.group(1)) == pool_off.k - pool_on.k and math.isclose(p_pool, float(m.group(3)), rel_tol=5e-3),
          "pooled discordant pairs and p")
    for r, nm in ((c2_off, "C2 arm A"), (c2_on, "C2 arm B"), (pool_off, "pooled arm A"), (pool_on, "pooled arm B"),
                  *[(r, f"C2 {sd}") for sd, pr in c2_side.items() for r in pr]):
        check_ci(r, nm)
    # Attacker strength (section 7 of the summary).
    src7 = "confirmatory_c2_summary.md section 7"
    sec7 = section(c2s, "## 7. Attacker strength (secondary)", src7)
    m = re.search(r"C2, both arms: no usable payload on (\d+)/(\d+) = .*?evidence payloads (\d+)/(\d+) =", sec7)
    check(m is not None and m.group(1) == "0" and m.group(2) == m.group(4), "C2 payload counts")
    n_att_c2, n_ev_c2 = int(m.group(2)), int(m.group(3))
    m = re.search(r"C1 \+ C2, both arms: no usable payload on (\d+)/(\d+) ", sec7)
    check(m is not None and m.group(1) == "0", "C1 + C2 payload counts")
    n_att_pool = int(m.group(2))
    m = re.search(r"Arm A successes at the first attempt: C2 (\d+) of (\d+) fooled case-sides", sec7)
    check(m is not None and int(m.group(1)) == first_c2 and int(m.group(2)) == c2_off.k, "C2 first-attempt successes")
    # Recount from the frozen run's records: fooled case-sides per arm, pooled with C1's, and the gate's review of
    # the judge's correct decisions in the gated arm (Section 7 of the write-up, exploratory).
    c2rec = {arm: [json.loads(x) for x in read(RES / "c2" / f"c2_{arm}.jsonl").splitlines() if x.strip()] for arm in "AB"}
    fooled_ids = {}
    for arm, rate in (("A", c2_off), ("B", c2_on)):
        ids = sorted({x["case_id"] for x in c2rec[arm]})
        fooled_ids[arm] = {c for c in ids if any(x["success"] for x in c2rec[arm] if x["case_id"] == c)}
        check((len(fooled_ids[arm]), len(ids)) == (rate.k, rate.n), f"c2_{arm}.jsonl: {len(fooled_ids[arm])}/{len(ids)}")
        both = [r for r in c1rec[arm] + c2rec[arm]]
        ids_p = {x["case_id"] for x in both}
        f_p = sum(any(x["success"] for x in both if x["case_id"] == c) for c in ids_p)
        prate = pool_off if arm == "A" else pool_on
        check((f_p, len(ids_p)) == (prate.k, prate.n), f"c1 + c2 {arm} records vs pooled {prate.kn()}")
    check(len(c2rec["A"]) + len(c2rec["B"]) == n_att_c2, "C2 attempts = records")
    ok_b = [x for x in c2rec["B"] if x["pre_gate"] and x["pre_gate"].get("liable_party") == x["ground_truth"]["liable_party"]]
    rev_ok_b = sum(x["gate"].get("verdict") == "review" for x in ok_b)
    must_contain(c2w, f"The gate sent {rev_ok_b} of those {len(ok_b)} to review", "CONFIRMATORY_C2.md section 7")
    # The three A01 ink case-sides (a single-item packing record on a two-unit line): H11-R without them.
    cs = table_at(c2s, "| Case-side | Phase 3 counterpart |", "confirmatory_c2_summary.md section 3")
    ink = {r["Case-side"] for r in cs if r["Scenario"] == "A01"}
    check(len(ink) == 3 and len(cs) == c2_off.n, "C2 ink case-sides")
    ink_off = Rate(len(fooled_ids["A"] - ink), c2_off.n - len(ink))
    ink_on = Rate(len(fooled_ids["B"] - ink), c2_on.n - len(ink))
    p_ink = mcnemar_one_sided(ink_off.k - ink_on.k, 0) if ink_on.k == 0 else None
    check(p_ink is not None, "C2 ink exclusion: arm B fooled none")
    must_contain(c2w, f"Without these three case-sides, H11-R is {ink_off.kn()} against {ink_on.kn()} (one-sided "
                      f"p = {sup(p_ink, 2)})", "CONFIRMATORY_C2.md section 7")
    # Model calls (section 1 of the summary; the project's ledger).
    m = re.search(r"\| \*\*total\*\* \| \*\*(\d+)\*\* of at most (\d+) \|", c2s)
    check(m is not None, "C2 calls")
    calls_c2 = int(m.group(1))
    calls_all = sum(1 for x in read(RES / "calls.jsonl").splitlines() if x.strip())
    # The write-up and the paper's wording.
    must_contain(c2w, f"exact McNemar one-sided **p = {sup(p_c2, 2)}**", "CONFIRMATORY_C2.md headline")
    check(pool_on.k == 0 and c2_on.k == 0, "the paper says 'none of 42' and 'to none'")
    must_contain(paper, f"two frozen, pre-registered tests on {pool_off.n} fresh case-sides ({c1_off.n}, then a "
                        f"replication on {c2_off.n})", "main.md abstract (C1 + C2)")
    must_contain(paper, f"the attacker fooled the judge on {pool_off.k} of {pool_off.n} case-sides with the gate off and "
                        f"on none of {pool_on.n} with it on (first test {c1_off.k} of {c1_off.n} against {c1_on.k} of "
                        f"{c1_on.n}, exact McNemar, one-sided p = {p_c1:.1g}; replication {c2_off.k} of {c2_off.n} "
                        f"against {c2_on.k} of {c2_on.n}, p = {sci(p_c2, 1)})", "main.md abstract (C1 + C2)")
    must_contain(paper, f"{calls_all:,} model calls in all: 6,560 before the reviews, 343 in C1 and {calls_c2} in C2",
                 "main.md 4 (calls)")
    bs, ms = c2_side["buyer"], c2_side["merchant"]
    must_contain(paper, f"H11-R is supported: {c2_off.k} of {c2_off.n} fooled with the gate off ({c2_off.pct}% "
                        f"[{c2_off.lo}, {c2_off.hi}]), {c2_on.k} of {c2_on.n} with it on ({c2_on.pct}% [{c2_on.lo}, "
                        f"{c2_on.hi}]); all {disc_a} discordant pairs go one way, exact McNemar one-sided "
                        f"p = {sci(p_c2, 2)}, {diff_c2}; buyer side {bs[0].k} of {bs[0].n} and merchant side "
                        f"{ms[0].k} of {ms[0].n} to none", "main.md 7 (C2)")
    must_contain(paper, f"Pooled with C1, descriptively since C1 was known: {pool_off.k} of {pool_off.n} against "
                        f"{pool_on.k} of {pool_on.n} ({pool_on.pct}% [{pool_on.lo}, {pool_on.hi}])", "main.md 7 (pooled)")
    must_contain(paper, f"The attacker wrote a payload on all {n_att_c2} attempts, fabricated evidence on {n_ev_c2} and "
                        f"won {first_c2} of its {c2_off.k} at the first attempt", "main.md 7 (C2 attacker)")
    must_contain(paper, f"Under attack the gate also reviewed {rev_ok_b} of the judge's {len(ok_b)} correct decisions",
                 "main.md 7 (C2 cost under attack)")
    must_contain(paper, f"fooled a second Claude judge on {pool_off.k} of {pool_off.n} fresh case-sides", "main.md 9.1")
    must_contain(paper, f"stopped an attacker that saw it on all {pool_on.n} fresh case-sides", "main.md 9.1")
    must_contain(paper, f"wrote one on all {n_att_pool} of its C1 and C2 attempts", "main.md 9.2")
    must_contain(paper, f"without them C2 is {ink_off.k} of {ink_off.n} against {ink_on.k} of {ink_on.n} "
                        f"(p = {sci(p_ink, 2)})", "main.md 9.4")
    must_contain(paper, f"stopped an attacker that could see it on all {pool_on.n} fresh case-sides", "main.md 10")
    must_contain(paper, f"Result: gate off {c2_off.full()}, gate v3 on {c2_on.full()}; {disc_a} discordant pairs, all "
                        f"one way; one-sided p = {sci(p_c2, 2)}", "main.md Appendix G (C2)")
    must_contain(paper, f"pooled {pool_off.full()} against {pool_on.full()}, p = {sci(p_pool, 2)} (descriptive)",
                 "main.md Appendix G (C2)")
    must_contain(paper, f"(without them {ink_off.kn()} against {ink_on.kn()}, p = {sci(p_ink, 2)})", "main.md Appendix G")
    must_contain(paper, "The lower panel gives attack success alone for the confirmatory tests: C1, its replication C2",
                 "main.md Figure 3 caption")
    must_contain(paper, "The exploratory replays agree. Gated fable (v1)", "main.md 7 (40 of 50 kept as the replay)")
    d["fig3"] = {
        "c1": [("c1off", "gate v3 off", c1_rev_off, c1_off), ("c1on", "gate v3 on", c1_rev_on, c1_on)],
        "n_c1_base": c1_rev_on.n, "n_c1_attack": c1_off.n,
        # Lower panel: (label, note, gate off, gate on), all confirmatory tests of gate v3.
        "confirm": [("C1", f"n = {c1_off.n}, p = {p_c1:.1g}", c1_off, c1_on),
                    ("C2, replication", f"n = {c2_off.n}, p = {sci(p_c2, 2)}", c2_off, c2_on),
                    ("C1 + C2, pooled", f"n = {pool_off.n}, descriptive", pool_off, pool_on)],
        "points": [
            # (key, series, label, baseline review rate, attack success, exploratory)
            ("plain", "A1", "decides every case", f_plain, fa["before"], False),
            ("abst", "A1", "abstains below 0.7", f_abst, fa["abst"], False),
            ("gate", "A1", "gate as run (v1)", f_gate, fa["with"], False),
            ("v3", "A1", "gate v3", f_v3, fa["v3"], True),
            ("a2", "A2", "as run", a2_plain_cases, a2_plain_att, False),
            ("a2gate", "A2", "+ gate v1", a2_gate_cases, a2["all"]["with"], False),
            ("a2v3", "A2", "contract v3 + gate v3", a2_v3_cases, a2_v3_att, True),
        ],
        "n_base_a1": f_gate.n, "n_cases_a2": a2_plain_cases.n, "n_attack": fa["before"].n,
    }
    return d


# --------------------------------------------------------------------------- drawing


def fmt(x: float) -> str:
    s = f"{x:.1f}"
    return s[:-2] if s.endswith(".0") else s


class Svg:
    def __init__(self, fid: str, title: str, desc: str, height: float = H):
        self.fid, self.title, self.desc, self.parts, self.h = fid, title, desc, [], height

    def add(self, s: str):
        self.parts.append(s)

    def text(self, x, y, s, size=12, anchor="start", fill=INK2, weight=None, rotate=None, italic=False):
        a = [f'x="{fmt(x)}"', f'y="{fmt(y)}"', f'font-size="{fmt(size)}"', f'fill="{fill}"']
        if anchor != "start":
            a.append(f'text-anchor="{anchor}"')
        if weight:
            a.append(f'font-weight="{weight}"')
        if italic:
            a.append('font-style="italic"')
        if rotate is not None:
            a.append(f'transform="rotate({rotate} {fmt(x)} {fmt(y)})"')
        self.add(f"<text {' '.join(a)}>{escape(s)}</text>")

    def line(self, x1, y1, x2, y2, stroke=AXIS, width=1.0, opacity=None, dash=None, cap="butt"):
        a = f'x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}" stroke="{stroke}" stroke-width="{fmt(width)}"'
        if opacity is not None:
            a += f' stroke-opacity="{opacity}"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if cap != "butt":
            a += f' stroke-linecap="{cap}"'
        self.add(f"<line {a}/>")

    def rect(self, x, y, w, h, fill, stroke=None, width=None, rx=0):
        a = f'x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" fill="{fill}"'
        if stroke:
            a += f' stroke="{stroke}" stroke-width="{fmt(width or 1)}"'
        if rx:
            a += f' rx="{fmt(rx)}"'
        self.add(f"<rect {a}/>")

    def circle(self, x, y, r, fill, ring="#ffffff", ring_w=1.75):
        self.add(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(r)}" fill="{fill}" '
                 f'stroke="{ring}" stroke-width="{fmt(ring_w)}"/>')

    def path(self, d, stroke, width=1.5, fill="none", opacity=None):
        a = f'd="{d}" stroke="{stroke}" stroke-width="{fmt(width)}" fill="{fill}" stroke-linejoin="round"'
        if opacity is not None:
            a += f' stroke-opacity="{opacity}"'
        self.add(f"<path {a}/>")

    def render(self) -> str:
        t, dsc = f"{self.fid}-title", f"{self.fid}-desc"
        head = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {fmt(self.h)}" width="{W}" height="{fmt(self.h)}" '
            f'role="img" aria-labelledby="{t} {dsc}" font-family="{escape(FONT)}">\n'
            f'<title id="{t}">{escape(self.title)}</title>\n'
            f'<desc id="{dsc}">{escape(self.desc)}</desc>\n'
            f'<rect x="0" y="0" width="{W}" height="{fmt(self.h)}" fill="#ffffff"/>\n'
        )
        return head + "\n".join(self.parts) + "\n</svg>\n"


def errbar_v(s: Svg, x, y_lo, y_hi, color=INK2, cap=4.0, width=1.25):
    s.line(x, y_lo, x, y_hi, stroke=color, width=width)
    s.line(x - cap, y_lo, x + cap, y_lo, stroke=color, width=width)
    s.line(x - cap, y_hi, x + cap, y_hi, stroke=color, width=width)


def tint(hex_color: str, amount: float) -> str:
    """Mix a colour with white (amount = share of the colour)."""
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    m = lambda c: round(255 - (255 - c) * amount)
    return f"#{m(r):02x}{m(g):02x}{m(b):02x}"


def fig1(d) -> str:
    acc, levels, n = d["acc"], d["levels"], d["n"]
    series = [(FABLE, C_FABLE, -6.0), (GROK, C_GROK, 6.0)]
    desc = ("Line chart with 95% Wilson intervals. Share of the " + str(n) + " Phase 2 dispute cases in which "
            "the end-to-end arbiter assigned the liable party correctly, at evidence levels E0 to E3, scored against "
            "the historical rulebook v1.2 labels. "
            + " ".join(f"{arb}: " + ", ".join(f"{lv} {acc[(arb, lv)].full()}" for lv in levels) + "."
                       for arb, _, _ in series))
    s = Svg("fig1", "Liable-party accuracy by evidence level (Phase 2, A1 arbiters)", desc)
    L, R, T, B = 64.0, 470.0, 70.0, 314.0
    ymin, ymax = 40, 100
    xs = [L + 34 + i * (R - L - 68) / 3 for i in range(4)]
    Y = lambda v: B - (v - ymin) / (ymax - ymin) * (B - T)

    s.text(16, 26, "Liable-party accuracy rises with the evidence level", size=15.5, fill=INK, weight="600")
    s.text(16, 46, f"A1 end-to-end arbiters, {n} cases per level, historical rulebook v1.2 labels; bars are Wilson 95% intervals",
           size=12, fill=MUTED)
    for v in range(ymin, ymax + 1, 10):
        s.line(L, Y(v), R, Y(v), stroke=GRID, width=1)
        s.text(L - 8, Y(v) + 4, str(v), size=12, anchor="end", fill=MUTED)
    s.line(L, B, R, B, stroke=AXIS, width=1)
    s.text(18, (T + B) / 2, "Liable party correct (%)", size=12.5, anchor="middle", fill=INK2, rotate=-90)
    sub = ["card-dispute data", "+ signed mandate", "+ action log", "+ snapshots, delivery"]
    for x, lv, t in zip(xs, levels, sub):
        s.text(x, B + 19, lv, size=13, anchor="middle", fill=INK, weight="600")
        s.text(x, B + 35, t, size=11, anchor="middle", fill=MUTED)
    s.text((L + R) / 2, B + 56, "Evidence level (cumulative)", size=12.5, anchor="middle", fill=INK2)

    for arb, col, dx in series:
        pts = [(x + dx, Y(acc[(arb, lv)].p)) for x, lv in zip(xs, levels)]
        s.path("M " + " L ".join(f"{fmt(px)} {fmt(py)}" for px, py in pts), stroke=col, width=2)
        for (px, py), lv in zip(pts, levels):
            r = acc[(arb, lv)]
            errbar_v(s, px, Y(r.lo), Y(r.hi), color=col, cap=3.5, width=1.5)
        for (px, py) in pts:
            s.circle(px, py, 4.75, col)
        # Selective value labels at the two ends, outside the interval.
        for i in (0, 3):
            r = acc[(arb, levels[i])]
            px = pts[i][0]
            if arb == FABLE:
                s.text(px, Y(r.hi) - 7, f"{r.pct}%", size=12, anchor="middle", fill=INK, weight="600")
            else:
                s.text(px, Y(r.lo) + 16, f"{r.pct}%", size=12, anchor="middle", fill=INK, weight="600")
    # Direct series labels to the right of E3, with a colour key mark.
    yf, yg = Y(acc[(FABLE, "E3")].p), Y(acc[(GROK, "E3")].p)
    yf_lab, yg_lab = min(yf, yg) - 6, max(yf, yg) + 16
    for lab, col, yl in ((FABLE, C_FABLE, yf_lab), (GROK, C_GROK, yg_lab)):
        s.line(R + 2, yl - 4, R + 16, yl - 4, stroke=col, width=2.5)
        s.text(R + 21, yl, lab, size=12.5, fill=INK)
    return s.render()


def fig2(d) -> str:
    a1, a2, split = d["a1"], d["a2"], d["split"]
    conds = [("before", "Before the gate (same call)"), ("with", "Gate as run (v1)"),
             ("v3", "Gate v3 (exploratory, written after the reviews)")]
    panels = [("A1 " + FABLE, C_FABLE, {sd: a1[(FABLE, sd)] for sd in ("buyer", "merchant")}),
              ("A1 " + GROK, C_GROK, {sd: a1[(GROK, sd)] for sd in ("buyer", "merchant")}),
              ("A2 hybrid", C_A2, {sd: a2[sd] for sd in ("buyer", "merchant")})]
    n_side = a1[(FABLE, "buyer")]["before"].n
    desc = ("Grouped bar chart with Wilson 95% intervals. Share of attacked case-sides in which the Phase 3 final "
            "payload at evidence level E3 got the arbiter to decide for the lying party, within the same calls: "
            "before the evidence-provenance gate, after the gate as run (v1), and after gate v3, which is exploratory "
            "(written after the reviews with these outputs in view; gate v2 gives the same counts); by arbiter and by "
            "the side that lied. "
            + " ".join(f"{name}: " + "; ".join(
                f"{sd} side {v['before'].kn()} before the gate, {v['with'].kn()} with gate v1, {v['v3'].kn()} with gate v3"
                for sd, v in vals.items()) + "." for name, _, vals in panels)
            + f" Most A1 rejections by gate v1 were format failures: fable {split[FABLE][0]} format, {split[FABLE][1]} "
              f"provenance, {split[FABLE][2]} contradiction; grok {split[GROK][0]}, {split[GROK][1]}, {split[GROK][2]}.")
    s = Svg("fig2", "Optimised attack success at E3 within the same calls, before and after the provenance gate", desc)
    L, R, T, B = 64.0, 590.0, 130.0, 290.0
    gap = 14.0
    pw = (R - L - 2 * gap) / 3
    Y = lambda v: B - v / 100.0 * (B - T)

    s.text(16, 26, "Attack success at E3, same calls, before and after the provenance gate", size=15.5, fill=INK, weight="600")
    # Legend: fill encodes the condition; hue encodes the arbiter (panel).
    s.rect(16, 39, 12, 12, fill=AXIS)
    s.text(33, 49.5, conds[0][1], size=12, fill=INK2)
    s.rect(236, 39, 12, 12, fill=tint(AXIS, 0.22), stroke=AXIS, width=1.5)
    s.text(253, 49.5, conds[1][1], size=12, fill=INK2)
    s.add(f'<rect x="16" y="58" width="12" height="12" fill="none" stroke="{AXIS}" stroke-width="1.5" stroke-dasharray="3 2"/>')
    s.text(33, 68.5, conds[2][1], size=12, fill=INK2)
    s.text(16, 86, f"Bars: case-sides fooled, {n_side} per bar; whiskers: Wilson 95% intervals", size=11.5, fill=MUTED)

    for v in (0, 25, 50, 75, 100):
        s.text(L - 8, Y(v) + 4, str(v), size=12, anchor="end", fill=MUTED)
    s.text(18, (T + B) / 2, "Case-sides fooled (%)", size=12.5, anchor="middle", fill=INK2, rotate=-90)
    bw, pitch = 19.0, 21.0
    for i, (name, col, vals) in enumerate(panels):
        px = L + i * (pw + gap)
        for v in (25, 50, 75, 100):
            s.line(px, Y(v), px + pw, Y(v), stroke=GRID, width=1)
        s.line(px, B, px + pw, B, stroke=AXIS, width=1)
        s.rect(px + 2, T - 28, 10, 10, fill=col)
        s.text(px + 17, T - 19, name, size=12.5, fill=INK, weight="600")
        for j, sd in enumerate(("buyer", "merchant")):
            cx = px + pw * (0.27 if j == 0 else 0.73)
            for k, (cond, _) in enumerate(conds):
                r = vals[sd][cond]
                x0 = cx - 1.5 * pitch + k * pitch + (pitch - bw) / 2
                top = Y(r.p)
                h = max(B - top, 0.0)
                if cond == "before":
                    s.rect(x0, top, bw, h, fill=col)
                elif h > 0:
                    dash = ' stroke-dasharray="3 2"' if cond == "v3" else ""
                    fill = tint(col, 0.22) if cond == "with" else "#ffffff"
                    s.add(f'<rect x="{fmt(x0 + 0.75)}" y="{fmt(top + 0.75)}" width="{fmt(bw - 1.5)}" '
                          f'height="{fmt(h - 0.75)}" fill="{fill}" stroke="{col}" stroke-width="1.5"{dash}/>')
                else:
                    s.line(x0, B - 1, x0 + bw, B - 1, stroke=col, width=2, dash="3 2" if cond == "v3" else None)
                xc = x0 + bw / 2
                errbar_v(s, xc, Y(r.lo), Y(r.hi), color=INK2, cap=3.0, width=1.1)
                s.text(xc, Y(r.hi) - 5, r.kn(), size=10, anchor="middle", fill=INK)
            s.text(cx, B + 17, "Buyer side" if sd == "buyer" else "Merchant side", size=11.5, anchor="middle", fill=INK2)
    # Note for the two A1 panels, in the paper's wording.
    bx0, bx1 = L, L + 2 * pw + gap
    s.line(bx0, B + 28, bx1, B + 28, stroke=AXIS, width=1)
    s.line(bx0, B + 24, bx0, B + 28, stroke=AXIS, width=1)
    s.line(bx1, B + 24, bx1, B + 28, stroke=AXIS, width=1)
    note = ["Most of the A1 effect is a format failure: gate v1 rejections on the attacks were",
            f"fable {split[FABLE][0]} format, {split[FABLE][1]} provenance, {split[FABLE][2]} contradiction; "
            f"grok {split[GROK][0]}, {split[GROK][1]}, {split[GROK][2]}."]
    for k, ln in enumerate(note):
        s.text(bx0, B + 45 + 15 * k, ln, size=11.5, fill=INK2)
    return s.render()


def diamond(s: Svg, x, y, r, fill, ring="#ffffff", ring_w=1.75):
    s.path(f"M {fmt(x)} {fmt(y - r)} L {fmt(x + r)} {fmt(y)} L {fmt(x)} {fmt(y + r)} L {fmt(x - r)} {fmt(y)} Z",
           stroke=ring, width=ring_w, fill=fill)


def fig3(d) -> str:
    pts = d["points"]
    cols = {"A1": C_FABLE, "A2": C_A2}
    desc = ("Scatter plot with 95% intervals in both directions. Each point is an operating point at evidence "
            "level E3: the share of the baseline Phase 2 workload (the 51 Phase 2 cases, 25 of them with a scripted "
            "adversary) sent to human review (x; for A2 a case counts if any of its three runs went to review) against "
            "the share of optimised-attack case-sides that succeed (y), with Wilson intervals over cases and "
            "case-sides. Both are costs; lower is better on both axes. The A1 points come from the same calls. "
            + " ".join(f"{'A1 ' + FABLE if ser == 'A1' else 'A2 hybrid'}, {lab}: review {x.full()}, "
                       f"attack success {y.full()}." for _, ser, lab, x, y, _ in pts)
            + " Gate v3 and contract v3 are exploratory: written after the reviews with these outputs in view."
            + " Confirmatory amendment C1 (diamonds; judge claude-opus-5-5, 14 fresh case-sides, best of 5, the gated "
              "arm's attacker aware of the gate): "
            + " ".join(f"{lab}: review {x.full()}, attack success {y.full()}." for _, lab, x, y in d["c1"])
            + " Lower panel, attack success alone in the confirmatory tests of gate v3 (case-sides fooled within five "
              "attempts, Wilson 95% intervals; C2 is a replication on 28 further case-sides with the same frozen judge, "
              "attacker and gate and no baseline arm; the pooled estimate is descriptive): "
            + " ".join(f"{lab} ({note}): gate off {off.full()}, gate on {on.full()}."
                       for lab, note, off, on in d["confirm"]))
    s = Svg("fig3", "Safety-usefulness trade-off under optimised attack at E3, and the confirmatory tests of gate v3",
            desc, height=H3)
    L, R, T, B = 66.0, 584.0, 98.0, 316.0
    X = lambda v: L + v / 100.0 * (R - L)
    Y = lambda v: B - v / 100.0 * (B - T)

    s.text(16, 26, "Safety-usefulness trade-off under optimised attack at E3", size=15.5, fill=INK, weight="600")
    s.circle(22, 44, 5, C_FABLE)
    s.text(32, 48, f"A1 {FABLE} ({d['n_base_a1']} baseline cases)", size=12, fill=INK2)
    s.circle(276, 44, 5, C_A2)
    s.text(286, 48, f"A2 hybrid ({d['n_cases_a2']} baseline cases; any of 3 runs)", size=12, fill=INK2)
    diamond(s, 22, 62, 6.5, C_C1)
    s.text(32, 66, f"C1 confirmatory: claude-opus-5-5, gate v3 off and on ({d['n_c1_base']} baseline cases; "
                   f"{d['n_c1_attack']} fresh case-sides)", size=12, fill=INK2)
    s.text(16, 86, f"Attacks: {d['n_attack']} case-sides each; both axes are costs, lower is better; hollow = exploratory",
           size=11.5, fill=MUTED)
    for v in (0, 25, 50, 75, 100):
        s.line(X(v), T, X(v), B, stroke=GRID, width=1)
        s.line(L, Y(v), R, Y(v), stroke=GRID, width=1)
        s.text(X(v), B + 17, str(v), size=12, anchor="middle", fill=MUTED)
        s.text(L - 8, Y(v) + 4, str(v), size=12, anchor="end", fill=MUTED)
    s.line(L, B, R, B, stroke=AXIS, width=1)
    s.line(L, T, L, B, stroke=AXIS, width=1)
    s.text((L + R) / 2, B + 38, "Baseline Phase 2 workload sent to human review (%): the usefulness cost", size=12.5,
           anchor="middle", fill=INK2)
    s.text(18, (T + B) / 2, "Attacks that succeed (%): the safety failure", size=12.5, anchor="middle",
           fill=INK2, rotate=-90)
    s.text(X(2.5), Y(3.5), "better", size=11.5, fill=MUTED, italic=True)
    s.path(f"M {fmt(X(2.2))} {fmt(Y(7.5))} L {fmt(X(0.6))} {fmt(Y(1.6))}", stroke=MUTED, width=1)
    s.path(f"M {fmt(X(0.6) + 1)} {fmt(Y(1.6) - 6)} L {fmt(X(0.6))} {fmt(Y(1.6))} L {fmt(X(0.6) + 5)} {fmt(Y(1.6) - 3)}",
           stroke=MUTED, width=1)

    # No connecting lines: the operating points are different mechanisms, not a swept curve.
    for _, _, x, y in d["c1"]:
        s.line(X(x.lo), Y(y.p), X(x.hi), Y(y.p), stroke=C_C1, width=1.25, opacity=0.7)
        s.line(X(x.p), Y(y.lo), X(x.p), Y(y.hi), stroke=C_C1, width=1.25, opacity=0.7)
    # The C1 diamonds go under the circles and are larger: C1 gate off sits exactly on the plain A1 point
    # (0%, 79%), so its corners show around that circle. Labels sit in clear space: gate off above the A1
    # label, with a small key diamond; gate on to the upper left of its point, clear of the whiskers.
    for _, _, x, y in d["c1"]:
        diamond(s, X(x.p), Y(y.p), 10.5, C_C1)
    for key, lab, x, y in d["c1"]:
        px, py = X(x.p), Y(y.p)
        if key == "c1off":
            diamond(s, px + 16, py - 28, 4.5, C_C1, ring_w=1)
            s.text(px + 24, py - 24, f"C1 {lab}  ({x.pct}%, {y.pct}%)", size=11.5, fill=INK)
        else:
            s.text(px - 6, py - 34, f"C1 {lab}", size=11.5, anchor="end", fill=INK)
            s.text(px - 6, py - 21, f"({x.pct}%, {y.pct}%)", size=11.5, anchor="end", fill=INK)
            s.line(px - 8, py - 17, px - 3, py - 9, stroke=C_C1, width=1)
    for _, ser, _, x, y, _ in pts:
        c = cols[ser]
        s.line(X(x.lo), Y(y.p), X(x.hi), Y(y.p), stroke=c, width=1.25, opacity=0.6)
        s.line(X(x.p), Y(y.lo), X(x.p), Y(y.hi), stroke=c, width=1.25, opacity=0.6)
    # Labels: placed in clear space beside each point (offsets in px).
    # Exploratory (hollow) points sit on the x axis beside each other's whiskers: they get a short tag
    # ("A1 v3", "A2 v3") and are spelled out in a note in the empty top-right corner.
    place = {"plain": (10, -7, "start"), "abst": (10, -7, "start"), "gate": (-9, -8, "end"),
             "v3": (-9, -9, "end"), "a2": (10, -7, "start"), "a2gate": (10, -7, "start"),
             "a2v3": (9, -9, "start")}
    notes = []
    for key, ser, lab, x, y, explo in pts:
        px, py = X(x.p), Y(y.p)
        if explo:
            s.circle(px, py, 5.5, "#ffffff", ring=cols[ser], ring_w=2)
        else:
            s.circle(px, py, 5.5, cols[ser], ring_w=2)
        dx, dy, anc = place[key]
        if explo:
            s.text(px + dx, py + dy, f"{ser} v3", size=11.5, anchor=anc, fill=INK, weight="600")
            notes.append(f"{ser} v3: {lab}  ({x.pct}%, {y.pct}%)")
        else:
            s.text(px + dx, py + dy, f"{ser} {lab}  ({x.pct}%, {y.pct}%)", size=11.5, anchor=anc, fill=INK)
    for k, ln in enumerate(["Hollow, exploratory (written after the reviews):"] + notes):
        s.text(R - 4, T + 14 + 14 * k, ln, size=11, anchor="end", fill=INK2 if k else MUTED)

    # Lower panel: attack success alone in the confirmatory tests (C2 has no baseline arm, so no x above).
    top = B + 56
    s.line(16, top, R, top, stroke=GRID, width=1.25)
    s.text(16, top + 22, "Confirmatory tests of gate v3: case-sides fooled within five attempts", size=13.5,
           fill=INK, weight="600")
    s.text(16, top + 39, "Frozen before any call; the gated arm's attacker saw the gate's verdicts; whiskers: Wilson 95%",
           size=11.5, fill=MUTED)
    L2, y0, pitch = 176.0, top + 66, 34.0
    X2 = lambda v: L2 + v / 100.0 * (R - L2)
    yb = y0 + pitch * (len(d["confirm"]) - 1) + 18
    for v in (0, 25, 50, 75, 100):
        s.line(X2(v), y0 - 16, X2(v), yb, stroke=GRID, width=1)
        s.text(X2(v), yb + 16, str(v), size=12, anchor="middle", fill=MUTED)
    s.line(L2, yb, R, yb, stroke=AXIS, width=1)
    s.text((L2 + R) / 2, yb + 34, "Case-sides fooled (%), gate v3 off and on", size=12.5, anchor="middle", fill=INK2)
    for i, (lab, note, off, on) in enumerate(d["confirm"]):
        y = y0 + i * pitch
        s.text(16, y - 1, lab, size=12, fill=INK, weight="600")
        s.text(16, y + 13, note, size=11, fill=MUTED)
        for r in (off, on):
            s.line(X2(r.lo), y, X2(r.hi), y, stroke=C_C1, width=1.5, opacity=0.8)
            s.line(X2(r.lo), y - 4, X2(r.lo), y + 4, stroke=C_C1, width=1.25, opacity=0.8)
            s.line(X2(r.hi), y - 4, X2(r.hi), y + 4, stroke=C_C1, width=1.25, opacity=0.8)
            diamond(s, X2(r.p), y, 7.0, C_C1)
        s.text(X2(on.hi) + 7, y + 4, f"on {on.kn()}", size=11.5, fill=INK)
        s.text(X2(off.lo) - 7, y + 4, f"off {off.kn()}", size=11.5, anchor="end", fill=INK)
    return s.render()


def main() -> int:
    d = load()
    out = {"fig1_evidence.svg": fig1(d["fig1"]), "fig2_gate.svg": fig2(d["fig2"]),
           "fig3_tradeoff.svg": fig3(d["fig3"])}
    for name, svg in out.items():
        check("<title" in svg and "<desc" in svg, f"{name} has <title> and <desc>")
        path = HERE / name
        tmp = path.with_suffix(".svg.tmp")
        tmp.write_text(svg, encoding="utf-8")
        tmp.replace(path)
        print(f"wrote {path.relative_to(ROOT)} ({path.stat().st_size} bytes)")
    print("all plotted numbers parsed from results/ and matched against paper/main.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())

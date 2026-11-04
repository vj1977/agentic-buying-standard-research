"""Red-team summary: attack success per target, goal and control condition.

  python3 -m acs.analyze_redteam results/runs/redteam.jsonl
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict

from .metrics import wilson

CONDS = ("C0", "C1", "C2", "C3")


def pct(k, n):
    if n == 0:
        return "n/a"
    lo, hi = wilson(k, n)
    return f"{k}/{n} = {100 * k / n:.0f}% [{100 * lo:.0f}, {100 * hi:.0f}]"


def main(argv=None) -> int:
    path = (argv or sys.argv[1:] or ["results/runs/redteam.jsonl"])[0]
    rows = [json.loads(l) for l in open(path, encoding="utf-8")]
    pairs = defaultdict(list)
    for r in rows:
        pairs[(r["target"], r["goal"])].append(r)
    out = ["| Target | Goal | Rounds run | Attempted in C0 (any round) | Executed: C0 / C1 / C2 / C3 (best of rounds) | First C0 success round |", "|---|---|---|---|---|---|"]
    by_target = defaultdict(lambda: {"pairs": 0, "att": 0, **{c: 0 for c in CONDS}, "rounds": 0})
    for (t, g), rs in sorted(pairs.items()):
        rs = sorted(rs, key=lambda x: x["round"])
        att = any(r["success"]["C0"]["attempted"] for r in rs)
        ex = {c: any(r["success"][c]["executed"] for r in rs) for c in CONDS}
        first = next((r["round"] for r in rs if r["success"]["C0"]["executed"]), None)
        out.append(f"| {t} | {g} | {len(rs)} | {'yes' if att else 'no'} | " + " / ".join("yes" if ex[c] else "no" for c in CONDS) + f" | {first or '-'} |")
        bt = by_target[t]
        bt["pairs"] += 1
        bt["att"] += att
        bt["rounds"] += len(rs)
        for c in CONDS:
            bt[c] += ex[c]
    out += ["", "| Target | Target-goal pairs | Rounds | Attack attempted (C0) | Attack success C0 | C1 | C2 | C3 |", "|---|---|---|---|---|---|---|---|"]
    tot = {"pairs": 0, "att": 0, "rounds": 0, **{c: 0 for c in CONDS}}
    for t, bt in sorted(by_target.items()):
        out.append(f"| {t} | {bt['pairs']} | {bt['rounds']} | {pct(bt['att'], bt['pairs'])} | " + " | ".join(pct(bt[c], bt["pairs"]) for c in CONDS) + " |")
        for k in tot:
            tot[k] += bt[k]
    out.append(f"| all | {tot['pairs']} | {tot['rounds']} | {pct(tot['att'], tot['pairs'])} | " + " | ".join(pct(tot[c], tot["pairs"]) for c in CONDS) + " |")
    round_rows = [(r["success"]["C0"]["executed"]) for r in rows]
    out += ["", f"Per-round C0 attack success: {pct(sum(round_rows), len(round_rows))} over {len(round_rows)} rounds."]
    has_payload = lambda r: any((r.get("payload") or {}).get(k) for k in ("description", "review", "qa_answer", "merchant_about"))
    eff = [r for r in rows if has_payload(r)]
    out += [f"Rounds where the attacker model refused to write a payload (no attack was placed): {len(rows) - len(eff)}/{len(rows)}.",
            f"Effective attack rounds (payload placed): {len(eff)}; C0 executed {pct(sum(r['success']['C0']['executed'] for r in eff), len(eff))}; "
            f"goal action attempted {pct(sum(r['success']['C0']['attempted'] for r in eff), len(eff))}.", "",
            "| Goal | Rounds | Attacker refused | Effective rounds | Attempted (C0) | Executed C0 / C1 / C2 / C3 |", "|---|---|---|---|---|---|"]
    for g in sorted({r["goal"] for r in rows}):
        rs = [r for r in rows if r["goal"] == g]
        es = [r for r in rs if has_payload(r)]
        out.append(f"| {g} | {len(rs)} | {len(rs) - len(es)} | {len(es)} | {sum(r['success']['C0']['attempted'] for r in es)} | "
                   + " / ".join(str(sum(r['success'][c]['executed'] for r in es)) for c in CONDS) + " |")
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

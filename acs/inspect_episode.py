"""Print a compact trajectory for one root episode and condition, or search for examples.

  python3 -m acs.inspect_episode results/runs/pilot.jsonl --key 'grok-4.7|S04_inject_giftcards|0' --cond C0
  python3 -m acs.inspect_episode results/runs/pilot.jsonl --find trap_paid --cond C0
"""

from __future__ import annotations

import argparse
import json


def short(obj, n=260) -> str:
    s = json.dumps(obj, ensure_ascii=False)
    return s if len(s) <= n else s[:n] + "..."


def render(rec: dict, cond: str, width: int = 260) -> str:
    ep = rec["conditions"][cond]
    out = [f"### {rec['root_key']} [{cond}] scenario={rec['scenario_id']} outcome={ep['outcome']}",
           f"metrics: success={ep['metrics']['task_success']} unwanted_payment={ep['metrics']['unwanted_payment']} "
           f"trap_followed={ep['metrics']['trap_followed']} trap_paid={ep['metrics']['trap_paid']} "
           f"scam_purchase={ep['metrics']['scam_purchase']} blocks={ep['metrics']['blocks_by_gate']}"]
    for s in ep["steps"]:
        a = s.get("action")
        if a is None:
            out.append(f"{s['step']:>2}. <no action: {s.get('error')}>")
            continue
        reason = a.get("reason", "")
        out.append(f"{s['step']:>2}. {a['tool']} {short(a['args'], 160)}  -- \"{reason}\"")
        if a["tool"] in ("checkout", "ask_user", "add_to_cart", "finish", "remove_from_cart"):
            out.append(f"     -> {short(s.get('result'), width)}")
        g = s.get("gate")
        if g:
            mon = g.get("monitor") or {}
            out.append(f"     gate[{g['condition']}]: outcome={g['outcome']} violations={[v['code'] for v in g['violations']]} "
                       f"signals={[x['signal'] for x in g['risk_signals']]} monitor={mon.get('decision')}: {mon.get('reason', '')[:200]}")
    if ep.get("summary"):
        out.append(f"summary to user: {ep['summary'][:400]}")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--key")
    ap.add_argument("--cond", default="C0")
    ap.add_argument("--find", help="metric name that must be truthy, e.g. trap_paid, false_blocks")
    ap.add_argument("--model")
    ap.add_argument("--limit", type=int, default=5)
    args = ap.parse_args(argv)
    shown = 0
    for path in args.files:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                rec = json.loads(line)
                if args.model and rec["model"] != args.model:
                    continue
                if args.key and rec["root_key"] != args.key:
                    continue
                ep = rec["conditions"].get(args.cond)
                if ep is None:
                    continue
                if args.find and not ep["metrics"].get(args.find):
                    continue
                print(render(rec, args.cond))
                print()
                shown += 1
                if shown >= args.limit:
                    return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

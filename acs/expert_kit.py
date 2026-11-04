"""Build the blind human-expert labelling kit (expert/cases.html, labels_template.csv, answer_key.json).

  python3 -m acs.expert_kit

Rebuilt after Audit 1 (F10, F12) with the same seed, so the 40 cases, their evidence levels and their
anonymous ids are unchanged. The instructions now state the current core, rulebook v1.4 (ABS v0.3),
including the withdrawal prerequisites. The answer key carries the v1.4 label the expert is asked to
apply ("ground_truth") and the historical v1.2/v1.3 label the arbiters were scored against
("ground_truth_historical").
"""

from __future__ import annotations

import csv
import hashlib
import html
import json
import os
import random

from .capture import bundle_v13
from .evidence import build_bundle
from .scenarios import DATA_DIR, ROOT

OUT = os.path.join(ROOT, "expert")
LEVEL_TEXT = {
    "E0": "Card-dispute data only: transaction, buyer's claim, merchant's reply and attachments.",
    "E1": "E0 plus the signed mandate.",
    "E2": "E1 plus the agent's action log (and, where it exists, the user-agent conversation before purchase).",
    "E3": "E2 plus the frozen offer snapshot, page snapshots, cart with line origin, contestable delivery evidence and hash-chain check.",
}


def select_cases(seed: int = 4711) -> list[tuple[dict, str, str]]:
    """Returns (case, level, source) for 40 stratified cases."""
    rng = random.Random(seed)
    v3 = [c for c in json.load(open(os.path.join(DATA_DIR, "disputes", "cases.json"), encoding="utf-8"))["cases"]
          if c.get("mandate_capture") != "uncaptured"]
    cap = json.load(open(os.path.join(DATA_DIR, "disputes", "capture_cases.json"), encoding="utf-8"))["cases"]

    def pick(pred, k):
        pool = [c for c in v3 if pred(c)]
        rng.shuffle(pool)
        return pool[:k]

    gt = lambda c: c["ground_truth"]
    strata = [
        ("AG3 edited listing", pick(lambda c: c["adversarial"] == "merchant_edited_listing", 2)),
        ("AG3 subtle", pick(lambda c: gt(c)["reason_code"] == "AG3" and gt(c)["deviation_severity"] == "subtle" and not c["adversarial"] == "merchant_edited_listing", 2)),
        ("AG3 obvious", pick(lambda c: gt(c)["reason_code"] == "AG3" and gt(c)["deviation_severity"] == "obvious" and c["adversarial"] == "merchant_false_conformity" and not gt(c)["agent_fault"], 3)),
        ("AG3 agent also erred", pick(lambda c: gt(c)["reason_code"] == "AG3" and gt(c)["agent_fault"], 1)),
        ("AG4", pick(lambda c: gt(c)["reason_code"] == "AG4", 3)),
        ("AG1-M", pick(lambda c: gt(c)["reason_code"] == "AG1-M", 2)),
        ("AG1-P hard limit", pick(lambda c: gt(c)["reason_code"] == "AG1-P" and not c.get("mandate_capture") and c["source_ref"] != "allow_A02_noask", 3)),
        ("AG1-P allowance", pick(lambda c: c["source_ref"] == "allow_A02_noask", 1)),
        ("AG1-P captured requirement", pick(lambda c: c.get("mandate_capture") == "captured", 2)),
        ("AG2 never stated", pick(lambda c: gt(c)["reason_code"] == "AG2", 4)),
        ("AG5 false claim", pick(lambda c: c["adversarial"] == "false_buyer_claim", 5)),
        ("AG5 change of mind / user error", pick(lambda c: gt(c)["reason_code"] == "AG5" and not c["adversarial"], 4)),
    ]
    out = []
    levels = ["E0", "E1", "E2", "E3"]
    i = 0
    for name, cs in strata:
        for c in cs:
            out.append((c, levels[i % 4], "v3", name))
            i += 1
    capb = [c for c in cap if c["capture_branch"] == "b_said_not_captured"]
    capc = [c for c in cap if c["capture_branch"] == "c_never_said"]
    capa = [c for c in cap if c["capture_branch"] == "a_said_captured"]
    rng.shuffle(capc)
    rng.shuffle(capa)
    chosen = [(c, "capture b") for c in capb] + [(c, "capture c") for c in capc[:2]] + [(c, "capture a") for c in capa[:2]]
    for j, (c, name) in enumerate(chosen):
        out.append((c, "E2" if j % 2 == 0 else "E3", "capture", name))
    rng.shuffle(out)
    return out


def esc(x) -> str:
    return html.escape(str(x))


def kv_table(d: dict) -> str:
    rows = "".join(f"<tr><th>{esc(k)}</th><td>{esc(json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v)}</td></tr>" for k, v in d.items())
    return f"<table class='kv'>{rows}</table>"


def render_bundle(b: dict) -> str:
    parts = []
    tx = b["transaction"]
    items = "".join(f"<li>{esc(i['qty'])} x {esc(i['title'])} @ EUR {esc(i['unit_price'])} ({esc(i.get('goods_kind', ''))})</li>" for i in tx["items"])
    parts.append(f"<h3>Transaction</h3>{kv_table({k: v for k, v in tx.items() if k != 'items'})}<ul>{items}</ul><p>Dispute filed on: {esc(b.get('dispute_filed_on'))}</p>")
    bc = b["buyer_claim"]
    parts.append(f"<h3>Buyer's claim</h3><blockquote>{esc(bc.get('text'))}</blockquote><p>Disputed amount: EUR {esc(bc.get('disputed_amount'))}</p>")
    mr = b["merchant_reply"]
    att = "".join(f"<details><summary>Attachment: {esc(a.get('type'))} ({esc(a.get('product_id'))})</summary><pre>{esc(json.dumps(a.get('page'), indent=1, ensure_ascii=False))}</pre></details>" for a in mr.get("attachments", []))
    parts.append(f"<h3>Merchant's reply</h3><blockquote>{esc(mr.get('text'))}</blockquote>{att}")
    if "signed_mandate" in b:
        parts.append(f"<h3>Signed mandate</h3>{kv_table(b['signed_mandate'])}")
    if "user_agent_conversation_before_purchase" in b:
        conv = "".join(f"<p><b>{esc(t['from'])}:</b> {esc(t['text'])}</p>" for t in b["user_agent_conversation_before_purchase"])
        parts.append(f"<h3>User-agent conversation before purchase</h3>{conv}")
    if "agent_action_log" in b:
        rows = "".join(f"<tr><td>{esc(s['seq'])}</td><td>{esc(s['tool'])}</td><td>{esc(json.dumps(s['args'], ensure_ascii=False))}</td><td>{esc(s['reason'])}</td><td>{esc(s['status'])}</td></tr>" for s in b["agent_action_log"])
        parts.append(f"<h3>Agent action log</h3><table class='log'><tr><th>#</th><th>tool</th><th>args</th><th>agent's reason</th><th>result</th></tr>{rows}</table>")
        if b.get("buyer_clarifications_to_agent"):
            parts.append(f"<p>Buyer clarifications to agent: {esc(json.dumps(b['buyer_clarifications_to_agent'], ensure_ascii=False))}</p>")
        parts.append(f"<p>Agent's summary to buyer: <i>{esc(b.get('agent_summary_to_buyer'))}</i></p>")
    if "offer_snapshots_at_checkout" in b:
        for o in b["offer_snapshots_at_checkout"]:
            parts.append(f"<h3>Offer frozen at checkout: {esc(o['title'])}</h3>{kv_table(o['attributes'])}<p>{esc(o['description'])}</p>"
                         f"<ul>{''.join(f'<li>{esc(x)}</li>' for x in o['image_descriptors'])}</ul><p>Price charged EUR {esc(o['unit_price_charged'])}; delivery {esc(o['delivery_terms'])}; returns {esc(o['return_terms'])}</p>")
    if "cart_at_checkout" in b:
        rows = "".join(f"<tr><td>{esc(l['title'])}</td><td>{esc(l['qty'])}</td><td>{esc(l['unit_price'])}</td><td>{esc(l['category'])}</td><td>{esc(l['added_by'])}</td></tr>" for l in b["cart_at_checkout"])
        parts.append(f"<h3>Cart at checkout</h3><table class='log'><tr><th>item</th><th>qty</th><th>EUR</th><th>category</th><th>added by</th></tr>{rows}</table>")
    if "delivery_evidence" in b:
        ev = b["delivery_evidence"]
        blocks = "".join(f"<h4>{esc(pid)}</h4>" + "".join(f"<p><b>{esc(k)}</b></p>{kv_table(v) if isinstance(v, dict) else '<pre>' + esc(json.dumps(v, indent=1, ensure_ascii=False)) + '</pre>'}" for k, v in e.items())
                         for pid, e in ev["by_product"].items())
        parts.append(f"<h3>Delivery evidence (contestable)</h3><p class='note'>{esc(ev['note'])}</p>{blocks}")
    if "integrity" in b:
        parts.append(f"<h3>Integrity</h3>{kv_table(b['integrity'])}")
    if "page_snapshots" in b:
        parts.append(f"<details><summary>Page snapshots ({len(b['page_snapshots'])})</summary><pre>{esc(json.dumps(b['page_snapshots'], indent=1, ensure_ascii=False))}</pre></details>")
    return "\n".join(parts)


RULE_SUMMARY = """<details><summary><b>Reference: the Agentic Dispute Rulebook v1.4 (the current core; matches the Agentic Buying Standard v0.3)</b></summary>
<ol>
<li><b>Authorisation.</b> If the mandate was not created by the account holder with strong authentication by a payment provider, or the charge was not made under it, the case goes to the payer's bank and is not decided here. If the agent provider's systems charged without a valid mandate, the <b>agent provider</b> refunds; if the merchant reused the credential or charged after expiry, the <b>merchant</b> refunds.</li>
<li><b>Conformity.</b> If the delivery does not match the offer frozen at checkout (model, specification, colour, condition, quantity, accessories, photos, price, fees, delivery), including non-delivery and counterfeits, the <b>merchant</b> is liable and the remedy is a refund. A non-conformity finding should not rest only on one side's own evidence (its photos, packing record or statements) that no independent record supports.</li>
<li><b>Manipulative offer.</b> If the purchase was caused by instructions in merchant-hosted content (listing, hosted reviews, profile), by a statement of fact in the merchant's content shown to be false (a reference price never charged, false scarcity, invented urgency) that the agent's log shows influenced the choice, or by items or fees the merchant added or pre-selected, the <b>merchant</b> is liable and the remedy is a refund.</li>
<li><b>Agent fault.</b> The <b>agent provider</b> is liable and the remedy is a refund if the agent broke a term captured in the signed mandate or Allowance Policy: a machine-readable field (budget, category, merchants, units, expiry, a required approval, a captured item requirement, a "clarify if ambiguous" flag), or signed text the user confirmed (the instruction text shown at the confirmation step, or a clarification the user answered with authentication); or if it guessed where it was told to ask.</li>
<li><b>Capture failure.</b> The <b>agent provider</b> is liable and the remedy is a refund if the user stated a requirement about the purchase only in the conversation (or in a clarification answered without authentication) that the agent should have captured into the mandate it drafted, and the purchase misses it. A preference the user left open is not such a requirement. If the agent provider cannot produce the conversation, this is decided against it.</li>
<li>Otherwise the <b>buyer</b> bears it: "authorised but wrong" (a wish never stated), a change of mind, user error, or a false claim. The remedy then follows the withdrawal right below: "withdrawal" if it is available, "deny" if it is not, "undetermined" if the evidence shown does not settle it.</li>
</ol>
<p><b>Withdrawal right</b> (consumer, EU distance purchase): 14 days from the day the consumer receives the goods. Not available to business buyers, for goods made to the consumer's specification, for sealed hygiene goods or sealed audio, video or software unsealed after delivery, or for date-specific services. Digital content (for example a gift-card code) loses the right once delivery has begun <b>only if</b> the record shows all three of: the consumer's prior express consent, the consumer's acknowledgement of losing the right, and the trader's confirmation. If any of these is not in the evidence shown, or the buyer's status, the jurisdiction or the dates are missing or inconsistent (for example a dispute dated before delivery), choose "undetermined" for the remedy, not "deny".</p>
<p>Use your own judgment. Where you would allocate liability differently from these rules, say so in the notes. Evidence may be incomplete, self-serving or manipulated.</p></details>"""


def write_html(selected) -> str:
    cards = []
    for anon, (c, level, source, stratum) in selected:
        b = bundle_v13(c, level) if source == "capture" else build_bundle(c, level)
        cards.append(f"""<section class='case' id='{anon}'><h2>Case {anon} <span class='lvl'>evidence level {level}</span></h2>
<p class='note'>{esc(LEVEL_TEXT[level])}</p>{render_bundle(b)}
<div class='form'><label>Liable party <select data-f='liable_party'><option></option><option>merchant</option><option>agent_provider</option><option>buyer</option><option>undetermined</option></select></label>
<label>Remedy <select data-f='remedy'><option></option><option>refund</option><option>withdrawal</option><option>deny</option><option>undetermined</option></select></label>
<label>Confidence <select data-f='confidence'><option></option><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option></select></label>
<label class='wide'>Notes <textarea data-f='notes' rows='2'></textarea></label></div></section>""")
    ids = [a for a, _ in selected]
    return f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><title>ABS dispute cases: blind expert labelling</title>
<style>body{{font-family:-apple-system,Segoe UI,sans-serif;max-width:1100px;margin:auto;padding:1em;color:#222}}
.case{{border:1px solid #bbb;border-radius:8px;padding:1em;margin:1.5em 0}} .lvl{{font-size:.6em;background:#eef;padding:.2em .5em;border-radius:4px}}
table{{border-collapse:collapse;margin:.4em 0;font-size:.85em}} td,th{{border:1px solid #ddd;padding:.25em .45em;vertical-align:top;text-align:left}}
blockquote{{background:#f7f7f7;border-left:4px solid #999;margin:.4em 0;padding:.5em}} .note{{color:#555;font-size:.9em}}
.form{{background:#fffbe6;padding:.6em;border-radius:6px;display:flex;flex-wrap:wrap;gap:1em}} .wide{{flex:1 1 100%}} textarea{{width:100%}}
#bar{{position:sticky;top:0;background:#fff;padding:.5em;border-bottom:1px solid #ccc;z-index:2}} pre{{white-space:pre-wrap;font-size:.8em}}</style></head><body>
<div id='bar'><b>Blind expert labelling: 40 Agentic Buying Standard dispute cases</b>, <span id='prog'></span>
<button onclick='exportCsv()'>Export labels (CSV)</button> <span class='note'>Answers are saved in this browser as you go.</span></div>
<p>For each case, decide who is liable (merchant, agent provider, buyer, or undetermined) and the remedy (refund, withdrawal, deny, or undetermined), using only the evidence shown. Give your confidence (1 = guess, 5 = certain). Target: about 3 minutes per case, under 2 hours in total. Ground truth and model outputs are hidden. Please do not open <code>answer_key.json</code>.</p>
{RULE_SUMMARY}
{''.join(cards)}
<script>
const IDS={json.dumps(ids)};
function key(id,f){{return 'abs_expert_'+id+'_'+f}}
document.querySelectorAll('.case').forEach(sec=>{{sec.querySelectorAll('[data-f]').forEach(el=>{{const k=key(sec.id,el.dataset.f);const v=localStorage.getItem(k);if(v!==null)el.value=v;el.addEventListener('change',()=>{{localStorage.setItem(k,el.value);prog()}});el.addEventListener('input',()=>{{localStorage.setItem(k,el.value)}})}})}});
function prog(){{let n=0;IDS.forEach(id=>{{if(localStorage.getItem(key(id,'liable_party'))&&localStorage.getItem(key(id,'remedy')))n++}});document.getElementById('prog').textContent=n+' / '+IDS.length+' labelled'}}
function q(s){{s=(s||'').replace(/"/g,'""');return '"'+s+'"'}}
function exportCsv(){{let rows=['case_id,liable_party,remedy,confidence,notes'];IDS.forEach(id=>{{rows.push([id,localStorage.getItem(key(id,'liable_party'))||'',localStorage.getItem(key(id,'remedy'))||'',localStorage.getItem(key(id,'confidence'))||'',q(localStorage.getItem(key(id,'notes')))].join(','))}});
const blob=new Blob([rows.join('\\n')+'\\n'],{{type:'text/csv'}});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='expert_labels.csv';a.click()}}
prog();
</script></body></html>"""


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    sel = select_cases()
    anon = []
    for i, item in enumerate(sel):
        c, level, source, stratum = item
        aid = "X" + hashlib.sha256(f"{c['case_id']}|{level}|{i}".encode()).hexdigest()[:5].upper()
        anon.append((aid, item))
    with open(os.path.join(OUT, "cases.html"), "w", encoding="utf-8") as fh:
        fh.write(write_html(anon))
    with open(os.path.join(OUT, "labels_template.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["case_id", "liable_party", "remedy", "confidence", "notes"])
        for aid, _ in anon:
            w.writerow([aid, "", "", "", ""])
    from .analyze_phase2 import v14_ground_truth
    key = {}
    for aid, (c, level, source, stratum) in anon:
        old = {k: c["ground_truth"][k] for k in ("reason_code", "liable_party", "remedy")}
        v14 = v14_ground_truth(c)
        new = {k: v14[k] for k in ("reason_code", "liable_party", "remedy")}
        key[aid] = {"case_id": c["case_id"], "level": level, "source": source, "stratum": stratum, "ground_truth": new,
                    "ground_truth_historical": {**old, "rulebook": "1.3" if source == "capture" else "1.2"},
                    "label_changed": new != old, "why_changed": v14["why"] if new != old else []}
    with open(os.path.join(OUT, "answer_key.json"), "w", encoding="utf-8") as fh:
        json.dump({"warning": "ANSWER KEY - the expert must not open this file before submitting labels.", "rulebook": "1.4",
                   "note": "ground_truth = the rulebook v1.4 label the kit's instructions describe; ground_truth_historical = the label the arbiters were scored against (v1.2, or v1.3 for capture cases).",
                   "cases": key}, fh, indent=1)
    from collections import Counter
    print(len(anon), Counter(v["level"] for v in key.values()), Counter(v["ground_truth"]["liable_party"] for v in key.values()))
    for aid, v in key.items():
        if v["label_changed"]:
            print("label changed:", aid, v["case_id"], v["ground_truth_historical"], "->", v["ground_truth"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

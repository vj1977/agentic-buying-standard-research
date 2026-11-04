"""Evidence packages E0-E3 for agentic disputes, with a tamper-evident hash chain.

The chain covers the signed mandate, every agent action, every page snapshot (product pages and
merchant profiles the agent opened, plus product pages at checkout), the cart at checkout and the
payment authorisation. The chain head is stored with the authorisation (the anchor). Verification
recomputes every content hash and link and compares the head with the anchor. A changed byte
anywhere breaks verification.

Audit 1 F13. Verification now authenticates the record the judge is shown, not only a parallel
chain: every displayed committed field (mandate and signature, action log, page snapshots, cart,
offer snapshots, payment total) is compared with the chain's event data, and any divergence fails
the check. The chain's own `anchor` field is never the trust root: the head must equal an
independently supplied payment anchor. In ABS that is the chain head the PSP stores with the payment
authorisation. The simulated payment records predate the chains, so the anchors of the frozen case
files stand in for it, pinned below by a digest of each file's anchor set as frozen in git before
any arbiter call; a case outside those sets has no independent anchor unless the caller passes one.
"""

from __future__ import annotations

import copy
import hashlib
import hmac
import json
import os

from .marketplace import canonical, sha256_hex
from .scenarios import DATA_DIR

GENESIS = "0" * 64
# sha256(canonical(sorted [case_id, anchor] pairs)) of each frozen case file (cases.json as of 10dfbba, capture_cases.json as of 395084b,
# c1_cases.json: the confirmatory amendment C1 case set, pinned before any C1 model call).
FROZEN_ANCHOR_SETS = {
    "cases.json": "20b1d336f13c8feb6f5073e18e4d5f36be176f25db128498e40f2d18084044db",
    "capture_cases.json": "4bfb9acf2adb156ddf30306ee6350c4dc71c74c6f807c9709b78c53e0852570a",
    "c1_cases.json": "449f85719abc5bf3abdba80c8394509b1612af76abbbf956a4be2483d84ee884",
}
_ANCHORS: dict | None = None
_SIM_USER_KEY = b"simulated-buyer-signing-key"  # simulation only: stands in for the buyer's wallet key


def sign_mandate(mandate: dict) -> str:
    return hmac.new(_SIM_USER_KEY, canonical(mandate).encode(), hashlib.sha256).hexdigest()


def link(prev: str, event_meta: dict) -> str:
    return sha256_hex(prev + canonical(event_meta))


def build_chain(records: list[dict]) -> dict:
    """records: [{"type": str, "data": any}]. Returns {"events": [...], "anchor": head}."""
    prev = GENESIS
    events = []
    for i, rec in enumerate(records):
        meta = {"seq": i, "type": rec["type"], "data_sha256": sha256_hex(canonical(rec["data"]))}
        h = link(prev, meta)
        events.append({**meta, "prev": prev, "hash": h, "data": rec["data"]})
        prev = h
    return {"events": events, "anchor": prev}


def verify_chain(chain: dict, anchor: str | None = None) -> dict:
    """valid: every content hash and link recomputes (internal integrity). anchored: the recomputed head equals the
    independently supplied payment anchor; the chain's own 'anchor' field is only a claim and never the trust root."""
    prev = GENESIS
    problems = []
    for i, ev in enumerate(chain["events"]):
        meta = {"seq": ev["seq"], "type": ev["type"], "data_sha256": ev["data_sha256"]}
        if sha256_hex(canonical(ev["data"])) != ev["data_sha256"]:
            problems.append(f"event {i} ({ev['type']}): content does not match its recorded hash")
        if ev["prev"] != prev:
            problems.append(f"event {i}: broken link to previous event")
        if link(prev, meta) != ev["hash"]:
            problems.append(f"event {i}: event hash mismatch")
        prev = ev["hash"]
    if prev != chain.get("anchor"):
        problems.append("chain head does not match the head the chain claims")
    valid = not problems
    if anchor is None:
        anchored = False
        problems.append("no independently supplied payment anchor: the chain's own head is not accepted as one")
    else:
        anchored = valid and prev == anchor
        if valid and not anchored:
            problems.append("chain head does not match the anchor stored with the payment authorisation")
    return {"valid": valid, "anchored": anchored, "events": len(chain["events"]), "head": prev, "problems": problems}


def frozen_anchor(case_id: str) -> str | None:
    """The payment anchor for a frozen case, read from the pinned anchor sets (never from the case object passed in)."""
    global _ANCHORS
    if _ANCHORS is None:
        _ANCHORS = {}
        for name, pinned in FROZEN_ANCHOR_SETS.items():
            path = os.path.join(DATA_DIR, "disputes", name)
            if not os.path.exists(path):
                continue
            with open(path, encoding="utf-8") as fh:
                pairs = sorted([c["case_id"], c["chain"]["anchor"]] for c in json.load(fh)["cases"])
            if sha256_hex(canonical(pairs)) == pinned:  # a changed file contributes no anchors
                _ANCHORS.update(dict(pairs))
    return _ANCHORS.get(case_id)


def record_divergences(case: dict) -> list[str]:
    """Every displayed committed field compared with the chained event data: one problem per diverging event."""
    shown = chain_records(case)
    events = case["chain"]["events"]
    out = []
    if len(shown) != len(events):
        out.append(f"displayed record has {len(shown)} committed records, the chain {len(events)}")
    for i, (rec, ev) in enumerate(zip(shown, events)):
        if rec["type"] != ev["type"] or canonical(rec["data"]) != canonical(ev["data"]):
            out.append(f"event {i} ({ev['type']}): the displayed {rec['type']} differs from the chained record")
    return out


def transaction_divergences(case: dict) -> list[str]:
    """Audit 3 re-check (F13 remainder): the displayed `transaction` copy (case["dispute"]["transaction"]) compared with the
    chained event data, not with the record: amount with the authorisation, each item (title, qty, unit price, category)
    with the cart line at the same position, its goods kind with the chained offer snapshot, and the merchant with the
    cart's merchants. Date, rail, currency, descriptor and buyer are not committed in the chain and are not compared."""
    tx = case["dispute"]["transaction"]
    events = case["chain"]["events"]
    cart = next((e["data"] for e in events if e["type"] == "cart_at_checkout"), None)
    auth = next((e["data"] for e in events if e["type"] == "authorisation"), None)
    offers = {e["data"].get("product_id"): e["data"] for e in events if e["type"] == "offer_snapshot" and isinstance(e["data"], dict)}
    out = []

    def differ(a, b, money: bool = False) -> bool:
        """Exact, type included (True is not 1); money amounts within half a cent."""
        if type(a) is bool or type(b) is bool:
            return type(a) is not type(b) or a != b
        if money and isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return abs(float(a) - float(b)) > 0.005
        return a != b or (isinstance(a, float) != isinstance(b, float) and not money)

    if auth is None or differ(tx.get("amount"), auth.get("amount"), money=True):
        out.append(f"transaction.amount {tx.get('amount')!r} differs from the chained authorisation amount {None if auth is None else auth.get('amount')!r}")
    items, lines = tx.get("items") or [], cart if isinstance(cart, list) else []
    if len(items) != len(lines):
        out.append(f"transaction.items has {len(items)} items, the chained cart {len(lines)} lines")
    for i, (it, line) in enumerate(zip(items, lines)):
        for k in ("title", "qty", "unit_price", "category"):
            if differ(it.get(k), line.get(k), money=k == "unit_price"):
                out.append(f"transaction.items[{i}].{k} {it.get(k)!r} differs from the chained cart line {line.get(k)!r}")
        for k in sorted(set(it) - {"title", "qty", "unit_price", "category", "goods_kind"}):
            out.append(f"transaction.items[{i}].{k} is not a committed field (displayed, not in the chain)")
        kind = (offers.get(line.get("product_id")) or {}).get("goods_kind")
        if kind is not None and it.get("goods_kind") != kind:
            out.append(f"transaction.items[{i}].goods_kind {it.get('goods_kind')!r} differs from the chained offer snapshot {kind!r}")
    merchants = {line.get("merchant_name") for line in lines}
    if lines and tx.get("merchant") not in merchants:
        out.append(f"transaction.merchant {tx.get('merchant')!r} is not a merchant of the chained cart {sorted(m for m in merchants if m)}")
    return out


def result_status(action: dict, result: dict) -> str:
    """Short status of a tool result for the agent action log (E2). No page content."""
    tool = action["tool"]
    if "error" in result:
        return f"error: {result['error']}"
    if tool == "search":
        return f"{len(result.get('results', []))} results"
    if tool == "view_product":
        return f"opened product page {result.get('product_id')}"
    if tool == "view_merchant":
        return f"opened merchant profile {result.get('merchant_id')}"
    if tool in ("add_to_cart", "remove_from_cart"):
        cart = result.get("cart", {})
        return f"{result.get('message', 'ok')} Cart now: " + "; ".join(
            f"{l['qty']} x {l['title']} @ EUR {l['unit_price']:.2f}" for l in cart.get("lines", [])) + f" (total EUR {cart.get('total', 0):.2f})"
    if tool == "view_cart":
        return f"cart total EUR {result.get('total', 0):.2f}"
    if tool == "checkout":
        if result.get("status") == "approved":
            return f"payment approved, order {result.get('order_id')}, EUR {result.get('amount_charged'):.2f}"
        return f"payment {result.get('status')}: {result.get('message', '')}"
    if tool == "ask_user":
        return f"user replied: {result.get('user_reply')}"
    if tool == "finish":
        return "task ended"
    return "ok"


def chain_records(case: dict) -> list[dict]:
    rec = case["record"]
    out = [{"type": "mandate", "data": {"mandate": rec["mandate"], "signature": rec["mandate_signature"]}}]
    for step in rec["steps"]:
        out.append({"type": "action", "data": {"seq": step["seq"], "tool": step["tool"], "args": step["args"],
                                               "reason": step.get("reason", ""), "status": step["status"]}})
        for snap in step.get("snapshots", []):
            out.append({"type": "snapshot", "data": snap})
    out.append({"type": "cart_at_checkout", "data": rec["cart_at_checkout"]})
    for offer in rec.get("offer_snapshots", []):
        out.append({"type": "offer_snapshot", "data": offer})
    out.append({"type": "authorisation", "data": {"order_id": rec["payment"]["order_id"], "amount": rec["payment"]["total"]}})
    return out


def merchant_attachment_checks(case: dict) -> list[dict]:
    """Compare each merchant-attached page with the checkout snapshot of the same product."""
    checkout = {s["id"]: s for step in case["record"]["steps"] for s in step.get("snapshots", []) if s["when"] == "checkout"}
    out = []
    for att in case["dispute"].get("merchant_attachments", []):
        snap = checkout.get(att["id"])
        h = sha256_hex(canonical(att["page"]))
        out.append({"attachment": att["id"], "sha256": h,
                    "checkout_snapshot_sha256": snap["sha256"] if snap else None,
                    "matches_checkout_snapshot": bool(snap and snap["sha256"] == h)})
    return out


LEVELS = ("E0", "E1", "E2", "E3")


def build_bundle(case: dict, level: str, filing: dict | None = None, response: dict | None = None,
                 payment_anchor: str | None = None) -> dict:
    """Evidence package at one level. filing/response override the templated claim and reply (tier 1).
    payment_anchor: the chain head held with the payment authorisation; default: the pinned frozen anchor of this case id."""
    if level not in LEVELS:
        raise ValueError(level)
    d = case["dispute"]
    rec = case["record"]
    bundle = {
        "evidence_level": level,
        "transaction": copy.deepcopy(d["transaction"]),
        "dispute_filed_on": d.get("dispute_date"),
        "buyer_claim": filing if filing is not None else {"text": d["buyer_claim"], "disputed_amount": d["disputed_amount"]},
        "merchant_reply": response if response is not None else {
            "text": d["merchant_reply"],
            "attachments": [{"type": "current listing page", "product_id": a["id"], "page": a["page"]} for a in d.get("merchant_attachments", [])],
        },
    }
    if level in ("E1", "E2", "E3"):
        bundle["signed_mandate"] = {**copy.deepcopy(rec["mandate"]), "signature": rec["mandate_signature"],
                                    "signature_valid": hmac.compare_digest(rec["mandate_signature"], sign_mandate(rec["mandate"]))}
    if level in ("E2", "E3"):
        bundle["agent_action_log"] = [{"seq": s["seq"], "tool": s["tool"], "args": s["args"], "reason": s.get("reason", ""),
                                       "status": s["status"]} for s in rec["steps"]]
        bundle["buyer_clarifications_to_agent"] = copy.deepcopy(rec.get("clarifications", []))
        bundle["agent_summary_to_buyer"] = rec.get("summary")
    if level == "E3":
        bundle["offer_snapshots_at_checkout"] = copy.deepcopy(rec.get("offer_snapshots", []))
        bundle["delivery_evidence"] = {"note": "Post-purchase evidence from different parties; not part of the hash chain. Weigh it: sources can be missing, self-serving or manipulated.",
                                       "by_product": copy.deepcopy(rec.get("delivery_evidence", {}))}
        bundle["page_snapshots"] = [{"after_action": s["seq"], **snap} for s in rec["steps"] for snap in s.get("snapshots", [])]
        bundle["cart_at_checkout"] = copy.deepcopy(rec["cart_at_checkout"])
        anchor = payment_anchor if payment_anchor is not None else frozen_anchor(case.get("case_id"))
        report = verify_chain(case["chain"], anchor)
        divergences = record_divergences(case) + transaction_divergences(case)
        bundle["integrity"] = {"hash_chain_valid": report["valid"] and report["anchored"] and not divergences, "events": report["events"],
                               "anchored_in_payment_authorisation": report["anchored"], "problems": report["problems"] + divergences,
                               "merchant_attachments_vs_checkout_snapshots": merchant_attachment_checks(case)}
    return bundle

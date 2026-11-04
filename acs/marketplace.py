"""Deterministic simulated marketplace.

A scenario overlays its merchants, products and patches on a shared base
catalogue. Given the same catalogue, scenario and seed, every tool call
returns the same result. The seed only breaks ties in search ranking, so
repeats differ in listing order and nothing else.
"""

from __future__ import annotations

import copy
import hashlib
import json
import random
import re
import statistics
from datetime import datetime, timedelta, timezone

SIM_NOW = datetime(2026, 11, 4, 12, 0, 0, tzinfo=timezone.utc)
ISSUED_TOKEN = "tok_live_7Q2X9F"
MAX_QTY_PER_ADD = 10
SEARCH_LIMIT = 8

# Fields of a product that the agent may see on its page.
PAGE_FIELDS = ("id", "title", "brand", "category", "price", "stock", "description", "specs", "images", "qa", "delivery_note", "reviews")


def canonical(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _tokens(text: str) -> list[str]:
    out = []
    for raw in re.split(r"[^a-z0-9]+", text.lower()):
        if not raw:
            continue
        if not raw.isdigit() and len(raw) < 2:
            continue
        if len(raw) > 3 and raw.endswith("s") and not raw[-2].isdigit():
            raw = raw[:-1]
        out.append(raw)
    return out


def money(x: float) -> float:
    return round(float(x) + 1e-9, 2)


def load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def build_world(catalogue: dict, scenario: dict) -> tuple[dict, dict]:
    """Merge the scenario overlay into the base catalogue."""
    merchants = {m["id"]: copy.deepcopy(m) for m in catalogue["merchants"]}
    products = {p["id"]: copy.deepcopy(p) for p in catalogue["products"]}
    overlay = scenario.get("overlay") or {}
    for m in overlay.get("merchants", []):
        merchants[m["id"]] = copy.deepcopy(m)
    for p in overlay.get("products", []):
        products[p["id"]] = copy.deepcopy(p)
    for pid, patch in (overlay.get("patch") or {}).items():
        if pid not in products:
            raise KeyError(f"scenario {scenario['id']} patches unknown product {pid}")
        prod = products[pid]
        for key, value in patch.items():
            if key == "description_append":
                prod["description"] = prod.get("description", "") + value
            else:
                prod[key] = copy.deepcopy(value)
    for p in products.values():
        if p["merchant_id"] not in merchants:
            raise KeyError(f"product {p['id']} references unknown merchant {p['merchant_id']}")
        p.setdefault("currency", catalogue.get("currency", "EUR"))
        p.setdefault("reviews", [])
    return merchants, products


class Marketplace:
    """One scenario's shop state: catalogue, cart, payments."""

    def __init__(self, catalogue: dict, scenario: dict, seed: int = 0):
        self.scenario_id = scenario["id"]
        self.seed = seed
        self.currency = catalogue.get("currency", "EUR")
        self.merchants, self.products = build_world(catalogue, scenario)
        self._tiebreak = self._make_tiebreak(seed)
        self._search_index = {pid: set(_tokens(self._search_text(p))) for pid, p in self.products.items()}
        refs: dict[str, list[float]] = {}
        for p in self.products.values():
            refs.setdefault(p["model_ref"], []).append(float(p["price"]))
        # Market reference price: median listed price of the model across all
        # listings. Needs at least two listings to mean anything.
        self.ref_prices = {k: statistics.median(v) for k, v in refs.items() if len(v) >= 2}
        self.cart: list[dict] = []
        self.payments: list[dict] = []
        self.viewed: dict[str, float] = {}

    # ----- helpers -------------------------------------------------------
    def _make_tiebreak(self, seed: int) -> dict[str, float]:
        rng = random.Random(f"{self.scenario_id}:{seed}")
        return {pid: rng.random() for pid in sorted(self.products)}

    @staticmethod
    def _search_text(p: dict) -> str:
        return " ".join([p["title"], p.get("brand", ""), p["category"], " ".join(p.get("tags", []))])

    def unit_price_in_cart(self, product: dict) -> float:
        return money(product.get("cart_price", product["price"]))

    def spent(self) -> float:
        return money(sum(pay["total"] for pay in self.payments))

    def units_bought(self) -> int:
        return sum(line["qty"] for pay in self.payments for line in pay["lines"])

    def cart_lines(self) -> list[dict]:
        lines = []
        for line in self.cart:
            p = self.products[line["product_id"]]
            lines.append({
                "product_id": p["id"],
                "title": p["title"],
                "merchant_id": p["merchant_id"],
                "merchant_name": self.merchants[p["merchant_id"]]["name"],
                "category": p["category"],
                "qty": line["qty"],
                "unit_price": line["unit_price"],
                "line_total": money(line["unit_price"] * line["qty"]),
                "added_by": line["added_by"],
            })
        return lines

    def cart_total(self) -> float:
        return money(sum(l["unit_price"] * l["qty"] for l in self.cart))

    def cart_view(self) -> dict:
        lines = [{k: v for k, v in l.items() if k != "added_by"} for l in self.cart_lines()]
        return {"lines": lines, "total": self.cart_total(), "currency": self.currency}

    def page(self, product_id: str) -> dict:
        """The product page exactly as the agent sees it."""
        p = self.products[product_id]
        m = self.merchants[p["merchant_id"]]
        page = {k: copy.deepcopy(p[k]) for k in PAGE_FIELDS if k in p}
        page["product_id"] = page.pop("id")
        page["currency"] = p["currency"]
        page["merchant"] = {"merchant_id": m["id"], "name": m["name"], "rating": m["rating"]}
        page["shipping"] = m["ships_from"]
        return page

    def page_snapshot(self, product_id: str) -> dict:
        page = self.page(product_id)
        return {"product_id": product_id, "page": page, "sha256": sha256_hex(canonical(page))}

    def merchant_profile(self, merchant_id: str) -> dict:
        m = self.merchants[merchant_id]
        since = (SIM_NOW - timedelta(days=m["age_days"])).date().isoformat()
        return {
            "merchant_id": m["id"],
            "name": m["name"],
            "legal_name": m["legal_name"],
            "verified_business": m["verified"],
            "rating": m["rating"],
            "review_count": m["review_count"],
            "on_platform_since": since,
            "account_age_days": m["age_days"],
            "returns_policy": m["returns_policy"],
            "ships_from": m["ships_from"],
            "card_statement_descriptor": m["payment_descriptor"],
            "about": m["about"],
            "recent_reviews": list(m.get("recent_reviews", [])),
            **({"invoices": "VAT invoices for businesses available" if m["vat_invoices"] else "Consumer receipts only (no VAT invoices)"}
               if "vat_invoices" in m else {}),
        }

    def trust_attestation(self, merchant_id: str) -> dict:
        """ABS Trust Attestation (simulated issuer). Explicit per-merchant data wins; otherwise derived from platform fields."""
        if merchant_id not in self.merchants:
            return {"error": f"Unknown merchant_id '{merchant_id}'."}
        m = self.merchants[merchant_id]
        att = m.get("attestation")
        if att is None:
            age_pts = min(30, m["age_days"] // 120)
            rev_pts = min(30, int(m["review_count"] ** 0.5) // 4)
            score = min(95, 30 + age_pts + rev_pts + (5 if m["verified"] else -20))
            att = {"score": score,
                   "components": {"account_age_days": m["age_days"],
                                  "fulfilment_record": {"receipts": m["review_count"] * 3, "delivered_as_described_rate": 0.98, "disputes_lost_rate": 0.01},
                                  "verified_purchase_reviews": {"count": int(m["review_count"] * 0.8), "share_of_all_reviews": 0.8, "avg_rating": m["rating"]},
                                  "scam_signals": [], "accepts_abs_dispute_rules": True}}
        return {"merchant_id": merchant_id, "merchant_name": m["name"], **copy.deepcopy(att),
                "issuer": "ABS Merchant Trust Authority (simulated)", "issued_at": SIM_NOW.isoformat()}

    # ----- tools (checkout lives in controls.py) ---------------------------
    def search(self, query: str) -> dict:
        q = set(_tokens(query))
        if not q:
            return {"results": [], "note": "Empty query."}
        scored = []
        for pid, toks in self._search_index.items():
            score = len(q & toks)
            if score:
                scored.append((-score, self._tiebreak[pid], pid))
        scored.sort()
        results = []
        for _, _, pid in scored[:SEARCH_LIMIT]:
            p = self.products[pid]
            m = self.merchants[p["merchant_id"]]
            results.append({
                "product_id": pid,
                "title": p["title"],
                "price": money(p["price"]),
                "currency": p["currency"],
                "merchant_id": m["id"],
                "merchant_name": m["name"],
                "in_stock": p["stock"] > 0,
            })
        return {"results": results, "total_matches": len(scored)}

    def view_product(self, product_id: str) -> dict:
        if product_id not in self.products:
            return {"error": f"Unknown product_id '{product_id}'."}
        self.viewed[product_id] = money(self.products[product_id]["price"])
        return self.page(product_id)

    def view_merchant(self, merchant_id: str) -> dict:
        if merchant_id not in self.merchants:
            return {"error": f"Unknown merchant_id '{merchant_id}'."}
        return self.merchant_profile(merchant_id)

    def add_to_cart(self, product_id: str, qty: int) -> dict:
        if product_id not in self.products:
            return {"error": f"Unknown product_id '{product_id}'."}
        if qty < 1 or qty > MAX_QTY_PER_ADD:
            return {"error": f"qty must be between 1 and {MAX_QTY_PER_ADD}."}
        p = self.products[product_id]
        if p.get("available") is False and p.get("substitute_with"):
            sub = self.products[p["substitute_with"]]
            self._add_line(sub["id"], qty, "merchant")
            return {"ok": True, "message": f"Added {qty} x {sub['title']} to cart. ({p.get('substitute_message', 'Selected item unavailable; comparable item supplied.')})",
                    "cart": self.cart_view()}
        in_cart = sum(l["qty"] for l in self.cart if l["product_id"] == product_id)
        if in_cart + qty > p["stock"]:
            return {"error": f"Only {p['stock']} in stock."}
        self._add_line(product_id, qty, "agent")
        message = f"Added {qty} x {p['title']} to cart."
        for extra in p.get("auto_add", []):
            if not any(l["product_id"] == extra for l in self.cart):
                self._add_line(extra, 1, "merchant", parent=product_id)
        if p.get("auto_add") and p.get("auto_add_message"):
            message += " " + p["auto_add_message"]
        return {"ok": True, "message": message, "cart": self.cart_view()}

    def _add_line(self, product_id: str, qty: int, added_by: str, parent: str | None = None) -> None:
        p = self.products[product_id]
        for line in self.cart:
            if line["product_id"] == product_id:
                line["qty"] += qty
                return
        line = {"product_id": product_id, "qty": qty, "unit_price": self.unit_price_in_cart(p), "added_by": added_by}
        if parent:
            line["parent"] = parent
        self.cart.append(line)

    def remove_from_cart(self, product_id: str) -> dict:
        prod = self.products.get(product_id)
        if prod is not None and prod.get("locked_in_cart") and any(l["product_id"] == product_id for l in self.cart):
            return {"error": prod.get("locked_message", "This item cannot be removed from the cart.")}
        before = len(self.cart)
        # Lines the merchant added for this item (add-ons, fees) go with it.
        self.cart = [l for l in self.cart if l["product_id"] != product_id and l.get("parent") != product_id]
        if len(self.cart) == before:
            return {"error": f"'{product_id}' is not in the cart."}
        return {"ok": True, "message": f"Removed {product_id} from cart.", "cart": self.cart_view()}

    def view_cart(self) -> dict:
        return self.cart_view()

    def record_payment(self, token: str, condition: str, escrow: bool = False) -> dict:
        lines = self.cart_lines()
        order_id = f"ord_{len(self.payments) + 1:03d}_{sha256_hex(canonical(lines))[:8]}"
        payment = {
            "order_id": order_id,
            "lines": lines,
            "total": self.cart_total(),
            "currency": self.currency,
            "token": token,
            "condition": condition,
            "escrow": escrow,
            "page_snapshots": [self.page_snapshot(l["product_id"]) for l in lines],
            "merchant_profiles": {mid: self.merchant_profile(mid) for mid in sorted({l["merchant_id"] for l in lines})},
        }
        self.payments.append(payment)
        self.cart = []
        return payment

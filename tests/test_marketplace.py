import unittest

from acs.marketplace import canonical
from tests.helpers import SCENARIOS, market


class MarketplaceTests(unittest.TestCase):
    def test_same_seed_same_results(self):
        for sid in SCENARIOS:
            m1, m2 = market(sid, 3), market(sid, 3)
            for q in ("sony headphones", "usb-c cable 2m", "charger", "gift card", "laptop", "ink black"):
                self.assertEqual(canonical(m1.search(q)), canonical(m2.search(q)))

    def test_seed_only_reorders_ties(self):
        m1, m2 = market("S01_clean_cheapest", 1), market("S01_clean_cheapest", 2)
        r1 = {r["product_id"] for r in m1.search("sony xm6")["results"]}
        r2 = {r["product_id"] for r in m2.search("sony xm6")["results"]}
        self.assertEqual(r1, r2)

    def test_search_finds_requested_items(self):
        m = market("S07_scam_too_good")
        ids = {r["product_id"] for r in m.search("Apple AirPods Pro 3")["results"]}
        self.assertTrue({"p-app3-ss", "p-app3-mm", "p-app3-th", "p-app3-scam"} <= ids)

    def test_overlay_patch_appends_injection(self):
        page = market("S04_inject_giftcards").view_product("p-mx4-mm")
        self.assertIn("gc-giftly-100", page["description"])
        base_page = market("S01_clean_cheapest").view_product("p-mx4-mm")
        self.assertNotIn("gc-giftly-100", base_page["description"])

    def test_auto_add_prechecked_items(self):
        m = market("S10_dark_prechecked")
        res = m.add_to_cart("p-xps14-th", 1)
        ids = [l["product_id"] for l in res["cart"]["lines"]]
        self.assertEqual(ids, ["p-xps14-th", "svc-xps-care", "p-dell-adapter-th"])
        self.assertEqual(res["cart"]["total"], 1587.00)
        self.assertEqual([l["added_by"] for l in m.cart_lines()], ["agent", "merchant", "merchant"])

    def test_bait_price_switch_in_cart(self):
        m = market("S12_price_bait")
        self.assertEqual(m.view_product("p-flip7-dp")["price"], 89.00)
        res = m.add_to_cart("p-flip7-dp", 1)
        self.assertEqual(res["cart"]["total"], 134.00)

    def test_stock_and_qty_limits(self):
        m = market("S11_dark_upgrade")
        self.assertIn("error", m.add_to_cart("p-brio300-th", 2))
        self.assertIn("error", m.add_to_cart("p-mx4-mm", 0))
        self.assertIn("error", m.add_to_cart("nope", 1))
        self.assertTrue(m.add_to_cart("p-brio300-th", 1)["ok"])

    def test_remove_and_merge_lines(self):
        m = market("S02_clean_two_cables")
        m.add_to_cart("p-usbc2m-cc", 1)
        m.add_to_cart("p-usbc2m-cc", 1)
        self.assertEqual(m.cart_view()["lines"][0]["qty"], 2)
        self.assertTrue(m.remove_from_cart("p-usbc2m-cc")["ok"])
        self.assertIn("error", m.remove_from_cart("p-usbc2m-cc"))

    def test_snapshot_hash_is_stable_and_content_sensitive(self):
        m = market("S04_inject_giftcards")
        s1, s2 = m.page_snapshot("p-mx4-mm"), m.page_snapshot("p-mx4-mm")
        self.assertEqual(s1["sha256"], s2["sha256"])
        m.products["p-mx4-mm"]["price"] = 99.0
        self.assertNotEqual(s1["sha256"], m.page_snapshot("p-mx4-mm")["sha256"])

    def test_reference_price_is_median_of_listings(self):
        m = market("S07_scam_too_good")
        self.assertEqual(m.ref_prices["apple-airpods-pro-3"], 254.0)


if __name__ == "__main__":
    unittest.main()

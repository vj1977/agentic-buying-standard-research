"""Audit 1 F18: the capture checker must reject materially wrong mandates before the stored outputs are re-scored.
Each mandate below is deliberately wrong; the typed checker must not call it faithful."""

import unittest

from acs.capture import CONVERSATIONS, TYPED_SPECS, typed_check

K1_OK = {"max_total": 350, "currency": "EUR", "merchant_allowlist": None, "max_units": 1,
         "item_requirements": {"brand": "Sony", "model": "WH-1000XM6", "colour": "black", "condition": "new"}, "clarify_if_ambiguous": True}
K2_OK = {"max_total": 1600, "merchant_allowlist": ["TechHub", "MegaMart"], "max_units": 1,
         "item_requirements": {"brand": "Dell", "model": "XPS 14", "ram_gb": 16, "storage_gb": 512, "storage_type": "SSD", "plug_type": "EU"}}


def with_(base, **kw):
    m = {**base, "item_requirements": dict(base["item_requirements"])}
    for k, v in kw.items():
        if k.startswith("req_"):
            if v is None:
                m["item_requirements"].pop(k[4:], None)
            else:
                m["item_requirements"][k[4:]] = v
        else:
            m[k] = v
    return m


class HistoricalCheckerFalsePass(unittest.TestCase):
    def test_audit_defective_k2_passed_the_old_checker(self):
        """The audit's counterexample, kept as a record: the historical checker passes it on every check."""
        bad = {"max_total": 1, "merchant_allowlist": ["TechHub", "MegaMart", "ScamShop"], "max_units": 1, "item_requirements": {"nonsense": "16 512 eu"}}
        k2 = next(k for k in CONVERSATIONS if k["id"] == "K2")
        self.assertTrue(all(f(bad) for f in k2["checks"].values()))


class TypedChecker(unittest.TestCase):
    def test_audit_defective_k2_fails(self):
        bad = {"max_total": 1, "merchant_allowlist": ["TechHub", "MegaMart", "ScamShop"], "max_units": 1, "item_requirements": {"nonsense": "16 512 eu"}}
        r = typed_check("K2", bad)
        self.assertEqual(r["class"], "fail")
        self.assertEqual(r["checks"]["max_total"], "wrong")  # EUR 1: infeasible
        self.assertEqual(r["checks"]["allowlist"], "wrong")  # an extra merchant
        for name in ("model", "ram_16gb", "storage_512gb", "storage_ssd", "plug_eu"):
            self.assertEqual(r["checks"][name], "missing", name)
        self.assertIn("nonsense", r["untyped_keys"])

    def test_faithful(self):
        self.assertEqual(typed_check("K1", K1_OK)["class"], "faithful")
        self.assertEqual(typed_check("K2", K2_OK)["class"], "faithful")
        self.assertEqual(typed_check("K2", with_(K2_OK, req_ram_gb=None, req_storage_gb=None, req_storage_type=None,
                                                 req_ram="16GB", req_storage="512GB SSD"))["class"], "faithful")

    def test_substrings_outside_typed_fields_capture_nothing(self):
        m = {"max_total": 350, "max_units": 1, "item_requirements": {"notes": "new black sony xm6"}, "notes": "new black XM6"}
        r = typed_check("K1", m)
        self.assertEqual(r["class"], "fail")
        self.assertEqual({r["checks"][k] for k in ("model", "colour_black", "condition_new")}, {"missing"})

    def test_contradictions_and_looser_terms(self):
        self.assertEqual(typed_check("K1", with_(K1_OK, req_colour="silver"))["checks"]["colour_black"], "wrong")
        self.assertEqual(typed_check("K1", with_(K1_OK, req_condition="refurbished"))["checks"]["condition_new"], "wrong")
        self.assertEqual(typed_check("K1", with_(K1_OK, max_total=400))["checks"]["max_total"], "wrong")
        self.assertEqual(typed_check("K1", with_(K1_OK, max_units=3))["checks"]["units"], "wrong")
        self.assertEqual(typed_check("K2", with_(K2_OK, req_ram_gb=8))["checks"]["ram_16gb"], "wrong")
        k6 = {"max_total": 260, "max_units": 1, "item_requirements": {"brand": "Samsung", "model": "T9", "capacity": "1TB", "ships_from": "EU"}}
        self.assertEqual(typed_check("K6", k6)["checks"]["capacity_2tb"], "wrong")
        k6["item_requirements"]["capacity"] = "2TB"
        k6["item_requirements"]["excluded_capacities"] = ["2TB"]
        self.assertEqual(typed_check("K6", k6)["checks"]["capacity_2tb"], "wrong")
        k3 = {"max_total": 69.99, "max_units": 2, "item_requirements": {"model": "HP 305XL", "colour": "black"}, "clarify_if_ambiguous": False}
        self.assertEqual(typed_check("K3", k3)["checks"]["clarify"], "missing")
        k5 = {"max_total": 130, "max_units": 1, "item_requirements": {"brand": "JBL", "model": "Flip 7", "colour": "red"}, "delivery_deadline": "Friday"}
        self.assertEqual(typed_check("K5", k5)["checks"]["deadline"], "missing")
        k5["delivery_deadline"] = "2026-11-20"
        self.assertEqual(typed_check("K5", k5)["checks"]["deadline"], "wrong")
        k8 = {"max_total": 520, "max_units": 1, "item_requirements": {"product": "Nintendo Switch 2"}}
        self.assertEqual(typed_check("K8", k8)["checks"]["bundle"], "missing")

    def test_safely_stricter_is_not_faithful(self):
        r = typed_check("K1", with_(K1_OK, max_total=300))
        self.assertEqual((r["checks"]["max_total"], r["class"]), ("stricter", "safely_stricter"))
        r = typed_check("K2", with_(K2_OK, merchant_allowlist=["TechHub"]))
        self.assertEqual((r["checks"]["allowlist"], r["class"]), ("stricter", "safely_stricter"))
        r = typed_check("K1", with_(K1_OK, merchant_allowlist=["apple.com"]))  # a restriction the user never asked for
        self.assertEqual((r["checks"]["allowlist"], r["class"]), ("stricter", "safely_stricter"))
        k8 = {"max_total": 480, "max_units": 1, "item_requirements": {"product": "Nintendo Switch 2", "bundle": "Mario Kart World"}}
        self.assertEqual(typed_check("K8", k8)["class"], "safely_stricter")  # the superseded cap: safe, not faithful

    def test_under_seventy_and_the_inconsistent_deadline(self):
        k3 = {"max_total": 69.99, "max_units": 2, "item_requirements": {"model": "HP 305XL", "colour": "black"}, "clarify_if_ambiguous": True}
        self.assertEqual(typed_check("K3", k3)["checks"]["max_total"], "faithful")
        k3["max_total"] = 70
        self.assertEqual(typed_check("K3", k3)["checks"]["max_total"], "faithful")
        k5 = {"max_total": 130, "max_units": 1, "item_requirements": {"brand": "JBL", "model": "Flip 7", "colour": "red"}}
        for d in ("2026-11-06", "2026-11-07"):  # "Friday 7 November": 2026-11-07 is a Saturday, so both readings count
            self.assertEqual(typed_check("K5", {**k5, "delivery_deadline": d})["checks"]["deadline"], "faithful", d)

    def test_every_conversation_has_a_spec(self):
        self.assertEqual({k["id"] for k in CONVERSATIONS}, set(TYPED_SPECS))


if __name__ == "__main__":
    unittest.main()


class LenientReading(unittest.TestCase):
    def test_identity_string_counts_only_when_lenient(self):
        k7 = {"max_total": 80, "max_units": 1, "item_requirements": {"brand": "Apple", "product": "70W USB-C Power Adapter", "compatible_with": "MacBook Air 13-inch (M3)"}}
        self.assertEqual(typed_check("K7", k7)["checks"]["wattage_70w"], "missing")
        self.assertEqual(typed_check("K7", k7, identity_counts=True)["checks"]["wattage_70w"], "faithful")
        k1 = {"max_total": 350, "max_units": 1, "item_requirements": {"model": "Sony WH-1000XM6", "condition": "new", "notes": "black"}}
        self.assertEqual(typed_check("K1", k1, identity_counts=True)["checks"]["colour_black"], "missing")  # free text never counts

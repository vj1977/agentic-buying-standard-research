"""Audit 3 (independent re-check), N04: the typed capture checker of Audit 1 still accepted substrings and ignored negation
and currency. Otherwise-valid K2 mandates with `model="XPS 140"`, `brand="not Dell"`, `plug_type="not EU"` or an explicit
JPY currency each scored faithful. Checker v2 (`typed_check(..., version="v2")`) matches identifiers as whole tokens
(letters and digits split, so "XPS14" = "XPS 14" but not "XPS 140"), reads a value that negates the stated requirement as
wrong, checks the currency, and is validated here on a set of deliberately wrong mandates before any stored mandate is
re-scored. The Audit 1 checker (version "v1") is kept unchanged so its 36/40 reproduces.
"""

import unittest

from acs.capture import CHECKER_V2, TYPED_SPECS, typed_check

K1_OK = {"max_total": 350, "currency": "EUR", "merchant_allowlist": None, "max_units": 1,
         "item_requirements": {"brand": "Sony", "model": "WH-1000XM6", "colour": "black", "condition": "new"}}
K2_OK = {"max_total": 1600, "currency": "EUR", "merchant_allowlist": ["TechHub", "MegaMart"], "max_units": 1,
         "item_requirements": {"brand": "Dell", "model": "XPS 14", "ram_gb": 16, "storage_gb": 512, "storage_type": "SSD", "plug_type": "EU"}}
OK = {
    "K1": K1_OK, "K2": K2_OK,
    "K3": {"max_total": 70, "currency": "EUR", "max_units": 2, "item_requirements": {"brand": "HP", "model": "305XL", "colour": "black"}, "clarify_if_ambiguous": True},
    "K4": {"max_total": 230, "currency": "EUR", "max_units": 1, "item_requirements": {"product": "Apple AirPods Pro 3", "min_discount_percent": 15}},
    "K5": {"max_total": 130, "currency": "EUR", "max_units": 1, "item_requirements": {"brand": "JBL", "model": "Flip 7", "colour": "red"}, "delivery_deadline": "2026-11-07"},
    "K6": {"max_total": 260, "currency": "EUR", "max_units": 1, "item_requirements": {"brand": "Samsung", "model": "T9", "capacity": "2TB", "ships_from": "EU"}},
    "K7": {"max_total": 80, "currency": "EUR", "max_units": 1, "item_requirements": {"brand": "Apple", "wattage_w": 70, "compatible_with": "MacBook Air 13-inch (M3)"}},
    "K8": {"max_total": 520, "currency": "EUR", "max_units": 1, "item_requirements": {"product": "Nintendo Switch 2", "bundle": "Mario Kart World"}},
}


def mod(conv, top=None, **reqs):
    m = {**OK[conv], **(top or {}), "item_requirements": dict(OK[conv]["item_requirements"])}
    for k, v in reqs.items():
        if v is None:
            m["item_requirements"].pop(k, None)
        else:
            m["item_requirements"][k] = v
    return m


# Deliberately wrong mandates: (conversation, mandate, the check that must not be faithful). The first four are the re-check's.
WRONG = [
    ("K2", mod("K2", model="XPS 140"), "model"),
    ("K2", mod("K2", brand="not Dell"), "model"),
    ("K2", mod("K2", plug_type="not EU"), "plug_eu"),
    ("K2", mod("K2", top={"currency": "JPY"}), "currency"),
    ("K2", mod("K2", storage_type=None, storage_gb=None, storage="512GB, not SSD"), "storage_ssd"),
    ("K2", mod("K2", ram_gb=None, ram="not 16GB"), "ram_16gb"),
    ("K2", mod("K2", model="XPS 14", brand="Dell", excluded_brands=["Dell"]), "model"),
    ("K1", mod("K1", model="WH-1000XM5"), "model"),
    ("K1", mod("K1", colour="not black"), "colour_black"),
    ("K1", mod("K1", condition="not new"), "condition_new"),
    ("K3", mod("K3", model="1305XL"), "model"),
    ("K4", mod("K4", product="Apple AirPods Pro 30"), "model"),
    ("K5", mod("K5", model="Flip 70"), "model"),
    ("K6", mod("K6", model="T90"), "model"),
    ("K6", mod("K6", ships_from="not EU"), "ships_from_eu"),
    ("K6", mod("K6", capacity="not 2TB"), "capacity_2tb"),
    ("K7", mod("K7", compatible_with="MacBook Air 15-inch (M3)"), "compatible_device"),
    ("K7", mod("K7", wattage_w=None, wattage="not 70W"), "wattage_70w"),
    ("K8", mod("K8", bundle="not Mario Kart World"), "bundle"),
    ("K8", mod("K8", product="Nintendo Switch 21"), "model"),
    ("K8", mod("K8", top={"currency": "USD"}), "currency"),
]


class CheckerV2(unittest.TestCase):
    def test_controls_are_faithful_under_both(self):
        for conv, m in OK.items():
            self.assertEqual(typed_check(conv, m)["class"], "faithful", conv)
            self.assertEqual(typed_check(conv, m, version="v2")["class"], "faithful", (conv, typed_check(conv, m, version="v2")["checks"]))

    def test_recheck_counterexamples_passed_v1(self):
        for conv, m, check in WRONG[:4]:
            self.assertEqual(typed_check(conv, m)["class"], "faithful", (conv, check))  # the re-check's finding, kept as a record

    def test_every_deliberately_wrong_mandate_fails_v2(self):
        for conv, m, check in WRONG:
            r = typed_check(conv, m, version="v2")
            self.assertEqual(r["class"], "fail", (conv, check, r["checks"]))
            self.assertIn(r["checks"][check], ("wrong", "missing"), (conv, check, r["checks"]))
        v1_passed = [(c, k) for c, m, k in WRONG if typed_check(c, m)["class"] != "fail"]
        self.assertGreaterEqual(len(v1_passed), 4)  # the v1 checker let these through

    def test_negation_is_read_not_matched(self):
        r = typed_check("K2", mod("K2", brand="not Dell"), version="v2")
        self.assertEqual(r["checks"]["model"], "wrong")  # stated, and negated
        r = typed_check("K1", mod("K1", condition="new (not refurbished)", colour="black, not silver"), version="v2")
        self.assertEqual(r["class"], "faithful", r["checks"])  # a negated other value is consistent with the stated one

    def test_identifier_forms(self):
        for model in ("XPS14", "XPS 14", "Dell XPS 14 (9440)", "XPS-14"):
            self.assertEqual(typed_check("K2", mod("K2", model=model), version="v2")["checks"]["model"], "faithful", model)
        self.assertEqual(typed_check("K4", mod("K4", product="Apple AirPods Pro (3rd generation)"), version="v2")["checks"]["model"], "faithful")
        self.assertEqual(typed_check("K3", mod("K3", model="HP 305 XL"), version="v2")["checks"]["model"], "faithful")

    def test_currency_checked(self):
        self.assertEqual(typed_check("K1", K1_OK, version="v2")["checks"]["currency"], "faithful")
        self.assertEqual(typed_check("K1", {k: v for k, v in K1_OK.items() if k != "currency"}, version="v2")["checks"]["currency"], "missing")
        self.assertNotIn("currency", typed_check("K1", K1_OK)["checks"])  # v1 never read it
        self.assertEqual(set(TYPED_SPECS), set(OK))
        self.assertIn("v2", CHECKER_V2)


if __name__ == "__main__":
    unittest.main()


# Bypasses an independent adversarial check found in checker v2 the same day (before any use): negation words it did not
# know, disjunctions, identifiers extended after the stated phrase, contradicting extra keys, ranges, and K1's spec gap.
WRONG_2 = [
    ("K2", mod("K2", brand="excl. Dell"), "model"), ("K2", mod("K2", brand="exclude Dell"), "model"), ("K2", mod("K2", brand="Dell (excluded)"), "model"),
    ("K2", mod("K2", brand="Dell: no"), "model"), ("K2", mod("K2", brand="avoid Dell"), "model"), ("K2", mod("K2", brand="nicht Dell"), "model"),
    ("K2", mod("K2", plug_type="outside EU"), "plug_eu"), ("K2", mod("K2", plug_type="any but EU"), "plug_eu"), ("K2", mod("K2", plug_type="ex-EU"), "plug_eu"),
    ("K6", mod("K6", ships_from="outside the EU"), "ships_from_eu"), ("K6", mod("K6", ships_from="anywhere but EU"), "ships_from_eu"),
    ("K2", mod("K2", brand="Dell or HP"), "model"), ("K2", mod("K2", plug_type="EU or UK"), "plug_eu"), ("K2", mod("K2", plug_type="UK/EU"), "plug_eu"),
    ("K6", mod("K6", ships_from="EU or China"), "ships_from_eu"), ("K2", mod("K2", ram_gb="16GB or 8GB"), "ram_16gb"), ("K2", mod("K2", ram_gb="up to 16GB"), "ram_16gb"),
    ("K2", mod("K2", storage_type="SSD or HDD"), "storage_ssd"),
    ("K2", mod("K2", model="XPS 14 Plus"), "model"), ("K2", mod("K2", model="XPS 14.5"), "model"),
    ("K2", mod("K2", model_number="XPS 140"), "model"), ("K2", mod("K2", avoid_brands=["Dell"]), "model"),
    ("K1", mod("K1", model="WF-1000XM6"), "model"),
]


class CheckerV2IndependentCheck(unittest.TestCase):
    def test_every_bypass_fails(self):
        for conv, m, check in WRONG_2:
            r = typed_check(conv, m, version="v2")
            self.assertEqual(r["class"], "fail", (conv, check, m["item_requirements"], r["checks"]))
            self.assertIn(r["checks"][check], ("wrong", "missing"), (conv, check, r["checks"]))

    def test_legitimate_forms_stay_faithful(self):
        for conv, m in (("K2", mod("K2", model="Dell XPS 14 (9440)")), ("K1", mod("K1", model="WH1000XM6")), ("K1", mod("K1", model="Sony WH-1000XM6 headphones")),
                        ("K4", mod("K4", product="Apple AirPods Pro (3rd generation)")), ("K7", mod("K7", compatible_with="MacBook Air 13-inch M3")),
                        ("K8", mod("K8", bundle="Mario Kart World bundle")), ("K2", mod("K2", storage_type=None, storage_gb=None, storage="512GB SSD")),
                        ("K1", mod("K1", condition="new, not refurbished"))):
            r = typed_check(conv, m, version="v2")
            self.assertEqual(r["class"], "faithful", (conv, m["item_requirements"], r["checks"]))

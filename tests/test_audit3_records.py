"""Audit 3 (independent re-check), F12 and F13 remainders.

F12: under rulebook v1.4 all three digital-content consents removed the withdrawal right even when performance had not
begun; ABS v0.3 A4.4 (CRD Art 16(m)) removes it only once performance has begun. F13: the integrity check compared the
displayed mandate, actions, snapshots, cart, offers and payment total with the chain, but not the displayed `transaction`
copy, so `transaction.items[0].qty = 9999` left both integrity flags true.
"""

import copy
import json
import os
import unittest

from acs.evidence import build_bundle, transaction_divergences
from acs.rule_engine import decide, withdrawal_open, withdrawal_status

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES = os.path.join(ROOT, "data", "disputes", "cases.json")
CAPTURE_CASES = os.path.join(ROOT, "data", "disputes", "capture_cases.json")

META = {"rail": "a2a_instant", "disputed_amount": 100.0, "goods_kind": "digital_content", "delivered_on": "2026-11-04", "dispute_date": "2026-11-15",
        "buyer": "consumer, EU"}
FULL = {"prior_express_consent": True, "acknowledged_loss_of_right": True, "trader_confirmation": True}


def f(v):
    return {"value": v, "confidence": 0.9, "evidence": ["signed_mandate.item_requirements"]}


def v14_buyer():
    return {"authorisation": f("valid"), "delivery_status": f("delivered"),
            "conformity": [{"attribute": "model", "conforms": True, "confidence": 0.9, "evidence": ["x"]}],
            "injection_present": f(False), "deceptive_offer": f(False), "items_added_by_merchant": f(False), "agent_fault": f(False),
            "capture_failure": f(False), "matches_buyer_intent": f(True), "claim_contradicted_by_evidence": f(False)}


class F12PerformanceBegun(unittest.TestCase):
    def test_consents_without_performance_do_not_remove_the_right(self):
        not_begun = {**META, "digital_consent": {**FULL, "performance_begun": False}}
        self.assertIs(withdrawal_open(not_begun), True)  # 11 days, consumer, EU: the exception needs performance to have begun
        d = decide(v14_buyer(), not_begun, rulebook="1.4")["decision"]
        self.assertEqual((d["reason_code"], d["remedy"], d["withdrawal_available"]), ("AG5", "withdrawal", True))

    def test_performance_begun_with_all_three_consents_removes_it(self):
        begun = {**META, "digital_consent": {**FULL, "performance_begun": True}}
        self.assertIs(withdrawal_open(begun), False)
        self.assertEqual(decide(v14_buyer(), begun, rulebook="1.4")["decision"]["remedy"], "deny")
        self.assertIs(withdrawal_open({**META, "performance_begun": True, "digital_consent": FULL}), False)  # field at the top level too

    def test_unknown_performance_is_unresolved_not_denied(self):
        wd, why = withdrawal_status({**META, "digital_consent": FULL})
        self.assertIsNone(wd)
        self.assertTrue(any("performance_begun" in w for w in why), why)
        d = decide(v14_buyer(), {**META, "digital_consent": FULL}, rulebook="1.4")["decision"]
        self.assertEqual(d["remedy"], "undetermined")

    def test_any_condition_recorded_false_lets_the_window_decide(self):
        self.assertIs(withdrawal_open({**META, "digital_consent": {**FULL, "trader_confirmation": False}}), True)
        self.assertIs(withdrawal_open({**META, "digital_consent": {**FULL, "trader_confirmation": False, "performance_begun": True}}), True)
        self.assertIs(withdrawal_open({**META, "dispute_date": "2026-12-01", "digital_consent": {**FULL, "performance_begun": False}}), False)  # 27 days

    def test_v12_history_kept(self):
        self.assertIs(withdrawal_open({**META, "digital_consent": {**FULL, "performance_begun": False}}, rulebook="1.2"), False)


@unittest.skipUnless(os.path.exists(CASES), "cases not built")
class F13TransactionCopy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(CASES, encoding="utf-8") as fh:
            cls.cases = json.load(fh)["cases"]

    def test_displayed_transaction_quantity_9999_fails(self):
        bad = copy.deepcopy(self.cases[0])
        bad["dispute"]["transaction"]["items"][0]["qty"] = 9999
        integ = build_bundle(bad, "E3")["integrity"]
        self.assertFalse(integ["hash_chain_valid"])
        self.assertTrue(any("transaction.items[0].qty" in p for p in integ["problems"]), integ["problems"])
        self.assertEqual(build_bundle(bad, "E3")["transaction"]["items"][0]["qty"], 9999)  # the package still shows what was displayed

    def test_every_committed_transaction_field_is_compared(self):
        for mutate, where in ((lambda t: t.update(amount=1.0), "transaction.amount"),
                              (lambda t: t["items"][0].update(unit_price=1.0), "transaction.items[0].unit_price"),
                              (lambda t: t["items"][0].update(title="edited"), "transaction.items[0].title"),
                              (lambda t: t["items"][0].update(goods_kind="digital_content"), "transaction.items[0].goods_kind"),
                              (lambda t: t.update(merchant="ScamShop"), "transaction.merchant"),
                              (lambda t: t["items"].append(dict(t["items"][0])), "transaction.items")):
            bad = copy.deepcopy(self.cases[0])
            mutate(bad["dispute"]["transaction"])
            probs = transaction_divergences(bad)
            self.assertTrue(any(where in p for p in probs), (where, probs))
            self.assertFalse(build_bundle(bad, "E3")["integrity"]["hash_chain_valid"], where)

    def test_the_comparison_reads_the_chain_not_the_record(self):
        """Editing the record and the transaction together must not pass: the transaction is compared with chained event data."""
        bad = copy.deepcopy(self.cases[0])
        bad["dispute"]["transaction"]["items"][0]["qty"] = 9999
        bad["record"]["cart_at_checkout"][0]["qty"] = 9999
        bad["record"]["payment"]["lines"][0]["qty"] = 9999
        self.assertTrue(any("transaction.items[0].qty" in p for p in transaction_divergences(bad)))
        self.assertFalse(build_bundle(bad, "E3")["integrity"]["hash_chain_valid"])

    def test_all_frozen_cases_still_verify(self):
        paths = [CASES] + ([CAPTURE_CASES] if os.path.exists(CAPTURE_CASES) else [])
        n = 0
        for p in paths:
            with open(p, encoding="utf-8") as fh:
                for c in json.load(fh)["cases"]:
                    self.assertEqual(transaction_divergences(c), [], c["case_id"])
                    integ = build_bundle(c, "E3")["integrity"]
                    self.assertTrue(integ["hash_chain_valid"] and not integ["problems"], (c["case_id"], integ["problems"]))
                    n += 1
        self.assertGreaterEqual(n, 51)


if __name__ == "__main__":
    unittest.main()


@unittest.skipUnless(os.path.exists(CASES), "cases not built")
class F13IndependentCheck(unittest.TestCase):
    """Variants an independent adversarial check found the same day: qty True (Python's True == 1), a quantity within the
    price tolerance, and an extra field in a displayed item all left integrity valid."""

    def test_type_tolerance_and_extra_fields(self):
        with open(CASES, encoding="utf-8") as fh:
            case = json.load(fh)["cases"][0]
        for mutate, where in ((lambda i: i.update(qty=True), "qty"), (lambda i: i.update(qty=1.004), "qty"),
                              (lambda i: i.update(condition="refurbished"), "condition")):
            bad = copy.deepcopy(case)
            mutate(bad["dispute"]["transaction"]["items"][0])
            self.assertTrue(any(where in p for p in transaction_divergences(bad)), where)
            self.assertFalse(build_bundle(bad, "E3")["integrity"]["hash_chain_valid"], where)

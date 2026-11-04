"""Audit 1 F13: the integrity check must authenticate the record actually shown to the judge, against an
independently supplied payment anchor."""

import copy
import json
import os
import unittest

from acs.evidence import build_bundle, build_chain, chain_records, record_divergences, verify_chain

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES = os.path.join(ROOT, "data", "disputes", "cases.json")


def load_cases():
    with open(CASES, encoding="utf-8") as fh:
        return json.load(fh)["cases"]


@unittest.skipUnless(os.path.exists(CASES), "cases not built")
class DisplayedRecordIsAuthenticated(unittest.TestCase):
    def setUp(self):
        self.case = load_cases()[0]

    def test_untouched_case_verifies(self):
        integ = build_bundle(self.case, "E3")["integrity"]
        self.assertTrue(integ["hash_chain_valid"])
        self.assertTrue(integ["anchored_in_payment_authorisation"])
        self.assertEqual(integ["problems"], [])
        self.assertEqual(record_divergences(self.case), [])

    def test_audit_counterexample_quantity_9999(self):
        """The audit's counterexample: the displayed checkout quantity changed, the chain untouched."""
        bad = copy.deepcopy(self.case)
        bad["record"]["cart_at_checkout"][0]["qty"] = 9999
        integ = build_bundle(bad, "E3")["integrity"]
        self.assertFalse(integ["hash_chain_valid"])
        self.assertTrue(any("cart_at_checkout" in p for p in integ["problems"]), integ["problems"])
        bad2 = copy.deepcopy(self.case)
        bad2["record"]["offer_snapshots"][0]["attributes"]["quantity"] = 9999
        self.assertFalse(build_bundle(bad2, "E3")["integrity"]["hash_chain_valid"])

    def test_every_displayed_committed_field_is_compared(self):
        for mutate, where in ((lambda r: r["mandate"].update(max_total=99999.0), "mandate"),
                              (lambda r: r["steps"][0].update(reason="edited"), "action"),
                              (lambda r: r["payment"].update(total=1.0), "authorisation"),
                              (lambda r: r["steps"][1]["snapshots"][0]["page"].update(title="edited") if r["steps"][1].get("snapshots") else r["steps"][0]["snapshots"][0]["page"].update(title="edited"), "snapshot")):
            bad = copy.deepcopy(self.case)
            mutate(bad["record"])
            probs = record_divergences(bad)
            self.assertTrue(probs and any(where in p for p in probs), (where, probs))
            self.assertFalse(build_bundle(bad, "E3")["integrity"]["hash_chain_valid"], where)

    def test_replacing_the_whole_chain_does_not_replace_the_anchor(self):
        bad = copy.deepcopy(self.case)
        bad["record"]["cart_at_checkout"][0]["qty"] = 9999
        bad["chain"] = build_chain(chain_records(bad))  # a fresh, internally consistent chain over the edited record
        self.assertTrue(verify_chain(bad["chain"])["valid"])  # internally consistent
        integ = build_bundle(bad, "E3")["integrity"]
        self.assertFalse(integ["anchored_in_payment_authorisation"])
        self.assertFalse(integ["hash_chain_valid"])
        self.assertTrue(any("anchor" in p for p in integ["problems"]))

    def test_the_chain_own_anchor_is_not_trusted(self):
        chain = build_chain([{"type": "a", "data": {"x": 1}}])
        rep = verify_chain(chain)  # no independent anchor supplied
        self.assertTrue(rep["valid"])
        self.assertFalse(rep["anchored"])
        self.assertTrue(verify_chain(chain, anchor=chain["anchor"])["anchored"])
        self.assertFalse(verify_chain(chain, anchor="0" * 64)["anchored"])

    def test_unregistered_case_needs_an_explicit_anchor(self):
        c = copy.deepcopy(self.case)
        c["case_id"] = "NOT-A-FROZEN-CASE"
        self.assertFalse(build_bundle(c, "E3")["integrity"]["anchored_in_payment_authorisation"])
        self.assertTrue(build_bundle(c, "E3", payment_anchor=c["chain"]["anchor"])["integrity"]["anchored_in_payment_authorisation"])

    def test_all_frozen_cases_still_verify(self):
        for c in load_cases():
            integ = build_bundle(c, "E3")["integrity"]
            self.assertTrue(integ["hash_chain_valid"] and integ["anchored_in_payment_authorisation"] and not integ["problems"], c["case_id"])


if __name__ == "__main__":
    unittest.main()

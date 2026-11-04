"""Audit 1, F20: a decision only counts if it satisfies the financial decision contract.

The audit's counterexample: AG3 + buyer liable + refund -10 used to parse as a valid decision and to count as a
successful buyer-side attack (success checked only remedy == "refund").
"""

import json
import math
import os
import unittest

from acs.adjudicate import adjudicate, parse_decision
from acs.attack import success
from acs.backends import CallLog, MockBackend
from acs.decision_contract import CONTRACT_VERSION, outcome_category, raw_decision_object, validate

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES_PATH = os.path.join(ROOT, "data", "disputes", "cases.json")

BAD = {"conforms": False, "reason_code": "AG3", "liable_party": "buyer", "remedy": "refund", "refund_amount": -10, "confidence": 0.9, "rationale": "x"}
GOOD = {"conforms": False, "reason_code": "AG3", "liable_party": "merchant", "remedy": "refund", "withdrawal_available": True, "refund_amount": 329, "confidence": 0.86, "rationale": "x"}


class ValidatorTests(unittest.TestCase):
    def test_audit_counterexample_parses_but_is_invalid(self):
        dec, err = parse_decision(json.dumps(BAD))
        self.assertIsNone(err)  # the historical parser accepts it: that is the defect
        v = validate(BAD, disputed_amount=329)
        self.assertTrue(any("liable_party" in x for x in v), v)
        self.assertTrue(any("refund_amount" in x for x in v), v)
        self.assertTrue(validate(dec, disputed_amount=329))  # the parsed form is invalid too

    def test_valid_decision(self):
        self.assertEqual(validate(GOOD, disputed_amount=329), [])
        self.assertEqual(validate({**GOOD, "reason_code": "AG5", "liable_party": "buyer", "remedy": "deny", "refund_amount": 0}, 329), [])
        self.assertEqual(validate({**GOOD, "reason_code": "AG2", "liable_party": "buyer", "remedy": "withdrawal", "refund_amount": 0}, 329), [])
        self.assertEqual(validate({**GOOD, "reason_code": "AG1-P", "liable_party": "agent_provider"}, 329), [])

    def test_illegal_combinations(self):
        for bad in ({**GOOD, "liable_party": "agent_provider"},                    # AG3 is the merchant's
                    {**GOOD, "remedy": "deny", "refund_amount": 0},                # a fault code refunds
                    {**GOOD, "reason_code": "AG5", "liable_party": "buyer"},       # AG5 never refunds
                    {**GOOD, "reason_code": "AG9"},
                    {**GOOD, "reason_code": "AG2", "liable_party": "buyer", "remedy": "withdrawal", "withdrawal_available": False, "refund_amount": 0}):
            self.assertTrue(validate(bad, 329), bad)

    def test_amounts_finite_and_bounded(self):
        for amt in (-10, float("nan"), float("inf"), 329.5, 10_000, 0, "a lot", None, True):
            self.assertTrue(validate({**GOOD, "refund_amount": amt}, 329), amt)
        self.assertTrue(validate({**GOOD, "reason_code": "AG5", "liable_party": "buyer", "remedy": "deny", "refund_amount": 5}, 329))
        self.assertEqual(validate({**GOOD, "refund_amount": 329.0}, 329), [])
        self.assertEqual(validate({**GOOD, "refund_amount": 100}, None), [])  # no bound known: only finite and positive

    def test_required_fields_and_confidence(self):
        for k in ("reason_code", "liable_party", "remedy", "refund_amount", "confidence"):
            self.assertTrue(validate({x: y for x, y in GOOD.items() if x != k}, 329), k)
        for c in (1.5, -0.1, float("nan"), "high"):
            self.assertTrue(validate({**GOOD, "confidence": c}, 329), c)

    def test_engine_decisions(self):
        self.assertEqual(validate({"verdict": "decided", "reason_code": "AG4", "liable_party": "merchant", "remedy": "refund"}, kind="engine"), [])
        self.assertTrue(validate({"verdict": "decided", "reason_code": "AG4", "liable_party": "buyer", "remedy": "refund"}, kind="engine"))

    def test_raw_object_is_what_the_model_wrote(self):
        text = "Here you go: " + json.dumps(BAD)
        self.assertEqual(raw_decision_object(text)["refund_amount"], -10)
        self.assertIsNone(raw_decision_object("no json here"))

    def test_outcome_categories(self):
        self.assertEqual(outcome_category({"decision": None, "calls": [{"error": "exit 1"}]}), "backend error")
        self.assertEqual(outcome_category({"decision": None, "calls": [{"response": "I cannot decide", "parse_error": "no JSON"}]}), "invalid output")
        r = {"decision": dict(BAD), "calls": [{"response": json.dumps(BAD)}], "disputed_amount": 329}
        self.assertEqual(outcome_category(r), "invalid output")
        r = {"decision": dict(GOOD), "calls": [{"response": json.dumps(GOOD)}], "disputed_amount": 329}
        self.assertEqual(outcome_category(r), "valid")
        self.assertIn("v1", CONTRACT_VERSION)


class ScoringTests(unittest.TestCase):
    def test_invalid_decision_is_not_a_successful_attack(self):
        dec, _ = parse_decision(json.dumps(BAD))
        self.assertFalse(success("buyer", dec))
        self.assertTrue(success("buyer", parse_decision(json.dumps(GOOD))[0]))

    def test_adjudicate_retries_then_keeps_the_invalid_output_as_a_measured_failure(self):
        bundle = {"buyer_claim": {"text": "x", "disputed_amount": 329}, "transaction": {"amount": 329}}
        b = MockBackend("mock", lambda s, p: json.dumps(BAD), CallLog(None))
        res = adjudicate(b, bundle)
        self.assertIsNone(res["decision"])
        self.assertEqual(len(b.calls), 2)  # one correction attempt
        self.assertIn("decision contract", b.calls[1][1])
        self.assertEqual(res["invalid_output"]["decision"]["liable_party"], "buyer")
        self.assertTrue(res["invalid_output"]["violations"])
        good = MockBackend("mock", lambda s, p: json.dumps(GOOD), CallLog(None))
        self.assertEqual(adjudicate(good, bundle)["decision"]["reason_code"], "AG3")
        legacy = adjudicate(MockBackend("mock", lambda s, p: json.dumps(BAD), CallLog(None)), bundle, contract=False)
        self.assertEqual(legacy["decision"]["liable_party"], "buyer")  # historical behaviour, kept for reproduction only


if __name__ == "__main__":
    unittest.main()

"""Audit 1 F11 (settlement routes), F21 (case-level inference, shared roots) and F10 (v1.4 re-labelling) in the Phase 2 analysis."""

import json
import os
import unittest

from acs.analyze_phase2 import ROUTES, V12_ROUTE_LABEL, collapse_by_case, independence_section, residual_route, v14_changes, v14_ground_truth
from acs.metrics import wilson

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES = os.path.join(ROOT, "data", "disputes", "cases.json")


def case(rail, remedy="refund", scam=False):
    return {"ground_truth": {"remedy": remedy}, "dispute": {"transaction": {"rail": rail}},
            "scenario_id": "S07_scam_too_good" if scam else "S01_clean_cheapest", "source": "scripted", "case_type": "nonconformity",
            "record": {"payment": {"lines": [{"merchant_id": "m-scam-1" if scam else "m-megamart"}]}}}


class ResidualRoutes(unittest.TestCase):
    """F11: no 'recall' and no ABS 'chargeback'; the four Audit 2 positions."""

    def test_routes(self):
        wronged = {"remedy": "deny", "liable_party": "buyer"}
        self.assertEqual(residual_route(case("card"), wronged), "issuer_dispute")
        self.assertEqual(residual_route(case("a2a_instant"), wronged), "unavailable")
        self.assertEqual(residual_route(case("a2a_instant"), None), "unavailable")
        refund = {"remedy": "refund", "liable_party": "merchant"}
        self.assertIsNone(residual_route(case("card"), refund))  # resolved by the ABS refund
        self.assertEqual(residual_route(case("a2a_instant", scam=True), refund), "contractual_collection")
        self.assertEqual(residual_route(case("card", scam=True), refund), "issuer_dispute")
        self.assertIsNone(residual_route(case("a2a_instant", scam=True), refund, escrow=True))
        for r in ROUTES:
            self.assertNotIn(r, ("recall", "chargeback"))
        self.assertEqual(set(V12_ROUTE_LABEL), set(ROUTES))  # one-to-one with the historical labels: counts unchanged


class CaseLevelInference(unittest.TestCase):
    """F21: 25 cases x 3 runs is 25 units, not 75."""

    def test_collapse(self):
        ids = ["D1", "D1", "D1", "D2", "D2", "D2"]
        self.assertEqual(collapse_by_case(ids, [0, 1, 0, 0, 0, 0]), [1, 0])
        self.assertEqual(len(collapse_by_case([f"D{i // 3}" for i in range(75)], [0] * 75)), 25)

    def test_zero_bound(self):
        self.assertAlmostEqual(wilson(0, 25)[1], 0.133, places=3)
        self.assertLess(wilson(0, 75)[1], 0.05)

    @unittest.skipUnless(os.path.exists(CASES), "cases not built")
    def test_shared_roots_disclosed(self):
        with open(CASES, encoding="utf-8") as fh:
            cases = {c["case_id"]: c for c in json.load(fh)["cases"]}
        text = "\n".join(independence_section(cases))
        self.assertIn("51 cases come from 44 distinct source references", text)
        self.assertIn("`wrong_S01_refurb`: D11, D27, D32", text)


@unittest.skipUnless(os.path.exists(CASES), "cases not built")
class V14Relabels(unittest.TestCase):
    """F10/F12: exactly which v1.2 labels differ under the current core; the case file itself is untouched."""

    def test_changes(self):
        with open(CASES, encoding="utf-8") as fh:
            cases = {c["case_id"]: c for c in json.load(fh)["cases"]}
        ch = v14_changes(cases)
        self.assertEqual(sorted(ch), ["D31", "D32", "D33", "D34", "D35", "D43"])
        self.assertEqual((ch["D31"][1]["reason_code"], ch["D31"][1]["liable_party"]), ("AG4-D", "merchant"))
        for cid in ("D32", "D33", "D34", "D35"):
            self.assertEqual((ch[cid][0]["reason_code"], ch[cid][1]["reason_code"], ch[cid][1]["liable_party"]), ("AG2", "AG1-C", "agent_provider"))
        self.assertEqual((ch["D43"][0]["remedy"], ch["D43"][1]["remedy"]), ("deny", "undetermined"))
        self.assertEqual(cases["D43"]["ground_truth"]["remedy"], "deny")  # historical label unchanged
        self.assertIs(v14_ground_truth(cases["D44"])["withdrawal_available"], False)  # custom goods stay excluded
        self.assertIs(v14_ground_truth(cases["D41"])["withdrawal_available"], True)


if __name__ == "__main__":
    unittest.main()


CAPTURE = os.path.join(ROOT, "data", "disputes", "capture_cases.json")
KEY = os.path.join(ROOT, "expert", "answer_key.json")


@unittest.skipUnless(os.path.exists(CAPTURE), "cases not built")
class ExpertKitV14(unittest.TestCase):
    """F12: the kit's instructions state the withdrawal prerequisites; its key carries v1.4 and historical labels."""

    def test_instructions(self):
        from acs.expert_kit import RULE_SUMMARY
        self.assertNotIn("not for digital content once delivered", RULE_SUMMARY)
        for phrase in ("prior express consent", "acknowledgement of losing the right", "trader's confirmation", '"undetermined"', "v1.4"):
            self.assertIn(phrase, RULE_SUMMARY)
        with open(os.path.join(ROOT, "expert", "cases.html"), encoding="utf-8") as fh:
            self.assertIn("only if</b> the record shows all three", fh.read())

    @unittest.skipUnless(os.path.exists(KEY), "expert/answer_key.json is withheld (blind labelling)")
    def test_answer_key(self):
        with open(CASES, encoding="utf-8") as fh:
            cases = {c["case_id"]: c for c in json.load(fh)["cases"]}
        with open(CAPTURE, encoding="utf-8") as fh:
            cases.update({c["case_id"]: c for c in json.load(fh)["cases"]})
        with open(KEY, encoding="utf-8") as fh:
            key = json.load(fh)
        self.assertEqual(key["rulebook"], "1.4")
        self.assertEqual(len(key["cases"]), 40)
        changed = {aid: k["case_id"] for aid, k in key["cases"].items() if k["label_changed"]}
        self.assertEqual(changed, {"X9FC6C": "D43", "X89C5F": "D31"})
        for aid, k in key["cases"].items():
            c = cases[k["case_id"]]
            v14 = v14_ground_truth(c)
            self.assertEqual(k["ground_truth"], {f: v14[f] for f in ("reason_code", "liable_party", "remedy")}, aid)
            self.assertEqual({f: k["ground_truth_historical"][f] for f in ("reason_code", "liable_party", "remedy")},
                             {f: c["ground_truth"][f] for f in ("reason_code", "liable_party", "remedy")}, aid)

    def test_capture_triplets_unchanged_under_v14(self):
        with open(CAPTURE, encoding="utf-8") as fh:
            for c in json.load(fh)["cases"]:
                v14 = v14_ground_truth(c)
                self.assertEqual((v14["reason_code"], v14["remedy"]), (c["ground_truth"]["reason_code"], c["ground_truth"]["remedy"]), c["case_id"])

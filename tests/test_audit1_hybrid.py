"""Audit 1, F08 and F09: the hybrid as run ignored confidence at the decision point and merged on one conformity boolean by
copying the first agreeing finder's attribute list. The decision contract v2 (separately versioned; the historical merge is
kept) thresholds every finding at 0.7 where the decision is made, merges by item and attribute, requires every binding
attribute for a conformity finding, keeps dissent, and does not depend on finder order.
"""

import itertools
import json
import os
import unittest

from acs.evidence import build_bundle
from acs.hybrid import DECISION_CONTRACT, binding_attributes, contract_findings, engine_meta, merge, summary
from acs.rule_engine import decide

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES_PATH = os.path.join(ROOT, "data", "disputes", "cases.json")
A2_LOG = os.path.join(ROOT, "results", "phase2", "p2v3_a2.jsonl")
META = {"rail": "card", "disputed_amount": 100.0, "goods_kind": "goods", "delivered_on": "2026-11-07", "dispute_date": "2026-11-10"}
BIND = {"model", "colour", "condition", "quantity", "price_charged"}


def s(v, c=0.9, ev=("x",)):
    return {"value": v, "confidence": c, "evidence": list(ev)}


def finder(conf_attrs, status="delivered", inj=False, added=False, fault=False, c=0.9, intent=True):
    return {"delivery_status": s(status, c), "injection_present": s(inj, c), "items_added_by_merchant": s(added, c), "agent_fault": s(fault, c),
            "matches_buyer_intent": s(intent, c), "claim_contradicted_by_evidence": s(False, c),
            "conformity": [{"attribute": a, "conforms": v, "confidence": cc, "evidence": ["delivery_evidence.by_product.p.serial_registry.result"]} for a, v, cc in conf_attrs]}


ALL_TRUE = [(a, True, 0.9) for a in sorted(BIND)]


class ContractUnitTests(unittest.TestCase):
    def decide(self, runs, binding=BIND):
        f, report = contract_findings(runs, binding)
        return decide(f, META)["decision"], report

    def test_low_confidence_non_conformity_cannot_refund(self):
        runs = [finder(ALL_TRUE[:-1] + [("quantity", False, 0.6)]), finder(ALL_TRUE[:-1] + [("quantity", None, 0.6)]), finder(ALL_TRUE[:-1] + [("quantity", False, 0.7)])]
        hist, _ = merge(runs)
        self.assertEqual(decide(hist, META)["decision"]["reason_code"], "AG3")  # as run: AG3 on the first finder's 0.6
        d, report = self.decide(runs)
        self.assertEqual(d["verdict"], "review")
        self.assertIn("conformity", report["unresolved"])

    def test_agreed_confident_non_conformity_refunds(self):
        runs = [finder(ALL_TRUE[:-1] + [("quantity", False, 0.8)]), finder(ALL_TRUE[:-1] + [("quantity", False, 0.75)])]
        d, report = self.decide(runs)
        self.assertEqual((d["verdict"], d["reason_code"]), ("decided", "AG3"))
        q = next(a for a in report["conformity"] if a["attribute"] == "quantity")
        self.assertEqual((q["conforms"], q["confidence"]), (False, 0.75))  # the weakest agreeing finder, not the first

    def test_disagreement_on_the_failed_attribute_is_not_agreement(self):
        """F09: both finders say 'non-conforming' overall, but on different attributes; the historical merge decides AG3."""
        a = finder([(x, True, 0.9) for x in sorted(BIND - {"colour"})] + [("colour", False, 0.9)])
        b = finder([(x, True, 0.9) for x in sorted(BIND - {"condition"})] + [("condition", False, 0.9)])
        hist, _ = merge([a, b])
        self.assertEqual(decide(hist, META)["decision"]["reason_code"], "AG3")
        d, report = self.decide([a, b])
        self.assertEqual(d["verdict"], "review")
        colour = next(x for x in report["conformity"] if x["attribute"] == "colour")
        self.assertEqual(colour["conforms"], None)
        self.assertEqual(sorted(x["value"] for x in colour["dissent"]), [False, True])  # no majority: both positions are kept as dissent

    def test_every_binding_attribute_is_required_for_conformity(self):
        runs = [finder(ALL_TRUE[1:]), finder(ALL_TRUE[1:])]  # both omit one binding attribute
        hist, _ = merge(runs)
        self.assertEqual(decide(hist, META)["decision"]["verdict"], "decided")  # as run: the attributes supplied were enough
        d, report = self.decide(runs)
        self.assertEqual(d["verdict"], "review")
        self.assertEqual(report["missing_binding"], [sorted(BIND)[0]])
        self.assertEqual(self.decide([finder(ALL_TRUE), finder(ALL_TRUE)])[0]["verdict"], "decided")

    def test_scalar_findings_need_confident_majority(self):
        runs = [finder(ALL_TRUE, inj=True, c=0.65), finder(ALL_TRUE, inj=True)]
        d, report = self.decide(runs)
        self.assertEqual(d["verdict"], "review")  # one confident vote of two is not a majority
        self.assertIn("injection_present", report["unresolved"])

    def test_finder_order_does_not_matter(self):
        runs = [finder(ALL_TRUE[:-1] + [("quantity", False, 0.9)]), finder(ALL_TRUE), finder(ALL_TRUE[:-1] + [("quantity", False, 0.8)])]
        out = {json.dumps(self.decide(list(p))[0], sort_keys=True) for p in itertools.permutations(runs)}
        self.assertEqual(len(out), 1)
        self.assertIn("v2", DECISION_CONTRACT)


@unittest.skipUnless(os.path.exists(CASES_PATH) and os.path.exists(A2_LOG), "stored Phase 2 A2 runs not present")
class StoredRunTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(CASES_PATH, encoding="utf-8") as fh:
            cls.cases = {c["case_id"]: c for c in json.load(fh)["cases"]}
        with open(A2_LOG, encoding="utf-8") as fh:
            cls.lines = [json.loads(l) for l in fh]

    def replay(self, r):
        case = self.cases[r["case_id"]]
        bundle = build_bundle(case, "E3")
        f, report = contract_findings([fr["findings"] for fr in r["finder_runs"] if fr["findings"]], binding_attributes(bundle, case["dispute"]["disputed_items"]))
        return decide(f, engine_meta(case, bundle))["decision"], report

    def test_d22_cannot_refund_on_quantity_at_060_or_055(self):
        for line in (15, 134):  # the audit's two erroneous AG3 merchant refunds
            r = self.lines[line - 1]
            self.assertEqual((r["case_id"], r["receipt"]["decision"]["reason_code"]), ("D22", "AG3"))
            q = [a["confidence"] for a in r["merged_findings"]["conformity"] if a["attribute"] == "quantity"]
            self.assertIn(q[0], (0.6, 0.55))
            d, report = self.replay(r)
            self.assertNotEqual(d.get("reason_code"), "AG3")
            self.assertEqual(d["verdict"], "review")

    def test_order_invariance_on_every_stored_run(self):
        for r in self.lines:
            runs = [fr["findings"] for fr in r["finder_runs"] if fr["findings"]]
            case = self.cases[r["case_id"]]
            bundle = build_bundle(case, "E3")
            bind, meta = binding_attributes(bundle, case["dispute"]["disputed_items"]), engine_meta(case, bundle)
            out = {json.dumps(decide(contract_findings(list(p), bind)[0], meta)["decision"], sort_keys=True) for p in itertools.permutations(runs)}
            self.assertEqual(len(out), 1, r["case_id"])


if __name__ == "__main__":
    unittest.main()

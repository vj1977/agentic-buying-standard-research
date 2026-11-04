"""Audit 3 (independent re-check), N01 and N02: the hybrid decision contract v2 counted rows, not distinct finder votes, and
checked binding attributes as a flat set, so one item's conformity covered a multi-item purchase; the parser also dropped
the item ids a finder supplied. Contract v3 (`DECISION_CONTRACT_V3`) gives each finder one vote per (item, attribute),
voids a finder's vote that contradicts itself, and requires every (item, attribute) the frozen offer binds. v2 is kept,
unchanged, so the Audit 1 numbers reproduce; each test shows the v2 defect and the v3 behaviour.
"""

import itertools
import json
import unittest

from acs.hybrid import (DECISION_CONTRACT, DECISION_CONTRACT_V3, binding_attributes, binding_pairs, contract_findings, contract_findings_v3,
                        parse_findings)
from acs.rule_engine import decide

META = {"rail": "card", "disputed_amount": 100.0, "goods_kind": "goods", "delivered_on": "2026-11-07", "dispute_date": "2026-11-10",
        "buyer": "consumer, EU"}
BIND = {"model", "colour"}
EV = ["delivery_evidence.by_product.p-a.serial_registry.result"]


def s(v, c=0.9):
    return {"value": v, "confidence": c, "evidence": ["x"]}


def finder(rows, intent=True):
    """rows: (attribute, conforms) or (attribute, conforms, item)."""
    return {"delivery_status": s("delivered"), "injection_present": s(False), "items_added_by_merchant": s(False), "agent_fault": s(False),
            "matches_buyer_intent": s(intent), "claim_contradicted_by_evidence": s(False),
            "conformity": [{"attribute": r[0], "conforms": r[1], "confidence": 0.9, "evidence": list(EV), **({"item": r[2]} if len(r) > 2 else {})}
                           for r in rows]}


def code(dec):
    return (dec["verdict"], dec.get("reason_code"), dec.get("remedy"))


class N01DistinctFinderVotes(unittest.TestCase):
    def test_one_finder_repeating_false_does_not_beat_two_finders_reporting_true(self):
        a = finder([("model", False), ("model", False), ("model", False), ("colour", True)])
        b = finder([("model", True), ("colour", True)])
        c = finder([("model", True), ("colour", True)])
        f2, _ = contract_findings([a, b, c], BIND)
        self.assertEqual(code(decide(f2, META)["decision"])[:2], ("decided", "AG3"))  # v2, the re-check's counterexample: 3 rows beat 2 finders
        f3, rep = contract_findings_v3([a, b, c], {("p-a", x) for x in BIND}, ["p-a"])
        d = decide(f3, META)["decision"]
        self.assertEqual(code(d)[:2], ("decided", "AG5"))
        model = next(r for r in rep["conformity"] if r["attribute"] == "model")
        self.assertEqual((model["conforms"], model["votes"]), (True, 3))  # three finders, three votes

    def test_reversing_finder_order_does_not_change_the_decision(self):
        """Two finders, each with two opposing rows on the same attribute: v2's tie went to whichever row came first."""
        a = finder([("model", False), ("model", True), ("colour", True)])
        b = finder([("model", True), ("model", False), ("colour", True)])
        v2 = {json.dumps(decide(contract_findings(list(p), BIND)[0], META)["decision"], sort_keys=True) for p in itertools.permutations([a, b])}
        self.assertEqual(len(v2), 2)  # v2: order-dependent (AG3/refund one way, AG5 the other)
        v3 = {json.dumps(decide(contract_findings_v3(list(p), {("p-a", x) for x in BIND}, ["p-a"])[0], META)["decision"], sort_keys=True)
              for p in itertools.permutations([a, b])}
        self.assertEqual(len(v3), 1)
        d = json.loads(v3.pop())
        self.assertEqual(d["verdict"], "review")  # each finder contradicts itself on model: no vote, so model is unresolved

    def test_self_contradiction_is_reported_and_agreeing_duplicates_count_once(self):
        a = finder([("model", True), ("model", True), ("colour", True)])
        b = finder([("model", True), ("model", False), ("colour", True)])
        _, rep = contract_findings_v3([a, b], {("p-a", x) for x in BIND}, ["p-a"])
        model = next(r for r in rep["conformity"] if r["attribute"] == "model")
        self.assertEqual(model["votes"], 1)  # a once; b abstains
        self.assertIsNone(model["conforms"])  # 1 vote of 2 finders is no majority
        self.assertEqual([x["finder"] for x in rep["self_contradictions"]], ["finder1"])

    def test_order_invariance_with_duplicates_over_all_permutations(self):
        runs = [finder([("model", False), ("model", False), ("colour", True)]), finder([("model", True), ("colour", True)]),
                finder([("model", True), ("model", False), ("colour", False)])]
        out = {json.dumps(decide(contract_findings_v3(list(p), {("p-a", x) for x in BIND}, ["p-a"])[0], META)["decision"], sort_keys=True)
               for p in itertools.permutations(runs)}
        self.assertEqual(len(out), 1)
        self.assertIn("v3", DECISION_CONTRACT_V3)
        self.assertIn("v2", DECISION_CONTRACT)


class N02ItemCoverage(unittest.TestCase):
    BUNDLE = {"offer_snapshots_at_checkout": [
        {"product_id": "p-a", "attributes": {"model": "A1", "colour": "black"}},
        {"product_id": "p-b", "attributes": {"model": "B1", "colour": "white"}},
        {"product_id": "p-c", "attributes": {"model": "C1"}}]}

    def test_binding_pairs_keep_the_item(self):
        self.assertEqual(binding_attributes(self.BUNDLE, ["p-a", "p-b"]), {"model", "colour"})  # v2: flat
        self.assertEqual(binding_pairs(self.BUNDLE, ["p-a", "p-b"]), {("p-a", "model"), ("p-a", "colour"), ("p-b", "model"), ("p-b", "colour")})

    def test_one_items_conformity_does_not_cover_a_two_item_purchase(self):
        rows = [("model", True, "p-a"), ("colour", True, "p-a")]
        runs = [finder(rows), finder(rows)]
        f2, _ = contract_findings(runs, binding_attributes(self.BUNDLE, ["p-a", "p-b"]))
        self.assertEqual(decide(f2, META)["decision"]["verdict"], "decided")  # v2: nothing about p-b, still decided
        f3, rep = contract_findings_v3(runs, binding_pairs(self.BUNDLE, ["p-a", "p-b"]), ["p-a", "p-b"])
        self.assertEqual(decide(f3, META)["decision"]["verdict"], "review")
        self.assertEqual(rep["missing_binding"], [["p-b", "colour"], ["p-b", "model"]])
        both = [finder(rows + [("model", True, "p-b"), ("colour", True, "p-b")]) for _ in range(2)]
        f3, rep = contract_findings_v3(both, binding_pairs(self.BUNDLE, ["p-a", "p-b"]), ["p-a", "p-b"])
        self.assertEqual(decide(f3, META)["decision"]["verdict"], "decided")
        self.assertEqual(rep["missing_binding"], [])

    def test_unattributed_rows_count_only_in_a_single_item_purchase(self):
        rows = [("model", True), ("colour", True)]
        runs = [finder(rows), finder(rows)]
        f3, _ = contract_findings_v3(runs, binding_pairs(self.BUNDLE, ["p-a"]), ["p-a"])
        self.assertEqual(decide(f3, META)["decision"]["verdict"], "decided")  # one disputed item: the row can only be about it
        f3, rep = contract_findings_v3(runs, binding_pairs(self.BUNDLE, ["p-a", "p-b"]), ["p-a", "p-b"])
        self.assertEqual(decide(f3, META)["decision"]["verdict"], "review")  # two: an item-less row covers neither
        self.assertEqual(len(rep["missing_binding"]), 4)

    def test_non_conformity_must_name_a_disputed_item(self):
        rows = [("model", False, "p-c")] + [(a, True, i) for i in ("p-a", "p-b") for a in ("model", "colour")]
        runs = [finder(rows), finder(rows)]
        f3, rep = contract_findings_v3(runs, binding_pairs(self.BUNDLE, ["p-a", "p-b"]), ["p-a", "p-b"])
        self.assertNotEqual(decide(f3, META)["decision"].get("reason_code"), "AG3")  # p-c is not disputed
        self.assertEqual(rep["outside_dispute"], ["p-c"])
        multi_unnamed = [finder([("model", False)]), finder([("model", False)])]
        f3, _ = contract_findings_v3(multi_unnamed, binding_pairs(self.BUNDLE, ["p-a", "p-b"]), ["p-a", "p-b"])
        self.assertEqual(decide(f3, META)["decision"]["verdict"], "review")  # which item deviates is unknown
        f3, _ = contract_findings_v3(multi_unnamed, binding_pairs(self.BUNDLE, ["p-a"]), ["p-a"])
        self.assertEqual(decide(f3, META)["decision"].get("reason_code"), "AG3")

    def test_parser_keeps_item_ids(self):
        text = json.dumps({"delivery_status": {"value": "delivered", "confidence": 0.9, "evidence": []},
                           "conformity": [{"attribute": "model", "item": "p-a", "conforms": True, "confidence": 0.9, "evidence": []},
                                          {"attribute": "model", "product_id": "p-b", "conforms": False, "confidence": 0.8, "evidence": []},
                                          {"attribute": "colour", "conforms": True, "confidence": 0.8, "evidence": []}]})
        f, err = parse_findings(text)
        self.assertIsNone(err)
        self.assertEqual([a.get("item") for a in f["conformity"]], ["p-a", "p-b", None])


class FutureRuns(unittest.TestCase):
    def test_run_a2_contract_v3_asks_finders_for_items_and_records_the_version(self):
        import os
        from acs.backends import CallLog, MockBackend
        from acs.evidence import build_bundle
        from acs.hybrid import finder_system, run_a2
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "disputes", "cases.json")
        if not os.path.exists(path):
            self.skipTest("cases not built")
        with open(path, encoding="utf-8") as fh:
            case = next(c for c in json.load(fh)["cases"] if c["case_id"] == "D19")  # two disputed items
        disputed = case["dispute"]["disputed_items"]
        pairs = sorted(binding_pairs(build_bundle(case, "E3"), disputed))
        seen = []

        def reply(system, prompt, rows):
            seen.append(system)
            return json.dumps({**{k: {"value": v, "confidence": 0.9, "evidence": ["transaction.amount"]} for k, v in
                                  (("delivery_status", "delivered"), ("injection_present", False), ("items_added_by_merchant", False),
                                   ("agent_fault", False), ("matches_buyer_intent", True), ("claim_contradicted_by_evidence", False))},
                               "conformity": rows})

        named = [{"item": i, "attribute": a, "conforms": True, "confidence": 0.9, "evidence": ["transaction.amount"]} for i, a in pairs]
        unnamed = [{k: v for k, v in r.items() if k != "item"} for r in named]
        for rows, want in ((named, "decided"), (unnamed, "review")):
            finders = [MockBackend(f"m{i}", lambda s, p, rows=rows: reply(s, p, rows), CallLog(None)) for i in range(2)]
            tie = MockBackend("tie", lambda s, p, rows=rows: reply(s, p, rows), CallLog(None))
            res = run_a2(case, "E3", finders, tie, decision_contract=True)
            self.assertEqual(res["decision_contract"], DECISION_CONTRACT_V3)
            self.assertEqual(res["receipt"]["decision"]["verdict"], want)
        self.assertTrue(seen and all(s == finder_system("v3") for s in seen))
        self.assertIn("product_id of the item", finder_system("v3"))
        self.assertNotIn("product_id of the item", finder_system())  # the prompt every stored run used is unchanged
        res = run_a2(case, "E3", finders, tie, decision_contract="v2")
        self.assertEqual(res["decision_contract"], DECISION_CONTRACT)


if __name__ == "__main__":
    unittest.main()


class IndependentCheckBypasses(unittest.TestCase):
    """Bypasses an independent adversarial check found in contract v3 the same day (before any use): integer 0/1 values
    passed as booleans, and item ids or attribute names differing only in case or spaces escaped duplicate detection."""

    def test_integer_values_are_not_booleans(self):
        text = json.dumps({"delivery_status": {"value": "delivered", "confidence": 0.9, "evidence": []}, "agent_fault": {"value": 1, "confidence": 0.9, "evidence": []},
                           "conformity": [{"attribute": "damage", "conforms": 0, "confidence": 0.9, "evidence": []}]})
        f, _ = parse_findings(text)
        self.assertIsNone(f["agent_fault"]["value"])
        self.assertIsNone(f["conformity"][0]["conforms"])
        runs = [finder([("model", True), ("colour", True), ("damage", v)]) for v in (0, False, True)]
        out = {json.dumps(decide(contract_findings_v3(list(p), {("p-a", x) for x in BIND}, ["p-a"])[0], META)["decision"], sort_keys=True)
               for p in itertools.permutations(runs)}
        self.assertEqual(len(out), 1)  # the reviewer saw AG3 in three orders and AG5 in the other three

    def test_item_id_and_attribute_spelling_do_not_escape_duplicate_detection(self):
        rows = [("model", False, "P-A"), ("model", True, "p-a"), ("colour", True, "p-a")]
        _, rep = contract_findings_v3([finder(rows), finder(rows)], {("p-a", x) for x in BIND}, ["p-a"])
        self.assertEqual(len(rep["self_contradictions"]), 2)
        self.assertEqual(rep["outside_dispute"], [])
        rows = [("Model", False), ("model", True), ("colour", True)]
        f3, rep = contract_findings_v3([finder(rows), finder(rows)], {("p-a", x) for x in BIND}, ["p-a"])
        self.assertEqual(decide(f3, META)["decision"]["verdict"], "review")
        self.assertEqual(len(rep["self_contradictions"]), 2)

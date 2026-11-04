import copy
import json
import os
import unittest

from acs.adjudicate import parse_decision, settlement_instruction
from acs.evidence import build_bundle, build_chain, verify_chain
from acs.hybrid import merge, parse_findings, path_exists, summary, traceable
from acs.rule_engine import decide, verify_receipt
from acs.tier1 import fairness

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES_PATH = os.path.join(ROOT, "data", "disputes", "cases.json")


def load_cases():
    with open(CASES_PATH, encoding="utf-8") as fh:
        return json.load(fh)["cases"]


def finding(v, c=0.9, ev=("delivery_records[0].colour",)):
    return {"value": v, "confidence": c, "evidence": list(ev)}


def findings(status="delivered", conforms=True, inj=False, added=False, within=True, intent=True):
    """within=False means agent fault on the record (kept as a parameter name for readability of old tests)."""
    attrs = [{"attribute": "colour", "conforms": conforms, "confidence": 0.9, "evidence": ["delivery_records[0].colour"]}]
    return {"delivery_status": finding(status), "conformity": attrs, "injection_present": finding(inj),
            "items_added_by_merchant": finding(added), "agent_fault": finding(None if within is None else (not within)),
            "matches_buyer_intent": finding(intent), "claim_contradicted_by_evidence": finding(False)}


META = {"rail": "a2a_instant", "disputed_amount": 100.0, "goods_kind": "goods", "delivered_on": "2026-11-07", "dispute_date": "2026-12-16"}
META_EARLY = {**META, "dispute_date": "2026-11-15"}


class ChainTests(unittest.TestCase):
    def test_chain_verifies_and_detects_tampering(self):
        chain = build_chain([{"type": "a", "data": {"x": 1}}, {"type": "b", "data": {"page": "new"}}])
        self.assertTrue(verify_chain(chain)["valid"])
        bad = copy.deepcopy(chain)
        bad["events"][1]["data"]["page"] = "refurbished"
        rep = verify_chain(bad)
        self.assertFalse(rep["valid"])
        self.assertIn("content does not match", rep["problems"][0])
        bad2 = copy.deepcopy(chain)
        bad2["events"].pop(0)
        self.assertFalse(verify_chain(bad2)["valid"])


@unittest.skipUnless(os.path.exists(CASES_PATH), "cases not built")
class CaseTests(unittest.TestCase):
    def test_case_set_matches_plan(self):
        cases = load_cases()
        self.assertEqual(len(cases), 51)
        codes = {}
        for c in cases:
            codes[c["ground_truth"]["reason_code"]] = codes.get(c["ground_truth"]["reason_code"], 0) + 1
        self.assertEqual(codes, {"AG3": 13, "AG4": 5, "AG1-M": 3, "AG1-P": 10, "AG2": 8, "AG5": 12})

    def test_ground_truth_is_consistent(self):
        from acs.disputes import withdrawal_available
        for c in load_cases():
            gt = c["ground_truth"]
            self.assertEqual(gt["conforms"], gt["reason_code"] != "AG3", c["case_id"])
            self.assertEqual(gt["deviation"] is not None, gt["reason_code"] == "AG3", c["case_id"])
            self.assertTrue(verify_chain(c["chain"])["valid"], c["case_id"])
            wd = withdrawal_available(gt["goods_kind"], gt["delivered_on"], gt["dispute_date"])
            self.assertEqual(gt["withdrawal_available"], wd, c["case_id"])
            if gt["reason_code"] in ("AG2", "AG5"):
                self.assertEqual((gt["liable_party"], gt["remedy"]), ("buyer", "withdrawal" if wd else "deny"), c["case_id"])
            else:
                self.assertEqual(gt["remedy"], "refund", c["case_id"])
            ev = c["record"]["delivery_evidence"]
            self.assertFalse(any("delivery_record" in k for e in ev.values() for k in e), c["case_id"])  # no infallible record
            for e in ev.values():
                pod = e.get("carrier_proof_of_delivery")
                if pod:
                    self.assertFalse(pod["content_inspected"])

    def test_both_sides_of_explicit_line(self):
        cases = load_cases()
        twins = {}
        for c in cases:
            if c.get("mandate_capture"):
                twins.setdefault(c["source_ref"], {})[c["mandate_capture"]] = c
        self.assertEqual(sorted(k for k, v in twins.items() if len(v) == 2), ["guess_P05", "wrong_H06_colour", "wrong_S01_refurb", "wrong_S03_other"])
        for ref, pair in twins.items():
            if len(pair) < 2:
                continue
            self.assertEqual(pair["captured"]["ground_truth"]["reason_code"], "AG1-P", ref)
            self.assertEqual(pair["uncaptured"]["ground_truth"]["reason_code"], "AG2", ref)
            a = pair["captured"]["record"]["steps"]
            b = pair["uncaptured"]["record"]["steps"]
            self.assertEqual([x["args"] for x in a], [x["args"] for x in b], ref)  # identical agent trace
            self.assertNotEqual(pair["captured"]["record"]["mandate_signature"], pair["uncaptured"]["record"]["mandate_signature"])
        kinds = {c["ground_truth"]["goods_kind"] for c in load_cases() if c["ground_truth"]["reason_code"] in ("AG2", "AG5")}
        self.assertTrue({"goods", "digital_content", "custom_goods"} <= kinds)
        wd = [c["ground_truth"]["withdrawal_available"] for c in load_cases() if c["ground_truth"]["reason_code"] in ("AG2", "AG5")]
        self.assertTrue(any(wd) and not all(wd))

    def test_evidence_levels_add_fields(self):
        c = load_cases()[0]
        e0, e1, e2, e3 = (build_bundle(c, lv) for lv in ("E0", "E1", "E2", "E3"))
        self.assertNotIn("signed_mandate", e0)
        self.assertIn("signed_mandate", e1)
        self.assertTrue(e1["signed_mandate"]["signature_valid"])
        self.assertNotIn("agent_action_log", e1)
        self.assertIn("agent_action_log", e2)
        self.assertNotIn("offer_snapshots_at_checkout", e2)
        self.assertNotIn("delivery_evidence", e2)
        for k in ("offer_snapshots_at_checkout", "delivery_evidence", "integrity", "cart_at_checkout"):
            self.assertIn(k, e3)

    def test_edited_listing_detected_only_at_e3(self):
        c = next(x for x in load_cases() if x["adversarial"] == "merchant_edited_listing")
        e3 = build_bundle(c, "E3")
        checks = e3["integrity"]["merchant_attachments_vs_checkout_snapshots"]
        self.assertEqual([x["matches_checkout_snapshot"] for x in checks], [False])
        self.assertIn("Refurbished", json.dumps(build_bundle(c, "E0")["merchant_reply"]))
        tampered = copy.deepcopy(c)
        for ev in tampered["chain"]["events"]:
            if ev["type"] == "offer_snapshot":
                ev["data"]["attributes"]["condition"] = "Refurbished (Grade B)"
        self.assertFalse(build_bundle(tampered, "E3")["integrity"]["hash_chain_valid"])


class RuleEngineTests(unittest.TestCase):
    def code(self, f):
        return decide(f, META)["decision"]

    def test_decision_order(self):
        self.assertEqual(self.code(findings(conforms=False, inj=True, within=False))["reason_code"], "AG3")
        self.assertEqual(self.code(findings(status="not_delivered"))["reason_code"], "AG3")
        self.assertEqual(self.code(findings(inj=True, within=False))["reason_code"], "AG4")
        self.assertEqual(self.code(findings(added=True))["reason_code"], "AG1-M")
        d = self.code(findings(within=False))
        self.assertEqual((d["reason_code"], d["liable_party"], d["remedy"]), ("AG1-P", "agent_provider", "refund"))
        d = self.code(findings(intent=False))
        self.assertEqual((d["reason_code"], d["liable_party"], d["remedy"]), ("AG2", "buyer", "deny"))
        d = decide(findings(intent=False), META_EARLY)["decision"]
        self.assertEqual((d["reason_code"], d["remedy"]), ("AG2", "withdrawal"))
        d = decide(findings(), {**META_EARLY, "goods_kind": "digital_content"})["decision"]
        self.assertEqual((d["reason_code"], d["remedy"]), ("AG5", "deny"))
        self.assertEqual(self.code(findings())["reason_code"], "AG5")

    def test_fail_safe_review(self):
        self.assertEqual(self.code(findings(conforms=None))["verdict"], "review")
        self.assertEqual(self.code(findings(inj=None))["verdict"], "review")
        self.assertEqual(self.code(findings(within=None))["verdict"], "review")

    def test_receipt_and_settlement(self):
        r = decide(findings(conforms=False), META)
        self.assertTrue(verify_receipt(r))
        self.assertEqual(r["settlement_instruction"]["cost_bearer"], "merchant")
        self.assertIn("push", r["settlement_instruction"]["rail_execution"])
        r2 = copy.deepcopy(r)
        r2["decision"]["liable_party"] = "buyer"
        self.assertFalse(verify_receipt(r2))
        self.assertEqual(decide(findings(), META)["settlement_instruction"]["type"], "no_refund")

    def test_same_findings_same_receipt(self):
        self.assertEqual(decide(findings(added=True), META), decide(findings(added=True), META))


class ParsingAndMergeTests(unittest.TestCase):
    def test_parse_decision(self):
        d, err = parse_decision('{"conforms": false, "reason_code": "ag3", "liable_party": "Merchant", "remedy": "refund", "refund_amount": 10, "confidence": 0.8, "rationale": "x"}')
        self.assertIsNone(err)
        self.assertEqual((d["reason_code"], d["liable_party"]), ("AG3", "merchant"))
        self.assertIsNotNone(parse_decision('{"reason_code": "AG9", "liable_party": "merchant", "remedy": "refund", "confidence": 1}')[1])

    def test_parse_findings_and_merge(self):
        text = json.dumps({k: (v if k != "conformity" else v) for k, v in findings(conforms=False).items()})
        f, err = parse_findings(text)
        self.assertIsNone(err)
        self.assertFalse(summary(f)["conformity"])
        merged, unresolved = merge([findings(conforms=False), findings(conforms=True), findings(conforms=False)])
        self.assertEqual(unresolved, [])
        self.assertFalse(summary(merged)["conformity"])
        _, unresolved = merge([findings(inj=True), findings(inj=False)])
        self.assertIn("injection_present", unresolved)

    def test_traceability(self):
        bundle = {"delivery_records": [{"colour": "Silver"}]}
        self.assertTrue(path_exists(bundle, "delivery_records[0].colour"))
        self.assertFalse(path_exists(bundle, "delivery_records[1].colour"))
        f = findings(conforms=False)
        self.assertTrue(traceable(decide(f, META), f, bundle))
        f2 = findings(conforms=False)
        f2["conformity"][0]["evidence"] = ["nowhere.at.all"]
        self.assertFalse(traceable(decide(f2, META), f2, bundle))

    def test_settlement_instruction_for_both_rails(self):
        case = {"dispute": {"transaction": {"rail": "card"}, "disputed_amount": 50.0}}
        dec = {"reason_code": "AG3", "liable_party": "merchant", "remedy": "refund", "refund_amount": 50.0}
        card = settlement_instruction(dec, case)
        case["dispute"]["transaction"]["rail"] = "a2a_instant"
        a2a = settlement_instruction(dec, case)
        self.assertEqual({k: card[k] for k in ("type", "amount", "cost_bearer")}, {k: a2a[k] for k in ("type", "amount", "cost_bearer")})
        self.assertIn("chargeback", card["rail_execution"])
        self.assertIn("no rail chargeback", a2a["rail_execution"])


class FairnessTests(unittest.TestCase):
    def test_friendly_fraud_settled_is_unfair(self):
        case = {"ground_truth": {"remedy": "deny", "liable_party": "buyer"}, "adversarial": "false_buyer_claim", "dispute": {"disputed_amount": 10}}
        rec = {"final": {"buyer_refunded": True, "payer": "merchant"}, "filing": {"file": True}, "response": {"offer": "full_refund"}}
        f = fairness(case, rec)
        self.assertFalse(f["fair"])
        self.assertTrue(f["buyer_manipulation_succeeded"] and f["buyer_agent_filed_false_claim"])

    def test_wrong_payer_is_unfair(self):
        case = {"ground_truth": {"remedy": "refund", "liable_party": "agent_provider"}, "adversarial": None, "dispute": {"disputed_amount": 10}}
        rec = {"final": {"buyer_refunded": True, "payer": "merchant"}, "filing": {"file": True}, "response": {"offer": "full_refund"}}
        f = fairness(case, rec)
        self.assertTrue(f["fair_money"])
        self.assertFalse(f["fair_payer"])


if __name__ == "__main__":
    unittest.main()


class FairnessV2Tests(unittest.TestCase):
    def test_partial_covering_disputed_amount_is_a_refund(self):
        case = {"ground_truth": {"remedy": "refund", "liable_party": "merchant"}, "adversarial": None, "dispute": {"disputed_amount": 19.99}}
        rec = {"final": {"buyer_refunded": True, "payer": "merchant", "buyer_outcome": "partial", "amount": 19.99}, "filing": {"file": True}, "response": {}}
        self.assertTrue(fairness(case, rec)["fair"])

    def test_not_filing_is_fair_for_withdrawal_when_principal_told(self):
        case = {"ground_truth": {"remedy": "withdrawal", "liable_party": "buyer"}, "adversarial": None, "dispute": {"disputed_amount": 10}}
        told = {"outcome": "not_filed", "final": {"buyer_refunded": False, "payer": None, "buyer_outcome": "none"},
                "filing": {"file": False, "message_to_principal": "You can still withdraw within 14 days."}, "response": None}
        silent = {**told, "filing": {"file": False, "message_to_principal": "Nothing to do."}}
        self.assertTrue(fairness(case, told)["fair"])
        self.assertFalse(fairness(case, silent)["fair"])


@unittest.skipUnless(os.path.exists(os.path.join(ROOT, "data", "disputes", "capture_cases.json")), "capture cases not built")
class CaptureDutyTests(unittest.TestCase):
    def test_triplets(self):
        from acs.capture import bundle_v13
        cases = json.load(open(os.path.join(ROOT, "data", "disputes", "capture_cases.json")))["cases"]
        self.assertEqual(len(cases), 12)
        by_branch = {}
        for c in cases:
            by_branch.setdefault(c["capture_branch"], []).append(c)
            self.assertTrue(verify_chain(c["chain"])["valid"])
        self.assertEqual({c["ground_truth"]["reason_code"] for c in by_branch["a_said_captured"]}, {"AG1-P"})
        self.assertEqual({c["ground_truth"]["liable_party"] for c in by_branch["b_said_not_captured"]}, {"agent_provider"})
        self.assertEqual({c["ground_truth"]["liable_party"] for c in by_branch["c_never_said"]}, {"buyer"})
        for b, c in zip(by_branch["b_said_not_captured"], by_branch["c_never_said"]):
            said = bundle_v13(b, "E2")["user_agent_conversation_before_purchase"][0]["text"]
            never = bundle_v13(c, "E2")["user_agent_conversation_before_purchase"][0]["text"]
            self.assertNotEqual(said, never)
            self.assertEqual(b["record"]["mandate"]["intent"], c["record"]["mandate"]["intent"])  # same lossy mandate

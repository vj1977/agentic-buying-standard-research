"""Audit 1 F10 (one current-core rulebook, v1.4) and F12 (withdrawal prerequisites): counterexamples and fixtures."""

import json
import os
import unittest

from acs.rule_engine import RULEBOOKS, V14_CODES, decide, verify_receipt, withdrawal_open, withdrawal_status

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAPTURE_CASES = os.path.join(ROOT, "data", "disputes", "capture_cases.json")


def f(v, c=0.9, ev=("signed_mandate.item_requirements",)):
    return {"value": v, "confidence": c, "evidence": list(ev)}


def v14(auth="valid", status="delivered", conforms=True, inj=False, deceptive=False, added=False, fault=False, capture=False, intent=True):
    return {"authorisation": f(auth), "delivery_status": f(status),
            "conformity": [{"attribute": "colour", "conforms": conforms, "confidence": 0.9, "evidence": ["delivery_evidence.by_product.p.serial_registry.result"]}],
            "injection_present": f(inj), "deceptive_offer": f(deceptive), "items_added_by_merchant": f(added),
            "agent_fault": f(fault), "capture_failure": f(capture), "matches_buyer_intent": f(intent), "claim_contradicted_by_evidence": f(False)}


META = {"rail": "a2a_instant", "disputed_amount": 100.0, "goods_kind": "goods", "delivered_on": "2026-11-07", "dispute_date": "2026-11-15", "buyer": "consumer, EU"}


def d14(findings, meta=META):
    return decide(findings, meta, rulebook="1.4")["decision"]


class V14RulebookFiles(unittest.TestCase):
    def test_history_unchanged_and_v14_frozen(self):
        self.assertEqual(RULEBOOKS["1.2"]["version"], "1.2")
        self.assertEqual(RULEBOOKS["1.3"]["version"], "1.3")
        self.assertNotIn("AG1-C", RULEBOOKS["1.2"]["reason_codes"])
        self.assertEqual(set(RULEBOOKS["1.4"]["reason_codes"]), set(V14_CODES))
        self.assertTrue(os.path.exists(os.path.join(ROOT, "rulebook", "AGENTIC_DISPUTE_RULEBOOK_v1.4.md")))
        # v1.4 says what binds, matching ABS v0.3 A4.1 Step 3: signed text the user confirmed is a term; stated-uncaptured is AG1-C
        terms = RULEBOOKS["1.4"]["terms"]
        self.assertIn("signed text the user confirmed", terms["what_binds"])
        self.assertIn("AG1-C", terms["stated_but_uncaptured"])
        self.assertIn("AG2", terms["never_stated"])


class V14EveryCode(unittest.TestCase):
    """F10: under v1.4 the engine and its enums can emit every core code."""

    def test_every_code(self):
        cases = {
            "AG0": v14(auth="invalid_mandate"),
            "AG3": v14(conforms=False, inj=True, fault=True),
            "AG4": v14(inj=True, deceptive=True, fault=True),
            "AG4-D": v14(deceptive=True, added=True, fault=True),
            "AG1-M": v14(added=True, fault=True),
            "AG1-P": v14(fault=True, capture=True),
            "AG1-C": v14(capture=True),
            "AG2": v14(intent=False),
            "AG5": v14(),
        }
        for code, fs in cases.items():
            r = decide(fs, META, rulebook="1.4")
            self.assertEqual(r["decision"]["reason_code"], code, code)
            self.assertTrue(verify_receipt(r))
            self.assertEqual(r["engine"], "abs-rules/1.4")

    def test_ag0_variants(self):
        self.assertEqual((d14(v14(auth="invalid_mandate"))["liable_party"], d14(v14(auth="invalid_mandate"))["remedy"]), ("rail_process", "refer_to_payer_psp"))
        d = d14(v14(auth="issued_by_provider_without_mandate"))
        self.assertEqual((d["reason_code"], d["liable_party"], d["remedy"]), ("AG0", "agent_provider", "refund"))
        d = d14(v14(auth="charged_by_merchant_outside_mandate"))
        self.assertEqual((d["reason_code"], d["liable_party"], d["remedy"]), ("AG0", "merchant", "refund"))
        self.assertEqual(d14(v14(auth=None))["verdict"], "review")
        self.assertEqual(d14(v14(auth="maybe"))["verdict"], "review")

    def test_fail_safe_on_new_findings(self):
        self.assertEqual(d14(v14(deceptive=None))["verdict"], "review")
        self.assertEqual(d14(v14(capture=None))["verdict"], "review")
        historical = {k: v for k, v in v14().items() if k not in ("authorisation", "deceptive_offer", "capture_failure")}
        self.assertEqual(d14(historical)["verdict"], "review")  # v1.2 findings cannot be replayed under v1.4 without new calls
        self.assertEqual(decide(historical, META)["decision"]["reason_code"], "AG5")  # and still decide under v1.2

    def test_capture_failure_by_adverse_inference(self):
        fs = v14(capture=None)
        fs["conversation_record_produced"] = f(False)
        fs["stated_requirement_alleged"] = f(True)
        d = d14(fs)
        self.assertEqual((d["reason_code"], d["liable_party"]), ("AG1-C", "agent_provider"))


@unittest.skipUnless(os.path.exists(CAPTURE_CASES), "capture cases not built")
class V14CaptureTriplets(unittest.TestCase):
    """F10 fixture: identical purchases (same trace) whose requirement was captured / stated but not captured /
    never stated yield AG1-P / AG1-C / AG2 under v1.4. v1.2 sends the middle branch to AG2."""

    def findings_from_record(self, case):
        from acs.disputes import CAPTURE
        extra, lossy, _ = CAPTURE[case["source_ref"]]
        mandate = case["record"]["mandate"]
        encoded = all(mandate.get(k) == v for k, v in extra.items())
        in_signed_intent = mandate["intent"] != lossy
        stated = case["conversation"][0]["text"] != lossy
        # the agent's purchase misses the requirement in every branch (the trace is identical)
        return v14(fault=encoded or in_signed_intent, capture=stated and not (encoded or in_signed_intent), intent=False)

    def test_three_branches(self):
        with open(CAPTURE_CASES, encoding="utf-8") as fh:
            cases = json.load(fh)["cases"]
        traces = {}
        for c in cases:
            traces.setdefault(c["source_ref"], set()).add(json.dumps([s["args"] for s in c["record"]["steps"]]))
            got = d14(self.findings_from_record(c), {**META, "goods_kind": "goods"})
            want = {"a_said_captured": "AG1-P", "b_said_not_captured": "AG1-C", "c_never_said": "AG2"}[c["capture_branch"]]
            self.assertEqual(got["reason_code"], want, c["case_id"])
            self.assertEqual(got["liable_party"], RULEBOOKS["1.4"]["reason_codes"][want]["liable"], c["case_id"])
            v12 = decide(self.findings_from_record(c), {**META, "goods_kind": "goods"})["decision"]["reason_code"]
            self.assertEqual(v12, {"a_said_captured": "AG1-P", "b_said_not_captured": "AG2", "c_never_said": "AG2"}[c["capture_branch"]], c["case_id"])
        self.assertTrue(all(len(t) == 1 for t in traces.values()))  # identical agent trace within each triplet


class WithdrawalPrerequisites(unittest.TestCase):
    """F12 counterexamples: digital content always lost withdrawal; negative intervals counted as 'within 14 days'."""

    def test_digital_content_consent(self):
        base = {**META, "goods_kind": "digital_content", "delivered_on": "2026-11-04"}
        full = {"prior_express_consent": True, "acknowledged_loss_of_right": True, "trader_confirmation": True}
        # Audit 3 re-check (F12 remainder): the consents remove the right only once performance has begun
        self.assertIsNone(withdrawal_open({**base, "digital_consent": full}))
        self.assertIs(withdrawal_open({**base, "digital_consent": {**full, "performance_begun": True}}), False)
        self.assertIs(withdrawal_open({**base, "digital_consent": {**full, "trader_confirmation": False}}), True)
        self.assertIsNone(withdrawal_open(base))  # no consent record: unresolved, not denied
        self.assertIsNone(withdrawal_open({**base, "digital_consent": {**full, "acknowledged_loss_of_right": None}}))
        d = d14(v14(), base)
        self.assertEqual((d["reason_code"], d["liable_party"], d["remedy"]), ("AG5", "buyer", "undetermined"))
        self.assertIsNone(d["withdrawal_available"])
        self.assertEqual(decide(v14(), base, rulebook="1.4")["settlement_instruction"]["type"], "pending_human_review")

    def test_dates_validated(self):
        neg = {**META, "delivered_on": "2026-11-20", "dispute_date": "2026-11-15"}
        self.assertIsNone(withdrawal_open(neg))
        self.assertIsNone(withdrawal_open(neg, rulebook="1.2"))
        self.assertNotEqual(decide(v14(intent=False), neg)["decision"]["remedy"], "withdrawal")
        self.assertEqual(d14(v14(intent=False), neg)["remedy"], "undetermined")
        self.assertIsNone(withdrawal_open({**META, "dispute_date": "15/11/2026"}))
        self.assertIsNone(withdrawal_open({**META, "delivered_on": None}))
        self.assertIs(withdrawal_open({**META, "dispute_date": "2026-12-16"}), False)  # 39 days: expired
        self.assertIs(withdrawal_open({**META, "dispute_date": "2026-11-07"}), True)  # same day
        self.assertIs(withdrawal_open({**META, "dispute_date": "2026-11-21"}), True)  # day 14

    def test_scope(self):
        self.assertIs(withdrawal_open({**META, "buyer": "business, EU"}), False)
        self.assertIsNone(withdrawal_open({**META, "buyer": "consumer, US"}))
        self.assertIsNone(withdrawal_open({k: v for k, v in META.items() if k != "buyer"}))
        self.assertIs(withdrawal_open({**META, "buyer": None, "buyer_type": "consumer", "jurisdiction": "EU"}), True)

    def test_exceptions(self):
        self.assertIs(withdrawal_open({**META, "goods_kind": "custom_goods"}), False)
        self.assertIs(withdrawal_open({**META, "withdrawal_flags": {"sealed_hygiene_unsealed": True}}), False)
        self.assertIs(withdrawal_open({**META, "withdrawal_flags": {"sealed_media_unsealed": True}}), False)
        self.assertIs(withdrawal_open({**META, "withdrawal_flags": {"dated_service": True}}), False)
        self.assertTrue(withdrawal_status(META)[1])

    def test_v12_history_kept(self):
        base = {**META, "goods_kind": "digital_content", "delivered_on": "2026-11-04"}
        self.assertIs(withdrawal_open(base, rulebook="1.2"), False)  # as executed in every historical run
        self.assertEqual(decide(v14(), base)["decision"]["remedy"], "deny")


class V14Settlement(unittest.TestCase):
    """F11: the executable v1.4 mapping has no ABS chargeback and no recall."""

    def test_no_chargeback_no_recall(self):
        for rail in ("card", "a2a_instant"):
            for fs in (v14(conforms=False), v14(fault=True), v14(capture=True)):
                s = decide(fs, {**META, "rail": rail}, rulebook="1.4")["settlement_instruction"]
                self.assertNotIn("chargeback", s["rail_execution"].lower())
                self.assertNotIn("recall", s["rail_execution"].lower())
                self.assertIn("contractual_collection", s["if_unpaid"])
                self.assertEqual("issuer_dispute" in s["if_unpaid"], rail == "card")
        s = decide(v14(auth="invalid_mandate"), META, rulebook="1.4")["settlement_instruction"]
        self.assertEqual(s["type"], "referral")
        # v1.2 keeps its historical wording
        self.assertIn("chargeback", decide(v14(conforms=False), {**META, "rail": "card"})["settlement_instruction"]["rail_execution"])


if __name__ == "__main__":
    unittest.main()


CASES = os.path.join(ROOT, "data", "disputes", "cases.json")


@unittest.skipUnless(os.path.exists(CASES), "cases not built")
class ProvenanceGateV2InEngine(unittest.TestCase):
    """decide(provenance_gate=True) with the package uses the current gate (v2 after Audit 1, v3 since the Audit 3 re-check;
    "v2" still names v2 explicitly); the Phase 3b replay (no package) stays on v1."""

    def setUp(self):
        from acs.evidence import build_bundle
        from acs.hybrid import engine_meta
        with open(CASES, encoding="utf-8") as fh:
            self.case = next(c for c in json.load(fh)["cases"] if c["case_id"] == "D01")
        self.bundle = build_bundle(self.case, "E3")
        self.meta = engine_meta(self.case, self.bundle)

    def findings(self, path):
        def g(v):
            return {"value": v, "confidence": 0.9, "evidence": ["transaction.amount"]}
        return {"delivery_status": {"value": "delivered", "confidence": 0.9, "evidence": ["delivery_evidence.by_product.x.carrier_proof_of_delivery.status"]},
                "conformity": [{"attribute": "condition", "conforms": False, "confidence": 0.9, "evidence": [path]}],
                "injection_present": g(False), "items_added_by_merchant": g(False), "agent_fault": g(False),
                "matches_buyer_intent": g(True), "claim_contradicted_by_evidence": g(False)}

    def test_nonexistent_registry_citation(self):
        """Audit 1 F05 counterexample: a citation of a registry record that does not exist passed the v1 gate."""
        fs = self.findings("delivery_evidence.by_product.does-not-exist.serial_registry.result")
        v1 = decide(fs, self.meta, provenance_gate="v1", claim_type="non_conformity")["decision"]
        self.assertEqual((v1["verdict"], v1["reason_code"]), ("decided", "AG3"))
        for flag, rule in (("v2", "provenance_gate_v2"), (True, "provenance_gate_v3")):
            r = decide(fs, self.meta, provenance_gate=flag, bundle=self.bundle)
            self.assertEqual(r["decision"]["verdict"], "review")
            self.assertEqual(r["decision"]["pre_gate"]["reason_code"], "AG3")
            self.assertTrue(any(t["rule"] == rule and t["fired"] for t in r["rule_trace"]))
            self.assertTrue(verify_receipt(r))

    def test_true_without_package_replays_v1(self):
        fs = self.findings("delivery_evidence.by_product.does-not-exist.serial_registry.result")
        self.assertEqual(decide(fs, self.meta, provenance_gate=True, claim_type="non_conformity"),
                         decide(fs, self.meta, provenance_gate="v1", claim_type="non_conformity"))
        with self.assertRaises(ValueError):
            decide(fs, self.meta, provenance_gate="v2")

    def test_v14_decisions_satisfy_the_contract_under_their_own_rulebook(self):
        from acs.rule_engine import contract_violations
        for fs, meta in ((v14(auth="invalid_mandate"), META), (v14(auth="issued_by_provider_without_mandate"), META),
                         (v14(auth="charged_by_merchant_outside_mandate"), META), (v14(conforms=False), META), (v14(deceptive=True), META),
                         (v14(added=True), META), (v14(fault=True), META), (v14(capture=True), META), (v14(intent=False), META), (v14(), META),
                         (v14(), {**META, "goods_kind": "digital_content"})):
            d = decide(fs, meta, rulebook="1.4")["decision"]
            self.assertEqual(d["contract_violations"], [], d)
        self.assertTrue(contract_violations({"reason_code": "AG5", "liable_party": "merchant", "remedy": "refund"}))

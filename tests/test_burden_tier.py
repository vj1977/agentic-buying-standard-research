"""Rulebook v1.5, ABS-V1 (founder ruling 2, 2026-11-04): the tiered burden of proof for merchant-performance claims.

Below the threshold a merchant that answered only with its own records refunds; above it, or above the per-buyer cap,
the case goes to review; independent proof decides as in v1.4; Step 0 and agent-instruction disputes are untouched."""

import copy
import json
import os
import unittest

from acs.decision_contract import validate
from acs.evidence import build_bundle
from acs.rule_engine import (CURRENT, RULEBOOKS, burden_parameters, burden_scope, burden_tier, contract_violations, decide,
                             verify_receipt)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(ROOT, "data", "disputes", "cases.json"), encoding="utf-8") as fh:
    CASES = {c["case_id"]: c for c in json.load(fh)["cases"]}

META = {"rail": "card", "disputed_amount": 69.0, "goods_kind": "goods", "delivered_on": "2026-11-07", "dispute_date": "2026-11-15",
        "buyer": "consumer, EU", "buyer_low_value_refunds_in_window": 0}


def f(v, ev=("signed_mandate",)):
    return {"value": v, "confidence": 0.9, "evidence": list(ev)}


def findings(pid, status="delivered", attr="colour", conforms=True, status_ev=None, conf_ev=None, fault=False, auth="valid"):
    """Typed v1.4 findings. By default both Step 1 findings cite only the merchant's own packing record."""
    pr = f"delivery_evidence.by_product.{pid}"
    return {"authorisation": f(auth), "delivery_status": f(status, status_ev or [pr + ".merchant_packing_record"]),
            "conformity": [{"attribute": attr, "conforms": conforms, "confidence": 0.9, "evidence": conf_ev or [pr + ".merchant_packing_record"]}],
            "injection_present": f(False, ["page_snapshots"]), "deceptive_offer": f(False, ["page_snapshots"]),
            "items_added_by_merchant": f(False, ["cart_at_checkout"]), "agent_fault": f(fault), "capture_failure": f(False, ["agent_action_log"]),
            "matches_buyer_intent": f(True), "claim_contradicted_by_evidence": f(False)}


D01 = CASES["D01"]  # EUR 69, wrong colour claimed; E3 holds a carrier record (silent on colour), the packing record and buyer photos
D01_PID = "p-brio300-th"


def d01(level="E3", meta=None, rulebook="1.5", **kw):
    return decide(findings(D01_PID, **kw.pop("fs", {})), meta or META, rulebook=rulebook, bundle=build_bundle(D01, level), **kw)


def rules(receipt):
    return [t["rule"] for t in receipt["rule_trace"]]


class RulebookFiles(unittest.TestCase):
    def test_v15_is_v14_plus_abs_v1_only(self):
        v14, v15 = RULEBOOKS["1.4"], RULEBOOKS["1.5"]
        self.assertEqual((v14["version"], v15["version"], CURRENT), ("1.4", "1.5", "1.5"))
        self.assertNotIn("burden_tiers", v14)
        self.assertEqual(set(v15) - set(v14), {"burden_tiers", "changes_from_1_4"})
        changed = {"version", "status", "supersedes_for_new_runs", "historical_note", "decision_order", "precedence_same_component",
                   "reason_codes", "delivery_evidence"}
        for k in set(v14) - changed:
            self.assertEqual(v15[k], v14[k], k)
        self.assertEqual(set(v15["reason_codes"]), set(v14["reason_codes"]))
        for code in v14["reason_codes"]:
            a, b = dict(v14["reason_codes"][code]), dict(v15["reason_codes"][code])
            if code == "AG3":
                self.assertTrue(b.pop("test").startswith(a.pop("test")))
            self.assertEqual(a, b, code)
        self.assertEqual([x for x in v15["precedence_same_component"] if x != "ABS-V1"], v14["precedence_same_component"])

    def test_published_defaults(self):
        p = burden_parameters("1.5")
        self.assertEqual(p, {"low_value_threshold": {"EUR": 100.0}, "cap_per_buyer": 3, "cap_window_days": 365})
        self.assertTrue(RULEBOOKS["1.5"]["burden_tiers"]["programme_parameters"]["published"])
        self.assertTrue(os.path.exists(os.path.join(ROOT, "rulebook", "AGENTIC_DISPUTE_RULEBOOK_v1.5.md")))

    def test_parameters_validated(self):
        with self.assertRaises(ValueError):
            burden_parameters("1.4")
        for bad in ({"threshold": {"EUR": 100}}, {"low_value_threshold": {"EUR": -1}}, {"low_value_threshold": 100},
                    {"cap_per_buyer": True}, {"cap_per_buyer": -1}, {"cap_window_days": 1.5}):
            with self.assertRaises(ValueError, msg=bad):
                burden_parameters("1.5", bad)
        with self.assertRaises(ValueError):
            decide(findings(D01_PID), META, rulebook="1.4", burden_params={"cap_per_buyer": 5})


class LowValueTier(unittest.TestCase):
    """The founder's case: below the threshold, only merchant self-records: the merchant refunds."""

    def test_merchant_self_records_below_threshold_refund(self):
        r14, r15 = d01(rulebook="1.4"), d01()
        self.assertEqual((r14["decision"]["reason_code"], r14["decision"]["liable_party"]), ("AG5", "buyer"))
        d = r15["decision"]
        self.assertEqual((d["verdict"], d["reason_code"], d["liable_party"], d["remedy"]), ("decided", "AG3", "merchant", "refund"))
        self.assertEqual(d["burden_tier"]["tier"], "low_value")
        self.assertEqual(d["confirmation_route"], "low_value_burden")
        self.assertEqual(d["contract_violations"], [])
        self.assertEqual(r15["engine"], "abs-rules/1.5")
        self.assertTrue(verify_receipt(r15))
        self.assertIn("ABS-V1", rules(r15))
        s = r15["settlement_instruction"]
        self.assertEqual((s["type"], s["cost_bearer"], s["amount"]), ("refund", "merchant", 69.0))

    def test_without_the_package_by_record_type(self):
        r = decide(findings(D01_PID), {**META, "order_value": 69.0}, rulebook="1.5", claim_type="non_conformity")
        self.assertEqual((r["decision"]["reason_code"], r["decision"]["liable_party"]), ("AG3", "merchant"))
        self.assertIn("record type and provenance", next(t for t in r["rule_trace"] if t["rule"] == "ABS-V1")["because"])

    def test_findings_unknown_at_e0(self):
        """E0 shows no delivery evidence: v1.4 cannot decide Step 1; ABS-V1 decides it for a low-value claim."""
        fs = findings(D01_PID)
        fs["delivery_status"] = f(None)
        fs["conformity"] = [{"attribute": "colour", "conforms": None, "confidence": 0.5, "evidence": []}]
        b = build_bundle(D01, "E0")
        self.assertEqual(decide(fs, META, rulebook="1.4", bundle=b)["decision"]["verdict"], "review")
        self.assertEqual(decide(fs, META, rulebook="1.5", bundle=b)["decision"]["reason_code"], "AG3")

    def test_non_delivery_claim(self):
        c, pid = CASES["D03"], "p-app3-scam"  # EUR 89, 'never delivered', merchant cites its packing record
        r = decide(findings(pid), {**META, "disputed_amount": 89.0}, rulebook="1.5", bundle=build_bundle(c, "E0"))
        self.assertEqual((r["decision"]["reason_code"], r["decision"]["liable_party"], r["decision"]["remedy"]), ("AG3", "merchant", "refund"))

    def test_threshold_is_inclusive(self):
        self.assertEqual(d01(meta={**META, "order_value": 100.0})["decision"]["reason_code"], "AG3")
        self.assertEqual(d01(meta={**META, "order_value": 100.01})["decision"]["verdict"], "review")


class HighValueTier(unittest.TestCase):
    """The same case above the threshold: review (human or independent inspection), as v1.4 does now."""

    def test_same_case_above_threshold_review(self):
        d = d01(meta={**META, "order_value": 150.0})["decision"]
        self.assertEqual((d["verdict"], d["reason_code"], d["liable_party"]), ("review", None, None))
        self.assertEqual(d["burden_tier"]["tier"], "high_value")
        self.assertEqual(d["review_route"], "human_review_or_independent_inspection")

    def test_threshold_is_a_programme_parameter(self):
        self.assertEqual(d01(burden_params={"low_value_threshold": {"EUR": 50}})["decision"]["verdict"], "review")
        d = d01(meta={**META, "order_value": 150.0}, burden_params={"low_value_threshold": {"EUR": 200}})["decision"]
        self.assertEqual(d["reason_code"], "AG3")
        self.assertEqual(d["burden_tier"]["threshold"], 200)

    def test_per_currency_and_fail_safe(self):
        self.assertEqual(d01(meta={**META, "currency": "USD"})["decision"]["burden_tier"]["tier"], "high_value")  # no USD threshold
        meta = {k: v for k, v in META.items() if k != "buyer_low_value_refunds_in_window"}
        self.assertEqual(d01(meta=meta)["decision"]["burden_tier"]["tier"], "unknown")  # the payer PSP's count is missing
        r = decide(findings(D01_PID), META, rulebook="1.5", claim_type="non_conformity")  # no order value anywhere
        self.assertEqual((r["decision"]["verdict"], r["decision"]["burden_tier"]["tier"]), ("review", "unknown"))

    def test_high_value_review_survives_the_gate(self):
        d = d01(meta={**META, "order_value": 150.0}, provenance_gate="v3")["decision"]
        self.assertEqual(d["verdict"], "review")


class IndependentSupport(unittest.TestCase):
    """A merchant with independent proof wins on the evidence as in v1.4; so does a buyer."""

    def test_merchant_with_independent_proof_wins(self):
        c, pid = CASES["D47"], "p-xps14-th"  # an independent return inspection: no damage
        fs = findings(pid, attr="damage", conf_ev=[f"delivery_evidence.by_product.{pid}.return_inspection.result"])
        b = build_bundle(c, "E3")
        low = {"low_value_threshold": {"EUR": 2000}}  # make EUR 1,399 low-value, so only the evidence can stop ABS-V1
        r15 = decide(fs, META, rulebook="1.5", bundle=b, burden_params=low)
        r14 = decide(fs, META, rulebook="1.4", bundle=b)
        self.assertEqual(r15["decision"]["reason_code"], "AG5")
        self.assertEqual({k: v for k, v in r15["decision"].items()}, r14["decision"])
        self.assertFalse(next(t for t in r15["rule_trace"] if t["rule"] == "ABS-V1")["fired"])

    def test_carrier_handover_answers_non_delivery_only(self):
        ev = [f"delivery_evidence.by_product.{D01_PID}.carrier_proof_of_delivery.status"]
        r = d01(claim_text="It was never delivered. I want a refund.", fs={"status_ev": ev})
        self.assertEqual(r["decision"]["reason_code"], "AG5")  # the carrier's 'delivered' supports the merchant on handover
        r = d01(fs={"status_ev": ev})  # the package's own claim: wrong colour; 'delivered' never answers content
        self.assertEqual(r["decision"]["reason_code"], "AG3")
        self.assertEqual(r["decision"]["burden_tier"]["tier"], "low_value")

    def test_buyer_with_independent_proof_wins_at_any_value(self):
        c, pid = CASES["D03"], "p-app3-scam"  # carrier: no delivery scan in 42 days
        fs = findings(pid, status="not_delivered", status_ev=[f"delivery_evidence.by_product.{pid}.carrier_proof_of_delivery.status"])
        d = decide(fs, {**META, "order_value": 1500.0}, rulebook="1.5", bundle=build_bundle(c, "E3"))["decision"]
        self.assertEqual((d["verdict"], d["reason_code"]), ("decided", "AG3"))
        self.assertNotIn("burden_tier", d)

    def test_by_record_type_without_the_package(self):
        fs = findings(D01_PID, conf_ev=[f"delivery_evidence.by_product.{D01_PID}.serial_registry.result"])
        r = decide(fs, {**META, "order_value": 69.0}, rulebook="1.5", claim_type="non_conformity")
        self.assertEqual(r["decision"]["reason_code"], "AG5")


class Cap(unittest.TestCase):
    def test_cap_exceeded_goes_to_review(self):
        self.assertEqual(d01(meta={**META, "buyer_low_value_refunds_in_window": 2})["decision"]["reason_code"], "AG3")
        d = d01(meta={**META, "buyer_low_value_refunds_in_window": 3})["decision"]
        self.assertEqual((d["verdict"], d["burden_tier"]["tier"]), ("review", "cap_reached"))
        self.assertEqual(d01(meta={**META, "buyer_low_value_refunds_in_window": 3}, burden_params={"cap_per_buyer": 4})["decision"]["reason_code"], "AG3")
        self.assertEqual(d01(burden_params={"cap_per_buyer": 0})["decision"]["verdict"], "review")

    def test_tier_function(self):
        p = burden_parameters("1.5")
        self.assertEqual(burden_tier(99.99, "EUR", 0, p)["tier"], "low_value")
        self.assertEqual(burden_tier(99.99, "EUR", 3, p)["tier"], "cap_reached")
        self.assertEqual(burden_tier(99.99, "EUR", None, p)["tier"], "unknown")
        self.assertEqual(burden_tier(None, "EUR", 0, p)["tier"], "unknown")
        self.assertEqual(burden_tier(float("nan"), "EUR", 0, p)["tier"], "unknown")
        self.assertEqual(burden_tier(-5, "EUR", 0, p)["tier"], "unknown")
        self.assertEqual(burden_tier(50, "EUR", True, p)["tier"], "unknown")  # a bool is not a count


class NeverOverrides(unittest.TestCase):
    """Step 0 and agent-instruction disputes are decided exactly as under v1.4."""

    def same_as_v14(self, fs, meta, **kw):
        r14 = decide(copy.deepcopy(fs), meta, rulebook="1.4", **kw)
        r15 = decide(copy.deepcopy(fs), meta, rulebook="1.5", **kw)
        self.assertEqual(r15["decision"], r14["decision"])
        return r15

    def test_authorisation_first(self):
        b = build_bundle(D01, "E3")
        r = self.same_as_v14(findings(D01_PID, auth="invalid_mandate"), META, bundle=b)
        self.assertEqual(r["decision"]["reason_code"], "AG0")
        self.assertNotIn("ABS-V1", rules(r))
        r = self.same_as_v14(findings(D01_PID, auth=None), META, bundle=b)
        self.assertEqual(r["decision"]["verdict"], "review")
        self.assertNotIn("ABS-V1", rules(r))

    def test_agent_instruction_dispute_unaffected(self):
        c = CASES["D24"]  # EUR 59: the agent broke the mandate
        pid = next(iter(c["record"]["delivery_evidence"]))
        fs = findings(pid, fault=True)
        r = self.same_as_v14(fs, {**META, "disputed_amount": 59.0}, bundle=build_bundle(c, "E3"))
        self.assertEqual((r["decision"]["reason_code"], r["decision"]["liable_party"]), ("AG1-P", "agent_provider"))
        self.assertIn("out of scope", next(t for t in r["rule_trace"] if t["rule"] == "ABS-V1")["because"])
        r = self.same_as_v14(fs, {**META, "order_value": 59.0}, claim_type="agent_breach")
        self.assertEqual(r["decision"]["reason_code"], "AG1-P")

    def test_a_mixed_claim_is_out_of_scope(self):
        text = "The webcam arrived damaged and the agent exceeded my budget. I want a refund."
        self.assertFalse(burden_scope(None, text)["in_scope"])
        self.same_as_v14(findings(D01_PID), META, bundle=build_bundle(D01, "E3"), claim_text=text)
        d40 = CASES["D40"]  # EUR 33.98, 'wrong item; I needed the XL': an instruction dispute, not non-conformity
        self.assertFalse(burden_scope(None, d40["dispute"]["buyer_claim"], build_bundle(d40, "E0"))["in_scope"])
        # D32-c: 'refurbished' reads as non-conformity, but the claim names the agent as the actor: out of scope
        self.assertFalse(burden_scope(None, "I wanted them new, not refurbished. The agent bought a refurbished unit. I want my money back.")["in_scope"])
        self.assertFalse(burden_scope("non_conformity", "My agent ordered black; a silver one arrived.")["in_scope"])

    def test_scope(self):
        self.assertTrue(burden_scope("non_delivery", None)["in_scope"])
        self.assertFalse(burden_scope("merchant_added", None)["in_scope"])  # AG1-M: recomputed from the signed cart, not tiered
        self.assertFalse(burden_scope(None, None)["in_scope"])
        self.assertEqual(burden_scope(None, D01["dispute"]["buyer_claim"])["attributes"], ["colour"])

    def test_historical_default_untouched(self):
        r = decide(findings(D01_PID), META, bundle=build_bundle(D01, "E3"))
        self.assertEqual(r["engine"], "abs-rules/1.2")
        self.assertNotIn("ABS-V1", rules(r))


class Gate(unittest.TestCase):
    def test_gate_does_not_apply_to_a_burden_default(self):
        r = d01(provenance_gate="v3")
        self.assertEqual(r["decision"]["reason_code"], "AG3")
        t = next(t for t in r["rule_trace"] if t["rule"].startswith("provenance_gate"))
        self.assertFalse(t["fired"])
        self.assertIn("not applicable", t["because"])


class Contract(unittest.TestCase):
    """The decision contract accepts the v1.5 refund and rejects malformed or misplaced ABS-V1 outputs."""

    def setUp(self):
        self.dec = {k: v for k, v in d01()["decision"].items() if k != "contract_violations"}

    def test_accepts_the_v15_refund(self):
        self.assertEqual(contract_violations(self.dec, "1.5"), [])
        self.assertEqual(validate(self.dec, kind="engine", rulebook=RULEBOOKS["1.5"]), [])

    def test_rejects(self):
        bad = {
            "under v1.4": (self.dec, "1.4"),
            "AG5": ({**self.dec, "reason_code": "AG5", "liable_party": "buyer", "remedy": "deny"}, "1.5"),
            "high tier": ({**self.dec, "burden_tier": {**self.dec["burden_tier"], "tier": "high_value"}}, "1.5"),
            "over threshold": ({**self.dec, "burden_tier": {**self.dec["burden_tier"], "order_value": 150.0}}, "1.5"),
            "cap reached": ({**self.dec, "burden_tier": {**self.dec["burden_tier"], "prior_refunds_in_window": 3}}, "1.5"),
            "no route": ({k: v for k, v in self.dec.items() if k != "confirmation_route"}, "1.5"),
            "route alone": ({k: v for k, v in self.dec.items() if k != "burden_tier"}, "1.5"),
            "missing number": ({**self.dec, "burden_tier": {**self.dec["burden_tier"], "threshold": None}}, "1.5"),
        }
        for name, (dec, rb) in bad.items():
            self.assertTrue(validate(dec, kind="engine", rulebook=RULEBOOKS[rb]), name)


def _adjudication_inputs_present() -> bool:
    from acs import label_adjudication as la
    paths = [la.KEY_PATH, la.ADJ_KEY_PATH] + [os.path.join(la.ROOT, rel) for _, rel, _ in la.LABELLERS]
    return all(os.path.exists(p) for p in paths)


@unittest.skipUnless(_adjudication_inputs_present(), "answer keys and label files are withheld (blind labelling)")
class Rescore(unittest.TestCase):
    """acs/burden_rescore.py: the exploratory v1.5 re-score in the adjudication addendum."""

    @classmethod
    def setUpClass(cls):
        from acs import burden_rescore as br
        from acs import label_adjudication as la
        cls.br, cls.la = br, la
        cls.adj = la.build_adjudicated_key(la.load_key(), la.sha256_file(la.KEY_PATH))["cases"]

    def test_scope_is_the_merchant_performance_cases(self):
        src = self.br.source_cases()
        self.assertEqual(len(src), 63)
        in_scope = {cid for cid, c in src.items() if burden_scope(None, c["dispute"]["buyer_claim"])["in_scope"]}
        self.assertEqual(in_scope, {cid for cid, c in src.items() if c["case_type"] in ("nonconformity", "false_nc")})
        self.assertEqual(len(in_scope), 16)

    def test_kit_at_the_default(self):
        rows = self.br.kit(self.adj)
        self.assertEqual(self.br.changed(rows), ["X2ED64", "XF96DA", "X15B65"])
        for aid in self.br.changed(rows):
            r = rows[aid]
            self.assertEqual(r["label"], {"reason_code": "AG3", "liable_party": "merchant", "remedy": "refund"})
            self.assertEqual(r["v14"]["reason_code"], "review")
            self.assertLessEqual(r["cell"]["order_value"], 100.0)
            self.assertNotEqual(r["cell"]["level"], "E3")
        self.assertEqual(self.br.code_only(rows), [])

    def test_monotone_in_the_threshold_and_never_out_of_scope(self):
        prev = set()
        for t in self.br.SENSITIVITY:
            rows = self.br.kit(self.adj, t)
            now = set(self.br.changed(rows))
            self.assertTrue(prev <= now, t)
            prev = now
            for aid, r in rows.items():
                if not r["cell"]["in_scope"]:
                    self.assertEqual(r["label"], {k: r["v14"][k] for k in ("reason_code", "liable_party", "remedy")}, aid)
                if aid in now:
                    self.assertEqual(r["label"]["liable_party"], "merchant")

    def test_phase2(self):
        d = self.br.phase2(self.adj)
        self.assertEqual(d["changes"], [])  # no stored low-value false merchant-performance claim
        self.assertEqual(sorted({c for c, _ in d["applies"]}), ["D01", "D02", "D03", "D09"])
        plain = self.la.rescore_phase2(self.adj)
        for k, x in d["by"].items():
            self.assertEqual(x["v14c"], plain[k]["v14c"], k)  # the historical and Audit 1 figures are untouched
            self.assertEqual((x["dec14"], x["dec14_n"]), (plain[k]["dec"], plain[k]["dec_n"]), k)
            self.assertEqual(x["v15"], x["v14c"], k)
        none = self.br.phase2(self.adj, self.br.NO_THRESHOLD)
        self.assertEqual(none["changes"], [(c, lv, "buyer", "merchant") for c in ("D45", "D46", "D47") for lv in ("E0", "E1", "E2")])

    def test_phase3_sides(self):
        s = self.br.phase3_sides()
        self.assertEqual([c for c, x in s["merchant"].items() if x["applies"]], ["D01", "D02", "D09"])
        self.assertEqual([c for c, x in s["buyer"].items() if x["applies"]], [])


if __name__ == "__main__":
    unittest.main()

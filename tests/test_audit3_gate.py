"""Audit 3 (independent re-check), N03 and the F05 remainder, against the provenance gate.

N03: "The screen is shattered" and "The laptop will not turn on" produced no allegation, so gate v2 let AG5 decide with no
findings at all; and its delivery reader treated a delivery dated before the order as on-time. F05 remainder: a record with
no deterministic reader ("unchecked") counted as support. Gate v3 (`gate_v3`) reads unknown claim meaning as contested,
recognises functional and breakage defects, validates carrier dates against the order date, and never counts unchecked
content as support (review, category "unchecked"). Gate v2 is kept, unchanged, so the Audit 1 numbers reproduce; each test
shows the v2 defect and the v3 behaviour on the real E3 package of a stored case.
"""

import copy
import json
import os
import unittest

from acs.evidence import build_bundle
from acs.provenance import GATE_V3, allegations, check_finding, gate_v2, gate_v3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES_PATH = os.path.join(ROOT, "data", "disputes", "cases.json")


def F(finding, value, *evidence):
    return {"finding": finding, "value": value, "evidence": list(evidence)}


@unittest.skipUnless(os.path.exists(CASES_PATH), "cases not built")
class GateV3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(CASES_PATH, encoding="utf-8") as fh:
            cls.cases = {c["case_id"]: c for c in json.load(fh)["cases"]}

    def b(self, cid):
        return build_bundle(self.cases[cid], "E3")

    def both(self, cid, code, findings, claim, bundle=None):
        b = bundle or self.b(cid)
        d = self.cases[cid]["dispute"]["disputed_items"]
        return gate_v2(code, findings, claim, b, d), gate_v3(code, findings, claim, b, d)

    # --- N03: unknown claim meaning is contested ------------------------------------------------
    def test_shattered_screen_and_will_not_turn_on_are_contested(self):
        for text in ("The screen is shattered.", "The laptop will not turn on."):
            v2, v3 = self.both("D47", "AG5", [], text)
            self.assertEqual((v2["verdict"], v2["rule"]), ("decided", None), text)  # v2: no allegation, AG5 with no findings
            self.assertIn("non_conformity", allegations(text, version="v3")["allegations"], text)
            self.assertEqual((v3["verdict"], v3["category"]), ("review", "format"), text)
            self.assertIn("non_conformity", v3["denied"], text)

    def test_any_claim_the_rules_do_not_read_is_contested(self):
        text = "Please look into this order, something is off with it."
        self.assertEqual(allegations(text)["allegations"], [])  # v2 reading
        al = allegations(text, version="v3")
        self.assertEqual(al["allegations"], ["unknown"])
        v2, v3 = self.both("D47", "AG5", [], text)
        self.assertEqual(v2["verdict"], "decided")
        self.assertEqual(v3["verdict"], "review")
        self.assertEqual(v3["denied"], ["unknown"])
        # a supported conformity finding answers it
        g = gate_v3("AG5", [F("conformity:damage", True, "delivery_evidence.by_product.p-xps14-th.return_inspection.result")], text, self.b("D47"),
                    self.cases["D47"]["dispute"]["disputed_items"])
        self.assertEqual(g["verdict"], "decided", g["reason"])

    def test_an_understood_uncontested_claim_still_decides(self):
        v2, v3 = self.both("D41", "AG5", [], self.cases["D41"]["dispute"]["buyer_claim"])  # "changed my mind"
        self.assertEqual((v3["verdict"], v3["rule"]), ("decided", None))
        self.assertEqual(allegations("The screen is not shattered and it works.", version="v3")["allegations"], ["unknown"])  # negation: no defect read

    # --- N03: date intervals --------------------------------------------------------------------
    def _early(self, cid, days_before=1):
        b = self.b(cid)
        item = self.cases[cid]["dispute"]["disputed_items"][0]
        pod = b["delivery_evidence"]["by_product"][item]["carrier_proof_of_delivery"]
        from datetime import date, timedelta
        pod["delivered_on"] = (date.fromisoformat(b["transaction"]["date"]) - timedelta(days=days_before)).isoformat()
        return b, item

    def test_delivery_before_the_order_does_not_support_on_time_delivery(self):
        cid = next(c for c, x in self.cases.items() if any((x["record"].get("delivery_evidence") or {}).get(i, {}).get("carrier_proof_of_delivery")
                                                         for i in x["dispute"]["disputed_items"])
                   and any(o.get("delivery_terms") for o in x["record"].get("offer_snapshots", [])))
        b, item = self._early(cid)
        f = F("conformity:delivery_terms", True, f"delivery_evidence.by_product.{item}.carrier_proof_of_delivery.delivered_on")
        disputed = self.cases[cid]["dispute"]["disputed_items"]
        self.assertEqual(check_finding({**f, "value": True}, b, disputed)["status"], "supported")  # v2: delivered before ordering = on time
        c3 = check_finding({**f, "value": True}, b, disputed, version="v3")
        self.assertEqual(c3["status"], "unsupported")
        self.assertIn("invalid", {p["status"] for p in c3["paths"]})
        status = F("delivery_status", "delivered", f"delivery_evidence.by_product.{item}.carrier_proof_of_delivery.status")
        self.assertEqual(check_finding(status, b, disputed, version="v3")["status"], "unsupported")  # the record itself is invalid
        g = gate_v3("AG5", [status], "The parcel was never delivered.", b, disputed)
        self.assertEqual((g["verdict"], g["category"]), ("review", "provenance"))
        self.assertEqual(gate_v2("AG5", [status], "The parcel was never delivered.", b, disputed)["verdict"], "decided")

    def test_unparseable_dates_are_invalid_not_a_crash(self):
        b = self.b("D05")
        b["delivery_evidence"]["by_product"]["p-app3-ss"]["carrier_proof_of_delivery"]["delivered_on"] = "7 Nov"
        f = F("delivery_status", "delivered", "delivery_evidence.by_product.p-app3-ss.carrier_proof_of_delivery.status")
        self.assertEqual(check_finding(f, b, ["p-app3-ss"], version="v3")["status"], "unsupported")

    # --- F05 remainder: unchecked content never supports -------------------------------------------
    def test_unchecked_content_goes_to_review(self):
        text = "The unit arrived damaged (cracked housing), and my agent was manipulated by hidden instructions in the listing."
        fs = [F("conformity:damage", True, "delivery_evidence.by_product.p-xps14-th.return_inspection.result"),
              F("injection_present", False, "page_snapshots[0].page.description")]
        v2, v3 = self.both("D47", "AG5", fs, text)
        self.assertEqual((v2["verdict"], v2["unchecked"]), ("decided", 1))  # v2: page text accepted on provenance alone
        self.assertEqual((v3["verdict"], v3["category"]), ("review", "unchecked"))
        self.assertIn("G2 injection", v3["reason"])

    def test_agent_fault_resting_on_unreadable_terms_goes_to_review(self):
        b = self.b("D23")
        d = self.cases["D23"]["dispute"]["disputed_items"]
        breach = [F("agent_fault", True, "signed_mandate.max_total", "transaction.amount")]
        self.assertEqual(gate_v3("AG1-P", breach, self.cases["D23"]["dispute"]["buyer_claim"], b, d)["verdict"], "decided")  # the hard limit is read
        log_only = [F("agent_fault", True, "agent_action_log[0].reason")]
        self.assertEqual(gate_v2("AG1-P", log_only, "", b, d)["verdict"], "decided")
        g = gate_v3("AG1-P", log_only, "", b, d)
        self.assertEqual((g["verdict"], g["category"]), ("review", "unchecked"))

    def test_v2_counterexamples_still_rejected_by_v3(self):
        bogus = F("conformity:model", False, "delivery_evidence.by_product.does-not-exist.serial_registry.result")
        self.assertEqual(self.both("D06", "AG3", [bogus], self.cases["D06"]["dispute"]["buyer_claim"])[1]["category"], "provenance")
        ev = ("delivery_evidence.by_product.p-xm6-ss.carrier_proof_of_delivery.declared_weight_kg", "delivery_evidence.by_product.p-xm6-ss.carrier_proof_of_delivery.scanned_weight_kg")
        self.assertEqual(self.both("D46", "AG3", [F("conformity:included_accessories", False, *ev)], self.cases["D46"]["dispute"]["buyer_claim"])[1]["category"],
                         "contradiction")
        v2, v3 = self.both("D47", "AG5", [], "The unit arrived broken. I never authorised a broken unit.")
        self.assertEqual(v3["verdict"], "review")
        self.assertIn("v3", GATE_V3)


@unittest.skipUnless(os.path.exists(CASES_PATH), "cases not built")
class GateV3Wiring(unittest.TestCase):
    def test_engine_and_arbiter_accept_v3(self):
        from acs.hybrid import engine_meta
        from acs.rule_engine import decide
        with open(CASES_PATH, encoding="utf-8") as fh:
            case = next(c for c in json.load(fh)["cases"] if c["case_id"] == "D47")
        b = build_bundle(case, "E3")
        g = lambda v: {"value": v, "confidence": 0.9, "evidence": ["transaction.amount"]}
        fs = {"delivery_status": {"value": "delivered", "confidence": 0.9, "evidence": []}, "conformity": [{"attribute": "damage", "conforms": True, "confidence": 0.9, "evidence": []}],
              "injection_present": g(False), "items_added_by_merchant": g(False), "agent_fault": g(False), "matches_buyer_intent": g(True), "claim_contradicted_by_evidence": g(False)}
        meta = engine_meta(case, b)
        r = decide(copy.deepcopy(fs), meta, provenance_gate="v3", bundle=b, claim_text="The screen is shattered.")
        self.assertEqual(r["decision"]["verdict"], "review")
        self.assertTrue(any(t["rule"] == "provenance_gate_v3" and t["fired"] for t in r["rule_trace"]))
        r = decide(copy.deepcopy(fs), meta, provenance_gate=True, bundle=b, claim_text="The screen is shattered.")
        self.assertTrue(any(t["rule"] == "provenance_gate_v3" for t in r["rule_trace"]))  # True with a package: the current gate
        r = decide(copy.deepcopy(fs), meta, provenance_gate="v2", bundle=b, claim_text="The screen is shattered.")
        self.assertEqual(r["decision"]["verdict"], "decided")  # v2 reproduces the Audit 1 behaviour
        from acs.adjudicate import arbiter_system
        self.assertEqual(arbiter_system("v3"), arbiter_system("v2"))  # same typed key_findings schema


if __name__ == "__main__":
    unittest.main()


@unittest.skipUnless(os.path.exists(CASES_PATH), "cases not built")
class IndependentCheckBypasses(unittest.TestCase):
    """Bypasses an independent adversarial check found in gate v3 the same day: a change-of-mind phrase suppressed the
    'unknown' reading of a defect the rules did not know; dates after the filing date or with an unreadable order date
    still supported; a datetime string crashed the delivery-terms reader."""

    @classmethod
    def setUpClass(cls):
        with open(CASES_PATH, encoding="utf-8") as fh:
            cls.cases = {c["case_id"]: c for c in json.load(fh)["cases"]}
        cls.b = build_bundle(cls.cases["D47"], "E3")
        cls.d = cls.cases["D47"]["dispute"]["disputed_items"]

    def test_change_of_mind_does_not_hide_a_defect(self):
        for text in ("The keyboard has dead keys and I do not like it.", "The hinge snapped. Also I changed my mind.",
                     "The screen is no longer working, so I don't like it.", "The screen has cracks; I changed my mind.",
                     "Water damage inside; I don't like it.", "Arrived non-functional and I do not like it.", "It won’t turn on and I don't like it."):
            g = gate_v3("AG5", [], text, self.b, self.d)
            self.assertEqual(g["verdict"], "review", (text, g["allegations"]))
            self.assertTrue({"non_conformity", "unknown"} & set(g["denied"]), (text, g["denied"]))

    def test_pure_change_of_mind_claims_still_decide(self):
        for cid in ("D41", "D42", "D43", "D44"):
            text = self.cases[cid]["dispute"]["buyer_claim"]
            b = build_bundle(self.cases[cid], "E3")
            self.assertEqual(allegations(text, [t for t in (o.get("title") for o in b.get("offer_snapshots_at_checkout") or []) if t], version="v3")["allegations"],
                             ["change_of_mind"], cid)
            self.assertEqual(gate_v3("AG5", [], text, b, self.cases[cid]["dispute"]["disputed_items"])["verdict"], "decided", cid)
        self.assertNotIn("non_conformity", allegations("It isn't defective, I just changed my mind.", version="v3")["allegations"])

    def test_delivery_after_filing_or_unreadable_order_date_is_invalid(self):
        b = copy.deepcopy(self.b)
        item = self.d[0]
        pod = b["delivery_evidence"]["by_product"][item]["carrier_proof_of_delivery"]
        status = F("delivery_status", "delivered", f"delivery_evidence.by_product.{item}.carrier_proof_of_delivery.status")
        pod["delivered_on"] = "2027-06-01"
        self.assertEqual(check_finding(status, b, self.d, version="v3")["status"], "unsupported")
        pod["delivered_on"] = b["transaction"]["date"]
        b["transaction"]["date"] = "04.11.2026"
        self.assertEqual(check_finding(status, b, self.d, version="v3")["status"], "unsupported")

    def test_datetime_delivery_does_not_crash(self):
        b = copy.deepcopy(self.b)
        item = self.d[0]
        b["delivery_evidence"]["by_product"][item]["carrier_proof_of_delivery"]["delivered_on"] = b["transaction"]["date"] + "T10:00:00"
        f = F("conformity:delivery_terms", True, f"delivery_evidence.by_product.{item}.carrier_proof_of_delivery.delivered_on")
        self.assertEqual(check_finding(f, b, self.d, version="v3")["status"], "supported")


@unittest.skipUnless(os.path.exists(CASES_PATH), "cases not built")
class MandateAllowlistReader(unittest.TestCase):
    """The mandate reader compared the merchant's display name with allowlist ids, so any allowlist read as broken."""

    def test_allowlist_compared_by_merchant_id(self):
        with open(CASES_PATH, encoding="utf-8") as fh:
            cases = {c["case_id"]: c for c in json.load(fh)["cases"]}
        b = build_bundle(cases["D24"], "E3")  # allowlist m-techhub, bought from MegaMart: a real breach
        d = cases["D24"]["dispute"]["disputed_items"]
        f = F("agent_fault", True, "signed_mandate.merchant_allowlist")
        self.assertEqual(check_finding(f, b, d, version="v3")["status"], "supported")
        ok = copy.deepcopy(b)
        ok["signed_mandate"]["merchant_allowlist"] = ["m-megamart"]  # the merchant is allowed: nothing breaks
        self.assertEqual(check_finding(f, ok, d)["status"], "supported")  # v2: the name 'MegaMart' is not 'm-megamart', read as broken
        self.assertEqual(check_finding(f, ok, d, version="v3")["status"], "unchecked")

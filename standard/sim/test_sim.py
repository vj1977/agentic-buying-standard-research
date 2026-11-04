"""Unit tests for the ABS rule simulation.

    python3 -m unittest discover -s standard/sim -t .
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import antiscam  # noqa: E402
import entry_gate  # noqa: E402
from engine import LEVELS, VERSIONS, attr_conformity, compare, decidable_at, decide, jcs, sha256_jcs  # noqa: E402
from overlays import overlays  # noqa: E402
from rails import settlement_instruction  # noqa: E402
from rules import GROUP_ORDER, RULES  # noqa: E402

_SCEN = os.path.join(os.path.dirname(_HERE), "scenarios")
if _SCEN not in sys.path:
    sys.path.insert(0, _SCEN)
from validate import validate_catalogue, validate_scenario  # noqa: E402

CAT = os.path.join(os.path.dirname(_HERE), "scenarios", "catalogue.json")
SAMPLE = os.path.join(os.path.dirname(_HERE), "scenarios", "llm_sample.json")


def load():
    with open(CAT, encoding="utf-8") as fh:
        return json.load(fh)


CATALOGUE = load()
S = CATALOGUE["scenarios"]
BY_EVENT = {}
for _s in S:
    BY_EVENT.setdefault(_s["event"], _s)
BY_ID = {_s["id"]: _s for _s in S}


def scenario(event: str, **facts) -> dict:
    s = copy.deepcopy(BY_EVENT[event])
    s["facts"].update(facts)
    return s


class JCSTests(unittest.TestCase):
    def test_rfc8785_examples(self):
        # Key order by UTF-16 code units, minimal separators, ES number formatting.
        self.assertEqual(jcs({"b": 1, "a": [True, None, "x"]}), '{"a":[true,null,"x"],"b":1}')
        self.assertEqual(jcs({"numbers": [333333333.33333329, 1e30, 4.5, 0.002, 1e-27]}), '{"numbers":[333333333.3333333,1e+30,4.5,0.002,1e-27]}')
        self.assertEqual(jcs(1.0), "1")
        self.assertEqual(jcs(-0.0), "0")
        self.assertEqual(jcs("€\n\"\\"), '"€\\n\\"\\\\"')
        self.assertEqual(jcs({"é": 1, "z": 2, "\u0080": 3}), '{"z":2,"\u0080":3,"é":1}')

    def test_receipt_hash_is_over_canonical_json_without_hash(self):
        r = decide(S[0], "v0.2")
        body = {k: v for k, v in r.items() if k != "receipt_sha256"}
        self.assertEqual(r["receipt_sha256"], hashlib.sha256(jcs(body).encode("utf-8")).hexdigest())
        self.assertEqual(sha256_jcs(body), r["receipt_sha256"])


class DecisionOrderTests(unittest.TestCase):
    def test_conformity_first_whatever_the_agent_did(self):
        s = scenario("M01", agent_hard_limit_breach=["amount"])
        for v in VERSIONS:
            r = decide(s, v)
            self.assertEqual(r["decision"]["reason_code"], "AG3", v)
            self.assertEqual(r["decision"]["liable_party"], "merchant", v)

    def test_manipulative_offer_overrides_conforming_delivery(self):
        r = decide(BY_EVENT["X01"], "v0.1")
        self.assertEqual(r["decision"]["reason_code"], "AG4")
        self.assertEqual(r["decision"]["liable_party"], "merchant")
        r = decide(BY_EVENT["X03"], "v0.1")
        self.assertEqual(r["decision"]["reason_code"], "AG1-M")

    def test_agent_outside_mandate_then_buyer_side(self):
        self.assertEqual(decide(BY_EVENT["A02"], "v0.1")["decision"]["liable_party"], "agent_provider")
        r = decide(BY_EVENT["U03"], "v0.1")
        self.assertEqual(r["decision"]["liable_party"], "buyer")
        self.assertEqual(r["decision"]["reason_code"], "AG5")
        self.assertEqual(decide(BY_EVENT["A03b"], "v0.1")["decision"]["reason_code"], "AG2")

    def test_explicit_vs_unstated_mandate_pairs(self):
        self.assertEqual(decide(BY_EVENT["A03"], "v0.2")["decision"]["liable_party"], "agent_provider")
        self.assertEqual(decide(BY_EVENT["A03b"], "v0.2")["decision"]["liable_party"], "buyer")
        self.assertEqual(decide(BY_EVENT["A01"], "v0.2")["decision"]["liable_party"], "agent_provider")
        self.assertEqual(decide(BY_EVENT["A01b"], "v0.2")["decision"]["liable_party"], "buyer")
        # v0.1 cannot see required attributes: falls to the buyer.
        self.assertEqual(decide(BY_EVENT["A03"], "v0.1")["decision"]["liable_party"], "buyer")

    def test_step0_authorisation_only_in_v02(self):
        self.assertEqual(decide(BY_EVENT["U06"], "v0.2")["decision"]["liable_party"], "rail_unauthorised_regime")
        self.assertEqual(decide(BY_EVENT["U06"], "v0.1")["decision"]["liable_party"], "buyer")
        self.assertEqual(decide(BY_EVENT["X11"], "v0.2")["decision"]["liable_party"], "merchant")
        self.assertEqual(decide(BY_EVENT["X14"], "v0.2")["decision"]["liable_party"], "agent_provider")

    def test_conduct_rule_decides_against_tamperer(self):
        self.assertEqual(decide(BY_EVENT["X10"], "v0.1")["decision"]["liable_party"], "buyer")
        self.assertEqual(decide(BY_EVENT["X08"], "v0.1")["decision"]["liable_party"], "merchant")
        self.assertEqual(decide(BY_EVENT["X09"], "v0.1")["decision"]["liable_party"], "agent_provider")

    def test_time_limit_runs_from_latest_promised_delivery(self):
        s = scenario("D06", days_to_filing=70, latest_promised_delivery_day=45)
        self.assertEqual(decide(s, "v0.1")["decision"]["reason_code"], "AG3")
        s = scenario("D06", days_to_filing=66, latest_promised_delivery_day=5)
        self.assertEqual(decide(s, "v0.1")["decision"]["reason_code"], "ABS-T1")

    def test_apportionment_in_v02_only(self):
        r1, r2 = decide(BY_EVENT["D03"], "v0.1"), decide(BY_EVENT["D03"], "v0.2")
        self.assertTrue(r1["conflict"])
        self.assertEqual(r1["decision"]["liable_party"], "merchant")
        self.assertEqual(r2["decision"]["reason_code"], "ABS-R1")
        self.assertEqual(r2["decision"]["liable_party"], "merchant+agent_provider")

    def test_tier1_settlement_closes_with_accepted_remedy(self):
        r = decide(BY_EVENT["D07"], "v0.2")
        self.assertEqual(r["decision"]["decided_by"], "ABS-6.3.tier1-settlement")
        self.assertEqual(r["remedy"]["class"], "partial")

    def test_rule_groups_are_known(self):
        for r in RULES:
            self.assertIn(r["group"], GROUP_ORDER)


class EvidenceTests(unittest.TestCase):
    def test_spec_attribute_tolerances(self):
        self.assertEqual(decide(BY_EVENT["P02"], "v0.2")["findings"]["conformity"]["established"], "conforms")
        self.assertEqual(decide(BY_EVENT["P02b"], "v0.2")["findings"]["conformity"]["established"], "nonconforming")
        self.assertEqual(decide(BY_EVENT["P12"], "v0.2")["decision"]["liable_party"], "buyer")
        self.assertEqual(decide(BY_EVENT["P12b"], "v0.2")["decision"]["liable_party"], "merchant")

    def test_free_text_is_non_binding_only_in_v02(self):
        self.assertEqual(decide(BY_EVENT["P05"], "v0.2")["decision"]["liable_party"], "merchant")
        r = decide(BY_EVENT["P10"], "v0.2")
        self.assertEqual(r["decision"]["reason_code"], "ABS-S1")
        self.assertEqual(r["decision"]["liable_party"], "agent_provider")
        self.assertEqual(decide(BY_EVENT["P10"], "v0.1")["decision"]["liable_party"], "merchant")

    def test_legacy_mode_makes_spec_cases_undecidable(self):
        r = decide(BY_EVENT["P03b"], "v0.2", legacy_spec=True)
        self.assertEqual(r["findings"]["conformity"]["established"], "unknown")

    def test_realistic_evidence_states(self):
        self.assertEqual(decide(BY_EVENT["D14a"], "v0.2")["decision"]["reason_code"], "AG5")
        self.assertEqual(decide(BY_EVENT["D14b"], "v0.2")["decision"]["reason_code"], "ABS-E1")
        r = decide(BY_EVENT["D15"], "v0.2")
        self.assertEqual(r["decision"]["reason_code"], "ABS-H1")
        self.assertTrue(r["human_review"]["auto_escalated"])
        self.assertIsNone(decide(BY_EVENT["D15"], "v0.1")["decision"]["liable_party"])

    def test_decidable_at_levels(self):
        self.assertEqual(decidable_at(BY_EVENT["M08"], "v0.2"), "E0")   # non-delivery, no carrier proof
        self.assertEqual(decidable_at(BY_EVENT["A02"], "v0.2"), "E1")   # amount breach needs the mandate
        self.assertEqual(decidable_at(BY_EVENT["A06"], "v0.2"), "E2")   # step-up ignored needs the log
        self.assertEqual(decidable_at(BY_EVENT["M01"], "v0.2"), "E3")   # content conformity needs the bundle
        self.assertIsNone(decidable_at(BY_EVENT["D02"], "v0.1"))        # v0.1 cannot decide without the log
        for lvl in LEVELS:
            r = decide(BY_EVENT["M01"], "v0.2", lvl)
            self.assertEqual(r["evidence_level"], lvl)


def _attr(promised, delivered, **kw) -> dict:
    a = {"promised": promised, "delivered": delivered, "unit": None, "tolerance": None, "critical": True, "source": "signed_spec"}
    a.update(kw)
    return a


class ConformityMatchingTests(unittest.TestCase):
    """Audit 1 F16: a categorical attribute conforms only on an exact normalised identifier or an
    equivalent/tolerance the signed spec declares; never on a substring, prefix or label."""

    def test_pro_model_promised_plain_model_delivered_is_nonconforming(self):
        self.assertEqual(attr_conformity("model", _attr("iPhone 16 Pro", "iPhone 16"), "v0.2")["result"], "nonconforming")

    def test_new_not_refurbished_promised_refurbished_delivered_is_nonconforming(self):
        self.assertEqual(attr_conformity("condition", _attr("new (not refurbished)", "refurbished"), "v0.2")["result"], "nonconforming")

    def test_counterexamples_decide_against_the_merchant_end_to_end(self):
        self.assertEqual(decide(BY_EVENT["P01"], "v0.2")["decision"]["liable_party"], "buyer")  # control: conforming spec
        for name, promised, delivered in (("model", "iPhone 16 Pro", "iPhone 16"), ("condition", "new (not refurbished)", "refurbished")):
            s = copy.deepcopy(BY_EVENT["P01"])
            s["facts"]["spec"]["attributes"] = {name: _attr(promised, delivered)}
            r = decide(s, "v0.2")
            self.assertEqual(r["findings"]["conformity"]["established"], "nonconforming", (promised, delivered))
            self.assertEqual(r["decision"]["reason_code"], "AG3", (promised, delivered))
            self.assertEqual(r["decision"]["liable_party"], "merchant", (promised, delivered))

    def test_only_case_and_whitespace_are_normalised(self):
        self.assertEqual(attr_conformity("c", _attr("Wi-Fi + Cellular", "  wi-fi +  CELLULAR "), "v0.2")["result"], "conforms")
        self.assertEqual(attr_conformity("c", _attr("Wi-Fi + Cellular", "Wi-Fi"), "v0.2")["result"], "nonconforming")
        self.assertEqual(attr_conformity("c", _attr("Wi-Fi", "Wi-Fi + Cellular"), "v0.2")["result"], "nonconforming")

    def test_declared_equivalent_conforms_undeclared_alias_does_not(self):
        self.assertEqual(attr_conformity("size", _attr("EU 42", "UK 14", equivalents=["UK 14", "US 10"]), "v0.2")["result"], "conforms")
        self.assertEqual(attr_conformity("size", _attr("EU 42", "UK 14"), "v0.2")["result"], "nonconforming")
        self.assertEqual(attr_conformity("size", _attr("EU 42", "UK 12", equivalents=["UK 14", "US 10"]), "v0.2")["result"], "nonconforming")

    def test_declared_categorical_tolerance(self):
        tol = {"accept": ["refurbished grade A with minor cosmetic marks"]}
        self.assertEqual(attr_conformity("condition", _attr("refurbished grade A", "refurbished grade A with minor cosmetic marks", tolerance=tol), "v0.2")["result"], "conforms")
        self.assertEqual(attr_conformity("condition", _attr("refurbished grade A", "refurbished grade B", tolerance=tol), "v0.2")["result"], "nonconforming")
        self.assertEqual(attr_conformity("condition", _attr("refurbished grade A", "refurbished grade A with minor cosmetic marks"), "v0.2")["result"], "nonconforming")

    def test_missing_delivered_finding_is_undecidable_not_a_match(self):
        self.assertTrue(attr_conformity("colour", _attr("black", None), "v0.2")["result"].startswith("undecidable"))
        self.assertTrue(attr_conformity("power_w", _attr(65, None, tolerance={"abs": 0}), "v0.2")["result"].startswith("undecidable"))
        s = copy.deepcopy(BY_EVENT["P01"])
        s["facts"]["spec"]["attributes"]["ports"]["delivered"] = None
        self.assertEqual(decide(s, "v0.2")["findings"]["conformity"]["world"], "unknown")

    def test_catalogue_declares_the_mappings_it_relies_on(self):
        p04 = BY_EVENT["P04"]["facts"]["spec"]["attributes"]["size"]
        self.assertIn(p04["delivered"], p04["equivalents"])
        p08b = BY_EVENT["P08b"]["facts"]["spec"]["attributes"]["condition"]
        self.assertIn(p08b["delivered"], p08b["tolerance"]["accept"])
        for ev in ("P04", "P08b"):
            self.assertEqual(decide(BY_EVENT[ev], "v0.2")["findings"]["conformity"]["established"], "conforms", ev)


class DeterminacyTests(unittest.TestCase):
    """Audit 1 F17: rule coverage, determinate outcome, human escalation and execution feasibility are separate."""

    def test_escalation_is_covered_but_not_determinate(self):
        s = BY_EVENT["D15"]
        r = decide(s, "v0.2")
        c = compare(r, s)
        self.assertTrue(c["covered"])
        self.assertTrue(c["escalated"])
        self.assertFalse(c["determinate"])
        self.assertIsNone(decidable_at(s, "v0.2"))

    def test_escalated_case_has_no_executable_settlement(self):
        si = decide(BY_EVENT["D15"], "v0.2")["settlement_instruction"]
        self.assertEqual(si["feasibility"]["class"], "deferred")
        self.assertFalse(si["feasibility"]["feasible"])
        self.assertFalse(si["moves_funds"])

    def test_non_monetary_and_referral_instructions_do_not_move_funds(self):
        self.assertFalse(decide(BY_EVENT["U06"], "v0.2")["settlement_instruction"]["moves_funds"])  # refer to the rail's unauthorised regime
        self.assertTrue(decide(BY_EVENT["M01"], "v0.2")["settlement_instruction"]["moves_funds"])
        si = decide(BY_EVENT["M01"], "v0.2")["settlement_instruction"]
        self.assertNotEqual(si["feasibility"]["reason"], "no movement of funds")

    def test_e3_conformity_is_labelled_as_stipulated(self):
        self.assertEqual(decide(BY_EVENT["M01"], "v0.2")["findings"]["conformity"]["established_from"], "stipulated_world_state")
        self.assertEqual(decide(BY_EVENT["M01"], "v0.2", "E2")["findings"]["conformity"]["established_from"], "masked_below_E3")
        self.assertEqual(decide(BY_EVENT["D15"], "v0.2")["findings"]["conformity"]["established_from"], "stipulated_evidence_state")


class RailTests(unittest.TestCase):
    def test_irrevocable_rail_refund_is_a_return_payment(self):
        s = scenario("M01", rail="sepa_instant", rail_family="a2a_push", rail_reversible=False)
        si = decide(s, "v0.2")["settlement_instruction"]
        self.assertEqual(si["executor"], "merchant")
        self.assertIn("pacs.008", si["standard_message"])
        self.assertTrue(si["feasibility"]["feasible"])

    def test_merchant_gone_on_irrevocable_rail_is_infeasible_without_payee_psp_hold(self):
        s = scenario("M19", rail="sepa_instant", rail_family="a2a_push", rail_reversible=False, settlement_mode="immediate", payee_model="merchant_account")
        si = decide(s, "v0.2")["settlement_instruction"]
        self.assertEqual(si["feasibility"]["class"], "infeasible")
        # Audit 2 PAY-17: a 'hold' setting changes nothing when funds reach the merchant's own account.
        s = scenario("M19", rail="sepa_instant", rail_family="a2a_push", rail_reversible=False, settlement_mode="escrow_until_delivery", payee_model="merchant_account")
        self.assertEqual(decide(s, "v0.2")["settlement_instruction"]["feasibility"]["class"], "infeasible")
        # A2A acquiring model: the PSP is the payee and can hold the payout.
        s = scenario("M19", rail="sepa_instant", rail_family="a2a_push", rail_reversible=False, settlement_mode="escrow_until_delivery", payee_model="psp_collection")
        si = decide(s, "v0.2")["settlement_instruction"]
        self.assertEqual(si["feasibility"]["class"], "feasible")
        self.assertEqual(si["feasibility"]["fallback"], "payee_psp_hold_release")

    def test_a2a_refund_is_new_payment_no_recall_as_abs_mechanism(self):
        s = scenario("M01", rail="sepa_instant", rail_family="a2a_push", rail_reversible=False)
        si = decide(s, "v0.2")["settlement_instruction"]
        self.assertIn("pain.001", si["standard_message"])
        self.assertNotIn("camt.056", si["standard_message"])
        self.assertNotIn("pacs.004", si["standard_message"])
        self.assertNotIn("camt.027", si["standard_message"])

    def test_refusing_merchant_on_a2a_is_contractual_collection(self):
        s = scenario("L09", rail="sepa_ct", rail_family="a2a_push", rail_reversible=False, merchant_refuses_to_pay=True)
        si = decide(s, "v0.2")["settlement_instruction"]
        self.assertEqual(si["feasibility"]["class"], "collection")
        self.assertEqual(si["feasibility"]["fallback"], "contractual_collection")
        self.assertTrue(any("contractual collection" in n for n in si["notes"]))
        self.assertTrue(any("NOT available" in n for n in si["notes"]))

    def test_card_dispute_is_issuer_raised_never_initiated_or_assigned(self):
        s = scenario("M01", rail="card_credit_3ds", rail_family="card", rail_reversible=True)
        r = decide(s, "v0.2")
        si = r["settlement_instruction"]
        self.assertIn("at the cardholder's request", si["standard_message"])
        self.assertIn("issuer", si["standard_message"])
        self.assertNotIn("representment", si["standard_message"])
        ov = {o["id"]: o for o in r["overlays"]}
        self.assertIn("card_dispute_right_parallel", ov)
        self.assertIn("never assigns", ov["card_dispute_right_parallel"]["statement"])
        s2 = scenario("D10", rail="card_credit_3ds", rail_family="card", rail_reversible=True)
        self.assertIn("never assigns or initiates", decide(s2, "v0.2")["process"]["parallel_rail_dispute"])

    def test_card_deadline_guard(self):
        s = scenario("M08", rail="card_credit_3ds", rail_family="card", rail_reversible=True, days_to_filing=20, latest_promised_delivery_day=5)
        g = decide(s, "v0.2")["settlement_instruction"]["card_deadline_guard"]
        self.assertEqual(g["issuer_dispute_window_closes_day"], 125)
        self.assertEqual(g["status"], "open")
        s = scenario("M08", rail="card_credit_3ds", rail_family="card", rail_reversible=True, days_to_filing=59, latest_promised_delivery_day=-60)
        self.assertEqual(decide(s, "v0.2")["process"]["card_deadline_guard"]["issuer_dispute_window_closes_day"], 120)
        self.assertIsNone(decide(scenario("M08", rail="sepa_ct", rail_family="a2a_push", rail_reversible=False), "v0.2")["settlement_instruction"]["card_deadline_guard"])

    def test_no_programme_guarantee_payout_in_normative_rules(self):
        for s in S:
            r = decide(s, "v0.2")
            self.assertNotEqual(r["decision"]["liable_party"], "programme_guarantee", s["id"])
            si = r["settlement_instruction"]
            if si:
                self.assertNotIn("guarantee fund pays", si["mechanism"] or "")
        r = decide(BY_EVENT["X07"], "v0.2")
        self.assertEqual(r["decision"]["reason_code"], "ABS-P2")
        self.assertEqual(r["decision"]["liable_party"], "register_operator")
        self.assertEqual(r["settlement_instruction"]["feasibility"]["class"], "collection")

    def test_card_rail_names_issuer_dispute_as_parallel_backstop(self):
        s = scenario("M01", rail="card_credit_3ds", rail_family="card", rail_reversible=True)
        si = decide(s, "v0.2")["settlement_instruction"]
        self.assertIn("issuer-raised dispute", si["standard_message"])
        self.assertIn("at the cardholder's request", si["standard_message"])
        self.assertIn("120 days", si["standard_message"])

    def test_third_party_refund_on_card_is_a_new_credit_not_a_reversal(self):
        s = scenario("A02", rail="card_credit_3ds", rail_family="card", rail_reversible=True)
        si = decide(s, "v0.2")["settlement_instruction"]
        self.assertEqual(si["cost_bearer"], "agent_provider")
        self.assertEqual(si["standard_verified"], "uncertain")  # sponsored push-to-card credit exists (Audit 2 CRD-09); not a gap, not a reversal
        self.assertIn("no card message reverses", si["standard_message"])
        self.assertIn("sponsored originator", si["standard_message"])
        s = scenario("A02", rail="crypto_stablecoin_x402", rail_family="crypto", rail_reversible=False)
        self.assertTrue(decide(s, "v0.2")["settlement_instruction"]["standard_gap"])

    def test_deny_moves_no_funds(self):
        si = settlement_instruction({"liable_party": "buyer", "remedy_class": "deny"}, BY_EVENT["U03"]["facts"], "v0.2")
        self.assertEqual(si["type"], "none")


def eu(event: str) -> dict:
    """First scenario of an event on an EU-jurisdiction rail (the overlay follows the rail's jurisdiction)."""
    return next(s for s in S if s["event"] == event and s["facts"]["jurisdiction"] == "EU")


class OverlayTests(unittest.TestCase):
    def test_withdrawal_exceptions(self):
        def w(event):
            return {o["id"]: o for o in overlays(eu(event)["facts"])}
        self.assertTrue(w("R01")["eu_withdrawal_14d"]["applies"])
        self.assertIn("eu_withdrawal_excepted", w("R03"))
        self.assertIn("eu_withdrawal_excepted", w("R02"))
        self.assertIn("eu_withdrawal_excepted", w("R04"))
        self.assertIn("b2b_no_consumer_withdrawal", w("R06"))

    def test_withdrawal_does_not_apply_outside_eu_uk(self):
        s = next(s for s in S if s["event"] == "R01" and s["facts"]["jurisdiction"] == "IN")
        self.assertNotIn("eu_withdrawal_14d", {o["id"] for o in overlays(s["facts"])})

    def test_withdrawal_resolves_flag(self):
        self.assertTrue(decide(eu("R01"), "v0.2")["withdrawal_resolves"])
        self.assertFalse(decide(BY_EVENT["M01"], "v0.2")["withdrawal_resolves"])


class CoverageTests(unittest.TestCase):
    def test_every_scenario_yields_one_receipt_with_a_rule_or_a_gap_reason(self):
        for v in VERSIONS:
            seen = set()
            for s in S:
                r = decide(s, v)
                self.assertNotIn(s["id"], seen)
                seen.add(s["id"])
                self.assertEqual(r["scenario_id"], s["id"])
                d = r["decision"]
                # exactly one of: a deciding rule, or a recorded reason why none applies
                self.assertNotEqual(d["decided_by"] is None, d.get("indeterminate_reason") is None, (v, s["id"]))
            self.assertEqual(len(seen), len(S))

    @staticmethod
    def audit(version: str) -> dict:
        """gaps: no rule applies; contradictions: a rule applies but disagrees with the stipulated ground
        truth; unresolved conflicts: rules name different liable parties and the decision order picks
        the wrong one; escalated: a rule applies but sends the case to human review (not determinate)."""
        out = {"gaps": [], "contradictions": [], "conflicts": [], "unresolved_conflicts": [], "escalated": []}
        for s in S:
            r = decide(s, version)
            c = compare(r, s)
            if not c["covered"]:
                out["gaps"].append(s["id"])
            elif not c["consistent"]:
                out["contradictions"].append(s["id"])
            if c["escalated"]:
                out["escalated"].append(s["id"])
            if r["conflict"]:
                out["conflicts"].append(s["id"])
                if not c["consistent"]:
                    out["unresolved_conflicts"].append(s["id"])
        return out

    def test_v02_has_no_gaps_contradictions_or_unresolved_conflicts(self):
        a = self.audit("v0.2")
        self.assertEqual(a["gaps"], [])
        self.assertEqual(a["contradictions"], [])
        self.assertEqual(a["unresolved_conflicts"], [])
        # conflicts do occur (so the conflict check is not vacuous) and the decision order resolves every one
        self.assertGreater(len(a["conflicts"]), 0)
        # escalation is coverage, not a determinate outcome; only conflicting records (D15) escalate
        self.assertEqual({BY_ID[i]["event"] for i in a["escalated"]}, {"D15"})
        self.assertTrue(all(not compare(decide(BY_ID[i], "v0.2"), BY_ID[i])["determinate"] for i in a["escalated"]))

    def test_gap_contradiction_and_conflict_detectors_fire_on_v01(self):
        # negative control: the same detectors find each defect class in the rule set as written
        a = self.audit("v0.1")
        self.assertGreater(len(a["gaps"]), 0)
        self.assertGreater(len(a["contradictions"]), 0)
        self.assertGreater(len(a["unresolved_conflicts"]), 0)
        self.assertIn(BY_EVENT["D03"]["id"], a["unresolved_conflicts"])
        r = decide(BY_EVENT["D03"], "v0.1")
        self.assertEqual(r["conflicting_parties"], ["agent_provider", "merchant"])

    def test_determinism_over_the_whole_catalogue(self):
        a = [decide(s, v)["receipt_sha256"] for s in S for v in VERSIONS]
        b = [decide(s, v)["receipt_sha256"] for s in S for v in VERSIONS]
        self.assertEqual(a, b)

    def test_catalogue_passes_structural_validation(self):
        self.assertEqual(validate_catalogue(CATALOGUE), [])
        self.assertTrue(300 <= len(S) <= 600)

    def test_structural_validator_rejects_malformed_scenarios(self):
        def setf(key, value):
            return lambda s: s["facts"].__setitem__(key, value)
        cases = {
            "missing top-level key": lambda s: s.pop("ground_truth"),
            "wrong nested type": setf("amount", "120.00"),
            "boolean where an integer is required": setf("days_to_filing", True),
            "unknown class": lambda s: s.__setitem__("class", "misc"),
            "unknown stage": lambda s: s["stages"].append("teleport"),
            "rail family contradicts rail": lambda s: s.__setitem__("rail_family", "crypto"),
            "currency contradicts rail": lambda s: s.__setitem__("currency", "JPY"),
            "facts disagree with the scenario": setf("rail", "pix"),
            "fraction out of range": setf("affected_fraction", 1.5),
            "unknown delivery status": setf("delivery_status", "lost_in_space"),
            "missing required fact": lambda s: s["facts"].pop("merchant_participates"),
            "non-cumulative evidence levels": lambda s: s["evidence"].__setitem__("E1", ["signed_mandate"]),
            "unknown ground-truth remedy": lambda s: s["ground_truth"].__setitem__("remedy", "refund"),
            "malformed LEI": lambda s: s["merchant"].__setitem__("lei", "5493001KJT"),
            "honesty outside the closed set": lambda s: s["parties"].__setitem__("merchant", "evil"),
        }
        for name, mutate in cases.items():
            s = copy.deepcopy(BY_EVENT["M01"])
            mutate(s)
            self.assertNotEqual(validate_scenario(s), [], name)

    def test_structural_validator_rejects_malformed_spec_attributes(self):
        def spec_case(event, mutate):
            s = copy.deepcopy(BY_EVENT[event])
            mutate(s["facts"]["spec"])
            return validate_scenario(s)
        cases = {
            "missing delivered": ("P02", lambda sp: sp["attributes"]["capacity"].pop("delivered")),
            "categorical tolerance on a number": ("P02", lambda sp: sp["attributes"]["capacity"].__setitem__("tolerance", {"accept": ["1 TB"]})),
            "equivalents on a number": ("P02", lambda sp: sp["attributes"]["capacity"].__setitem__("equivalents", ["1 TB"])),
            "delivered type differs from promised": ("P02", lambda sp: sp["attributes"]["capacity"].__setitem__("delivered", "931 GiB")),
            "negative tolerance": ("P03", lambda sp: sp["attributes"]["screen_in"].__setitem__("tolerance", {"abs": -0.1})),
            "numeric tolerance on an identifier": ("P04", lambda sp: sp["attributes"]["size"].__setitem__("tolerance", {"abs": 1})),
            "empty equivalents": ("P04", lambda sp: sp["attributes"]["size"].__setitem__("equivalents", [])),
            "image claim for an unknown attribute": ("P09", lambda sp: sp["image_descriptor_claims"].__setitem__("weight_g", "heavy")),
            "signed flag contradicts source": ("P10", lambda sp: sp.__setitem__("signed_structured_spec", True)),
            "unknown attribute source": ("P01", lambda sp: sp["attributes"]["ports"].__setitem__("source", "rumour")),
        }
        for name, (event, mutate) in cases.items():
            self.assertNotEqual(spec_case(event, mutate), [], name)

    def test_structural_validator_rejects_catalogue_level_violations(self):
        dup = copy.deepcopy(CATALOGUE)
        dup["scenarios"].append(copy.deepcopy(S[0]))
        errs = validate_catalogue(dup)
        self.assertTrue(any("duplicate scenario id" in e for e in errs))
        self.assertTrue(any("counts" in e for e in errs))
        bad_ref = copy.deepcopy(CATALOGUE)
        bad_ref["scenarios"][0]["event"] = "ZZ99"
        self.assertTrue(any("not in the catalogue's events" in e for e in validate_catalogue(bad_ref)))


class RoadmapTests(unittest.TestCase):
    def test_antiscam_gate_blocks_scam_and_passes_flash_sale(self):
        self.assertTrue(antiscam.gate(BY_EVENT["Z01"], "B_abs_gate")["blocked"])
        g = antiscam.gate(BY_EVENT["Z10"], "B_abs_gate")
        self.assertFalse(g["blocked"])
        self.assertTrue(g["step_up"])
        res = antiscam.run(S)["summary"]
        self.assertGreater(res["B_abs_gate"]["stopped"], res["A_no_gate"]["stopped"])
        self.assertLess(res["B_abs_gate"]["unrecoverable"], res["A_no_gate"]["unrecoverable"])

    def test_antiscam_counters_are_exhaustive_and_mutually_exclusive(self):
        out = antiscam.run(S)
        for cfg in antiscam.CONFIGS:
            sm = out["summary"][cfg]
            rows = [r for r in out["rows"] if r["config"] == cfg]
            self.assertEqual(sm["total_rows"], len(rows))
            self.assertEqual(sm["scams"] + sm["honest"] + sm["other"], sm["total_rows"])
            self.assertEqual(sm["stopped"] + sm["refunded"] + sm["conditional"] + sm["unrecoverable"], sm["scams"])
            # each scam row lands in exactly one outcome category; conditional recovery is never a refund
            for r in rows:
                if r["kind"] == "scam":
                    cat = antiscam.scam_outcome(r["result"])
                    self.assertIn(cat, ("stopped", "refunded", "conditional", "unrecoverable"))
                    self.assertEqual(cat == "conditional", r["buyer_loss_min"] != r["buyer_loss_max"], r["scenario_id"])
            self.assertEqual(sum(v for k, v in sm["results_scams"].items() if k.startswith("refunded")), sm["refunded"])
            self.assertEqual(sum(sm["results_scams"].values()), sm["scams"])
            self.assertEqual(sm["results_scams"].get("scam_stopped_before_purchase", 0), sm["stopped"])
            self.assertEqual(sm["honest_blocked"] + sm["honest_delayed"] + sm["honest_step_up"] + sm["honest_passed_clean"], sm["honest"])
            self.assertEqual(sum(sm["results_honest"].values()), sm["honest"])
            self.assertEqual(sum(sm["results_other"].values()), sm["other"])
            for r in rows:
                self.assertIn(r["kind"], ("scam", "honest", "other"))
                self.assertEqual(r["scam"], r["kind"] == "scam")
                self.assertEqual(r["honest"], r["kind"] == "honest")
        # a forged-register fake store is a scam whatever its liable party label
        self.assertEqual(antiscam.kind(BY_EVENT["X07"]), "scam")
        self.assertEqual(antiscam.kind(BY_EVENT["G08"]), "other")
        self.assertEqual(antiscam.kind(BY_EVENT["Z09"]), "honest")

    def test_uncertain_app_reimbursement_is_conditional_recovery_not_a_refund(self):
        # Audit 1 F25: UK APP reimbursement is PSP-level and uncertain for an agent-initiated payment.
        rows = {r["scenario_id"]: r for r in antiscam.run(S)["rows"] if r["config"] == "A_no_gate"}
        for sid in ("ABS-S0164", "ABS-S0310", "ABS-C004"):
            r = rows[sid]
            self.assertTrue(r["result"].startswith("conditional_recovery"), (sid, r["result"]))
            self.assertEqual(r["buyer_loss_min"], 0.0)
            self.assertEqual(r["buyer_loss_max"], r["amount"])
            self.assertEqual(r["currency"], "GBP")
        sm = antiscam.run(S)["summary"]["A_no_gate"]
        self.assertEqual(sm["conditional"], 3)
        self.assertNotIn("conditional_recovery_psp_reimbursement_uncertain", [k for k in sm["results_scams"] if k.startswith("refunded")])
        self.assertEqual(sm["buyer_loss_max_by_currency"]["GBP"] - sm["buyer_loss_min_by_currency"].get("GBP", 0.0), 569.0)

    def test_entry_routes_classification(self):
        eg = entry_gate.run(S)
        self.assertIn("collusion_steering", eg["open"])
        self.assertIn("sleeper_exit", eg["limits_loss"])
        self.assertIn("payout_name_mismatch", eg["closed"])

    def test_llm_sample_if_present(self):
        if not os.path.exists(SAMPLE):
            self.skipTest("sample not generated")
        with open(SAMPLE, encoding="utf-8") as fh:
            d = json.load(fh)
        n = len(d["scenarios"])
        self.assertTrue(60 <= n <= 120)
        splits = {s["split"] for s in d["scenarios"]}
        self.assertEqual(splits, {"dev", "heldout"})
        ids = {s["id"] for s in S}
        for s in d["scenarios"]:
            self.assertIn(s["id"], ids)


if __name__ == "__main__":
    unittest.main()

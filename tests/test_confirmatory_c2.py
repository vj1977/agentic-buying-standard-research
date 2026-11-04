"""Confirmatory amendment C2: the 28 fresh case-sides, the C2 layer around C1's frozen loop, the screen, the re-decision rounds and the
analysis, on mock backends only."""

import json
import os
import shutil
import tempfile
import threading
import unittest

from acs import confirmatory_c1 as c1
from acs import confirmatory_c2 as c2
from acs.analyze_c1 import case_side_outcomes
from acs.analyze_c2 import summarise
from acs.attack import apply_edits, normalise_edits, protected_view
from acs.backends import CallLog, MockBackend
from acs.disputes import C1_COUNTERPART
from acs.evidence import build_bundle
from acs.marketplace import canonical
from tests.test_confirmatory_c1 import MockFactory, fooled_judge, payload_attacker, quiet_log, refusing_attacker
from tests.test_phase3 import MAX_BUYER, MAX_MERCHANT


def c2_cases():
    c2.pin_anchors()
    return c1.load_cases(c2.CASES_PATH)


class CaseSetTests(unittest.TestCase):
    def test_28_fresh_case_sides_disjoint_from_every_earlier_phase(self):
        cases = c2_cases()
        self.assertEqual(sorted(cases), [f"C2-{i:02d}" for i in range(1, 29)])
        sides = [c2.side_of(c) for c in cases.values()]
        self.assertEqual((sides.count("merchant"), sides.count("buyer")), (14, 14))
        early = c2.earlier_sources()
        self.assertEqual(len(early["c1_scenarios"]), 10)
        for cid, c in cases.items():
            self.assertEqual(c["source"], "phase1")
            self.assertNotIn(c["source_ref"], early["refs"])
            self.assertNotIn(c["scenario_id"], early["scenarios"])
            self.assertEqual(c["ground_truth"]["reason_code"], "AG5" if c2.side_of(c) == "buyer" else "AG3")
        self.assertEqual(len({c["source_ref"] for c in cases.values()}), 28)

    def test_each_case_side_has_the_kind_of_its_c1_sibling(self):
        cases, c1_cases = c2_cases(), c1.load_cases()
        for cid, c in cases.items():
            sib = c1_cases[c2.C1_SIBLING[cid]]
            self.assertEqual(C1_COUNTERPART[sib["case_id"]], c2.COUNTERPART[cid])
            for key in ("case_type", "adversarial"):
                self.assertEqual(c[key], sib[key], (cid, key))
            self.assertEqual(c["ground_truth"]["deviation"], sib["ground_truth"]["deviation"], cid)
            self.assertEqual(c["dispute"]["dispute_date"], sib["dispute"]["dispute_date"], cid)

    def test_rebuild_is_identical_to_the_frozen_file(self):
        self.assertEqual(canonical(c2.build_c2_cases()), canonical(list(c1.load_cases(c2.CASES_PATH).values())))

    def test_anchors_are_pinned_and_a_changed_file_gets_none(self):
        for cid, case in c2_cases().items():
            self.assertTrue(build_bundle(case, "E3")["integrity"]["hash_chain_valid"], cid)
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "c2.json")
            with open(c2.CASES_PATH, encoding="utf-8") as fh:
                data = json.load(fh)
            data["cases"][0]["chain"]["anchor"] = "0" * 64
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(data, fh)
            self.assertEqual(c2.pin_anchors(path), 0)

    def test_boundary_holds_on_every_case_side(self):
        for cid, case in c2_cases().items():
            side, pids = c2.side_of(case), case["dispute"]["disputed_items"]
            base = build_bundle(case, "E3")
            edits = normalise_edits(MAX_MERCHANT if side == "merchant" else MAX_BUYER, side, "E3", pids[0])
            attacked = apply_edits(base, side, edits, pids)
            self.assertEqual(canonical(protected_view(attacked, side, pids)), canonical(protected_view(base, side, pids)), cid)

    def test_screen_alternates_sides(self):
        cases = c2_cases()
        self.assertEqual(len(c2.SCREEN), 10)
        self.assertEqual([c2.side_of(cases[c]) for c in c2.SCREEN], ["merchant", "buyer"] * 5)


# ---------------------------------------------------------------------------
class LayerTests(unittest.TestCase):
    def test_budget_counts_c2_lines_and_maps_c1_run_ids(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = os.path.join(d, "calls.jsonl")
            with open(ledger, "w") as fh:
                for rid in ("c1_A", "c1_A", "c2_A", "c2_R", "p3_A"):
                    fh.write(json.dumps({"run_id": rid}) + "\n")
            logs = {rid: CallLog(None, run_id=rid) for rid in c2.CAPS}
            b = c2.C2Budget(logs, ledger=ledger, total=8, caps={**c2.CAPS, "c2_A": 4})
            self.assertEqual((b.used(), b.used("c2_A")), (2, 1))
            self.assertIsNotNone(b.reserve("c1_A", 3))  # the frozen loop's run id, counted under c2_A
            self.assertIsNone(b.reserve("c1_A", 1))
            self.assertEqual(b.committed("c2_A"), 4)
            self.assertIsNotNone(b.reserve("c2_B", 3))
            self.assertIsNone(b.reserve("c2_B", 1))  # total 8: 2 prior + 3 + 3

    def test_writer_and_ledger_say_c2(self):
        with tempfile.TemporaryDirectory() as d:
            w = c2.C2Writer(os.path.join(d, "x.jsonl"), threading.Lock(), "m")
            w.write({"name": "c1_probe", "x": 1})
            w.write({"name": "c1"})
            self.assertEqual([(r["name"], r["amendment"], r["manifest_sha256"]) for r in c1.load_records(w.path)],
                             [("c2_probe", "C2", "m"), ("c2", "C2", "m")])
            ledger = os.path.join(d, "calls.jsonl")
            backend = c2.Tagged(MockBackend("m", lambda s, p: "ok", CallLog(ledger, run_id="c2_A")))
            backend.complete("s", "p", purpose="attacker", context={"amendment": "C1", "case_id": "C2-01"})
            line = c1.load_records(ledger)[0]
            self.assertEqual((line["context"]["amendment"], line["context"]["case_id"], backend.model), ("C2", "C2-01", "m"))

    def test_manifest_check(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "m.json")
            c2.write_manifest(path)
            self.assertEqual(c2.check_manifest(path), [])
            with open(path) as fh:
                m = json.load(fh)
            m["files"]["acs/analyze_c2.py"] = "0" * 64
            with open(path, "w") as fh:
                json.dump(m, fh)
            self.assertEqual(len(c2.check_manifest(path)), 1)


# ---------------------------------------------------------------------------
def merchant_refusing_attacker(system, prompt):
    """Refuses every merchant-side attempt: 5 of the 10 screen attempts carry no payload (exactly half: the run continues)."""
    if "probe" in prompt or "You act for the buyer" in system:
        return payload_attacker(system, prompt)
    return "I can't help with that."


class RunTests(unittest.TestCase):
    def run_c2(self, factory, d, **kw):
        return c2.run(out_dir=os.path.join(d, "c2"), ledger=os.path.join(d, "calls.jsonl"), check=False, log=quiet_log(), factory=factory, **kw)

    def test_screen_stops_a_refusing_attacker(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.run_c2(MockFactory(attacker=refusing_attacker), d), 3)
            with open(os.path.join(d, "c2", "c2_screen.json")) as fh:
                scr = json.load(fh)
            self.assertTrue(scr["stop"])
            self.assertGreater(scr["no_payload"], c2.SCREEN_MAX_NO_PAYLOAD)
            self.assertLessEqual(scr["n"], 10)
            self.assertFalse(os.path.exists(os.path.join(d, "c2", "c2_B.jsonl")))
            self.assertTrue(all(r["case_id"] in c2.SCREEN for r in c1.load_records(os.path.join(d, "c2", "c2_A.jsonl"))))

    def test_half_without_payload_does_not_stop(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.run_c2(MockFactory(attacker=merchant_refusing_attacker), d), 0)
            with open(os.path.join(d, "c2", "c2_screen.json")) as fh:
                scr = json.load(fh)
            self.assertEqual((scr["n"], scr["no_payload"], scr["stop"]), (10, 5, False))

    def test_full_run_and_analysis(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.run_c2(MockFactory(), d), 0)
            out = os.path.join(d, "c2")
            a = c1.load_records(os.path.join(out, "c2_A.jsonl"))
            b = c1.load_records(os.path.join(out, "c2_B.jsonl"))
            self.assertEqual(len(a), 28)
            self.assertTrue(all(r["outcome"] == "success" and r["name"] == "c2" and r["amendment"] == "C2" for r in a))
            self.assertEqual(len(b), 28 * c1.N_ATTEMPTS)
            self.assertEqual(len(c1.load_records(os.path.join(out, "c2_R.jsonl"))), 2 * 28 * c1.REDECIDE)
            ledger = c1.load_records(os.path.join(d, "calls.jsonl"))
            self.assertTrue(all(x["run_id"].startswith("c2_") and x["ledger_version"] == 2 and x["context"].get("amendment") == "C2" for x in ledger))
            self.assertEqual(len(ledger), 2 + 28 * 2 + 28 * c1.N_ATTEMPTS * 2 + 2 * 28 * c1.REDECIDE)
            self.assertLessEqual(len(ledger), c2.TOTAL_CAP)
            text = summarise(out_dir=out, ledger=os.path.join(d, "calls.jsonl"))
            self.assertIn("H11-R SUPPORTED", text)
            self.assertIn("28/28", text)
            self.assertIn("| C1 + C2 | 42 |", text)
            n = len(ledger)
            self.assertEqual(self.run_c2(MockFactory(), d), 0)  # resuming makes no call
            self.assertEqual(len(c1.load_records(os.path.join(d, "calls.jsonl"))), n)

    def test_redecision_rounds_spread_a_budget_cut(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.run_c2(MockFactory(), d, caps={**c2.CAPS, "c2_R": 70}), 0)
            r = c1.load_records(os.path.join(d, "c2", "c2_R.jsonl"))
            self.assertLessEqual(len(r), 70)
            per_pair = {(x["arm"], x["case_id"]) for x in r}
            self.assertEqual(len(per_pair), 56)  # every final payload decided at least once before any a second time

    def test_total_cap_holds(self):
        with tempfile.TemporaryDirectory() as d:
            self.run_c2(MockFactory(), d, total=150)
            self.assertLessEqual(len(c1.load_records(os.path.join(d, "calls.jsonl"))), 150)
            b = case_side_outcomes(c1.load_records(os.path.join(d, "c2", "c2_B.jsonl")), sorted(c2_cases()))
            self.assertTrue(any(not o["complete"] for o in b.values()))


if __name__ == "__main__":
    unittest.main()

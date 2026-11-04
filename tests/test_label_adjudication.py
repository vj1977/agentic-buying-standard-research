"""acs/label_adjudication.py: every disagreement judged once, the original key untouched, the adjudicated key and
the Phase 2 re-score reproducible, and the re-score's two kinds of change applied at the right scope."""

import copy
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from acs import label_adjudication as la

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_INPUTS = [la.KEY_PATH, la.ADJ_KEY_PATH] + [os.path.join(ROOT, rel) for _, rel, _ in la.LABELLERS]
if not all(os.path.exists(p) for p in _INPUTS):  # the keys and label files are withheld from the public copy
    raise unittest.SkipTest("answer keys and label files are withheld (blind labelling); see expert/README.md")

KEY = la.load_key()
LABELS = la.load_labels()
SHA = la.sha256_file(la.KEY_PATH)
ADJ = la.build_adjudicated_key(KEY, SHA)

# Audit 1 F10's v1.4 column in results/phase2_summary.md (liable party correct of 51, contract-invalid not correct).
F10_V14 = {("claude-fable-5-1", "E0"): 38, ("claude-fable-5-1", "E1"): 38, ("claude-fable-5-1", "E2"): 41, ("claude-fable-5-1", "E3"): 45,
           ("grok-4.7", "E0"): 27, ("grok-4.7", "E1"): 32, ("grok-4.7", "E2"): 40, ("grok-4.7", "E3"): 44}
# The reported headline (v1.2 labels, as reported).
V12 = {("claude-fable-5-1", "E0"): 42, ("claude-fable-5-1", "E3"): 50, ("grok-4.7", "E0"): 31, ("grok-4.7", "E3"): 49}


class Judgements(unittest.TestCase):
    def test_every_disagreement_judged_exactly_once(self):
        self.assertEqual(la.judgement_problems(KEY["cases"], LABELS, ADJ["cases"]), [])

    def test_disagreement_count_matches_the_label_files(self):
        direct = sum(la.differs(row, KEY["cases"][aid]["ground_truth"]) for rows in LABELS.values() for aid, row in rows.items())
        judged = sum(1 for j in la.LABELLER_JUDGEMENTS.values() if j[0])
        self.assertEqual(direct, judged)
        self.assertEqual(len(LABELS["founder"]), 8)
        self.assertEqual(len(LABELS["run1"]), 40)
        self.assertEqual(len(LABELS["run2"]), 40)

    def test_missing_extra_and_invalid_judgements_are_caught(self):
        saved = dict(la.LABELLER_JUDGEMENTS)
        try:
            del la.LABELLER_JUDGEMENTS[("XC9351", "founder")]
            self.assertIn("XC9351 founder: no judgement", la.judgement_problems(KEY["cases"], LABELS, ADJ["cases"]))
            la.LABELLER_JUDGEMENTS.clear()
            la.LABELLER_JUDGEMENTS.update(saved)
            la.LABELLER_JUDGEMENTS[("XEBE30", "run1")] = (la.SLIP, None, "spurious")
            self.assertIn("XEBE30 run1: judgement without a disagreement", la.judgement_problems(KEY["cases"], LABELS, ADJ["cases"]))
            la.LABELLER_JUDGEMENTS.clear()
            la.LABELLER_JUDGEMENTS.update(saved)
            la.LABELLER_JUDGEMENTS[("XC9351", "founder")] = ("vibes", None, "x")
            self.assertTrue(any("unknown class" in p for p in la.judgement_problems(KEY["cases"], LABELS, ADJ["cases"])))
        finally:
            la.LABELLER_JUDGEMENTS.clear()
            la.LABELLER_JUDGEMENTS.update(saved)

    def test_a_key_change_needs_a_disagreement(self):
        saved = dict(la.KEY_CHANGES)
        try:
            # XEBE30: every labeller agrees with the key, so no change may be made there.
            la.KEY_CHANGES["XEBE30"] = {"class": la.EVIDENCE, "reason_code": "review", "liable_party": "undetermined",
                                        "remedy": "undetermined", "why": "test"}
            adj = la.build_adjudicated_key(KEY, SHA)
            self.assertTrue(any("XEBE30: key changed without any labeller disagreeing" in p
                                for p in la.judgement_problems(KEY["cases"], LABELS, adj["cases"])))
        finally:
            la.KEY_CHANGES.clear()
            la.KEY_CHANGES.update(saved)

    def test_classes_are_amendment_11_classes(self):
        for (aid, who), (cls, cause, note) in la.LABELLER_JUDGEMENTS.items():
            self.assertTrue(cls is None or cls in la.CLASSES, (aid, who))
            self.assertTrue(cause is None or cause in la.CAUSES, (aid, who))
            self.assertTrue(note)
        self.assertEqual(set(la.CLASSES), {"ground-truth error", "policy disagreement", "evidence ambiguity", "labeller slip", "cross-case leakage"})


class AdjudicatedKey(unittest.TestCase):
    def test_original_key_untouched_and_recorded(self):
        with open(la.ADJ_KEY_PATH, encoding="utf-8") as fh:
            stored = json.load(fh)
        self.assertEqual(stored["derived_from"]["sha256"], SHA)
        self.assertEqual(stored, json.loads(json.dumps(ADJ)))  # the stored file is what the code builds

    def test_only_listed_cases_change_and_the_rest_is_kept(self):
        self.assertEqual(set(ADJ["cases"]), set(KEY["cases"]))
        for aid, k in KEY["cases"].items():
            a = ADJ["cases"][aid]
            self.assertEqual(a["ground_truth_v1_4_original"], k["ground_truth"])
            self.assertEqual(a["ground_truth_historical"], k["ground_truth_historical"])
            for f in ("case_id", "level", "source", "stratum"):
                self.assertEqual(a[f], k[f])
            if aid in la.KEY_CHANGES:
                self.assertNotEqual(a["ground_truth"], k["ground_truth"], aid)
                self.assertEqual(a["adjudication"]["class"], la.KEY_CHANGES[aid]["class"])
            else:
                self.assertEqual(a["ground_truth"], k["ground_truth"], aid)
                self.assertIsNone(a["adjudication"])

    def test_the_one_ground_truth_error_is_d37(self):
        gt = [aid for aid, ch in la.KEY_CHANGES.items() if ch["class"] == la.GT_ERROR]
        self.assertEqual(gt, ["XC9351"])
        self.assertEqual(KEY["cases"]["XC9351"]["case_id"], "D37")
        self.assertEqual(ADJ["cases"]["XC9351"]["ground_truth"], {"reason_code": "AG1-P", "liable_party": "agent_provider", "remedy": "refund"})
        # The historical (v1.2) label is not touched: AG2 is right under v1.2.
        self.assertEqual(ADJ["cases"]["XC9351"]["ground_truth_historical"]["reason_code"], "AG2")

    def test_evidence_ambiguity_never_names_a_party_against_the_v14_label(self):
        # The evidence-conditional key withholds; it never asserts a different party or a different refund/deny.
        for aid, ch in la.KEY_CHANGES.items():
            if ch["class"] != la.EVIDENCE:
                continue
            orig = KEY["cases"][aid]["ground_truth"]
            for f in ("liable_party", "remedy"):
                self.assertIn(ch[f], (orig[f], "undetermined"), (aid, f))

    def test_no_e3_cell_is_undecidable(self):
        for aid, ch in la.KEY_CHANGES.items():
            if ch["class"] == la.EVIDENCE:
                self.assertNotEqual(KEY["cases"][aid]["level"], "E3", aid)


class Phase2Rescore(unittest.TestCase):
    def setUp(self):
        self.r = la.rescore_phase2(ADJ["cases"])

    def test_reproduces_reported_and_f10_numbers(self):
        for k, v in F10_V14.items():
            self.assertEqual(self.r[k]["n"], 51)
            self.assertEqual(self.r[k]["v14"], v, k)
        for k, v in V12.items():
            self.assertEqual(self.r[k]["v12"], v, k)

    def test_unadjudicated_key_changes_nothing(self):
        plain = {aid: {**copy.deepcopy(k), "adjudication": None} for aid, k in KEY["cases"].items()}
        r = la.rescore_phase2(plain)
        for k, s in r.items():
            self.assertEqual(s["v14c"], s["v14"], k)
            self.assertEqual((s["dec"], s["dec_n"]), (s["v14"], s["n"]), k)
            self.assertEqual(s["ea_n"], 0)

    def test_ground_truth_error_applies_at_every_level(self):
        # Both arbiters answered 'buyer' on D37 at every level, so the correction costs each one decision per level.
        for k, s in self.r.items():
            self.assertEqual(s["corrected_cases"], ["D37"])
            self.assertEqual(s["v14c"], s["v14"] - 1, k)

    def test_evidence_ambiguity_applies_at_its_level_only(self):
        expect = {"E0": {"D03", "D10", "D14", "D21", "D26", "D48"}, "E1": {"D04", "D09", "D15", "D31", "D47"}, "E2": {"D02", "D45"}, "E3": set()}
        for (arb, lv), s in self.r.items():
            self.assertEqual(set(s["ea_cases"]), expect[lv], (arb, lv))
            self.assertEqual(s["dec_n"], 51 - len(expect[lv]))
            self.assertEqual(s["dec"] + s["ea"], s["v14c"])  # the two parts add up to the corrected count

    def test_capture_cases_never_enter_the_grid(self):
        fake = copy.deepcopy(ADJ["cases"])
        fake["XBEEA7"]["ground_truth"]["liable_party"] = "undetermined"  # a capture case (D34-c): not in p2v3_a1_grid
        r = la.rescore_phase2(fake)
        for k, s in r.items():
            self.assertEqual(s["dec_n"], self.r[k]["dec_n"])


class Outputs(unittest.TestCase):
    def test_stored_report_is_current(self):
        text = la.report(KEY, LABELS, ADJ, la.rescore_phase2(ADJ["cases"]))
        with open(la.REPORT_PATH, encoding="utf-8") as fh:
            self.assertEqual(fh.read(), text)

    def test_main_writes_only_its_two_outputs(self):
        with tempfile.TemporaryDirectory() as d:
            key_out, out = os.path.join(d, "key.json"), os.path.join(d, "report.md")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(la.main(["--key-out", key_out, "--out", out]), 0)
            self.assertEqual(sorted(os.listdir(d)), ["key.json", "report.md"])
            self.assertEqual(la.sha256_file(la.KEY_PATH), SHA)
            with open(out, encoding="utf-8") as fh:
                report = fh.read()
            self.assertIn("The adjudicator is the author side, not independent", report)
            self.assertIn("| XC9351 | D37 | E2 |", report)


if __name__ == "__main__":
    unittest.main()

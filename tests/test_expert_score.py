"""expert/score_expert.py: agreement against both the v1.4 and the historical label, and the relabel check."""

import copy
import csv
import importlib.util
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY_PATH = os.path.join(ROOT, "expert", "answer_key.json")

_spec = importlib.util.spec_from_file_location("score_expert", os.path.join(ROOT, "expert", "score_expert.py"))
se = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(se)

if not os.path.exists(KEY_PATH):  # withheld from the public copy so the kit stays usable for blind labellers
    raise unittest.SkipTest("expert/answer_key.json is withheld (blind labelling); see expert/README.md")
with open(KEY_PATH, encoding="utf-8") as _fh:
    KEY = json.load(_fh)["cases"]


def hist(k):
    return k.get("ground_truth_historical", k["ground_truth"])


def write_labels(path, key, pick, ids=None):
    """Write a label CSV answering pick(key entry) -> label dict for each id (default: all)."""
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["case_id", "liable_party", "remedy", "confidence", "notes"])
        for aid in ids if ids is not None else key:
            g = pick(key[aid])
            w.writerow([aid, g["liable_party"], g["remedy"], "4", "synthetic"])


class ExpertScoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def score(self, pick, ids=None, key=KEY):
        path = os.path.join(self.dir, "labels.csv")
        write_labels(path, key, pick, ids)
        return se.score(key, se.read_labels(path), arb={})

    def expected(self, answer, against):
        """Matches of an expert answering `answer` labels against the `against` labels, from the key."""
        out = {}
        for f in ("liable_party", "remedy"):
            out[f] = sum(answer(k)[f] == against(k)[f] for k in KEY.values())
        out["both"] = sum(answer(k)["liable_party"] == against(k)["liable_party"] and answer(k)["remedy"] == against(k)["remedy"]
                          for k in KEY.values())
        return out

    def test_key_has_the_two_documented_relabels(self):
        self.assertEqual(len(KEY), 40)
        # X89C5F changes liable party only, X9FC6C changes remedy only: fixes the expected counts below.
        self.assertNotEqual(KEY["X89C5F"]["ground_truth"]["liable_party"], hist(KEY["X89C5F"])["liable_party"])
        self.assertEqual(KEY["X89C5F"]["ground_truth"]["remedy"], hist(KEY["X89C5F"])["remedy"])
        self.assertEqual(KEY["X9FC6C"]["ground_truth"]["liable_party"], hist(KEY["X9FC6C"])["liable_party"])
        self.assertNotEqual(KEY["X9FC6C"]["ground_truth"]["remedy"], hist(KEY["X9FC6C"])["remedy"])

    def test_expert_answering_v14_labels(self):
        text, stats = self.score(lambda k: k["ground_truth"])
        ov = stats["overall"]
        self.assertEqual(ov["n"], 40)
        self.assertEqual(ov["v1.4"], {"liable_party": 40, "remedy": 40, "both": 40})
        exp = self.expected(lambda k: k["ground_truth"], hist)
        self.assertEqual(exp, {"liable_party": 39, "remedy": 39, "both": 38})
        self.assertEqual(ov["historical"], exp)
        self.assertIn("Labelled cases: 40 of 40.", text)
        self.assertIn("| Liable party and remedy both | 40/40 = 100%", text)
        # By level / stratum sum to the overall counts under both labels.
        for field in ("by_level", "by_stratum"):
            for v in ("v1.4", "historical"):
                for f in ("liable_party", "remedy", "both"):
                    self.assertEqual(sum(s[v][f] for s in stats[field].values()), ov[v][f], (field, v, f))
        self.assertEqual(stats["by_level"]["E1"]["historical"]["liable_party"], stats["by_level"]["E1"]["n"] - 1)
        self.assertEqual(stats["by_level"]["E0"]["historical"]["remedy"], stats["by_level"]["E0"]["n"] - 1)
        self.assertEqual(stats["calibration"]["4"], {"n": 40, "v1.4": 40, "historical": 39})
        # Disagreement list: only the two relabelled cases, each against the historical label only.
        self.assertEqual(stats["disagreements"], {"X89C5F": ["historical"], "X9FC6C": ["historical"]})
        self.assertIn("| X89C5F | D31 |", text)
        self.assertIn("AG4-D / merchant / refund | AG1-P / agent_provider / refund | historical |", text)

    def test_expert_answering_historical_labels(self):
        text, stats = self.score(hist)
        ov = stats["overall"]
        self.assertEqual(ov["historical"], {"liable_party": 40, "remedy": 40, "both": 40})
        exp = self.expected(hist, lambda k: k["ground_truth"])
        self.assertEqual(exp, {"liable_party": 39, "remedy": 39, "both": 38})
        self.assertEqual(ov["v1.4"], exp)
        self.assertEqual(stats["disagreements"], {"X89C5F": ["v1.4"], "X9FC6C": ["v1.4"]})
        self.assertIn("| X9FC6C | D43 |", text)

    def test_arbiter_columns_report_both_labels(self):
        # A synthetic arbiter that answers the historical liable party everywhere.
        arb = {aid: {"A1 test": (hist(k)["liable_party"], hist(k)["remedy"])} for aid, k in KEY.items()}
        path = os.path.join(self.dir, "labels.csv")
        write_labels(path, KEY, lambda k: k["ground_truth"])
        text, stats = se.score(KEY, se.read_labels(path), arb=arb)
        s = stats["arbiters"]["A1 test"]
        self.assertEqual(s["n"], 40)
        self.assertEqual(s["agree"], 39)
        self.assertEqual(s["v1.4"], {"expert_only": 1, "arbiter_only": 0})
        self.assertEqual(s["historical"], {"expert_only": 0, "arbiter_only": 1})
        self.assertIn("| A1 test | 40 | 39/40", text)

    def test_partial_label_file(self):
        ids = list(KEY)[:5]
        text, stats = self.score(lambda k: k["ground_truth"], ids=ids)
        self.assertIn("Labelled cases: 5 of 40.", text)
        self.assertEqual(stats["labelled"], 5)
        self.assertEqual(stats["overall"]["v1.4"]["liable_party"], 5)

    def test_relabel_check_real_key(self):
        derived, warnings = se.relabel_check(KEY)
        self.assertEqual(set(derived), {"X89C5F", "X9FC6C"})
        self.assertEqual(derived, se.DOCUMENTED_RELABELS)
        self.assertEqual(warnings, [])
        text, _ = self.score(lambda k: k["ground_truth"])
        self.assertNotIn("WARNING", text)
        self.assertIn("X89C5F (D31), X9FC6C (D43)", text)

    def test_relabel_check_doctored_key_warns(self):
        key = copy.deepcopy(KEY)
        third = next(aid for aid in key if aid not in se.DOCUMENTED_RELABELS)
        key[third]["ground_truth"] = dict(key[third]["ground_truth"], remedy="undetermined"
                                          if key[third]["ground_truth"]["remedy"] != "undetermined" else "deny")
        derived, warnings = se.relabel_check(key)
        self.assertEqual(set(derived), {"X89C5F", "X9FC6C", third})
        self.assertTrue(warnings)
        self.assertTrue(all(w.startswith("WARNING") for w in warnings))
        self.assertIn(third, warnings[0])
        # Written to the key file and run end-to-end: the report carries the WARNING, nothing crashes.
        key_path = os.path.join(self.dir, "key.json")
        with open(key_path, "w", encoding="utf-8") as fh:
            json.dump({"cases": key}, fh)
        labels = os.path.join(self.dir, "labels.csv")
        write_labels(labels, key, lambda k: k["ground_truth"])
        out = os.path.join(self.dir, "report.md")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(se.main([labels, "--key", key_path, "--out", out]), 0)
        with open(out, encoding="utf-8") as fh:
            self.assertIn("WARNING", fh.read())

    def test_main_end_to_end_writes_only_to_out(self):
        labels = os.path.join(self.dir, "labels.csv")
        write_labels(labels, KEY, lambda k: k["ground_truth"])
        out = os.path.join(self.dir, "expert_baseline.md")
        with redirect_stdout(io.StringIO()) as buf:
            self.assertEqual(se.main([labels, "--out", out]), 0)
        self.assertTrue(os.path.exists(out))
        with open(out, encoding="utf-8") as fh:
            report = fh.read()
        self.assertEqual(buf.getvalue(), report + "\n")
        self.assertIn("Labelled cases: 40 of 40.", report)
        self.assertIn("## Relabel check", report)
        self.assertIn("## Expert vs each arbiter", report)
        self.assertNotIn("WARNING", report)

    def test_title_and_note_label_a_partial_report(self):
        labels = os.path.join(self.dir, "labels.csv")
        write_labels(labels, KEY, lambda k: k["ground_truth"], ids=list(KEY)[:8])
        out = os.path.join(self.dir, "partial.md")
        default = os.path.join(self.dir, "default.md")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(se.main([labels, "--out", out, "--title", "Partial check", "--note", "Author-labelled; n = 8."]), 0)
            self.assertEqual(se.main([labels, "--out", default]), 0)
        with open(out, encoding="utf-8") as fh:
            partial = fh.read()
        with open(default, encoding="utf-8") as fh:
            plain = fh.read()
        self.assertTrue(partial.startswith("# Partial check\n\nAuthor-labelled; n = 8.\n\nLabelled cases: 8 of 40.\n"))
        self.assertTrue(plain.startswith("# " + se.TITLE + "\n\nLabelled cases: 8 of 40.\n"))
        # Everything after the heading block is identical: the options only label the report.
        self.assertEqual(partial.split("Labelled cases:", 1)[1], plain.split("Labelled cases:", 1)[1])


if __name__ == "__main__":
    unittest.main()

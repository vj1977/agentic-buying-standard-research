"""Tests for tools/schema_check (Audit 3, finding F15): the draft 2020-12 subset validator, and the
document check on the real standard/ABS_v0.3.md (embedded schemas and Appendix F examples)."""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.schema_check.cli import run
from tools.schema_check.mini2020 import SchemaError, Validator, apply_patch, self_tests, subset_scan

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standard" / "ABS_v0.3.md"


def valid(schema, inst, extra=None):
    """True if inst validates against schema (given $id 't'); extra: other schemas by $id."""
    schemas = {"t": {"$id": "t", **schema}, **(extra or {})}
    return not Validator(schemas).validate(inst, "t")


class KeywordTests(unittest.TestCase):
    # (keyword, schema, an instance that must validate, an instance that must not)
    CASES = [
        ("type", {"type": "string"}, "a", 1),
        ("type list", {"type": ["string", "null"]}, None, 1),
        ("type integer accepts 1.0, not true", {"type": "integer"}, 1.0, True),
        ("type integer rejects 1.5", {"type": "integer"}, 2, 1.5),
        ("type number rejects bool", {"type": "number"}, 1.5, False),
        ("enum", {"enum": ["a", 1]}, "a", "b"),
        ("enum: true is not 1", {"enum": [1]}, 1.0, True),
        ("const", {"const": "x"}, "x", "y"),
        ("const: false is not 0", {"const": False}, False, 0),
        ("required", {"required": ["a"]}, {"a": 1}, {"b": 1}),
        ("properties", {"properties": {"a": {"type": "string"}}}, {"a": "x"}, {"a": 1}),
        ("additionalProperties false", {"properties": {"a": {}}, "additionalProperties": False}, {"a": 1}, {"a": 1, "b": 2}),
        ("additionalProperties schema", {"properties": {"a": {}}, "additionalProperties": {"type": "integer"}},
         {"a": "x", "b": 2}, {"a": "x", "b": "y"}),
        ("items", {"items": {"type": "integer"}}, [1, 2], [1, "x"]),
        ("minItems", {"minItems": 1}, [1], []),
        ("maxItems", {"maxItems": 1}, [1], [1, 2]),
        ("minLength", {"minLength": 2}, "ab", "a"),
        ("maxLength", {"maxLength": 2}, "ab", "abc"),
        ("pattern", {"pattern": "^sha256:[0-9a-f]{4}$"}, "sha256:ab12", "sha256:AB12"),
        ("minimum", {"minimum": 1}, 1, 0.5),
        ("maximum", {"maximum": 1}, 1, 2),
        ("format date-time", {"format": "date-time"}, "2026-11-04T09:12:31Z", "2026-11-04 09:12"),
        ("format date", {"format": "date"}, "2026-11-04", "04/11/2026"),
        ("format uri", {"format": "uri"}, "urn:abs:mandate:1", "not a uri"),
        ("allOf", {"allOf": [{"type": "string"}, {"minLength": 2}]}, "ab", "a"),
        ("anyOf", {"anyOf": [{"type": "string"}, {"type": "integer"}]}, 1, None),
        ("not", {"not": {"type": "string"}}, 1, "a"),
        ("true schema / false schema", {"properties": {"a": True, "b": False}}, {"a": 1}, {"b": 1}),
    ]

    def test_each_keyword_accepts_and_rejects(self):
        for name, schema, good, bad in self.CASES:
            with self.subTest(keyword=name):
                self.assertTrue(valid(schema, good), f"{name}: {good!r} should validate")
                self.assertFalse(valid(schema, bad), f"{name}: {bad!r} should not validate")

    def test_type_specific_keywords_ignore_other_types(self):
        self.assertTrue(valid({"minLength": 5, "minimum": 3, "required": ["a"], "minItems": 2}, True))

    def test_one_of_requires_exactly_one(self):
        schema = {"oneOf": [{"type": "integer"}, {"minimum": 0}]}
        self.assertTrue(valid(schema, -1))    # integer only
        self.assertTrue(valid(schema, 1.5))   # minimum only
        v = Validator({"t": {"$id": "t", **schema}})
        self.assertEqual(v.validate(1, "t"), ["$: matches 2 of oneOf"])     # both
        self.assertEqual(v.validate(-1.5, "t"), ["$: matches 0 of oneOf"])  # neither

    def test_if_then_else(self):
        schema = {"if": {"properties": {"seq": {"const": 0}}, "required": ["seq"]},
                  "then": {"not": {"required": ["prev"]}},
                  "else": {"required": ["prev"]}}
        self.assertTrue(valid(schema, {"seq": 0}))
        self.assertFalse(valid(schema, {"seq": 0, "prev": "h"}))   # then branch
        self.assertTrue(valid(schema, {"seq": 1, "prev": "h"}))
        self.assertFalse(valid(schema, {"seq": 1}))                # else branch
        self.assertTrue(valid({"if": {"const": 1}}, 2))            # if alone has no effect

    def test_ref_local_json_pointer(self):
        schema = {"properties": {"h": {"$ref": "#/$defs/Hash"}},
                  "$defs": {"Hash": {"type": "string", "pattern": "^h:"}, "a/b~c": {"const": 1}}}
        self.assertTrue(valid(schema, {"h": "h:1"}))
        self.assertFalse(valid(schema, {"h": "x"}))
        escaped = {"$ref": "#/$defs/a~1b~0c", "$defs": schema["$defs"]}
        self.assertTrue(valid(escaped, 1))
        self.assertFalse(valid(escaped, 2))

    def test_ref_absolute_urn_with_pointer_and_sibling_keywords(self):
        other = {"urn:x:defs": {"$id": "urn:x:defs", "$defs": {"Hash": {"type": "string", "pattern": "^h:"},
                                                               "Ptr": {"$ref": "#/$defs/Hash"}}}}
        self.assertTrue(valid({"$ref": "urn:x:defs#/$defs/Hash", "maxLength": 4}, "h:1", other))
        self.assertFalse(valid({"$ref": "urn:x:defs#/$defs/Hash", "maxLength": 4}, "h:12345", other))  # sibling applies
        self.assertFalse(valid({"$ref": "urn:x:defs#/$defs/Hash"}, "x", other))
        # a local $ref inside the referenced document resolves against that document, not the caller
        self.assertFalse(valid({"$ref": "urn:x:defs#/$defs/Ptr"}, "x", other))

    def test_unresolved_ref_raises(self):
        for ref in ("urn:x:missing", "#/$defs/Missing", "#/$defs/A/0"):
            with self.subTest(ref=ref), self.assertRaises(SchemaError):
                valid({"$ref": ref, "$defs": {"A": {"type": "string"}}}, 1)

    def test_unsupported_keyword_raises(self):
        for kw, val in [("uniqueItems", True), ("prefixItems", [{}]), ("patternProperties", {}), ("contains", {}),
                        ("exclusiveMinimum", 0), ("minProperties", 1), ("dependentRequired", {}),
                        ("unevaluatedProperties", False), ("$dynamicRef", "#x")]:
            with self.subTest(keyword=kw), self.assertRaises(SchemaError):
                valid({kw: val}, 1)
        with self.assertRaises(SchemaError):
            valid({"properties": {"a": {"uniqueItems": True}}}, {"a": [1]})   # nested, when reached
        with self.assertRaises(SchemaError):
            valid({"format": "email"}, "a@b.c")                               # format outside the subset
        with self.assertRaises(SchemaError):
            valid({"items": [{"type": "integer"}]}, [1])                     # draft-4 tuple items

    def test_subset_scan_finds_unreached_and_malformed_nodes(self):
        schema = {"$id": "s", "$schema": "https://json-schema.org/draft/2020-12/schema",
                  "$defs": {"Unused": {"uniqueItems": True}, "Nested": {"$id": "inner"},
                            "T": {"type": "str"}, "F": {"format": "email"}, "P": {"pattern": "("},
                            "I": {"items": [{}]}, "O": {"oneOf": []}}}
        nodes, probs = subset_scan({"s": schema})
        text = "\n".join(probs)
        for needle in ("unsupported keyword(s) ['uniqueItems']", "nested $id", "unknown type(s) ['str']",
                       "unsupported format 'email'", "pattern does not compile", "/items: schema is list",
                       "/oneOf: not a non-empty array"):
            self.assertIn(needle, text)
        self.assertEqual(subset_scan({"s": {"$id": "s", "$schema": "http://json-schema.org/draft-07/schema#"}})[1],
                         ["s: $schema 'http://json-schema.org/draft-07/schema#' is not a root draft 2020-12 declaration"])
        self.assertEqual(subset_scan({"s": {"$id": "s", "type": "object", "properties": {"a": {"type": "string"}}}}),
                         (2, []))

    def test_apply_patch(self):
        base = {"a": 1, "b": {"c": [1, 2]}}
        out = apply_patch(base, [{"op": "replace", "path": "/a", "value": 2}, {"op": "remove", "path": "/b/c/0"},
                                 {"op": "add", "path": "/d~1e", "value": True}])
        self.assertEqual(out, {"a": 2, "b": {"c": [2]}, "d/e": True})
        self.assertEqual(base, {"a": 1, "b": {"c": [1, 2]}})  # not mutated
        with self.assertRaises(ValueError):
            apply_patch(base, [{"op": "replace", "path": "/z", "value": 1}])
        with self.assertRaises(ValueError):
            apply_patch(base, [{"op": "move", "from": "/a", "path": "/z"}])

    def test_builtin_self_tests(self):
        n, bad = self_tests()
        self.assertEqual((n, bad), (8, []))


FENCE = "```"
SYNTHETIC = f"""# Test document

{FENCE}json
{{"$id": "urn:t:s", "type": "object", "required": ["a"], "additionalProperties": false,
 "properties": {{"a": {{"type": "integer"}}, "b": {{"$ref": "#/$defs/B"}}}}, "$defs": {{"B": {{"type": "string"}}}}}}
{FENCE}

{FENCE}json
{{"$id": "urn:t:other", "type": "object", "required": ["z"]}}
{FENCE}

## Appendix F. Example instances

**F.1** (valid against `urn:t:s`). A positive example.

{FENCE}json
{{"example": "F.1", "schema": "urn:t:s", "expect": "valid", "instance": {{"a": 1, "b": "x"}}}}
{FENCE}

**F.2** (invalid against `urn:t:s`, patch of F.1). A negative example: a is a string.

{FENCE}json
{{"example": "F.2", "schema": "urn:t:s", "expect": "invalid", "base": "F.1",
 "patch": [{{"op": "replace", "path": "/a", "value": "x"}}]}}
{FENCE}
"""


class DocumentCheckTests(unittest.TestCase):
    def run_text(self, text):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "doc.md")
            with open(p, "w", encoding="utf-8") as f:
                f.write(text)
            return run(p)

    def assert_fails(self, text, needle):
        r = self.run_text(text)
        self.assertTrue(r["failures"], "the check passed a broken document")
        self.assertTrue(any(needle in f for f in r["failures"]), f"{needle!r} not in {r['failures']}")

    def test_synthetic_document_passes(self):
        r = self.run_text(SYNTHETIC)
        self.assertEqual(r["failures"], [])
        self.assertEqual((r["schemas"], r["positive"], r["positive_valid"], r["negative"], r["negative_invalid"]),
                         (2, 1, 1, 1, 1))

    def test_each_defect_class_fails(self):
        s = SYNTHETIC
        cases = [
            ("unparsable block", s.replace('"b": "x"}}', '"b": "x"}'), "does not parse"),
            ("unsupported keyword", s.replace('"required": ["z"]', '"required": ["z"], "uniqueItems": true'),
             "unsupported keyword(s) ['uniqueItems']"),
            ("unresolved $ref", s.replace("#/$defs/B", "#/$defs/C"), "pointer does not resolve"),
            ("positive fails", s.replace('"instance": {"a": 1,', '"instance": {"a": "1",'), "expected valid"),
            ("negative validates", s.replace('"value": "x"', '"value": 2'), "but it validates"),
            ("caption disagrees", s.replace("**F.1** (valid", "**F.1** (invalid"), "caption and block disagree"),
            ("caption missing", s.replace("**F.2** (invalid against `urn:t:s`, patch of F.1).", "F.2."), "no caption"),
            ("base invalid for the negative's schema",
             s.replace('"example": "F.2", "schema": "urn:t:s"', '"example": "F.2", "schema": "urn:t:other"')
              .replace("(invalid against `urn:t:s`, patch", "(invalid against `urn:t:other`, patch"),
             "not attributable to the patch"),
            ("non-example block in Appendix F", s + f'\n{FENCE}json\n{{"a": 1}}\n{FENCE}\n', "is not an example object"),
            ("no examples", s.split("## Appendix F")[0], "no 'Appendix F' heading"),
        ]
        for name, text, needle in cases:
            with self.subTest(defect=name):
                self.assert_fails(text, needle)


class RealStandardTests(unittest.TestCase):
    def test_abs_v03_schemas_and_appendix_f(self):
        r = run(str(STANDARD))
        self.assertEqual(r["failures"], [], "standard/ABS_v0.3.md fails the schema check:\n" + "\n".join(r["failures"]))
        self.assertGreaterEqual(r["schemas"], 1)
        self.assertGreaterEqual(r["positive"], 1)
        self.assertGreaterEqual(r["negative"], 1)
        self.assertEqual(r["positive_valid"], r["positive"])
        self.assertEqual(r["negative_invalid"], r["negative"])

    def test_cli_exit_codes(self):
        ok = subprocess.run([sys.executable, "-B", "-m", "tools.schema_check", str(STANDARD)], cwd=ROOT,
                            capture_output=True, text=True)
        self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
        self.assertIn("RESULT: all checks passed", ok.stdout)
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "bad.md")
            with open(p, "w", encoding="utf-8") as f:
                f.write(SYNTHETIC.replace('"value": "x"', '"value": 2'))
            bad = subprocess.run([sys.executable, "-B", "-m", "tools.schema_check", p], cwd=ROOT,
                                 capture_output=True, text=True)
            self.assertEqual(bad.returncode, 1, bad.stdout + bad.stderr)
            self.assertIn("RESULT: 1 failure(s)", bad.stdout)
            missing = subprocess.run([sys.executable, "-B", "-m", "tools.schema_check", os.path.join(d, "absent.md")],
                                     cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(missing.returncode, 2)


if __name__ == "__main__":
    unittest.main()

import unittest

from acs.agent import build_prompt, parse_action
from acs.marketplace import ISSUED_TOKEN


class ParseTests(unittest.TestCase):
    def test_plain(self):
        r = parse_action('{"tool": "search", "args": {"query": "mouse"}, "reason": "x"}')
        self.assertEqual(r.action, {"tool": "search", "args": {"query": "mouse"}, "reason": "x"})
        self.assertFalse(r.lenient)

    def test_fenced_with_prose(self):
        r = parse_action('Sure.\n```json\n{"tool": "view_cart", "args": {}}\n```\nDone')
        self.assertEqual(r.action["tool"], "view_cart")

    def test_alternate_keys_and_string_qty(self):
        r = parse_action('{"action": "add_to_cart", "arguments": {"product_id": "p1", "qty": "2"}}')
        self.assertEqual(r.action["args"], {"product_id": "p1", "qty": 2})
        self.assertTrue(r.lenient)

    def test_default_qty(self):
        r = parse_action('{"tool": "add_to_cart", "args": {"product_id": "p1"}}')
        self.assertEqual(r.action["args"]["qty"], 1)

    def test_errors(self):
        self.assertIsNone(parse_action("no json here").action)
        self.assertIn("unknown tool", parse_action('{"tool": "pay", "args": {}}').error)
        self.assertIn("needs argument", parse_action('{"tool": "checkout", "args": {}}').error)
        self.assertIn("integer", parse_action('{"tool": "add_to_cart", "args": {"product_id": "p", "qty": true}}').error)
        self.assertIn("string", parse_action('{"tool": "search", "args": {"query": 5}}').error)

    def test_first_valid_object_wins(self):
        r = parse_action('{"note": 1} then {"tool": "finish", "args": {"summary": "ok"}}')
        self.assertEqual(r.action["tool"], "finish")

    def test_braces_inside_strings(self):
        r = parse_action('{"tool": "ask_user", "args": {"question": "Which {model} do you want?"}}')
        self.assertEqual(r.action["args"]["question"], "Which {model} do you want?")

    def test_prompt_contains_task_token_and_history(self):
        p = build_prompt("Buy X", [{"action": {"tool": "view_cart", "args": {}}, "result": {"lines": []}}], "bad")
        self.assertIn("Buy X", p)
        self.assertIn(ISSUED_TOKEN, p)
        self.assertIn('[1] action: {"args":{},"tool":"view_cart"}', p)
        self.assertIn("PREVIOUS REPLY WAS INVALID: bad", p)


if __name__ == "__main__":
    unittest.main()


class RepairTests(unittest.TestCase):
    def test_missing_closing_brace_is_repaired(self):
        from acs.agent import extract_json_objects
        self.assertEqual(extract_json_objects('{"file": false, "note": "a } b"'), [{"file": False, "note": "a } b"}])
        self.assertEqual(extract_json_objects('{"x": [1, {"y": "z"'), [{"x": [1, {"y": "z"}]}])
        self.assertEqual(extract_json_objects('no json'), [])


class RepairOuterTests(unittest.TestCase):
    def test_truncated_outer_action_wins_over_inner_object(self):
        from acs.agent import parse_action
        self.assertEqual(parse_action('{"tool": "search", "args": {"query": "x"}').action["tool"], "search")

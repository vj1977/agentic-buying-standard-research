"""Audit 1, F27: the Claude isolation check must fail closed, and every future call is content-addressed in the ledger.

No CLI is run: the subprocess layer is replaced by fixtures.
"""

import json
import os
import tempfile
import unittest
from unittest import mock

from acs import backends
from acs.backends import CallLog, ClaudeCLI, GrokCLI, IsolationError, MockBackend, sha256_text

ACCOUNT = {"config_dir": None, "email": "test@example.org", "subscription": "test"}
RESULT = {"type": "result", "subtype": "success", "is_error": False, "result": "{\"ok\": true}", "num_turns": 1,
          "usage": {"input_tokens": 10, "output_tokens": 3}}


def claude_stdout(*events) -> str:
    return json.dumps(list(events))


class ClaudeIsolationTests(unittest.TestCase):
    def _complete(self, stdout: str):
        b = ClaudeCLI("claude-test", None, CallLog(None))
        with mock.patch.object(backends, "resolve_claude_account", return_value=dict(ACCOUNT)), \
                mock.patch.object(ClaudeCLI, "_run", return_value=(stdout, "", 0.1)):
            return b._complete("system", "prompt")

    def test_missing_init_event_is_an_isolation_failure(self):
        """The audit's counterexample: no init event used to be accepted and reported as tools=[]."""
        with self.assertRaises(IsolationError):
            self._complete(claude_stdout(RESULT))

    def test_init_without_a_tools_attestation_fails(self):
        with self.assertRaises(IsolationError):
            self._complete(claude_stdout({"type": "system", "subtype": "init", "model": "claude-test"}, RESULT))

    def test_init_with_tools_or_mcp_fails(self):
        with self.assertRaises(IsolationError):
            self._complete(claude_stdout({"type": "system", "subtype": "init", "tools": ["Bash"], "mcp_servers": []}, RESULT))
        with self.assertRaises(IsolationError):
            self._complete(claude_stdout({"type": "system", "subtype": "init", "tools": [], "mcp_servers": [{"name": "x", "status": "connected"}]}, RESULT))

    def test_positive_attestation_passes_and_records_served_model(self):
        comp = self._complete(claude_stdout({"type": "system", "subtype": "init", "tools": [], "mcp_servers": [], "model": "claude-test-served"}, RESULT))
        self.assertEqual(comp.meta["tools"], [])
        self.assertEqual(comp.meta["served_model"], "claude-test-served")
        self.assertTrue(comp.meta["isolation_attested"])

    def test_single_result_object_without_init_fails(self):
        with self.assertRaises(IsolationError):
            self._complete(json.dumps(RESULT))


class GrokIsolationTests(unittest.TestCase):
    def test_missing_tool_count_fails_closed(self):
        b = GrokCLI("grok-test", None, CallLog(None))
        with mock.patch.object(GrokCLI, "_run", return_value=(json.dumps({"text": "x"}), "", 0.1)), \
                mock.patch.object(GrokCLI, "_user_mcp_servers", return_value=[]):
            with self.assertRaises(IsolationError):
                b._complete("system", "prompt")


class LedgerTests(unittest.TestCase):
    def test_future_calls_are_content_addressed(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "calls.jsonl")
            with open(path, "w", encoding="utf-8") as fh:  # a historical line: never rewritten
                fh.write(json.dumps({"ts": 1, "run_id": "old", "model": "m", "prompt_chars": 5}) + "\n")
            log = CallLog(path, run_id="new", blob_dir=os.path.join(d, "blobs"))
            b = MockBackend("mock-m", lambda s, p: "OUT", log)
            b.complete("SYS", "PROMPT", purpose="arbiter", context={"bundle_sha256": "b" * 64, "case_id": "D01"})
            lines = [json.loads(l) for l in open(path, encoding="utf-8")]
            self.assertEqual(lines[0], {"ts": 1, "run_id": "old", "model": "m", "prompt_chars": 5})
            rec = lines[1]
            self.assertEqual(rec["ledger_version"], 2)
            self.assertEqual(rec["system_sha256"], sha256_text("SYS"))
            self.assertEqual(rec["prompt_sha256"], sha256_text("PROMPT"))
            self.assertEqual(rec["output_sha256"], sha256_text("OUT"))
            self.assertEqual(rec["context"], {"bundle_sha256": "b" * 64, "case_id": "D01"})
            self.assertEqual(rec["cli"], {"backend": "mock", "version": "mock"})
            self.assertEqual(rec["config"]["model"], "mock-m")
            self.assertIn("commit", rec["revision"])
            for h, text in ((rec["system_sha256"], "SYS"), (rec["prompt_sha256"], "PROMPT"), (rec["output_sha256"], "OUT")):
                with open(os.path.join(d, "blobs", h[:2], h + ".txt"), encoding="utf-8") as fh:
                    self.assertEqual(fh.read(), text)

    def test_failed_call_is_ledgered_without_output(self):
        def boom(s, p):
            raise backends.BackendError("down")
        log = CallLog(None)
        seen = []
        log.write = lambda rec: seen.append(rec)
        with self.assertRaises(backends.BackendError):
            MockBackend("mock-m", boom, log).complete("S", "P")
        self.assertEqual((seen[0]["ok"], seen[0]["output_sha256"], seen[0]["prompt_sha256"]), (False, None, sha256_text("P")))


if __name__ == "__main__":
    unittest.main()

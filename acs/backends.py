"""Model backends: stateless CLI calls (subscription logins) plus a mock.

Each call runs in a fresh, empty temporary working directory with the
CLI's own tools disabled, so the model can only return text. Isolation is
checked at runtime, not assumed, and the check fails closed (Audit 1, F27):
  * claude: the output must contain an init event, it must carry a "tools" list that is empty, and it
    must list no MCP servers. A missing init event is an isolation failure. (Before Audit 1 a missing
    init event was accepted and reported as tools=[]; every stored A1 Claude call with a meta record,
    866 of them, carries the init event's served model, so that path was not taken there.)
  * grok: the debug log must report tool_count=0 for every request.
A failed check raises IsolationError, which stops the run.

Ledger (Audit 1, F27; applies to calls made after the audit, the historical lines of
results/calls.jsonl are never rewritten): every call appends one record with ledger_version 2 carrying
the SHA-256 of the system prompt, the user prompt (which contains the evidence package) and the output,
an optional caller context (for example the canonical bundle hash), the git revision, the CLI and its
version, and the backend configuration. With a blob directory the three texts are also stored
content-addressed (<blob_dir>/<hash[:2]>/<hash>.txt).
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import threading
import time
import tomllib
from dataclasses import dataclass, field

CALL_TIMEOUT_S = 240
_LOG_LOCK = threading.Lock()
# A matching error is fatal: the run stops instead of logging the failure as a record. Phase 3b (Deviation 6): grok's
# "402 Payment Required: ... usage balance exhausted" did not match and turned 20 calls into no-decision records.
LIMIT_PATTERNS = re.compile(r"usage limit|rate limit|quota|too many requests|weekly limit|limit reached|429|payment required|balance exhausted|"
                            r"usage balance|credit balance|out of credits|insufficient (?:credit|funds|balance)", re.I)


class BackendError(Exception):
    def __init__(self, message: str, fatal: bool = False):
        super().__init__(message)
        self.fatal = fatal


class IsolationError(BackendError):
    def __init__(self, message: str):
        super().__init__(message, fatal=True)


@dataclass
class Completion:
    text: str
    duration_s: float
    meta: dict = field(default_factory=dict)


def sha256_text(text: str | None) -> str | None:
    return None if text is None else hashlib.sha256(text.encode("utf-8")).hexdigest()


_REVISION: dict | None = None
CODE_PATHS = ("acs", "rulebook", "models.json", "tools", "data/disputes")


def code_revision() -> dict:
    """The git commit of this checkout and whether its code (CODE_PATHS: code, rulebook, model registry, case files) differs from
    that commit (computed once per process)."""
    global _REVISION
    if _REVISION is None:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        rev = {"commit": None, "dirty": None}
        try:
            head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, timeout=20)
            if head.returncode == 0:
                rev["commit"] = head.stdout.strip()
                # code paths only: the call ledger and result files change during a run and say nothing about the code that ran
                st = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no", "--", *CODE_PATHS], cwd=root, capture_output=True, text=True, timeout=20)
                rev["dirty"] = bool(st.stdout.strip()) if st.returncode == 0 else None
        except (OSError, subprocess.TimeoutExpired):
            pass
        _REVISION = rev
    return dict(_REVISION)


class CallLog:
    """Append-only JSONL log of every model call (call count and, from Audit 1, the content-addressed ledger)."""

    def __init__(self, path: str | None, run_id: str = "", blob_dir: str | None = None):
        self.path = path
        self.run_id = run_id
        self.count = 0
        self.thread_counts: dict[int, int] = {}  # calls written per thread (C1 budget: the calls a work unit has made so far)
        self.blob_dir = blob_dir if blob_dir is not None else (os.path.join(os.path.dirname(path), "call_blobs") if path else None)

    def store_blob(self, text: str | None) -> None:
        if text is None or not self.blob_dir:
            return
        h = sha256_text(text)
        d = os.path.join(self.blob_dir, h[:2])
        target = os.path.join(d, h + ".txt")
        if os.path.exists(target):
            return
        os.makedirs(d, exist_ok=True)
        tmp = f"{target}.{os.getpid()}.{threading.get_ident()}.tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.replace(tmp, target)

    def write(self, record: dict) -> None:
        with _LOG_LOCK:
            self.count += 1
            tid = threading.get_ident()
            self.thread_counts[tid] = self.thread_counts.get(tid, 0) + 1
            if not self.path:
                return
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            with open(self.path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps({"ts": time.time(), "run_id": self.run_id, **record}) + "\n")


class Backend:
    backend = "base"

    def __init__(self, model: str, effort: str | None = None, call_log: CallLog | None = None,
                 timeout_s: int = CALL_TIMEOUT_S):
        self.model = model
        self.effort = effort
        self.call_log = call_log or CallLog(None)
        self.timeout_s = timeout_s

    def account(self) -> dict:
        return {}

    _cli_versions: dict = {}
    _cli_lock = threading.Lock()

    def cli_version(self) -> str | None:
        """The CLI's own --version output, asked once per backend kind and process (no model call)."""
        cls = type(self)
        if cls.backend not in ("claude", "grok", "codex", "gemini"):
            return None
        with Backend._cli_lock:
            if cls.backend not in Backend._cli_versions:
                try:
                    proc = subprocess.run([cls.backend, "--version"], capture_output=True, text=True, timeout=30, stdin=subprocess.DEVNULL)
                    Backend._cli_versions[cls.backend] = (proc.stdout or proc.stderr).strip()[:200] or None
                except (OSError, subprocess.TimeoutExpired):
                    Backend._cli_versions[cls.backend] = None
            return Backend._cli_versions[cls.backend]

    def config(self) -> dict:
        return {"model": self.model, "effort": self.effort, "timeout_s": self.timeout_s, **({"max_turns": self.max_turns} if hasattr(self, "max_turns") else {})}

    def complete(self, system: str, prompt: str, purpose: str = "agent", context: dict | None = None) -> Completion:
        """context: optional caller facts for the ledger (for example {"bundle_sha256": ..., "case_id": ...})."""
        t0 = time.time()
        err = None
        comp = None
        try:
            comp = self._complete(system, prompt)
            return comp
        except BackendError as exc:
            err = str(exc)[:500]
            raise
        finally:
            dur = time.time() - t0
            meta = comp.meta if comp else {}
            output = comp.text if comp else None
            for text in (system, prompt, output):
                self.call_log.store_blob(text)
            self.call_log.write({"backend": self.backend, "model": self.model, "purpose": purpose,
                                 "duration_s": round(dur, 2), "ok": err is None, "error": err,
                                 "prompt_chars": len(system) + len(prompt),
                                 "tokens_in": meta.get("tokens_in"), "tokens_out": meta.get("tokens_out"),
                                 # ledger v2 (Audit 1, F27)
                                 "ledger_version": 2, "system_sha256": sha256_text(system), "prompt_sha256": sha256_text(prompt),
                                 "output_sha256": sha256_text(output), "context": context or {}, "revision": code_revision(),
                                 "cli": {"backend": self.backend, "version": self.cli_version()}, "config": self.config(),
                                 "served_model": meta.get("served_model"), "isolation": {k: meta[k] for k in ("isolation_attested", "tools", "tool_count", "item_types") if k in meta}})

    def _complete(self, system: str, prompt: str) -> Completion:  # pragma: no cover - abstract
        raise NotImplementedError

    # ---- shared subprocess helper -----------------------------------------
    def _run(self, cmd: list[str], stdin: str | None, cwd: str, env: dict | None = None) -> tuple[str, str, float]:
        t0 = time.time()
        try:
            proc = subprocess.run(cmd, input=stdin, capture_output=True, text=True, cwd=cwd,
                                  env=env, timeout=self.timeout_s)
        except subprocess.TimeoutExpired as exc:
            raise BackendError(f"{self.backend} timed out after {self.timeout_s}s") from exc
        dur = time.time() - t0
        if proc.returncode != 0:
            blob = (proc.stdout or "")[-1500:] + "\n" + (proc.stderr or "")[-1500:]
            raise BackendError(f"{self.backend} exit {proc.returncode}: {blob.strip()[:1200]}",
                               fatal=bool(LIMIT_PATTERNS.search(blob)))
        return proc.stdout, proc.stderr, dur


def claude_auth_status(config_dir: str | None) -> dict:
    env = dict(os.environ)
    if config_dir:
        env["CLAUDE_CONFIG_DIR"] = config_dir
    else:
        env.pop("CLAUDE_CONFIG_DIR", None)
    try:
        proc = subprocess.run(["claude", "auth", "status"], capture_output=True, text=True, env=env, timeout=60)
        return json.loads(proc.stdout)
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError):
        return {"loggedIn": False}


_CLAUDE_ACCOUNT: dict | None = None
_CLAUDE_ACCOUNT_LOCK = threading.Lock()


def resolve_claude_account() -> dict:
    """Use ~/.claude-vjuruss (or $ACS_CLAUDE_CONFIG_DIR) when it holds a login, else the default login."""
    global _CLAUDE_ACCOUNT
    with _CLAUDE_ACCOUNT_LOCK:
        if _CLAUDE_ACCOUNT is None:
            candidate = os.environ.get("ACS_CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude-vjuruss")
            chosen = None
            if os.path.isdir(candidate):
                st = claude_auth_status(candidate)
                if st.get("loggedIn"):
                    chosen = {"config_dir": candidate, "email": st.get("email"), "subscription": st.get("subscriptionType")}
            if chosen is None:
                st = claude_auth_status(None)
                chosen = {"config_dir": None, "email": st.get("email"), "subscription": st.get("subscriptionType"),
                          "logged_in": bool(st.get("loggedIn"))}
            cfg = os.path.join(chosen["config_dir"], ".claude.json") if chosen["config_dir"] else os.path.expanduser("~/.claude.json")
            try:
                with open(cfg, encoding="utf-8") as fh:
                    chosen["claude_json_email"] = (json.load(fh).get("oauthAccount") or {}).get("emailAddress")
            except (OSError, json.JSONDecodeError):
                chosen["claude_json_email"] = None
            _CLAUDE_ACCOUNT = chosen
        return dict(_CLAUDE_ACCOUNT)


def check_claude_isolation(init: dict | None) -> None:
    """Positive attestation: an init event exists, carries a "tools" list, the list is empty, and no MCP server is listed."""
    if init is None:
        raise IsolationError("claude output had no init event; cannot verify that the session had no tools")
    if not isinstance(init.get("tools"), list):
        raise IsolationError(f"claude init event carried no tools list ({sorted(init)}); cannot verify isolation")
    if init["tools"] or init.get("mcp_servers"):
        raise IsolationError(f"claude session had tools {init.get('tools')} / MCP {init.get('mcp_servers')}")


class ClaudeCLI(Backend):
    backend = "claude"

    def account(self) -> dict:
        return resolve_claude_account()

    def _complete(self, system: str, prompt: str) -> Completion:
        acct = resolve_claude_account()
        env = dict(os.environ)
        if acct.get("config_dir"):
            env["CLAUDE_CONFIG_DIR"] = acct["config_dir"]
        else:
            env.pop("CLAUDE_CONFIG_DIR", None)
        work = tempfile.mkdtemp(prefix="acs-claude-")
        try:
            cmd = ["claude", "-p", "--model", self.model, "--output-format", "json",
                   "--tools", "", "--system-prompt", system, "--strict-mcp-config",
                   "--no-session-persistence", "--safe-mode", "--disable-slash-commands"]
            if self.effort:
                cmd += ["--effort", self.effort]
            out, _err, dur = self._run(cmd, prompt, work, env=env)
        finally:
            shutil.rmtree(work, ignore_errors=True)
        try:
            events = json.loads(out)
        except json.JSONDecodeError as exc:
            raise BackendError(f"claude returned non-JSON output: {out[:300]}") from exc
        if isinstance(events, dict):
            events = [events]
        init = next((e for e in events if isinstance(e, dict) and e.get("type") == "system" and e.get("subtype") == "init"), None)
        check_claude_isolation(init)
        result = next((e for e in events if e.get("type") == "result"), None)
        if result is None:
            raise BackendError("claude output had no result event")
        if result.get("is_error"):
            text = str(result.get("result"))
            raise BackendError(f"claude error: {text[:500]}", fatal=bool(LIMIT_PATTERNS.search(text)))
        usage = result.get("usage") or {}
        tokens_in = sum(int(usage.get(k) or 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
        return Completion(text=result.get("result") or "", duration_s=dur,
                          meta={"tokens_in": tokens_in, "tokens_out": usage.get("output_tokens"),
                                "num_turns": result.get("num_turns"), "tools": init["tools"], "isolation_attested": True,
                                "account": acct.get("email"), "served_model": init.get("model")})


class GrokCLI(Backend):
    """grok headless, isolated from the user's Claude/Cursor config, MCP servers and tools."""

    backend = "grok"
    max_turns = 1  # attacker backends in Phase 3 use 3: the models often emit a plan message before the answer
    _overlay_lock = threading.Lock()
    _overlay_dir: str | None = None

    @classmethod
    def _overlay(cls) -> str:
        with cls._overlay_lock:
            if cls._overlay_dir is None:
                d = tempfile.mkdtemp(prefix="acs-grok-overlay-")
                os.makedirs(os.path.join(d, "home"))
                with open(os.path.join(d, "overlay.toml"), "w") as fh:
                    fh.write('[ui]\nyolo = false\npermission_mode = "default"\n\n[subagents]\nenabled = false\n')
                cls._overlay_dir = d
            return cls._overlay_dir

    @staticmethod
    def _user_mcp_servers() -> list[str]:
        path = os.path.expanduser("~/.grok/config.toml")
        try:
            with open(path, "rb") as fh:
                return sorted((tomllib.load(fh).get("mcp_servers") or {}).keys())
        except (OSError, tomllib.TOMLDecodeError):
            return []

    def _complete(self, system: str, prompt: str) -> Completion:
        overlay = self._overlay()
        work = tempfile.mkdtemp(prefix="acs-grok-")
        side = tempfile.mkdtemp(prefix="acs-grok-io-")
        try:
            # Project-scoped config replaces same-named user MCP servers: disable them all.
            os.makedirs(os.path.join(work, ".grok"))
            with open(os.path.join(work, ".grok", "config.toml"), "w") as fh:
                for name in self._user_mcp_servers():
                    fh.write(f'[mcp_servers."{name}"]\nurl = "http://127.0.0.1:9/disabled"\nenabled = false\n\n')
            prompt_file = os.path.join(side, "prompt.txt")
            debug_file = os.path.join(side, "debug.log")
            with open(prompt_file, "w", encoding="utf-8") as fh:
                fh.write(prompt)
            env = dict(os.environ)
            env.update({"HOME": os.path.join(overlay, "home"), "GROK_HOME": os.path.expanduser("~/.grok"),
                        "GROK_CONFIG": os.path.join(overlay, "overlay.toml"), "GROK_DISABLE_AUTOUPDATER": "1",
                        "GROK_SUBAGENTS": "0", "GROK_MEMORY": "0"})
            cmd = ["grok", "-m", self.model, "--prompt-file", prompt_file, "--output-format", "json",
                   "--system-prompt-override", system, "--tools", "todo_write",
                   "--disallowed-tools", "todo_write,Agent,search_tool,use_tool", "--disable-web-search",
                   "--no-subagents", "--max-turns", str(self.max_turns), "--verbatim", "--debug-file", debug_file]
            if self.effort:
                cmd += ["--reasoning-effort", self.effort]
            out, _err, dur = self._run(cmd, None, work, env=env)
            try:
                with open(debug_file, encoding="utf-8", errors="replace") as fh:
                    dbg = fh.read()
            except OSError:
                dbg = ""
        finally:
            shutil.rmtree(work, ignore_errors=True)
            shutil.rmtree(side, ignore_errors=True)
        counts = [int(x) for x in re.findall(r"tool_count=(\d+)", dbg)]
        if not counts:
            raise IsolationError("grok debug log did not report tool_count; cannot verify isolation")
        if max(counts) > 0:
            raise IsolationError(f"grok request carried tools (tool_count={max(counts)})")
        try:
            data = json.loads(out)
        except json.JSONDecodeError as exc:
            raise BackendError(f"grok returned non-JSON output: {out[:300]}",
                               fatal=bool(LIMIT_PATTERNS.search(out))) from exc
        text = data.get("text")
        if text is None:
            raise BackendError(f"grok output had no text: {str(data)[:300]}", fatal=bool(LIMIT_PATTERNS.search(str(data))))
        usage = data.get("usage") or {}
        return Completion(text=text, duration_s=dur,
                          meta={"tokens_in": (usage.get("input_tokens") or 0) + (usage.get("cache_read_input_tokens") or 0),
                                "tokens_out": usage.get("output_tokens"), "tool_count": max(counts)})


# Confirmatory amendment C1: the codex backend is isolated by configuration and checked at runtime, failing closed.
# Configuration: the user's config.toml (MCP servers, notify hooks, project trust) and exec-policy rules are not loaded, project
# docs are off, web search is disabled, approvals never prompt, the sandbox is read-only and every tool feature the CLI lists is
# disabled. Runtime check (`check_codex_isolation`) on the --json event stream: a thread.started and a turn.completed event and at
# least one agent_message item must be present, and every item must be an agent_message or reasoning item (an "error" item is
# recorded, not a tool); any other item (command_execution, file_change, mcp_tool_call, web_search, todo_list, collab or unknown)
# is an IsolationError, which stops the run. A missing or unparsable event stream is an IsolationError too.
CODEX_DISABLED_FEATURES = ("shell_tool", "unified_exec", "apps", "plugins", "hooks", "multi_agent", "image_generation", "view_image",
                           "browser_use", "browser_use_external", "computer_use", "in_app_browser", "sleep_tool", "goals", "tool_suggest",
                           "code_mode_host", "skill_mcp_dependency_install")
CODEX_TEXT_ITEMS = {"agent_message", "reasoning"}


def _codex_item_type(item) -> str | None:
    if not isinstance(item, dict):
        return None
    return item.get("type") or item.get("item_type")


def parse_codex_events(stdout: str) -> list[dict]:
    events = []
    for line in (stdout or "").splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(ev, dict):
            events.append(ev)
    return events


def check_codex_isolation(events: list[dict]) -> dict:
    """Positive attestation from `codex exec --json` events (fail closed). Returns {text, item_types, errors, usage, thread_id}."""
    if not events:
        raise IsolationError("codex produced no JSON events; cannot verify that the session used no tools")
    kinds = [str(e.get("type")) for e in events]
    failed = [e for e in events if e.get("type") in ("turn.failed", "error")]
    if failed and "turn.completed" not in kinds:
        msg = json.dumps(failed[-1])[:500]
        raise BackendError(f"codex turn failed: {msg}", fatal=bool(LIMIT_PATTERNS.search(msg)))
    if "thread.started" not in kinds:
        raise IsolationError("codex event stream has no thread.started event; cannot verify isolation")
    if "turn.completed" not in kinds:
        raise IsolationError("codex event stream has no turn.completed event; cannot verify isolation")
    items = [e.get("item") or {} for e in events if str(e.get("type", "")).startswith("item.")]
    types = {_codex_item_type(i) for i in items}
    errors = [i.get("message") or i.get("text") for i in items if _codex_item_type(i) == "error"]
    bad = sorted(str(t) for t in types - CODEX_TEXT_ITEMS - {"error"})
    if bad:
        raise IsolationError(f"codex session produced non-text items {bad}: tools were available and used")
    messages = [i for e in events if e.get("type") == "item.completed" for i in [e.get("item") or {}] if _codex_item_type(i) == "agent_message"]
    if not messages:
        raise IsolationError("codex event stream has no completed agent_message")
    usage = next((e.get("usage") or {} for e in reversed(events) if e.get("type") == "turn.completed"), {})
    thread = next((e.get("thread_id") for e in events if e.get("type") == "thread.started"), None)
    return {"text": messages[-1].get("text") or "", "item_types": sorted(str(t) for t in types), "errors": errors, "usage": usage, "thread_id": thread}


class CodexCLI(Backend):
    """codex exec, read-only sandbox, ephemeral, user config ignored, tool features disabled, --json events checked (fail closed).
    It has no system-prompt flag, so the system text is prepended."""

    backend = "codex"

    def command(self, work: str, last: str) -> list[str]:
        cmd = ["codex", "exec", "-m", self.model, "--skip-git-repo-check", "-s", "read-only", "--ephemeral", "--ignore-user-config", "--ignore-rules",
               "--color", "never", "--json", "-C", work, "--output-last-message", last,
               "-c", 'approval_policy="never"', "-c", 'web_search="disabled"', "-c", "project_doc_max_bytes=0"]
        for feature in CODEX_DISABLED_FEATURES:
            cmd += ["--disable", feature]
        if self.effort:
            cmd += ["-c", f'model_reasoning_effort="{self.effort}"']
        return cmd + ["-"]

    def config(self) -> dict:
        return {**super().config(), "sandbox": "read-only", "ignore_user_config": True, "web_search": "disabled",
                "disabled_features": list(CODEX_DISABLED_FEATURES)}

    def _complete(self, system: str, prompt: str) -> Completion:
        work = tempfile.mkdtemp(prefix="acs-codex-")
        side = tempfile.mkdtemp(prefix="acs-codex-io-")
        try:
            last = os.path.join(side, "last.txt")
            out, _err, dur = self._run(self.command(work, last), f"{system}\n\n{prompt}\n\nDo not run any commands. Reply with text only.", work)
            att = check_codex_isolation(parse_codex_events(out))
            try:
                with open(last, encoding="utf-8") as fh:
                    text = fh.read()
            except OSError:
                text = att["text"]
        finally:
            shutil.rmtree(work, ignore_errors=True)
            shutil.rmtree(side, ignore_errors=True)
        usage = att["usage"]
        return Completion(text=text, duration_s=dur,
                          meta={"tokens_in": (usage.get("input_tokens") or 0), "tokens_out": usage.get("output_tokens"),
                                "isolation_attested": True, "tools": [], "item_types": att["item_types"], "codex_errors": att["errors"],
                                "thread_id": att["thread_id"]})


class GeminiCLI(Backend):
    backend = "gemini"

    def _complete(self, system: str, prompt: str) -> Completion:
        work = tempfile.mkdtemp(prefix="acs-gemini-")
        try:
            cmd = ["gemini", "-m", self.model, "-o", "json", "--skip-trust", "--approval-mode", "plan", "-p", ""]
            out, _err, dur = self._run(cmd, f"{system}\n\n{prompt}", work)
        finally:
            shutil.rmtree(work, ignore_errors=True)
        try:
            data = json.loads(out)
        except json.JSONDecodeError as exc:
            raise BackendError(f"gemini returned non-JSON output: {out[:300]}") from exc
        return Completion(text=data.get("response") or "", duration_s=dur, meta={})


class MockBackend(Backend):
    """Deterministic scripted backend for tests. policy(system, prompt) -> text."""

    backend = "mock"

    def __init__(self, model: str, policy, call_log: CallLog | None = None):
        super().__init__(model, None, call_log)
        self.policy = policy
        self.calls: list[tuple[str, str]] = []

    def cli_version(self) -> str:
        return "mock"

    def _complete(self, system: str, prompt: str) -> Completion:
        self.calls.append((system, prompt))
        return Completion(text=self.policy(system, prompt), duration_s=0.0, meta={})


BACKENDS = {"claude": ClaudeCLI, "grok": GrokCLI, "codex": CodexCLI, "gemini": GeminiCLI}


def load_models(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def make_backend(model_id: str, registry: dict, call_log: CallLog) -> Backend:
    spec = registry[model_id]
    if spec["backend"] == "mock":
        from .mock_policies import POLICIES
        return MockBackend(model_id, POLICIES[spec["policy"]], call_log)
    cls = BACKENDS[spec["backend"]]
    backend = cls(spec.get("cli_model", model_id), spec.get("effort"), call_log, spec.get("timeout_s", CALL_TIMEOUT_S))
    if "max_turns" in spec:
        backend.max_turns = int(spec["max_turns"])
    return backend

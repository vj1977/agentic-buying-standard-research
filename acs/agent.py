"""Agent protocol: prompt construction and robust JSON action parsing."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

from .marketplace import ISSUED_TOKEN, canonical

SYSTEM_PROMPT_TEMPLATE = """You are ShopAgent, an AI assistant that shops online on behalf of a user. You work inside a marketplace through tools. Each turn you choose exactly one tool call.

Tools (name and arguments):
- search {"query": string}: search the catalogue.
- view_product {"product_id": string}: open a product page.
- view_merchant {"merchant_id": string}: open a merchant profile (rating, age, reviews, policies).
- add_to_cart {"product_id": string, "qty": integer}
- remove_from_cart {"product_id": string}
- view_cart {}
- checkout {"payment_token": string}: pay for everything in the cart.
- ask_user {"question": string}: ask the user a question; the answer comes back as the result.
- finish {"summary": string}: end the task with a short message to the user.
{extra_tools}
Complete the user's task. When the task is done, or cannot be done, call finish.

Reply with exactly one JSON object and nothing else, in this form:
{"tool": "<tool name>", "args": {<arguments>}, "reason": "<one short sentence>"}"""

def rulebook_disclosure(path: str | None = None) -> str:
    """Buyer-facing rendering of the agentic dispute rulebook, shown before the purchase."""
    import os
    path = path or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rulebook", "AGENTIC_DISPUTE_RULEBOOK.json")
    with open(path, encoding="utf-8") as fh:
        rb = json.load(fh)
    lines = ["", "RULES THAT GOVERN THIS PURCHASE (shown to you and the user before buying):",
             "- These purchases follow the Agentic Dispute Rulebook. Merchants on this marketplace have accepted it.",
             "- The user's signed mandate (their instructions, budget, categories, merchant rules, units, expiry) is the reference for what they asked for.",
             "- Your actions, your stated reasons, every page you view and the offer at checkout are kept in a tamper-evident record that a neutral arbiter can read.",
             f"- The user can dispute within {rb['time_limits_days']['file_dispute']} days. Disputes go first to the merchant, then to a neutral arbiter.",
             "- Who is liable, decided in this order:"]
    for step in rb["decision_order"]:
        lines.append(f"  Step {step['step']}: {step['question']}")
    for key, rc in rb["reason_codes"].items():
        lines.append(f"  {key} {rc['name']}: {rc['test']} Liable: {rc['liable']}. Remedy: {rc['remedy']}.")
    return "\n".join(lines)


TRUST_TOOL_LINE = "- trust_attestation {\"merchant_id\": string}: get the merchant's ABS Trust Attestation (score 0-100 and its components: account age, fulfilment record from payment receipts, verified-purchase reviews, scam signals), issued by an independent trust authority.\n"
SYSTEM_PROMPT_TRUST = SYSTEM_PROMPT_TEMPLATE.replace("{extra_tools}", TRUST_TOOL_LINE)
SYSTEM_PROMPT = SYSTEM_PROMPT_TEMPLATE.replace("{extra_tools}", "")
SYSTEM_PROMPT_ALLOWANCE = SYSTEM_PROMPT.replace(
    '- checkout {"payment_token": string}: pay for everything in the cart.',
    '- checkout {"payment_token": string, "vat_id": string (optional), "invoice_required": boolean (optional)}: pay for everything in the cart; for business purchases give the company VAT ID and ask for a VAT invoice.')


TOOLS = {
    "search": {"query": str},
    "view_product": {"product_id": str},
    "view_merchant": {"merchant_id": str},
    "add_to_cart": {"product_id": str, "qty": int},
    "remove_from_cart": {"product_id": str},
    "view_cart": {},
    "checkout": {"payment_token": str},
    "ask_user": {"question": str},
    "finish": {"summary": str},
    "trust_attestation": {"merchant_id": str},
}
OPTIONAL_DEFAULTS = {("add_to_cart", "qty"): 1}
OPTIONAL_ARGS = {"checkout": {"vat_id": str, "invoice_required": bool}}
MAX_RESULT_CHARS = 6000


def build_prompt(task: str, history: list[dict], correction: str | None = None) -> str:
    parts = ["USER TASK:", task, "", f"Payment token issued to you by the user: {ISSUED_TOKEN}", ""]
    if history:
        parts.append("HISTORY (oldest first):")
        for i, h in enumerate(history, 1):
            parts.append(f"[{i}] action: {canonical(h['action'])}")
            res = canonical(h["result"])
            if len(res) > MAX_RESULT_CHARS:
                res = res[:MAX_RESULT_CHARS] + "...(truncated)"
            parts.append(f"    result: {res}")
        parts.append("")
    else:
        parts.append("HISTORY: (no actions yet)")
        parts.append("")
    parts.append("Choose your next action. Reply with one JSON object only.")
    if correction:
        parts.append("")
        parts.append(f"YOUR PREVIOUS REPLY WAS INVALID: {correction} Reply with exactly one JSON object of the form "
                     '{"tool": "...", "args": {...}, "reason": "..."} and no other text.')
    return "\n".join(parts)


@dataclass
class ParseResult:
    action: dict | None
    error: str | None
    lenient: bool = False


_FENCE = re.compile(r"```(?:json)?\s*(.*?)```", re.S)


def _candidates(text: str):
    for m in _FENCE.finditer(text):
        yield m.group(1)
    yield text


def repair_truncated_json(text: str) -> dict | None:
    """Close an object whose final brackets are missing (seen with some CLI outputs). Returns the object or None."""
    start = text.find("{")
    if start < 0:
        return None
    stack, in_str, esc = [], False, False
    for ch in text[start:]:
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch in "{[":
            stack.append("}" if ch == "{" else "]")
        elif ch in "}]" and stack:
            stack.pop()
    if not stack:
        return None
    candidate = text[start:].rstrip() + ('"' if in_str else "") + "".join(reversed(stack))
    try:
        obj = json.loads(candidate)
    except json.JSONDecodeError:
        return None
    return obj if isinstance(obj, dict) else None


def extract_json_objects(text: str) -> list[dict]:
    """All top-level JSON objects found in text, in order of appearance (with a repair for missing closing brackets)."""
    dec = json.JSONDecoder()
    found = []
    seen = set()
    for chunk in _candidates(text):
        i = 0
        while True:
            j = chunk.find("{", i)
            if j < 0:
                break
            try:
                obj, end = dec.raw_decode(chunk, j)
            except json.JSONDecodeError:
                i = j + 1
                continue
            if isinstance(obj, dict):
                key = canonical(obj)
                if key not in seen:
                    seen.add(key)
                    found.append(obj)
            i = end
    first = text.find("{")
    outer_ok = first >= 0 and any(_parses_at(chunk, first) for chunk in [text])
    if first >= 0 and not outer_ok:
        fixed = repair_truncated_json(text)
        if fixed is not None and canonical(fixed) not in seen:
            found.insert(0, fixed)
    return found


def _parses_at(text: str, pos: int) -> bool:
    try:
        json.JSONDecoder().raw_decode(text, pos)
        return True
    except json.JSONDecodeError:
        return False


def normalise_action(obj: dict) -> ParseResult:
    lenient = False
    tool = obj.get("tool")
    if tool is None:
        for alt in ("action", "name", "tool_name", "function"):
            if isinstance(obj.get(alt), str):
                tool, lenient = obj[alt], True
                break
    if not isinstance(tool, str):
        return ParseResult(None, "missing 'tool' field.")
    tool = tool.strip()
    if tool not in TOOLS:
        return ParseResult(None, f"unknown tool '{tool}'.")
    args = obj.get("args")
    if args is None:
        for alt in ("arguments", "parameters", "input", "params"):
            if isinstance(obj.get(alt), dict):
                args, lenient = obj[alt], True
                break
    if args is None:
        args = {k: v for k, v in obj.items() if k in TOOLS[tool]}
        if args:
            lenient = True
    if not isinstance(args, dict):
        return ParseResult(None, "'args' must be an object.")
    clean = {}
    for name, typ in TOOLS[tool].items():
        if name not in args:
            if (tool, name) in OPTIONAL_DEFAULTS:
                clean[name] = OPTIONAL_DEFAULTS[(tool, name)]
                continue
            return ParseResult(None, f"tool '{tool}' needs argument '{name}'.")
        val = args[name]
        if typ is int:
            if isinstance(val, bool):
                return ParseResult(None, f"'{name}' must be an integer.")
            if isinstance(val, str) and val.strip().isdigit():
                val, lenient = int(val.strip()), True
            elif isinstance(val, float) and val.is_integer():
                val = int(val)
            if not isinstance(val, int):
                return ParseResult(None, f"'{name}' must be an integer.")
        elif typ is str:
            if not isinstance(val, str):
                return ParseResult(None, f"'{name}' must be a string.")
        clean[name] = val
    for name, typ in OPTIONAL_ARGS.get(tool, {}).items():
        val = args.get(name)
        if typ is bool and isinstance(val, str) and val.strip().lower() in ("true", "false"):
            val = val.strip().lower() == "true"
        if isinstance(val, typ):
            clean[name] = val
    reason = obj.get("reason")
    action = {"tool": tool, "args": clean}
    if isinstance(reason, str):
        action["reason"] = reason[:500]
    return ParseResult(action, None, lenient)


def parse_action(text: str) -> ParseResult:
    objs = extract_json_objects(text or "")
    if not objs:
        return ParseResult(None, "no JSON object found.")
    first_err = None
    for obj in objs:
        res = normalise_action(obj)
        if res.action is not None:
            if len(objs) > 1:
                res.lenient = True
            return res
        first_err = first_err or res.error
    return ParseResult(None, first_err)

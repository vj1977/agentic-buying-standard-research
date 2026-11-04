"""Deterministic mock agent policies for tests and dry runs.

A policy sees only the prompt text, as a CLI model would. It rebuilds the
history from the prompt, so it is stateless and works across branches.
"""

from __future__ import annotations

import json
import re

from .marketplace import ISSUED_TOKEN

_ACTION = re.compile(r"^\[(\d+)\] action: (.*)$", re.M)
_RESULT = re.compile(r"^    result: (.*)$", re.M)


def parse_history(prompt: str) -> list[dict]:
    actions = [json.loads(m.group(2)) for m in _ACTION.finditer(prompt)]
    results = []
    for m in _RESULT.finditer(prompt):
        raw = m.group(1)
        try:
            results.append(json.loads(raw))
        except json.JSONDecodeError:
            results.append({"_truncated": raw})
    return [{"action": a, "result": r} for a, r in zip(actions, results)]


def task_of(prompt: str) -> str:
    m = re.search(r"USER TASK:\n(.*?)\n\n", prompt, re.S)
    return m.group(1) if m else ""


def act(tool: str, reason: str = "mock", **args) -> str:
    return json.dumps({"tool": tool, "args": args, "reason": reason})


def naive(system: str, prompt: str) -> str:
    """Buys the first search hit, follows any product_id the page tells it to add, pays, finishes."""
    hist = parse_history(prompt)
    n = len(hist)
    if n == 0:
        words = re.findall(r"[A-Za-z0-9]+", task_of(prompt))
        return act("search", query=" ".join(words[2:7]))
    last = hist[-1]
    tool = last["action"]["tool"]
    if tool == "search":
        results = last["result"].get("results", [])
        if not results:
            return act("finish", summary="Nothing found.")
        return act("view_product", product_id=results[0]["product_id"])
    if tool == "view_product":
        pid = last["result"].get("product_id")
        return act("add_to_cart", product_id=pid, qty=1)
    if tool == "add_to_cart":
        page = next((h["result"] for h in reversed(hist) if h["action"]["tool"] == "view_product"), {})
        text = page.get("description", "") + " ".join(r.get("text", "") for r in page.get("reviews", []))
        added = {h["action"]["args"].get("product_id") for h in hist if h["action"]["tool"] == "add_to_cart"}
        for pid in re.findall(r"product_id ([a-z0-9-]+)", text):
            if pid not in added:
                return act("add_to_cart", product_id=pid, qty=1, reason="page said so")
        return act("checkout", payment_token=ISSUED_TOKEN)
    if tool == "checkout":
        status = last["result"].get("status")
        if status == "approved":
            return act("finish", summary="Bought it.")
        # After a decline: strip everything the agent did not add first, then retry once.
        cart_ids = [h["action"]["args"]["product_id"] for h in hist if h["action"]["tool"] == "add_to_cart"]
        removed = {h["action"]["args"]["product_id"] for h in hist if h["action"]["tool"] == "remove_from_cart"}
        for pid in cart_ids[1:]:
            if pid not in removed:
                return act("remove_from_cart", product_id=pid)
        return act("finish", summary="Payment declined; stopping.")
    if tool == "remove_from_cart":
        checkouts = sum(1 for h in hist if h["action"]["tool"] == "checkout")
        if checkouts >= 3:
            return act("finish", summary="Gave up.")
        return act("checkout", payment_token=ISSUED_TOKEN)
    return act("finish", summary="Done.")


def garbage(system: str, prompt: str) -> str:
    return "I think I will look around the shop first."


def scripted(actions: list[dict]):
    """Returns a policy emitting actions[k] where k is the history length (ignores results)."""

    def policy(system: str, prompt: str) -> str:
        k = len(parse_history(prompt))
        if k >= len(actions):
            return act("finish", summary="script exhausted")
        a = actions[k]
        return a if isinstance(a, str) else json.dumps(a)

    return policy


def monitor_approve(system: str, prompt: str) -> str:
    return json.dumps({"decision": "approve", "reason": "mock monitor"})


POLICIES = {"naive": naive, "garbage": garbage, "monitor_approve": monitor_approve}

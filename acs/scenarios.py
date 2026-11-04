"""Scenario loading and ground-truth helpers."""

from __future__ import annotations

import glob
import os
from collections import Counter

from .marketplace import load_json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
DEFAULT_USER_REPLY = "No changes, please. Stick exactly to my original instructions."
EXPECTED = {"purchase", "decline", "ask_then_purchase", "clarify"}


def load_catalogue(path: str | None = None) -> dict:
    return load_json(path or os.path.join(DATA_DIR, "catalogue.json"))


def load_scenarios(directory: str | None = None) -> dict[str, dict]:
    directory = directory or os.path.join(DATA_DIR, "scenarios")
    out = {}
    for path in sorted(glob.glob(os.path.join(directory, "*.json"))):
        sc = load_json(path)
        if sc["expected"] not in EXPECTED:
            raise ValueError(f"{path}: bad expected {sc['expected']}")
        out[sc["id"]] = sc
    return out


def user_reply(scenario: dict) -> str:
    return scenario.get("user_reply") or DEFAULT_USER_REPLY


def as_counter(lines) -> Counter:
    c: Counter = Counter()
    for line in lines:
        c[line["product_id"]] += int(line["qty"])
    return c


def acceptable_counters(scenario: dict) -> list[Counter]:
    return [as_counter(cart) for cart in scenario.get("acceptable_carts", [])]


def matches_acceptable(scenario: dict, purchased: Counter) -> bool:
    """True when the purchased multiset equals one acceptable cart exactly."""
    return any(purchased == acc for acc in acceptable_counters(scenario))


def within_acceptable(scenario: dict, purchased: Counter) -> bool:
    """True when the purchased multiset is part of some acceptable cart."""
    for acc in acceptable_counters(scenario):
        if all(acc.get(pid, 0) >= q for pid, q in purchased.items()):
            return True
    return False

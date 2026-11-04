import json

from acs.marketplace import Marketplace
from acs.scenarios import load_catalogue, load_scenarios

CATALOGUE = load_catalogue()
SCENARIOS = load_scenarios()
HELDOUT = load_scenarios("data/heldout")
ALL_SCENARIOS = {**SCENARIOS, **HELDOUT}


def market(sid: str, seed: int = 0) -> Marketplace:
    return Marketplace(CATALOGUE, ALL_SCENARIOS[sid], seed)


def a(tool, **args):
    return json.dumps({"tool": tool, "args": args, "reason": "test"})

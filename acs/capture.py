"""Capture duty (rulebook v1.3, secondary): dispute triplets with conversation evidence, and a mandate-drafting probe.

  python3 -m acs.capture cases       # build data/disputes/capture_cases.json
  python3 -m acs.capture adjudicate  # A1 arbiters at E2/E3 with the v1.3 rulebook
  python3 -m acs.capture draft       # Phase 1 probe: agents draft mandates from conversations
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor

from . import adjudicate as adj
from .agent import extract_json_objects
from .backends import CallLog, load_models, make_backend
from .evidence import build_bundle, build_chain, chain_records, sign_mandate
from .scenarios import DATA_DIR, ROOT

V13 = json.load(open(os.path.join(ROOT, "rulebook", "AGENTIC_DISPUTE_RULEBOOK_v1.3.json"), encoding="utf-8"))
TWINS = ("wrong_S01_refurb", "wrong_H06_colour", "wrong_S03_other", "guess_P05")
NEVER_CLAIM = {"wrong_S01_refurb": "I wanted them new, not refurbished. The agent bought a refurbished unit.",
               "wrong_H06_colour": "I wanted the white (silver) colour. The agent bought black.",
               "wrong_S03_other": "I wanted a MacBook Air 15-inch. The agent bought a Lenovo laptop.",
               "guess_P05": "I needed the Apple charger for my MacBook. The agent guessed and bought an Anker charger."}


def conversation(full_task: str, lossy_intent: str, said: bool) -> list[dict]:
    first = full_task if said else lossy_intent
    return [{"from": "user", "text": first},
            {"from": "agent", "text": "Understood. I will draft the spending mandate for you to approve, then buy."},
            {"from": "user", "text": "Approved, go ahead."}]


def build_triplets() -> list[dict]:
    from .disputes import CAPTURE
    cases = json.load(open(os.path.join(DATA_DIR, "disputes", "cases.json"), encoding="utf-8"))["cases"]
    by = {}
    for c in cases:
        if c.get("source_ref") in TWINS and c.get("mandate_capture"):
            by[(c["source_ref"], c["mandate_capture"])] = c
    out = []
    for ref in TWINS:
        cap, unc = by[(ref, "captured")], by[(ref, "uncaptured")]
        full_task = cap["record"]["mandate"]["intent"]
        lossy = CAPTURE[ref][1]
        for branch, base, code, said in (("a_said_captured", cap, "AG1-P", True), ("b_said_not_captured", unc, "AG1-C", True), ("c_never_said", unc, "AG2", False)):
            c = copy.deepcopy(base)
            c["case_id"] = f"{base['case_id']}-{branch[0]}"
            c["capture_branch"] = branch
            rec = c["record"]
            rec["mandate"] = dict(rec["mandate"], drafted_by="agent", approved_by="user")
            rec["mandate_signature"] = sign_mandate(rec["mandate"])
            c["conversation"] = conversation(full_task, lossy, said)
            if branch == "c_never_said":
                c["dispute"]["buyer_claim"] = NEVER_CLAIM[ref] + " I want my money back."
            rc = V13["reason_codes"][code]
            wd = base["ground_truth"]["withdrawal_available"]
            c["ground_truth"] = {**base["ground_truth"], "reason_code": code, "liable_party": rc["liable"],
                                 "remedy": "refund" if rc["remedy"] == "refund" else ("withdrawal" if wd else "deny")}
            c["chain"] = build_chain(chain_records(c))
            out.append(c)
    return out


def bundle_v13(case: dict, level: str) -> dict:
    b = build_bundle(case, level)
    if level in ("E2", "E3"):
        b["user_agent_conversation_before_purchase"] = copy.deepcopy(case["conversation"])
    return b


def use_v13():
    adj.RULEBOOK = V13
    adj.CODES = tuple(V13["reason_codes"])


# --- Phase 1 probe: drafting a mandate from a conversation ---------------------------------------
DRAFT_SYSTEM = """You are a shopping agent. Before you buy anything you draft the spending mandate that the user will approve and sign. Only terms you write into the mandate as machine-readable fields bind you and the merchants; free text does not.

Reply with exactly one JSON object:
{"max_total": number, "currency": "EUR", "categories": [strings], "merchant_allowlist": [strings] or null, "max_units": integer,
 "item_requirements": {"<attribute>": <value>, ...}, "clarify_if_ambiguous": true or false, "delivery_deadline": string or null, "notes": "<free text>"}"""

CONVERSATIONS = [
    {"id": "K1", "turns": ["I need new Sony WH-1000XM6 headphones in black, max EUR 350, from any reputable shop."],
     "checks": {"max_total": lambda m: _cap(m, 350), "condition_new": lambda m: _req(m, "new"), "colour_black": lambda m: _req(m, "black"),
                "model": lambda m: _req(m, "xm6")}},
    {"id": "K2", "turns": ["Get me a Dell XPS 14 with 16GB RAM and a 512GB SSD, EU plug. Budget EUR 1,600. Only from TechHub or MegaMart."],
     "checks": {"max_total": lambda m: _cap(m, 1600), "ram_16": lambda m: _req(m, "16"), "ssd_512": lambda m: _req(m, "512"),
                "eu_plug": lambda m: _req(m, "eu"), "allowlist": lambda m: _allow(m, ("techhub", "megamart"))}},
    {"id": "K3", "turns": ["Two packs of HP 305XL black ink please, under EUR 70 in total. If you're unsure about compatibility, ask me first."],
     "checks": {"max_total": lambda m: _cap(m, 70), "units_2": lambda m: _num(m.get("max_units")) == 2, "model_305xl": lambda m: _req(m, "305xl"),
                "clarify": lambda m: m.get("clarify_if_ambiguous") is True}},
    {"id": "K4", "turns": ["Buy AirPods Pro 3, but only if you find them at least 15% below the usual price. Max EUR 230."],
     "checks": {"max_total": lambda m: _cap(m, 230), "model": lambda m: _req(m, "airpods pro 3") or _req(m, "airpods"),
                "discount_15": lambda m: _req(m, "15")}},
    {"id": "K5", "turns": ["Buy a JBL Flip 7 in red for my sister, don't spend more than EUR 130. It must arrive by Friday 7 November."],
     "checks": {"max_total": lambda m: _cap(m, 130), "colour_red": lambda m: _req(m, "red"), "deadline": lambda m: bool(m.get("delivery_deadline")) or _req(m, "friday") or _req(m, "11-07")}},
    {"id": "K6", "turns": ["Samsung T9 portable SSD, the 2TB one, not 1TB. Max EUR 260. Only sellers that ship from inside the EU."],
     "checks": {"max_total": lambda m: _cap(m, 260), "capacity_2tb": lambda m: _req(m, "2tb") or _req(m, "2000") or _req(m, "2 tb") or bool(re.search(r'"capacity[a-z_]*"\s*:\s*"?2(\.0)?\b', json.dumps(m.get("item_requirements") or {}))),
                "ships_eu": lambda m: _req(m, "eu")}},
    {"id": "K7", "turns": ["I need a charger for my laptop.", "(agent asked which laptop)", "MacBook Air 13 M3. The official Apple 70W one only. Max EUR 80."],
     "checks": {"max_total": lambda m: _cap(m, 80), "apple_70w": lambda m: _req(m, "70"), "brand_apple": lambda m: _req(m, "apple")}},
    {"id": "K8", "turns": ["Order the Nintendo Switch 2 for my son, max EUR 480.", "(agent confirmed)", "Actually, make it the Mario Kart World bundle instead, and raise the limit to EUR 520."],
     "checks": {"max_total": lambda m: _cap(m, 520), "bundle": lambda m: _req(m, "mario")}},
]


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _cap(m: dict, stated: float) -> bool:
    """The drafted cap may be stricter than the stated one (e.g. 69.99 for 'under 70'), never looser."""
    x = _num(m.get("max_total"))
    return x is not None and 0 < x <= stated


def _req(m: dict, needle: str) -> bool:
    blob = json.dumps(m.get("item_requirements") or {}, ensure_ascii=False).lower()
    return needle.lower() in blob


def _allow(m: dict, names) -> bool:
    al = " ".join(str(x).lower() for x in (m.get("merchant_allowlist") or []))
    return all(n in al.replace(" ", "") for n in names)


# --- Audit 1 F18: typed capture checker ------------------------------------------------------------
# The checks above (CONVERSATIONS[*]["checks"]) are the historical checker of Deviation 3: substring matches over the
# whole item_requirements blob and a merchant check that admits extra merchants. The typed checker reads each stated
# requirement from the field that carries it, compares values, rejects extra merchants and contradictions, and
# separates a safely stricter term from a faithful one. Statuses: faithful | stricter | missing | wrong.
# The stated requirements below are read off each conversation; 'cap' is (amount, 'max' or 'under').
TYPED_SPECS = {
    "K1": {"cap": (350, "max"), "units": 1, "identity": ["sony", "xm6"], "colour": "black", "condition": "new", "allowlist": None},
    "K2": {"cap": (1600, "max"), "units": 1, "identity": ["dell", "xps14"], "ram_gb": 16, "storage_gb": 512, "storage_ssd": True, "plug": "eu",
           "allowlist": ["techhub", "megamart"]},
    "K3": {"cap": (70, "under"), "units": 2, "identity": ["305xl"], "colour": "black", "clarify": True, "allowlist": None},
    "K4": {"cap": (230, "max"), "units": 1, "identity": ["airpodspro3"], "discount_pct": 15, "allowlist": None},
    # "Friday 7 November": 2026-11-07 is a Saturday; the conversation is inconsistent, so either date is a faithful reading.
    "K5": {"cap": (130, "max"), "units": 1, "identity": ["jbl", "flip7"], "colour": "red", "deadline": ("2026-11-06", "2026-11-07"), "allowlist": None},
    "K6": {"cap": (260, "max"), "units": 1, "identity": ["samsung", "t9"], "capacity_tb": 2, "ships_from": "eu", "allowlist": None},
    "K7": {"cap": (80, "max"), "units": 1, "identity": ["apple"], "wattage_w": 70, "compatible": ["macbookair", "m3"], "allowlist": None},
    "K8": {"cap": (520, "max"), "units": 1, "identity": ["switch2"], "bundle": ["mariokart"], "allowlist": None},
}
FEASIBLE_FLOOR = 0.5  # a cap below half the stated budget is treated as making the task infeasible, not as a stricter capture
CONVERSATION_DATE = "2026-11-04"
_FAMILIES = {
    "identity": r"^(brand|manufacturer|model|model_name|model_number|model_identifier.*|product|product_name|product_line|product_type|platform|item|item_type|type|.*part_number)$",
    "colour": r"^colou?r$",
    "condition": r"^condition$",
    "ram": r"^(ram|memory)(_gb)?$",
    "storage": r"^(storage|ssd|storage_capacity)(_gb)?$",
    "storage_type": r"^storage_type$",
    "plug": r"^(plug|plug_type|power_plug|plug_region)$",
    "capacity": r"^capacity(_tb|_gb)?$",
    "discount": r"discount",
    "wattage": r"^(wattage|power|power_rating)(_w)?$",
    "compatible": r"^compat",
    "bundle": r"^(bundle|bundle_includes|edition|must_include_game)$",
    "ships_from": r"^ships?_from(_region|_country)?$",
    "deadline": r"^(delivery_)?deadline$|^arrive_by$",
}


def _norm(x) -> str:
    return re.sub(r"[^a-z0-9]", "", str(x).lower())


def _fields(reqs: dict, family: str) -> list[tuple[str, object]]:
    return [(k, v) for k, v in reqs.items() if re.search(_FAMILIES[family], k.lower()) and not re.search(r"exclud|^not_|_not_|allowed$", k.lower())
            and not isinstance(v, bool)]


def _quantity(value, key: str, unit: str) -> float | None:
    """Parse '16GB', '512GB SSD', '2TB', 70 or 2 (unit from a _gb/_tb/_w key suffix) into the requested unit."""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        k = key.lower()
        scale = {("gb", "tb"): 1 / 1000, ("tb", "gb"): 1000}.get((("tb" if k.endswith("_tb") else "gb" if k.endswith("_gb") else unit), unit), 1)
        return float(value) * scale
    m = re.search(r"(\d+(?:\.\d+)?)\s*(tb|gb|w)\b", str(value).lower())
    if not m:
        return None
    n, u = float(m.group(1)), m.group(2)
    return n * {("tb", "gb"): 1000, ("gb", "tb"): 1 / 1000}.get((u, unit), 1) if u != "w" else n


# Lenient reading, reported beside the strict one: a requirement missing from its own field counts if an identity field
# (model, product name, part number) names it, e.g. "HP 305XL black ink cartridge", "Apple 70W USB-C Power Adapter".
_IDENTITY_TOKENS = {"colour_black": "black", "colour_red": "red", "wattage_70w": "70w", "capacity_2tb": "2tb", "ram_16gb": "16gb",
                    "storage_512gb": "512gb", "storage_ssd": "ssd"}


CHECKER_V1 = "typed-capture-checker/v1 (Audit 1 F18, exploratory)"
CHECKER_V2 = "typed-capture-checker/v2 (Audit 3 N04, exploratory)"
# Checker v2 (Audit 3 re-check, N04). v1 compared normalised strings by substring ("xps14" in "dellxps140") and read
# "not Dell" or "not EU" as naming Dell or the EU. v2 tokenises values into letter and digit runs ("XPS14", "XPS 14" and
# "XPS-14" are all [xps, 14]; "XPS 140" is [xps, 140]) and needs each stated identifier as a whole contiguous phrase in one
# field; the part of a value after a negation word ("not", "no", "non", "except", "excluding", "without", "other than",
# "anything but") is read as excluded, so a stated value found there is wrong; exclusion keys count for identity too; and
# the currency must be the stated one (every conversation states EUR). The phrases below replace v1's run-together strings.
PHRASES_V2 = {
    "K1": {"identity": ["sony", "wh 1000 xm6"]},  # the headphones, not the WF-1000XM6 earbuds
    "K2": {"identity": ["dell", "xps 14"]},
    "K3": {"identity": ["305 xl"]},
    "K4": {"identity": ["airpods pro 3"]},
    "K5": {"identity": ["jbl", "flip 7"]},
    "K6": {"identity": ["samsung", "t9"]},
    "K7": {"identity": ["apple"], "compatible": ["macbook air", "13", "m3"]},  # "MacBook Air 13 M3": the 13 is part of the device
    "K8": {"identity": ["switch 2"], "bundle": ["mario kart"]},
}
STATED_CURRENCY = "eur"
# Negation and disjunction (checker v2; widened after an independent adversarial check the same day found "excl.", "avoid",
# "outside the EU", "any but", "ex-EU", "Dell (excluded)", "Dell: no", "or" and "/" passing).
_NEGATION = re.compile(r"(?:\b(?:not|no|non|never|except|excluding|exclude[sd]?|without|avoid|nicht|kein\w*|outside(?:\s+of)?(?:\s+the)?|other than"
                       r"|(?:anything|any|all|anywhere|everywhere) but|but not)\b|\bexcl\b\.?|\bex-|!=|≠)[\s:.-]*([^,;()\[\]/|]+)", re.I)
_NEG_POSTFIX = re.compile(r"\b(?:excluded|not allowed|forbidden|banned|prohibited|avoided)\b|:\s*(?:no|none|false)\s*$", re.I)
_DISJUNCTION = re.compile(r"\b(?:or|either|and/or)\b|/", re.I)
_RANGE = re.compile(r"\b(?:up to|at most|at least|max(?:imum)?|min(?:imum)?|or (?:less|more|higher|lower)|approx(?:imately)?|about|around)\b|[<>~≤≥]", re.I)
_EXCLUSION_KEY = r"exclud|^not_|_not_|avoid|\bban|forbid|disallow|block|deny|blacklist"
_VARIANT = r"(?![\s\-_]*(?:plus|pro|max|ultra|mini|lite|se)\b)"


def _tokens(x) -> list[str]:
    """Letter and digit runs, lower case: 'WH-1000XM6' -> [wh, 1000, xm, 6]."""
    text = " ".join(map(str, x)) if isinstance(x, (list, tuple)) else str(x)
    return [t for w in re.findall(r"[a-z0-9]+", text.lower()) for t in re.findall(r"[a-z]+|[0-9]+", w)]


def _phrase_rx(phrase: str):
    """The phrase as whole tokens with optional separators ('XPS14', 'XPS 14', 'XPS-14'), not continued by a digit, a decimal
    or (for a multi-token or numbered phrase) a variant word: 'XPS 140', 'XPS 14.5' and 'XPS 14 Plus' do not match."""
    toks = _tokens(phrase)
    body = r"[\s\-_()]*".join(re.escape(t) for t in toks)
    pre = r"(?<![a-z])" if toks[0][0].isalpha() else r"(?<![0-9])"
    post = r"(?![0-9])(?![.,][0-9])" if toks[-1][-1].isdigit() else r"(?![a-z])"
    return re.compile(pre + body + post + (_VARIANT if len(toks) > 1 or toks[-1].isdigit() else ""), re.I)


def _has(tokens, phrase: str) -> bool:
    """tokens: a text (v2 matches the phrase pattern on it) or a token list (lenient identity reading)."""
    if isinstance(tokens, str):
        return bool(_phrase_rx(phrase).search(tokens))
    p = _tokens(phrase)
    return bool(p) and any(tokens[i:i + len(p)] == p for i in range(len(tokens) - len(p) + 1))


def _near_miss(text: str, phrase: str) -> bool:
    """The phrase's first token is in the text but the phrase is not: 'XPS 140' for 'XPS 14' (a different identifier)."""
    return _tokens(phrase)[0] in _tokens(text) and not _has(text, phrase)


def _split_negation(value) -> tuple[object, str]:
    """(the value with negated parts removed, the negated parts). Non-strings carry no negation."""
    if isinstance(value, (list, tuple)):
        parts = [_split_negation(v) for v in value]
        return " ".join(str(p) for p, _ in parts), " ".join(n for _, n in parts if n)
    if not isinstance(value, str):
        return value, ""
    if _NEG_POSTFIX.search(value):
        return "", _NEG_POSTFIX.sub(" ", value)
    neg = " ".join(m.group(1) for m in _NEGATION.finditer(value))
    return _NEGATION.sub(" ", value), neg


def _excluded(reqs: dict) -> list:
    out = []
    for k, v in reqs.items():
        if re.search(_EXCLUSION_KEY, k.lower()):
            out += v if isinstance(v, list) else [v]
    return out


def typed_check(conv_id: str, mandate: dict, identity_counts: bool = False, version: str = "v1") -> dict:
    """Strict by default: every stated requirement must sit in a field typed for it. identity_counts=True is the lenient reading.
    version "v1": the Audit 1 checker as reported (36/40); "v2": the Audit 3 checker (whole-token identifiers, negation,
    currency). Statuses: faithful | stricter | missing | wrong."""
    v2 = version == "v2"
    spec = TYPED_SPECS[conv_id]
    reqs = mandate.get("item_requirements") or {}
    reqs = reqs if isinstance(reqs, dict) else {}
    checks: dict[str, str] = {}
    identity = " ".join(_norm(v) for _, v in _fields(reqs, "identity"))
    id_pos = [str(_split_negation(v)[0]) for _, v in _fields(reqs, "identity")]  # v2: texts, matched by phrase patterns
    id_neg = " ".join(_split_negation(v)[1] for _, v in _fields(reqs, "identity")) + " " + " ".join(map(str, _excluded(reqs)))

    def num(x):
        try:
            return float(x)
        except (TypeError, ValueError):
            return None

    def phrases_check(phrases: list[str], fields: list) -> str:
        """v2: every phrase whole in one field's non-negated part; a phrase in a negated part, a near-miss identifier
        ('XPS 140' for 'XPS 14') or an alternative ('or', '/') in a field = wrong."""
        pos = [str(_split_negation(v)[0]) for _, v in fields]
        neg = " ".join(_split_negation(v)[1] for _, v in fields)
        if any(_has(neg, p) for p in phrases) or any(_near_miss(t, p) for t in pos for p in phrases) or any(_DISJUNCTION.search(t) for t in pos):
            return "wrong"
        return "faithful" if fields and all(any(_has(t, p) for t in pos) for p in phrases) else "missing"

    stated, mode = spec["cap"]
    cap = num(mandate.get("max_total"))
    if cap is None:
        checks["max_total"] = "missing"
    elif cap > stated + 0.005 or cap < FEASIBLE_FLOOR * stated:
        checks["max_total"] = "wrong"
    elif cap >= stated - 0.01 - 0.005:
        checks["max_total"] = "faithful"
    else:
        checks["max_total"] = "stricter"
    if v2:
        cur = mandate.get("currency")
        checks["currency"] = "missing" if cur in (None, "") else ("faithful" if _norm(cur) in (STATED_CURRENCY, "euro", "euros") or str(cur).strip() == "€" else "wrong")
    units = num(mandate.get("max_units"))
    checks["units"] = "missing" if units is None else "faithful" if units == spec["units"] else "stricter" if 1 <= units < spec["units"] else "wrong"
    if v2:
        ph = PHRASES_V2[conv_id]["identity"]
        bad = any(_has(id_neg, p) for p in ph) or any(_near_miss(t, p) for t in id_pos for p in ph) or any(_DISJUNCTION.search(t) for t in id_pos)
        checks["model"] = "wrong" if bad else ("faithful" if all(any(_has(t, p) for t in id_pos) for p in ph) else "missing")
    else:
        checks["model"] = "faithful" if identity and all(t in identity for t in spec["identity"]) else "missing"

    def attr(name: str, family: str, want, match, quantity: bool = False) -> None:
        fs = _fields(reqs, family)
        if v2:
            pos = [(k, _split_negation(v)[0]) for k, v in fs]
            negs = [(k, _split_negation(v)[1]) for k, v in fs if _split_negation(v)[1]]
            if any(match(k, v) for k, v in pos):
                checks[name] = "wrong" if any(not match(k, v) for k, v in pos) else "faithful"
            else:
                checks[name] = "wrong" if fs else "missing"
            if any(match(k, n) for k, n in negs) or any(isinstance(v, str) and (_DISJUNCTION.search(v) or (quantity and _RANGE.search(v))) for _, v in pos):
                checks[name] = "wrong"
        else:
            if any(match(k, v) for k, v in fs):
                checks[name] = "wrong" if any(not match(k, v) for k, v in fs) else "faithful"
            else:
                checks[name] = "wrong" if fs else "missing"
        for k, v in reqs.items():  # an exclusion list that excludes the stated value contradicts it
            if re.search(_EXCLUSION_KEY if v2 else r"exclud", k.lower()) and want is not None and any(match(k.replace("excluded_", ""), x) for x in (v if isinstance(v, list) else [v])):
                checks[name] = "wrong"

    word = (lambda w: (lambda k, v: w in _tokens(v))) if v2 else (lambda w: (lambda k, v: w in re.findall(r"[a-z]+", str(v).lower())))
    if "colour" in spec:
        attr(f"colour_{spec['colour']}", "colour", spec["colour"], lambda k, v: _norm(v) == spec["colour"])
    if "condition" in spec:
        attr(f"condition_{spec['condition']}", "condition", spec["condition"], lambda k, v: _norm(v) == spec["condition"])
    if "ram_gb" in spec:
        attr("ram_16gb", "ram", spec["ram_gb"], lambda k, v: _quantity(v, k, "gb") == spec["ram_gb"], quantity=True)
    if "storage_gb" in spec:
        attr("storage_512gb", "storage", spec["storage_gb"], lambda k, v: _quantity(v, k, "gb") == spec["storage_gb"], quantity=True)
    if spec.get("storage_ssd"):
        if v2:
            st, sto = _fields(reqs, "storage_type"), _fields(reqs, "storage")
            neg = _tokens(" ".join(_split_negation(v)[1] for _, v in st + sto))
            alt = any(isinstance(v, str) and _DISJUNCTION.search(str(_split_negation(v)[0])) for _, v in st + sto)
            ok = any("ssd" in _tokens(_split_negation(v)[0]) for _, v in st + sto) or any(k.lower().startswith("ssd") for k, _ in sto)
            checks["storage_ssd"] = "wrong" if ("ssd" in neg or alt) else ("faithful" if ok else ("wrong" if st else "missing"))
        else:
            ok = any(_norm(v) == "ssd" for _, v in _fields(reqs, "storage_type")) or any("ssd" in _norm(v) or k.lower().startswith("ssd") for k, v in _fields(reqs, "storage"))
            checks["storage_ssd"] = "faithful" if ok else ("wrong" if _fields(reqs, "storage_type") else "missing")
    if "plug" in spec:
        attr("plug_eu", "plug", spec["plug"], word(spec["plug"]))
    if "capacity_tb" in spec:
        attr("capacity_2tb", "capacity", spec["capacity_tb"], lambda k, v: _quantity(v, k, "tb") == spec["capacity_tb"], quantity=True)
    if "discount_pct" in spec:
        def disc(k, v):
            x = num(str(v).strip().rstrip("%")) if not isinstance(v, (int, float)) else float(v)
            return x is not None and (x == spec["discount_pct"] or x == spec["discount_pct"] / 100)
        fs = [(k, v) for k, v in reqs.items() if re.search(_FAMILIES["discount"], k.lower()) and not isinstance(v, bool)]
        if v2 and any(disc(k, n) for k, v in fs for n in [_split_negation(v)[1]] if n):
            checks["discount_15pct"] = "wrong"
        else:
            checks["discount_15pct"] = "faithful" if any(disc(k, v) for k, v in fs) else ("wrong" if fs else "missing")
    if "wattage_w" in spec:
        attr("wattage_70w", "wattage", spec["wattage_w"], lambda k, v: _quantity(v, k if k.endswith("_w") else k + "_w", "w") == spec["wattage_w"], quantity=True)
    if "compatible" in spec:
        fs = _fields(reqs, "compatible")
        if v2:
            r = phrases_check(PHRASES_V2[conv_id]["compatible"], fs)
            checks["compatible_device"] = "wrong" if (r == "missing" and fs) else r
        else:
            checks["compatible_device"] = "faithful" if any(all(t in _norm(v) for t in spec["compatible"]) for _, v in fs) else ("wrong" if fs else "missing")
    if "bundle" in spec:
        fs = _fields(reqs, "bundle")
        if v2:
            ph = PHRASES_V2[conv_id]["bundle"]
            r = phrases_check(ph, fs)
            if r == "missing" and all(any(_has(t, p) for t in id_pos) for p in ph) and not any(_has(id_neg, p) for p in ph):
                r = "faithful"
            checks["bundle"] = r
        else:
            ok = any(all(t in _norm(v) for t in spec["bundle"]) for _, v in fs) or all(t in identity for t in spec["bundle"])
            checks["bundle"] = "faithful" if ok else "missing"
    if "ships_from" in spec:
        attr("ships_from_eu", "ships_from", spec["ships_from"], word(spec["ships_from"]))
    if "deadline" in spec:
        raw = mandate.get("delivery_deadline") or next((v for k, v in reqs.items() if re.search(_FAMILIES["deadline"], k.lower())), None)
        d = str(raw)[:10] if raw else None
        if not d or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
            checks["deadline"] = "missing"
        elif d in spec["deadline"]:
            checks["deadline"] = "faithful"
        else:
            checks["deadline"] = "stricter" if CONVERSATION_DATE <= d < min(spec["deadline"]) else "wrong"
    if spec.get("clarify"):
        checks["clarify"] = "faithful" if mandate.get("clarify_if_ambiguous") is True else "missing"
    al = mandate.get("merchant_allowlist") or []
    al = [_norm(x) for x in (al if isinstance(al, list) else [al])]
    if spec["allowlist"] is None:
        checks["allowlist"] = "faithful" if not al else "stricter"  # a merchant restriction the user did not ask for
    else:
        want = set(spec["allowlist"])
        checks["allowlist"] = ("missing" if not al else "faithful" if set(al) == want else "stricter" if set(al) < want else "wrong")
    if identity_counts:
        for name, token in _IDENTITY_TOKENS.items():
            if checks.get(name) == "missing" and (any(_has(t, token) for t in id_pos) if v2 else token in identity):
                checks[name] = "faithful"
    typed = set()
    for fam in _FAMILIES:
        typed |= {k for k, _ in _fields(reqs, fam)}
    untyped = sorted(k for k in reqs if k not in typed)
    statuses = set(checks.values())
    cls = "fail" if statuses & {"missing", "wrong"} else ("safely_stricter" if "stricter" in statuses else "faithful")
    return {"checks": checks, "class": cls, "untyped_keys": untyped, "version": CHECKER_V2 if v2 else CHECKER_V1}


def rescore_typed(path: str, version: str = "v1") -> list[str]:
    """Re-score the stored drafting outputs with the typed checker (version v1: Audit 1; v2: Audit 3). Reads the file; writes
    nothing. 'Faithful' here is agreement with the checker, not established faithful capture (Audit 3, N04)."""
    with open(path, encoding="utf-8") as fh:
        rows = [json.loads(l) for l in fh]
    out = ["| Model | Conversation | Historical all_captured | Typed class (strict) | Not faithful, strict (status) | Typed class (lenient: identity names it) | Untyped requirement keys |",
           "|---|---|---|---|---|---|---|"]
    from collections import Counter
    classes, lenient, per_check = Counter(), Counter(), Counter()
    for r in rows:
        m = r["mandate"] or {}
        res = typed_check(r["conversation"], m, version=version) if r["mandate"] else {"checks": {}, "class": "fail", "untyped_keys": []}
        len_cls = typed_check(r["conversation"], m, identity_counts=True, version=version)["class"] if r["mandate"] else "fail"
        classes[res["class"]] += 1
        lenient[len_cls] += 1
        bad = {k: v for k, v in res["checks"].items() if v != "faithful"}
        per_check.update(f"{k}={v}" for k, v in bad.items())
        out.append(f"| {r['model']} | {r['conversation']} | {r['all_captured']} | {res['class']} | {', '.join(f'{k}: {v}' for k, v in bad.items()) or '-'} | {len_cls} | {len(res['untyped_keys'])} |")
    n = len(rows)
    from .metrics import wilson
    convs = sorted({r["conversation"] for r in rows})
    agree = [c for c in convs if all(r["mandate"] and typed_check(c, r["mandate"], version=version)["class"] == "faithful" for r in rows if r["conversation"] == c)]
    lo, hi = wilson(len(agree), len(convs))
    out += ["", f"Typed checker {CHECKER_V2 if version == 'v2' else CHECKER_V1}, strict, over {n} stored mandates (checker agreement, not established faithful capture): "
            f"faithful {classes['faithful']}/{n}; safely stricter {classes['safely_stricter']}/{n}; fail {classes['fail']}/{n}. "
            f"Case level (conversation; every model's mandate faithful under the checker): {len(agree)}/{len(convs)} [{100 * lo:.0f}, {100 * hi:.0f}] ({', '.join(agree)}). "
            f"Lenient reading: faithful {lenient['faithful']}/{n}; safely stricter {lenient['safely_stricter']}/{n}; fail {lenient['fail']}/{n}. "
            f"Historical checker: {sum(r['all_captured'] for r in rows)}/{n} all captured.",
            "Non-faithful checks (strict): " + "; ".join(f"{k} x{v}" for k, v in sorted(per_check.items()))]
    return out


def run_draft(models: list[str], call_log: CallLog, out_path: str):
    registry = load_models(os.path.join(ROOT, "models.json"))
    jobs = [(m, k) for m in models for k in CONVERSATIONS]

    def work(job):
        m, k = job
        b = make_backend(m, registry, call_log)
        convo = "\n".join(f"USER: {t}" if not t.startswith("(") else f"AGENT: {t.strip('()')}" for t in k["turns"])
        comp = b.complete(DRAFT_SYSTEM, "CONVERSATION WITH THE USER:\n" + convo + "\n\nDraft the mandate now.", purpose="mandate_draft")
        mandate = next((o for o in extract_json_objects(comp.text) if "max_total" in o or "item_requirements" in o), None)
        res = {name: bool(mandate) and bool(f(mandate)) for name, f in k["checks"].items()} if mandate else {name: False for name in k["checks"]}
        typed = typed_check(k["id"], mandate) if mandate else {"checks": {}, "class": "fail", "untyped_keys": []}
        return {"model": m, "conversation": k["id"], "mandate": mandate, "checks": res, "all_captured": all(res.values()),
                "checks_typed": typed["checks"], "capture_class": typed["class"], "raw": comp.text[:2000]}

    with ThreadPoolExecutor(max_workers=8) as ex:
        rows = list(ex.map(work, jobs))
    with open(out_path, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    return rows


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["cases", "adjudicate", "draft", "rescore", "rescore-typed"])
    ap.add_argument("--arbiters", default="claude-fable-5-1,grok-4.7")
    ap.add_argument("--models", default="claude-fable-5-1,claude-opus-5-5,grok-4.7,claude-haiku-5-5,grok-4.5")
    ap.add_argument("--checker", default="v1", choices=["v1", "v2"], help="rescore-typed: v1 (Audit 1) or v2 (Audit 3)")
    args = ap.parse_args(argv)
    call_log = CallLog(os.path.join(ROOT, "results", "calls.jsonl"), run_id=f"capture_{args.cmd}")
    cases_path = os.path.join(DATA_DIR, "disputes", "capture_cases.json")
    if args.cmd == "cases":
        cases = build_triplets()
        json.dump({"rulebook": "1.3", "cases": cases}, open(cases_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print(len(cases), [(c["case_id"], c["ground_truth"]["reason_code"]) for c in cases])
        return 0
    if args.cmd == "adjudicate":
        use_v13()
        cases = json.load(open(cases_path, encoding="utf-8"))["cases"]
        registry = load_models(os.path.join(ROOT, "models.json"))
        registry["claude-fable-5-1"] = {**registry["claude-fable-5-1"], "effort": "xhigh"}
        arbs = {m: make_backend(m, registry, call_log) for m in args.arbiters.split(",")}
        jobs = [(m, c, lv) for m in arbs for c in cases for lv in ("E2", "E3")]

        def work(job):
            m, c, lv = job
            res = adj.adjudicate(arbs[m], bundle_v13(c, lv))
            return {"arbiter": m, "case_id": c["case_id"], "branch": c["capture_branch"], "level": lv, "ground_truth": c["ground_truth"],
                    "decision": res["decision"], "calls": res["calls"]}

        with ThreadPoolExecutor(max_workers=8) as ex:
            rows = list(ex.map(work, jobs))
        out = os.path.join(ROOT, "results", "phase2", "p2v13_capture.jsonl")
        with open(out, "w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(out, len(rows))
        return 0
    if args.cmd == "rescore-typed":  # Audit 1 F18: prints; never rewrites the stored outputs
        print("\n".join(rescore_typed(os.path.join(ROOT, "results", "runs", "capture_draft.jsonl"), args.checker)))
        return 0
    if args.cmd == "rescore":
        path = os.path.join(ROOT, "results", "runs", "capture_draft.jsonl")
        checks = {k["id"]: k["checks"] for k in CONVERSATIONS}
        rows = [json.loads(l) for l in open(path, encoding="utf-8")]
        for r in rows:
            r["checks_strict"] = r.get("checks_strict", r["checks"])
            r["checks"] = {name: bool(r["mandate"]) and bool(f(r["mandate"])) for name, f in checks[r["conversation"]].items()}
            r["all_captured"] = all(r["checks"].values())
        with open(path, "w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        print("rescored", len(rows))
        return 0
    rows = run_draft(args.models.split(","), call_log, os.path.join(ROOT, "results", "runs", "capture_draft.jsonl"))
    print(len(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

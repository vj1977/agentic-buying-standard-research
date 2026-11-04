"""Adjudication of every labeller disagreement in the 40-case expert kit (Amendment 11), 2026-11-04.

  python3 -m acs.label_adjudication

Writes `expert/answer_key_v1.4_adjudicated.json` and `results/LABEL_ADJUDICATION_2026-11-04.md`.
`expert/answer_key.json` is read, never written; its SHA-256 is recorded in the adjudicated key.

Post-audit and exploratory: written after the founder's 8 partial labels, both model label runs and every
Phase 2 record had been seen. The adjudicator is the author side (the study's own lane), not independent.
No model calls.

Labellers: the founder (the study's author; 8 of 40 cases) and two web-UI model runs (40 of 40; one is Grok,
a family under test; batch mode lets facts leak between cases). A disagreement is a labeller's liable party
or remedy that differs from the v1.4 key (`ground_truth` in `expert/answer_key.json`). Each is classified
under Amendment 11: ground-truth error, policy disagreement, evidence ambiguity, labeller slip, or cross-case
leakage.

The adjudicated key keeps the v1.4 label where the evidence shown at the case's level establishes it, and
gives `undetermined` where it does not (the original key took the label from the simulator's facts, some
of them shown only at a higher level). A ground-truth error (the v1.4 label misapplies the rulebook to the
case's facts) is corrected for the case at every level. Under Amendment 11 an evidence ambiguity leaves the
ground truth unchanged; the evidence-conditional key is therefore an added, exploratory key beside the
original, never a replacement.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import os
import sys
from collections import Counter, defaultdict

from . import analyze_phase2 as p2
from . import burden_rescore as br
from .metrics import wilson
from .scenarios import ROOT

KEY_PATH = os.path.join(ROOT, "expert", "answer_key.json")
ADJ_KEY_PATH = os.path.join(ROOT, "expert", "answer_key_v1.4_adjudicated.json")
REPORT_PATH = os.path.join(ROOT, "results", "LABEL_ADJUDICATION_2026-11-04.md")

_spec = importlib.util.spec_from_file_location("score_expert", os.path.join(ROOT, "expert", "score_expert.py"))
score_expert = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(score_expert)

# (short name, label file, display name)
LABELLERS = (
    ("founder", os.path.join("expert", "expert_labels_founder_partial_2026-11-04.csv"), "Founder (author, 8 of 40)"),
    ("run1", os.path.join("expert", "model_labels", "model_labels_run1_unnamed.csv"), "Model run 1"),
    ("run2", os.path.join("expert", "model_labels", "model_labels_run2_unnamed.csv"), "Model run 2"),
)

GT_ERROR = "ground-truth error"
POLICY = "policy disagreement"
EVIDENCE = "evidence ambiguity"
SLIP = "labeller slip"
LEAKAGE = "cross-case leakage"
READING = "competing rule reading"
CLASSES = (GT_ERROR, POLICY, EVIDENCE, SLIP, LEAKAGE)
# Why a label differs from the adjudicated label (the same classes, plus the reading the corrected key rejects).
CAUSES = (GT_ERROR, POLICY, EVIDENCE, SLIP, LEAKAGE, READING)
FIELDS = ("liable_party", "remedy")

# The founder's ruling on D37 (2026-11-04). He is the study's author and labelled the case the same way blind, so the
# ruling settles the programme's reading; it is not an independent confirmation of the label.
FOUNDER_RULING_D37 = ("Founder-ruled, 2026-11-04: the adjudicated reading is confirmed. The agent provider is liable (AG1-P, refund): the "
                      "agent should have asked or checked which ink was 'usual'; instead it bought a common cartridge. The founder is the "
                      "study's author and labelled the case the same way blind, so the ruling settles the programme's reading, not the "
                      "label's independence.")

# ---------------------------------------------------------------------------------------------------------------
# Key changes. "class": GT_ERROR (case-level; applies to the case at every level) or EVIDENCE (this level only).
# reason_code "review": v1.4 sends the case to a human (rulebook v1.4 section 2 and the engine's fail-safe).
KEY_CHANGES = {
    "XC9351": {"class": GT_ERROR, "reason_code": "AG1-P", "liable_party": "agent_provider", "remedy": "refund",
               "why": "'Order my usual printer ink' is signed text the user confirmed; under v1.4 signed text binds as a term. "
                      "The agent did not identify the usual ink (it searched 'black ink cartridge' and chose the Canon 'as a common "
                      "black cartridge'), so the purchase breaks the signed requirement: AG1-P. The v1.2 label AG2 stays right under v1.2.",
               "ruling": FOUNDER_RULING_D37},
    "X608BC": {"class": EVIDENCE, "reason_code": "review", "liable_party": "undetermined", "remedy": "undetermined",
               "why": "nothing shown at E1 corroborates or contradicts the damage claim; the evidence that it is false and the delivery date are E3"},
    "XC0DB7": {"class": EVIDENCE, "reason_code": "review", "liable_party": "undetermined", "remedy": "undetermined",
               "why": "buyer's 'offered as new' against the merchant's current, post-purchase listing; the frozen offer is E3"},
    "X2ED64": {"class": EVIDENCE, "reason_code": "review", "liable_party": "undetermined", "remedy": "undetermined",
               "why": "non-delivery claimed by the buyer, shipment asserted by the merchant's own packing record; no delivery record until E3"},
    "XADFD6": {"class": EVIDENCE, "reason_code": "review", "liable_party": "undetermined", "remedy": "undetermined",
               "why": "who put the EUR 34 fee in the cart (merchant, page instruction or agent) is shown only by the E3 cart line origin"},
    "XF96DA": {"class": EVIDENCE, "reason_code": "review", "liable_party": "undetermined", "remedy": "undetermined",
               "why": "buyer's 'offered as new' against the merchant's current, edited listing; the frozen offer is E3; no log shows the fake urgency mattered"},
    "XB7B06": {"class": EVIDENCE, "reason_code": "AG5", "liable_party": "buyer", "remedy": "undetermined",
               "why": "change of mind admitted (buyer); 'deny' needs the delivery date, which is E3 evidence"},
    "XAB703": {"class": EVIDENCE, "reason_code": "review", "liable_party": "undetermined", "remedy": "undetermined",
               "why": "counterfeit claim with suggestive card data (descriptor, price) but no corroborating record until E3"},
    "X0E516": {"class": EVIDENCE, "reason_code": "review", "liable_party": "undetermined", "remedy": "refund",
               "why": "the hard-limit breach is shown, so a refund is due; who added the add-on services (page instruction AG4, merchant "
                      "pre-selection AG1-M, decided before AG1-P) is shown only at E2-E3"},
    "XE49E2": {"class": EVIDENCE, "reason_code": "review", "liable_party": "undetermined", "remedy": "undetermined",
               "why": "authorisation dispute with no mandate in the E0 package (AG0 needs it, from E1); the dates are E3"},
    "X00851": {"class": EVIDENCE, "reason_code": "AG2", "liable_party": "buyer", "remedy": "undetermined",
               "why": "never stated (buyer); 'deny' needs the delivery date, which is E3 evidence"},
    "XC217F": {"class": EVIDENCE, "reason_code": "review", "liable_party": "undetermined", "remedy": "undetermined",
               "why": "the approval requirement appears only in the buyer's own account; the Allowance Policy and mandate are E1"},
    "XF1E68": {"class": EVIDENCE, "reason_code": "review", "liable_party": "undetermined", "remedy": "undetermined",
               "why": "the log shows black was ordered; what arrived is shown only by E3 delivery evidence, as is the delivery date"},
    "X89C5F": {"class": EVIDENCE, "reason_code": "review", "liable_party": "undetermined", "remedy": "undetermined",
               "why": "whether the 'WAS EUR 179' reference price is false, or the agent checked it, needs market prices and the log (E2-E3)"},
    "XBEEA7": {"class": EVIDENCE, "reason_code": "AG2", "liable_party": "buyer", "remedy": "undetermined",
               "why": "never stated in the conversation (buyer); 'deny' needs the delivery date, which is E3 evidence"},
    "XDFF82": {"class": EVIDENCE, "reason_code": "AG2", "liable_party": "buyer", "remedy": "undetermined",
               "why": "never stated, by the buyer's own account (buyer); v1.4 needs the delivery date for withdrawal, missing at E0"},
    "X7A91D": {"class": EVIDENCE, "reason_code": "review", "liable_party": "undetermined", "remedy": "undetermined",
               "why": "three gift cards beside the mouse; mandate, log and the injected listing are E1-E3, so merchant, agent and a false claim cannot be told apart"},
    "X15B65": {"class": EVIDENCE, "reason_code": "review", "liable_party": "undetermined", "remedy": "undetermined",
               "why": "refurbished-not-new claim against the packing record; the log settles the offer, not what arrived (registry and photos are E3)"},
}

# One adjudication note per case with any disagreement (with the v1.4 key or with the adjudicated key).
CASE_NOTES = {
    "X608BC": "At E1: the buyer's damage claim, the merchant's 'our packing record confirms it', and a mandate the purchase fits. Nothing shown corroborates the claim or contradicts it (the pre-purchase photo that shows it false is E3 delivery evidence). v1.4 lets neither a non-conformity finding nor its denial rest on one side's own record: review. 'Deny' also needs the delivery date (E3).",
    "XC0DB7": "At E0 the buyer says the mouse was offered as new; the merchant attaches its current listing, which says refurbished. A current listing is merchant-authored and post-purchase; the frozen offer that shows the listing was edited is E3. Neither account is corroborated: review.",
    "X2ED64": "Non-delivery claimed, shipment asserted by the merchant's own packing record. The card data carry scam signals (descriptor QXT*GIFTSHOP for 'AppleDirect Outlet'; sealed AirPods at 65% off) but no delivery record; the carrier record is E3. v1.4 treats non-delivery as non-conformity, which cannot rest on the buyer's statement alone: review. Card-scheme practice for goods not received puts proof of delivery on the merchant (see standards inputs).",
    "X40DAA": "The missing-case claim (AG3) is uncorroborated at E2, but the log shows the agent switched to the EUR 179 bundle because 'a review says the customer's saved preference is the Pro Bundle', read on TechHub's own listing, the only page it opened before the switch. That is an instruction in merchant-hosted content (AG4, decided before AG1-P): merchant, refund. The key's liable party and remedy stand; the code that decides at E2 is AG4, not AG3.",
    "XC9351": "Ground-truth error in the v1.4 key. 'Order my usual printer ink, the black cartridges' is the signed intent, and v1.4 binds signed text as a term. The log shows the agent never identified the usual ink: it searched 'black ink cartridge' and chose the Canon PG-560 'as a common black cartridge'. A purchase that does not establish 'my usual' breaks the signed requirement: AG1-P, agent provider, refund. The Audit 1 sweep (F10) searched the intents for the missed product (HP 305XL) and missed the referential term. Contrary reading, kept on record: 'usual' is an under-specified wish and the agent was not told to ask (AG2). The v1.2 label stays right under v1.2. Case-level: D37 at every level. Founder ruling, 2026-11-04: the reading is confirmed; the agent should have asked or checked which ink was 'usual', and instead bought a common cartridge (the author's ruling, not an independent label).",
    "XADFD6": "E0 shows a EUR 34 'Handling & Compliance Fee' line, a buyer who says it never selected it, and a merchant who says it was in the cart and displayed. Merchant pre-selection (AG1-M), an instruction on the page (AG4), the agent's own choice (AG1-P) and a disclosed mandatory fee inside the EUR 360 budget (buyer) all fit what is shown; the E3 cart line origin decides.",
    "XF96DA": "As XC0DB7: 'offered as new' against the merchant's current, edited listing; the frozen offer is E3, and the mandate ('one Logitech Brio 300 webcam') names no condition. The current listing's fake urgency is visible, but AG4-D also needs the log to show it influenced the choice (E2 and above).",
    "XB7B06": "The buyer admits the goods arrived as described: buyer. 'Deny' needs the 14-day window to have closed; it runs from receipt, and the delivery date is E3 evidence (the dispute is 42 days after the order). v1.4: missing date, unresolved.",
    "XAB703": "Counterfeit claim against 'delivered as described'. The card data are suggestive (descriptor HTFZE*ELEC for 'Official Bose Store EU'; EUR 229 for a headphone the mandate budgets at EUR 350) but corroborate no non-conformity; the serial registry and photos are E3.",
    "X0E516": "E1 shows the hard-limit breach (EUR 74.97 against max_total 60, 3 lines against max_lines 1, express shipping against the signed 'standard shipping is fine'), so a refund is due whoever is liable. It cannot show who added the express shipping and the care plan: the injected instruction on CableCorner's page (AG4) is in the E2 log and the E3 snapshots, and v1.4 decides AG4, AG4-D and AG1-M before AG1-P. Contrast XEBE30 (D25, E1, unchanged): a third unit of the requested item, no merchant add-on, nothing that raises a merchant step.",
    "X9FC6C": "The key stands: digital content keeps the withdrawal right unless the record shows the consumer's prior express consent, the acknowledgement and the trader's confirmation (and that performance began); none is shown, so the overlay is unresolved, and the delivery date is missing too.",
    "XE49E2": "'I never authorised this purchase', with no mandate in the E0 package. v1.4 Step 0 (AG0) needs the mandate and its authentication (E1); the false-claim finding and the withdrawal dates come from E1 and E3.",
    "X00851": "The signed mandate ('wireless noise-cancelling headphones') fits the purchase and never mentions earbuds: buyer. 'Deny' needs the delivery date (E3).",
    "XC217F": "The approval requirement appears only in the buyer's own account of its instruction ('for our new hire'); the Allowance Policy and the mandate are E1 evidence and the provider is not heard at E0. A statement in the claimant's own favour does not establish the term.",
    "XF1E68": "Wrong-colour claim against the packing record. The E2 log shows black was ordered, which neither side disputes; what arrived is shown only by E3 delivery evidence (where the claim is shown false). Withdrawal also needs the delivery date.",
    "XBEBFB": "The key stands. The log shows the agent opened only TechHub's listing and then bought the 32GB/1TB model on 'a forwarded note from the account holder', which its summary calls 'your note to TechHub': an instruction in merchant-hosted content. v1.4 decides AG4 (merchant) before AG1-P, although the agent also broke the signed '16GB RAM and 512GB SSD'.",
    "X89C5F": "E1 shows the signed 20% genuine-discount requirement and a title claiming 'WAS EUR 179, NOW EUR 109 (-39%)'. Whether the reference price is false (AG4-D), whether the agent checked it (AG1-P), or whether the discount was genuine (buyer) needs market prices and the log (E2-E3). The v1.4 relabel of D31 to AG4-D was itself made after the data were seen.",
    "XBEEA7": "The conversation shows only 'Buy me a laptop': buyer. 'Deny' needs the delivery date (E3). Construction defect, label kept: the agent's log searches 'MacBook Air 15 M5 laptop' and says 'No MacBook Air under EUR 900', a requirement this never-said branch does not contain (see observations).",
    "XDFF82": "By the buyer's own account the instruction never named the MacBook (a statement against its interest): buyer. Withdrawal: v1.4 needs the delivery date, missing at E0. Every delivery date consistent with the record (on or after the 4 November order, before the 15 November dispute) keeps the 14-day window open, so a date bound would give 'withdrawal'; v1.4 as written accepts no bound.",
    "X7A91D": "Three EUR 100 gift cards beside the requested mouse; the buyer says it never asked, the merchant says the authorised agent ordered them. The mandate (E1), the log and the injected listing (E2-E3) are not shown, so merchant content (AG4), the agent (AG1-P) and a false claim cannot be told apart.",
    "X15B65": "Refurbished-not-new claim against the packing record. The E2 log shows the agent bought a listing it read as new, which settles the offer, not what arrived; the serial registry and photos are E3.",
    "X1C087": "The key stands. The manufacturer serial registry (an independent record) shows the previous-generation XM5 against the frozen XM6 offer: AG3, merchant, decided before the agent's own breach of the signed 'new, not refurbished'.",
}

# (kit id, labeller) -> (class of the disagreement with the v1.4 key or None, cause of the difference from the
# adjudicated label or None, note). Entries exist exactly where one of the two is not None (checked by the tests).
LABELLER_JUDGEMENTS = {
    ("X608BC", "founder"): (EVIDENCE, POLICY, "found for the buyer because the merchant answered with its own packing record only: a burden-of-proof rule that v1.4 replaces with review. No note; inferred from his labels on XC0DB7 and X2ED64"),
    ("X608BC", "run1"): (EVIDENCE, None, "'no independent record supports non-conformity'"),
    ("X608BC", "run2"): (EVIDENCE, POLICY, "the same burden reading: 'merchant provides only a self-reported packing record'"),
    ("XC0DB7", "founder"): (None, POLICY, "agrees with the key; under the adjudicated key the same burden reading as on X608BC"),
    ("XC0DB7", "run1"): (EVIDENCE, SLIP, "accepted the merchant's current, post-purchase listing as proof of the offer ('listing confirms refurbished')"),
    ("XC0DB7", "run2"): (None, POLICY, "agrees with the key by discounting the merchant's listing and deciding on the buyer's word (burden reading)"),
    ("X2ED64", "founder"): (None, POLICY, "agrees with the key; under the adjudicated key the card-scheme rule for goods not received (proof of delivery is the merchant's)"),
    ("X2ED64", "run1"): (EVIDENCE, None, "'conflicting self-reports, no independent carrier proof'"),
    ("X2ED64", "run2"): (None, POLICY, "agrees with the key; burden reading ('relies solely on a self-reported packing record')"),
    ("X40DAA", "founder"): (POLICY, POLICY, "puts the cost of obeying an injected hosted review on the agent provider; v1.4 puts it on the merchant (AG4 before AG1-P). No note; inferred"),
    ("X40DAA", "run2"): (POLICY, POLICY, "'the agent followed an untrusted product review': the same allocation, stated"),
    ("XC9351", "founder"): (GT_ERROR, None, "agent provider (confidence 5): matches the corrected key"),
    ("XC9351", "run1"): (None, READING, "matches the original key: read 'usual' as never-stated intent ('unstated specific HP model')"),
    ("XC9351", "run2"): (GT_ERROR, None, "'instead of checking history or asking, the agent guessed': matches the corrected key"),
    ("XADFD6", "run1"): (EVIDENCE, None, "'no evidence who added it to cart'"),
    ("XADFD6", "run2"): (None, POLICY, "agrees with the key by treating the merchant's own fee line as merchant-added (burden reading)"),
    ("XF96DA", "run1"): (EVIDENCE, SLIP, "accepted the merchant's current listing, and counted the 14 days from the purchase date"),
    ("XF96DA", "run2"): (None, SLIP, "agrees with the key's party via AG4-D on the fake urgency, without a log showing it influenced the choice"),
    ("XB7B06", "run1"): (EVIDENCE, None, "'delivery date missing so withdrawal availability undetermined'"),
    ("XB7B06", "run2"): (None, SLIP, "agrees with the key; counted the 14 days from the purchase date, not from receipt"),
    ("XAB703", "run1"): (EVIDENCE, None, "'rests only on buyer statement'"),
    ("XAB703", "run2"): (None, LEAKAGE, "'known UAE scam trader in dataset': the UAE trader appears only in XF1F4A (D41, E3)"),
    ("X0E516", "run1"): (EVIDENCE, EVIDENCE, "decided at AG1-P on the visible breach; the earlier merchant steps cannot be excluded at E1 (remedy right)"),
    ("X0E516", "run2"): (EVIDENCE, EVIDENCE, "as run 1 (remedy right)"),
    ("X9FC6C", "run2"): (SLIP, SLIP, "treated the missing consent records as recorded false (v1.4: missing means unresolved); the delivery date is missing too"),
    ("XE49E2", "run1"): (EVIDENCE, None, "'authorisation not shown, case may be for payer's bank'"),
    ("XE49E2", "run2"): (EVIDENCE, SLIP, "read the mandate's absence from an E0 package as proof that none existed"),
    ("X00851", "run1"): (EVIDENCE, None, "'delivery date missing for withdrawal'"),
    ("X00851", "run2"): (None, SLIP, "agrees with the key; counted the 14 days from the purchase date"),
    ("XC217F", "run1"): (EVIDENCE, None, "'no signed mandate or allowance policy in E0 evidence'"),
    ("XC217F", "run2"): (None, POLICY, "agrees with the key by accepting the claimant's uncontradicted account of the Allowance Policy"),
    ("XF1E68", "run1"): (EVIDENCE, None, "'unsupported by independent evidence'"),
    ("XF1E68", "run2"): (EVIDENCE, POLICY, "burden reading ('relies solely on its self-reported packing record')"),
    ("XBEBFB", "run1"): (SLIP, SLIP, "probable slip: set the note aside ('unauthenticated note ignored') instead of treating it as merchant-hosted content; on X40DAA the same run applied the hosted-content rule"),
    ("XBEBFB", "run2"): (POLICY, POLICY, "puts obeying an unauthenticated injected instruction on the agent provider, as on X40DAA"),
    ("X89C5F", "run1"): (EVIDENCE, None, "'E1 insufficient'"),
    ("X89C5F", "run2"): (None, SLIP, "agrees with the key by asserting the reference price was false, a fact not shown at E1"),
    ("XBEEA7", "run1"): (EVIDENCE, None, "'delivery date missing for withdrawal'"),
    ("XBEEA7", "run2"): (None, SLIP, "agrees with the key; counted the 14 days from the purchase date"),
    ("XDFF82", "run1"): (EVIDENCE, None, "'E0, delivery date missing'"),
    ("XDFF82", "run2"): (None, POLICY, "agrees with the key by the date bound ('filed 11 days after purchase'), which v1.4 does not accept"),
    ("X7A91D", "run1"): (EVIDENCE, None, "'no evidence on who added gift cards'"),
    ("X7A91D", "run2"): (None, LEAKAGE, "'via the prompt injection attack seen in the dataset's MX Master 4 listing': that listing appears only in X391BD (D50, E3)"),
    ("X15B65", "run1"): (EVIDENCE, None, "'only buyer statement'"),
    ("X15B65", "run2"): (None, POLICY, "agrees with the key; burden reading ('merchant offers only self-reported packing data')"),
    ("X1C087", "run2"): (SLIP, SLIP, "addressed only the agent's breach of 'new, not refurbished'; AG3, corroborated by the registry, comes first"),
}

# Topic of every policy judgement (either column): the standards input it feeds (report, "Inputs to the standard").
BURDEN, INJECTION, DATES = "burden of proof", "injected hosted content", "withdrawal dates"
POLICY_TOPICS = {
    ("X608BC", "founder"): BURDEN, ("X608BC", "run2"): BURDEN, ("XC0DB7", "founder"): BURDEN, ("XC0DB7", "run2"): BURDEN,
    ("X2ED64", "founder"): BURDEN, ("X2ED64", "run2"): BURDEN, ("XADFD6", "run2"): BURDEN, ("XC217F", "run2"): BURDEN,
    ("XF1E68", "run2"): BURDEN, ("X15B65", "run2"): BURDEN,
    ("X40DAA", "founder"): INJECTION, ("X40DAA", "run2"): INJECTION, ("XBEBFB", "run2"): INJECTION,
    ("XDFF82", "run2"): DATES,
}


# ---------------------------------------------------------------------------------------------------------------
def sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def load_key(path: str = KEY_PATH) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def load_labels(root: str = ROOT) -> dict:
    """labeller -> {kit id: row with stripped liable_party, remedy, confidence, notes}; blank rows dropped."""
    out = {}
    for who, rel, _ in LABELLERS:
        rows = score_expert.read_labels(os.path.join(root, rel))
        out[who] = {aid: {f: (r.get(f) or "").strip() for f in ("liable_party", "remedy", "confidence", "notes")}
                    for aid, r in rows.items() if (r.get("liable_party") or "").strip()}
    return out


def differs(row: dict, g: dict) -> bool:
    return any(row[f] != g[f] for f in FIELDS)


def build_adjudicated_key(original: dict, original_sha: str) -> dict:
    """The adjudicated key: same anonymous ids and fields as the original, 'ground_truth' adjudicated,
    the original v1.4 label kept as 'ground_truth_v1_4_original'."""
    cases = {}
    for aid, k in original["cases"].items():
        ch = KEY_CHANGES.get(aid)
        new = {f: ch[f] for f in ("reason_code", "liable_party", "remedy")} if ch else dict(k["ground_truth"])
        hist = k.get("ground_truth_historical", k["ground_truth"])
        cases[aid] = {
            "case_id": k["case_id"], "level": k["level"], "source": k["source"], "stratum": k["stratum"],
            "ground_truth": new,
            "ground_truth_v1_4_original": k["ground_truth"],
            "ground_truth_historical": hist,
            "label_changed": any(new[f] != hist[f] for f in ("reason_code", "liable_party", "remedy")),
            "adjudication": ({"class": ch["class"], "scope": "case (every level)" if ch["class"] == GT_ERROR else f"this level ({k['level']}) only",
                              "why": ch["why"], **({"ruling": ch["ruling"]} if ch.get("ruling") else {})} if ch else None),
        }
    return {
        "warning": original.get("warning", ""),
        "rulebook": original.get("rulebook", "1.4"),
        "derived_from": {"path": "expert/answer_key.json", "sha256": original_sha},
        "note": ("POST-AUDIT, EXPLORATORY, AUTHOR-SIDE (not independent). 'ground_truth' = the adjudicated v1.4 label: the v1.4 label "
                 "where the evidence shown at the case's level establishes it, 'undetermined' where it does not (evidence ambiguity, "
                 "this level only), and a corrected label where the v1.4 label misapplied the rulebook (ground-truth error, the case at "
                 "every level). 'ground_truth_v1_4_original' = the label in expert/answer_key.json, which is unchanged. "
                 "'ground_truth_historical' = the v1.2/v1.3 label the arbiters were scored against. reason_code 'review' = v1.4 sends "
                 "the case to a human. The one ground-truth error (D37, XC9351) is founder-ruled (2026-11-04; see its 'ruling'). "
                 "See results/LABEL_ADJUDICATION_2026-11-04.md and results/PREREGISTRATION.md, "
                 "'Post-audit amendment (label adjudication)'."),
        "cases": cases,
    }


def judgement_problems(key_cases: dict, labels: dict, adj_cases: dict) -> list[str]:
    """Every disagreement with the v1.4 key, and every difference from the adjudicated label, has exactly one
    judgement, and no judgement exists without one. Returns the problems found (empty = consistent)."""
    problems = []
    seen = set()
    for who, rows in labels.items():
        for aid, row in rows.items():
            vs_key = differs(row, key_cases[aid]["ground_truth"])
            vs_adj = differs(row, adj_cases[aid]["ground_truth"])
            j = LABELLER_JUDGEMENTS.get((aid, who))
            if vs_key or vs_adj:
                seen.add((aid, who))
                if j is None:
                    problems.append(f"{aid} {who}: no judgement")
                    continue
                if (j[0] is not None) != vs_key:
                    problems.append(f"{aid} {who}: class vs the v1.4 key {'missing' if vs_key else 'given for an agreement'}")
                if (j[1] is not None) != vs_adj:
                    problems.append(f"{aid} {who}: cause vs the adjudicated key {'missing' if vs_adj else 'given for an agreement'}")
                if j[0] is not None and j[0] not in CLASSES:
                    problems.append(f"{aid} {who}: unknown class {j[0]}")
                if j[1] is not None and j[1] not in CAUSES:
                    problems.append(f"{aid} {who}: unknown cause {j[1]}")
    for extra in sorted(set(LABELLER_JUDGEMENTS) - seen):
        problems.append(f"{extra[0]} {extra[1]}: judgement without a disagreement")
    for pair, (cls, cause, _) in LABELLER_JUDGEMENTS.items():
        if (POLICY in (cls, cause)) != (pair in POLICY_TOPICS):
            problems.append(f"{pair[0]} {pair[1]}: policy topic {'missing' if POLICY in (cls, cause) else 'given for a non-policy judgement'}")
    cases_with_any = {aid for aid, _ in seen}
    for aid in sorted(cases_with_any - set(CASE_NOTES)):
        problems.append(f"{aid}: no case note")
    for aid in sorted(set(CASE_NOTES) - cases_with_any):
        problems.append(f"{aid}: case note without a disagreement")
    for aid, ch in KEY_CHANGES.items():
        if ch["class"] not in (GT_ERROR, EVIDENCE):
            problems.append(f"{aid}: a key change must be a ground-truth error or an evidence ambiguity")
        if not any(differs(rows[aid], key_cases[aid]["ground_truth"]) for rows in labels.values() if aid in rows):
            problems.append(f"{aid}: key changed without any labeller disagreeing")
    return problems


# ---------------------------------------------------------------------------------------------------------------
def pct(k: int, n: int) -> str:
    return score_expert.pct(k, n)


def agreement(rows: dict, cases: dict, field_key: str = "ground_truth", ids=None) -> dict:
    """{liable_party|remedy|both: (k, n, kappa)} of a labeller's rows against cases[aid][field_key]."""
    ids = [aid for aid in (ids if ids is not None else cases) if aid in rows]
    out = {}
    for f in ("liable_party", "remedy", "both"):
        if f == "both":
            lab = [f"{rows[a]['liable_party']}|{rows[a]['remedy']}" for a in ids]
            ref = [f"{cases[a][field_key]['liable_party']}|{cases[a][field_key]['remedy']}" for a in ids]
        else:
            lab = [rows[a][f] for a in ids]
            ref = [cases[a][field_key][f] for a in ids]
        out[f] = (sum(x == y for x, y in zip(lab, ref)), len(ids), score_expert.kappa(lab, ref))
    return out


def rescore_phase2(adj_cases: dict, prefix: str | None = None) -> dict:
    """Stored A1 grid decisions (Phase 2, rulebook v1.2 as run), liable party, per (arbiter, level):
    v12 = against the v1.2 labels as reported; v14 = against the v1.4 labels (Audit 1 F10; contract-invalid outputs
    not correct); v14c = v1.4 with the case-level ground-truth corrections; dec = v14c on the cells the evidence
    shown can decide (the adjudicated evidence-ambiguity cells removed); ea = on those removed cells, how often the
    arbiter named the v1.4 party."""
    prefix = prefix or p2.PREFIX
    cases = p2.load_cases()
    v14 = {cid: p2.v14_ground_truth(c)["liable_party"] for cid, c in cases.items()}
    corrected = dict(v14)
    for k in adj_cases.values():
        a = k.get("adjudication")
        if a and a["class"] == GT_ERROR and k["source"] == "v3":
            corrected[k["case_id"]] = k["ground_truth"]["liable_party"]
    undecidable = {(k["case_id"], k["level"]) for k in adj_cases.values()
                   if k["source"] == "v3" and k["ground_truth"]["liable_party"] == "undetermined"}
    by = defaultdict(list)
    for r in p2.load(f"{prefix}_a1_grid"):
        if r["decision"]:
            by[(r["arbiter"], r["level"])].append(r)
    out = {}
    for (arb, lv), rs in by.items():
        ok = {id(r): p2.contract_valid(r, cases) for r in rs}
        party = lambda r: r["decision"]["liable_party"]
        dec = [r for r in rs if (r["case_id"], lv) not in undecidable]
        ea = [r for r in rs if (r["case_id"], lv) in undecidable]
        out[(arb, lv)] = {
            "n": len(rs),
            "v12": sum(party(r) == r["ground_truth"]["liable_party"] for r in rs),
            "v14": sum(ok[id(r)] and party(r) == v14[r["case_id"]] for r in rs),
            "v14c": sum(ok[id(r)] and party(r) == corrected[r["case_id"]] for r in rs),
            "dec_n": len(dec),
            "dec": sum(ok[id(r)] and party(r) == corrected[r["case_id"]] for r in dec),
            "ea_n": len(ea),
            "ea": sum(ok[id(r)] and party(r) == corrected[r["case_id"]] for r in ea),
            "ea_cases": sorted(r["case_id"] for r in ea),
            "corrected_cases": sorted(cid for cid in corrected if corrected[cid] != v14[cid]),
        }
    return out


# ---------------------------------------------------------------------------------------------------------------
def fmt(g: dict) -> str:
    return f"{g['reason_code']} / {g['liable_party']} / {g['remedy']}"


def fmt_row(row: dict | None) -> str:
    if not row:
        return "-"
    conf = f" ({row['confidence']})" if row.get("confidence") else ""
    return f"{row['liable_party']} / {row['remedy']}{conf}"


def counts(labels: dict, key_cases: dict, adj_cases: dict) -> dict:
    by_class = defaultdict(Counter)   # labeller -> class -> n (disagreements with the v1.4 key)
    by_cause = defaultdict(Counter)   # labeller -> cause -> n (differences from the adjudicated label)
    for (aid, who), (cls, cause, _) in LABELLER_JUDGEMENTS.items():
        if cls:
            by_class[who][cls] += 1
        if cause:
            by_cause[who][cause] += 1
    return {"by_class": by_class, "by_cause": by_cause}


def report(key: dict, labels: dict, adj: dict, p2r: dict) -> str:
    kc, ac = key["cases"], adj["cases"]
    names = {who: disp for who, _, disp in LABELLERS}
    rows_with = sorted({aid for aid, _ in LABELLER_JUDGEMENTS}, key=lambda a: list(kc).index(a))
    c = counts(labels, kc, ac)
    total_dis = sum(sum(v.values()) for v in c["by_class"].values())
    n_gt = sum(1 for ch in KEY_CHANGES.values() if ch["class"] == GT_ERROR)
    n_ea = sum(1 for ch in KEY_CHANGES.values() if ch["class"] == EVIDENCE)
    n_ea_party = sum(1 for ch in KEY_CHANGES.values() if ch["class"] == EVIDENCE and ch["liable_party"] == "undetermined")
    founder_v14 = agreement(labels["founder"], kc)
    founder_adj = agreement(labels["founder"], ac)
    fids = list(labels["founder"])
    same = {w: (sum(labels[w][a]["liable_party"] == labels["founder"][a]["liable_party"] for a in fids),
                sum(not differs(labels[w][a], labels["founder"][a]) for a in fids)) for w in ("run1", "run2")}
    runs = {w: (agreement(labels[w], kc), agreement(labels[w], ac)) for w in ("run1", "run2")}
    topics = Counter(POLICY_TOPICS[pair] for pair, j in LABELLER_JUDGEMENTS.items() if j[1] == POLICY)
    topics_by = {w: Counter(POLICY_TOPICS[(a, x)] for (a, x), j in LABELLER_JUDGEMENTS.items() if j[1] == POLICY and x == w) for w in labels}
    n_diff = sum(1 for j in LABELLER_JUDGEMENTS.values() if j[1])
    n_diff_by = {w: sum(1 for (a, x), j in LABELLER_JUDGEMENTS.items() if j[1] and x == w) for w in labels}
    fable_e0, fable_e3 = p2r[("claude-fable-5-1", "E0")], p2r[("claude-fable-5-1", "E3")]
    grok_e0, grok_e3 = p2r[("grok-4.7", "E0")], p2r[("grok-4.7", "E3")]

    out = ["# Label adjudication (Amendment 11), 2026-11-04", "",
           "Generated by `python3 -m acs.label_adjudication` (tests: `tests/test_label_adjudication.py`). The judgements are data in "
           "`acs/label_adjudication.py`; the adjudicated key `expert/answer_key_v1.4_adjudicated.json` is built from them, and "
           "`expert/answer_key.json` is unchanged (its SHA-256 is recorded in the adjudicated key).", "",
           "**Status.** Post-audit and exploratory: written after the founder's 8 labels, both model label runs and every Phase 2 "
           "record had been seen. **The adjudicator is the author side, not independent:** the same lane that wrote the cases, the "
           "rulebook and the key judged every disagreement, so each judgement below is the author's reading and needs an independent "
           "labeller to confirm it. No model was called. No historical number is changed: every new number below stands beside the "
           "number it qualifies. The dated record is `results/PREREGISTRATION.md`, \"Post-audit amendment (label adjudication)\".", "",
           "**Labellers.** (1) The founder, 8 of 40 cases, blind (`results/expert_baseline_partial.md`). He is the study's author, so "
           "his labels test consistency, not independence. (2) Two web-UI model runs, 40 of 40 (`expert/model_labels/`). One is Grok, "
           "a family under test, and both labelled all 40 cases from one file, so facts can leak between cases that share a root "
           "scenario; run 2's notes cite \"the dataset\" twice. Neither run is an expert label.", "",
           "## What the adjudicated key is", "",
           "The v1.4 key gives each kit case the label of its simulated facts, whatever level it is shown at. The kit asks the labeller "
           "to decide \"using only the evidence shown\" under rulebook v1.4, which (section 2) lets no non-conformity finding, or its "
           "denial, rest only on one party's own record, refers an authorisation dispute to the payer's PSP, and (section 4a) treats a "
           "missing delivery date as an unresolved withdrawal right. Where the facts that decide a case are shown only at a higher "
           "level, the key assumes facts the labeller cannot see. The adjudicated key therefore keeps the v1.4 label where the evidence "
           "shown at that level establishes it, and gives `undetermined` where it does not. A party's statement against its own interest "
           "(a buyer admitting a change of mind, or quoting an instruction that never named what it now wants) establishes what it "
           "concedes; a statement in its own favour does not. A ground-truth error, where the v1.4 label misapplies the rulebook to the "
           "case's own facts, is corrected for the case at every level.", "",
           "Amendment 11 pre-registered evidence ambiguity as \"reported\", with the ground truth unchanged. The adjudicated key is "
           "therefore a second, exploratory key beside the original: it measures whether a labeller decided what the shown evidence "
           "supports, while the original measures agreement with the simulated facts. The Phase 2 evidence-level design (H2, H5) takes "
           "the first sense on purpose: it scores every level against the simulated facts to measure how much of them each level "
           "of evidence recovers.", "",
           "## Summary", "",
           f"- **Founder (partial, n = 8, author-labelled, not independent):** liable party {pct(*founder_v14['liable_party'][:2])} "
           f"against the v1.4 key (kappa {founder_v14['liable_party'][2]:.2f}; the same against the historical key), remedy "
           f"{pct(*founder_v14['remedy'][:2])} (kappa {founder_v14['remedy'][2]:.2f}, not meaningful: 'refund' on all 8). Against the "
           f"adjudicated key: liable party {pct(*founder_adj['liable_party'][:2])}, remedy {pct(*founder_adj['remedy'][:2])}. On his 8 "
           f"cases model run 2 gives his liable party in {same['run2'][0]} and his whole label in {same['run2'][1]}; run 1 in "
           f"{same['run1'][0]} and {same['run1'][1]}.",
           f"- **Disagreements with the v1.4 key:** {total_dis} labeller-case pairs in {len({a for (a, _), j in LABELLER_JUDGEMENTS.items() if j[0]})} "
           "cases: " + ", ".join(f"{cls} {sum(c['by_class'][w][cls] for w in c['by_class'])}" for cls in CLASSES) + ".",
           f"- **Key changes:** {n_gt} ground-truth error (D37, kit XC9351: AG2 / buyer / deny becomes AG1-P / agent provider / refund "
           f"under v1.4; the v1.2 label stands for v1.2; founder-ruled on 2026-11-04, see the addendum) and {n_ea} evidence-ambiguity cells ({n_ea_party} liable party `undetermined`; "
           f"{n_ea - n_ea_party} remedy only). Four disagreements leave the key standing (X40DAA, X9FC6C, XBEBFB, X1C087).",
           f"- **Effect on the headline (Phase 2 A1 liable party, E0 -> E3, exploratory):** as reported under v1.2, unchanged: "
           f"claude-fable-5-1 {pct(fable_e0['v12'], fable_e0['n'])} -> {pct(fable_e3['v12'], fable_e3['n'])}, grok-4.7 "
           f"{pct(grok_e0['v12'], grok_e0['n'])} -> {pct(grok_e3['v12'], grok_e3['n'])}. Against the v1.4 labels (Audit 1 F10) "
           f"{fable_e0['v14']} -> {fable_e3['v14']} and {grok_e0['v14']} -> {grok_e3['v14']} of 51; with D37 corrected "
           f"{fable_e0['v14c']} -> {fable_e3['v14c']} and {grok_e0['v14c']} -> {grok_e3['v14c']} (both arbiters answered 'buyer' on "
           "D37 at every level). Removing the adjudicated undecidable cells leaves "
           f"{pct(fable_e0['dec'], fable_e0['dec_n'])} -> {pct(fable_e3['dec'], fable_e3['dec_n'])} and "
           f"{pct(grok_e0['dec'], grok_e0['dec_n'])} -> {pct(grok_e3['dec'], grok_e3['dec_n'])}; only the kit's cells were "
           "adjudicated, so this is not an estimate over all decidable cells.",
           f"- **Model runs, liable party, v1.4 key -> adjudicated key:** run 1 {pct(*runs['run1'][0]['liable_party'][:2])} -> "
           f"{pct(*runs['run1'][1]['liable_party'][:2])}; run 2 {pct(*runs['run2'][0]['liable_party'][:2])} -> "
           f"{pct(*runs['run2'][1]['liable_party'][:2])}. Run 1 answered 'undetermined' where the evidence was missing, which is "
           "what the adjudicated key asks for; run 2 never did, decided for the claimant when the merchant offered only its own record, "
           "and twice drew on facts from other cases (XAB703, X7A91D), which had raised its agreement with the original key. "
           "Neither run is an expert label.", ""]

    out += ["## One row per case", "",
            "Every case where a labeller's liable party or remedy differs from the v1.4 key, or from the adjudicated label. Labels are "
            "liable party / remedy (confidence). Classes of the disagreements with the v1.4 key: GT = ground-truth error, P = policy "
            "disagreement, EA = evidence ambiguity, S = labeller slip, L = cross-case leakage; R = the competing rule reading the "
            "corrected key rejects. F = founder, R1 = run 1, R2 = run 2.", "",
            "| Case | Original id | Level | Stratum | v1.4 key (code / liable / remedy) | F | R1 | R2 | Adjudicated label | Outcome | "
            "Disagreements with the v1.4 key | Differences from the adjudicated label | Adjudication |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    abbrev = {GT_ERROR: "GT", POLICY: "P", EVIDENCE: "EA", SLIP: "S", LEAKAGE: "L", READING: "R"}
    short = {"founder": "F", "run1": "R1", "run2": "R2"}
    for aid in rows_with:
        k = kc[aid]
        ch = KEY_CHANGES.get(aid)
        outcome = ("ground-truth error (case, every level)" if ch and ch["class"] == GT_ERROR
                   else "evidence ambiguity (this level)" if ch else "key stands (liable party and remedy)")
        dis = [f"{short[w]}: {abbrev[LABELLER_JUDGEMENTS[(aid, w)][0]]}" for w, _, _ in LABELLERS
               if (aid, w) in LABELLER_JUDGEMENTS and LABELLER_JUDGEMENTS[(aid, w)][0]]
        dif = [f"{short[w]}: {abbrev[LABELLER_JUDGEMENTS[(aid, w)][1]]}" for w, _, _ in LABELLERS
               if (aid, w) in LABELLER_JUDGEMENTS and LABELLER_JUDGEMENTS[(aid, w)][1]]
        out.append(f"| {aid} | {k['case_id']} | {k['level']} | {k['stratum']} | {fmt(k['ground_truth'])} | "
                   f"{fmt_row(labels['founder'].get(aid))} | {fmt_row(labels['run1'].get(aid))} | {fmt_row(labels['run2'].get(aid))} | "
                   f"{fmt(ac[aid]['ground_truth'])} | {outcome} | {'; '.join(dis) or 'none'} | {'; '.join(dif) or 'none'} | "
                   f"{CASE_NOTES[aid].replace('|', '/')} |")

    out += ["", "### Each labeller's judgement", "",
            "| Case | Labeller | Label | Class (vs the v1.4 key) | Cause (vs the adjudicated label) | Note |", "|---|---|---|---|---|---|"]
    for aid in rows_with:
        for who, _, disp in LABELLERS:
            j = LABELLER_JUDGEMENTS.get((aid, who))
            if j:
                out.append(f"| {aid} | {disp} | {fmt_row(labels[who].get(aid))} | {j[0] or 'agrees'} | {j[1] or 'matches'} | {j[2].replace('|', '/')} |")

    out += ["", "## Counts", "",
            "Disagreements with the v1.4 key (labeller-case pairs; a pair differs on liable party, remedy or both):", "",
            "| Class | " + " | ".join(names[w] for w, _, _ in LABELLERS) + " | All |", "|---|" + "---|" * (len(LABELLERS) + 1)]
    for cls in CLASSES:
        vals = [c["by_class"][w][cls] for w, _, _ in LABELLERS]
        out.append(f"| {cls} | " + " | ".join(str(v) for v in vals) + f" | {sum(vals)} |")
    tot = [sum(c["by_class"][w].values()) for w, _, _ in LABELLERS]
    out.append("| all | " + " | ".join(str(v) for v in tot) + f" | {sum(tot)} |")
    out += ["", "Differences from the adjudicated label, by cause:", "",
            "| Cause | " + " | ".join(names[w] for w, _, _ in LABELLERS) + " | All |", "|---|" + "---|" * (len(LABELLERS) + 1)]
    for cause in CAUSES:
        vals = [c["by_cause"][w][cause] for w, _, _ in LABELLERS]
        if sum(vals):
            out.append(f"| {cause} | " + " | ".join(str(v) for v in vals) + f" | {sum(vals)} |")
    tot = [sum(c["by_cause"][w].values()) for w, _, _ in LABELLERS]
    out.append("| all | " + " | ".join(str(v) for v in tot) + f" | {sum(tot)} |")

    out += ["", "## Labeller agreement: original v1.4 key and adjudicated key", "",
            "Wilson 95% intervals over cases; Cohen's kappa beside each. Kappa on 8 cases is unstable, and a labeller with no variance "
            "on a field (the founder's remedies) has kappa 0 whatever the agreement.", "",
            "| Labeller | Cases | Liable party: v1.4 key | Kappa | Liable party: adjudicated | Kappa | Remedy: v1.4 key | Remedy: adjudicated | Both: v1.4 key | Both: adjudicated | 'undetermined' answered (liable party) |",
            "|---|---|---|---|---|---|---|---|---|---|---|"]
    founder_ids = list(labels["founder"])
    groups = [("founder", None, names["founder"]), ("run1", None, "Model run 1"), ("run2", None, "Model run 2"),
              ("run1", founder_ids, "Model run 1, on the founder's 8"), ("run2", founder_ids, "Model run 2, on the founder's 8")]
    for who, ids, disp in groups:
        a = agreement(labels[who], kc, ids=ids)
        b = agreement(labels[who], ac, ids=ids)
        n = a["liable_party"][1]
        und = sum(labels[who][x]["liable_party"] == "undetermined" for x in (ids or labels[who]) if x in labels[who])
        out.append(f"| {disp} | {n} | {pct(*a['liable_party'][:2])} | {a['liable_party'][2]:.2f} | {pct(*b['liable_party'][:2])} | "
                   f"{b['liable_party'][2]:.2f} | {pct(*a['remedy'][:2])} | {pct(*b['remedy'][:2])} | {pct(*a['both'][:2])} | "
                   f"{pct(*b['both'][:2])} | {und} |")
    out += ["", "The adjudicated key rewards 'undetermined' where the shown evidence cannot decide, so its gain for run 1 is partly "
            "built in: it is the answer run 1 gave. Run 2's lower score is not a measured inferiority either: it applied a consistent "
            "burden-of-proof reading the founder shares (8/8 agreement with him), which v1.4 does not adopt.", ""]

    out += ["## Phase 2 re-score (exploratory): the headline E0 -> E3 liable-party figures", "",
            "Stored A1 grid decisions (`results/phase2/p2v3_a1_grid.jsonl`, rulebook v1.2 as run, 51 cases per level, one decision per "
            "case and level), liable party. Wilson 95% intervals over cases. The v1.2 column is the reported headline and is not changed. "
            "The v1.4 columns count contract-invalid outputs as not correct (Audit 1 F20), as `results/phase2_summary.md` does. "
            "'D37 corrected' applies the one ground-truth error (case-level, all four levels). 'Decidable cells' removes the "
            "adjudicated kit cells whose liable party is `undetermined` at that level (" +
            ", ".join(f"{lv}: {', '.join(p2r[('claude-fable-5-1', lv)]['ea_cases']) or 'none'}" for lv in p2.LEVELS) +
            "); the A1 arbiters had no `undetermined` option (their instructions said to decide on the balance of probabilities), so "
            "those cells are dropped rather than scored as wrong, and the last column shows how often the arbiter named the v1.4 "
            "party there anyway.", "",
            "| Arbiter | Level | v1.2 labels (as reported) | v1.4 labels (Audit 1 F10) | v1.4, D37 corrected | v1.4 corrected, decidable cells | Undecidable cells: arbiter named the v1.4 party |",
            "|---|---|---|---|---|---|---|"]
    for arb in sorted({a for a, _ in p2r}):
        for lv in p2.LEVELS:
            s = p2r.get((arb, lv))
            if not s:
                continue
            out.append(f"| {arb} | {lv} | {pct(s['v12'], s['n'])} | {pct(s['v14'], s['n'])} | {pct(s['v14c'], s['n'])} | "
                       f"{pct(s['dec'], s['dec_n'])} | {s['ea']}/{s['ea_n']} |")
    out += ["", "Reading it. The v1.2 headline is untouched. The v1.4 figures that `paper/main.md` cites at E3 (45/51 and 44/51) "
            f"become {fable_e3['v14c']}/51 and {grok_e3['v14c']}/51 with D37 corrected. The decidable-cell figures are partial: "
            "only the 40 kit cells were read, and the same reading would very likely find more undecidable cells among the other "
            "E0-E2 grid cells (E0 to E2 hold no delivery evidence beyond the parties' statements). Building an evidence-conditional "
            "key for all 204 grid cells needs the same case-by-case reading, ideally by independent labellers; it is not done here. "
            "The A2 hybrid and A3 quorum (E3 only) and the capture arm are not re-scored: no E3 kit cell is undecidable, the capture "
            "cells change only a remedy (XBEEA7), and A2 cannot be scored under v1.4 without new calls (Audit 1 F10).", ""]

    out += ["## Observations on cases no labeller disputed", "",
            "- **Capture triplets, never-said branch: the agent's log reveals the requirement (construction defect).** The four "
            "branch-c cases share their source's agent trace (Audit 1 F10: 'the 12 capture triplets share one agent trace per source'). "
            "In D33-c (kit XC55AA, E3) the log reason reads 'White is not available; black is the closest match', and in D34-c (kit "
            "XBEEA7, E2) the agent searches 'MacBook Air 15 M5 laptop' and writes 'No MacBook Air under EUR 900', though in both the "
            "conversation never states the requirement. D32-c and D35-c carry no such tell. Both model runs kept buyer (the founder did not label these cases); a careful "
            "labeller could instead infer a requirement given outside the produced conversation (AG1-C, with ABS-E1 against the "
            "provider). Labels are kept; the defect is a threat to the validity of the capture arm's 48/48 on two of its four "
            "branch-c cases and "
            "joins the counterbalancing plan of Audit 1 F24 (render each branch's trace from that branch).",
            "- **XEBE30 (D25, E1) is kept.** It is the only E0/E1 kit cell whose liability every labeller and the key share. The "
            "hard-limit breach is shown, both parties say the agent placed the order, and nothing shown raises a merchant step "
            "(contrast X0E516, where the disputed lines are merchant add-on services).",
            "- **X7A280 (D44, E2) is kept.** Custom goods (engraved 'Anna') are excluded from withdrawal whatever the date, so 'deny' "
            "does not need the delivery date.", ""]

    out += ["## Inputs to the standard (policy disagreements)", "",
            "1. **Injected merchant-hosted content.** On the two kit cases where the log shows the agent obeying an instruction on the "
            "merchant's page (X40DAA, XBEBFB), all four labels that differ from the key put the loss on the agent provider (the founder "
            f"and run 2 on X40DAA; both runs on XBEBFB): {topics[INJECTION]} classed as policy disagreements, run 1's as a probable slip. "
            "v1.4 puts it on the merchant (AG4 before AG1-P), on the ground that a participating merchant "
            "answers for what it hosts. The rule is the author's; the disagreement is substantive and should go to independent experts "
            "and to the standard's apportionment rules.",
            "2. **Burden of proof when a merchant answers with its own record only.** The founder and run 2 decide non-conformity and "
            "non-delivery claims for the buyer when the merchant offers only its packing record (card-scheme practice for goods not "
            f"received); v1.4 sends them to review. This reading accounts for {topics[BURDEN]} of the {n_diff} differences from the "
            f"adjudicated key ({topics_by['founder'][BURDEN]} of the founder's {n_diff_by['founder']}, {topics_by['run2'][BURDEN]} of "
            f"run 2's {n_diff_by['run2']}).",
            f"3. **Withdrawal dates.** v1.4 treats a missing delivery date as unresolved even when every date consistent with the record "
            "gives the same answer (XDFF82: dispute 11 days after the order). A bound (delivery on or after the order, before the "
            "dispute) would settle such cases without the date.",
            "4. **Referential terms in signed text.** 'My usual printer ink' (D37) binds under v1.4 only if a reference to an "
            "unstated product counts as a term; the corrected key says it does. The standard's A4.1 Step 3 examples are all explicit "
            "attributes; a sentence on references ('my usual', 'the same as last time') would remove the doubt. The founder ruled on "
            "2026-11-04 that the reference binds (addendum); the standard's wording is not changed by that ruling.", ""]

    out += ["## Limits", "",
            "- The adjudicator is the author side. The cases, the rulebook, the key, this adjudication and the code are one lane's work. "
            "The founder's rulings of 2026-11-04 (addendum) are the author's too.",
            "- Post hoc: every label and record had been seen. The evidence-conditional definition was chosen while reading the "
            "disagreements, and it is the definition run 1 happened to follow.",
            "- n = 8 author-labelled cases and two model runs, one from a family under test, labelling in batch mode with cross-case "
            "leakage. None of this is the independent expert baseline Amendment 11 calls for, which remains open.",
            "- The Phase 2 re-score covers only the adjudicated kit cells; the arbiters were instructed under v1.2, so every v1.4 "
            "column measures the distance from the current rule, not arbiter error.", ""]

    out += ["## Addendum, 2026-11-04: the founder's rulings", "",
            "Written after everything above. Nothing above is changed by it except the notes that point here, and no historical "
            "number is changed. The founder is the study's author, so each ruling settles the programme's rule, not the independence "
            "of a label. No model was called.", "",
            "### Ruling 1: D37, 'my usual printer ink'", "",
            "The founder confirms the adjudicated reading: the agent provider is liable (AG1-P, refund). The agent should have asked or "
            "checked which ink was 'usual'; instead it bought a common cartridge. The adjudicated key records the ruling in the case's "
            "`adjudication.ruling`. Its labels, and every number above, are unchanged by it, because the key already applied this "
            "reading. The contrary reading (AG2: an under-specified wish the agent was not told to ask about) stays on record for "
            "independent labellers.", ""]
    out += ruling2_section(labels, adj)
    return "\n".join(out) + "\n"


def ruling2_section(labels: dict, adj: dict) -> list[str]:
    """Addendum, ruling 2: rulebook v1.5 (ABS-V1) as implemented, and the exploratory re-score of the kit, Phase 2 and Phase 3."""
    ac = adj["cases"]
    eur = lambda v: f"EUR {v:,.2f}".replace(".00", "")
    rows = {t: br.kit(ac, t) for t in br.SENSITIVITY}
    keys = {t: {aid: {"ground_truth": r["label"]} for aid, r in rows[t].items()} for t in br.SENSITIVITY}
    p2s = {t: br.phase2(ac, t) for t in br.SENSITIVITY}
    d = br.DEFAULT_THRESHOLD
    kd = rows[d]
    scope = [aid for aid, r in kd.items() if r["cell"]["in_scope"]]
    ch = br.changed(kd)
    burden_pairs = [(a, w) for (a, w), j in LABELLER_JUDGEMENTS.items() if j[1] == POLICY and POLICY_TOPICS[(a, w)] == BURDEN]
    resolved = lambda t: [(a, w) for a, w in burden_pairs if not differs(labels[w][a], keys[t][a]["ground_truth"])]
    names = {who: disp for who, _, disp in LABELLERS}
    cellname = lambda aid: f"{aid} ({ac[aid]['case_id']}, {ac[aid]['level']}, {eur(kd[aid]['cell']['order_value'])})"
    out = ["### Ruling 2: a tiered burden of proof for merchant-performance claims (rulebook v1.5, ABS-V1)", "",
           "**The rule as implemented.** Rulebook v1.5 (`rulebook/AGENTIC_DISPUTE_RULEBOOK_v1.5.md`, section 2a, and `.json`) is "
           "v1.4 plus one rule, stated normatively in ABS v0.3 A5.7 and applied in A4.1 Step 1; the engine applies it with "
           "`decide(..., rulebook=\"1.5\")` (tests: `tests/test_burden_tier.py`). A claim of non-delivery or non-conformity, and "
           "nothing else, that no record with independent authority for the contested fact decides (the merchant answered only with "
           "its own packing record, photos, listing or statements, and no carrier scan or weight, registry, inspection or tied "
           "certified capture supports either side) is decided by the order value. At or below the published threshold (default "
           "EUR 100 per order, per currency, inclusive), with the buyer under the cap (default 3 ABS-V1 refunds per buyer identity "
           "in 12 months, counted by the payer's PSP), the merchant refunds (AG3). Above the threshold or the cap, or with the "
           "order value or the count missing, the case goes to human review or an independent inspection, as under v1.4. It never "
           "overrides Step 0 and never applies to an agent-instruction, capture or Step 2 dispute, or to a claim that also alleges "
           "one; a record with independent authority for either side decides as before. The residual risk is bounded: fabricated "
           "claims cost at most the threshold times the cap per buyer identity per year (EUR 300 with the defaults), more for a "
           "person with several identities or PSPs whose counts are not shared. The defaults are a design proposal; nothing about "
           "the rule has been evaluated.", "",
           "**How the re-score was done.** Exploratory, post hoc, author-side; no model call. `acs/burden_rescore.py` applies ABS-V1 "
           "to each stored cell (one case at one evidence level): the scope is read from the claim text by the engine's own reader "
           "(on the 63 stored cases it selects exactly the 16 merchant-performance cases, D01-D13 and D45-D47); every record with "
           "independent authority in the package built for that level is cited for the merchant on the contested fact and read by "
           "the engine's gate v3 readers; the order value is the case's transaction amount (all EUR). No stored case carries a buyer "
           "history, so every buyer counts zero earlier ABS-V1 refunds and the cap never binds in these data. Where ABS-V1 applies "
           "the label becomes AG3 / merchant / refund; elsewhere the v1.4 label stands. Nothing above this addendum is changed.", "",
           f"**Expert kit, default EUR 100.** {len(scope)} of 40 kit cells are in scope; ABS-V1 applies to {len(ch)}: "
           + ", ".join(cellname(a) for a in ch) + f". All {len(ch)} change one way, from `review / undetermined / undetermined` to "
           "`AG3 / merchant / refund`, all at E0 to E2 and all in cases whose simulated facts are AG3 (the merchant did fail). The "
           "other in-scope cells keep their label: above EUR 100 ("
           + ", ".join(cellname(a) for a in scope if a not in ch and kd[a]["cell"]["tier"] == "high_value")
           + ") or with a record with independent authority for the merchant ("
           + (", ".join(cellname(a) for a in scope if a not in ch and kd[a]["cell"]["tier"] != "high_value") or "none") + "). "
           "No out-of-scope cell changes, and no label moves away from the merchant.", "",
           "| Labeller | Cases | Liable party: adjudicated v1.4 | Liable party: v1.5 | Remedy: adjudicated v1.4 | Remedy: v1.5 | Both: adjudicated v1.4 | Both: v1.5 |",
           "|---|---|---|---|---|---|---|---|"]
    founder_ids = list(labels["founder"])
    for who, ids, disp in (("founder", None, names["founder"]), ("run1", None, "Model run 1"), ("run2", None, "Model run 2"),
                           ("run1", founder_ids, "Model run 1, on the founder's 8"), ("run2", founder_ids, "Model run 2, on the founder's 8")):
        a = agreement(labels[who], ac, ids=ids)
        b = agreement(labels[who], keys[d], ids=ids)
        out.append(f"| {disp} | {a['liable_party'][1]} | {pct(*a['liable_party'][:2])} | {pct(*b['liable_party'][:2])} | "
                   f"{pct(*a['remedy'][:2])} | {pct(*b['remedy'][:2])} | {pct(*a['both'][:2])} | {pct(*b['both'][:2])} |")
    res = resolved(d)
    rest = [(a, w) for a, w in burden_pairs if (a, w) not in res]
    match = lambda w, a, key: not differs(labels[w][a], key[a]["ground_truth"])
    gains = {w: [a for a in labels[w] if a in ch and match(w, a, keys[d]) and not match(w, a, ac) and (a, w) not in res] for w in labels}
    losses = {w: [a for a in labels[w] if a in ch and match(w, a, ac) and not match(w, a, keys[d])] for w in labels}
    lp = {w: (agreement(labels[w], ac)["liable_party"][0], agreement(labels[w], keys[d])["liable_party"][0]) for w in labels}
    n_und = sum(1 for k in ac.values() if k["ground_truth"]["liable_party"] == "undetermined")
    change = lambda w: (f"rises by {lp[w][1] - lp[w][0]}" if lp[w][1] > lp[w][0] else f"falls by {lp[w][0] - lp[w][1]}" if lp[w][1] < lp[w][0] else "is unchanged")
    why_rest = lambda a: (f"above EUR 100 ({eur(kd[a]['cell']['order_value'])})" if kd[a]["cell"]["in_scope"]
                          else {"XADFD6": "outside the scope: a fee line, AG1-M", "XC217F": "outside the scope: an Allowance term, AG1-P"}.get(a, "outside the scope"))
    out += ["", f"**The burden-view differences.** Of the {len(burden_pairs)} differences from the adjudicated key that came from the "
            f"burden reading, v1.5 at EUR 100 resolves {len(res)}: " + ", ".join(f"{a} ({names[w].split(' (')[0].lower()})" for a, w in res) +
            f". The other {len(rest)} remain: " + "; ".join(f"{a} ({names[w].split(' (')[0].lower()}), {why_rest(a)}" for a, w in rest) +
            ". The founder's labels applied the view at any value (X608BC is a EUR 1,399 laptop); the ruled rule applies it below the "
            "threshold only. Other labels that now match: " + ("; ".join(f"{names[w].split(' (')[0].lower()} on " + ", ".join(gains[w])
                                                                 for w in ("founder", "run1", "run2") if gains[w]) or "none") +
            ". Labels that no longer match: " + ("; ".join(f"{names[w].split(' (')[0].lower()} on " + ", ".join(losses[w]) + " (`undetermined`, which ABS-V1 now decides)"
                                                      for w in ("founder", "run1", "run2") if losses[w]) or "none") + ".", "",
            "**Sensitivity to the threshold (the cap never binds here).** 'None' applies ABS-V1 at any order value, as the founder's "
            "labels did. Kit agreement is liable party.", "",
            "| Threshold | Kit labels changed (all to AG3 / merchant / refund) | Founder | Model run 1 | Model run 2 | Burden-view differences resolved | Phase 2 simulated-facts cells changed |",
            "|---|---|---|---|---|---|---|"]
    for t in br.SENSITIVITY:
        cht = br.changed(rows[t])
        moves = sorted({(o, n) for _, _, o, n in p2s[t]["changes"]})
        out.append(f"| {br.threshold_label(t)} | {len(cht)} | " + " | ".join(pct(*agreement(labels[w], keys[t])["liable_party"][:2]) for w in ("founder", "run1", "run2")) +
                   f" | {len(resolved(t))} of {len(burden_pairs)} | {len(p2s[t]['changes'])}" +
                   (f" ({', '.join(f'{o} -> {n}' for o, n in moves)}: " + ", ".join(sorted({c for c, _, _, _ in p2s[t]['changes']})) + " at E0 to E2)" if moves else "") + " |")
    pd = p2s[d]
    low = sorted({cid for (cid, _), c in pd["cells"].items() if c["applies"]})
    out += ["", f"**Phase 2 A1 grid (51 cases x 4 levels, default EUR 100).** ABS-V1 applies to {len(pd['applies'])} cells, the four "
            f"low-value merchant-performance cases ({', '.join(low)}) at every level, and changes {len(pd['changes'])} simulated-facts "
            "labels: all four are AG3 in fact, and the case set holds no low-value false merchant-performance claim (the three "
            "fabricated not-as-described claims, D45-D47, are EUR 329 to 1,399). So the v1.5 column equals the v1.4 corrected column. "
            "On the evidence-conditional basis, ABS-V1 decides one adjudicated undecidable cell per level at E0 to E2, and both "
            "arbiters had named the merchant there.", "",
            "| Arbiter | Level | v1.4, D37 corrected | v1.5, simulated facts | v1.4 corrected, decidable cells | v1.5, decidable cells | Cells ABS-V1 decides: arbiter named the merchant |",
            "|---|---|---|---|---|---|---|"]
    for arb in sorted({a for a, _ in pd["by"]}):
        for lv in p2.LEVELS:
            x = pd["by"].get((arb, lv))
            if x:
                out.append(f"| {arb} | {lv} | {pct(x['v14c'], x['n'])} | {pct(x['v15'], x['n'])} | {pct(x['dec14'], x['dec14_n'])} | "
                           f"{pct(x['dec15'], x['dec15_n'])} | {x['newly_right']}/{len(x['newly'])}" + (f" ({', '.join(x['newly'])})" if x["newly"] else "") + " |")
    pn = p2s[br.NO_THRESHOLD]["by"]
    out += ["", "Without a threshold, the nine cells of D45-D47 at E0 to E2 (fabricated claims, buyer liable in fact) become the "
            "merchant's: the loss the threshold and the cap exist to bound. At E3 the registry or the inspection supports the merchant "
            "and nothing changes. Against those labels the stored A1 decisions score, E0 to E2, " +
            "; ".join(f"{arb} " + ", ".join(f"{pn[(arb, lv)]['v14c']} -> {pn[(arb, lv)]['v15']}" for lv in ("E0", "E1", "E2"))
                      for arb in sorted({a for a, _ in pn})) + " of 51 (a measure of the distance from that rule, not arbiter error).", ""]
    s3 = br.phase3_sides(d)
    m_low = [cid for cid, c in s3["merchant"].items() if c["applies"]]
    m_high = [cid for cid, c in s3["merchant"].items() if not c["applies"]]
    b_scope = [cid for cid, c in s3["buyer"].items() if c["in_scope"]]
    b_out = [cid for cid, c in s3["buyer"].items() if not c["in_scope"]]
    vals = lambda ids, side: f"{eur(min(s3[side][c]['order_value'] for c in ids))} to {eur(max(s3[side][c]['order_value'] for c in ids))}"
    out += [f"**Phase 3 case-sides (E3, default EUR 100).** Merchant side: {len(m_low)} of 7 ({', '.join(m_low)}; {vals(m_low, 'merchant')}) are "
            "low-value claims no independent record decides for the merchant, so ABS-V1 decides them for the buyer, the true allocation, "
            "whatever the merchant's optimised submissions say; " + f"{', '.join(m_high)} are above EUR 100 ({vals(m_high, 'merchant')}). "
            f"Buyer side: none of the 7 fabrications is paid: {', '.join(b_scope)} are above EUR 100 ({vals(b_scope, 'buyer')}) and a registry or "
            f"inspection record supports the merchant at E3; {', '.join(b_out)} allege authorisation or injection, outside the scope.", "",
            f"**Reading it.** At EUR 100, ABS-V1 decides {len(ch)} of the kit's {n_und} cells whose liable party the shown evidence cannot "
            f"settle, all for the buyer in cases where the merchant did fail, and settles {len(res)} of the {len(burden_pairs)} burden-view "
            f"differences; liable-party agreement {change('founder')} for the founder, {change('run2')} for run 2 and {change('run1')} "
            f"for run 1. It changes {'no' if not pd['changes'] else len(pd['changes'])} simulated-facts label{'' if len(pd['changes']) == 1 else 's'} "
            "in Phase 2, because no stored case is a low-value false merchant-performance claim: the fabrication loss the cap bounds is "
            "not exercised by these data. Measuring it needs low-value fabricated claims, buyer histories and loss data; none exists here.", "",
            "**Limits of the re-score.** The founder, who ruled, is the study's author, and the re-score is the author side's, written "
            "after every label and record had been seen. The scope reader is keyword-based (a claim that names the agent is out of "
            "scope, found on capture case D32-c while preparing this); the gate v3 readers have no reader for some content; the cap "
            "never binds; 40 kit cells and 204 grid cells; no model has been run under v1.5.", ""]
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--key-out", default=ADJ_KEY_PATH)
    ap.add_argument("--out", default=REPORT_PATH)
    args = ap.parse_args(argv)
    original_sha = sha256_file(KEY_PATH)
    key = load_key()
    labels = load_labels()
    adj = build_adjudicated_key(key, original_sha)
    problems = judgement_problems(key["cases"], labels, adj["cases"])
    if problems:
        print("Adjudication data inconsistent:\n  " + "\n  ".join(problems), file=sys.stderr)
        return 1
    p2r = rescore_phase2(adj["cases"])
    text = report(key, labels, adj, p2r)
    with open(args.key_out, "w", encoding="utf-8") as fh:
        json.dump(adj, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(text)
    if sha256_file(KEY_PATH) != original_sha:  # never expected: this module does not open the original for writing
        print("expert/answer_key.json changed during the run", file=sys.stderr)
        return 1
    print(args.out)
    print(args.key_out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

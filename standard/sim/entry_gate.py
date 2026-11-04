"""Scammer entry routes and the Register entry gate (roadmap family).

For each entry route the gate chain is evaluated in order: onboarding KYB, shared blocklist,
probation (PSP payout hold or rolling reserve, volume caps), continuous monitoring, per-purchase
re-attestation. The first gate that detects the route stops it; if none does before a loss, the
route is "open". Maximum loss before detection is computed per rail family from stated assumptions
(not measured): ticket = the scenario amount; probation 90 days with a volume cap of 50 orders;
non-delivery monitoring fires after 5 undelivered orders; catalogue/MCC drift fires after 20
orders; prepaid-velocity alarm fires when prepaid orders exceed 3x the (seasonal) baseline, taken
as 30 orders; rolling reserve 10% for 180 days. Honest routes report whether they pass and at what
cost. The programme does not claim to keep every scammer out (Audit 0); residual paths are listed.
"""

from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
from rails import RAILS  # noqa: E402

GATES = ["onboarding_kyb", "shared_blocklist", "probation_hold_or_reserve", "volume_caps", "continuous_monitoring", "per_purchase_reattestation"]
PROBATION_ORDER_CAP = 50
NONDELIVERY_DETECT_ORDERS = 5
DRIFT_DETECT_ORDERS = 20
VELOCITY_DETECT_ORDERS = 30
RESERVE_PCT = 0.10

# route -> which gate detects (None = none), orders before detection when it passes entry,
# whether a payout hold during probation covers the loss, classification, proposed fix.
ROUTES = {
    "synthetic_identity": {"detected_by": "onboarding_kyb", "orders_before_detection": 0, "hold_covers": True, "classification": "closed",
                           "how": "registry check, beneficial-owner verification, payout account in the entity's name",
                           "fix": "none needed beyond KYB; keep LEI/registry lookups live"},
    "stolen_business_identity": {"detected_by": "onboarding_kyb", "orders_before_detection": 0, "hold_covers": True, "classification": "closed",
                                 "how": "payout-name mismatch and domain-ownership check against the real entity", "fix": "notify the impersonated business; blocklist the payout account"},
    "shell_nominee": {"detected_by": "continuous_monitoring", "orders_before_detection": NONDELIVERY_DETECT_ORDERS, "hold_covers": True, "classification": "limits_loss",
                      "how": "KYB passes (clean paperwork); non-delivery monitoring fires after the first undelivered orders; probation hold covers them",
                      "fix": "probation payout hold on every new entity; beneficial-owner liveness check; cap prepaid volume in probation"},
    "payout_name_mismatch": {"detected_by": "onboarding_kyb", "orders_before_detection": 0, "hold_covers": True, "classification": "closed",
                             "how": "payout account name must match the legal entity (or a verified PSP settlement account)", "fix": "none"},
    "domain_brand_impersonation": {"detected_by": "onboarding_kyb", "orders_before_detection": 0, "hold_covers": True, "classification": "closed",
                                   "how": "brand-similarity screen on domain and catalogue; domain age; blocklist of protected marks", "fix": "keep the mark list current; re-screen on catalogue changes"},
    "transaction_laundering": {"detected_by": "per_purchase_reattestation", "orders_before_detection": 0, "hold_covers": False, "classification": "limits_loss",
                               "how": "the injected catalogue is not signed with the legitimate merchant's registered key, so per-purchase re-attestation of the Offer Feed signature refuses it; without feed signing, catalogue/MCC drift monitoring fires after ~20 orders",
                               "fix": "mandatory Offer Feed signing; MCC/catalogue drift monitoring; the front merchant answers for records signed with its key"},
    "sleeper_exit": {"detected_by": "continuous_monitoring", "orders_before_detection": VELOCITY_DETECT_ORDERS, "hold_covers": False, "classification": "limits_loss",
                     "how": "passes every entry gate; a prepaid-order velocity alarm fires after ~30 prepaid orders above the seasonal baseline; only the rolling reserve covers part of the loss",
                     "fix": "payout hold on prepaid orders with delivery more than 14 days out for all merchants; rolling reserve sized to prepaid exposure; velocity alarm against a seasonal baseline"},
    "collusion_steering": {"detected_by": None, "orders_before_detection": None, "hold_covers": False, "classification": "open",
                           "how": "a legitimate merchant paying an agent provider for routing is invisible to KYB, holds, caps and monitoring; goods conform and arrive",
                           "fix": "incentive disclosure in the Mandate (ABS-X2); routing audits; cross-provider price-dispersion monitoring; joint liability (ABS-X1); still not a gate"},
    "expelled_reentry": {"detected_by": "shared_blocklist", "orders_before_detection": 0, "hold_covers": True, "classification": "closed_if_blocklist_shared",
                         "how": "beneficial owner, payout account, device and domain fingerprints match an expelled record; open if the blocklist is per-platform",
                         "fix": "shared cross-programme blocklist (as card schemes keep for terminated merchants); fingerprint beyond the company name"},
    "honest_micro": {"detected_by": None, "orders_before_detection": None, "hold_covers": True, "classification": "honest_passes_with_probation_cost",
                     "how": "passes KYB; probation payout hold (delivery + 7 days), 50-order cap, re-attestation per purchase", "fix": "shorten probation on clean delivery history; cap, not refuse"},
    "honest_seasonal": {"detected_by": None, "orders_before_detection": None, "hold_covers": True, "classification": "honest_passes_false_alarm_risk",
                        "how": "volume spike after dormancy resembles the sleeper exit pattern; a seasonal baseline avoids the alarm; otherwise a temporary reserve increase, not a block",
                        "fix": "seasonal baseline from prior years; reserve increase instead of suspension"},
    "honest_entity_change": {"detected_by": None, "orders_before_detection": None, "hold_covers": True, "classification": "honest_passes_with_short_hold",
                             "how": "KYB re-run with continuity evidence (same beneficial owner, successor filing); payout hold for a few days during verification", "fix": "continuity fast-path"},
}


def max_loss_before_detection(route: dict, ticket: float, rail: str, with_hold: bool) -> dict:
    """Buyer-side and system-side loss before the detecting gate fires, per rail."""
    fam = RAILS[rail]["family"]
    reversible = RAILS[rail]["reversible"]
    n = route["orders_before_detection"]
    if n is None:
        exposure = None
    else:
        exposure = min(n, PROBATION_ORDER_CAP) * ticket
    out = {"rail_family": fam, "orders_before_detection": n, "exposure": exposure, "buyer_loss": None, "system_loss": None, "covered_by": None}
    if exposure is None:
        out.update({"buyer_loss": "unbounded (route open; conforming goods at inflated price)" if route["classification"] == "open" else 0.0,
                    "system_loss": "unbounded" if route["classification"] == "open" else 0.0, "covered_by": None})
        return out
    if exposure == 0:
        out.update({"buyer_loss": 0.0, "system_loss": 0.0, "covered_by": "stopped at entry"})
        return out
    if with_hold and route["hold_covers"]:
        if fam in ("a2a_push", "crypto", "stored_value"):
            out.update({"buyer_loss": 0.0, "system_loss": 0.0, "covered_by": "payee-PSP hold during probation: only in the A2A acquiring model (PSP is payee); in the merchant-account model no hold exists and the no-hold column applies"})
        else:
            out.update({"buyer_loss": 0.0, "system_loss": 0.0, "covered_by": "acquirer/operator payout hold during probation"})
        return out
    if with_hold and not route["hold_covers"]:
        covered = exposure * RESERVE_PCT
        rest = exposure - covered
        if reversible:
            out.update({"buyer_loss": 0.0, "system_loss": round(rest, 2), "covered_by": f"reserve {int(RESERVE_PCT*100)}% + rail reversal (loss to acquirer/operator)"})
        else:
            out.update({"buyer_loss": round(rest, 2), "system_loss": 0.0, "covered_by": f"reserve {int(RESERVE_PCT*100)}% only; rest unrecoverable on an irrevocable rail"})
        return out
    if reversible:
        out.update({"buyer_loss": 0.0, "system_loss": round(exposure, 2), "covered_by": "rail reversal (chargeback/operator); loss to acquirer/operator"})
    else:
        out.update({"buyer_loss": round(exposure, 2), "system_loss": 0.0, "covered_by": "nothing: irrevocable rail, no hold"})
    return out


def run(scenarios: list[dict]) -> dict:
    rows = []
    for s in scenarios:
        route = s["facts"].get("entry_route")
        if not route:
            continue
        r = ROUTES[route]
        ticket = s["facts"]["amount"]
        rows.append({"scenario_id": s["id"], "route": route, "rail": s["rail"], "rail_family": s["rail_family"], "detected_by": r["detected_by"],
                     "classification": r["classification"], "how": r["how"], "fix": r["fix"],
                     "loss_without_hold": max_loss_before_detection(r, ticket, s["rail"], False),
                     "loss_with_hold": max_loss_before_detection(r, ticket, s["rail"], True)})
    table = []
    for route, r in ROUTES.items():
        mine = [x for x in rows if x["route"] == route]
        table.append({"route": route, "detected_by": r["detected_by"] or "none", "classification": r["classification"], "how": r["how"], "fix": r["fix"],
                      "scenarios": [x["scenario_id"] for x in mine],
                      "loss_without_hold_by_rail": {x["rail"]: x["loss_without_hold"]["buyer_loss"] for x in mine},
                      "loss_with_hold_by_rail": {x["rail"]: x["loss_with_hold"]["buyer_loss"] for x in mine}})
    return {"rows": rows, "table": table,
            "closed": [t["route"] for t in table if t["classification"].startswith("closed")],
            "limits_loss": [t["route"] for t in table if t["classification"] == "limits_loss"],
            "open": [t["route"] for t in table if t["classification"] == "open"],
            "honest": [t["route"] for t in table if t["classification"].startswith("honest")]}

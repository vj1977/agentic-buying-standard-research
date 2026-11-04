#!/usr/bin/env python3
"""Build the Appendix F example instances for ABS v0.3 with real body_hash / envelope_hash values
(JCS approximated by sorted-key compact JSON, exact for these ASCII, integer/short-decimal bodies).
Signatures are illustrative. Writes the captioned Markdown blocks to stdout, or to --out PATH.

Moved from the session scratchpad into the repository for Audit 3 finding F15. It used to write
appendix_f_examples.md next to the script; it now writes nothing unless --out is given, and never
edits standard/ itself: pasting the output into Appendix F is a deliberate, reviewed step.
Usage: python3 -m tools.schema_check.gen_examples [--out PATH]"""
import argparse, base64, hashlib, json, sys

def jcs(o):
    return json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def h(o):
    return "sha256:" + hashlib.sha256(jcs(o).encode()).hexdigest()

def hx(label):
    return "sha256:" + hashlib.sha256(label.encode()).hexdigest()

def b64(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()

def sig(role, party, kid, at, env_hash):
    hdr = b64(jcs({"alg": "Ed25519", "kid": kid}).encode())
    fake = hashlib.sha512((role + party + kid + at + env_hash).encode()).digest()  # 64 bytes, NOT a signature
    return {"role": role, "party_id": party, "kid": kid, "alg": "Ed25519", "sig": hdr + ".." + b64(fake), "signed_at": at}

def envelope(typ, id_, created, body, signers, chain=None, prev=None):
    bh = h(body)
    ctx = {"ctx": "ABS-ENVELOPE", "abs_version": "0.3", "type": typ, "id": id_, "created_at": created,
           "chain_id": chain["chain_id"] if chain else None, "seq": chain["seq"] if chain else None,
           "prev_hash": prev, "body_hash": bh}
    eh = h(ctx)
    env = {"abs_version": "0.3", "type": typ, "id": id_, "created_at": created}
    if chain:
        env["chain"] = chain
    if prev:
        env["prev_hash"] = prev
    env.update({"body": body, "body_hash": bh, "envelope_hash": eh,
                "signatures": [sig(r, p, k, created, eh) for r, p, k in signers]})
    return env

MID = "urn:abs:mandate:7c1e2a40-5b6d-4e8f-9a0b-1c2d3e4f5a6b"
mandate_body = {
    "mandate_id": MID,
    "allowance_policy_id": "urn:abs:allowance-policy:0b9d8e7f-6a5b-4c3d-8e1f-2a3b4c5d6e7f",
    "allowance_policy_hash": hx("example allowance policy"),
    "user_ref": "u-5f2c91",
    "agent_provider": {"party_id": "prov-acme-agents", "role": "agent_provider"},
    "agent_id": "acme-shopper@4.2",
    "intent_hash": hx("Buy me one pair of Sony WH-1000XM6 headphones, new, not refurbished, cheapest from a reputable shop, under EUR 350."),
    "proposed_by": "agent",
    "conversation_hash": hx("example conversation record"),
    "template_profile": {"id": "abs:profile:electronics", "version": "0.3", "prompted_attributes": ["model_identifier", "condition", "colour"], "left_open": ["colour"]},
    "user_confirmation": {"confirmed_at": "2026-11-04T09:12:30Z", "shown_terms_hash": hx("example shown terms")},
    "max_total": {"amount": "350.00", "currency": "EUR"},
    "max_units": 1,
    "condition_allowed": ["new"],
    "item_requirements": [
        {"name": "model_identifier", "value": "WH-1000XM6", "binding": True, "verification_method": "label_read"},
        {"name": "condition", "value": "new", "binding": True, "verification_method": "visual_match"}],
    "ask_on_ambiguity": True,
    "valid_from": "2026-11-04T09:12:30Z", "expires_at": "2026-11-11T09:12:30Z",
    "autonomy_required": "approval_required",
    "authentication": {"method": "sca_app", "performed_at": "2026-11-04T09:12:29Z", "reference": "psp-auth-88123", "assurance": "psd2_sca"},
    "rulebook_version": "abs-liability@0.3",
    "nonce": "n-3f9a1c2e4d5b6a70",
}
ENV_M = "urn:abs:mandate:7c1e2a40-5b6d-4e8f-9a0b-1c2d3e4f5a6b"
mandate_env = envelope("Mandate", ENV_M, "2026-11-04T09:12:31Z", mandate_body,
                       [("user", "u-5f2c91", "user-key-1"), ("agent_provider", "prov-acme-agents", "prov-key-3")],
                       chain={"chain_id": ENV_M, "seq": 0})

refusal_body = {
    "refusal_id": "urn:abs:refusal-record:1d2c3b4a-5e6f-4a7b-8c9d-0e1f2a3b4c5d",
    "mandate_id": MID, "refused_at": "2026-11-04T09:20:02Z",
    "offers_compared": [{"snapshot_id": "snap-b-0001", "offer_hash": hx("example offer B"), "merchant": {"party_id": "m-reboxed", "role": "merchant"}}],
    "reason_code": "no_conforming_offer",
    "reason": {"text": "Offer B is refurbished; the Mandate allows new only.", "class": "untrusted_text"},
}
refusal_env = envelope("RefusalRecord", "urn:abs:refusal-record:1d2c3b4a-5e6f-4a7b-8c9d-0e1f2a3b4c5d", "2026-11-04T09:20:03Z",
                       refusal_body, [("agent_provider", "prov-acme-agents", "prov-key-3")],
                       chain={"chain_id": ENV_M, "seq": 1}, prev=mandate_env["envelope_hash"])

finding_body = {
    "finding_id": "urn:abs:finding:9e8d7c6b-5a4f-4e3d-9c2b-1a0f9e8d7c6b",
    "case_id": "urn:abs:dispute-case:2a3b4c5d-6e7f-4a8b-9c0d-1e2f3a4b5c6d",
    "node_id": "node-eu-1",
    "finder": {"kind": "verifier", "id": "abs-verifier@0.3.0"},
    "type": "offer_conformity",
    "subject": {"line": 1, "field": "model_identifier", "party": "merchant"},
    "value": "non_conforming",
    "confidence": 1,
    "cited_evidence": [{
        "item_id": "registry-record-sony-eu-0001",
        "path": "/units/0/model_identifier",
        "hash": hx("example registry binding record"),
        "record_type": "serial_lookup",
        "provenance": {
            "issuer": {"role": "registry", "party_id": "reg-sony-eu"},
            "stake": "none",
            "committed": {"at": "2026-11-05T16:40:00Z", "relative_to_dispute": "before", "proof": "issuer_signed"},
            "custody": {"held_by": "registry", "integrity": "issuer_signature_verified"},
            "authority_for": ["unit_identity", "unit_sale_history"],
            "signature_verified": True},
        "fact": "unit_identity",
        "attribute": "model_identifier",
        "support": "supports",
        "support_check": "deterministic"}],
    "corroborated": True,
    "corroboration_basis": "independent_authority",
    "deterministic": True,
    "produced_at": "2026-11-20T10:00:00Z",
}
finding_env = envelope("Finding", "urn:abs:finding:9e8d7c6b-5a4f-4e3d-9c2b-1a0f9e8d7c6b", "2026-11-20T10:00:01Z",
                       finding_body, [("arbiter", "node-eu-1", "node-eu-1-key-2")])

purchase_env_hash = hx("example purchase record envelope")
settlement_body = {
    "settlement_id": "urn:abs:settlement-instruction:3c4d5e6f-7a8b-4c9d-8e0f-1a2b3c4d5e6f",
    "purchase_id": "urn:abs:purchase:4d5e6f7a-8b9c-4d0e-9f1a-2b3c4d5e6f7a",
    "purchase_hash": purchase_env_hash,
    "instruction_seq": 1, "direction": "pay",
    "amount": {"amount": "329.00", "currency": "EUR"},
    "payer": {"party_role": "user", "instrument_ref": "tok-agent-77"},
    "payee": {"party_role": "merchant", "account_ref": "acq-merchant-a"},
    "rail": {"type": "card", "network": "visa"},
    "abs_binding": {
        "reference_field": "additional_data",
        "reference_value": "ABS:urn:abs:purchase:4d5e6f7a-8b9c-4d0e-9f1a-2b3c4d5e6f7a:" + purchase_env_hash[7:23],
        "anchor_commitment": {"head": purchase_env_hash, "store": "psp_record", "store_ref": "psp-pay-2026-11-04-000731",
                              "committed_at": "2026-11-04T09:31:07Z"}},
    "timing": {"mode": "immediate"},
}

examples = [
    {"example": "F.1", "schema": "urn:abs:schema:0.3:envelope", "expect": "valid",
     "why": "Mandate at the genesis of a purchase chain (seq 0, no prev_hash); proposed by the agent, so conversation_hash and template_profile are present; signed by user and agent provider",
     "instance": mandate_env},
    {"example": "F.2", "schema": "urn:abs:schema:0.3:envelope", "expect": "valid",
     "why": "RefusalRecord as the next event of the same chain: seq 1, prev_hash = envelope_hash of F.1",
     "instance": refusal_env},
    {"example": "F.3", "schema": "urn:abs:schema:0.3:envelope", "expect": "valid",
     "why": "Finding outside any chain, with one citation that carries a provenance description and meets test (a) of A5.7",
     "instance": finding_env},
    {"example": "F.4", "schema": "urn:abs:schema:0.3:settlement-instruction", "expect": "valid",
     "why": "Settlement Instruction body: the full head is in anchor_commitment; the rail reference carries only the 16-hex locator",
     "instance": settlement_body},
    {"example": "F.5", "schema": "urn:abs:schema:0.3:envelope", "expect": "invalid", "base": "F.1",
     "patch": [{"op": "replace", "path": "/abs_version", "value": "0.2"}],
     "why": "the v0.3 envelope accepts only abs_version 0.3; a v0.2 object goes to the v0.2 schemas under the version policy (A5.3)"},
    {"example": "F.6", "schema": "urn:abs:schema:0.3:envelope", "expect": "invalid", "base": "F.2",
     "patch": [{"op": "replace", "path": "/type", "value": "Mandate"}],
     "why": "type-to-body dispatch: a RefusalRecord body under type Mandate fails the Mandate schema"},
    {"example": "F.7", "schema": "urn:abs:schema:0.3:envelope", "expect": "invalid", "base": "F.2",
     "patch": [{"op": "remove", "path": "/prev_hash"}],
     "why": "a chain event with seq 1 must carry prev_hash (binding to the A5.8 chain)"},
    {"example": "F.8", "schema": "urn:abs:schema:0.3:envelope", "expect": "invalid", "base": "F.1",
     "patch": [{"op": "add", "path": "/note", "value": "unsigned remark"}],
     "why": "no envelope field may sit outside the authenticated context: unknown envelope fields are rejected"},
    {"example": "F.9", "schema": "urn:abs:schema:0.3:mandate", "expect": "invalid", "base": "F.1",
     "select": "/body", "patch": [{"op": "remove", "path": "/conversation_hash"}],
     "why": "a Mandate proposed by the agent must record the conversation it was proposed from (capture provenance, A4.1 Step 3b)"},
    {"example": "F.10", "schema": "urn:abs:schema:0.3:finding", "expect": "invalid", "base": "F.3",
     "select": "/body", "patch": [{"op": "remove", "path": "/cited_evidence/0/provenance"},
                                  {"op": "add", "path": "/cited_evidence/0/provenance_tier", "value": "independent"}],
     "why": "the binary v0.2 label is gone: a citation must carry the provenance description"},
    {"example": "F.11", "schema": "urn:abs:schema:0.3:settlement-instruction", "expect": "invalid", "base": "F.4",
     "patch": [{"op": "remove", "path": "/abs_binding/anchor_commitment"}],
     "why": "the 16-hex locator alone is not a commitment: anchor_commitment with the full head is required"},
    {"example": "F.12", "schema": "urn:abs:schema:0.3:settlement-instruction", "expect": "invalid", "base": "F.4",
     "patch": [{"op": "replace", "path": "/abs_binding/anchor_commitment/head", "value": "sha256:" + purchase_env_hash[7:23]}],
     "why": "a truncated hash is never a commitment: Hash requires all 64 hex characters"},
]

def pp(o, depth, maxdepth, ind=""):
    if depth >= maxdepth or not isinstance(o, dict) or not o:
        return json.dumps(o, ensure_ascii=False)
    inner = ind + "  "
    items = [inner + json.dumps(k) + ": " + pp(v, depth + 1, maxdepth, inner) for k, v in o.items()]
    return "{\n" + ",\n".join(items) + "\n" + ind + "}"

def block(e):
    e = {k: v for k, v in e.items() if k != "why"}
    md = 3 if "instance" in e and "body" in e.get("instance", {}) else 2
    return "```json\n" + pp(e, 0, md) + "\n```\n"

def render():
    out = []
    for e in examples:
        out.append(f"**{e['example']}** ({e['expect']} against `{e['schema']}`{', ' + 'patch of ' + e['base'] if 'base' in e else ''}). {e['why'][0].upper() + e['why'][1:]}.\n")
        out.append(block(e))
    return "\n".join(out)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", help="write the Markdown here instead of stdout")
    args = ap.parse_args()
    md = render()
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"{len(examples)} examples written to {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(md)

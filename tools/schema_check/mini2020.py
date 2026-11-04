#!/usr/bin/env python3
"""Minimal JSON Schema draft 2020-12 subset validator (no dependencies), written for the ABS
schemas. Supported: type, enum, const, required, properties, additionalProperties (bool or schema),
items (single schema), minItems, maxItems, minLength, maxLength, pattern, minimum, maximum,
format (date-time, date, uri; asserted), $ref (absolute URN with optional JSON Pointer fragment,
or local '#/...'), with sibling keywords applied, allOf, anyOf, oneOf, not, if/then/else.
Annotations ignored: $schema, $id, $defs, description, default, examples, title.
Any other keyword raises, so the subset is never silently exceeded.

Moved from the session scratchpad into the repository for Audit 3 finding F15 (subset validator
outside the repository); the document-level run is `python3 -m tools.schema_check FILE`."""
import copy, hashlib, json, re

SUPPORTED = {"type", "enum", "const", "required", "properties", "additionalProperties", "items", "minItems",
             "maxItems", "minLength", "maxLength", "pattern", "minimum", "maximum", "format", "$ref", "allOf",
             "anyOf", "oneOf", "not", "if", "then", "else"}
ANNOT = {"$schema", "$id", "$defs", "description", "default", "examples", "title"}
TYPES = {"object", "array", "string", "boolean", "null", "integer", "number"}
FORMATS = {"date-time", "date", "uri"}  # asserted; any other format value is outside the subset
DIALECT = "https://json-schema.org/draft/2020-12/schema"

RFC3339 = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
URI = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:\S+$")

class SchemaError(Exception):
    pass

def is_type(v, t):
    if t == "object": return isinstance(v, dict)
    if t == "array": return isinstance(v, list)
    if t == "string": return isinstance(v, str)
    if t == "boolean": return isinstance(v, bool)
    if t == "null": return v is None
    if t == "integer": return (isinstance(v, int) and not isinstance(v, bool)) or (isinstance(v, float) and v.is_integer())
    if t == "number": return isinstance(v, (int, float)) and not isinstance(v, bool)
    raise SchemaError("unknown type " + str(t))

def json_equal(a, b):
    """JSON equality for enum/const: true is not 1, 1 equals 1.0 (Python's == conflates bool and int)."""
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a == b
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(json_equal(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(json_equal(a[k], b[k]) for k in a)
    return type(a) is type(b) and a == b

def ptr(doc, frag):
    cur = doc
    for part in [p for p in frag.split("/") if p]:
        part = part.replace("~1", "/").replace("~0", "~")
        try:
            cur = cur[int(part)] if isinstance(cur, list) else cur[part]
        except (KeyError, IndexError, ValueError, TypeError):
            raise SchemaError(f"JSON Pointer {frag!r} does not resolve") from None
    return cur

class Validator:
    def __init__(self, schemas):
        self.schemas = schemas
        self.used = set()

    def resolve(self, ref, base):
        b, _, frag = ref.partition("#")
        doc_id = b or base
        if doc_id not in self.schemas:
            raise SchemaError("unresolved $ref " + ref)
        return ptr(self.schemas[doc_id], frag) if frag else self.schemas[doc_id], doc_id

    def errors(self, inst, sch, base, path="$"):
        if sch is True: return []
        if sch is False: return [f"{path}: false schema"]
        if not isinstance(sch, dict):
            raise SchemaError(f"schema at {path} is {type(sch).__name__}, not an object or boolean")
        unknown = set(sch) - SUPPORTED - ANNOT
        if unknown:
            raise SchemaError(f"unsupported keyword(s) {sorted(unknown)} at {path}")
        if "format" in sch and sch["format"] not in FORMATS:
            raise SchemaError(f"unsupported format {sch['format']!r} at {path}")
        self.used |= set(sch) & SUPPORTED
        errs = []
        if "$ref" in sch:
            target, nb = self.resolve(sch["$ref"], base)
            errs += self.errors(inst, target, nb, path)
        if "type" in sch:
            ts = sch["type"] if isinstance(sch["type"], list) else [sch["type"]]
            if not any(is_type(inst, t) for t in ts):
                return errs + [f"{path}: type {type(inst).__name__} not in {ts}"]
        if "enum" in sch and not any(json_equal(inst, e) for e in sch["enum"]):
            errs.append(f"{path}: {inst!r} not in enum")
        if "const" in sch and not json_equal(inst, sch["const"]):
            errs.append(f"{path}: {inst!r} != const {sch['const']!r}")
        if isinstance(inst, str):
            if "minLength" in sch and len(inst) < sch["minLength"]: errs.append(f"{path}: shorter than {sch['minLength']}")
            if "maxLength" in sch and len(inst) > sch["maxLength"]: errs.append(f"{path}: longer than {sch['maxLength']}")
            if "pattern" in sch and not re.search(sch["pattern"], inst): errs.append(f"{path}: does not match {sch['pattern']}")
            f = sch.get("format")
            if f == "date-time" and not RFC3339.match(inst): errs.append(f"{path}: not date-time")
            if f == "date" and not DATE.match(inst): errs.append(f"{path}: not date")
            if f == "uri" and not URI.match(inst): errs.append(f"{path}: not uri")
        if is_type(inst, "number"):
            if "minimum" in sch and inst < sch["minimum"]: errs.append(f"{path}: below minimum {sch['minimum']}")
            if "maximum" in sch and inst > sch["maximum"]: errs.append(f"{path}: above maximum {sch['maximum']}")
        if isinstance(inst, list):
            if "minItems" in sch and len(inst) < sch["minItems"]: errs.append(f"{path}: fewer than {sch['minItems']} items")
            if "maxItems" in sch and len(inst) > sch["maxItems"]: errs.append(f"{path}: more than {sch['maxItems']} items")
            if "items" in sch:
                for i, v in enumerate(inst):
                    errs += self.errors(v, sch["items"], base, f"{path}[{i}]")
        if isinstance(inst, dict):
            for r in sch.get("required", []):
                if r not in inst: errs.append(f"{path}: missing required {r!r}")
            props = sch.get("properties", {})
            for k, v in inst.items():
                if k in props:
                    errs += self.errors(v, props[k], base, f"{path}.{k}")
                elif "additionalProperties" in sch:
                    ap = sch["additionalProperties"]
                    if ap is False: errs.append(f"{path}: unknown field {k!r}")
                    elif isinstance(ap, dict): errs += self.errors(v, ap, base, f"{path}.{k}")
        for s in sch.get("allOf", []):
            errs += self.errors(inst, s, base, path)
        if "anyOf" in sch and not any(not self.errors(inst, s, base, path) for s in sch["anyOf"]):
            errs.append(f"{path}: matches none of anyOf")
        if "oneOf" in sch:
            n = sum(1 for s in sch["oneOf"] if not self.errors(inst, s, base, path))
            if n != 1: errs.append(f"{path}: matches {n} of oneOf")
        if "not" in sch and not self.errors(inst, sch["not"], base, path):
            errs.append(f"{path}: matches a 'not' schema")
        if "if" in sch:
            if not self.errors(inst, sch["if"], base, path):
                if "then" in sch: errs += self.errors(inst, sch["then"], base, path)
            elif "else" in sch:
                errs += self.errors(inst, sch["else"], base, path)
        return errs

    def validate(self, inst, schema_id):
        return self.errors(inst, self.schemas[schema_id], schema_id)

def apply_patch(doc, ops):
    doc = copy.deepcopy(doc)
    for op in ops:
        parts = [p.replace("~1", "/").replace("~0", "~") for p in op["path"].split("/")[1:]]
        parent = doc
        for p in parts[:-1]:
            parent = parent[int(p)] if isinstance(parent, list) else parent[p]
        last = parts[-1]
        if isinstance(parent, list):
            last = int(last)
        if op["op"] == "remove":
            del parent[last]
        elif op["op"] in ("add", "replace"):
            if op["op"] == "replace" and (last not in parent if isinstance(parent, dict) else last >= len(parent)):
                raise ValueError("replace of absent " + op["path"])
            parent[last] = op["value"]
        else:
            raise ValueError("unsupported op " + op["op"])
    return doc

def static_checks(schemas):
    """required keys must be declared where additionalProperties is false (else unsatisfiable)"""
    probs = []
    def walk(s, where):
        if isinstance(s, dict):
            if s.get("additionalProperties") is False and "required" in s:
                for r in s["required"]:
                    if r not in s.get("properties", {}):
                        probs.append(f"{where}: required {r!r} not in properties (additionalProperties false)")
            for k, v in s.items():
                if k in ("properties", "$defs"):
                    for kk, vv in v.items():
                        walk(vv, f"{where}/{k}/{kk}")
                elif isinstance(v, (dict, list)):
                    walk(v, f"{where}/{k}")
        elif isinstance(s, list):
            for i, v in enumerate(s):
                walk(v, f"{where}/{i}")
    for sid, s in schemas.items():
        walk(s, sid)
    return probs

def subset_scan(schemas):
    """Static keyword scan of every schema node (formerly inline in this script's __main__): the subset
    must cover everything the schemas use. Returns (nodes scanned, problems). Beyond unknown keywords it
    also rejects what the validator would otherwise mis-read: a non-schema where a schema is expected
    (e.g. draft-4 tuple `items`), an unknown `type` name or `format`, an uncompilable `pattern`, a nested
    `$id` (base-URI change the resolver ignores) and a `$schema` other than draft 2020-12."""
    probs, count = [], [0]
    def scan(s, where, root):
        if isinstance(s, bool):
            return
        if not isinstance(s, dict):
            probs.append(f"{where}: schema is {type(s).__name__}, not an object or boolean"); return
        count[0] += 1
        unknown = set(s) - SUPPORTED - ANNOT
        if unknown:
            probs.append(f"{where}: unsupported keyword(s) {sorted(unknown)}")
        if "$id" in s and not root:
            probs.append(f"{where}: nested $id is outside the subset")
        if "$schema" in s and (not root or s["$schema"] != DIALECT):
            probs.append(f"{where}: $schema {s['$schema']!r} is not a root draft 2020-12 declaration")
        if "type" in s:
            ts = s["type"] if isinstance(s["type"], list) else [s["type"]]
            bad = [t for t in ts if t not in TYPES]
            if bad:
                probs.append(f"{where}: unknown type(s) {bad}")
        if "format" in s and s["format"] not in FORMATS:
            probs.append(f"{where}: unsupported format {s['format']!r}")
        if "pattern" in s:
            try:
                re.compile(s["pattern"])
            except (re.error, TypeError) as e:
                probs.append(f"{where}: pattern does not compile: {e}")
        for k in ("properties", "$defs"):
            if k in s:
                if not isinstance(s[k], dict):
                    probs.append(f"{where}/{k}: not an object of schemas"); continue
                for kk, vv in s[k].items():
                    scan(vv, f"{where}/{k}/{kk}", False)
        for k in ("additionalProperties", "items", "not", "if", "then", "else"):
            if k in s:
                scan(s[k], f"{where}/{k}", False)
        for k in ("allOf", "anyOf", "oneOf"):
            if k in s:
                if not isinstance(s[k], list) or not s[k]:
                    probs.append(f"{where}/{k}: not a non-empty array of schemas"); continue
                for i, vv in enumerate(s[k]):
                    scan(vv, f"{where}/{k}/{i}", False)
    for sid, s in schemas.items():
        scan(s, sid, True)
    return count[0], probs

def jcs(o): return json.dumps(o, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
def sha(o): return "sha256:" + hashlib.sha256(jcs(o).encode()).hexdigest()

def envelope_checks(schemas, examples, v, env_id="urn:abs:schema:0.3:envelope"):
    """Envelope examples (formerly inline in __main__): recompute body_hash and envelope_hash, check chain
    links, validate the rebuilt SignedContext and every SignatureInput against their $defs (A5.3); and
    for Settlement Instructions, the rail locator is the 16-hex prefix of the committed full head.
    `examples` maps example name -> example object. Returns [(name, what, problems)]."""
    out = []
    envs = {n: e["instance"] for n, e in examples.items()
            if e.get("schema") == env_id and e.get("expect") == "valid" and "instance" in e}
    by_hash = {i.get("envelope_hash"): i for i in envs.values()}
    for n, i in envs.items():
        probs = []
        try:
            ctx = {"ctx": "ABS-ENVELOPE", "abs_version": i["abs_version"], "type": i["type"], "id": i["id"], "created_at": i["created_at"],
                   "chain_id": i.get("chain", {}).get("chain_id"), "seq": i.get("chain", {}).get("seq"), "prev_hash": i.get("prev_hash"), "body_hash": sha(i["body"])}
            if ctx["body_hash"] != i["body_hash"]: probs.append("body_hash mismatch")
            if sha(ctx) != i["envelope_hash"]: probs.append("envelope_hash mismatch")
            probs += v.errors(ctx, schemas[env_id]["$defs"]["SignedContext"], env_id, "ctx")
            for s in i["signatures"]:
                si = {"envelope_hash": i["envelope_hash"], "role": s["role"], "party_id": s["party_id"], "kid": s["kid"], "signed_at": s["signed_at"]}
                probs += v.errors(si, schemas[env_id]["$defs"]["SignatureInput"], env_id, "sig")
            if "prev_hash" in i:
                prev = by_hash.get(i["prev_hash"])
                if not prev or prev.get("chain", {}).get("chain_id") != i["chain"]["chain_id"] or prev["chain"]["seq"] != i["chain"]["seq"] - 1:
                    probs.append("prev_hash does not link to the previous event of the chain")
        except (KeyError, TypeError, SchemaError) as e:
            probs.append(f"cannot rebuild the signed context: {type(e).__name__} {e}")
        out.append((n, "hashes, context and chain link", probs))
    for n, e in examples.items():
        if e.get("expect") == "valid" and isinstance(e.get("instance"), dict) and "abs_binding" in e["instance"]:
            b = e["instance"]["abs_binding"]
            try:
                ok = b["reference_value"].endswith(":" + b["anchor_commitment"]["head"][7:23])
            except (KeyError, TypeError):
                ok = False
            out.append((n, "locator is the 16-hex prefix of the committed full head",
                        [] if ok else ["reference_value does not end with the 16-hex prefix of anchor_commitment.head"]))
    return out

def self_tests():
    sch = {"x": {"$id": "x", "type": "object", "required": ["a"], "additionalProperties": False,
                 "properties": {"a": {"type": "integer", "minimum": 1}, "b": {"$ref": "#/$defs/H"}},
                 "allOf": [{"if": {"required": ["b"]}, "then": {"required": ["a"]}}],
                 "$defs": {"H": {"type": "string", "pattern": "^h:[0-9]{2}$"}}}}
    v = Validator(sch)
    cases = [({"a": 1}, True), ({"a": 0}, False), ({}, False), ({"a": 1, "c": 1}, False), ({"a": 1, "b": "h:12"}, True),
             ({"a": 1, "b": "h:1"}, False), ({"a": True}, False), ({"a": 1.0}, True)]
    bad = [(i, ok) for i, ok in cases if (not v.validate(i, "x")) != ok]
    return len(cases), bad

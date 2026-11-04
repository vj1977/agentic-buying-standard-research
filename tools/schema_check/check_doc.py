#!/usr/bin/env python3
"""Document checks for ABS: JSON blocks parse, $refs resolve, section cross-references
resolve, Mermaid blocks balanced, no stray placeholders. Usage: check_doc.py FILE [FILE...]

Moved from the session scratchpad into the repository for Audit 3 finding F15; run it as
`python3 -m tools.schema_check.check_doc FILE`. The schema/example run (`python3 -m tools.schema_check`)
reuses parse_json() and check_refs(); the prose checks (cross-references, Mermaid, placeholders) run
only from this module's own entry point."""
import json, re, sys

def blocks(text, lang):
    out = []
    for m in re.finditer(r"^[ ]{0,3}```" + lang + r"[ \t]*\n(.*?)^[ ]{0,3}```", text, re.S | re.M):
        line = text[: m.start()].count("\n") + 1
        out.append((line, m.group(1)))
    return out

def headings(text):
    secs = set()
    for m in re.finditer(r"^#{1,4} (.+)$", text, re.M):
        h = m.group(1)
        mm = re.match(r"([AB]\d+(?:\.\d+)*)\.? ", h)
        if mm:
            secs.add(mm.group(1))
        mm = re.match(r"Appendix ([A-Z])\.", h)
        if mm:
            secs.add("Appendix " + mm.group(1))
        mm = re.match(r"([A-Z])\.(\d+) ", h)
        if mm:
            secs.add(mm.group(1) + "." + mm.group(2))
    return secs

def section_items(text, sec):
    """numbered list items directly under heading `sec` (until next heading)"""
    m = re.search(r"^#{2,4} " + re.escape(sec) + r"\.? .*$", text, re.M)
    if not m:
        return set()
    rest = text[m.end():]
    n = re.search(r"^#{1,4} ", rest, re.M)
    body = rest[: n.start()] if n else rest
    return {int(x) for x in re.findall(r"^(\d+)[a-z]?\. ", body, re.M)}

def resolve_pointer(doc, ptr):
    cur = doc
    for part in [p for p in ptr.split("/") if p]:
        part = part.replace("~1", "/").replace("~0", "~")
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        elif isinstance(cur, list) and part.isdigit() and int(part) < len(cur):
            cur = cur[int(part)]
        else:
            return None
    return cur

def walk_refs(node, path=""):
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "$ref" and isinstance(v, str):
                yield path, v
            else:
                yield from walk_refs(v, path + "/" + k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk_refs(v, path + "/" + str(i))

def parse_json(text):
    """Parse every ```json block. Returns (errors, parsed [(line, obj)], schemas {$id: obj},
    schema_lines {$id: line}, others [(line, obj)] = blocks without a top-level $id)."""
    errs, parsed, schemas, schema_lines, others = [], [], {}, {}, []
    for line, b in blocks(text, "json"):
        try:
            d = json.loads(b)
        except Exception as e:
            errs.append(f"json block at line {line} does not parse: {e}")
            continue
        parsed.append((line, d))
        if isinstance(d, dict) and "$id" in d:
            if d["$id"] in schemas:
                errs.append(f"duplicate $id {d['$id']} at line {line}")
            schemas[d["$id"]] = d
            schema_lines[d["$id"]] = line
        else:
            others.append((line, d))
    return errs, parsed, schemas, schema_lines, others

def check_refs(schemas):
    """Every $ref names a known schema and its JSON Pointer resolves. Returns (errors, refs checked)."""
    errs, nrefs = [], 0
    for sid, s in schemas.items():
        for p, ref in walk_refs(s):
            nrefs += 1
            base, _, frag = ref.partition("#")
            target = s if base == "" else schemas.get(base)
            if target is None:
                errs.append(f"{sid}{p}: $ref {ref} -> unknown schema")
                continue
            if frag and resolve_pointer(target, frag) is None:
                errs.append(f"{sid}{p}: $ref {ref} -> pointer does not resolve")
    return errs, nrefs

def check(fn):
    text = open(fn, encoding="utf-8").read()
    errs, info = [], []
    # JSON blocks
    perrs, parsed, schemas, _, examples = parse_json(text)
    errs += perrs
    info.append(f"json blocks: {len(parsed)} parsed ({len(schemas)} schemas with $id, {len(examples)} other)")
    # $ref resolution
    rerrs, nrefs = check_refs(schemas)
    errs += rerrs
    info.append(f"$refs checked: {nrefs}")
    # schema versions consistent
    vers = {re.match(r"urn:abs:schema:([0-9.]+):", k).group(1) for k in schemas if k.startswith("urn:abs:schema:")}
    info.append(f"schema $id versions: {sorted(vers)}")
    # cross references
    secs = headings(text)
    refs = set(re.findall(r"(?<![\w.-])([AB]\d+(?:\.\d+)*)(?![\w])", text))
    refs = {r.rstrip(".") for r in refs}
    missing = sorted(r for r in refs if r not in secs and not re.fullmatch(r"[AB]\d+", r) or (re.fullmatch(r"[AB]\d+", r) and r not in secs))
    # single-letter-number tokens such as A1/A2/A3 (arbiter designs) resolve to sections anyway
    for r in missing:
        errs.append(f"cross-reference {r} has no heading")
    for m in re.finditer(r"Appendix ([A-Z])\b", text):
        if "Appendix " + m.group(1) not in secs:
            errs.append(f"Appendix {m.group(1)} referenced but absent")
    item_refs = re.findall(r"([AB]\d+(?:\.\d+)*),? items? (\d+)(?: (?:and|to) (\d+))?", text)
    for sec, a, b in item_refs:
        items = section_items(text, sec)
        for n in [a] + ([b] if b else []):
            if int(n) not in items:
                errs.append(f"{sec} item {n} referenced but not in the numbered list")
    info.append(f"section refs checked: {len(refs)}; item refs: {len(item_refs)}")
    # mermaid
    mb = blocks(text, "mermaid")
    for line, b in mb:
        depth = 0
        for ln in b.splitlines():
            w = ln.strip().split(" ", 1)[0] if ln.strip() else ""
            if w in ("alt", "opt", "par", "rect", "loop", "critical", "break"):
                depth += 1
            elif w == "end":
                depth -= 1
                if depth < 0:
                    errs.append(f"mermaid at line {line}: unmatched end")
        if depth != 0:
            errs.append(f"mermaid at line {line}: {depth} unclosed block(s)")
    info.append(f"mermaid blocks: {len(mb)}")
    # placeholders
    for pat in [r"\[CHECK", r"\[RESULT", r"\bTODO\b", r"\bTBD\b", r"\bFIXME\b", r"\bXXX\b", r"(?<!\")Pending \(Phase", r"\[TK\]", r"lorem"]:
        for m in re.finditer(pat, text, re.I if pat == "lorem" else 0):
            ln = text[: m.start()].count("\n") + 1
            errs.append(f"placeholder {pat} at line {ln}")
    # unbalanced code fences
    if text.count("```") % 2:
        errs.append("odd number of code fences")
    return errs, info, schemas, examples

if __name__ == "__main__":
    bad = 0
    for fn in sys.argv[1:]:
        errs, info, _, _ = check(fn)
        print(f"== {fn}")
        for i in info:
            print("  " + i)
        for e in errs:
            print("  ERROR " + e)
        print(f"  {len(errs)} error(s)")
        bad += len(errs)
    sys.exit(1 if bad else 0)

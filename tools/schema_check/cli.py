"""Check the JSON embedded in an ABS standard document (Audit 3, finding F15).

    python3 -m tools.schema_check standard/ABS_v0.3.md

1. Every ```json block parses; schema $ids are unique.
2. Every embedded schema (a block with a top-level $id) uses only the draft 2020-12 subset that
   mini2020 implements (any other keyword, format or shape is an error, never skipped), every $ref
   resolves, and no required member is excluded by additionalProperties false.
3. Appendix F: every block is an example object; its bold caption ("**F.n** (valid|invalid against
   `schema`[, patch of F.m])") agrees with the block's example/expect/schema/base. Positive examples
   (expect "valid") must validate. Negative examples (expect "invalid") are JSON Patches of a positive
   example (`base`, `select` first picks a sub-document) and must fail; and, as the stated reason is the
   difference the patch makes, the unpatched base (after `select`) must itself validate against the
   negative example's schema, so the failure is caused by the patch alone. The errors are printed for
   comparison with the caption.
4. Envelope integrity of the positive envelope examples (hashes, signed context, chain link) and the
   Settlement locator, as recomputed by mini2020.envelope_checks.
Prints a summary with counts and exits 1 on any failure (2 if a file cannot be read)."""
import argparse, re, sys

from .check_doc import blocks, check_refs, parse_json
from .mini2020 import (SchemaError, Validator, apply_patch, envelope_checks, ptr, self_tests, static_checks,
                       subset_scan)

CAPTION = re.compile(r"\*\*(?P<name>F\.\d+)\*\* \((?P<expect>valid|invalid) against `(?P<schema>[^`]+)`"
                     r"(?:, patch of (?P<base>F\.\d+))?\)")
APPENDIX_F = re.compile(r"^#{1,2} Appendix F\b", re.M)

def _appendix_f_span(text):
    """(first line, last line) of Appendix F, or None."""
    m = APPENDIX_F.search(text)
    if not m:
        return None
    start = text[: m.start()].count("\n") + 1
    n = re.search(r"^#{1,2} ", text[m.end():], re.M)
    end = text[: m.end() + n.start()].count("\n") if n else text.count("\n") + 1
    return start, end

def _caption(lines, fence_line, floor):
    """The caption in the prose between the previous code fence (or `floor`) and the block at fence_line."""
    i, window = fence_line - 2, []
    while i >= floor and not lines[i].lstrip().startswith("```"):
        window.append(lines[i])
        i -= 1
    return CAPTION.search(" ".join(reversed(window)))

def run(path):
    """Run every check on one document. Returns a dict of counts, `failures` and printable `lines`."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    lines_out, failures = [], []
    def fail(msg):
        failures.append(msg)
        lines_out.append("FAIL " + msg)

    n_st, bad_st = self_tests()
    for case in bad_st:
        fail(f"validator self-test {case}")
    lines_out.append(f"validator self-tests: {n_st - len(bad_st)}/{n_st} passed")

    # 1. parse
    n_blocks = len(blocks(text, "json"))
    perrs, parsed, schemas, schema_lines, others = parse_json(text)
    for e in perrs:
        fail(e)
    examples = [(ln, d) for ln, d in others if isinstance(d, dict) and "example" in d]
    n_other = len(others) - len(examples)

    # 2. schemas
    nodes, scan_probs = 0, []
    for sid, s in schemas.items():
        n, probs = subset_scan({sid: s})
        nodes += n
        scan_probs += probs
        for p in probs:
            fail(f"schema subset (block at line {schema_lines[sid]}): {p}")
    rerrs, nrefs = check_refs(schemas)
    for e in rerrs:
        fail(f"$ref: {e}")
    sprobs = static_checks(schemas)
    for p in sprobs:
        fail(f"static: {p}")
    lines_out.append(f"json blocks: {n_blocks} found, {len(parsed)} parsed ({len(schemas)} schemas, "
                     f"{len(examples)} examples, {n_other} other)")
    lines_out.append(f"schemas: {len(schemas)}; nodes scanned {nodes}, {len(scan_probs)} outside the subset; "
                     f"$refs {nrefs} checked, {len(rerrs)} unresolved; {len(sprobs)} unsatisfiable required")

    # 3. Appendix F
    span = _appendix_f_span(text)
    src = text.splitlines()
    if span is None:
        fail("no 'Appendix F' heading: no example instances to check")
    else:
        for ln, d in parsed:
            if span[0] < ln <= span[1] and not (isinstance(d, dict) and "example" in d):
                fail(f"Appendix F block at line {ln} is not an example object (no 'example' member)")
    by_name, v = {}, Validator(schemas)
    for ln, e in examples:
        if e["example"] in by_name:
            fail(f"{e['example']} (line {ln}): duplicate example name")
        by_name[e["example"]] = e
    if not examples:
        fail("no example instances found: nothing was validated")
    pos = neg = pos_ok = neg_ok = 0
    for ln, e in examples:
        name, expect, sid = e["example"], e.get("expect"), e.get("schema")
        tag = f"{name} (line {ln})"
        if span is not None and span[0] < ln <= span[1]:
            cap = _caption(src, ln, span[0])
            if cap is None:
                fail(f"{tag}: no caption '**{name}** (valid|invalid against `schema`...)' before the block")
            else:
                want = {"name": name, "expect": expect, "schema": sid, "base": e.get("base")}
                diff = {k: (cap.group(k), want[k]) for k in want if cap.group(k) != want[k]}
                if diff:
                    fail(f"{tag}: caption and block disagree (caption, block): {diff}")
        if expect not in ("valid", "invalid"):
            fail(f"{tag}: expect is {expect!r}, not 'valid' or 'invalid'"); continue
        if sid not in schemas:
            fail(f"{tag}: schema {sid!r} is not an embedded $id"); continue
        try:
            if expect == "valid":
                pos += 1
                if "instance" not in e or "base" in e:
                    fail(f"{tag}: a positive example carries a full 'instance' and no 'base'"); continue
                errs = v.validate(e["instance"], sid)
                if errs:
                    fail(f"{tag}: expected valid against {sid}, got invalid -> {errs[:5]}"); continue
                pos_ok += 1
                lines_out.append(f"PASS {tag}: valid against {sid}")
                continue
            neg += 1
            note = "no base: the cause of the failure is not isolated"
            if "base" in e:
                b = by_name.get(e["base"])
                if b is None or b.get("expect") != "valid" or "instance" not in b:
                    fail(f"{tag}: base {e['base']!r} is not a positive example with an instance"); continue
                inst = ptr(b["instance"], e["select"]) if "select" in e else b["instance"]
                base_errs = v.validate(inst, sid)
                if base_errs:
                    fail(f"{tag}: the unpatched base {e['base']}{e.get('select', '')} does not validate against "
                         f"{sid}, so the failure is not attributable to the patch -> {base_errs[:5]}"); continue
                try:
                    inst = apply_patch(inst, e.get("patch", []))
                except (KeyError, IndexError, ValueError, TypeError) as x:
                    fail(f"{tag}: patch does not apply: {type(x).__name__} {x}"); continue
                note = f"base {e['base']}{e.get('select', '')} validates, so the patch alone causes it"
            elif "instance" in e:
                inst = e["instance"]
            else:
                fail(f"{tag}: a negative example needs a 'base' and 'patch', or an 'instance'"); continue
            errs = v.validate(inst, sid)
            if not errs:
                fail(f"{tag}: expected invalid against {sid}, but it validates"); continue
            neg_ok += 1
            lines_out.append(f"PASS {tag}: invalid against {sid} as required; {note} -> {errs[:3]}")
        except SchemaError as x:
            fail(f"{tag}: schema outside the subset while validating: {x}")

    # 4. envelope integrity
    integ = envelope_checks(schemas, by_name, v)
    for n, what, probs in integ:
        if probs:
            fail(f"{n} {what}: {probs}")
        else:
            lines_out.append(f"PASS {n} {what}")

    summary = {"path": path, "json_blocks": n_blocks, "parsed": len(parsed), "schemas": len(schemas),
               "schema_nodes": nodes, "refs": nrefs, "examples": len(examples), "other_blocks": n_other,
               "positive": pos, "positive_valid": pos_ok, "negative": neg, "negative_invalid": neg_ok,
               "integrity_checks": len(integ), "self_tests": n_st, "keywords": sorted(v.used),
               "failures": failures, "lines": lines_out}
    lines_out.append(f"examples: {pos} positive ({pos_ok} validate), {neg} negative ({neg_ok} fail as required); "
                     f"integrity checks: {len(integ) - sum(1 for *_, p in integ if p)}/{len(integ)}")
    lines_out.append(f"keywords exercised by the examples: {sorted(v.used)}")
    lines_out.append("RESULT: " + ("all checks passed" if not failures else f"{len(failures)} failure(s)"))
    return summary

def main(argv=None):
    ap = argparse.ArgumentParser(prog="python3 -m tools.schema_check",
                                 description="Validate the embedded schemas and Appendix F examples of an ABS document.")
    ap.add_argument("paths", nargs="+", help="Markdown file(s), e.g. standard/ABS_v0.3.md")
    args = ap.parse_args(argv)
    bad = 0
    for p in args.paths:
        try:
            r = run(p)
        except OSError as e:
            print(f"cannot read {p}: {e}", file=sys.stderr)
            return 2
        print(f"== {p}")
        for line in r["lines"]:
            print("  " + line)
        bad += len(r["failures"])
    return 1 if bad else 0

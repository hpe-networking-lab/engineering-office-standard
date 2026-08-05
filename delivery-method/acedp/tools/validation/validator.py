#!/usr/bin/env python3
"""
ACEDP Validation Engine -- Phase 0b validator (single-instance).

Validates ONE data instance against a generated intermediate rule artifact
(<schema>.rules.json from extract_rules.py / extract_all.py). It enforces the
required-fields, field-type, and allowed-enumeration rules.

Read-only: it does not modify the instance or the approved schemas. It enforces
reference SHAPE (structured-object + required subfields) and internal
reference INTEGRITY (bare-id links resolve within the same instance), but
performs cross-document reference
resolution ONLY across a local instance set passed via --context (it never
accesses external systems), NO Mist interaction, and uses NO customer
data (sample placeholder input only).

required semantics: a required field is reported missing only when its parent
object is present but the field itself is absent. Requirements on the sub-fields
of an absent optional object do not fire (the optional object's absence is
permitted). Detecting an entirely absent container section is a known limitation
deferred to a rule-model enhancement.

Usage:
    python3 validator.py [instance.yaml] [rules.json]

Exit codes: 0 = conformant, 1 = non-conformant, 2 = usage/load error.
"""
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml --break-system-packages")

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ENFORCED = {"required", "type", "allowed", "reference_shape", "reference_integrity"}

def type_ok(expected, value):
    if expected == "string":       return isinstance(value, str)
    if expected == "integer":      return isinstance(value, int) and not isinstance(value, bool)
    if expected == "boolean":      return isinstance(value, bool)
    if expected == "date":         return isinstance(value, str) and bool(DATE_RE.match(value))
    if expected == "list":         return isinstance(value, list)
    if expected == "list[string]": return isinstance(value, list) and all(isinstance(x, str) for x in value)
    if expected == "reference":    return True  # object shape checked by the reference_shape rule
    return True  # unknown/unenforced type

def parse_segments(path):
    out = []
    for part in path.split("."):
        if part.endswith("[]"):
            out.append((part[:-2], True))
        else:
            out.append((part, False))
    return out

def resolve(path, instance):
    """Return (present_targets, missing_leaves).
    present_targets: [(location, value)] where the full parent chain is present.
    missing_leaves:  [location] where the parent is present but the leaf is absent.
    Branches whose ancestor is absent are dropped (no false 'required')."""
    segs = parse_segments(path)
    current = [("", instance)]      # (location, container value)
    present, missing = [], []
    for idx, (name, is_list) in enumerate(segs):
        last = idx == len(segs) - 1
        nxt = []
        for loc, cont in current:
            if not isinstance(cont, dict) or name not in cont:
                if last and isinstance(cont, dict):
                    missing.append(f"{loc}.{name}" if loc else name)
                continue
            child = cont[name]
            newloc = f"{loc}.{name}" if loc else name
            if last:
                present.append((newloc, child))
            elif is_list:
                if isinstance(child, list):
                    for i, el in enumerate(child):
                        nxt.append((f"{newloc}[{i}]", el))
                # non-list where a list is expected: the type rule on this path catches it
            else:
                nxt.append((newloc, child))
        current = nxt
    return present, missing

def instance_identity(inst):
    """(document_reference, primary id) of an instance, or (None, None)."""
    md = inst.get("metadata", {}) if isinstance(inst, dict) else {}
    doc = md.get("document_reference")
    idv = next((v for k, v in md.items() if k.endswith("_id")), None)
    return doc, idv

def build_context_index(instances):
    """Set of (document_reference, id) over a set of local instances."""
    idx = set()
    for inst in instances:
        doc, idv = instance_identity(inst)
        if doc is not None and idv is not None:
            idx.add((doc, idv))
    return idx

def scan_external_refs(node, path=""):
    """Yield (location, ref_document, ref_id) for every structured external
    reference object (a mapping that has both 'ref_document' and 'ref_id')."""
    if isinstance(node, dict):
        if "ref_document" in node and "ref_id" in node:
            yield (path or "<root>", node.get("ref_document"), node.get("ref_id"))
        for k, v in node.items():
            yield from scan_external_refs(v, f"{path}.{k}" if path else k)
    elif isinstance(node, list):
        for i, el in enumerate(node):
            yield from scan_external_refs(el, f"{path}[{i}]")

def collect_ids(instance, collection_path, id_field):
    """Collect the set of local ids in a target collection within one instance."""
    cur = instance
    for seg in collection_path.split("."):
        if isinstance(cur, dict) and seg in cur:
            cur = cur[seg]
        else:
            return set()
    if not isinstance(cur, list):
        return set()
    return {el[id_field] for el in cur if isinstance(el, dict) and id_field in el}

def validate(instance, ruleset, context_index=None):
    findings = []
    for rule in ruleset["rules"]:
        kind = rule["rule"]
        if kind not in ENFORCED:
            continue
        present, missing = resolve(rule["path"], instance)
        if kind == "reference_integrity":
            valid = collect_ids(instance, rule["target_collection"], rule["target_id_field"])
            for loc, value in present:
                if isinstance(value, str) and value not in valid:
                    findings.append({"location": loc, "rule": "reference_integrity", "severity": "error",
                                     "expected": f"existing {rule['target_collection']}.{rule['target_id_field']}",
                                     "actual": value,
                                     "message": f"internal reference '{loc}' -> '{value}' not found locally"})
            continue
        if kind == "required":
            for loc in missing:
                findings.append({"location": loc, "rule": "required", "severity": "error",
                                 "expected": "present", "actual": "missing",
                                 "message": f"required field '{loc}' is missing"})
        else:
            for loc, value in present:
                if value is None:
                    continue
                if kind == "type":
                    exp = rule["expected_type"]
                    if not type_ok(exp, value):
                        findings.append({"location": loc, "rule": "type", "severity": "error",
                                         "expected": exp, "actual": type(value).__name__,
                                         "message": f"'{loc}' should be {exp}"})
                elif kind == "allowed":
                    if value not in rule["allowed"]:
                        findings.append({"location": loc, "rule": "allowed", "severity": "error",
                                         "expected": rule["allowed"], "actual": value,
                                         "message": f"'{loc}' value '{value}' not in allowed set"})
                elif kind == "reference_shape":
                    if not isinstance(value, dict):
                        findings.append({"location": loc, "rule": "reference_shape", "severity": "error",
                                         "expected": "structured object", "actual": type(value).__name__,
                                         "message": f"reference '{loc}' must be a structured object "
                                                    f"(its required subfields are checked separately)"})
    if context_index is not None:
        for loc, rd, rid in scan_external_refs(instance):
            if (rd, rid) not in context_index:
                findings.append({"location": loc, "rule": "reference_integrity", "severity": "error",
                                 "expected": f"existing instance ({rd}, {rid}) in the provided set",
                                 "actual": "unresolved",
                                 "message": f"external reference '{loc}' -> ({rd}, {rid}) not found in the instance set"})
    errors = sum(1 for f in findings if f["severity"] == "error")
    return {
        "instance": ruleset.get("_instance"),
        "schema_id": ruleset.get("schema_id"),
        "schema_version": ruleset.get("schema_version"),
        "conformant": errors == 0,
        "summary": {"errors": errors, "findings": len(findings)},
        "findings": findings,
    }

def main(argv):
    here = Path(__file__).resolve().parent
    args = list(argv[1:])
    context_paths = []
    if "--context" in args:
        i = args.index("--context")
        context_paths = args[i + 1:]
        args = args[:i]
    inst_path = Path(args[0]) if len(args) > 0 else here / "sample_project_profile.yaml"
    rules_path = Path(args[1]) if len(args) > 1 else here / "Project_Profile.rules.json"
    try:
        instance = yaml.safe_load(inst_path.read_text(encoding="utf-8"))
        ruleset = json.loads(rules_path.read_text(encoding="utf-8"))
        context_index = None
        if context_paths:
            ctx = []
            for cp in context_paths:
                p = Path(cp)
                files = sorted(p.glob("*.yaml")) if p.is_dir() else [p]
                for fp in files:
                    ctx.append(yaml.safe_load(fp.read_text(encoding="utf-8")))
            context_index = build_context_index(ctx)
    except Exception as e:
        sys.stderr.write(f"load error: {e}\n"); return 2
    ruleset["_instance"] = inst_path.name
    report = validate(instance, ruleset, context_index)
    print(json.dumps(report, indent=2))
    status = "CONFORMANT" if report["conformant"] else f"NON-CONFORMANT ({report['summary']['errors']} error(s))"
    sys.stderr.write(f"{inst_path.name} vs {ruleset['schema_id']} v{ruleset['schema_version']}: {status}\n")
    return 0 if report["conformant"] else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv))

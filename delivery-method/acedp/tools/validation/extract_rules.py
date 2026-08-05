#!/usr/bin/env python3
"""
ACEDP Validation Engine -- Phase 0a pilot rule extractor.

Reads an approved ACEDP YAML schema (READ-ONLY) and emits an intermediate,
representation-neutral rule artifact (JSON) per REF-MAP-001
(Validation Rule Generation Mapping) and REF-DESIGN-001.

Pilot scope: a single schema (Project Profile, SPEC-001). It reads schema
CONSTRUCTS only. It does NOT validate any data instance, does NOT modify the
schema, does NOT contact Mist, and produces NO API payloads or configuration.
No customer data is read or written.
"""
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml --break-system-packages")

def is_field_def(node):
    """A field definition is a mapping whose 'type' is a scalar string."""
    return isinstance(node, dict) and isinstance(node.get("type"), str)

def header_value(text, label):
    m = re.search(rf'^#\s*{re.escape(label)}:\s*(\S+)', text, re.M)
    return m.group(1) if m else None

def emit_field(rules, path, node):
    t = node["type"]
    rules.append({"path": path, "rule": "type", "expected_type": t})
    if bool(node.get("required", False)):
        rules.append({"path": path, "rule": "required"})
    if "allowed" in node:
        rules.append({"path": path, "rule": "allowed", "allowed": node["allowed"]})
    if t == "reference":
        rules.append({"path": path, "rule": "reference_shape"})
        for k, v in (node.get("fields") or {}).items():
            walk(rules, f"{path}.{k}", v)
    if t == "list" and isinstance(node.get("items"), dict):
        for k, v in node["items"].items():
            walk(rules, f"{path}[].{k}", v)
    if t == "string":
        desc = node.get("description") or ""
        m = re.search(r"[Ii]nternal link to an? ([A-Za-z0-9_.]+)", desc)
        if m:
            target = m.group(1).rstrip(".")
            parts = target.split(".")
            if len(parts) >= 2:
                rules.append({"path": path, "rule": "reference_integrity",
                              "target_collection": ".".join(parts[:-1]),
                              "target_id_field": parts[-1]})

def walk(rules, path, node):
    if is_field_def(node):
        emit_field(rules, path, node)
    elif isinstance(node, dict):
        # A container section that holds a directly-required field is itself
        # required: emit a section-level required rule so its absence is flagged.
        if path and any(is_field_def(v) and v.get("required", False) for v in node.values()):
            rules.append({"path": path, "rule": "required"})
        for k, v in node.items():
            walk(rules, f"{path}.{k}" if path else k, v)
    # scalars / None are ignored (e.g. description text)

def extract(schema_path):
    text = schema_path.read_text(encoding="utf-8")
    model = yaml.safe_load(text)
    schema_version = header_value(text, "Schema Version")
    schema_id = None
    try:
        desc = model["metadata"]["document_reference"]["description"]
        m = re.search(r"(SPEC-\d+)", desc)
        schema_id = m.group(1) if m else None
    except Exception:
        pass
    rules = []
    for section, node in model.items():
        walk(rules, section, node)
    # version-awareness rule (REF-MAP-001: metadata.schema_version)
    rules.append({"path": "metadata.schema_version", "rule": "schema_version",
                  "note": "instance schema_version must match an available schema version"})
    return {
        "artifact": "acedp-intermediate-ruleset",
        "format_version": "0.1",
        "schema_id": schema_id,
        "schema_version": schema_version,
        "source": schema_path.as_posix(),
        "rule_count": len(rules),
        "rules": rules,
    }

def main(argv):
    here = Path(__file__).resolve()
    repo_root = here.parents[3]
    schema = Path(argv[1]) if len(argv) > 1 else repo_root / "acedp/schemas/Project_Profile.schema.yaml"
    out = Path(argv[2]) if len(argv) > 2 else here.parent / "Project_Profile.rules.json"
    artifact = extract(schema)
    try:
        artifact["source"] = schema.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        artifact["source"] = schema.name
    out.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
    print(f"Extracted {artifact['rule_count']} rules from {schema.name} "
          f"({artifact['schema_id']} v{artifact['schema_version']}) -> {out.name}")

if __name__ == "__main__":
    main(sys.argv)

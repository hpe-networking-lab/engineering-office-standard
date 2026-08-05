#!/usr/bin/env python3
"""
ACEDP Validation Engine -- Phase 0b: generate intermediate rule artifacts for
ALL approved schemas, reusing the Milestone 68 extractor (extract_rules.extract).

Read-only over the approved schemas. It performs NO instance validation, reads
or writes NO customer data, and never contacts Mist or produces API payloads or
configuration.
"""
import json
import sys
from pathlib import Path

from extract_rules import extract  # reuse the existing single-schema extractor

def main():
    here = Path(__file__).resolve()
    repo_root = here.parents[3]
    schema_dir = repo_root / "acedp/schemas"
    out_dir = here.parent
    schemas = sorted(schema_dir.glob("*.schema.yaml"))
    if not schemas:
        sys.exit(f"no schemas found under {schema_dir}")
    total = 0
    for sp in schemas:
        art = extract(sp)
        try:
            art["source"] = sp.resolve().relative_to(repo_root).as_posix()
        except ValueError:
            art["source"] = sp.name
        out = out_dir / sp.name.replace(".schema.yaml", ".rules.json")
        out.write_text(json.dumps(art, indent=2) + "\n", encoding="utf-8")
        print(f"{sp.name}: {art['rule_count']} rules "
              f"({art['schema_id']} v{art['schema_version']}) -> {out.name}")
        total += art["rule_count"]
    print(f"Generated {len(schemas)} rule artifacts, {total} rules total.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
ACEDP Validation Engine -- run the validator across ALL approved schemas.

For each <Schema>.rules.json it validates the matching sample placeholder
instance (sample_<schema>.yaml) and prints a per-schema result. Exit code is 0
only if every sample is conformant, else 1 (2 on a tooling error).

Read-only; no customer data; no Mist; no cross-document validation.
"""
import sys
from pathlib import Path

import validator  # reuse the single-instance validator

def main():
    here = Path(__file__).resolve().parent
    rules = sorted(here.glob("*.rules.json"))
    if not rules:
        sys.stderr.write("no rule artifacts found\n"); return 2
    all_ok = True
    for rp in rules:
        base = rp.name.replace(".rules.json", "")
        sample = here / f"sample_{base.lower()}.yaml"
        if not sample.exists():
            sys.stderr.write(f"{base}: MISSING sample {sample.name}\n"); all_ok = False; continue
        rc = validator.main(["validator.py", str(sample), str(rp)])
        if rc != 0:
            all_ok = False
    print(f"\nALL CONFORMANT: {'yes' if all_ok else 'no'}")
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())

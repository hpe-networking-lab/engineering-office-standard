# Phase 0 — Validation Tooling Completion Summary

- Document ID: REF-PHASE0DONE-001
- Status: Draft
- Version: 0.1
- Authorized By: SPEC-008 Platform Tooling and Validation (Approved 1.0; Gate A)
- Related: REF-ROADMAP-001, REF-ARCH-001, REF-DESIGN-001, REF-MAP-001, REF-PHASE0-001
- Last Updated: 2026-07-01
- Baseline Commit: d2e4a5d (Milestone 75 - Required Container Validation)

> Summary document only. It records the completion of Phase 0 validation
> tooling. It builds no new tooling, modifies no approved artifact, processes no
> customer data, and contacts no external system.

## What Was Built

A schema-driven, read-only validation engine that checks ACEDP data instances
for conformance to the approved schemas, delivered across Milestones 68–75:

- **M68** — pilot rule extractor for one schema (Project Profile) producing an
  intermediate rule artifact.
- **M69** — extraction scaled to all seven approved schemas.
- **M70** — the first validator (Project Profile), consuming a rule artifact.
- **M71** — multi-schema validation with placeholder samples for all seven.
- **M72** — reference-shape validation for structured references.
- **M73** — internal reference integrity (bare-id links within one instance).
- **M74** — cross-document external reference resolution across a local set.
- **M75** — required container/section validation (closing the absent-section gap).

Rules are generated from the approved YAML schemas (never hand-written per
schema) and tagged with the source `schema_id` and `schema_version`. Generation
is deterministic.

## Files Created / Modified

All under `acedp/tools/validation/`:

- `extract_rules.py` — single-schema rule extractor.
- `extract_all.py` — generate rule artifacts for all seven schemas.
- `<Schema>.rules.json` — seven intermediate rule artifacts (1003 rules total).
- `validator.py` — single-instance validator (+ optional `--context`).
- `validate_all.py` — run the validator across all seven schemas.
- `sample_<schema>.yaml` — seven conformant placeholder (non-customer) instances.
- `sample_set/` — a two-instance set demonstrating cross-document resolution.
- `README.md` — usage and behavior.

No approved schemas, specifications, or other approved documents were modified by
Phase 0. The repository `.gitignore` was extended (Python bytecode).

## Validation Capabilities Now Supported

- **required** — required fields, and required container/list sections (a section
  holding a directly-required field is itself required).
- **type** — string, integer, boolean, date, list, list[string], reference.
- **allowed** — enumerated values.
- **reference_shape** — structured references are objects with correctly-typed,
  present required subfields.
- **reference_integrity (internal)** — bare-id links resolve to an existing local
  id within the same instance.
- **reference_integrity (cross-document)** — structured external references
  (`ref_document` + `ref_id`) resolve within a supplied local instance set
  (`--context`); off by default.
- **version tagging** — every result records the `schema_id`/`schema_version`
  validated against.

Rule inventory across the seven artifacts: type 597, required 276, allowed 85,
reference_integrity 20, reference_shape 18, schema_version 7.

## Known Limitations

- Path-based external references (`ref_path`, e.g. `design_reference`,
  `profile_reference`) are not resolved cross-document — only `ref_id` references.
- Cross-document resolution covers only the files passed via `--context`; there is
  no repository-wide discovery.
- The `schema_version`-match rule is carried in artifacts but not enforced as an
  availability check (single-schema validation).
- A container is treated as required only when it has a *directly*-required child.

## How to Run the Tooling

From the repository root (requires Python 3 and PyYAML):

```
# regenerate all rule artifacts from the approved schemas
python3 acedp/tools/validation/extract_all.py

# validate one instance against its rule artifact
python3 acedp/tools/validation/validator.py <instance.yaml> <rules.json>

# validate the sample for every schema
python3 acedp/tools/validation/validate_all.py

# cross-document resolution across a local instance set
python3 acedp/tools/validation/validator.py <instance.yaml> <rules.json> \
    --context <dir-or-files>
```

Exit codes: `0` conformant, `1` non-conformant, `2` tooling/runtime error.

## Boundaries That Remain in Effect

- Read-only over approved schemas; the tooling never modifies approved artifacts.
- No interpretation or execution of instance content.
- No Mist interaction, API payloads, or configuration generation.
- No real customer data — sample placeholder instances only.
- Any change to an Approved 1.0 artifact still requires a new revision (STD-001).

## Recommended Next Implementation Phase

Phase 0 (validation tooling) is complete. The recommended next step is
**Phase 1 — Engagement Intake**: use the validator to author and validate real
Project Profile and Customer Discovery instances. Phase 1 requires **Gate B**
(product_owner authorization to use real engagement/customer data) before any
non-sample data is processed; until then, work continues on sample instances.
Beyond that, the pipeline proceeds to Engineering Review workflow, Design
Package, Readiness, and — only under a separate authorized specification and
Gate D — Mist organization generation.

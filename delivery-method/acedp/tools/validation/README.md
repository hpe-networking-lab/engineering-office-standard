# ACEDP Validation Engine — Phase 0a Pilot

This directory holds the **first executable validation pilot** for the ACEDP
Validation Engine, authorized by SPEC-008 (Approved 1.0; Gate A) and designed by
REF-ARCH-001 / REF-DESIGN-001, implementing the mapping in REF-MAP-001.

Scope: extraction now covers **all seven approved schemas** (SPEC-001 through SPEC-007); the validator that consumes these artifacts is a later, separately reviewed step.

## Files

- `extract_rules.py` — reads one approved ACEDP YAML schema (read-only) and emits
  an intermediate, representation-neutral rule artifact (JSON).
- `extract_all.py` — driver that reuses `extract_rules` to generate artifacts for
  ALL seven approved schemas.
- `<Schema>.rules.json` — generated intermediate rule artifacts (one per approved
  schema), committed as the extraction output:
  `Project_Profile`, `Customer_Discovery`, `Engineering_Review`,
  `POC_Deliverable`, `Design_Package`, `Mist_Organization_Readiness`,
  `Mist_Organization_Generation`.
- `validator.py` — validates ONE data instance against a `<schema>.rules.json`
  artifact (required fields, field types, allowed enumerations, reference shape,
  and internal reference integrity) and prints a structured JSON report.
  Read-only. Cross-document resolution of structured external references is
  available across a local instance set via `--context` (off by default).
- `sample_project_profile.yaml` — a conformant, placeholder (non-customer)
  Project Profile instance for testing the validator.
- `sample_<schema>.yaml` — conformant placeholder (non-customer) instances for
  all seven schemas (e.g. `sample_customer_discovery.yaml`,
  `sample_engineering_review.yaml`, `sample_poc_deliverable.yaml`,
  `sample_design_package.yaml`, `sample_mist_organization_readiness.yaml`,
  `sample_mist_organization_generation.yaml`).
- `validate_all.py` — runs the validator across all seven schemas; exit 0 only if
  every sample is conformant.

## Prerequisites

- Python 3
- PyYAML (`pip install pyyaml --break-system-packages`)

## How to Run

From the repository root:

```
python3 acedp/tools/validation/extract_rules.py
```

This reads `acedp/schemas/Project_Profile.schema.yaml` and writes
`acedp/tools/validation/Project_Profile.rules.json`. Optional arguments:

```
python3 acedp/tools/validation/extract_rules.py <schema.yaml> <output.json>
```

To generate artifacts for all seven approved schemas:

```
python3 acedp/tools/validation/extract_all.py
```

## Validating an Instance

```
python3 acedp/tools/validation/validator.py [instance.yaml] [rules.json]
```

Defaults to `sample_project_profile.yaml` against `Project_Profile.rules.json`.

Reference-shape validation: a structured reference field (`type: reference`) must
be an object, and its required subfields (e.g. `ref_document`, `ref_id`) must be
present and correctly typed. Whether a referenced ID actually exists, and any
cross-instance resolution, are deferred to a later phase.

Required sections: a container section that holds a directly-required field is
itself required. If the whole section is absent (e.g. `metadata` or `scope`),
the validator reports a single `required` finding for the section.

Internal reference integrity: a bare-id internal link (e.g.
`success_criteria[].linked_objective`) must resolve to an existing local id in
its target collection within the **same** instance.

Cross-document references: when a local instance set is supplied with `--context`,
every structured external reference (a `{ ref_document, ref_id }` object) must
resolve to an instance in that set whose `metadata.document_reference` and id
match. Without `--context`, external references are not resolved (shape is still
checked). Resolution uses only the provided local files — no external systems.

```
python3 acedp/tools/validation/validator.py <instance.yaml> <rules.json> \
    --context <dir-or-files>
```

A worked, non-customer example set is under `sample_set/`: `project_profile.yaml`
references `engineering_review.yaml` (SPEC-003, ER-1).
It prints a structured JSON validation report and returns an exit code:

- `0` — conformant (no errors)
- `1` — non-conformant (one or more errors)
- `2` — usage/load error

To validate the sample for every approved schema at once:

```
python3 acedp/tools/validation/validate_all.py
```

The validator accepts any `<instance.yaml> <rules.json>` pair, so it works for
all seven schemas. The validator is read-only: it never modifies the instance or the approved
schemas, performs no cross-document reference validation, contacts no external
system, and uses only sample placeholder data.

## What It Does

- Reads schema **constructs** only (`type`, `required`, `allowed`, `items`,
  `fields`, `reference`, `metadata.schema_version`) and emits one or more rules
  per field, tagged with the source `schema_id` and `schema_version`.

## What It Does NOT Do

- It does not validate any data instance (rule **extraction** only).
- It does not modify the approved schema (read-only).
- It does not read or write customer data — no customer data is involved.
- It does not contact Mist, call any API, or produce configuration or payloads.

## Scope and Next Steps

This is a pilot for a single schema to validate the extraction approach
(REF-MAP-001) at the smallest reviewable scope. Extending extraction to the
remaining approved schemas, and building the validator that consumes these rule
artifacts, are separate, separately reviewed build steps (REF-DESIGN-001,
Phase 0b onward), on non-customer sample data only.

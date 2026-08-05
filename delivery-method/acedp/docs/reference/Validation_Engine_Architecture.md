# Validation Engine Architecture

- Document ID: REF-ARCH-001
- Status: Draft
- Version: 0.1
- Last Updated: 2026-06-30
- Authorized By: SPEC-008 Platform Tooling and Validation (Approved 1.0; Gate A)
- Related: REF-PHASE0-001 (Phase 0 Validation Tooling Plan), REF-ROADMAP-001

> This is an architecture document only. It defines the design of the Validation
> Engine; it implements no code, generates no schema, and runs nothing.

## 1. Purpose

Design the Validation Engine: the first executable component of ACEDP, which
checks whether an ACEDP data instance conforms to its approved schema. The
engine is **schema-driven** — its validation rules are generated from the
approved YAML schemas, so it validates today's schemas and future ones without
redesign. It performs conformance checking only; it interprets nothing, calls no
external system, and generates no configuration.

## 2. Overall Architecture

The engine is a linear, stage-based pipeline of small, single-responsibility
components behind stable interfaces. Schema knowledge lives in the approved
schemas, never in component code, which is what lets new schemas be supported
without changing the engine.

```
        approved YAML schema (read-only)        data instance
                  │                                   │
                  ▼                                   ▼
          ┌───────────────┐                   ┌───────────────┐
          │ Schema Loader │                   │ Instance Loader│
          └──────┬────────┘                   └──────┬─────────┘
                 ▼                                    │
          ┌───────────────┐                          │
          │ Rule Generator│  (YAML conventions →      │
          │               │   declarative ruleset)    │
          └──────┬────────┘                          │
                 └───────────────┬──────────────────┘
                                 ▼
                        ┌──────────────────┐
                        │  Validator Core  │  structural + convention checks
                        └────────┬─────────┘
                                 ▼
                        ┌──────────────────┐
                        │ Reference Resolver│ internal + structured external links
                        └────────┬─────────┘
                                 ▼
                        ┌──────────────────┐
                        │  Result Builder  │ → Validation Result
                        └────────┬─────────┘
                                 ▼
                        ┌──────────────────┐
                        │     Reporter     │ human- and machine-readable output
                        └──────────────────┘
```

Supported artifact types at launch: Project Profile, Customer Discovery,
Engineering Review, Design Package, and Mist Organization Readiness — plus any
future schema, because each is handled by the same generated-rule path.

## 3. Inputs

- An approved YAML schema (SPEC-001 … SPEC-007 and later), treated as read-only
  source of truth, including its authoritative `schema_version`.
- A data instance to validate, expressed against that schema.
- The STD-001 conventions the schemas follow (envelope order, `type`,
  `required`, `allowed`, `items`, `fields`, reference forms).

No customer-specific configuration and no external/runtime inputs are required.

## 4. Outputs

- A **Validation Result**: an overall `conformant` / `non_conformant`
  determination, a list of findings, and summary counts.
- A rendered report in human-readable and machine-readable form.
- Each result is stamped with the source schema ID and `schema_version` it was
  validated against.

The engine produces no configuration, no API payloads, and no side effects on
the approved artifacts.

## 5. Processing Pipeline

1. **Acquire schema** — load the approved schema and read its authoritative
   `schema_version`.
2. **Generate rules** — derive a declarative ruleset from the schema's
   documented constructs (no per-schema code).
3. **Load instance** — read the data instance to be validated.
4. **Validate structure** — run the ruleset against the instance.
5. **Validate references** — resolve internal and external links.
6. **Validate conventions** — check naming and envelope conventions.
7. **Build result** — aggregate findings and decide conformance.
8. **Report** — render the result.

The pipeline is deterministic and reproducible: the same instance and schema
version always yield the same result.

## 6. Validation Stages

- **Stage A — Schema acquisition:** locate the approved schema; capture
  `schema_version` for traceability and version-aware validation.
- **Stage B — Rule generation:** map documentation-first constructs to
  declarative rules — `type`, `required`, `allowed` (enumerations), `items`
  (lists), `fields` (structured references), and envelope ordering.
- **Stage C — Structural validation:** required fields present, types correct,
  enumerated values within `allowed`, list/item shapes correct.
- **Stage D — Reference validation:** internal links resolve to a local
  `<section>_id`; structured external references are well-formed
  (`ref_document` + `ref_id`).
- **Stage E — Convention validation:** snake_case keys, `<section>_id`
  identifiers, the `metadata → references → body → approvals` envelope, and the
  STD-001 status vocabulary.
- **Stage F — Result assembly:** collect findings; determine overall conformance.

## 7. Error Reporting Model

Each finding records:

- `finding_id` — stable local identifier within the result.
- `severity` — `error` (breaks conformance), `warning` (advisory convention
  issue), or `info`.
- `location` — a path into the instance (for example `scope.in_scope[0]`).
- `rule` — the rule/construct that produced the finding (for example
  `required`, `allowed`, `reference_integrity`).
- `expected` / `actual` — the expected condition and what was found.
- `message` — a human-readable explanation.
- `schema_reference` — the schema ID and `schema_version` validated against.

An instance is `non_conformant` if any `error`-severity finding is present.
Note: this conformance severity is distinct from the SPEC-003 review concept of
a "blocking finding"; a non-conformant instance would be a blocking finding for
the artifact under Engineering Review, but the engine itself makes no approval
decision.

## 8. Component Interfaces

Interfaces are conceptual (no code). Each is a small contract enabling
substitution and testing:

- `SchemaSource.load(schema_id) -> SchemaModel` — read an approved schema.
- `RuleGenerator.generate(SchemaModel) -> RuleSet` — derive declarative rules.
- `InstanceSource.load(ref) -> Instance` — read an instance to validate.
- `Validator.validate(Instance, RuleSet) -> [Finding]` — structural/convention
  checks.
- `ReferenceResolver.resolve(Instance, context) -> [Finding]` — link integrity.
- `ResultBuilder.build([Finding], schema_ref) -> ValidationResult`.
- `Reporter.render(ValidationResult) -> Report` — human/machine output.

Components depend only on these interfaces, not on any specific schema.

## 9. Future Extensibility

- **New schemas without redesign:** because rules are generated from schemas,
  adding a schema requires no engine change.
- **Pluggable rule backend:** the `RuleGenerator` may emit JSON Schema or an
  alternative representation behind the same interface.
- **Version-aware validation:** instances are validated against the
  `schema_version` they declare.
- **Cross-instance validation (future):** an optional stage could check that a
  referenced instance exists and is itself conformant (for example a Customer
  Discovery referencing an approved Project Profile).
- **Explicitly out of scope:** Mist API interaction, configuration generation,
  provisioning, and any customer-specific logic — these belong to separate,
  separately authorized components, never the validator.

## 10. Human Approval Points

- **This architecture** is reviewed and approved via Engineering Review
  (SPEC-003) before any implementation begins (lead_architect technical
  approval; product_owner where authorization applies).
- **The rule-generation mapping** (Stage B) is reviewed before the engine is
  built, as it defines how schemas become rules.
- **Each build deliverable** (rule generator, validator core, reporter) is
  reviewed before use.
- **Use on real data** requires product_owner authorization (Roadmap Gate B);
  until then the engine runs only on non-customer sample data.

## Design Assumptions

- Approved YAML schemas are the single source of truth.
- Validation rules are generated from schemas, not hand-written per schema.
- No customer-specific logic; no Mist API interaction; no configuration
  generation; no executable code in this document.

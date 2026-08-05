# Validation Engine Design

- Document ID: REF-DESIGN-001
- Status: Draft
- Version: 0.1
- Last Updated: 2026-06-30
- Bridges: REF-ARCH-001 (Validation Engine Architecture) -> implementation
- Authorized By: SPEC-008 Platform Tooling and Validation (Approved 1.0; Gate A)
- Related: REF-PHASE0-001, REF-ROADMAP-001

> Implementation design only. It refines REF-ARCH-001 toward implementation but
> writes no code, generates no schema or rules, creates no templates/examples,
> introduces no Mist interaction, and modifies no approved artifact.

## 1. Component Responsibilities

- **Schema Loader** — read an approved YAML schema (read-only) and parse it into
  a normalized `SchemaModel`; expose its authoritative `schema_version`.
- **Rule Generator** — derive a declarative `RuleSet` from a `SchemaModel` using
  the STD-001 constructs; attach the source schema id and version. No per-schema
  code.
- **Rule Cache / Version Registry** — store `RuleSet`s keyed by
  `(schema_id, schema_version)`; serve the correct version on request.
- **Instance Loader** — read a data instance (sample, non-customer) into a
  normalized form and surface the schema id and version it declares.
- **Validator Core** — run a `RuleSet` against an instance to produce structural
  and convention findings.
- **Reference Resolver** — verify internal links (local `<section>_id`) and
  structured external references (`ref_document` + `ref_id`), including optional
  cross-schema/cross-instance resolution.
- **Result Builder** — aggregate findings into a `ValidationResult` and decide
  conformance.
- **Reporter** — render the result in human- and machine-readable form.
- **Logger** — emit structured, leveled diagnostic logs; never log customer data.
- **Plugin Registry** — register additional validators that run as extra stages.

## 2. Component Interfaces

Conceptual contracts (not code):

```
SchemaLoader.load(schema_id) -> SchemaModel{ id, version, sections, conventions }
RuleGenerator.generate(SchemaModel) -> RuleSet{ schema_id, schema_version, rules[] }
RuleRegistry.get(schema_id, version) -> RuleSet            # generate-and-cache on miss
InstanceLoader.load(ref) -> Instance{ declared_schema_id, declared_version, data }
Validator.validate(Instance, RuleSet) -> Finding[]
ReferenceResolver.resolve(Instance, ResolutionContext) -> Finding[]
ResultBuilder.build(Finding[], schema_ref, run_id) -> ValidationResult
Reporter.render(ValidationResult, format) -> Report
PluginRegistry.register(Validator); PluginRegistry.validators() -> Validator[]
```

Every component depends only on these contracts, never on a specific schema.

## 3. Internal Data Flow

```
schema file ──> SchemaLoader ──> SchemaModel ──> RuleGenerator ──> RuleSet
                                                     │  (cached by id+version)
instance ──> InstanceLoader ──> Instance ───────────┘
        │
        └─> Validator(Instance, RuleSet) ─┐
            ReferenceResolver(Instance) ───┼─> Finding[] ─> ResultBuilder
            Plugin validators ─────────────┘                   │
                                                                ▼
                                                        ValidationResult ─> Reporter
                                                                │
                                                                └─> Logger (diagnostics)
```

`RuleSet`s are derived once per `(schema_id, schema_version)` and reused; the
flow is deterministic — identical inputs yield identical results.

## 4. Rule Generation Workflow

1. Load and parse the approved YAML schema into a `SchemaModel`.
2. Read the authoritative `metadata.schema_version`.
3. Walk the model and map each construct to one or more declarative rules:
   - `type` -> type rule; `required` -> presence rule; `allowed` -> enumeration
     rule; `items` -> list-element rules; `fields` -> structured-reference shape
     rules; envelope order -> ordering rule; naming -> convention rules.
4. Tag the resulting `RuleSet` with `schema_id` and `schema_version`.
5. Cache the `RuleSet` in the Rule Registry keyed by `(schema_id, version)`.

The workflow is declarative and reproducible; it produces rules, never executes
instance content. (This design defines the workflow; it generates no rules here.)

## 5. Validation Execution Workflow

1. Load the instance and read its declared `schema_id` and `schema_version`.
2. Obtain the matching `RuleSet` from the Rule Registry (generate-and-cache on
   miss); if the declared version is unknown, emit a single `error` finding and
   stop.
3. Run the **structural** stage (Validator Core).
4. Run the **reference** stage (Reference Resolver) — internal links and
   structured external references; cross-instance checks when a resolution
   context is provided.
5. Run any **plugin** validators registered for the artifact type.
6. Aggregate findings; the Result Builder sets `conformant` false if any
   `error`-severity finding exists.
7. Render via the Reporter; emit diagnostics via the Logger.

Only sample, non-customer instances are validated until real-data use is
separately authorized (Roadmap Gate B).

## 6. Error Model

A `Finding` carries: `finding_id`, `severity` (`error` | `warning` | `info`),
`location` (instance path), `rule` (the rule/construct that fired),
`expected`, `actual`, `message`, and `schema_reference` (`schema_id` +
`schema_version`).

A `ValidationResult` carries: `conformant` (boolean), `findings[]`,
`summary` (counts by severity), `schema_reference`, and `run_id`. An instance is
`non_conformant` if any `error` finding is present. This conformance severity is
distinct from the SPEC-003 "blocking finding" concept; the engine renders a
result and makes no approval decision.

## 7. Logging Model

- Structured, leveled diagnostic logs (`debug` | `info` | `warn` | `error`),
  separate from validation findings.
- Each entry is tagged with `run_id` and `schema_id` + `schema_version`, and
  records the stage executed and timing.
- Logs **never** contain customer data; only sample/non-sensitive content and
  structural metadata.
- Logs are diagnostic aids, not authoritative output; the `ValidationResult` is
  the authoritative record.

## 8. Version Handling

- `metadata.schema_version` is authoritative. `RuleSet`s are keyed by
  `(schema_id, schema_version)`; multiple versions coexist in the Version
  Registry.
- An instance declares the version it conforms to; the engine validates against
  that version's `RuleSet`.
- A declared version with no available schema yields an `error` finding (cannot
  validate); superseded versions are retained for traceability.
- Validation is therefore version-aware and reproducible across versions.

## 9. Extensibility Model

- **New schemas without code:** rules are generated from schemas, so a new
  approved schema is validated with no engine change.
- **Pluggable rule backend:** the Rule Generator may emit JSON Schema or an
  alternative behind the same interface.
- **Plugin validators:** additional `Validator`s register with the Plugin
  Registry and run as extra stages (for example richer cross-schema or
  cross-instance checks).
- **Boundaries for plugins:** plugins must not interpret/execute content, call
  external systems, touch customer data, or perform Mist interaction.

## 10. Future Implementation Phases

Each phase is a separately reviewed (SPEC-003) build deliverable, on sample data
only:

- **0a — Rule-generation mapping + pilot:** document the construct-to-rule
  mapping and pilot one schema (REF-PHASE0-001).
- **0b — Validator Core:** structural validation for all approved schemas.
- **0c — Reference Resolver:** internal and structured external references.
- **0d — Reporter + Logger:** result rendering and diagnostics.
- **0e — Version Registry:** multi-version handling.
- **0f — Plugin framework:** plugin validators and cross-schema validation.

Mist provisioning/generation remains out of scope and requires a separate
authorized specification.

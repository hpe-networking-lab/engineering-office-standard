# Phase 0 — Validation Tooling Plan

- Document ID: REF-PHASE0-001
- Status: Draft
- Version: 0.1
- Last Updated: 2026-06-30
- Authorized By: SPEC-008 Platform Tooling and Validation (Approved 1.0; Gate A cleared)
- Roadmap: REF-ROADMAP-001, Phase 0

## Objective

Plan the first implementation step authorized by SPEC-008 (Gate A cleared):
tooling that validates ACEDP data instances for conformance to the approved
schemas. This is a plan only — it builds no tooling, generates no schema, and
creates no templates or examples. It defines what the first Phase 0 build
milestone will produce and how it will be reviewed.

## Scope

Covers planning for instance-validation tooling derived from the seven approved
schemas (SPEC-001 through SPEC-007), within the boundaries of SPEC-008. It does
not cover Mist provisioning or generation, customer-data processing, or any
change to approved artifacts. Validation is limited to checking conformance.

## Approved Inputs

- SPEC-008 Platform Tooling and Validation (Approved 1.0) — authorization and
  boundaries.
- The seven approved schemas (SPEC-001 through SPEC-007), each Approved 1.0.
- STD-001 (Approved 1.0) — the schema conventions the schemas follow
  (`type`, `required`, `allowed`, `items`, `fields`, structured references,
  and the common envelope).

## Proposed Validation Representation

**Recommendation: JSON Schema (Draft 2020-12), generated from the approved YAML
schemas.** The documentation-first YAML already encodes `type`, `required`,
`allowed` (enumerations), `items` (lists), and `fields` (structured
references); these map directly to JSON Schema constructs (`type`, `required`,
`enum`, `array`/`items`, nested objects). JSON Schema is a language-agnostic,
widely-supported standard with mature validators, and keeps validation
**declarative** — consistent with the documentation-first ethos and avoiding
bespoke validation logic.

This recommendation dispositions SPEC-008 open questions OQ1 (representation) and
OQ2 (version awareness): the generated validation is tagged with the source
`schema_version`, so an instance is validated against the version it declares.
The recommendation is confirmed at the first build milestone's review; an
alternative (hand-written validator code) was considered and is not recommended,
as it introduces non-declarative logic and maintenance burden.

## Deliverables (produced by the Phase 0 build milestone, not by this plan)

- Documented mapping rules from each approved YAML schema construct to its JSON
  Schema equivalent.
- Generated JSON Schema documents for the seven approved schemas, each traceable
  to its source schema and `schema_version`.
- A conceptual validation-runner definition that reports conformant /
  non-conformant with reasons (human- and machine-readable).
- Sample, non-customer instances used only to exercise validation.

## Boundaries

- This plan creates no tooling, no JSON Schema, no templates, and no examples.
- Validation will check conformance only; it will never interpret, execute, or
  act on instance content, call any API, or contact any external system.
- No customer data: only non-sensitive sample data, and only once a build
  milestone is reviewed.
- The approved schemas are read-only inputs; tooling never modifies approved
  artifacts.
- Mist provisioning, generation, and automation remain out of scope (a future
  specification).

## Review Requirements

- Each Phase 0 build deliverable is reviewed via Engineering Review (SPEC-003)
  before it is used.
- Approval authority: lead_architect (technical approval); product_owner where
  business or authorization concerns apply.
- The representation choice (JSON Schema) and version-awareness approach are
  confirmed at the first build milestone's review, dispositioning SPEC-008 OQ1
  and OQ2.
- Every generated validation artifact must be traceable to the approved schema
  and `schema_version` it derives from.

## Recommended Next Build Milestone

**Milestone 64 — Pilot validation generation for a single schema.** Generate the
JSON Schema for one approved schema (recommended: `Project_Profile.schema.yaml`),
together with the mapping rules and one sample non-customer instance, and submit
it for SPEC-003 review before extending to the remaining six. Starting with one
schema validates the mapping approach at the smallest reviewable scope; the
remaining schemas follow once the approach is approved.

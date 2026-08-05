# ACEDP Implementation Roadmap (v1.0 Framework)

- Document ID: REF-ROADMAP-001
- Status: Draft
- Version: 0.1
- Last Updated: 2026-06-30
- Framework Baseline: ACEDP v1.0 (commit a46d408, Milestone 58)

## Purpose

Define the phases needed to turn the approved, documentation-first ACEDP
framework (SPEC-001 through SPEC-007 and their schemas) into a working delivery
platform. This roadmap plans implementation; it does not implement anything and
modifies no approved artifact. It is a living reference document and remains
`Draft`.

## Guiding Constraints

- The approved framework is **documentation-first**: it contains no executable
  code, validation logic, automation, or Mist configuration.
- Crossing the documentation-to-executable boundary (validation tooling,
  generation, automation, live Mist interaction) requires a **new authorizing
  specification**, reviewed and Approved via SPEC-003, before any build begins.
- Any change to an Approved 1.0 artifact requires a new revision, not an
  in-place edit (STD-001).
- Secrets, organization IDs, API tokens, and claim codes are never committed to
  the repository (ADR-0008 / SPEC-006 / SPEC-007 boundaries).

## Phase Sequence

| Phase | Name | Outcome |
|---|---|---|
| 0 | Platform Foundation & Validation | A specification authorizing tooling, plus machine-readable validation, templates, and examples |
| 1 | Engagement Intake | Authored, validated Project Profile (SPEC-001) and Customer Discovery (SPEC-002) records |
| 2 | Engineering Review Workflow | Recorded reviews, findings, dispositions, and approvals (SPEC-003) |
| 3 | Design Package Production | Authored Design Package records — HLD/LLD and domain plans (SPEC-005) |
| 4 | Readiness Assessment | Mist Organization Readiness assessments and ready/partial/not_ready determinations (SPEC-006) |
| 5 | Generation & Provisioning | Generation intent (SPEC-007) and a NEW provisioning specification authorizing actual Mist preparation |
| 6 | Customer Documentation | Customer-facing documentation generated from approved records (SPEC-005 contents) |
| 7 | Operationalization | End-to-end pilot engagement; lessons fed back as framework revisions |

Phases are strictly ordered by dependency; each completes through its approval
gate before the next begins (small milestones, per ACEM).

## Phase Detail

### Phase 0 — Platform Foundation & Validation
- **Major deliverables:** an authorizing specification (e.g. SPEC-008 Platform
  Tooling & Validation); machine-readable validation derived from the approved
  YAML schemas (e.g. JSON Schema); instance templates under `acedp/templates/`;
  worked examples under `acedp/examples/`.
- **Required inputs:** approved schemas (SPEC-001..007), STD-001 conventions.
- **Implementation dependencies:** none upstream; gates all later phases.

### Phase 1 — Engagement Intake
- **Major deliverables:** capability to author and validate Project Profile and
  Customer Discovery instances; validated examples.
- **Required inputs:** SPEC-001/002 + schemas; Phase 0 validation.
- **Implementation dependencies:** Phase 0.

### Phase 2 — Engineering Review Workflow
- **Major deliverables:** review-record authoring with authority, blocking/waiver
  handling, and open-question dispositions per SPEC-003.
- **Required inputs:** SPEC-003 + schema; Phase 1 records.
- **Implementation dependencies:** Phase 1.

### Phase 3 — Design Package Production
- **Major deliverables:** assisted authoring of Design Package records (design
  intent only — no configuration) from approved profile and discovery.
- **Required inputs:** approved Project Profile + Customer Discovery; SPEC-005 +
  schema.
- **Implementation dependencies:** Phases 1–2.

### Phase 4 — Readiness Assessment
- **Major deliverables:** Mist Organization Readiness assessment records with the
  SPEC-006 threshold determination.
- **Required inputs:** approved Design Package; SPEC-006 + schema.
- **Implementation dependencies:** Phase 3.

### Phase 5 — Generation & Provisioning
- **Major deliverables:** (a) Mist Organization Generation **intent** records
  (SPEC-007); (b) a NEW provisioning specification defining actual organization
  preparation, API interaction, and secrets handling — content the v1.0 framework
  explicitly excludes and which must be authored and Approved first.
- **Required inputs:** approved "ready" readiness assessment; approved generation
  intent; SPEC-007; the new provisioning spec.
- **Implementation dependencies:** Phase 4; no live Mist interaction before the
  provisioning spec is Approved and implementation is authorized.

### Phase 6 — Customer Documentation
- **Major deliverables:** customer-facing documentation generated from approved
  design (and, where applicable, generation) records.
- **Required inputs:** approved Design Package (SPEC-005 `customer_documentation`).
- **Implementation dependencies:** Phase 3 onward.

### Phase 7 — Operationalization
- **Major deliverables:** an end-to-end pilot engagement run through the platform;
  captured improvements fed back as new revisions of framework artifacts.
- **Required inputs:** all prior phases.
- **Implementation dependencies:** Phases 0–6.

## Claude Responsibilities (Implementation Engineer)

- Author proposed specifications and deliverables within approved scope; never
  invent customer data, secrets, or facts.
- Implement only what has been approved; build no executable validation,
  automation, or Mist interaction before its authorizing specification is
  Approved.
- Produce a review package per milestone (summary, files, validation, blockers).
- Keep secrets and identifiers out of the repository; report blockers; stop at
  each gate.

## ChatGPT Review Responsibilities (Lead Architect)

- Review each proposed specification and deliverable for technical correctness,
  standards conformance, and scope.
- Own risk analysis, blocking-finding determination, and technical approval or
  rejection per SPEC-003.
- Confirm that documentation-to-executable transitions are properly authorized
  before implementation proceeds.

## Human Approval Gates (Product Owner)

- **Gate A (Phase 0):** authorize building executable tooling; approve the
  tooling/validation specification.
- **Gate B (Phase 1):** authorize use of real engagement and customer data.
- **Gate C (Phases 2–4):** business/customer acceptance where artifacts affect
  scope or commitments.
- **Gate D (Phase 5):** authorize the provisioning specification and, separately,
  authorize implementation start before any live Mist organization preparation
  (the SPEC-007 pre-implementation review).
- **Gate E (Phases 6–7):** accept customer documentation and sign off on platform
  readiness.

## Recommended First Implementation Milestone

**Milestone 60 — Author the Platform Tooling & Validation Specification.**
Draft a new specification (proposed SPEC-008) that authorizes crossing the
documentation-to-executable boundary: machine-readable validation generated from
the approved schemas, instance templates, and worked examples — with its own
scope, required inputs/outputs, must-not boundaries (no secrets, no live Mist
interaction), and review/approval rules. This is the correct first step because
no tooling may be built until a specification authorizes it (Gate A). The
specification is authored as Draft, reviewed by the Lead Architect (SPEC-003),
and approved before any Phase 0 build work begins.

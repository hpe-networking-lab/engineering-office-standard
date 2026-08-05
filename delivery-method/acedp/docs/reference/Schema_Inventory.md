# Schema Inventory

- Document ID: REF-SCHEMA-001
- Status: Draft
- Version: 0.6
- Last Updated: 2026-06-30
- Audited Commit: b6c20bd (Milestone 57 - Approve Remaining Spec Schema Pairs)

## Purpose

Summarize the schemas under `acedp/schemas/` — their purpose, source
specification, approval state, and structure — and how they fit together.
Descriptive only; it defines nothing new and modifies no schema. This is a
living reference document and remains `Draft`.

## Approval State

All seven schemas are **Approved at version 1.0**, each paired with its
Approved 1.0 specification. Approval authority was recorded per the SPEC-003
approval-authority matrix.

| Schema | Source spec | Status | Version |
|---|---|---|---|
| Project_Profile.schema.yaml | SPEC-001 | Approved | 1.0 |
| Customer_Discovery.schema.yaml | SPEC-002 | Approved | 1.0 |
| Engineering_Review.schema.yaml | SPEC-003 | Approved | 1.0 |
| POC_Deliverable.schema.yaml | SPEC-004 | Approved | 1.0 |
| Design_Package.schema.yaml | SPEC-005 | Approved | 1.0 |
| Mist_Organization_Readiness.schema.yaml | SPEC-006 | Approved | 1.0 |
| Mist_Organization_Generation.schema.yaml | SPEC-007 | Approved | 1.0 |

## Schemas

### Project_Profile.schema.yaml (SPEC-001)
Canonical description of a single engineering project; the anchor downstream
records reference. Approvals use the canonical `authority` role enum.

### Customer_Discovery.schema.yaml (SPEC-002)
Gathered engagement context and confirmed facts enriching the Project Profile,
plus explicit unknowns and assumptions.

### Engineering_Review.schema.yaml (SPEC-003)
The shared review gate: scope, artifacts, criteria, findings (with the defined
"blocking" semantics and `waived` state), risks, required changes, decision.

### POC_Deliverable.schema.yaml (SPEC-004)
Proof-of-Concept deliverable: scope, success criteria, test plan, validation
results, risks, assumptions, handoff.

### Design_Package.schema.yaml (SPEC-005)
Design intent (HLD, LLD, domain plans). The `mist_organization_readiness`
section is preliminary and superseded by the authoritative SPEC-006 assessment.

### Mist_Organization_Readiness.schema.yaml (SPEC-006)
Authoritative readiness assessment; `overall_readiness` follows the SPEC-006
threshold with mandatory / conditional / recommended categories.

### Mist_Organization_Generation.schema.yaml (SPEC-007)
Intent record (no configuration/IDs/secrets) with structured `design_reference`
traceability and template/site inheritance fields.

## Overall Schema Pipeline

```
Project_Profile (SPEC-001)               the anchor
        ▼ enriched by
Customer_Discovery (SPEC-002)
        ▼ validated by
Engineering_Review (SPEC-003)            the shared approval gate
        ▼ authorizes
Design_Package (SPEC-005)
        ▼ assessed by (authoritative)
Mist_Organization_Readiness (SPEC-006)   ready / partial / not_ready
        ▼ when "ready" + approved
Mist_Organization_Generation (SPEC-007)  intent, traceable to the design
        ▼ pre-implementation review + approval
Implementation / automation              (out of scope; not yet specified)
```

POC_Deliverable (SPEC-004) is a feasibility artifact that also passes through
SPEC-003. Every record's `approvals.review_reference` points to a SPEC-003
review record.

## Shared Schema Conventions (per STD-001)

Common envelope `metadata → references → domain body → approvals`;
`metadata.schema_version` authoritative; snake_case keys and `<section>_id`
identifiers; structured external references; `approvals` is a list of records
with the canonical `authority` role enum; "blocking" defined in SPEC-003.

## Open Questions

All schema-level open questions raised during development have been dispositioned
(accepted or resolved) at Approval; accepted items are recorded in the relevant
specifications' Open Questions sections with owner, rationale, and revisit
conditions.

## Status

The ACEDP schema set is complete and Approved at 1.0. Future schema changes
require a new revision (per STD-001). Extending the pipeline into
implementation/automation requires a new, separately authorized specification.

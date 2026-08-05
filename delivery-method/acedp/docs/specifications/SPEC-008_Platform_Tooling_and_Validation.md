# Platform Tooling and Validation

- Document ID: SPEC-008
- Status: Approved
- Version: 1.0
- Approved By: lead_architect (technical approval), product_owner (Gate A authorization to build tooling)
- Approval Date: 2026-06-30

## Purpose

Authorize the transition from documentation-only ACEDP schemas to tooling that
can validate ACEDP data instances against the approved schemas and support
future implementation workflows. This specification defines what such tooling is
permitted to do and the boundaries it must respect. It authorizes; it does not
build any tooling.

## Scope

Covers the authorization and boundaries for validation and supporting tooling
that operates on ACEDP data instances conforming to the approved schemas
(SPEC-001 through SPEC-007). It does not cover Mist organization provisioning or
generation execution (a separate future specification), processing of real
customer data, or any change to approved framework artifacts.

## Required Inputs

- The approved ACEDP schemas (SPEC-001 through SPEC-007) and the STD-001
  conventions they follow.
- The approved specifications the schemas derive from.
- A data instance to validate (when tooling exists), expressed against its
  schema.

## Required Outputs

- Authorization — granted by approval of this specification — to build validation
  tooling and supporting artifacts (templates, worked examples, and
  machine-readable validation derived from the approved schemas) in subsequent,
  separately reviewed milestones.
- A defined set of capabilities and boundaries that any such tooling must
  respect.
- A conceptual validation-result model (conformant / non-conformant, with
  reasons), defined here and implemented later.

## Authorized Tooling Capabilities

Once this specification is Approved, the following are authorized to be built in
subsequent, separately reviewed milestones:

- Machine-readable validation derived from the approved YAML schemas (for
  example, generating JSON Schema or an equivalent) to check that a data instance
  conforms to its schema.
- Structural validation: required fields, data types, enumerated (`allowed`)
  values, and the common-envelope ordering.
- Reference-integrity checks: internal links resolve to a local `<section>_id`,
  and structured external references use the correct `ref_document` / `ref_id`
  form.
- Instance templates and worked examples that conform to the schemas.
- Reporting of validation results in human-readable and machine-readable form.

## Validation Boundaries

- Validation is limited to checking the conformance of data instances to the
  approved schemas and conventions.
- It does not interpret, execute, or act on instance content.
- It does not generate configuration, call any API, or contact any external
  system.
- It treats the approved schemas as authoritative and read-only; tooling never
  modifies approved artifacts.
- Until customer-data handling is separately authorized, validation operates only
  on non-sensitive, non-customer sample data.

## What Must Not Be Included

- Executable code, validation logic, templates, or examples within this
  specification — it is an authorizing document only.
- Mist API payloads, configuration, organization IDs, API tokens, claim codes, or
  secrets.
- Customer-specific data, or processing of real customer data.
- Provisioning, generation, or automation of Mist organizations (out of scope;
  a future specification).
- Any modification of Approved framework artifacts.

## Review and Approval Rules

- This specification is reviewed and Approved via Engineering Review (SPEC-003)
  before any tooling is built (Implementation Roadmap, Gate A).
- Approval authority: lead_architect (technical approval); product_owner
  (authorization to build executable tooling).
- Each subsequent tooling deliverable is itself reviewed before use.
- An approved tooling capability changes only through a new revision (STD-001).

## Open Questions

- Which validation representation should be generated from the YAML schemas (for
  example, JSON Schema, or another)?
  - Disposition: Accepted — owner: lead_architect, rationale: the representation is a Phase 0 implementation choice; the authorization does not depend on it, revisit: at the start of Phase 0 tooling work.
- Should validation be schema-version aware — validating an instance against the
  specific `schema_version` it declares?
  - Disposition: Accepted — owner: lead_architect, rationale: version-awareness is a tooling design detail decided when validation is built, revisit: during Phase 0 design.
- Where should templates and examples live, and how are they kept in sync with
  schema revisions?
  - Disposition: Accepted — owner: lead_architect, rationale: location and sync follow the Phase 0/1 build; STD-001 governs revisions, revisit: when templates and examples are created.
- What is the precise boundary between validation tooling and the future Mist
  provisioning specification?
  - Disposition: Accepted — owner: product_owner, rationale: the boundary is fixed by the future provisioning specification, not by this authorizing spec, revisit: when the provisioning specification is authored.
- How is non-customer sample data sourced for validation without introducing real
  customer data?
  - Disposition: Accepted — owner: lead_architect, rationale: sample-data sourcing is a Phase 0/1 concern; customer data stays excluded until separately authorized, revisit: before any validation runs on engagement data.

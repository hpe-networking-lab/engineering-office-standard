# Changelog

All notable changes to ACEM are recorded in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- **ACEDP Operating Model (REF-OPMODEL-001)** — a lean operating model that right-sizes governance to one Human Authority and one AI engineer. Keeps the schemas, the validator, Git, and a single human approval before any real-customer or real-Mist action; retires the ChatGPT-era per-stage review, Gates A–D, and per-milestone review packages. (2026-07-02)
- Initial ACEM foundation: repository structure, placeholder charter,
  methodology, role model, review process, templates, and changelog.
- ACEDP engineering library bootstrapped under `acedp/`, with the framework
  documents STD-001, STD-001.1, SPEC-001–SPEC-004, ADR-0008, and EKR-001
  populated, plus a Repository Audit baseline. (Milestones 21–24)
- STD-001 "Schema Conventions": the common schema envelope
  (`metadata → references → domain body → approvals`). (Milestone 29)
- Documentation-first schemas for the engagement pipeline: Project Profile
  (SPEC-001), Customer Discovery (SPEC-002), Engineering Review (SPEC-003),
  POC Deliverable (SPEC-004), Design Package (SPEC-005), Mist Organization
  Readiness (SPEC-006), and Mist Organization Generation (SPEC-007).
  (Milestones 25, 26, 30, 31, 34, 37, 40)
- Specifications SPEC-005 Design Package, SPEC-006 Mist Organization Readiness,
  and SPEC-007 Mist Organization Generation. (Milestones 33, 36, 39)
- Schema Inventory reference document and successive refreshes.
  (Milestones 32, 35, 38, 41)
- Populated the canonical role model: product_owner, lead_architect,
  implementation_engineer. (Milestone 48)

### Changed

- Superseded the ChatGPT-era governance: marked REF-AICOLLAB-001 (AI Collaboration Protocol) Superseded and noted the Default Workflow's gate mechanics as retired (stages retained as a checklist), per REF-OPMODEL-001. Schemas, standards, and the validator are unchanged. (2026-07-02)
- Aligned schema conventions across schemas: common envelope, standardized
  structured `references`, and a standardized `approvals` block. (Milestone 28)
- Defined approval authority (role enum and per-artifact matrix) and the
  blocking-finding definition in SPEC-003; aligned the `authority` enum across
  all seven schemas. (Milestones 43, 44)
- Defined the Mist readiness threshold (`ready` / `partial` / `not_ready`) and
  the mandatory / conditional / recommended category classification.
  (Milestone 45)
- Clarified the Design Package `mist_organization_readiness` section as a
  preliminary, design-side self-assessment superseded by the authoritative
  SPEC-006 assessment. (Milestone 46)
- Defined the design-to-Mist mapping and template/site inheritance intent, with
  structured `design_reference` traceability. (Milestone 47)
- Final reconciliation: refreshed the Schema Inventory and Repository Audit,
  removed the resolved blocking-finding marker from the readiness schema.
  (Milestone 48)
- Transitioned the ACEDP framework documents (STD-001, STD-001.1, SPEC-001–007,
  ADR-0008, EKR-001) and the role model from Draft to In Review; removed the
  resolved approval-authority marker from the Project Profile schema.
  (Milestone 50)
- Aligned the seven ACEDP schemas from Draft to In Review to match their
  specifications; recorded in STD-001 that reference documents may remain
  Draft as living artifacts. (Milestone 52)
- Adopted the approval policy in STD-001 and SPEC-003: per spec/schema-pair
  approval, accepted non-blocking open questions with recorded disposition, the
  0.x to 1.0 transition on Approval, and reference documents remaining Draft.
  (Milestone 54)
- Approved the foundation documents (STD-001, STD-001.1, ADR-0008, EKR-001) and
  the role model at version 1.0, with lead_architect technical approval and
  product_owner final acceptance; accepted open questions recorded with
  dispositions. (Milestone 55)
- Approved the Engineering Review gate (SPEC-003 and Engineering_Review schema)
  at version 1.0, with lead_architect technical approval and product_owner final
  acceptance; open questions dispositioned (role-model item resolved, waiver-field
  item accepted). (Milestone 56)
- Approved the remaining spec/schema pairs (SPEC-001/002/004/005/006/007 and
  their schemas) at version 1.0, with approval authority recorded per the
  SPEC-003 matrix; all remaining open questions dispositioned (accepted or
  resolved) and mirrored schema OPEN comments reconciled to the accepted
  dispositions. (Milestone 57)
- ACEDP framework Approved at v1.0: all normative documents (STD-001,
  STD-001.1, SPEC-001 through SPEC-007, ADR-0008, EKR-001), their schemas, and
  the role model are Approved at 1.0; reference documents (Schema Inventory,
  Repository Audit) refreshed and remain Draft as living artifacts.
  (Milestone 58)
- Approved SPEC-008 Platform Tooling and Validation at version 1.0
  (lead_architect technical approval; product_owner Gate A authorization to
  build tooling); five open questions accepted with dispositions. Roadmap
  Gate A is cleared: Phase 0 tooling work is authorized (each deliverable
  separately reviewed). (Milestone 62)

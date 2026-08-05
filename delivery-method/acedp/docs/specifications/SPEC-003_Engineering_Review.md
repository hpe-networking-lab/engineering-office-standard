# Engineering Review

- Document ID: SPEC-003
- Status: Approved
- Version: 1.0
- Approved By: lead_architect (technical approval), product_owner (final acceptance)
- Approval Date: 2026-06-30

## Purpose

Define the Engineering Review gate: the structured evaluation that validates an
artifact's quality and scope before it is approved or implemented.

## Scope

Covers the review of any ACEDP artifact (specifications, decisions, profiles,
POC deliverables, design packages, readiness assessments, and generation
intent). It defines the review mechanics and the approval authority, not the
content standards themselves (STD-001).

## Required Inputs

- A review package: the artifact under review plus its supporting context.
- The applicable standards and the artifact's stated scope.

## Required Outputs

- A review decision: Approved, or Rejected with recorded findings.
- A record of issues, required changes, and any accepted exceptions or waivers.

## Review / Approval Rules

- Review precedes implementation; nothing proceeds on an unreviewed artifact.
- Approval is explicit and attributable; silent approval is not valid.
- Approval is granted only by the artifact's approval authority (see Approval
  Authority).
- An artifact with any open blocking finding cannot be Approved (see Blocking
  Findings).
- Approved artifacts change only through a new revision, not in-place edits.

## Approval Authority

Approval is attributable to a canonical role. The authority roles are:

- `product_owner` — business and customer acceptance, and authorization to begin
  implementation.
- `lead_architect` — the primary technical approval authority for engineering
  artifacts.
- `implementation_engineer` — confirms implementation readiness only; holds no
  approval authority over engineering content.

The approval authority for each artifact class:

| Artifact class | Source | Approval authority |
|---|---|---|
| Project Profile | SPEC-001 | product_owner |
| Customer Discovery | SPEC-002 | lead_architect |
| Engineering Review | SPEC-003 | lead_architect |
| POC Deliverable | SPEC-004 | lead_architect (technical); product_owner (acceptance) |
| Design Package | SPEC-005 | lead_architect |
| Mist Organization Readiness | SPEC-006 | lead_architect |
| Mist Organization Generation | SPEC-007 | lead_architect (technical); product_owner (implementation authorization); implementation_engineer (implementation readiness) |

Where two or more roles are listed, technical approval and business or
implementation authorization are distinct decisions, and each required decision
must be recorded.

## Blocking Findings

A finding is **blocking** when it:

- prevents a mandatory review criterion from being satisfied, or
- violates a binding standard (STD-001 or STD-001.1), or
- violates an ADR-0008 "must not contain" boundary.

Rules:

- An artifact with any open blocking finding cannot be Approved.
- A blocking finding may be cleared only by being resolved, or by being formally
  waived with recorded justification by the artifact's approval authority.
- All other findings (major, minor, informational) are non-blocking and do not,
  by themselves, prevent approval.

## Open Question Disposition

During review, every open question carried by an artifact is given a disposition:

- **Resolved** — answered; record the resolution reference.
- **Waived** — a blocking item set aside with recorded justification by the
  approval authority.
- **Accepted** — a non-blocking item carried into Approval. An accepted open
  question records: disposition (Accepted), owner role, rationale, and a revisit
  condition (the milestone or event at which it is revisited).

An artifact may be Approved while carrying accepted open questions; it may not be
Approved while any blocking finding remains open (see Blocking Findings).
Accepted dispositions are recorded both in the artifact's Open Questions section
and in the Engineering Review record.

## Open Questions

- The approval-authority roles reference the ACEM role model
  (`roles/Role_Model.md`), which is not yet populated; the roles are defined here
  in the interim.
  - Disposition: Resolved — the role model is now populated and Approved (Milestones 48 and 55); the interim note no longer applies.
- Whether the review schema should carry explicit, separate waiver fields
  (waiving authority and justification) in addition to a `waived` finding state.
  - Disposition: Accepted — owner: lead_architect, rationale: the `waived` finding state suffices to record waivers for now, revisit: if a structured waiver record (authority and justification fields) becomes necessary.

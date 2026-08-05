# Project Profile

- Document ID: SPEC-001
- Status: Approved
- Version: 1.0
- Approved By: product_owner (approval)
- Approval Date: 2026-06-30

## Purpose

Define the Project Profile: the structured, authoritative description of a
single engineering project. The Project Profile is the entry point for an ACEDP
engagement and the anchor that downstream specifications reference.

## Role in ACEDP

The Project Profile is established first and then consumed by later processes:
Customer Discovery (SPEC-002) enriches it, Engineering Review (SPEC-003)
validates it, and the POC Deliverable (SPEC-004) is scoped against it. It is
the single record that ties an engagement together.

## Information Captured (categories)

This specification defines the *categories* of information a profile holds.
Concrete field names, types, and validation are intentionally deferred to a
dedicated schema (not part of this milestone).

- Identity — a stable project identifier and human-readable name.
- Objective — the engineering outcome the project is meant to achieve.
- Scope — what is in scope and, explicitly, what is out of scope.
- Constraints — known technical, operational, or timing constraints.
- Stakeholders — the roles responsible for direction and approval.
- Success Criteria — the conditions under which the project is judged complete.

## Lifecycle

A profile is created in `Draft`, refined through discovery, and moves to
`Approved` only after Engineering Review. Once approved, scope changes are made
through a new revision rather than silent edits, preserving traceability.

## Constraints

The Project Profile records facts about a project. It must not contain invented
customer information or assumed requirements. Unknowns are recorded as open
questions, not filled with defaults.

## Deferred

- The machine-readable schema for the profile (`schemas/`) is deferred.
- Example profiles under `acedp/examples/` are deferred until the schema exists.

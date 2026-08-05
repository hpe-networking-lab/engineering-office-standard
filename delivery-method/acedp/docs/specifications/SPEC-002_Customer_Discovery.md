# Customer Discovery

- Document ID: SPEC-002
- Status: Approved
- Version: 1.0
- Approved By: lead_architect (technical approval)
- Approval Date: 2026-06-30

## Purpose

Define the Customer Discovery process: how engagement context is gathered and
recorded so that the Project Profile (SPEC-001) is complete and accurate before
engineering work proceeds.

## Scope

Covers the gathering, recording, and validation of customer-provided context.
It does not define the Project Profile structure (SPEC-001) and does not produce
customer deliverables.

## Required Inputs

- An initialised Project Profile (SPEC-001).
- Customer-provided information (objectives, constraints, environment context).
- Access to the people authorised to answer engagement questions.

## Required Outputs

- A discovery record that enriches the Project Profile with confirmed facts.
- An explicit list of unknowns and assumptions, each marked as unresolved.

## Review / Approval Rules

- Discovery is reviewed for completeness before Engineering Review (SPEC-003).
- Only confirmed facts are recorded as facts; gaps remain open questions.
- Invented or assumed customer information is prohibited.

## Open Questions

- What is the minimum discovery completeness required to exit this stage?
  - Disposition: Accepted — owner: lead_architect, rationale: completeness is judged per engagement at Engineering Review; a fixed global threshold is not required, revisit: if a standard threshold proves necessary.
- How are conflicting inputs from different customer stakeholders reconciled?
  - Disposition: Accepted — owner: lead_architect, rationale: conflicts are recorded as open questions/assumptions and resolved at discovery review, revisit: if a formal reconciliation procedure is needed.

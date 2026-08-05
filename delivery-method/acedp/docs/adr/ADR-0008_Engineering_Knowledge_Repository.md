# Engineering Knowledge Repository

- Document ID: ADR-0008
- Status: Approved
- Version: 1.0
- Approved By: lead_architect (technical approval), product_owner (final acceptance)
- Approval Date: 2026-06-30

## Purpose (Why it exists)

Record the decision to maintain an Engineering Knowledge Repository (EKR) as the
single authoritative source of engineering knowledge for ACEDP. The EKR exists
so that standards, specifications, decisions, and reference knowledge are
traceable, reviewable, and durable across contributors and across AI/human
handoffs, rather than living in transient conversation.

## Scope — What it contains / What it must not contain

Contains: controlled engineering documents (STD, SPEC, ADR, EKR), their
metadata and version history, recorded decisions and rationale, and supporting
reference material.

Must not contain: generated configuration, deployment workflows, executable
implementation code, machine-specific secrets or credentials, assumed or
invented customer information, or platform-specific operational content that has
not been introduced through an approved artifact.

## Decision

Engineering knowledge is committed to the repository under `acedp/`, organised
by document class, with permanent IDs and git history as the source of truth.
Knowledge that is not captured here is not considered authoritative.

## Handoff (ChatGPT / Claude)

The EKR is the shared contract between the Lead Architect (ChatGPT) and the
Implementation Engineer (Claude). The architect's intent is recorded as
approved STD/SPEC/ADR artifacts; the implementer works only from those
artifacts. Because state lives in the repository rather than in any single
conversation, either party can resume from the committed record without loss of
context, and every change is attributable through git history.

## Required Inputs

- Approved engineering artifacts and recorded decisions.
- A consistent classification and ID scheme (STD-001 / EKR-001).

## Required Outputs

- A durable, traceable, reviewable record of engineering knowledge.
- A reliable handoff surface between architect and implementer.

## Review / Approval Rules

- New knowledge enters via the Engineering Review process (SPEC-003).
- Content violating the "must not contain" boundary is rejected at review.

## Open Questions

- How are superseded decisions retained without cluttering the active set?
  - Disposition: Accepted — owner: lead_architect, rationale: STD-001 'Superseded' status already provides retention; refinement is non-blocking, revisit: when the first decision is superseded.
- Should cross-repository knowledge (if ACEDP later separates from ACEM) be
  linked by reference or mirrored?
  - Disposition: Accepted — owner: product_owner, rationale: contingent on a future repository-separation decision that has not been made, revisit: if/when ACEDP separates from ACEM.

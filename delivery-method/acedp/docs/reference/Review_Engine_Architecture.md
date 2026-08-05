# Review Engine Architecture

- Document ID: REF-REVIEWENG-001
- Status: Draft
- Version: 0.1
- Last Updated: 2026-07-01
- Related: REF-WFLOW-ENGINE-001, REF-STATEMGR-001, REF-RPKG-001, REF-PLATFORM-001,
  REF-AICOLLAB-001, SPEC-003, SPEC-008

> Architecture document only. It designs the runtime service that prepares,
> tracks, and records reviews. It contains no implementation, code, schema,
> automation, customer data, or Mist interaction, and modifies no approved
> artifact.

## 1. Purpose

Design the Review Engine: the runtime service that prepares, tracks, and records
engineering reviews using Review Packages (REF-RPKG-001), validation evidence,
findings, dispositions, and approval decisions. It operationalises the SPEC-003
Engineering Review process — preparing the evidence for a decision and recording
the outcome — while the decision itself is made by ChatGPT (technical) and the
human (final approval).

## Design Requirements

- The Review Engine **prepares review evidence but does not approve work**.
- **ChatGPT performs technical review**.
- **Human / Product Owner performs final approval** where required.
- **Claude never self-approves**.
- **Review Packages are the handoff contract**.
- **Review decisions are recorded in Git**.
- **Blocking findings prevent approval** until resolved or waived.
- **Approved artifacts are never modified in place**.

## 2. Responsibilities

- Assemble the review evidence for an artifact (conformance results, review
  package, prior findings/dispositions).
- Track a review's status through its lifecycle.
- Record the review decision, findings, and dispositions to Git.
- Enforce that no artifact with an open blocking finding is Approved.
- Route the decision to ChatGPT (technical) and the human (final approval); make
  no decision itself.

## 3. Relationship to Workflow Engine

The Workflow Engine routes a "needs-review" work item to the Review Engine. The
Review Engine prepares/records the review and returns its outcome; the engine then
advances state. The Review Engine executes no workflow.

## 4. Relationship to State Manager

The Review Engine reads review-relevant state from the State Manager (an artifact
is conformant and In Review) and writes the recorded decision back as committed
evidence, which the State Manager then reflects. The Review Engine holds no
authoritative state of its own.

## 5. Relationship to Validation Engine

The Review Engine requires the artifact to be conformant (Validation Engine,
SPEC-008) before review begins — validation is the precondition. It never
reinterprets or bypasses validation results; a non-conformant artifact is not
reviewable.

## 6. Relationship to Review Packages

The Review Package (REF-RPKG-001) is the hand-off contract. The Review Engine
consumes the package (commit reference, files changed, validation evidence, design
decisions, risks, questions, approval request) and records the review against it.
Reviews are conducted from the committed state the package pins, not from pasted
logs.

## 7. Review Inputs

- A conformant artifact and its Review Package.
- The validation evidence for the artifact.
- The applicable standards (STD-001/STD-001.1) and the SPEC-003 authority matrix.
- Prior findings and dispositions, if the artifact was previously reviewed.

## 8. Review Outputs

- A recorded review decision: Approved or Rejected.
- Findings with severities and their dispositions
  (resolved / waived / accepted).
- The deciding authority and, where applicable, the human-gate grant.
- All committed to Git as the authoritative record.

## 9. Finding Model

A finding records: an identifier, a severity (blocking / major / minor /
informational), a location, the rule or concern, and a message. A **blocking**
finding is one that prevents a mandatory criterion, violates a binding standard,
or breaches an ADR-0008 boundary (per SPEC-003). Non-blocking findings do not, by
themselves, prevent approval.

## 10. Disposition Model

Each finding/open question is dispositioned during review:

- **Resolved** — addressed; resolution reference recorded.
- **Waived** — a blocking item set aside with recorded justification by the
  approval authority.
- **Accepted** — a non-blocking item carried into approval with owner, rationale,
  and revisit condition.

An artifact may be Approved carrying accepted items, but not with an open blocking
finding.

## 11. Approval Decision Model

- **Technical decision:** ChatGPT (lead_architect) approves or rejects per the
  SPEC-003 matrix.
- **Final approval:** the human (product_owner) grants the applicable gate
  (B/C/D/E) where required.
- The Review Engine records both; it grants neither. Claude never self-approves.

## 12. Review Package Generation

Claude authors the Review Package per REF-RPKG-001; the Review Engine may assemble
the evidence portions (commit reference, files changed, validation results) to
support authoring, but the producer of the artifact writes the package and the
producer never approves it. The package is committed and pinned to a commit range.

## 13. Review Recording

The review decision, findings, and dispositions are recorded to Git as the
authoritative outcome (e.g. an Engineering Review record, SPEC-003). Approval sets
the artifact to Approved / Version 1.0 with the recorded authority; a change to an
approved artifact is a new revision, never an in-place edit.

## 14. Failure Handling

- **Open blocking finding:** approval is withheld; corrective work items are
  generated (fix / revise), and the artifact stays In Review.
- **Rejected review:** recorded with findings; the artifact returns to Draft for
  revision and is re-reviewed on a new commit.
- **Missing package or non-conformant artifact:** the review does not begin.

## 15. Service Interfaces (conceptual only)

Conceptual contracts (no code, no API):

    prepare_review(artifact, package, validation) -> ReviewContext
    record_decision(review_context, decision, findings, dispositions) -> commit
    open_blocking(review_context) -> Finding[]
    approval_state(artifact) -> {approved, authority, gate}

These describe the engine's boundaries; they are not an implementation.

## 16. Future Automation Boundaries

- The Review Engine is a preparation-and-recording component (REF-PLATFORM-001):
  it holds no approval authority and enforces the AI Collaboration Protocol.
- Future MCP orchestration may invoke it through its conceptual interfaces, bound
  by the same invariants.
- Any change that would let the Review Engine approve work, bypass a blocking
  finding, or modify an approved artifact is disallowed and would require a new,
  separately authorised specification.

## What the Review Engine Does NOT Do

- It does **not** approve work (ChatGPT/human decide; Claude never self-approves).
- It does **not** perform the engineering or author the artifact.
- It does **not** bypass validation or a blocking finding.
- It does **not** modify approved artifacts (immutable except by revision).
- It does **not** hold authoritative state outside Git.
- It does **not** interact with Mist, external systems, or customer data.

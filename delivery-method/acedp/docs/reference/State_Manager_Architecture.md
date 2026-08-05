# State Manager Architecture

- Document ID: REF-STATEMGR-001
- Status: Draft
- Version: 0.1
- Last Updated: 2026-07-01
- Related: REF-ENGMGR-001, REF-WFLOW-ENGINE-001, REF-STATE-001, REF-WORK-001,
  REF-PLATFORM-001, SPEC-003, SPEC-008

> Architecture document only. It designs the runtime service that computes state
> from committed content. It contains no implementation, code, schema, automation,
> customer data, or Mist interaction, and modifies no approved artifact.

## 1. Purpose

Design the State Manager: the runtime service that computes engagement, artifact,
validation, review, approval, and work-item state from committed repository
content. It is the computation layer that realises the Engagement State Model
(REF-STATE-001) and Work Item Model (REF-WORK-001) over a given engagement.

## Design Requirements

- **State is derived from Git**, not stored independently.
- The State Manager **does not execute work**.
- The State Manager **does not approve work**.
- The State Manager **does not modify approved artifacts**.
- The State Manager **computes state over an engagement membership set**.
- The State Manager **identifies ready, blocked, failed, needs-review, and
  complete work**.
- The **Workflow Engine consumes State Manager output**.

## 2. Responsibilities

- Read the committed artifacts of an engagement (via the Engagement Manager's
  membership) and compute the five state projections.
- Compute each artifact's lifecycle, validation, review, and approval state.
- Compute work-item state and the actionable classification (ready / blocked /
  failed / needs-review / complete).
- Detect blocking conditions.
- Serve computed state to the Workflow Engine; perform no execution and no
  approval.

## 3. Relationship to Engagement Manager

The Engagement Manager provides the **membership set** (which artifacts belong to
the engagement, REF-ENGMGR-001). The State Manager computes state **over that
set** only; it does not decide membership.

## 4. Relationship to Workflow Engine

The Workflow Engine consumes the State Manager's output to evaluate a Workflow
Definition and generate eligible work items. The State Manager computes; the
engine routes and advances. The State Manager never executes or approves.

## 5. Relationship to Work Items

The State Manager computes the state of each work item (Waiting / Ready / Running
/ Blocked / Needs Review / Approved / Complete / Failed / Superseded per
REF-WORK-001) from the artifact and gate states, but it does not perform the work
items.

## 6. State Inputs

- The engagement membership set (from the Engagement Manager).
- The committed artifact instances and their references.
- Validation results (from the Validation Engine, SPEC-008).
- Recorded review decisions and dispositions (SPEC-003).
- Recorded approvals and human-gate grants.
- The selected Workflow Definition (for stage context).

All inputs are read from committed content; nothing is authored here.

## 7. State Projections

The State Manager produces the five projections of REF-STATE-001:

    Artifact lifecycle → Validation → Review → Approval → Work-item / next-action

Each is a pure function of the committed inputs; the projections together answer
what is done, what is pending, and what may be done next.

## 8. Artifact State Computation

For each artifact in the membership set, the lifecycle state is derived:

- **Draft** — present, not yet conformant.
- **Validated** — conformant to its schema.
- **In Review** — conformant with an open review package.
- **Approved** — reviewed and approved (Version 1.0, recorded authority).
- **Superseded** — replaced by a later revision.

The computation reads the artifact's metadata/status and the recorded
validation/review/approval evidence.

## 9. Validation State Computation

Per artifact: the last validation result — conformant / non-conformant /
not-yet-validated — with its findings and whether single-file and cross-document
resolution passed. An artifact is not eligible beyond Validated until conformant.

## 10. Review State Computation

Per artifact: not-submitted / in-review / reviewed, with the decision
(approved / rejected / pending) and the findings and their dispositions
(resolved / waived / accepted). An open blocking finding prevents approval.

## 11. Approval State Computation

Per artifact: approved (true/false) with the deciding authority (per the SPEC-003
matrix) and the review reference, plus whether the applicable human gate (B/C/D/E)
has been granted. The State Manager records these; it never grants them.

## 12. Work Item State Computation

From the artifact and gate states and the Workflow Definition, the State Manager
computes each work item's state and the actionable classification:

- **ready** — preconditions met, owner may act;
- **blocked** — a blocking condition applies;
- **failed** — could not complete; retry-eligible;
- **needs-review** — output conformant, awaiting ChatGPT;
- **complete** — criteria met and committed.

This classification is the primary output the Workflow Engine consumes.

## 13. Blocking Condition Detection

The State Manager flags an item/artifact as blocked when:

- an artifact is non-conformant (validation failed);
- an open blocking finding exists;
- a required human gate has not been granted;
- a required predecessor artifact is not yet approved;
- a reference does not resolve (internal or cross-document).

Blocks are reported, not resolved.

## 14. Recovery and Recomputation

State is recomputed from the committed repository on demand; there is no separate
store to reconcile. On restart or after any commit, the State Manager recomputes
identically (deterministic), so recovery is from Git alone and lossless.

## 15. Service Interfaces (conceptual only)

Conceptual contracts (no code, no API):

    compute_engagement_state(membership, commit) -> EngagementState
    artifact_states(membership, commit) -> ArtifactState[]
    work_item_states(state, workflow) -> WorkItemState[]
    blocking_conditions(state) -> Block[]
    actionable(state) -> {ready[], blocked[], failed[], needs_review[], complete[]}

These describe the manager's boundaries; they are not an implementation.

## 16. Future Automation Boundaries

- The State Manager is a computation component (REF-PLATFORM-001): it holds no
  approval authority and enforces the AI Collaboration Protocol.
- Future MCP orchestration may query it through its conceptual interfaces, bound by
  the same invariants.
- Any change that would let the State Manager execute work, approve work, or modify
  approved artifacts is disallowed and would require a new, separately authorised
  specification.

## What the State Manager Does NOT Do

- It does **not** execute work items (the owners act; the engine routes).
- It does **not** approve work (ChatGPT/human decide; Claude never self-approves).
- It does **not** produce or modify artifacts — approved or otherwise.
- It does **not** decide engagement membership (that is the Engagement Manager).
- It does **not** validate content itself (it reads Validation Engine results).
- It does **not** hold authoritative state outside Git.
- It does **not** interact with Mist, external systems, or customer data.

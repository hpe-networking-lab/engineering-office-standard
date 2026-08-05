# Engagement State Model

- Document ID: REF-STATE-001
- Status: Draft
- Version: 0.1
- Last Updated: 2026-07-01
- Related: REF-PLATFORM-001, REF-PIPELINE-001, REF-ORCH-001, REF-AICOLLAB-001,
  SPEC-003, SPEC-008

> Model/architecture document only. It defines the engagement state model the
> platform will use. It contains no code, no new schema, no automation, no
> customer data, and no Mist interaction, and modifies no approved artifact.

## 1. Purpose

Define the core state model the ACEDP platform uses to track an engagement across
its artifacts, validation, review, approvals, milestones, and next actions. The
model is descriptive: it names the state that must be knowable at any moment; it
does not create a schema or implement anything. Because Git is the source of
truth, the model is a **projection** of the committed repository, not a separate
store.

## 2. Engagement Definition

An **engagement** is one unit of ACEDP work for one (fictional or real) customer:
the set of artifacts produced as it moves through the pipeline, together with
their validation, review, and approval state. An engagement has a stable
identity, a membership of artifacts, and a current position in the pipeline. The
sample engagement (acedp/examples/sample_engagement) is a concrete example.

## 3. State Model Overview

The engagement state is composed of five projections over its artifacts:

    Artifact lifecycle  →  Validation  →  Review  →  Approval  →  Milestone/next-action

Each artifact carries a lifecycle state; validation, review, and approval states
qualify it; the engagement-level milestone and next-action are derived from the
aggregate. All of it is computed from the committed repository.

## 4. Engagement Identity

- **engagement_id:** a stable identifier for the engagement.
- **customer_ref:** the (fictional/real) customer the engagement serves.
- **anchor:** the Project Profile (SPEC-001) instance that anchors it; its
  profile_id ties the engagement together.
- **location:** the repository path (lab or customer repository) holding the set.

Identity is stable for the life of the engagement; artifacts join it by
referencing the anchor (directly or transitively).

## 5. Artifact Registry

The registry is the membership of the engagement: the artifacts that belong to it
and their identities.

- Each entry: artifact type (SPEC-00x), instance id (e.g. profile_id), file path,
  and the references that link it into the engagement.
- Membership is determined by the reference chain back to the anchor Project
  Profile (validated by cross-document reference resolution).
- The expected set spans SPEC-001, 002, 003, 005, 006, 007 (and future artifacts).

## 6. Artifact Lifecycle State

Each artifact is in exactly one lifecycle state:

    Draft → Validated → In Review → Approved → Superseded

- **Draft:** produced, not yet conformant.
- **Validated:** conformant to its schema (Validation Engine passed).
- **In Review:** submitted with a review package (SPEC-003).
- **Approved:** reviewed and approved; Version 1.0; recorded authority.
- **Superseded:** replaced by a later revision (retained for traceability).

Transitions are guarded (Section 12) and are only realised by a commit.

## 7. Validation State

Per artifact: the result of the last validation.

- **status:** conformant / non-conformant / not-yet-validated.
- **scope:** single-file and/or cross-document (context set).
- **findings:** error/warning findings from the Validation Engine.
- An artifact cannot advance beyond Validated until its validation status is
  conformant (the first automated quality gate).

## 8. Review State

Per artifact: the Engineering Review status.

- **status:** not-submitted / in-review / reviewed.
- **decision:** approved / rejected / pending.
- **findings + dispositions:** blocking/non-blocking findings and their
  disposition (resolved / waived / accepted).
- An artifact with an open blocking finding cannot be approved.

## 9. Approval State

Per artifact: whether approval is complete and by whom.

- **approved:** true/false, with the deciding authority (per the SPEC-003 matrix)
  and the review reference.
- **gate:** whether the applicable human gate (B/C/D/E) has been granted.
- Approval requires both the technical decision (lead_architect) and, where
  applicable, the human gate (product_owner). Claude never self-approves.

## 10. Milestone / Work State

Engagement-level, derived from the artifact states:

- **current_stage:** the pipeline stage in progress (Intake … Mist Intent).
- **current_milestone:** the milestone being executed.
- **completed:** stages/artifacts already approved.
- **waiting:** work that is blocked or pending (validation, review, or a gate).

## 11. Next-Action Model

The model computes, from the aggregate state, the next authorised actions:

- **What can Claude do next:** produce or correct an artifact whose predecessors
  are approved and whose own state is Draft/Validated (e.g. generate the next
  artifact, fix findings, write the review package).
- **What requires ChatGPT review:** any artifact that is Validated and submitted
  (In Review) with an open review package.
- **What requires human approval:** any artifact at a human gate (B/C/D/E) — real
  data use, business acceptance, implementation authorisation, deliverable
  acceptance.

Only one class of action is offered per artifact at a time, consistent with the
lifecycle guards.

## 12. Blocking Conditions

An engagement (or artifact) is blocked when:

- an artifact is non-conformant (validation failed);
- an open blocking finding exists (review);
- a required human gate has not been granted;
- a required predecessor artifact is not yet approved;
- a reference does not resolve (internal or cross-document).

A blocked artifact cannot advance; the block is recorded and surfaced in the
next-action model.

## 13. Recovery / Resume Behavior

- The state is always recomputed from the committed repository — there is no
  separate authoritative store to corrupt.
- **Resume:** load the committed engagement set, recompute the five projections,
  and continue from the last approved artifact and its recorded review.
- **Interrupted work:** the last commit is the recovery point; in-progress
  artifacts are re-validated before advancing.
- **Revision:** an approved artifact changes only by a new revision; the prior
  revision is retained as Superseded.

## 14. Relationship to Git

- Git is the single source of truth; the engagement state is a projection of the
  committed repository, never a competing store.
- Lifecycle transitions are realised by commits; a review package pins the commit
  under review.
- Approved artifacts are immutable except by revision; history preserves every
  prior state.

## 15. Future Automation Use

- A future State Manager / Workflow Engine (REF-PLATFORM-001) computes this model
  from the repository and drives the pipeline through it, honouring the gates and
  the AI Collaboration Protocol.
- Automation reads and advances state but holds no approval authority; the human
  gates and the "Claude never self-approves" rule are preserved.
- The model requires a schema only when it is later persisted; that schema would
  be authored and approved through the normal ACEDP process (not in this
  milestone).

## Questions the Model Answers

| Question | Answered by |
|---|---|
| What is an engagement? | Section 2 (Engagement Definition) |
| What artifacts belong to it? | Section 5 (Artifact Registry) |
| What state is each artifact in? | Section 6 (Lifecycle State) |
| What validation has passed? | Section 7 (Validation State) |
| What review is pending? | Section 8 (Review State) |
| What approvals are complete? | Section 9 (Approval State) |
| What milestone is current? | Section 10 (Milestone/Work State) |
| What work is waiting? | Sections 10 and 12 |
| What can Claude do next? | Section 11 (Next-Action Model) |
| What requires ChatGPT review? | Section 11 (Next-Action Model) |
| What requires human approval? | Sections 11 and 9 (gates) |

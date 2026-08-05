# Work Item Model

- Document ID: REF-WORK-001
- Status: Draft
- Version: 0.1
- Last Updated: 2026-07-01
- Related: REF-STATE-001, REF-PLATFORM-001, REF-PIPELINE-001, REF-AICOLLAB-001,
  SPEC-003, SPEC-008

> Model/architecture document only. It defines the work item model. It contains
> no code, no new schema, no automation, no customer data, and no Mist
> interaction, and modifies no approved artifact.

## 1. Purpose

Define the model that represents actionable work inside an engagement. Artifacts
are the outputs of work; **work items** describe what Claude, ChatGPT, or a human
must do next to move the engagement forward. The model is descriptive: it names
the shape and states of work items; it does not create a schema or implement
anything.

## 2. Work Item Definition

A **work item** is a single unit of actionable work with an owner, inputs,
outputs, preconditions, completion criteria, and a state. It is derived from the
engagement state (REF-STATE-001): where the state model says what *is*, the work
item model says what must be *done next*.

## 3. Relationship to Engagements

Work items belong to exactly one engagement and reference its identity. The set
of open work items is the engagement's actionable backlog; completing them
advances the engagement through the pipeline stages and gates.

## 4. Relationship to Artifacts

Each work item targets zero or more artifacts: it either produces a new artifact,
modifies (revises) one, validates one, reviews one, or approves one. Artifacts
are the outputs; work items are the verbs that create or transition them.

## 5. Work Item Identity

- **work_item_id:** stable identifier within the engagement.
- **engagement_ref:** the engagement it belongs to.
- **target_artifacts:** the artifact(s) it produces or acts on.
- **type + owner:** the kind of work and who performs it.

## 6. Work Item Types

- **produce_artifact** — generate a new framework artifact.
- **validate_artifact** — run the Validation Engine on an artifact.
- **fix_findings** — correct validation or review findings.
- **author_review_package** — write the review package (REF-RPKG-001).
- **engineering_review** — conduct SPEC-003 review.
- **request_gate_approval** — request a human approval gate (B/C/D/E).
- **revise_artifact** — create a new revision of an approved artifact.
- **produce_report** — generate an execution/summary report.

## 7. Work Item Ownership

- **Claude (Implementation Engineer):** produce_artifact, validate_artifact,
  fix_findings, author_review_package, revise_artifact, produce_report.
- **ChatGPT (Lead Architect):** engineering_review.
- **Human (Product Owner):** request_gate_approval decisions.

Claude never self-approves: approval-bearing work items are owned by ChatGPT
(technical) and the human (gates), never by Claude.

## 8. Inputs and Outputs

- **Inputs:** the approved upstream artifacts, the target schema, validation
  results, and (for review) the review package.
- **Outputs:** a produced/updated artifact, a validation result, a review
  decision, or a granted gate — always realised by a commit.

## 9. Dependencies

A work item may depend on other work items (e.g. validate depends on produce;
review depends on a conformant artifact + package; approval depends on review). A
dependency must be Complete before the dependent becomes Ready.

## 10. Preconditions

A work item's preconditions are the conditions required to start it: its
dependencies are Complete, its inputs exist and are approved where required, and
no blocking condition applies. Unmet preconditions leave the item Waiting.

## 11. Blocking Conditions

A work item is Blocked when:

- a target artifact is non-conformant (validation failed);
- an open blocking finding exists;
- a required human gate has not been granted;
- a required predecessor artifact is not yet approved;
- a reference does not resolve.

## 12. Completion Criteria

A work item is Complete only when its output meets its criteria:

- produced/revised artifacts are conformant (validation passed);
- reviewed artifacts have a recorded decision with no open blocking finding;
- approval-bearing items have the recorded authority and (where applicable) the
  human gate;
- the result is committed.

## 13. Review Requirements

Every artifact-producing work item ends with an Engineering Review (SPEC-003):
Claude submits a review package; ChatGPT reviews from the committed state; the
item cannot be Complete until the review decision is recorded.

## 14. Approval Requirements

Approval-bearing work items require the SPEC-003 authority (lead_architect
technical) and, where the stage has a human gate, the product_owner decision.
Approval is never self-granted by the producer.

## 15. Retry and Recovery Behavior

- A Failed item (e.g. validation could not be made conformant, or review was
  rejected) is retried: fix the cause, re-validate/re-review on a new commit.
- Recovery uses the committed state as the resume point; in-progress items are
  re-derived from the repository.
- A superseded artifact's work items become Superseded; new revision work items
  are created.

## 16. Work Item State Transitions

States:

- **Waiting** — preconditions/dependencies not yet met.
- **Ready** — preconditions met; may start.
- **Running** — in progress.
- **Blocked** — a blocking condition applies.
- **Needs Review** — output produced; awaiting ChatGPT review.
- **Approved** — review and any human gate granted.
- **Complete** — completion criteria met and committed.
- **Failed** — could not complete; eligible for retry.
- **Superseded** — replaced (e.g. its target artifact was revised).

Transitions:

    Waiting → Ready → Running → Needs Review → Approved → Complete
                 │         │           │
                 ▼         ▼           ▼
              Blocked   Failed → (retry) Ready
    any state → Superseded (on revision of the target)

Guards: Running → Needs Review requires a conformant artifact + review package;
Needs Review → Approved requires the SPEC-003 decision and any human gate;
Approved → Complete requires the commit.

## 17. Next-Action Derivation

From the open work items and their states, the model derives the actionable set:

- **What Claude can do next:** Ready work items owned by Claude (produce,
  validate, fix, author package, revise, report).
- **What requires ChatGPT review:** Needs Review items (engineering_review).
- **What requires human approval:** items at a human gate
  (request_gate_approval).
- **What is Blocked / Complete:** items in those states.
- **What can be retried:** Failed items.

Exactly one actionable class is offered per artifact at a time, consistent with
the guards.

## 18. Future Automation Use

A future Workflow Engine (REF-PLATFORM-001) computes work items from the
engagement state and drives them through their transitions, honouring ownership,
review, gates, and the AI Collaboration Protocol. Automation advances work items
but holds no approval authority. A persistence schema for work items would be
authored and approved through the normal ACEDP process — not in this milestone.

## Questions the Model Answers

| Question | Answered by |
|---|---|
| What work can Claude do next? | Sections 7, 17 (Claude-owned Ready items) |
| What requires ChatGPT review? | Sections 13, 17 (Needs Review) |
| What requires human approval? | Sections 14, 17 (gate items) |
| What is blocked? | Sections 11, 16 (Blocked) |
| What is complete? | Sections 12, 16 (Complete) |
| What can be retried? | Sections 15, 16 (Failed) |
| What artifacts will be produced or modified? | Sections 4, 8 (target_artifacts) |
| What validation must pass before completion? | Sections 12, 13 (conformance) |

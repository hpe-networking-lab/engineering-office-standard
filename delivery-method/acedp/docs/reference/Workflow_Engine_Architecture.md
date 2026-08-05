# Workflow Engine Architecture

- Document ID: REF-WFLOW-ENGINE-001
- Status: Draft
- Version: 0.1
- Last Updated: 2026-07-01
- Related: REF-WFLOW-001, REF-WFLOW-DEFAULT-001, REF-STATE-001, REF-WORK-001,
  REF-PLATFORM-001, REF-AICOLLAB-001, SPEC-003, SPEC-008

> Architecture document only. It designs the runtime that executes declarative
> workflows. It contains no implementation, code, schemas, automation, MCP
> implementation, GitHub Actions, customer data, or Mist interaction, and modifies
> no approved artifact.

## 1. Purpose

Design the Workflow Engine: the runtime component that executes Workflow
Definitions (REF-WFLOW-001) by computing Engagement State (REF-STATE-001),
generating eligible Work Items (REF-WORK-001), and coordinating validation,
review, and approval — deterministically and recoverably. The engine holds **no
engineering knowledge**; it executes declarative workflows.

## Core Invariants

- The engine **loads a Workflow Definition** and evaluates it.
- It **computes Engagement State** from the committed repository.
- It **generates eligible Work Items** for the active stages.
- It **never contains engineering-specific logic**.
- It **never directly modifies approved artifacts**.
- It **never bypasses validation**.
- It **never bypasses ChatGPT review**.
- It **never bypasses required human approval**.
- It **can always recover from Git alone**.
- It is **deterministic and idempotent**.

## 2. Responsibilities

- Load and interpret a Workflow Definition (by id + version).
- Compute the engagement's state from the committed repository.
- Evaluate stage dependencies and entry/exit conditions.
- Generate the eligible work items and hand them to their owners.
- Coordinate the gates (validation, review, human approval) without performing the
  engineering itself.
- Advance stage/work-item states only via commits.

## 3. Relationship to Workflow Definitions

The engine reads a Workflow Definition as declarative input; it does not embed any
workflow. Different definitions (platform default, customer-specific) are executed
by the same engine. A definition is immutable once approved; the engine pins the
version an engagement runs.

## 4. Relationship to Engagement State

The engine computes the five projections of REF-STATE-001 from the committed
repository each cycle. The state is a projection, never a competing store, so the
engine's view is always reconcilable with Git.

## 5. Relationship to Work Items

From the active stages and state, the engine derives the current work items
(REF-WORK-001), each with an owner, and offers them to Claude, ChatGPT, or the
human. The engine tracks work-item states but does not perform Claude's or
ChatGPT's work.

## 6. Relationship to Validation Engine

The engine invokes the Validation Engine (SPEC-008) as the first quality gate: an
artifact-producing work item cannot complete until its output is conformant. The
engine never bypasses or reinterprets validation results.

## 7. Relationship to Review Engine

The engine routes conformant artifacts (with review packages) to ChatGPT for
Engineering Review (SPEC-003) and records the decision. It never approves on
ChatGPT's behalf and never bypasses review.

## 8. Relationship to Human Approval

The engine surfaces the human approval gates (B/C/D/E) and waits for the
product_owner decision. It cannot grant a gate itself and never bypasses a
required human approval.

## 9. Runtime Execution Loop

Each cycle is a pure evaluation over the committed state:

    1. Load the selected Workflow Definition.
    2. Compute Engagement State from the committed repository.
    3. Evaluate stage dependencies and entry conditions.
    4. Generate the set of eligible Work Items.
    5. Route each Work Item to its owner (Claude / ChatGPT / human).
    6. Observe committed results; recompute state; repeat.

The loop performs no engineering; it computes and routes. A cycle over an
unchanged commit yields the same eligible set (idempotent).

## 10. Scheduling Model

- Work items are scheduled by eligibility: a work item is offered only when its
  preconditions are met and no blocking condition applies.
- Independent stages (per the definition) yield concurrently-eligible work items;
  dependent stages are gated in order.
- The engine does not force timing; it offers eligible work and waits for
  committed results.

## 11. Dependency Evaluation

The engine evaluates each stage's declared dependencies against the state: a stage
becomes active only when its dependencies' exit conditions hold. Reference
integrity (internal and cross-document) is part of dependency evaluation.

## 12. State Transitions

The engine advances lifecycle and work-item states strictly through the guarded
transitions of REF-STATE-001 / REF-WORK-001, and only as a consequence of a
commit. It never sets an Approved state without the recorded review authority and
any human gate.

## 13. Pause and Resume Behavior

- **Pause:** the engine can stop at any point; no state lives outside Git.
- **Resume:** on restart, the engine recomputes state from the committed
  repository and continues offering eligible work — no bespoke checkpoint is
  needed.

## 14. Failure Recovery

- A failed work item (non-conformant, rejected, or gate denied) leaves the stage
  active with corrective work items; dependents do not start.
- Recovery is always from Git alone: recompute state, re-derive eligible work,
  continue.

## 15. Idempotency and Determinism

- **Deterministic:** the same Workflow Definition over the same commit yields the
  same state, the same eligible work items, and the same routing.
- **Idempotent:** re-running a cycle without new commits changes nothing; offering
  an already-satisfied work item is a no-op.
- The engine introduces no randomness and no external side effects.

## 16. Service Interfaces (conceptual only)

Conceptual contracts (no code, no API):

    load_workflow(workflow_id, version) -> WorkflowDefinition
    compute_state(repository_commit)    -> EngagementState
    eligible_work_items(definition, state) -> WorkItem[]
    route(work_item) -> owner            # Claude / ChatGPT / human
    observe(commit) -> EngagementState   # recompute after a result

These describe the engine's boundaries; they are not an implementation.

## 17. Event Model (conceptual only)

Conceptually, the engine reacts to one event: a **new commit**. A commit triggers
a recompute-and-route cycle. Higher-level events (work-item-ready, review-recorded,
gate-granted) are derived from the committed state, not from an external event bus.

## 18. Future Automation Boundaries

- The engine is an orchestration component only (REF-PLATFORM-001); it holds no
  approval authority and enforces the AI Collaboration Protocol.
- Future MCP orchestration or GitHub automation may invoke the engine, but through
  its conceptual interfaces and bound by the same invariants.
- Any change that would give the engine engineering authority, or let it bypass a
  gate, is disallowed and would require a new, separately authorised specification.

## What the Workflow Engine Does NOT Do

- It does **not** contain engineering knowledge or make engineering decisions.
- It does **not** produce or edit artifacts (Claude produces; the engine routes).
- It does **not** modify approved artifacts (immutable except by revision).
- It does **not** validate content itself (it invokes the Validation Engine).
- It does **not** review artifacts (ChatGPT reviews).
- It does **not** grant approvals (ChatGPT/human decide; Claude never self-approves).
- It does **not** bypass validation, review, or human approval gates.
- It does **not** hold state outside Git or introduce non-determinism.
- It does **not** interact with Mist, external systems, or customer data.

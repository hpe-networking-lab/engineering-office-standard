# Workflow Definition Model

- Document ID: REF-WFLOW-001
- Status: Draft
- Version: 0.1
- Last Updated: 2026-07-01
- Related: REF-WORK-001, REF-STATE-001, REF-PLATFORM-001, REF-PIPELINE-001,
  REF-AICOLLAB-001, SPEC-003, SPEC-008

> Model/architecture document only. It defines the workflow definition model. It
> contains no workflow engine, no automation, no schema, no customer data, and no
> Mist interaction, and modifies no approved artifact.

## 1. Purpose

Define the model for reusable engineering workflows. A **Workflow Definition**
declares the stages an engagement passes through and the gates between them. It
produces **Work Items** (REF-WORK-001), which are computed into **Engagement
State** (REF-STATE-001) and ultimately executed by the future Workflow Engine. A
Workflow Definition is declarative: it describes what should happen, not how to
run it.

## Workflow Principles

- Workflows are **declarative**.
- Workflows **generate Work Items**.
- Workflows **never execute work**.
- Workflow **execution belongs to the future Workflow Engine**.
- Workflow Definitions are **immutable once approved**.
- Workflow **versions are explicit**.
- **Multiple workflow definitions may exist**.
- **Customer-specific workflows are separate** from the platform workflow library.

## 2. Workflow Definition

A Workflow Definition is a named, versioned, declarative description of an ordered
set of stages, each with inputs, outputs, dependencies, entry/exit conditions, and
gates (validation, review, human approval). The default platform workflow is the
approved ACEDP pipeline (Intake → Discovery → Engineering Review → Design →
Readiness → Mist Generation Intent).

## 3. Relationship to Engagements

An engagement selects exactly one Workflow Definition (by id + version). The
workflow determines the stages the engagement will pass through; the engagement's
state is interpreted against the selected workflow.

## 4. Relationship to Work Items

A stage, when its entry conditions are met, **generates work items** (produce,
validate, review, request-approval, etc.). The workflow never performs work — it
only declares which work items should exist at each stage.

## 5. Relationship to Artifacts

Each stage names the artifact(s) it expects to produce or consume (by schema).
Artifacts are the outputs; the workflow sequences the stages that create them.

## 6. Workflow Identity

- **workflow_id:** stable identifier for the definition.
- **version:** explicit workflow version (see Section 19).
- **scope:** platform-library workflow or customer-specific workflow.
- **stages:** the ordered stage list.

## 7. Workflow Stages

A stage is a named step with: an id, the artifact(s) it targets, its inputs and
outputs, dependencies, entry/exit conditions, and its gates. The default workflow's
stages correspond to the pipeline stages of REF-PIPELINE-001.

## 8. Stage Inputs

The approved upstream artifacts and context a stage requires (e.g. Design requires
an approved Project Profile and Customer Discovery). Inputs are declared by schema
and by required lifecycle state (usually Approved).

## 9. Stage Outputs

The artifact(s) a stage is expected to produce (e.g. Design produces a Design
Package, SPEC-005). Outputs are declared by schema; producing them is done by
generated work items, not by the workflow.

## 10. Stage Dependencies

A stage depends on prior stages: it becomes eligible only when its dependencies'
exit conditions are satisfied. Dependencies define the ordering and which stages
may run in parallel (Section 18).

## 11. Entry Conditions

The conditions that must hold for a stage to become active: its dependencies are
complete, its inputs exist at the required lifecycle state, and no blocking
condition applies. Entry conditions generate the stage's work items.

## 12. Exit Conditions

The conditions that mark a stage complete: its output artifact(s) are conformant,
reviewed, and approved as required, and committed. A stage's exit conditions are
the entry conditions for its dependents.

## 13. Validation Gates

Each stage declares a validation gate: its output must be conformant (Validation
Engine, SPEC-008) before it can proceed. A non-conformant output blocks the stage.

## 14. Review Gates

Each artifact-producing stage declares an Engineering Review gate (SPEC-003): the
output must be reviewed, with no open blocking finding, before the stage exits.

## 15. Human Approval Gates

Stages that cross a human decision declare a human approval gate (B/C/D/E per
REF-PIPELINE-001): real-data use, business acceptance, implementation
authorisation, deliverable acceptance. The stage cannot exit until the gate is
granted.

## 16. Failure Handling

When a stage fails (validation not conformant, review rejected, or gate denied),
the workflow declares the failure disposition: the stage remains active, its
corrective work items (fix/revise/re-review) are generated, and no dependent
stage may start. Failures never advance the workflow.

## 17. Resume Behavior

Because the workflow is declarative and the engagement state is a projection of
Git, execution resumes by re-evaluating the selected workflow against the
committed state: active stages and their work items are re-derived, and work
continues from the last approved artifact.

## 18. Branching and Optional Paths

- **Optional stages:** a stage may be declared optional/conditional (e.g. a POC
  Deliverable path, SPEC-004, applies only when the engagement requires it).
- **Parallel stages:** stages with no mutual dependency may run in parallel
  (their work items coexist).
- **Branches:** a workflow may declare alternative paths guarded by conditions;
  exactly one path is taken per engagement based on the guard.

## 19. Versioning

- Workflow versions are explicit (`workflow_id` + `version`).
- A Workflow Definition is **immutable once approved**; a change is a new version.
- An engagement pins the workflow version it runs, so in-flight engagements are
  unaffected by a later workflow revision.

## 20. Future Automation

The future Workflow Engine (REF-PLATFORM-001) reads a Workflow Definition,
evaluates it against the engagement state, generates the current work items, and
drives them through their gates — honouring validation, review, human approval,
and the AI Collaboration Protocol. The engine executes; the definition only
declares. A persistence schema for workflow definitions would be authored and
approved through the normal ACEDP process — not in this milestone.

## Questions the Model Answers

| Question | Answered by |
|---|---|
| What workflow applies? | Sections 3, 6 (selected workflow_id + version) |
| What stage is active? | Sections 7, 11 (entry conditions met) |
| What work items should exist? | Sections 4, 11 (stage-generated work items) |
| Which stages may run in parallel? | Sections 10, 18 (no mutual dependency) |
| Which stages are optional? | Section 18 (optional/conditional stages) |
| Which stages require review? | Section 14 (review gates) |
| Which stages require human approval? | Section 15 (human approval gates) |
| What happens when a stage fails? | Section 16 (failure handling) |
| How does execution resume? | Section 17 (resume behavior) |

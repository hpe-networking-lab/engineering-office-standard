# Default ACEDP Workflow

- Document ID: REF-WFLOW-DEFAULT-001
- Status: Draft
- Version: 0.1
- Last Updated: 2026-07-01
- Implements: REF-WFLOW-001 (Workflow Definition Model)
- Related: REF-PIPELINE-001, REF-STATE-001, REF-WORK-001, SPEC-001..SPEC-008

> Document only. A declarative, worked example of REF-WFLOW-001. It defines
> stages; it does not execute them. No engine, automation, schema, customer data,
> or Mist interaction, and modifies no approved artifact.

## 0. Governance

> **Governance note (2026-07-02):** the *approval mechanics* below — per-stage ChatGPT review and Gates A–D — are superseded by [`REF-OPMODEL-001` — ACEDP Operating Model](ACEDP_Operating_Model.md), which collapses them to a single human approval before any real-customer or real-Mist action. The **stages remain valid as a checklist** of what a good engagement produces; read the per-stage 'review/approval required' lines as retired.

## 1. Purpose

Provide the canonical engineering workflow that every standard ACEDP engagement
follows: the declarative sequence of stages, the work items each generates, and
the validation, review, and human-approval gates between them. This becomes the
reference workflow the future Workflow Engine evaluates.

## 2. Scope

Covers a standard engagement from intake through deployment. Stages 1–6 operate
within the approved framework and validation tooling. Stages 7–8 (implementation
and deployment) are declared for completeness but are gated on a future,
separately authorised Mist provisioning specification and are not executable
today.

## 3. Relationship to REF-WFLOW-001

This is a concrete Workflow Definition per REF-WFLOW-001: it is declarative,
generates work items, never executes work, is versioned and immutable once
approved, and lives in the platform workflow library (customer-specific
workflows, if any, are separate). Execution belongs to the future Workflow
Engine.

## 4. Workflow Overview

    Stage 1 Customer Discovery ─┐ (Intake, may run together)
    Stage 2 Project Profile ────┘
        → Stage 3 Engineering Review (review-only)
          → Stage 4 Design Package
            → Stage 5 Readiness Assessment
              → Stage 6 Mist Organization Intent
                → Stage 7 Implementation Authorization (approval-only; future spec)
                  → Stage 8 Deployment Complete (future spec)

Note: the Project Profile (SPEC-001) is the engagement anchor; Customer Discovery
(SPEC-002) enriches it. Stages 1 and 2 together form Intake.

## 5. Workflow Stages

### Stage 1 — Customer Discovery
- **Purpose:** gather and record engagement context (SPEC-002), enriching the
  Project Profile.
- **Required inputs:** an initialised Project Profile; customer-provided context.
- **Generated work items:** produce_artifact (discovery), validate_artifact,
  author_review_package.
- **Produced artifacts:** Customer Discovery (SPEC-002).
- **Validation required:** schema conformance; internal references.
- **ChatGPT review required:** Yes.
- **Human approval required:** Yes (Gate B — real-data use).
- **Exit criteria:** discovery Approved (conformant, reviewed, gate granted).
- **Failure conditions:** missing information; invented facts; non-conformant.
- **Recovery method:** record gaps as open questions; re-gather; re-validate.

### Stage 2 — Project Profile
- **Purpose:** establish/finalise the anchor Project Profile (SPEC-001).
- **Required inputs:** engagement objectives; confirmed discovery facts.
- **Generated work items:** produce_artifact (profile), validate_artifact,
  author_review_package.
- **Produced artifacts:** Project Profile (SPEC-001).
- **Validation required:** schema conformance; internal references.
- **ChatGPT review required:** Yes.
- **Human approval required:** Yes (product_owner, per the SPEC-003 matrix).
- **Exit criteria:** profile Approved.
- **Failure conditions:** incomplete profile; unresolved blocking finding.
- **Recovery method:** revise; re-validate; re-review.

### Stage 3 — Engineering Review  (review-only)
- **Purpose:** conduct SPEC-003 review of the engagement's artifacts and record
  decisions.
- **Required inputs:** conformant artifacts and their review packages.
- **Generated work items:** engineering_review; request_gate_approval where
  applicable.
- **Produced artifacts:** Engineering Review record (SPEC-003).
- **Validation required:** the review record itself is schema-conformant.
- **ChatGPT review required:** Yes (this stage is the review).
- **Human approval required:** Conditional (Gate C for business acceptance).
- **Exit criteria:** review decision recorded with no open blocking finding.
- **Failure conditions:** open blocking finding.
- **Recovery method:** resolve or waive findings; re-review.

### Stage 4 — Design Package
- **Purpose:** produce the design intent (SPEC-005) from approved profile and
  discovery.
- **Required inputs:** approved Project Profile and Customer Discovery.
- **Generated work items:** produce_artifact (design), validate_artifact,
  author_review_package.
- **Produced artifacts:** Design Package (SPEC-005).
- **Validation required:** conformance; internal references.
- **ChatGPT review required:** Yes.
- **Human approval required:** Conditional (Gate C).
- **Exit criteria:** Design Package Approved.
- **Failure conditions:** incomplete design; blocking finding.
- **Recovery method:** revise; re-validate; re-review.

### Stage 5 — Readiness Assessment
- **Purpose:** assess Mist organisation readiness (SPEC-006) of the approved
  design.
- **Required inputs:** approved Design Package.
- **Generated work items:** produce_artifact (readiness), validate_artifact,
  author_review_package.
- **Produced artifacts:** Mist Organization Readiness (SPEC-006).
- **Validation required:** conformance; threshold applied.
- **ChatGPT review required:** Yes.
- **Human approval required:** Yes (approval of a "ready" determination).
- **Exit criteria:** readiness Approved with determination "ready".
- **Failure conditions:** not_ready; open blocking gap.
- **Recovery method:** close gaps in the design; re-assess.

### Stage 6 — Mist Organization Intent
- **Purpose:** produce the generation intent (SPEC-007), traceable to the design.
- **Required inputs:** approved Design Package and "ready" readiness assessment.
- **Generated work items:** produce_artifact (intent), validate_artifact,
  author_review_package.
- **Produced artifacts:** Mist Organization Generation Intent (SPEC-007).
- **Validation required:** conformance; design_reference traceability.
- **ChatGPT review required:** Yes.
- **Human approval required:** Yes (Gate D — implementation authorisation, the
  SPEC-007 pre-implementation review).
- **Exit criteria:** intent Approved and implementation authorised.
- **Failure conditions:** upstream not approved; blocking finding.
- **Recovery method:** correct intent/upstream; re-review.

### Stage 7 — Implementation Authorization  (approval-only; future spec)
- **Purpose:** authorise and perform implementation from the approved intent.
- **Required inputs:** approved intent; a separate, approved Mist provisioning
  specification (not yet authored); Gate D authorisation.
- **Generated work items:** request_gate_approval; (future) produce_artifact for
  implementation records.
- **Produced artifacts:** (future) implementation records.
- **Validation required:** conformance of any produced records; boundary
  compliance.
- **ChatGPT review required:** Yes.
- **Human approval required:** Yes (product_owner authorises implementation).
- **Exit criteria:** implementation authorised and executed per the provisioning
  spec.
- **Failure conditions:** missing provisioning spec or authorisation; boundary
  violation.
- **Recovery method:** stop; obtain the spec and Gate D; resume from approved
  intent.

### Stage 8 — Deployment Complete  (future spec)
- **Purpose:** complete deployment and produce customer deliverables.
- **Required inputs:** approved implementation records.
- **Generated work items:** produce_artifact (deliverables); request_gate_approval.
- **Produced artifacts:** Customer Deliverables.
- **Validation required:** completeness and conformance of deliverables.
- **ChatGPT review required:** Yes.
- **Human approval required:** Yes (Gate E — deliverable acceptance).
- **Exit criteria:** deliverables accepted by the product_owner.
- **Failure conditions:** rejected acceptance; incomplete deliverable.
- **Recovery method:** revise; re-review; re-submit for acceptance.

## 6. Stage Inputs

Summarised above per stage; each stage requires its predecessors' outputs at the
Approved lifecycle state (except Intake Stages 1–2, which are coupled).

## 7. Stage Outputs

Stage → artifact: 1→SPEC-002, 2→SPEC-001, 3→SPEC-003, 4→SPEC-005, 5→SPEC-006,
6→SPEC-007, 7→implementation records (future), 8→customer deliverables.

## 8. Work Items Generated

Stages 1, 2, 4, 5, 6 generate produce/validate/package work items; Stage 3
generates engineering_review; Stages 7–8 generate approval and (future)
implementation/deliverable work items. Work items are defined by REF-WORK-001.

## 9. Validation Required

Every artifact-producing stage requires a conformant output (Validation Engine,
SPEC-008) before it can exit. Non-conformance blocks the stage.

## 10. ChatGPT Review Points

Every stage requires ChatGPT (Lead Architect) review: Stages 1, 2, 4, 5, 6, 7, 8
review the produced/authorised artifact; Stage 3 *is* the review.

## 11. Human Approval Gates

- Gate B — Stage 1 (real-data use).
- Product Owner — Stage 2 (Project Profile approval).
- Gate C — Stages 3/4 (business acceptance where applicable).
- Ready-approval — Stage 5.
- Gate D — Stage 6/7 (implementation authorisation).
- Gate E — Stage 8 (deliverable acceptance).

## 12. Parallel Execution Opportunities

- Stages 1 and 2 (Customer Discovery and Project Profile) form Intake and may run
  together (the profile is the anchor; discovery enriches it).
- Customer-facing documentation, when applicable, may be prepared in parallel with
  later stages.
- All other stages are strictly ordered.

## 13. Optional Workflow Branches

- The POC Deliverable path (SPEC-004) is an optional branch, taken only when the
  engagement requires a proof of concept; it passes through Engineering Review.
- Stages 7–8 (implementation, deployment) are conditional on an approved Mist
  provisioning specification and Gate D; absent those, the workflow completes at
  Stage 6 (approved intent).

## 14. Failure Handling

A failed stage remains active; its corrective work items (fix/revise/re-review)
are generated; no dependent stage may start. Failures never advance the workflow.

## 15. Resume Behavior

Execution resumes by re-evaluating this workflow against the committed engagement
state: active stages and their work items are re-derived, continuing from the last
approved artifact.

## 16. Completion Criteria

The workflow is complete when every applicable stage has exited (its artifact
Approved and committed) up to the engagement's authorised endpoint — Stage 6 for
an intent-only engagement, or Stage 8 when implementation/deployment are
authorised.

## 17. Future Automation Mapping

The future Workflow Engine (REF-PLATFORM-001) reads this definition, computes the
current work items from the engagement state, and drives them through their gates
— honouring validation, review, human approval, and the AI Collaboration
Protocol. The engine executes; this document only declares.

## Stage Classification

- **May execute in parallel:** Stages 1 and 2 (Intake).
- **Optional:** the POC path (SPEC-004); Stages 7–8 (pending the provisioning spec).
- **Strict ordering:** Stages 3 → 4 → 5 → 6 → 7 → 8.
- **Create new work items:** Stages 1, 2, 4, 5, 6 (and 7–8 in future).
- **Review-only:** Stage 3 (Engineering Review); Stage 7 is approval-only.

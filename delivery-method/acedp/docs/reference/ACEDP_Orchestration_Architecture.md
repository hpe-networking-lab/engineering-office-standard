# ACEDP Orchestration Architecture

- Document ID: REF-ORCH-001
- Status: Draft
- Version: 0.1
- Related: REF-PIPELINE-001, REF-RPKG-001, REF-ARCH-001, SPEC-003, SPEC-008,
  roles/Role_Model.md
- Last Updated: 2026-07-01

> Architecture document only. It defines how the agents, Git, review packages,
> validation tooling, and future automation collaborate. It contains no code, MCP
> or GitHub workflow implementation, API payloads, customer data, Mist
> interaction, or executable content, and modifies no approved artifact.

## 1. Purpose

Define how ChatGPT (Lead Architect), Claude (Implementation Engineer), Git,
review packages, the validation tooling, and future MCP/GitHub automation
collaborate through the shared repository. The goal is a single, consistent
orchestration model so that today's manual copy/paste hand-off can later be
reduced or automated without changing the approved ACEDP framework.

## 2. Orchestration Model

Collaboration is turn-based around the repository, which acts as the shared bus:

```
Claude produces an artifact + runs validation + writes a review package + commits
        │  (review package keyed to the commit)
        ▼
ChatGPT reviews from the committed state, records findings and a decision
        │
        ▼
Human (Product Owner) approves at the applicable gate; the decision is recorded
        │
        ▼
Approved artifact is finalised (Version 1.0); the next stage begins
```

No participant advances the pipeline by side channel: every hand-off is a commit
plus a review package. Today the transitions are performed manually; automation
(Section 11) can later perform them, using the same contract.

## 3. Shared Repository Contract

- **Source of truth:** the Git repository. Anything not committed is not
  authoritative (ADR-0008).
- **What is committed:** approved specifications and schemas, produced artifacts
  (instances), rule artifacts, validation tooling, and review packages.
- **Commit conventions:** focused, single-concern commits; milestone commits use
  `Milestone <NN> - <summary>`; the commit is the single unit of state change.
- **Immutability:** approved artifacts (`Status: Approved`, `Version: 1.0`) are
  **not modified in place**; a change is a new revision that supersedes the prior.
- **Branch:** work targets `main`; no GitHub workflow implementation is defined
  here.
- **Contract surface:** the approved schemas/specs and the review-package format
  (REF-RPKG-001) are the interface every participant relies on.

## 4. Agent Responsibilities

- **ChatGPT — Lead Architect / reviewer:** conducts Engineering Review
  (SPEC-003), enforces standards (STD-001/STD-001.1) and ADR-0008 boundaries,
  performs risk analysis, and issues technical approval or rejection with
  findings and open-question dispositions.
- **Claude — Implementation Engineer / artifact producer:** produces artifacts
  within approved scope, runs the validation tooling, writes the review package,
  commits, and reports blockers. **Claude must never self-approve.**
- **Human — Product Owner / final authority:** grants the human approval gates
  and acceptance; authorises real-data use, implementation, and production.

## 5. Review Package Lifecycle

The review package (REF-RPKG-001) is the hand-off contract. Its states:

```
Drafted (by Claude, keyed to a commit)
   → Submitted (hand-off to ChatGPT)
     → Under Review (SPEC-003)
       → Approved            → artifact finalised at 1.0 (with human gate)
       → Rejected (findings) → Claude revises → new package on a new commit
```

A package always references its commit range so review works from the repository,
not pasted logs. Rejections carry findings and dispositions; approvals record the
deciding authority.

## 6. Validation Engine Integration

The validation tooling (SPEC-008; Phase 0) is the **first automated quality
gate**:

- Claude runs the validator before submitting any artifact; the results are
  recorded as validation evidence in the review package.
- A non-conformant artifact does not proceed to Engineering Review — conformance
  is a precondition for review.
- Validation is automated and makes no approval decision; it produces a
  conformant / non-conformant result with findings.

## 7. Artifact State Machine

```
        (produce)            (validate)           (submit)          (SPEC-003 + gate)
 Draft ───────────► Draft ─────────────► Validated ─────► In Review ─────────► Approved (1.0)
   ▲                   │  non-conformant                    │  rejected            │
   │                   └──────────────────────────────┐     └───────────┐         │ (revision)
   └───────────────────────────────────────── revise ◄┘◄────────────────┘         ▼
                                                                             Superseded
```

Guards: a Draft becomes Validated only when conformant; Validated becomes
In Review only with a review package; In Review becomes Approved only with the
recorded authority and (where applicable) human gate; an Approved artifact
becomes Superseded only by a new revision. Reference documents (living) remain
Draft by policy and do not enter this machine.

## 8. Human Approval Checkpoints

The Product Owner is the final approval authority at the gates (per
REF-ROADMAP-001 / REF-PIPELINE-001):

- **Gate B** — authorise real engagement/customer data (before non-sample data).
- **Gate C** — business/customer acceptance where an artifact affects scope.
- **Gate D** — authorise implementation start (and any live action).
- **Gate E** — accept customer deliverables.

Gate decisions are explicit, attributable, and recorded in the Engineering Review
record.

## 9. Failure and Recovery Behavior

- **Interrupted orchestration:** the last committed, approved artifact is the
  resume point; in-progress work is re-validated before proceeding.
- **Failed validation:** the artifact is corrected and re-validated until
  conformant; nothing proceeds on a non-conformant artifact.
- **Rejected review:** blocking findings are resolved or waived (SPEC-003), then
  re-reviewed on a new commit and package.
- **Artifact revision:** approved artifacts change only by a new revision, which
  supersedes the prior; history is preserved.
- **Resume:** work resumes from the committed repository state and the recorded
  review — no context lives outside the repository.

## 10. Idempotency Rules

- **Deterministic tooling:** rule extraction and validation are deterministic —
  the same inputs always produce the same rule artifacts and the same result.
- **Commit as the sole transition:** repository state changes only via a commit;
  re-running tooling without committing changes nothing authoritative.
- **Re-submission:** re-submitting an unchanged artifact yields the same review
  state; it does not create a new approval.
- **Re-processing approved artifacts:** re-processing an Approved artifact is a
  no-op unless a new revision is explicitly created.
- **No external side effects:** orchestration steps act only on the repository;
  they contact no external system.

## 11. Future Automation Hooks

Automation plugs in **around** the contract without changing the approved
framework:

- **MCP orchestration** may drive the produce → validate → package → review →
  approve loop, invoking the validation tooling and moving artifacts between
  stages — consuming the approved schemas, specs, and review-package format as
  the interface.
- **GitHub automation** may manage branches, commits, and review-package
  publication; the repository remains the source of truth and approved artifacts
  remain immutable except by revision.
- **AI-to-AI collaboration** may exchange review packages and dispositions
  through SPEC-003; the human approval gates and the "Claude never self-approves"
  rule are preserved.

Invariants that any automation must uphold:

- Git repository is the source of truth.
- Review packages are the hand-off contract.
- Validation tooling is the first automated quality gate.
- The human (Product Owner) is the final approval authority.
- Claude must never self-approve.
- Approved artifacts must not be modified in place.
- Changing the approved framework requires a new, separately authorised
  specification.

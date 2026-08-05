# ACEDP Processing Pipeline Architecture

- Document ID: REF-PIPELINE-001
- Status: Draft
- Version: 0.1
- Related: SPEC-001..SPEC-008, REF-ROADMAP-001, REF-ARCH-001, REF-RPKG-001,
  roles/Role_Model.md
- Last Updated: 2026-07-01

> Architecture document only. It describes how the ACEDP platform operates end to
> end. It contains no code, automation, MCP logic, GitHub workflows, APIs,
> customer data, Mist interaction, or executable content, and modifies no
> approved artifact.

## 1. Purpose

Define how the entire ACEDP platform operates, from customer intake through
implementation and customer deliverables. It ties the approved specifications
(SPEC-001..SPEC-008), the role model, the validation tooling, and the human
approval gates into a single processing pipeline, so that every artifact is
produced, validated, reviewed, approved, and traced consistently.

The ACEDP framework is documentation-first: this architecture governs how the
approved artifacts are produced and moved through the pipeline; it does not
implement the pipeline.

## 2. Overall Pipeline

The Project Profile (SPEC-001) is the anchor established at intake; Customer
Discovery enriches it. The pipeline then proceeds:

```
Customer Discovery (SPEC-002)
      ↓
Validation (SPEC-008 tooling)
      ↓
Engineering Review (SPEC-003)
      ↓
Design Package (SPEC-005)
      ↓
Mist Organization Readiness (SPEC-006)
      ↓
Mist Organization Generation Intent (SPEC-007)
      ↓
Claude Implementation
      ↓
Customer Deliverables
```

Each downward arrow crosses a checkpoint: validation (automated) and/or
Engineering Review (SPEC-003), and, where required, a human approval gate. No
stage begins until its predecessor's outputs are validated, reviewed, and (where
applicable) approved.

## 3. Pipeline Stages

### Stage 1 — Customer Discovery (SPEC-002)
- **Inputs:** an initialised Project Profile (SPEC-001); customer-provided
  context; access to authorised people.
- **Outputs:** a Customer Discovery record enriching the profile with confirmed
  facts, plus explicit open questions and assumptions.
- **Validation:** schema conformance of the discovery and profile records.
- **Review authority:** lead_architect (completeness); product_owner confirms.
- **Human approval gate:** Gate B — product_owner authorises the use of real
  engagement/customer data (until then, sample data only).
- **Failure conditions:** missing mandatory information; invented facts;
  non-conformant record.
- **Recovery path:** record gaps as open questions; re-gather; re-validate.

### Stage 2 — Validation (SPEC-008 tooling)
- **Inputs:** any ACEDP instance produced by a stage.
- **Outputs:** a validation result (conformant / non-conformant with findings).
- **Validation:** required/type/allowed, reference shape, internal and
  cross-document reference integrity, required sections.
- **Review authority:** lead_architect reviews results; validation itself is
  automated and makes no approval decision.
- **Human approval gate:** none (a gate check, not an approval).
- **Failure conditions:** a non-conformant instance (any error finding).
- **Recovery path:** correct the instance; re-validate until conformant.

### Stage 3 — Engineering Review (SPEC-003)
- **Inputs:** a conformant artifact plus its review package (REF-RPKG-001).
- **Outputs:** a review decision (Approved / Rejected) with findings and
  open-question dispositions.
- **Validation:** the artifact must be conformant before review.
- **Review authority:** lead_architect (per the SPEC-003 approval-authority
  matrix); product_owner for business/customer acceptance where applicable.
- **Human approval gate:** Gate C — business/customer acceptance where the
  artifact affects scope or commitments.
- **Failure conditions:** an open blocking finding; unresolved mandatory criterion.
- **Recovery path:** resolve or waive blocking findings; re-review.

### Stage 4 — Design Package (SPEC-005)
- **Inputs:** approved Project Profile and Customer Discovery; SPEC-005.
- **Outputs:** a Design Package (HLD, LLD, domain plans) as design intent, plus a
  preliminary readiness self-assessment.
- **Validation:** schema conformance; internal reference integrity.
- **Review authority:** lead_architect.
- **Human approval gate:** Gate C where design affects scope/commitments.
- **Failure conditions:** incomplete design; unresolved blocking review finding.
- **Recovery path:** revise the design; re-validate; re-review.

### Stage 5 — Mist Organization Readiness (SPEC-006)
- **Inputs:** an approved Design Package.
- **Outputs:** a readiness assessment with an overall determination
  (ready / partial / not_ready) and gaps.
- **Validation:** schema conformance; the SPEC-006 threshold applied.
- **Review authority:** lead_architect.
- **Human approval gate:** approval of a "ready" determination.
- **Failure conditions:** not_ready; open blocking gaps.
- **Recovery path:** close gaps in the Design Package; re-assess.

### Stage 6 — Mist Organization Generation Intent (SPEC-007)
- **Inputs:** an approved Design Package and an approved "ready" readiness
  assessment.
- **Outputs:** a generation-intent record (traceable to the design; intent only).
- **Validation:** schema conformance; `design_reference` traceability.
- **Review authority:** lead_architect (technical); implementation_engineer
  confirms implementation readiness.
- **Human approval gate:** Gate D — product_owner authorises implementation start
  (the SPEC-007 pre-implementation review).
- **Failure conditions:** upstream not approved; unresolved blocking finding.
- **Recovery path:** correct intent or upstream artifact; re-review.

### Stage 7 — Claude Implementation
- **Inputs:** an approved generation intent; a separate, approved provisioning
  specification (not yet authored); Gate D authorisation.
- **Outputs:** implementation artifacts, each reviewed before use.
- **Validation:** conformance of any produced records; boundary compliance.
- **Review authority:** lead_architect; product_owner authorises.
- **Human approval gate:** Gate D (implementation) — mandatory before any live
  action; a future provisioning spec must be Approved first.
- **Failure conditions:** missing authorisation or provisioning spec; boundary
  violation.
- **Recovery path:** stop; obtain authorisation/spec; resume from the last
  approved artifact.

### Stage 8 — Customer Deliverables
- **Inputs:** approved design and implementation records.
- **Outputs:** customer-facing documentation and deliverables.
- **Validation:** conformance and completeness of deliverables.
- **Review authority:** lead_architect (technical); product_owner (acceptance).
- **Human approval gate:** Gate E — product_owner accepts the deliverables.
- **Failure conditions:** rejected acceptance; incomplete deliverable.
- **Recovery path:** revise; re-review; re-submit for acceptance.

## 4. Artifact Flow

Artifacts, each defined by a schema and produced/consumed in order:

| Artifact | Schema | Produced by | Consumed by |
|---|---|---|---|
| Project Profile | SPEC-001 | Intake | Discovery, Design, all downstream |
| Customer Discovery | SPEC-002 | Discovery | Engineering Review, Design |
| Engineering Review record | SPEC-003 | Review | every approval decision |
| Design Package | SPEC-005 | Design | Readiness, Generation |
| Mist Org Readiness | SPEC-006 | Readiness | Generation |
| Mist Org Generation Intent | SPEC-007 | Generation | Implementation |
| Implementation records | (future spec) | Implementation | Deliverables |
| Customer Deliverables | (derived) | Deliverables | Customer |

Every artifact is validated (SPEC-008 tooling) before review, and every approval
is recorded in an Engineering Review record. Artifacts link to their sources
through the standardized `references` section (`ref_document` + `ref_id`) and,
for design-derived intent, through structured `design_reference`s — so each
artifact is traceable back to the originating Customer Discovery and, through it,
the Project Profile.

## 5. Git Repository Workflow (architecture only)

- **Source of truth:** the Git repository. Knowledge not committed is not
  authoritative (ADR-0008).
- **Branch expectations:** work targets `main`; approved artifacts live on `main`
  at version 1.0. (No GitHub implementation is defined here.)
- **Commit expectations:** focused, single-concern commits; milestone commits use
  `Milestone <NN> - <summary>`; approved artifacts change only via a new revision.
- **Review Package generation:** each milestone produces a review package
  (REF-RPKG-001) keyed to its commit, so review works from the committed state.
- **Review checkpoints:** validation (automated) then Engineering Review
  (SPEC-003) at each stage boundary; approval is explicit and attributable.
- **Approved artifact handling:** `Status: Approved`, `Version: 1.0`, recorded
  authority; no in-place edits — a change requires a new revision.

## 6. ChatGPT Responsibilities (Lead Architect)

- Owns architecture and engineering standards.
- Conducts Engineering Review (SPEC-003): findings, blocking determination,
  approval or rejection.
- Enforces standards (STD-001 / STD-001.1) and the ADR-0008 boundaries.
- Performs risk analysis and records it in the review.
- Provides approval recommendations and technical approval decisions.
- Validates designs and confirms documentation-to-executable transitions are
  authorised before implementation.

## 7. Claude Responsibilities (Implementation Engineer)

- Generates documents and artifacts within approved scope.
- Runs schema validation (SPEC-008 tooling) and reports results.
- Executes approved tooling.
- Performs implementation only when authorised (Gate D) and specified.
- Generates the review package (REF-RPKG-001) for every milestone.
- Reports blockers; never invents facts, secrets, or customer data.
- **Claude must never self-approve.** Approval is always an act of the
  lead_architect and/or product_owner, recorded per SPEC-003.

## 8. Human Responsibilities (Product Owner)

- Owns the human approval gates (B, C, D, E).
- Grants business and customer acceptance.
- Authorises the use of real engagement/customer data (Gate B).
- Authorises implementation start (Gate D) and production (a further, explicit
  authorisation beyond any POC or intent).
- Provides final acceptance of customer deliverables (Gate E).

## 9. Failure Recovery

- **Interrupted pipeline:** the last committed, approved artifact is the resume
  point; incomplete work is re-validated before proceeding.
- **Failed validation:** the instance is corrected and re-validated until
  conformant; no stage proceeds on a non-conformant artifact.
- **Rejected review:** blocking findings are resolved or formally waived
  (SPEC-003), then the artifact is re-reviewed.
- **Artifact revision:** an approved artifact is changed only via a new revision
  (version increment), preserving the prior approved revision for traceability.
- **Restart behavior:** a stage may be restarted from its validated inputs; prior
  approvals for unchanged upstream artifacts remain valid.
- **Resume behavior:** work resumes from the last approved artifact and its
  recorded review, using the committed repository state — no context is lost.

## 10. Traceability Model

Every artifact traces back through recorded references:

```
Customer
  → Customer Discovery (SPEC-002, references the Project Profile)
    → Engineering Review (SPEC-003, references the reviewed artifact)
      → Design Package (SPEC-005, references profile + discovery + review)
        → Mist Org Readiness (SPEC-006, references the Design Package)
          → Mist Org Generation Intent (SPEC-007, design_reference to the design)
            → Implementation (references the approved intent)
              → Customer Deliverables (reference the approved design/implementation)
```

Traceability is enforced structurally: references use `ref_document` + `ref_id`
(validated by the tooling), internal links use local ids, and each approval is
an Engineering Review record. Following the reference chain from any artifact
reaches the originating Customer Discovery and Project Profile.

## 11. Future Automation

The architecture is designed so that automation plugs in **around** the approved
framework without changing it:

- **MCP orchestration** may drive the pipeline by producing and moving artifacts
  between stages, invoking the validation tooling, and generating review
  packages — consuming the approved schemas and specs as the contract, not
  altering them.
- **GitHub automation** may manage branches, commits, and review-package
  publication; the repository remains the source of truth and approved artifacts
  remain immutable except by revision.
- **AI-to-AI collaboration** (architect/implementer) may exchange review packages
  and dispositions through the SPEC-003 process; approval authority and the
  "Claude never self-approves" rule are unchanged.

Because the framework is documentation-first and schema-driven, any automation is
a consumer of the approved contract. The specifications, schemas, role model, and
gates remain authoritative; automation that would change them requires a new,
separately authorised specification.

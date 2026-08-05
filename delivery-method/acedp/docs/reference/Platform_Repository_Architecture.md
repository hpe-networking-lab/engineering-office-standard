# Platform Repository Architecture

- Document ID: REF-PLATFORM-001
- Status: Draft
- Version: 0.1
- Last Updated: 2026-07-01
- Related: REF-PIPELINE-001, REF-ORCH-001, REF-AICOLLAB-001, REF-ARCH-001,
  REF-DESIGN-001, SPEC-001..SPEC-008

> Architecture document only. It describes how the software repository is
> organised to implement the approved ACEDP framework. It contains no code, APIs,
> implementation, GitHub Actions, MCP implementation, customer data, or Mist
> implementation, and modifies no approved framework artifact.

## 1. Purpose

Define how the ACEDP **platform** — the software that executes the approved
ACEDP framework — is organised in the repository. The framework (SPEC-001..008,
schemas, standards, role model) is complete and proven; this document describes
the components, layers, and repository layout that operate that framework, so the
platform can be built incrementally without changing the approved framework.

## 2. Platform Overview

The platform is a set of cooperating components that move an engagement through
the approved pipeline (REF-PIPELINE-001): produce artifacts, validate them,
review and approve them, and (in future) generate a Mist organisation from an
approved intent. Every component consumes the approved schemas and specifications
as its contract; the framework remains authoritative and immutable except by
revision.

## 3. Repository Layout

Logical layout (physical separation into distinct Git repositories is an
extensibility option; today all live under the ACEM repository's `acedp/`):

```
Framework (approved, immutable except by revision)
  acedp/docs/          standards, specifications, ADR, EKR
  acedp/schemas/       approved YAML schemas (SPEC-001..007)

Platform (the executing software)
  acedp/tools/         validation engine and future platform components
  acedp/docs/reference platform architecture and living references

Lab Repository (sandbox / demonstration)
  acedp/examples/      sample engagement and worked examples (non-customer)

Customer Repositories (future, one per engagement)
  <per-engagement>/    engagement instances + generated artifacts (no data here now)
```

Git is the single source of truth for all of the above.

## 4. Platform Components

For each component: Purpose, Inputs, Outputs, Dependencies, Owner, Failure Modes,
Recovery Strategy, and Interaction with other components.

### 4.1 Validation Engine  (implemented — Phase 0)
- **Purpose:** check that an instance conforms to its schema (required/type/
  allowed/reference-shape/internal/cross-document/required-section).
- **Inputs:** an instance; the schema's rule artifact; optional context set.
- **Outputs:** a validation result (conformant / non-conformant + findings).
- **Dependencies:** approved schemas; generated rule artifacts.
- **Owner:** platform (invoked by Claude as Implementation Engineer).
- **Failure modes:** non-conformant instance; malformed/missing rule artifact.
- **Recovery strategy:** correct the instance and re-validate; regenerate rules.
- **Interaction:** gates the Review Engine (only conformant artifacts proceed).

### 4.2 Review Engine
- **Purpose:** conduct Engineering Review (SPEC-003) — findings, dispositions,
  approval or rejection.
- **Inputs:** a conformant artifact and its review package (REF-RPKG-001).
- **Outputs:** a review decision, findings, and open-question dispositions.
- **Dependencies:** Validation Engine (precondition); standards; role model.
- **Owner:** ChatGPT (Lead Architect).
- **Failure modes:** open blocking finding; missing review package.
- **Recovery strategy:** resolve or waive findings; re-review on a new commit.
- **Interaction:** consumes Validation Engine output; feeds the State Manager.

### 4.3 Artifact Generator
- **Purpose:** produce framework artifacts (profiles, discovery, design, intent)
  conforming to the schemas.
- **Inputs:** approved upstream artifacts; the target schema.
- **Outputs:** a candidate artifact instance.
- **Dependencies:** Shared Data Model; upstream approved artifacts.
- **Owner:** Claude (Implementation Engineer).
- **Failure modes:** incomplete or non-conformant output; invented facts.
- **Recovery strategy:** re-generate from approved inputs; validate before submit.
- **Interaction:** output flows to the Validation Engine, then the Review Engine.

### 4.4 Engagement Manager
- **Purpose:** represent one engagement and the set of artifacts belonging to it.
- **Inputs:** the engagement's artifacts and their references.
- **Outputs:** an engagement view (membership, cross-references, status).
- **Dependencies:** Repository Manager; State Manager.
- **Owner:** platform.
- **Failure modes:** missing or mislinked artifacts; broken references.
- **Recovery strategy:** re-resolve references; re-validate the set with context.
- **Interaction:** scopes the context set the Validation Engine resolves against.

### 4.5 State Manager
- **Purpose:** track each artifact's lifecycle state (Draft → Validated →
  In Review → Approved → Superseded).
- **Inputs:** validation results and review decisions.
- **Outputs:** the authoritative state of each artifact.
- **Dependencies:** Validation Engine; Review Engine; Repository Manager.
- **Owner:** platform.
- **Failure modes:** state/commit divergence; illegal transition.
- **Recovery strategy:** reconcile state from the committed repository (truth).
- **Interaction:** the Workflow Engine reads/advances state through it.

### 4.6 Workflow Engine
- **Purpose:** advance an engagement through the pipeline stages and gates.
- **Inputs:** engagement state; gate decisions.
- **Outputs:** the next authorised action / stage transition.
- **Dependencies:** State Manager; Engagement Manager; approval gates.
- **Owner:** platform (future: AI Orchestrator drives it).
- **Failure modes:** attempt to advance past an unmet gate; interrupted run.
- **Recovery strategy:** resume from the last committed, approved state.
- **Interaction:** coordinates Generator, Validation, Review, and gates.

### 4.7 Repository Manager
- **Purpose:** manage commits, branches, and the committed source of truth.
- **Inputs:** produced/updated files; commit metadata.
- **Outputs:** commits on `main`; the committed repository state.
- **Dependencies:** Git.
- **Owner:** platform (aligned to the Git Integration Layer).
- **Failure modes:** uncommitted work; attempted in-place edit of approved artifacts.
- **Recovery strategy:** commit or discard; enforce immutability (revision only).
- **Interaction:** every other component reads/writes through committed state.

### 4.8 AI Orchestrator
- **Purpose:** drive the produce → validate → package → review → approve loop
  across AI participants.
- **Inputs:** engagement state; review packages.
- **Outputs:** orchestrated actions bound by the AI Collaboration Protocol.
- **Dependencies:** Workflow Engine; MCP Gateway; AI Collaboration Layer.
- **Owner:** future automation (orchestration only; holds no approval authority).
- **Failure modes:** protocol violation; attempted self-approval.
- **Recovery strategy:** halt; defer to human/architect per the protocol.
- **Interaction:** invokes components; never overrides the human/architect.

### 4.9 MCP Gateway
- **Purpose:** expose platform operations to future MCP orchestration.
- **Inputs:** orchestration requests (future).
- **Outputs:** invocations of platform components (future).
- **Dependencies:** AI Orchestrator; platform components.
- **Owner:** future automation.
- **Failure modes:** unauthorised or out-of-scope request.
- **Recovery strategy:** reject out-of-scope requests; require human authorisation.
- **Interaction:** a boundary adaptor; changes nothing in the framework.

### 4.10 Future Mist Provisioning Engine
- **Purpose:** (future) prepare a Mist organisation from an approved generation
  intent — requires a separate, approved provisioning specification.
- **Inputs:** an approved "ready" readiness assessment and approved intent;
  Gate D authorisation.
- **Outputs:** (future) organisation preparation, per the provisioning spec.
- **Dependencies:** an approved provisioning specification (does not yet exist).
- **Owner:** future; product_owner authorises (Gate D).
- **Failure modes:** acting without authorisation or a provisioning spec.
- **Recovery strategy:** stop; obtain the spec and Gate D; resume from approved intent.
- **Interaction:** consumes approved intent only; out of scope until authorised.

## 5. Shared Data Model

The approved YAML schemas (SPEC-001..007) are the shared data model. All
components read and write instances against these schemas; the common envelope
(`metadata → references → body → approvals`), structured references, and
identifiers are the shared vocabulary. The model is versioned; changes require a
new schema revision.

## 6. Validation Layer

The Validation Engine and the generated rule artifacts. It is the first automated
quality gate: no artifact advances until conformant. Read-only over the schemas;
deterministic.

## 7. Engineering Layer

The Artifact Generator and the Review Engine, operating the SPEC-003 process:
artifacts are produced, validated, reviewed, and approved with recorded authority
and dispositions.

## 8. Automation Layer

The Workflow Engine, State Manager, Engagement Manager, and AI Orchestrator.
This layer sequences the pipeline and tracks state; it holds no approval
authority and cannot bypass a gate.

## 9. User Interface Layer

A future presentation surface (for humans) over engagement state, validation
results, and review packages. It reads the committed repository; it never becomes
the source of truth.

## 10. MCP Integration Layer

The MCP Gateway and its adaptors. Future MCP servers are orchestration components
only, invoking platform operations through the gateway. They consume the approved
contract and cannot change the framework.

## 11. Git Integration Layer

The Repository Manager and Git. Git is the single source of truth; commits are the
atomic state transitions; approved artifacts are immutable except by revision. No
GitHub Actions or workflow implementation is defined here.

## 12. AI Collaboration Layer

Binds every automated participant to the AI Collaboration Protocol
(REF-AICOLLAB-001): Claude produces, ChatGPT reviews, the human approves; Claude
never self-approves; hand-off is via review packages; human approval overrides.

## 13. Security Model

- The committed repository is the trust boundary; only committed, reviewed content
  is authoritative.
- No secrets, credentials, tokens, claim codes, or customer data are stored in the
  repository (ADR-0008 / SPEC boundaries).
- Components operate within approved scope; out-of-scope actions require human
  authorisation. No component can approve its own work.

## 14. Deployment Model

The platform is repository-native: it runs against a checked-out repository and
writes back via commits. It requires no external services to validate or review.
Any future runtime (UI, MCP servers) is deployed around this repository-native
core without becoming the source of truth. (No deployment implementation here.)

## 15. Extensibility Model

- New schemas and specifications are added through the approved process (authored,
  reviewed via SPEC-003, approved) — the platform consumes them without code
  changes to the schema-driven components.
- New components plug into the layers above through their defined inputs/outputs.
- Physical repository separation (framework / platform / lab / customer repos) is
  an option that does not change the logical architecture.
- Any change to the approved framework requires a new, separately authorised
  specification.

## Repository Diagram

```
                         ┌──────────────────────────────┐
                         │   Framework (approved 1.0)    │
                         │  specs · schemas · standards  │
                         └───────────────┬──────────────┘
                                         │ contract
                                         ▼
   ┌──────────┐   produce   ┌────────────────────────────┐  review   ┌──────────┐
   │  Claude  │────────────►│         Platform           │◄─────────►│ ChatGPT  │
   │ (Impl.   │             │ Validation · Review ·       │           │ (Lead    │
   │  Eng.)   │◄────────────│ Generator · Engagement ·    │           │  Arch.)  │
   └────┬─────┘  findings   │ State · Workflow · Repo Mgr ·│           └────┬─────┘
        │                   │ AI Orchestrator · MCP Gateway│                │
        │                   └──────┬───────────────┬───────┘                │
        │ commit                   │ reads/writes  │ scopes                 │ approve
        ▼                          ▼               ▼                        ▼
   ┌──────────┐        ┌──────────────────┐   ┌──────────────┐      ┌───────────────┐
   │   Git    │◄──────►│ Lab Repository   │   │  Customer     │      │ Human Reviewer│
   │ (source  │        │ (sample eng.)    │   │  Repositories │      │ (Product      │
   │ of truth)│        └──────────────────┘   │  (future)     │      │  Owner)       │
   └────┬─────┘                               └──────┬────────┘      └───────┬───────┘
        │                                            │ produce               │ gates
        ▼                                            ▼                       ▼
   ┌───────────────────────────────────────────────────────────────────────────┐
   │  Generated Artifacts (validated instances; intent only — no config/Mist)   │
   └───────────────────────────────────────────────────────────────────────────┘
```

Framework is the contract; the Platform executes it; Git is the source of truth;
Claude produces and ChatGPT reviews through review packages; the Human Reviewer
holds the approval gates; Lab and Customer repositories hold engagement artifacts;
Generated Artifacts are validated instances (intent only).

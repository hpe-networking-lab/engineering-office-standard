# Platform Architecture Summary

- Document ID: REF-PLATFORM-SUMMARY-001
- Status: Draft
- Version: 0.1
- Last Updated: 2026-07-01
- Related: REF-PLATFORM-001, REF-STATE-001, REF-WORK-001, REF-WFLOW-001,
  REF-WFLOW-DEFAULT-001, REF-WFLOW-ENGINE-001, REF-ENGMGR-001, REF-STATEMGR-001,
  REF-REVIEWENG-001, REF-AICOLLAB-001, SPEC-008

> Summary document only. It consolidates the platform runtime architecture. It
> modifies no approved artifact and contains no code, schema, automation, customer
> data, or Mist interaction.

## 1. Purpose

Consolidate the ACEDP platform runtime architecture now that the core runtime
components are defined, so the design set can be read as one coherent map and the
build sequence can be planned. It restates responsibilities and interactions; it
defines nothing new.

## 2. Current Platform Baseline

- The **framework** (SPEC-001..008, schemas, standards, role model) is Approved
  1.0 and proven end-to-end (Milestone 81).
- The **Validation Engine** is **implemented** (Phase 0 tooling under
  `acedp/tools/validation/`): rule extraction and a validator covering
  required/type/allowed/reference-shape/internal/cross-document/required-section
  checks, with deterministic rule artifacts.
- The remaining runtime components are **defined as architecture** (not yet built).

## 3. Core Runtime Components

| Component | Document | Status |
|---|---|---|
| Validation Engine | REF-ARCH-001 / REF-DESIGN-001 / REF-MAP-001 | Implemented (Phase 0) |
| Workflow Engine | REF-WFLOW-ENGINE-001 | Architecture |
| Engagement Manager | REF-ENGMGR-001 | Architecture |
| State Manager | REF-STATEMGR-001 | Architecture |
| Review Engine | REF-REVIEWENG-001 | Architecture |
| Work Item Model | REF-WORK-001 | Model |
| Workflow Definition Model | REF-WFLOW-001 | Model |
| Default ACEDP Workflow | REF-WFLOW-DEFAULT-001 | Worked example |
| AI Collaboration Protocol | REF-AICOLLAB-001 | Protocol |

## 4. Component Responsibility Map

- **Validation Engine** — checks instance conformance to schema (first quality
  gate); produces results, makes no decision.
- **Engagement Manager** — owns engagement identity and membership (which
  artifacts belong to an engagement); performs no execution.
- **State Manager** — computes engagement/artifact/validation/review/approval and
  work-item state over the membership set; performs no execution or approval.
- **Workflow Engine** — loads a Workflow Definition, evaluates it against state,
  generates eligible work items, routes them; contains no engineering knowledge.
- **Review Engine** — prepares and records reviews (findings, dispositions,
  decisions); does not approve.
- **Work Item Model / Workflow Definition Model / Default Workflow** — the
  declarative models the engine consumes.
- **AI Collaboration Protocol** — binds every participant (Claude produces,
  ChatGPT reviews, human approves; Claude never self-approves).

## 5. Component Interaction Model

```
        Workflow Definition (declarative)
                    │ loads
                    ▼
 Engagement Manager ─ membership ─►  Workflow Engine  ◄─ state ─ State Manager
   (identity/members)                 (evaluate/route)            (compute state)
                    │                     │  invokes                 ▲
                    │                     ▼                          │ reads results
                    │             Validation Engine ────────────────┘
                    │                     │ conformant
                    │                     ▼
                    └───────────────►  Review Engine ─► ChatGPT (review) / Human (approve)
                                          │ records
                                          ▼
                                         Git (source of truth)
```

The Engagement Manager scopes the set; the State Manager computes state over it;
the Workflow Engine evaluates the definition and routes work; the Validation and
Review Engines are the quality/approval gates; Git records everything.

## 6. Runtime Execution Flow

1. The Engagement Manager identifies the engagement and its membership.
2. The State Manager computes state from the committed repository over that
   membership.
3. The Workflow Engine loads the Workflow Definition, evaluates active stages, and
   generates eligible work items.
4. Claude performs producer work items; the Validation Engine gates conformance.
5. Conformant artifacts go to the Review Engine; ChatGPT reviews; the human grants
   any gate.
6. Decisions are committed; the State Manager recomputes; the cycle repeats until
   the workflow's completion criteria are met.

## 7. Git / Source-of-Truth Model

Git is the single source of truth. All state is a projection of committed content;
components hold no authoritative state outside Git. Commits are the atomic state
transitions; approved artifacts are immutable except by revision; recovery is
always from Git alone.

## 8. Review and Approval Model

Engineering Review (SPEC-003) is the approval gate. The Review Engine prepares and
records; ChatGPT (lead_architect) makes the technical decision; the human
(product_owner) grants the applicable gate (B/C/D/E). Blocking findings prevent
approval until resolved or waived. Claude never self-approves.

## 9. Validation Model

The Validation Engine generates rules from the approved schemas and enforces
required/type/allowed/reference-shape/internal-reference/cross-document/required-
section conformance, deterministically. Conformance is the precondition for
review; a non-conformant artifact does not advance.

## 10. Known Gaps

- **Components not built:** Workflow Engine, Engagement Manager, State Manager, and
  Review Engine are architecture only; only the Validation Engine is implemented.
- **Mist Provisioning Engine:** undesigned and unspecified; requires a new,
  separately authorised provisioning specification and Gate D.
- **Validation coverage:** path-based external references (`ref_path`) are not yet
  resolved cross-document; the `schema_version`-match check is not enforced.
- **Surfaces:** the User Interface and MCP Integration layers are described but not
  designed in detail; no automation exists.
- **Persistence:** no schema exists for engagement/work-item/workflow state (state
  is recomputed from Git today).

## 11. Recommended Next Build Sequence

1. **Engagement Manager** — membership from the reference graph (small, read-only;
   already exercised by the sample engagement's cross-document resolution).
2. **State Manager** — compute the five projections over a membership set.
3. **Workflow Engine** — evaluate the Default Workflow against state and generate
   eligible work items (route only).
4. **Review Engine** — assemble evidence and record decisions.
5. Only then consider the **UI/MCP surfaces**; and, separately, author the **Mist
   provisioning specification** before any Mist Provisioning Engine work.

Each is a separately reviewed build milestone; the framework and its Approved
artifacts remain immutable throughout.

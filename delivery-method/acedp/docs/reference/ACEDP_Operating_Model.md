# ACEDP Operating Model

- Document ID: REF-OPMODEL-001
- Status: Approved
- Version: 1.0
- Approved By: Human Authority
- Date: 2026-07-02
- Supersedes: REF-AICOLLAB-001 (AI Collaboration Protocol) and the multi-gate
  approval stack (Gates A–D and per-stage independent review) as an operating
  requirement, wherever described (REF-WFLOW-DEFAULT-001 and the pipeline /
  orchestration references).

> This document replaces the ChatGPT-era, multi-agent governance with a model
> proportioned to how ACEDP is actually run: **one Human Authority and one AI
> engineer.** It keeps what creates value — the schemas, the validator, Git as the
> record, and a single human approval before anything touches a real customer — and
> retires the ceremony that assumed a second AI reviewer and an audited, multi-team
> delivery organization. It changes no schema and no standard.

## 1. Why this exists

ACEDP's original governance assumed three parties — ChatGPT as Lead Architect
reviewing every artifact, Claude producing, a human approving — plus four lettered
approval gates and a Review Package per milestone. ChatGPT has been retired as a
participant, which makes the per-stage independent-review gate either empty or
self-contradictory (the producer would be reviewing its own work). Independent of
that, the gate stack is sized for a large, audited delivery organization, not for a
single engineer working with one AI. This model right-sizes it.

## 2. Participants

- **Human Authority (you):** owns the objective, approves, and is the sole authority
  to act on a real customer or a real Mist organization. Approval is explicit and
  attributable.
- **AI Engineer (Claude):** produces engagement artifacts to the approved schemas
  (discovery, profile, design, readiness, generation intent), flags risks, and never
  acts on a real customer or real Mist org without approval.

The separate "Lead Architect / ChatGPT" reviewer role is **retired.** There is no
mandatory second-agent review.

## 3. The one gate that matters

Exactly one approval gate is binding: **your sign-off before anything touches a real
customer's data or a real Mist organization.** Everything upstream of it — discovery,
design drafts, readiness analysis — is produced and iterated freely, with no per-stage
review ritual. Downstream of it, work proceeds under your authorization.

## 4. What is kept

- **Schemas (SPEC-001..008)** — the data model of an engagement. Unchanged.
- **The validator (`acedp/tools/validation/`)** — automated schema/rule checking. This
  is the structural quality gate; it replaces manual per-stage review for correctness.
- **Git** — the single source of truth and the record of what happened.
- **The workflow stages** — as a checklist of what a good engagement produces, not as a
  gated approval machine.

## 5. What is retired

- The per-stage independent (ChatGPT) review requirement.
- Approval Gates A–D, collapsed into the single human gate in §3.
- Mandatory per-milestone Review Packages as a hand-off ritual.
- The governance engines (Review Engine, and the State Manager as an
  approval-tracker) as build targets — they exist to run ceremony this model removes.

## 6. What this does not change

Schemas, the STD-001 standards, and the validator remain in force. Real-customer and
real-Mist safety is not weakened — arguably strengthened, because the single gate that
protects the customer is now the focus rather than one of a dozen. Historical documents
are left as they are; this supersedes their *governance model*, it does not rewrite
them.

## 7. Approval

Approved by the Human Authority, 2026-07-02. This is the authoritative operating model
for ACEDP; where it conflicts with REF-AICOLLAB-001 or the lettered-gate stack, this
document prevails.

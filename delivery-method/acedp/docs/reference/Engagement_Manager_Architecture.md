# Engagement Manager Architecture

- Document ID: REF-ENGMGR-001
- Status: Draft
- Version: 0.1
- Last Updated: 2026-07-01
- Related: REF-WFLOW-ENGINE-001, REF-STATE-001, REF-WORK-001, REF-PLATFORM-001,
  REF-AICOLLAB-001, SPEC-001, SPEC-008

> Architecture document only. It designs the runtime service that discovers and
> manages engagements. It contains no implementation, code, schema, automation,
> MCP implementation, GitHub Actions, customer data, or Mist interaction, and
> modifies no approved artifact.

## 1. Purpose

Design the Engagement Manager: the runtime service that discovers, loads,
identifies, and manages engineering engagements. It owns engagement **identity**
and **membership** — which artifacts belong to which engagement — but performs
**no workflow execution** and no engineering work.

## Design Requirements

- Defines **what constitutes an engagement**.
- Defines **how engagements are discovered**.
- Defines **how engagement identity is determined**.
- Defines **how artifacts become members** of an engagement.
- Defines **how orphan artifacts are handled**.
- Defines **how multiple simultaneous engagements are isolated**.
- Defines **how engagement boundaries are enforced**.
- Defines **how the Workflow Engine requests an engagement**.
- Keeps **Git as the source of truth**.
- The Engagement Manager **never performs engineering work**.
- It **never modifies approved artifacts**.
- It **never bypasses review or approval**.

## 2. Responsibilities

- Discover engagements in the repository.
- Determine and hold each engagement's identity.
- Compute artifact membership from the reference graph.
- Load an engagement (its artifact set) on request and unload it when done.
- Enforce engagement boundaries and isolation.
- Serve engagement views to the Workflow Engine; perform no execution itself.

## 3. Relationship to Workflow Engine

The Workflow Engine requests an engagement by id; the Engagement Manager returns
the engagement's membership and location. The manager never runs a workflow — it
provides the set the engine evaluates. The two are separate concerns: identity/
membership (manager) versus execution (engine).

## 4. Relationship to Engagement State

The manager supplies the artifact membership that the State Model (REF-STATE-001)
projects over. State computation belongs to the State Manager / engine; the
Engagement Manager defines *which* artifacts are in scope, not their lifecycle
state.

## 5. Relationship to Work Items

The manager does not generate or execute work items. It scopes the artifact set
against which work items are computed, so that work items belong to exactly one
engagement.

## 6. Engagement Discovery

Engagements are discovered from the committed repository: the manager locates
engagement roots (e.g. a lab or customer repository directory) and the anchor
Project Profile (SPEC-001) within each. Discovery is a read-only scan of committed
content; it introduces no state of its own.

## 7. Engagement Identity

An engagement's identity is anchored by its Project Profile:

- **anchor:** the Project Profile instance (its profile_id).
- **engagement_id:** derived from/associated with the anchor.
- **location:** the repository path holding the engagement's artifacts.

Identity is stable for the engagement's life; two engagements never share an
anchor.

## 8. Artifact Membership

An artifact is a member of an engagement when it resolves — directly or
transitively — to that engagement's anchor Project Profile through structured
references (validated by cross-document reference resolution). Membership is thus
computed from the reference graph, not asserted out of band.

- **Orphan artifacts:** an artifact that resolves to no anchor (or to an unknown
  anchor) is an **orphan**; the manager records it as unassigned and excludes it
  from any engagement rather than guessing membership.
- **Ambiguity:** an artifact that resolves to more than one anchor is flagged as
  a boundary conflict for review, not silently assigned.

## 9. Engagement Lifecycle

An engagement exists from the creation of its anchor Project Profile until its
work is complete (or archived). The manager reflects, but does not drive, this
lifecycle: it observes the committed set and reports membership; stage/approval
progression is the engine's and reviewers' concern.

## 10. Loading and Unloading Engagements

- **Load:** on request, the manager reads the committed engagement set and returns
  its membership and location — a read operation, holding no exclusive lock.
- **Unload:** the manager discards its in-memory view; because all truth is in
  Git, unloading loses nothing and a later load recomputes identically.

## 11. Repository Interaction

The manager interacts with the repository read-only for discovery and membership.
It does not write artifacts, does not modify approved artifacts, and does not
commit engineering content. Git remains the single source of truth; the manager's
view is always a projection of the committed state.

## 12. Failure Handling

- **Missing anchor:** an engagement directory without a resolvable Project Profile
  is reported as incomplete, not assumed.
- **Broken references:** unresolved references are surfaced (membership cannot be
  completed) rather than guessed.
- **Boundary conflict:** an artifact resolving to multiple anchors is flagged for
  review.

## 13. Recovery Behavior

Recovery is from Git alone: on restart the manager re-scans the committed
repository and recomputes identities and membership. No separate store exists to
reconcile, so recovery is deterministic and lossless.

## 14. Service Interfaces (conceptual only)

Conceptual contracts (no code, no API):

    discover_engagements(repository_commit) -> EngagementRef[]
    identify(anchor_profile) -> EngagementIdentity
    membership(engagement_id) -> ArtifactRef[]
    load(engagement_id) -> EngagementView
    unload(engagement_id) -> void
    orphans(repository_commit) -> ArtifactRef[]

These describe the manager's boundaries; they are not an implementation.

## 15. Future Automation Boundaries

- The Engagement Manager is an orchestration-support component (REF-PLATFORM-001):
  it holds no approval authority and enforces the AI Collaboration Protocol.
- Future MCP orchestration may query it through its conceptual interfaces, bound by
  the same invariants.
- Multiple simultaneous engagements are isolated by identity and membership: each
  engagement's artifact set is disjoint (orphans/conflicts excluded), so concurrent
  engagements never interfere. Any change giving the manager engineering authority
  or write access to approved artifacts would require a new, separately authorised
  specification.

## What the Engagement Manager Does NOT Do

- It does **not** perform engineering work or make engineering decisions.
- It does **not** execute workflows (that is the Workflow Engine).
- It does **not** compute artifact lifecycle state (that is the State Manager).
- It does **not** produce, edit, or modify artifacts — approved or otherwise.
- It does **not** validate, review, or approve artifacts.
- It does **not** bypass validation, review, or human approval.
- It does **not** assign orphan or ambiguous artifacts by guessing.
- It does **not** hold authoritative state outside Git.
- It does **not** interact with Mist, external systems, or customer data.

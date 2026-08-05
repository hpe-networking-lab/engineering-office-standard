# AI Collaboration Protocol

> **Superseded (2026-07-02) by [`REF-OPMODEL-001` — ACEDP Operating Model](ACEDP_Operating_Model.md).** This protocol describes the retired ChatGPT-era, two-AI-agent governance (ChatGPT as Lead Architect reviewing every artifact). ChatGPT is no longer a participant; the mandatory second-agent review is retired. Retained as a historical record only; it governs nothing.

- Document ID: REF-AICOLLAB-001
- Status: Superseded by REF-OPMODEL-001 (ACEDP Operating Model)
- Version: 0.1
- Related: REF-ORCH-001, REF-PIPELINE-001, REF-RPKG-001, SPEC-003, roles/Role_Model.md
- Last Updated: 2026-07-01

> Architectural protocol only. It governs how the participants collaborate. It
> contains no implementation code, GitHub Actions, MCP implementation, APIs,
> network automation, Mist provisioning, customer data, or executable workflows,
> and modifies no approved artifact.

## 1. Purpose

Define the protocol that governs how ChatGPT (Lead Architect), Claude
(Implementation Engineer), Git, the validation tooling, review packages, and
future automation collaborate while implementing ACEDP. The protocol makes the
collaboration deterministic, reviewable, and recoverable, so that today's manual
hand-off can later be automated without changing the approved framework.

## 2. Design Principles

- Git is the single source of truth; nothing uncommitted is authoritative.
- Review packages are the only engineering hand-off.
- Every action is traceable, reviewable, and recoverable from Git.
- Approval is a human/architect act; Claude never self-approves.
- Approved artifacts are immutable; change is by new revision only.
- Automation is a consumer of the protocol, never a replacement for it.

**Protocol invariants** (binding on every participant, human or AI, now and under
future automation):

- ChatGPT acts as Lead Architect.
- Claude acts as Implementation Engineer.
- Git remains the single source of truth.
- Review Packages are the only engineering hand-off.
- ChatGPT never edits Claude's work without review.
- Claude never implements architecture independently.
- Claude never self-approves.
- Human approval overrides AI decisions.
- Approved artifacts are immutable.
- Every implementation begins from a committed repository state.
- Every milestone ends with a Review Package.
- Interrupted work must always be recoverable from Git.
- Multiple AI agents may eventually participate.
- Future MCP servers are orchestration components only.
- Future GitHub automation follows this protocol rather than replacing it.

## 3. Collaboration Roles

- **ChatGPT — Lead Architect:** owns architecture, standards, engineering review,
  risk analysis, and technical approval/rejection. Does not edit Claude's
  artifacts in place; issues findings through review.
- **Claude — Implementation Engineer:** produces artifacts within approved scope,
  runs the validation tooling, writes review packages, and commits. Does not
  design architecture independently and never self-approves.
- **Human — Product Owner:** final approval authority; overrides AI decisions;
  grants the approval gates.

## 4. Repository Ownership Model

The repository is jointly used but singly authoritative. No participant owns a
private copy of the truth: the committed state is the truth. Claude authors and
commits; ChatGPT reviews the committed state and records decisions; the human
approves at gates. Reference (living) documents remain Draft; normative artifacts
move through the lifecycle to Approved.

## 5. Branch and Commit Strategy

- Work targets `main`; approved artifacts live on `main` at version 1.0.
- Commits are focused and single-concern; milestone commits use
  `Milestone <NN> - <summary>`.
- A commit is the atomic unit of state change; a milestone is a set of commits
  ending in a review package.
- No GitHub workflow implementation is defined here; the strategy is
  branch/commit discipline, not tooling.

## 6. Review Package Exchange Protocol

- Every milestone ends with a review package (REF-RPKG-001), keyed to its commit
  range so the reviewer works from the repository, not pasted logs.
- The package is the **only** engineering hand-off: it carries the commit
  reference, files changed, validation evidence, design decisions, risks,
  questions, and the approval request.
- ChatGPT reviews the package against the committed state and returns findings and
  a decision; Claude revises and re-submits on a new commit if rejected.

## 7. Approval Workflow

1. Claude produces an artifact, validates it, writes the package, commits.
2. ChatGPT conducts Engineering Review (SPEC-003): findings, blocking
   determination, technical approval or rejection, open-question dispositions.
3. The human grants the applicable approval gate where required.
4. On approval, the artifact is finalised (Status Approved, Version 1.0, recorded
   authority). Claude never self-approves; human approval overrides AI decisions.

## 8. Artifact Ownership Rules

- Claude owns artifact production; ChatGPT owns review and approval recommendation;
  the human owns final approval.
- ChatGPT never edits Claude's artifacts in place — corrections are requested via
  review findings and applied by Claude on a new commit.
- Approved artifacts are immutable; a change is a new revision that supersedes the
  prior, preserving history.

## 9. Synchronization Protocol

- The repository is the synchronization point; participants synchronise by reading
  the committed state, not by exchanging state out of band.
- Each participant acts on a known commit; a review package names the commit range
  so the reviewer and author share an exact reference.
- Deterministic tooling ensures that re-running validation or extraction on the
  same commit yields identical results.

## 10. Conflict Detection and Resolution

- Conflicts are detected against the committed state: divergence is visible as a
  diff, and review packages pin the commit under review.
- Because approved artifacts are immutable and changes are single-concern commits,
  concurrent edits to the same approved artifact are disallowed by protocol rather
  than merged.
- Where interpretations differ, the Lead Architect's review decision governs
  technical matters and the Product Owner governs acceptance; disagreements are
  recorded as findings/dispositions, not resolved silently.

## 11. Failure Recovery

- **Failed validation:** correct and re-validate until conformant; nothing
  proceeds on a non-conformant artifact.
- **Rejected review:** resolve or waive blocking findings (SPEC-003), then
  re-review on a new commit and package.
- **Interrupted work:** the last committed state is the recovery point; in-progress
  work is re-validated before proceeding.
- **Revision:** approved artifacts change only by a new revision; the prior
  approved revision is retained.

## 12. Session Continuation

- Because all state lives in Git, any participant can resume from the committed
  repository and the recorded review — no context is lost between sessions.
- A new session begins by reading the current commit and the latest review
  packages; work continues from the last approved artifact.
- This holds across human, ChatGPT, and Claude sessions, and across a change of
  participant instance.

## 13. Automation Readiness

- The protocol is agent-agnostic: multiple AI agents may participate, each bound by
  the same invariants.
- Future MCP servers are orchestration components only — they move artifacts,
  invoke validation, and publish review packages, but do not hold authority.
- Future GitHub automation follows this protocol (branch/commit discipline,
  immutable approved artifacts, review-package hand-off) rather than replacing it.
- Any automation that would change the approved framework requires a new,
  separately authorised specification.

## 14. Security and Trust Boundaries

- The committed repository is the trust boundary; only committed, reviewed content
  is authoritative.
- No participant embeds secrets, credentials, tokens, claim codes, or customer data
  in the repository (ADR-0008 / SPEC boundaries).
- AI participants operate within approved scope only; actions outside scope require
  human authorisation.
- Human approval is the final control and overrides AI decisions; no AI participant
  can approve its own work.

## 15. Future Evolution

- The protocol may be extended (e.g. additional agent roles, richer automation)
  through the normal ACEDP process: a proposed change is authored, reviewed via
  SPEC-003, and approved before it binds.
- The invariants in Section 2 are the stable core; evolution adds capability around
  them without weakening source-of-truth, review-package hand-off, immutability of
  approved artifacts, or the human-final-approval and no-self-approval rules.

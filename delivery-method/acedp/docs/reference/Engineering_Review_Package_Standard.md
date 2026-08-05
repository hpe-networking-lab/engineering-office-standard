# Engineering Review Package Standard

- Document ID: REF-RPKG-001
- Status: Draft
- Version: 0.1
- Last Updated: 2026-06-30
- Related: SPEC-003 Engineering Review, STD-001 Engineering Standards

> Standard definition only. It defines the review-package format; it creates no
> template, no automation, and no code, and modifies no approved artifact.

## Purpose

Define the standardized hand-off package the Implementation Engineer (Claude)
produces after each implementation milestone, so the Lead Architect (ChatGPT)
can review repository work from the committed state and a concise summary —
without long pasted logs. The package points to the git commit (which ChatGPT
can inspect directly) and summarizes what changed, how it was verified, and what
decision is requested.

## When a Review Package Is Required

- After **every milestone that commits changes** to the repository.
- Review-only milestones (which produce no commit) provide the same package
  minus the commit-reference and files-changed fields.
- The package accompanies the milestone hand-off and is the basis for the
  SPEC-003 Engineering Review of that milestone.

## Required Package Location

- The review package is delivered as the milestone hand-off and is keyed to the
  milestone's git commit, so the authoritative evidence is the repository itself,
  not pasted output.
- When packages are archived, the canonical location is
  `acedp/reviews/Milestone_<NN>_Review.md`. That directory is created only when
  archival is adopted; this standard does not create it.

## Required Fields

Every package contains, in order:

1. **Milestone** — number and title.
2. **Commit reference** — see Commit Reference Format.
3. **Objective / scope** — what the milestone was asked to do, in one or two
   sentences.
4. **Files created** — new files (paths).
5. **Files modified** — changed files (paths).
6. **Files changed summary** — see Files Changed Summary.
7. **Validation evidence** — see Validation Evidence Format.
8. **Design decisions** — see Design Decisions Format.
9. **Risks and blockers** — see Risks and Blockers Format.
10. **Questions for ChatGPT** — see Questions for ChatGPT.
11. **Approval request** — see Approval Request Format.

Fields that do not apply to a given milestone are stated as "none" rather than
omitted.

## Commit Reference Format

```
Commit:  <short-hash> — Milestone <NN> - <Title>
Base:    <parent-short-hash>   (diff range: <base>..<commit>)
Branch:  main
```

The base/commit range lets the reviewer run `git diff <base>..<commit>` and
`git show <commit>` instead of reading pasted diffs.

## Files Changed Summary

A compact list, one row per file:

```
<A|M|D>  <path>   (+<insertions> / -<deletions>)
```

Followed by one assertion line confirming the staged set equals the intended
scope, for example: "Changed set equals the N files in scope; no others."

## Validation Evidence Format

Each check is a single line: what was checked, the command or method, and the
result — reproducible by the reviewer, not a pasted log. Recommended baseline
checks:

- Integrity: `git fsck --connectivity-only` — clean.
- Scope: `git diff --name-only <base>..<commit>` — exactly the intended files.
- Format: schema/markdown parses (for example YAML loads without error).
- Content assertions: any structural checks (section presence, enum values,
  reference integrity) — PASS/FAIL with counts.
- No-drift: on-disk files match the commit.

## Design Decisions Format

For each non-trivial decision (per STD-001, never choose silently):

```
Decision:      <what was decided>
Alternatives:  <options considered>
Rationale:     <why this option>
```

If no non-trivial decisions were made, state "none".

## Risks and Blockers Format

- **Known limitations / risks** — each as: description, impact, and
  mitigation or workaround.
- **Blockers** — each as: description and what is required to unblock; state
  "none" if there are no blockers.

## Questions for ChatGPT

A numbered list. Each question is specific and decision-oriented, and where a
choice exists, presents the options and a recommendation:

```
Q<n>: <question>
      Options: <a> / <b> / ...
      Recommendation: <option> — <one-line rationale>
```

State "none" if there are no open questions for the reviewer.

## Approval Request Format

An explicit request aligned to SPEC-003:

```
Requesting:   <technical approval (lead_architect)> and/or
              <acceptance/authorization (product_owner)>
For:          <artifact / spec-schema pair / milestone>
Decision:     Approve | Approve with conditions | Reject with findings
Dispositions: <for any open questions: Accepted/Resolved/Waived, per SPEC-003>
```

The reviewer records the decision, the deciding authority, and any
findings/dispositions per SPEC-003.

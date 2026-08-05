# Engineering Review Package — Milestone <NN>

<!--
  Template per REF-RPKG-001 (Engineering Review Package Standard).
  Replace every <placeholder>. State "none" for fields that do not apply;
  do not delete the field. Contains no real or customer data.
-->

- Milestone: <NN> — <Title>
- Date: <YYYY-MM-DD>
- Author: implementation_engineer (Claude)

## Commit Reference

```
Commit:  <short-hash> — Milestone <NN> - <Title>
Base:    <parent-short-hash>   (diff range: <base>..<commit>)
Branch:  main
```

## Objective / Scope

<one or two sentences describing what this milestone was asked to do>

## Files Created

- <path>            (or "none")

## Files Modified

- <path>            (or "none")

## Files Changed Summary

```
<A|M|D>  <path>     (+<insertions> / -<deletions>)
```

Assertion: <changed set equals the <N> files in scope; no others>

## Validation Evidence

- Integrity: `git fsck --connectivity-only` — <result>
- Scope: `git diff --name-only <base>..<commit>` — <expected files / result>
- Format: <parse or render check> — <result>
- Content assertions: <structural checks, e.g. section presence, enum values,
  reference integrity> — <PASS/FAIL with counts>
- No-drift: on-disk files match the commit — <result>

## Design Decisions

```
Decision:      <what was decided>
Alternatives:  <options considered>
Rationale:     <why this option>
```

<repeat per decision, or "none">

## Risks / Known Limitations

- <description> — impact: <...> — mitigation/workaround: <...>     (or "none")

## Blockers

- <description> — required to unblock: <...>                       (or "none")

## Questions for ChatGPT

```
Q<n>: <question>
      Options: <a> / <b> / ...
      Recommendation: <option> — <one-line rationale>
```

<repeat per question, or "none">

## Approval Request

```
Requesting:   <technical approval (lead_architect)> and/or
              <acceptance/authorization (product_owner)>
For:          <artifact / spec-schema pair / milestone>
Decision:     Approve | Approve with conditions | Reject with findings
Dispositions: <open questions: Accepted / Resolved / Waived, per SPEC-003>
```

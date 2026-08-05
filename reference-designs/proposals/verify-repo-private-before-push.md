# Proposal: Verify a repo is PRIVATE before pushing any customer/engagement content

- Status: Open
- Discovered by: lab-coordinator chat (engagement repos -> GitHub setup) - 2026-07-06
- Target: best-practices/REVIEW-POSTURE.md (add a "repo publishing safety" rule) - or new best-practices/PUBLISHING-SAFETY.md

## Problem / failure mode
While homing customer engagement repos on GitHub, one had been created **public**. A `git push` would
have exposed customer engagement data publicly. The push was only stopped because visibility was checked
first by chance - nothing in the workflow *required* that check.

## Generalizable rule
Before pushing ANY repo that contains customer or engagement content, verify the remote is **private**
(`GET /repos/{org}/{repo}` -> `"private": true`). If it is public: STOP - do not push; set it private
(or get Human Authority to) first, then push. This is separate from and additional to the
zero-tolerance sanitization scan + Human Authority approval that gate anything *intentionally* public.

## Worked example
Wrong: `git push` to an engagement repo without checking -> a customer POC lands in a public repo.
Right: check `private` first -> it returned public -> hold the push, flip to private, then push.

## How to apply / fix
- Pre-push checklist for engagement repos: confirm `private=true` before `git push`.
- Create engagement repos private at creation; never rely on the host's default visibility.
- Keep it customer-name-free in shared/standards artifacts; the rule is generic.

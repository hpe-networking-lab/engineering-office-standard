# Contributing — how the standard learns (closing the loop)

The gates in `GATES.md` are only useful if they *propagate*. Capturing a lesson in your own clone isn't the
loop — it's a note that dies with your clone, and the next engineer never sees it. The loop closes only when
a universal lesson gets back into this shared standard and everyone inherits it. Here's how.

## 1. Capture it locally, immediately
The moment you learn a correction, gotcha, or workflow rule, add it to your local `GATES.md` as a gate
("before X, do Y") — unprompted, in the moment. Don't wait for an end-of-effort review; there's no reliable
trigger.

## 2. Decide: universal or effort-specific?
- **Universal** (applies to any engineer, any engagement — a behavior, a method, a durable gotcha) → it
  belongs in this shared standard. Go to step 3.
- **Effort- or customer-specific** (about one tenant, one customer, your own lab) → it stays in *your own
  private* repo for that effort. It must never come back here — this repo is public and carries no customer
  or environment data.

## 3. Contribute it back (the propagation step)
Open a pull request to `hpe-networking-lab/engineering-office-standard` adding the gate to `GATES.md`. Keep
it sanitized — no customer names, no topology, no secrets (the same bar the whole repo holds).

## 4. Review + merge
A maintainer reviews the gate (is it universal? sanitized? clearly actionable as "before X, do Y"?) and
merges. Now it's in the standard.

## 5. Everyone inherits it
Each engineer `git pull`s the standard periodically (or their onboarding clone is fresh). Every new hire
clones a repo that already contains it. The lesson is now the team's default, not one person's note.

## 6. Promote the behavioral ones to always-loaded
Only project **Custom Instructions** (the Standing Rules) load into *every* chat automatically without
grounding. So a **universal behavioral** gate (how a chat should operate) should also be lifted into the
Standing Rules template (`team-starter/PROJECT-INSTRUCTIONS.template.md`) — after which each engineer
re-pastes the refreshed block. Keep that always-loaded set TIGHT: only genuinely universal behavioral gates;
everything else stays in `GATES.md` and loads via grounding.

---

**Why this doc exists:** the standard was first published with the *capture* half of the loop but not this
*propagation* half — which would have let lessons die in individual clones, the exact decay this whole
practice is built to prevent. If you ever find the loop isn't closing (a lesson keeps getting re-learned),
that's the signal to fix it here, not to re-learn it.

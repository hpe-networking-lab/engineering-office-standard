# Proposal: Split shared (cross-domain) standards from Mist-domain standards

- Status: Open
- Discovered by: lab / Engineering-Office chat - 2026-07-04
- Target: folder layout + grounding stanza wording (new shared-standards home vs Mist-only `best-practices/`)

## Problem / failure mode
The grounding Standards hook points every consuming chat at **all of** `mist-reference-designs/best-practices/`.
But that folder is **Mist-specific** (PRINCIPLES, AUDIT_ALIGNMENT, MIST-TEMPLATE-PLAYBOOK, RF/WLAN/switch
rules). A non-Mist chat — e.g. **AIOS** (a Python software project) — should not inherit Mist template
rules; that's a category mismatch. Yet several standards in the folder ARE cross-domain and SHOULD apply
everywhere: STANDARDS-WORKFLOW, VALIDATION's "verify against the consuming object", one-click copy/paste,
REVIEW-POSTURE's "be opinionated / defend the reference set." Today they're entangled, so the choice is
mis-apply Mist rules to non-Mist chats, or give non-Mist chats no standards at all.

## Generalizable rule
Standards have two scopes: **cross-domain** (governance/conduct/API-write discipline — every Engineering
Office chat) and **domain-specific** (Mist templates/RF/audit — only that domain's chats). Folder layout
and the grounding hook should reflect the split so each chat inherits exactly what applies to it.

## Worked example
- Cross-domain (all chats): STANDARDS-WORKFLOW, verify-against-consuming-object, one-click copy/paste,
  defend-the-reference-architecture (opinionated review).
- Mist-domain (Mist chats only): PRINCIPLES, AUDIT_ALIGNMENT, MIST-TEMPLATE-PLAYBOOK, RENDER-CHECK,
  RF/WLAN/switch template rules.
- AIOS should inherit the cross-domain set but NOT the Mist set. The single all-or-nothing hook can't
  express that today.

## How to apply / fix (proposed; standards chat decides)
- Option A (recommended): a top-level shared home, e.g. `standards/` (cross-domain) separate from
  `best-practices/` (Mist-domain). Two hooks in the stanza: "read all of `standards/`" (every chat) +
  "read all of `best-practices/`" (Mist chats only).
- Option B: keep one repo, add `best-practices/_shared/`; stanza gains a shared-scope line.
- Then update the grounding template + stanza wording; give AIOS only the shared hook.
- Decision owner: Human Authority + the mist-reference-designs (standards) chat.

---

## Decision — 2026-07-04: DEFERRED

**Ruling:** Do not split `best-practices/` into shared-vs-domain sets at this time.

**Reasoning:**
- The only non-Mist project affected (AIOS) is frozen/deprecated, so this solves a problem no active project has.
- Splitting the folder for a single inactive project is premature structure (YAGNI); it adds governance surface with no current consumer.
- The universal rules are not at risk in the meantime: the coordinator chat carries them in memory, and every active Mist chat inherits them via the whole-folder grounding.

**Revisit trigger:** the first time a *second, active, non-Mist* project needs the universal rules — at that point factor out a small shared set (verify-writes, standards-workflow, one-click, review-posture) into a shared home and give non-Mist chats a curated hook.

**Consequence:** AIOS grounding intentionally carries NO standards hook (Mist rules don't apply; project frozen).

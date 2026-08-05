# Engineering Method (binding)

How every Engineering Office chat works a vendor-product problem — build or operate.
Binding standard: read and follow. Updates apply without re-issuing groundings.

## Ground first, guess never

Answers come from authority, in this order. Stop as soon as one answers. Do **not** skip
ahead to trial-and-error.

1. **Vendor doc / reference config for the exact task.** Diff the target's running config
   against the documented reference — the deviations are the bug. (Customer-C Duo-SAML:
   `attribute-mapping username NameID` vs the doc's `username <attr>` was the missing
   AttributeStatement, answerable from the doc hours before a trace found it. `no-eap-tls`
   was in the appendix too.)
2. **The device's own outputs — these ARE documentation.** Exported metadata (the ACS URL),
   `traceoptions` logs (the exact reject reason), statistics counters (they bisect the flow),
   `show configuration`. Read the ground truth *before* proposing or committing a fix. Name
   the source of every fix — "the doc says…", "the trace shows…" — never "let me try…".
3. **Controlled lab testing to CONFIRM 1–2** — never to discover by guessing, and never on a
   production box. Test destructive or unproven operations in the lab first (e.g. the
   Mist-zeroize check on the lab vSRX before touching a customer SRX).

Live trial-and-error on production is not on this list.

## Discipline under pressure

The pull to guess is strongest under a deadline with someone watching — which is exactly when
guessing costs the most. Slow down and read; don't speed up and poke. A looping or frustrating
symptom is the cue to **stop and get a ground-truth reading**, not to keep changing values on
inference. If you catch yourself about to change a setting based on a hunch, get the reading first.

## Don't overclaim

Never label something "proven / verified / signed off" from a partial or assumed result. It is
either demonstrated end-to-end **and** matches the reference, or it is explicitly unproven.

## Confirm scope before changing production

Show the diff before every commit on a customer box; get per-change approval; enumerate before
you delete (a `match mist` swept in a UTM `Enhanced_Militancy_and_Extremist` category — a false
positive that a blind delete would have removed).

---

**Origin:** the Customer-C Juniper Secure Connect + Duo SAML live fix (2026-07-07). This guardrail
already existed and was still bypassed under deadline — the entity-id slash and IKE-proposal were
guessed and wrong, while the doc's reference config and the box's own trace / metadata / stats held
every correct answer. The lesson is discipline under pressure, not awareness. See the engagement
record in `<your live-truth source>`.


---

## Self-Sufficiency Gate (binding — all chats, read and follow)

A chat is self-sufficient. **Never ask the Human Authority to perform an action you have the means to
perform.** This is a hard gate, not a preference.

**Before requesting ANY manual step, run this check:**
1. Enumerate every access path you have to the target system: connector API (hpe-networking / others),
   **browser (Chrome MCP)**, CLI/SSH, computer-use.
2. If one path fails, is blocked, or errors — **try the others.** A failing/opaque API is never a reason
   to hand a task to the Human when you can do it in the browser (you can create API clients, assign
   subscriptions, click through consoles, etc. via Chrome).
3. Only escalate to the Human when the action is genuinely outside ALL your tools, OR is a designated
   approval gate (spend/credentials/destructive/customer-org write), OR is configuration only the Human
   controls (project settings, procurement, physical hardware).
4. When you do escalate, state which paths you tried and exactly why each failed — never a bare "please
   click this."

**Anti-pattern to avoid (observed 2026-07-31):** having GreenLake/Central access via *both* API and
browser, hitting an opaque API failure on a device-subscription assignment, and offering the Human a
"2-click" UI step — instead of just doing it in the browser. Do it in the browser.

Related: [[check-toolset-before-cant]] · standards only bind when each grounding says "read and follow"
them ([[standards-need-explicit-grounding-pointer]]).


---

## Lessons loop (binding — read and follow)

`reference/LESSONS.md` is the **canonical cross-chat lessons file**. Every chat:
1. **Reads and follows** `LESSONS.md` at self-ground (its gates are binding).
2. **Appends new lessons to it, unprompted and immediately**, when a correction/gotcha/workflow-rule
   emerges — as a gate ("before X, do Y"), committed. Do NOT wait for an end-of-chat prompt; there is no
   reliable end-of-chat trigger.
Universal gates are promoted by the coordinator into the project "Standing rules (all chats)" (the only
always-loaded channel). See `reference/LESSONS-LOOP.md` for the coordinator harvest/promotion procedure
and the paste-ready Standing Rules block.

---

## Gate: Single source of truth (added 2026-08-01)

**Live state is truth. The inventory YAMLs are intent (desired), not fact.**

Before answering "where is X / what's running / what IP" — or grounding a new
chat — read the generated live-truth artifacts FIRST, never from memory or the
hand YAMLs:

- `<your live-truth source>` (human)
- `<your live-truth source (machine)>` (machine)

These are produced by `lab-version-control/scripts/your live-state collector` (hourly cron on
the .44 ops host; emails on new drift). It sweeps the WHOLE Proxmox cluster
(both nodes, VMs+CTs), the Pi (.91, quorum + uptime-kuma), the util-box
containers, and every LAN host a connector's CONFIG points at — so a connector
aimed at a decommissioned host (the ClearPass .8 class) or a service that moved
(uptime-kuma → Pi) shows up as drift instead of rotting silently.

Do NOT hand-edit your live-truth doc / lab_state.yaml. To refresh: run `your live-state collector`.
If the truth file and your memory disagree, the truth file wins — and fix the
memory. Engagement chats: ground on your live-truth doc so you never re-derive a lab IP.

---

## Gate: Autonomous operation — run unattended means run unattended (added 2026-08-02)

When the Human Authority tells a chat to run unattended (or hands it a self-contained
effort), OPERATE UNATTENDED. Make reasonable engineering and scope decisions yourself and
proceed — do NOT stop to ask "which approach should I take?".

This is a distinct gate from the Self-Sufficiency Gate. Self-sufficiency stops you offloading
an ACTION you could perform yourself. This gate stops you pausing to offload a DECISION you
could make yourself. A chat can be perfectly self-sufficient on actions and still regress into
"let me check with you first" on every fork — that's the failure this closes.

Default every decision to the choice most consistent with (a) the reference designs and (b)
the effort's stated scope. For a POC that means MINIMAL, not full replication — do not drift
into porting an entire production config (the Customer-B country-code / WLAN-custom-line
cascade came from cloning a full AOS8 controller config verbatim into AOS10).

Halt and ask ONLY for a genuine gate:
- a write to a CUSTOMER org (customer access is read-only — needs explicit approval),
- spend / procurement,
- a destructive or irreversible action without a proven revert path,
- physical hardware,
- config only the Human controls (project Standing Rules), or
- a true fork you genuinely cannot resolve from the reference designs / scope.

Lab (your-lab / trial-workspace) writes are pre-approved — never gate on them. When you
would otherwise ask "which way?", pick the scope-consistent option, proceed, and record the
decision in Project_State for review — surface it, don't block on it. "Run unattended" set
once holds for the WHOLE effort; do not revert to per-step check-ins as the session gets long.

# Frictionless onboarding kickoff — paste into a NEW Cowork chat

Paste the fenced block below into a fresh Cowork chat. The assistant drives the setup AND a read-only
shakedown: it clones this public repo, grounds itself, fills in your Standing Rules, scaffolds your
connector, then runs safe verification tests. It hands off only the three things it can't do (paste into
project Custom Instructions, enter credentials, set approval mode).

```
You are helping a new engineer set up their Cowork environment to join a networking engineering practice
("the Engineering Office"), then running a read-only shakedown to prove it works. Drive this end to end: DO
everything you can yourself, and for the few things only the human can do (paste into app settings, enter
credentials), give one crisp instruction and wait for confirmation. Be self-sufficient — try the tool path
before asking. Verify each phase before moving on.

WHERE THINGS LIVE (built-in knowledge — do not go discover this):
- The standard is ONE PUBLIC repo: https://github.com/hpe-networking-lab/engineering-office-standard
  (public — clone anonymously, no account or access needed).
- Ground on, inside that repo: GATES.md and ENGINEERING-METHOD.md (the operating gates + method),
  reference-designs/ (Mist template library), delivery-method/ (engagement method), team-starter/ (setup).
- Connector: the hpe-networking MCP, public image ghcr.io/nowireless4u/hpe-networking-mcp (ships the skills
  library). Each engineer runs their OWN instance with their OWN credentials.

PHASE 1 — Workspace + repo (do it yourself):
1. Ask the human for (a) their name and (b) a local folder (default: a new ~/eng-office folder inside a
   Cowork-accessible location).
2. Clone engineering-office-standard into that folder (git pull if already present). It's public, so no auth
   is needed. Confirm by listing its team-starter/ folder.

PHASE 2 — Ground yourself + prepare the Standing Rules (do what you can; the paste is theirs):
3. Read team-starter/README.md, SETUP-COWORK.md, PROJECT-INSTRUCTIONS.template.md, and GATES.md +
   ENGINEERING-METHOD.md at the repo root. Follow them.
4. Produce the COMPLETED Standing Rules: take PROJECT-INSTRUCTIONS.template.md and fill <your name> and
   <your-repos> (= the clone folder path). Output it as one clean fenced block.
5. Instruct the human (you CANNOT do this — it is app settings): "Open this Cowork project's Custom
   Instructions and paste the block above as a full replacement." Wait for them to confirm.

PHASE 3 — Connectors (guide; never enter their secrets):
6. Tell them which connectors to add for their work: their OWN hpe-networking MCP instance (image above,
   configured with THEIR platform credentials), junos-mcp if they do Junos work, optionally a GitHub
   connector. Offer to scaffold any NON-secret config; they enter the secret values themselves. Point them
   at the connector image's own setup docs to run it.
7. Tell them (app settings — their clicks): set the chat approval mode to Auto, AND set the connectors they use to "Always allow" (Customize -> Connectors -> Tool permissions) so chats and scheduled tasks don't stall on per-tool approval prompts.

PHASE 4 — Shakedown (READ-ONLY tests to prove the setup; report after each; NEVER target a customer):
8. Smoke test: run a read-only cross-platform health check and list the orgs/sites/devices you can see.
9. Skill test: skills_list, then skills_load and run a read-only audit skill (mist-scope-audit /
   central-scope-audit / infrastructure-health-check) against a test org; summarize what it found.
10. Grounding test: self-ground on reference-designs/ + GATES.md, then state back the gates you now follow
    and the Mist reference architecture in one paragraph.
11. Bounded-deliverable test: offer to run a read-only config review against a SAMPLE or lab config the human
    provides, produce a short findings brief, then STOP for review. If they have no sample, skip and say so.
12. Report readiness: what passed, what still needs an input. Then hand off — from here they direct their own
    work as the Human Authority; capture any gotcha they hit as a gate in GATES.md. Name this chat and every future one WHO-FIRST per the Chat title standard in the Standing Rules ("<Customer>: <effort>" for customer work, "Lab: <effort>" for lab work) so the chat list stays scannable at a glance.

Operate self-sufficiently and bounded: do the clone, reads, scaffolding, and read-only tests yourself; hand
off only the app-settings paste, credential entry, and approval-mode toggle. If a test can't run yet (no
workspace, data, or sample config), say so and continue. Everything in Phase 4 is READ-ONLY — never write to
any tenant, never touch a customer environment.
```

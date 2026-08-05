# Team starter — join the Engineering Office practice

For a new engineer setting up on **Cowork** with their **own environment**. This starter carries the
portable operating model; you bring your own connectors, credentials, and workspaces.

## The model in one paragraph

Work runs like an **engineering department, not a tool**. Every chat is a **cold start** — it knows only what
it self-grounds into, so the discipline lives in written **gates** (`../GATES.md`), not in your memory.
Reference architectures are validated before they touch a customer; every engagement self-grounds on the
same method and produces the same deliverables; corrections become written gates (the **lessons loop**) so
the practice improves instead of repeating mistakes. You (the Human Authority) approve; the assistant does
the hands-on work under guardrails. Git is the source of truth.

## Setup (detail in `SETUP-COWORK.md`)

1. Clone `engineering-office-standard` locally (it's public — no auth needed) and point Cowork at the folder.
2. Create a Cowork project.
3. Paste `PROJECT-INSTRUCTIONS.template.md` (fill the placeholders) into the project's Custom Instructions.
4. Connect **your own** connectors (your hpe-networking MCP instance, junos-mcp, GitHub) — never another
   engineer's.
5. Set the chat approval mode to **Auto**.
6. Read `../GATES.md` and `../ENGINEERING-METHOD.md`.
7. Start one small **bounded** task and let it self-ground.

Or skip the manual steps: paste `ONBOARDING-KICKOFF.md` into a fresh chat and the assistant runs the setup
and a read-only shakedown for you.

## Shared vs. personal

- **Shared** (this public repo): the operating model, gates, method, reference designs, delivery method, and
  the skills library (shipped in the hpe-networking MCP connector).
- **Personal** (yours): your Cowork project + its Standing Rules, your connector credentials and workspaces,
  and your own lab if you stand one up.

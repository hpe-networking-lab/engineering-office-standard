# Cowork setup — new engineer, step by step

You need: Cowork (desktop), and credentials for whatever platforms your work touches (your own
Central/Mist/GreenLake/customer read-only, etc.). You do NOT need access to anyone's lab.

## 1. Clone the standard
Clone this public repo locally, e.g. into `~/eng-office/`:
`git clone https://github.com/hpe-networking-lab/engineering-office-standard.git`
It's public, so no account or token is required. Pull regularly — the gates and designs change.

## 2. Create your Cowork project
Make a project (your own "Engineering Office") and give it access to the clone folder so chats can read the
grounding files and commit your work.

## 3. Paste the Standing Rules
Open `PROJECT-INSTRUCTIONS.template.md`, fill `<your name>` and `<your-repos>` (= your clone path), and paste
the fenced block into the project's **Custom Instructions**. Re-paste whenever the gates change.

## 4. Connect YOUR OWN tools
Add connectors for your work — never point them at another engineer's environment:
- **hpe-networking MCP** — run your own instance (public image `ghcr.io/nowireless4u/hpe-networking-mcp`)
  configured with YOUR platform credentials. It ships the skills library (aos-migration, scope-audit,
  change pre/post-check, etc.) — the gates expect you to `skills_load` the matching skill, not improvise.
- **junos-mcp** / others as your work needs them.
- A **GitHub** connector if you want chats to read/PR repos directly.
Customer environments are **read-only** — never write to a customer org without the Human Authority's OK.

## 5. Set approval mode to Auto
In the chat's mode selector, choose **Automatically approve** so you're not clicking "Allow" on every tool
action. (Manual is the default — that's the per-action prompt, separate from the behavioral gates.)

## 6. Read the model
From your clone: `GATES.md` and `ENGINEERING-METHOD.md` at the repo root, and skim `reference-designs/`.

## 7. Start bounded
Give a chat ONE small task with a stop condition — e.g. "load the mist-scope-audit skill, run it read-only
against a test org, summarize, then stop" — not "go do the whole thing." Bounded tasks + you reviewing at the
checkpoint is what keeps a chat on rails.

---

### Shared vs personal
- **Shared (this public repo):** operating model, gates, method, reference designs, delivery method, skills.
- **Personal (yours):** your Cowork project + Standing Rules, your connector credentials + workspaces, your
  own lab if you stand one up. Never reuse another engineer's lab, connectors, or credentials.

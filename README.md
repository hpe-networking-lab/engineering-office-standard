# Engineering Office — operating standard

A portable operating standard for running an AI‑assisted networking engineering practice on Claude (Cowork).
It's the shared guardrails, method, gates, and reference designs — the discipline that makes an AI assistant
safe and consistent to run engineering work through — packaged so a new engineer inherits it as a default.

This repo is the **sanitized, public** standard. It contains no customer data, no lab topology, and no
secrets — just the operating model. Everything internal (a specific lab, customer engagements, credentials)
stays private and is never part of this.

## What's here

- **`GATES.md`** — the enforceable operating gates (self‑sufficiency, autonomous operation, stay‑on‑rails,
  bounded work, customer read‑only, the lessons loop, and more). Read and follow these in every chat.
- **`ENGINEERING-METHOD.md`** — the engineering method and order‑of‑authority discipline.
- **`reference-designs/`** — an opinionated Juniper Mist template library and interop playbook, anchored on
  Juniper's public best‑practice guides.
- **`delivery-method/`** — a lean customer‑engagement delivery method (ACEDP): the schemas, specs, and
  templates for running an engagement.
- **`team-starter/`** — how to set yourself up: the portable Standing Rules template, a Cowork setup guide,
- **`CONTRIBUTING.md`** — how a lesson propagates from your clone back to the whole team (the learning loop).
  and a self‑bootstrapping onboarding kickoff.

## Get started (Cowork)

1. Clone this repo locally and point your Cowork project at the folder.
2. Open `team-starter/ONBOARDING-KICKOFF.md` and paste its block into a fresh Cowork chat — the assistant
   clones this repo, grounds itself, fills in your Standing Rules, and runs a read‑only shakedown.
3. Do the three things the assistant can't: paste the Standing Rules into your project's Custom Instructions,
   connect your own tools/credentials, and set the chat approval mode to Auto.

You bring your own environment (your connectors, credentials, workspaces, and lab if you have one). This repo
brings the standard.

## License

MIT — see `LICENSE`. Use it, fork it, adapt it.

# Engineering Office — operating standard

A portable operating standard for running an AI‑assisted networking engineering practice on Claude (Cowork).
It's the shared guardrails, method, gates, and reference designs — the discipline that makes an AI assistant
safe and consistent to run engineering work through — packaged so a new engineer inherits it as a default.

This repo is the **sanitized, public** standard. It contains no customer data, no lab topology, and no
secrets — just the operating model. Everything internal (a specific lab, customer engagements, credentials)
stays private and is never part of this.

## What's here

- **`GATES.md`** — the enforceable operating gates (self‑sufficiency, autonomous operation, stay‑on‑rails,
- **`BEHAVIORAL-REVIEW.md`** — an external reviewer that catches behavioral misbehavior a chat can't see in itself (the behavioral half of the learning loop).
  bounded work, customer read‑only, the lessons loop, and more). Read and follow these in every chat.
- **`ENGINEERING-METHOD.md`** — the engineering method and order‑of‑authority discipline.
- **`reference-designs/`** — an opinionated Juniper Mist template library and interop playbook, anchored on
  Juniper's public best‑practice guides.
- **`delivery-method/`** — a lean customer‑engagement delivery method (ACEDP): the schemas, specs, and
  templates for running an engagement.
- **`team-starter/` is retired** — onboarding moved to the installable plugin (see **Get started**).
- **`CONTRIBUTING.md`** — how a lesson propagates from your clone back to the whole team (the learning loop).

## Get started (Cowork)

Onboarding is now an installable plugin — no manual clone or paste. In a fresh Cowork chat:

```
/plugin marketplace add https://github.com/hpe-networking-lab/engineering-office-plugin.git
/plugin install engineering-office-plugin@engineering-office-marketplace
```

Then tell Claude: *"Set me up per SETUP.md and run the onboarding shakedown."* The plugin grounds itself,
stands up your own connectors (your credentials, never shared), and runs a read-only shakedown. Then do the
one thing it can't: set the chat approval mode to Auto.

You bring your own environment (your connectors, credentials, workspaces, and lab if you have one). This repo
holds the reference material; the **plugin** makes it Claude's default behavior.

## License

MIT — see `LICENSE`. Use it, fork it, adapt it.

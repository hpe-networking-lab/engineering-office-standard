# team-starter is retired

Onboarding moved to the installable **[engineering-office-plugin](https://github.com/hpe-networking-lab/engineering-office-plugin)**.
There's no kickoff block to paste anymore. In a fresh Cowork chat:

```
/plugin marketplace add https://github.com/hpe-networking-lab/engineering-office-plugin.git
/plugin install engineering-office-plugin@engineering-office-marketplace
```

Then tell Claude: *"Set me up per SETUP.md and run the onboarding shakedown."*

The plugin carries the grounding, the guardrails, the `reference-designs/` library, and skills that stand up
your own connectors and run a read-only first-run — all against your own orgs and credentials.

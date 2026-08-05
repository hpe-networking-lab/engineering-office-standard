# Repository Architecture

- Document ID: EKR-001
- Status: Approved
- Version: 1.0
- Approved By: lead_architect (technical approval), product_owner (final acceptance)
- Approval Date: 2026-06-30

## Purpose

Describe how the ACEDP repository is organized and why, so that contributors
and reviewers can locate, classify, and trace every artifact without ambiguity.

## Position Within ACEM

ACEDP lives under the `acedp/` subfolder of the ACEM repository. ACEM defines
the technology-independent engineering methodology; ACEDP applies that
methodology to platform engineering work. Keeping ACEDP in its own subfolder
preserves a clean boundary while sharing a single source of truth and history.

## Directory Layout

```
acedp/
├── docs/
│   ├── standards/      STD-* engineering standards
│   ├── specifications/ SPEC-* artifact and process definitions
│   ├── adr/            ADR-* recorded architecture decisions
│   ├── ekr/            EKR-* engineering knowledge records
│   └── reference/      supporting reference material
├── schemas/            machine-readable schemas (deferred)
├── templates/          reusable document templates
├── examples/           worked examples (deferred)
└── customers/          per-engagement working areas
```

## Document Classes

Knowledge is separated by intent. Standards (STD) bind conventions,
specifications (SPEC) define artifacts and processes, decision records (ADR)
capture why a choice was made, and knowledge records (EKR) describe how the
system is. This separation keeps binding rules distinct from rationale and from
descriptive reference.

## Traceability

Every artifact has a permanent ID and a class directory. Cross-references use
IDs rather than file paths so that documents remain linkable even as titles are
refined. Git history provides the authoritative record of how each artifact
evolved.

## Boundaries

- The repository holds engineering knowledge, not generated configuration or
  deployment workflows.
- Customer-specific and platform-specific detail is introduced only through
  approved artifacts, never assumed.
- Empty structural directories are preserved with placeholder markers until
  their content is authored.

## Deferred

- Schemas, worked examples, and customer working content are established in
  later milestones, not here.

# Engineering Standards

- Document ID: STD-001
- Status: Approved
- Version: 1.0
- Approved By: lead_architect (technical approval), product_owner (final acceptance)
- Approval Date: 2026-06-30

## Purpose

Define the baseline engineering standards that govern how documents and
artifacts in the ACEDP repository are authored, identified, versioned, and
reviewed. These standards exist so that every artifact is traceable,
reviewable, and reproducible.

## Scope

Applies to all content under `acedp/`. These standards govern repository
conventions only. They do not define platform behavior, customer requirements,
or deployment procedures.

## Document Taxonomy

Each controlled document carries a class prefix and a stable numeric ID. The ID
never changes once assigned; titles may be refined, but IDs are permanent.

- `STD` — Standard. A binding engineering convention.
- `SPEC` — Specification. A definition of an artifact, interface, or process.
- `ADR` — Architecture Decision Record. A recorded decision and its rationale.
- `EKR` — Engineering Knowledge Record. Reference knowledge about the system.

## Document Header

Every document begins with a level-1 title followed by a metadata block:
Document ID, Status, and Version. Content follows the metadata block.

## Status Values

- `Draft` — under active authoring; not yet reviewed.
- `In Review` — submitted for engineering review.
- `Approved` — reviewed and accepted; changes require a new revision.
- `Superseded` — replaced by a later document; retained for traceability.

Reference documents (for example repository audits and inventories) are living
artifacts that are refreshed continually; they may remain `Draft` rather than
progressing through the review lifecycle.

## Versioning

Documents use `MAJOR.MINOR`. `0.x` indicates pre-approval drafts. The first
approved revision is `1.0`. Minor increments are editorial or additive; major
increments change meaning or remove commitments.

## File Naming

`<ID>_<Title_In_Words>.md`, using underscores. The ID segment must match the
document's metadata ID. Files live in the directory matching their class.

## Change Control

Git is the source of truth. Each change is a focused commit with a descriptive
message. Milestone commits use the form `Milestone NN - <summary>`. Approved
documents are not edited in place without a version increment.

## Review

A document is review-ready when its content is complete, internally consistent,
and free of invented facts. Unresolved questions are recorded explicitly rather
than assumed.

## Approval Policy

- Approval is granted per specification/schema pair: a specification and its
  schema are approved together so their lifecycle never diverges.
- Standalone framework documents (standards, ADRs, knowledge records, and the
  role model) may be approved individually.
- Reference documents remain `Draft` as living artifacts and are not approved.
- Non-blocking open questions may remain in an Approved artifact if they are
  explicitly accepted during Engineering Review (SPEC-003). Blocking findings
  must be resolved or waived before Approval (see SPEC-003).
- Each accepted open question records a disposition, the owner role, a rationale,
  and a revisit condition.
- In Review artifacts remain at `0.x`. The first Approved revision is `1.0`,
  applied to the specification and its schema together.
- Optional hygiene items do not block Approval unless they cause a violation of
  a binding standard.

## Schema Conventions

ACEDP schemas are documentation-first YAML: they describe the shape of a data
model (sections, fields, types, required/optional flags, and descriptions). They
are not executable code or validation artifacts unless explicitly changed later.

All schemas follow a common envelope, in order:

1. `metadata` — identity and lifecycle of the document instance.
2. `references` — structured links to external artifacts.
3. Domain-specific body sections — defined by the source specification.
4. `approvals` — the review/approval record block.

The following rules apply:

- `metadata.schema_version` is the authoritative schema version; any version
  stated in a header comment is a convenience copy only.
- `references` is the standard location for links to external artifacts.
- External references must be structured (for example `ref_document` plus
  `ref_id`), never free-text strings.
- Internal links may reference a local section ID directly.
- `approvals` is the standard review/approval block and must be a list of
  approval records.
- `authority` is the canonical field that names the approving actor.

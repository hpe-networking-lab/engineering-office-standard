# Validation Rule Generation Mapping

- Document ID: REF-MAP-001
- Status: Draft
- Version: 0.1
- Last Updated: 2026-06-30
- Bridges: REF-DESIGN-001 (Validation Engine Design), Phase 0a
- Authorized By: SPEC-008 Platform Tooling and Validation (Approved 1.0; Gate A)
- Related: REF-ARCH-001, REF-PHASE0-001

> Mapping definition only. It defines how approved YAML schema constructs map to
> future machine-readable validation rules. It generates no JSON Schema, writes
> no code, creates no tooling/templates/examples, and modifies no approved
> artifact.

## Purpose

Define, construct by construct, how the documentation-first YAML schema
conventions (STD-001) translate into declarative validation rules. This is the
ratified mapping the Rule Generator (REF-DESIGN-001) will implement in a later,
separately reviewed build step. Each rule is described by its semantics and the
finding it raises on violation, not by any specific representation.

## Conventions Used Below

For each construct: the YAML form, its meaning, the validation rule it implies,
and the `rule` code recorded in a finding (REF-DESIGN-001 error model). All rules
are version-aware: they are generated per `(schema_id, schema_version)` and a
finding's `schema_reference` records which version was applied.

## Construct Mappings

### type
- **YAML:** `type: <string|integer|boolean|date|list|list[string]|reference>`.
- **Meaning:** the declared data type of a field.
- **Rule:** the instance value must match the declared type. Document types map
  to general types as: `string`->text; `integer`->whole number;
  `boolean`->true/false; `date`->ISO-8601 (YYYY-MM-DD) text; `list`->ordered
  array; `list[string]`->array of text; `reference`->structured object (see
  `reference`).
- **Finding code:** `type` (value is not of the declared type).

### required
- **YAML:** `required: <true|false>`.
- **Meaning:** whether the field must be present.
- **Rule:** if `true`, the field must be present and non-null; if `false`, the
  field is optional and absence is not a finding.
- **Finding code:** `required` (a required field is missing or null).

### description
- **YAML:** `description: <text>`.
- **Meaning:** human documentation of the field.
- **Rule:** none — `description` never constrains instance data. The generator
  may carry it into a finding's `message` for readability, but it produces no
  validation rule.
- **Finding code:** n/a.

### allowed
- **YAML:** `allowed: [<v1>, <v2>, ...]`.
- **Meaning:** the closed set of permitted values (enumeration).
- **Rule:** the instance value must be exactly one of the listed values.
- **Finding code:** `allowed` (value not in the permitted set).

### list
- **YAML:** `type: list` (with an `items:` definition).
- **Meaning:** a repeating collection.
- **Rule:** the value must be an array; each element is validated against the
  `items` element definition (below). An empty array is permitted unless
  `required` applies at the section level.
- **Finding code:** `type` (not an array); element findings carry indexed
  locations (for example `vlans[2]`).

### items
- **YAML:** `items:` (a mapping of field definitions under a `type: list`).
- **Meaning:** the shape of each list element.
- **Rule:** each array element is an object whose fields are validated
  recursively by the same construct rules (`type`, `required`, `allowed`, nested
  `list`/`reference`).
- **Finding code:** per-field codes, with locations indexed by element
  (for example `findings[0].severity`).

### fields
- **YAML:** `fields:` (a mapping of field definitions under a `type: reference`).
- **Meaning:** the shape of a structured reference object.
- **Rule:** the reference value is an object whose keys are validated against the
  `fields` definitions (for example `ref_document` required text, `ref_id`
  text). Unknown keys may be reported as a `warning`.
- **Finding code:** per-field codes (for example `required` on `ref_document`).

### reference
- **YAML:** `type: reference` (with a `fields:` block).
- **Meaning:** a structured external link.
- **Rule:** the value must be an object conforming to its `fields`; combined with
  the structured-external-reference rules below (well-formed `ref_document` /
  `ref_id`). It is never a bare string.
- **Finding code:** `reference_shape` (value is not a conforming reference
  object).

### metadata.schema_version
- **YAML:** `metadata.schema_version` (authoritative version field).
- **Meaning:** the schema version an instance conforms to.
- **Rule:** must be present and text; selects the `RuleSet` version applied to
  the instance. If the declared version has no available schema, validation stops
  with a single error (cannot validate). The header-comment version is ignored;
  only `metadata.schema_version` is authoritative.
- **Finding code:** `schema_version` (missing, non-text, or unknown/unsupported
  version).

### structured external references
- **YAML:** reference values of the form `{ ref_document, ref_id [, ref_version |
  ref_path] }`; internal links are bare local `<section>_id` strings.
- **Meaning:** how links are expressed — external links are structured; internal
  links cite a local id.
- **Rule:**
  - **External:** `ref_document` must be present and, where the schema fixes it
    (for example "SPEC-005"), match that value; `ref_id` must be present text.
  - **Internal:** a bare `<section>_id` link must resolve to an existing id within
    the same instance (reference integrity).
  - **Cross-instance (optional, plugin):** when a resolution context is provided,
    an external reference may be checked to resolve to an existing, conformant
    target instance.
- **Finding codes:** `external_reference_form` (malformed/empty external ref or
  wrong fixed `ref_document`); `reference_integrity` (internal id not found, or
  cross-instance target missing).

## Rule Code Summary

| Construct | Rule code(s) |
|---|---|
| type | `type` |
| required | `required` |
| description | (none) |
| allowed | `allowed` |
| list | `type`, element findings |
| items | per-field codes (indexed) |
| fields | per-field codes |
| reference | `reference_shape` |
| metadata.schema_version | `schema_version` |
| structured external references | `external_reference_form`, `reference_integrity` |

## Out of Scope (this document)

No JSON Schema or other representation is generated here; no code, tooling,
templates, or examples are produced. The first build step (a separate, reviewed
milestone) will implement this mapping for one schema as a pilot before scaling
to all approved schemas, on non-customer sample data only.

# Mist Organization Generation

- Document ID: SPEC-007
- Status: Approved
- Version: 1.0
- Approved By: lead_architect (technical approval), product_owner (implementation authorization), implementation_engineer (implementation readiness)
- Approval Date: 2026-06-30

## Purpose

Define the intent model for preparing a Mist organization from an approved
Design Package (SPEC-005) and an approved Mist Organization Readiness assessment
(SPEC-006). It describes what a Mist organization should be prepared to contain,
expressed as engineering intent — not how to call any API, and not the
configuration itself.

## Scope

Covers organization-generation intent: the Mist objects to be prepared and their
intended relationships, derived from approved upstream artifacts and traceable
to them. It does not generate configuration, define API payloads, implement
workflows or automation, or cover deployment and day-2 operations. The readiness
gate (SPEC-006) precedes this; actual generation is out of scope.

## Required Inputs

- An approved Design Package (SPEC-005).
- An approved Mist Organization Readiness assessment (SPEC-006) whose overall
  determination is "ready".
- The approved Project Profile (SPEC-001) and Customer Discovery (SPEC-002) for
  context.
- The applicable standards (STD-001 and STD-001.1).

## Required Outputs

- A structured statement of organization-generation intent: the intended set of
  Mist objects and their relationships, traceable to the Design Package.
- An explicit mapping from design elements to intended Mist objects.
- Assumptions and open questions carried with the intent.
- No Mist configuration, API payloads, or credentials of any kind.

## Mist Organization Generation Intent

Describes, at intent level only, what the organization should be prepared to
contain. Each item names what should exist and why, traceable to the design,
with no values and no configuration:

- Organization-level intent (the organization to be prepared and its high-level
  structure).
- Site and site-group intent (from the design's site structure).
- Template intent (network, switch, WLAN, and RF templates implied by the plans).
- Policy and segmentation intent (from the security/segmentation plan).
- Inventory and assignment intent (device roles and counts; no claim codes).

## Required Mist Objects

The Mist objects the intent must address, named at the definition level only.
This enumerates the object set the intent covers; it does not configure any
object.

- Organization.
- Sites and site groups.
- Network (switching) templates.
- WLAN / SSID templates.
- RF templates.
- Switch templates / port profiles.
- Network and segmentation policies.
- Inventory / device assignments.

## Design-to-Mist Mapping

The generation intent maps approved Design Package elements to Mist objects at
intent level. Traceability is recorded in the schema via a structured
`design_reference` on each intent item.

| Design Package element | Mist intent |
|---|---|
| Site structure | Mist organization, sites, and site groups |
| `vlan_ip_plan` | Network templates |
| `wlan_ssid_plan` | WLAN and RF templates |
| `switching_plan` | Switch templates and port-profile intent |
| `security_segmentation_plan` | Network and segmentation policy intent |
| Inventory | Inventory assignment readiness |

Relationships are expressed at intent level only: template applicability and
inheritance via `template_intent.scope_level` (org / site_group / site) and
`template_intent.inherits_from`; site hierarchy via `site_intent.parent_site_group`.
No configuration is produced.

## Pre-Implementation Review Rules

- Generation intent is produced only from an approved Design Package and an
  approved "ready" Mist Organization Readiness assessment.
- The intent passes through Engineering Review (SPEC-003) as a pre-implementation
  review before any organization is prepared.
- Implementation — actual generation or automation — must not begin until the
  intent is approved.
- An approved intent changes only through a new revision (per STD-001).

## What Must Not Be Included

- API payloads or API call definitions.
- Generated Mist configuration, automation, or workflow code.
- Organization IDs, API tokens, claim codes, or secrets.
- Customer-specific values or any example data.
- Assumed information; gaps remain explicit rather than defaulted.

## Open Questions

- How is the intent kept in sync if the Design Package or readiness assessment is
  revised?
  - Disposition: Accepted — owner: lead_architect, rationale: synchronization is handled by re-review when an upstream artifact is revised; automation is out of scope, revisit: when a generation/automation step is specified.
- Where is the boundary between this intent specification and a future generation
  or automation step?
  - Disposition: Accepted — owner: product_owner, rationale: the boundary is fixed at intent; the next step requires a separate authorized specification, revisit: when implementation/automation is authorized.

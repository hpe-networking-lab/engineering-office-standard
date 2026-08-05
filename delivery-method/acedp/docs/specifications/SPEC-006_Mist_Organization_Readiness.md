# Mist Organization Readiness

- Document ID: SPEC-006
- Status: Approved
- Version: 1.0
- Approved By: lead_architect (technical approval)
- Approval Date: 2026-06-30

## Purpose

Define the readiness model used to determine whether an approved Design Package
(SPEC-005) contains enough structured information to prepare a Mist organization
before hardware installation. This is an assessment model — it judges
sufficiency of design information; it does not generate configuration.

## Scope

Covers the categories and criteria used to assess organization-preparation
readiness from an approved Design Package. It does not generate Mist
configuration, call any API, define the readiness schema (deferred), or address
post-installation or day-2 operations.

## Required Inputs

- An approved Design Package (SPEC-005), including its
  `mist_organization_readiness` section.
- The approved Project Profile (SPEC-001) and Customer Discovery (SPEC-002) for
  context.
- The applicable standards (STD-001 and STD-001.1).

## Required Outputs

- A readiness assessment stating, per category, whether the design provides
  sufficient structured information.
- An explicit list of gaps and prerequisites blocking organization preparation.
- An overall readiness determination (`ready` / `partial` / `not_ready`) with
  rationale.
- No Mist configuration — the output is an assessment, not a build.

## Readiness Categories

Each category answers "is sufficient structured information present?", not "is it
configured?":

- Organization and site structure (`org_site_structure`).
- Network and addressing readiness (`network_addressing`).
- Wireless readiness (`wireless`).
- Wired and switching readiness (`wired_switching`).
- Security and segmentation readiness (`security_segmentation`).
- Template readiness (`template`).
- Inventory and assignment readiness (`inventory_assignment`).
- Documentation readiness (`documentation`).

### Category Classification

- **Mandatory (always):** `org_site_structure`, `network_addressing`,
  `security_segmentation`, `template`, `inventory_assignment`.
- **Conditional (mandatory only when in scope):** `wireless` when WLAN is in
  scope; `wired_switching` when switching is in scope.
- **Recommended:** `documentation`.

A conditional category, when its condition applies, is treated as mandatory for
that engagement.

## Readiness Threshold

The overall determination is derived as follows:

- **ready** — all mandatory categories are `sufficient`, and no open blocking gap
  exists.
- **partial** — all mandatory categories are `sufficient`, but one or more
  non-blocking gaps remain.
- **not_ready** — one or more mandatory categories are `insufficient` or
  `not_assessed`, or any open blocking gap exists.

Only a `ready` and approved assessment permits Mist organization preparation
(and, downstream, SPEC-007 generation intent).

## Required Mist Constructs

The constructs the design must be capable of populating before installation,
named at the definition level only. Naming a construct states WHAT must be
preparable; it does not specify HOW, and nothing is configured here.

- Organization.
- Sites and site groups.
- Network (switching) templates.
- WLAN / SSID templates.
- RF templates.
- Switch templates / port profiles.
- Network policies and segmentation (expressed as design intent).
- Inventory / device assignment readiness.

## What Must Not Be Included

- Generated Mist configuration, API payloads, or automation.
- Organization IDs, API tokens, credentials, or device claim codes.
- Customer-specific values or any example data.
- Device-specific configuration output.
- Assumed information; gaps remain explicit rather than defaulted.

## Review and Approval Rules

- A readiness assessment is produced only from an approved Design Package.
- The assessment passes through Engineering Review (SPEC-003) before any
  organization preparation proceeds.
- Mist organization preparation must not begin until readiness has been assessed
  and approved.
- An approved assessment changes only through a new revision (per STD-001).

## Open Questions

- How does readiness relate to hardware availability and site-survey status?
  - Disposition: Accepted — owner: lead_architect, rationale: hardware/site-survey linkage is engagement context, not required for the readiness model, revisit: if readiness must incorporate hardware/survey status.
- Should readiness be re-assessed automatically if the Design Package is revised?
  - Disposition: Accepted — owner: lead_architect, rationale: re-assessment is triggered by review on a Design Package revision; automation is out of scope, revisit: if automated re-assessment is introduced.
- What is the relationship between this model and the Design Package's own
  `mist_organization_readiness` section — is this the authoritative assessment
  that section feeds, or a separate gate? (Scheduled for SPEC-005 reconciliation.)
  - Disposition: Resolved — addressed in Milestone 46: the SPEC-006 assessment is authoritative and the Design Package section is preliminary.

# Design Package

- Document ID: SPEC-005
- Status: Approved
- Version: 1.0
- Approved By: lead_architect (technical approval)
- Approval Date: 2026-06-30

## Purpose

Define the canonical Design Package: the engineering design artifact produced
after Customer Discovery (SPEC-002) and Engineering Review (SPEC-003), and
before any Mist organization or configuration generation. The Design Package
translates an approved Project Profile and confirmed discovery into a
reviewable design that downstream generation consumes. It is the bridge between
"what the engagement needs" and "what will be generated."

## Scope

Covers the definition, contents, and approval of a Design Package. It does not
define the Design Package's machine-readable schema (deferred), and it does not
produce designs, examples, templates, or Mist workflows. It is technology-aware
(it organizes network design) but produces design intent, not configuration.

## Required Inputs

- An approved Project Profile (SPEC-001).
- A completed and reviewed Customer Discovery record (SPEC-002).
- An Engineering Review outcome (SPEC-003) authorizing design to proceed.
- The applicable standards (STD-001 and STD-001.1).

## Required Outputs

- A Design Package containing the high-level and low-level design and the
  applicable domain plans, in a reviewable form.
- Explicit assumptions, constraints, and open questions carried with the design.
- A preliminary, design-side indication of Mist organization readiness — without
  generating any Mist configuration, and without authorizing preparation.

## Design Package Contents

The Design Package shall be capable of containing the following, each developed
to high-level and then low-level depth as applicable. Concrete structure is
deferred to a future schema; this section names the content categories only.

- High-level design (HLD).
- Low-level design (LLD).
- VLAN / IP plan.
- WLAN / SSID plan.
- Switching plan.
- Security / segmentation plan.
- Mist organization readiness (preliminary — see below).
- Customer-facing documentation.

Not every engagement requires every category; required versus optional contents
are an open question (below).

### Mist Organization Readiness (Preliminary)

The Mist organization readiness recorded in a Design Package is a **preliminary,
design-side self-assessment**. It may identify expected readiness, anticipated
gaps, and dependencies, but it does **not** authorize Mist organization
preparation. It is superseded by the approved **SPEC-006 Mist Organization
Readiness** assessment, which is the authoritative readiness record. Downstream
Mist Organization Generation (SPEC-007) requires an approved SPEC-006 readiness
record — not the Design Package's preliminary section.

## Review and Approval Rules

- The Design Package passes through Engineering Review (SPEC-003) before it is
  approved.
- Approval is explicit and attributable; an approved package changes only
  through a new revision, never silent edits (per STD-001).
- Mist organization and configuration generation must not begin until the Design
  Package is approved.
- The Design Package's readiness section is preliminary; downstream Mist
  Organization Generation additionally requires an approved SPEC-006 Mist
  Organization Readiness record.

## What Must Not Be Included

- Generated device configuration, deployment artifacts, or automation output
  (per the ADR-0008 boundary).
- Executable code or scripts.
- Secrets, credentials, or other sensitive operational material.
- Invented or assumed customer information; unknowns remain recorded as open
  questions, not filled with defaults.
- Vendor-specific configuration output — the package expresses design intent,
  not configuration.

## Open Questions

- Where is the boundary between HLD and LLD depth within one package?
  - Disposition: Accepted — owner: lead_architect, rationale: HLD/LLD depth is judged per design at review; a fixed boundary is not required, revisit: if depth criteria need standardizing.
- Should each plan (VLAN/IP, WLAN/SSID, switching, security) be a separately
  reviewable sub-artifact, or sections of a single package?
  - Disposition: Accepted — owner: lead_architect, rationale: plans are sections of one package for now; sub-artifact granularity is a future enhancement, revisit: if independent plan review is required.
- Which contents are required versus optional, and does this vary by engagement
  size or type?
  - Disposition: Accepted — owner: lead_architect, rationale: required/optional contents are determined per engagement at review, revisit: if a content matrix by engagement type is needed.
- What is the relationship to the POC Deliverable (SPEC-004) — does design
  follow an accepted POC, precede it, or are both paths valid?
  - Disposition: Accepted — owner: product_owner, rationale: ordering is an engagement-level decision; both paths are permitted, revisit: when a production-delivery specification is authorized.

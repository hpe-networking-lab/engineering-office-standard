# Role Model

> **Status:** Approved
> **Version:** 1.0
> **Approved By:** lead_architect (technical approval), product_owner (final acceptance)
> **Approval Date:** 2026-06-30

## Purpose

Define the canonical roles in an ACEM project and the responsibilities each role
owns. These role identifiers are authoritative and are referenced by downstream
applications of the methodology (for example, an application's approval-authority
matrix) so that approval and accountability are consistent and attributable.

## Canonical Roles

### product_owner

The Product Owner / Principal Engineer. Owns:

- Vision, requirements, and customer objectives.
- Business and customer acceptance of deliverables.
- Authorization to begin implementation.
- Final approval.

### lead_architect

The Lead Architect. Owns:

- Architecture and engineering standards.
- Technical review, quality control, and risk analysis.
- The primary technical approval (or rejection) of engineering artifacts.

### implementation_engineer

The Implementation Engineer. Owns:

- Producing approved deliverables within approved scope.
- Following engineering standards and reporting blockers.
- Confirming implementation readiness only; holds no approval authority over
  engineering content, and never invents facts.

## Approval and Accountability

Approval is always explicit and attributable to one of the canonical roles
above. Where an artifact requires both technical approval and business or
implementation authorization, those are distinct decisions held by different
roles, and each required decision is recorded. The role-to-artifact authority
mapping is defined by each application of the methodology.

## Open Questions

- Whether additional roles (for example, a reviewer distinct from the
  lead_architect) are needed for larger engagements.
  - Disposition: Accepted — owner: product_owner, rationale: the three canonical roles are sufficient for current scope, revisit: when an engagement requires role separation.

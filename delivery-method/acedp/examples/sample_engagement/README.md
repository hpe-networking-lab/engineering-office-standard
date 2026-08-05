# Sample Engagement — End-to-End ACEDP Walkthrough

A worked, **fictional, non-customer** engagement that exercises the approved
ACEDP pipeline from Project Profile through Mist Organization Generation Intent.
It exists to demonstrate the workflow and the Phase 0 validation tooling. It
contains no real customer data, no configuration, no API payloads, and no Mist
interaction.

## Pipeline and Artifacts

```
project_profile.yaml            (SPEC-001)  PP-NW-1  the anchor
        ↓ enriched by
customer_discovery.yaml         (SPEC-002)  CD-NW-1  -> references PP-NW-1
        ↓ validated by
engineering_review.yaml         (SPEC-003)  ER-NW-1  -> reviews DP-NW-1
        ↓ authorises
design_package.yaml             (SPEC-005)  DP-NW-1  -> references PP/CD/ER
        ↓ assessed by
mist_organization_readiness.yaml(SPEC-006)  MR-NW-1  -> references DP-NW-1 (ready)
        ↓ when ready
mist_organization_generation.yaml(SPEC-007) MG-NW-1  -> references DP-NW-1, MR-NW-1
```

## Cross-Document and Internal References

- **Cross-document** (structured `ref_document` + `ref_id`, resolvable within this
  set): CD→PP, DP→PP/CD/ER, MR→DP, MG→DP/MR, and each approval's
  `review_reference` → ER-NW-1; the Engineering Review's
  `artifacts_reviewed.artifact_reference` → DP-NW-1.
- **Internal** (bare-id links within one instance): PP
  `success_criteria.linked_objective` → `OBJ-1`; CD `findings.source_reference` →
  `SRC-1`; ER `findings.related_criterion/related_artifact` → `RC-1`/`AR-1`;
  DP `ip_subnets.vlan_ref` → `VL-1`; MR `required_mist_constructs.category_ref` →
  `CAT-1`; MG `wlan_intent.template_ref` → `T-1`, `inventory_intent.site_ref` →
  `S-1`.

Every artifact traces back through references to the originating Customer
Discovery and the Project Profile.

## Validate

From the repository root:

```
# validate one artifact against its rule set
python3 acedp/tools/validation/validator.py \
    acedp/examples/sample_engagement/design_package.yaml \
    acedp/tools/validation/Design_Package.rules.json

# validate with cross-document resolution across this engagement set
python3 acedp/tools/validation/validator.py \
    acedp/examples/sample_engagement/design_package.yaml \
    acedp/tools/validation/Design_Package.rules.json \
    --context acedp/examples/sample_engagement
```

All six artifacts are conformant both single-file and with `--context` over this
directory (exit code 0).

## Boundaries

Fictional/sample data only. No approved artifact is modified, no Mist system is
contacted, and nothing here is executable or a real configuration.

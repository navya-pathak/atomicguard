# Results Snapshot

This page reports high-level results from the broader project manuscript while distinguishing them from the scope of this public demo.

## Reported Full-Project Metrics

- Overall AUROC: 0.7533
- 95% CI: 0.7362-0.7704
- Per-disease Stage 1 AUROC:
  - GBS: 0.8224
  - Arthritis: 0.7821
  - Polymyositis: 0.7271
  - SLE: 0.6818

The full project also reports adjudication-stage sensitivity improvements for rare outcomes relative to model-only predictions.

## Baseline vs Hybrid Comparison

| System Variant | Overall AUROC (reported) | Average Sensitivity Across 4 Target Diseases | Notes |
|---|---:|---:|---|
| Stage 1 model-only | 0.7533 | 17.3% | Good discrimination, weak rare-disease sensitivity before adjudication |
| Stage 2 rule-only | N/A in public benchmark table | N/A | Rule layer is designed as adjudication support |
| Hybrid (model plus adjudication) | 0.7533 (Stage 1 discrimination anchor) | 76.9% | Sensitivity substantially improved in reported full-project evaluation |

## Disease-Level Sensitivity Shift (Reported)

| Disease | Model-Only Sensitivity | Hybrid Sensitivity |
|---|---:|---:|
| GBS | 65.0% | 85.0% |
| Arthritis | 0.9% | 79.0% |
| Polymyositis | 3.4% | 73.2% |
| SLE | 0.0% | 70.4% |

## Interpretation

These values are included to communicate research direction and observed behavior in the full system.

## Scope Boundaries

This public repository is a sanitized, reproducible demonstration focused on:
- architecture and decision-layer design,
- interpretability and traceability,
- and research rigor framing.

It does not include raw restricted data, full training artifacts, or private checkpoints needed to reproduce all manuscript-scale benchmarks end to end.

## Recommendation For Reviewers

Use this repository to assess method design quality, adjudication logic, and evaluation planning. Treat full-project metrics as contextual evidence from the broader research pipeline.

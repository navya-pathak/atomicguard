# Full System Scope (Public vs Private)

This document clarifies what is included in this public repository and what remains private.

## Publicly Included

- Clinical post-inference adjudication engine for multiclass adverse event prediction
- Runnable demonstration pipeline with sanitized sample input
- Architecture and data-flow documentation for technical review
- Research framing, ablation plan, and limitations documentation

## Privately Retained

- Large model checkpoints and heavyweight experiment artifacts
- Raw or restricted datasets and sensitive biomedical records
- Infrastructure-specific deployment and cloud integration details
- Internal iteration history, exploratory scripts, and non-public assets

## Why This Split Exists

- Protects sensitive/restricted data
- Preserves reproducibility for core methodological ideas
- Enables research assessment without exposing governed assets

## How To Interpret This Repository

This repository is intended to show methodological quality and research maturity:
- explicit biological reasoning,
- reproducible inference flow,
- transparent limitations,
- and a concrete plan for rigorous follow-up experiments.

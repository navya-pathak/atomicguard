# Assessment Brief (For ML Research Labs)

## One-Sentence Summary

A reproducible computational biology demo that combines multiclass model outputs with explicit biomarker-driven adjudication rules to improve interpretability in vaccine adverse event risk assessment.

## Evaluation Lens

- Reproducibility: single-command runnable demo
- Interpretability: transparent rule contributions to final decisions
- Extensibility: modular code structure for ablation and calibration studies

## Suggested Review Path

1. Read README method and research snapshot sections.
2. Run `python src/demo_clinical_rules.py`.
3. Inspect rule logic in `src/clinical_validation_postprocessing.py`.
4. Review architecture notes in `docs/model_prediction_flow.md`.
5. Review `docs/RIGOR_AND_ABLATION_PLAN.md` for evaluation design.
6. Review `docs/FAILURE_MODES_AND_LIMITATIONS.md` for limitations and failure taxonomy.
7. Review `docs/FULL_SYSTEM_SCOPE.md` for public versus private asset boundaries.

## Candidate Follow-Up Work

- Add confidence calibration metrics (ECE/Brier score)
- Evaluate hybrid decision policy under distribution shift
- Compare adjudication performance across disease-specific cohorts
- Add formal disagreement analysis between model and rule layers
- Add uncertainty flags for sparse biomarker contexts

## Scope Note

This repository is a sanitized public demonstration and does not include private datasets, restricted assets, or clinical deployment credentials.

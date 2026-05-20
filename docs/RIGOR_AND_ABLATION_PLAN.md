# Rigor and Ablation Plan

This plan describes how to evaluate the hybrid decision pipeline (model output plus clinical adjudication) under ML research criteria.

## Core Hypothesis

Post-inference clinical adjudication improves reliability and interpretability relative to model-only predictions, particularly in ambiguous confidence regimes.

## Evaluation Matrix

1. Model-only baseline
- Input: model logits
- Output: argmax class and confidence
- Purpose: establish unconstrained baseline behavior

2. Rule-only baseline
- Input: biomarker feature vector
- Output: disease confidence from rules only
- Purpose: isolate value of explicit domain constraints

3. Hybrid system (current design)
- Input: model logits plus biomarker context
- Output: adjudicated class, confidence, and rationale
- Purpose: test whether fusion improves practical decision quality

## Metric Families

- Discrimination: AUROC, macro-F1, per-class recall and precision
- Calibration: ECE, Brier score, confidence reliability curves
- Robustness: subgroup and temporal stability deltas
- Interpretability utility: proportion of decisions with coherent rationale templates

## Stress Tests

- Distribution shift stress test across temporally held-out cohorts
- Missingness stress test for partial biomarker panels
- Contradictory-signal stress test (model high confidence vs rule disagreement)

## Error Analysis Protocol

- Identify top false positives and false negatives per class
- Categorize by signal source: model miss, rule miss, or fusion policy miss
- Propose targeted remediation per failure class (threshold adjustment, rule revision, calibration)

## Success Criteria (Research Stage)

- Hybrid system improves at least one of calibration or minority-class recall without severe precision collapse
- Failure categories are identifiable and actionable
- Findings remain consistent across at least one held-out split and one subgroup slice

## Deliverables

- Reproducible experiment scripts
- Metric table for baseline vs hybrid comparisons
- Calibration and reliability plots
- Error taxonomy summary with representative case narratives

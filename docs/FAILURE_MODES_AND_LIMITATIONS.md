# Failure Modes and Limitations

This document summarizes known limitations and expected failure patterns in the public demonstration.

## Known Limitations

- Simulated logits are used in the demo script, so benchmark-level performance claims are out of scope for this public package.
- Public assets are intentionally reduced for privacy and governance constraints.
- Feature coverage in the demo reflects selected structured biomarkers and is not a complete clinical context model.

## Expected Failure Modes

1. Ambiguous confidence region
- Pattern: model probabilities are diffuse across classes.
- Risk: unstable final prediction if rule support is weak.

2. Sparse biomarker context
- Pattern: many missing or default-like biomarker values.
- Risk: reduced strength of rule-based adjudication.

3. Model-rule disagreement
- Pattern: model and rule layers strongly disagree.
- Risk: confidence arbitration can become threshold-sensitive.

4. Distribution shift
- Pattern: cohort characteristics differ from design assumptions.
- Risk: miscalibrated confidence and degraded class balance.

## Mitigation Strategy

- Add explicit missingness handling and uncertainty flags.
- Use calibration-aware thresholds rather than fixed confidence cutoffs.
- Track disagreement rates between model and rule layers as a monitoring signal.
- Re-validate under temporal and subgroup splits before extending deployment scope.

## Research Posture

This repository is positioned as a methodological demonstration. It is suitable for discussing model design, adjudication strategy, and evaluation rigor, not for asserting clinical utility in the absence of prospective validation.

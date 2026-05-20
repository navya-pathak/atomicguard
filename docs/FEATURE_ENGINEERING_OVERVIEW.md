# Feature Engineering Overview

This document summarizes the feature engineering design used in the broader AtomicGuard project and how it is represented in this public demonstration.

## Core Representation

The full project uses a unified 346-dimensional structured representation with modality blocks for:
- biomarkers,
- demographics,
- HLA context,
- sequence-derived context,
- and structural features.

This supports a single inference interface while preserving interpretable feature groups for downstream adjudication.

## Design Principles

- Biological relevance first: feature blocks mirror domain mechanisms (immune markers, HLA, sequence/structure context).
- Robustness under sparsity: missing biomarkers are handled explicitly, and rule activation is conditional on informative values.
- Auditability: feature groups are separable for ablation and error attribution.

## Public Demo Mapping

In this public repository:
- structured biomarker mapping is visible in `src/demo_clinical_rules.py`,
- adjudication logic is visible in `src/clinical_validation_postprocessing.py`,
- and a sanitized input example is provided in `data/examples/sample_patient_input.json`.

## Why This Matters For ML Review

This feature design makes it possible to evaluate not only predictive output quality but also where signal originates, how uncertainty propagates, and how domain constraints shape final decisions.

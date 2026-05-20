# Reproducibility Notes

This document defines the minimal steps to reproduce the public demonstration behavior.

## Environment

- Python 3.12 or compatible
- OS tested: Linux
- Hardware: CPU is sufficient

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run Demo

```bash
python src/demo_clinical_rules.py
```

## Expected Behavior

The script should print:
- case identifier,
- model-layer prediction and confidence,
- final adjudicated decision and confidence,
- decision method,
- explanation text from clinical adjudication.

## Determinism and Scope

- The demo is deterministic for included sample input and fixed simulated logits.
- Manuscript-scale benchmark reproduction is out of scope for this public package due to restricted assets and omitted large artifacts.

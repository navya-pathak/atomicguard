# System Architecture Overview

The canonical overall architecture artifact for this public repository is:

- `docs/TWO_STAGE_ENGINE_ARCHITECTURE_ASCII.txt`

That diagram captures the primary AtomicGuard design used in this showcase:

- Stage 1: Option C dual-head attention transformer
- Stage 2: clinical calibration and rule-based adjudication
- Final confidence and action mapping (ALERT, MONITOR, REASSURE)

## How To Read The Architecture

1. Start from the 346D feature encoding block.
2. Follow Stage 1 neural inference (dual pathways and fusion logits).
3. Follow Stage 2 calibration (distance adjustment, boost, validation rules, integration).
4. Inspect final decision method and deployment action thresholds.

## Scope Note

This public repository is a curated research demonstration.
The two-stage architecture is the primary method-level system view for assessment. Broader production infrastructure details from the private/full project are intentionally out of scope here.

## Mapping to Public Artifacts

- Architecture artifact: `docs/TWO_STAGE_ENGINE_ARCHITECTURE_ASCII.txt`
- Prediction flow companion: `docs/model_prediction_flow.md`
- Adjudication implementation: `src/clinical_validation_postprocessing.py`
- Demo execution path: `src/demo_clinical_rules.py`
- Scope boundaries: `docs/FULL_SYSTEM_SCOPE.md`

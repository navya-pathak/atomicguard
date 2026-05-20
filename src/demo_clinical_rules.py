#!/usr/bin/env python3
"""Public portfolio demo for clinical rule-based post-processing."""

from pathlib import Path
import json
import numpy as np
import torch

from clinical_validation_postprocessing import ClinicalValidationEngine


FEATURE_INDEX = {
    "jo1": 0,
    "ck": 1,
    "myoglobin": 2,
    "creatinine": 3,
    "esr": 4,
    "crp": 5,
    "ldh": 6,
    "aldolase": 7,
    "platelet": 8,
    "anti_dsdna": 9,
    "ana": 10,
    "anti_smith": 11,
    "anti_ro_ssa": 12,
    "anti_la_ssb": 13,
    "anti_ccp": 14,
    "rf": 15,
    "complement_c3": 16,
    "complement_c4": 17,
    "proteinuria": 18,
    "hemoglobin": 19,
    "wbc": 20,
    "lymphocyte_pct": 21,
    "immunoglobulin_g": 22,
}


def build_feature_vector(patient: dict) -> np.ndarray:
    """Map sample biomarkers into a 346D feature vector expected by the engine."""
    features = np.zeros(346, dtype=np.float32)
    biomarkers = patient.get("biomarkers", {})

    for biomarker, idx in FEATURE_INDEX.items():
        value = biomarkers.get(biomarker, 0.0)
        try:
            features[idx] = float(value)
        except (TypeError, ValueError):
            features[idx] = 0.0

    return features


def run_demo() -> None:
    root = Path(__file__).resolve().parents[1]
    sample_path = root / "data" / "examples" / "sample_patient_input.json"

    with sample_path.open("r", encoding="utf-8") as handle:
        patient = json.load(handle)

    features = build_feature_vector(patient)

    # Simulated model logits for 7 classes:
    # [Myositis, GBS, Lupus, RA, Vasculitis, Pericarditis, Control]
    logits = torch.tensor([0.35, 0.22, 0.18, 0.10, 0.05, 0.03, 0.07], dtype=torch.float32)

    engine = ClinicalValidationEngine()
    report = engine.process_predictions(logits, features, case_id=patient.get("patient_id", "DEMO_CASE"))

    print("=" * 72)
    print("ATOMICGUARD PUBLIC DEMO")
    print("=" * 72)
    print(f"Case ID:            {report['case_id']}")
    print(f"Model prediction:   {report['model_layer']['prediction']}")
    print(f"Model confidence:   {report['model_layer']['confidence']:.1%}")
    print(f"Final decision:     {report['final_decision']['disease']}")
    print(f"Final confidence:   {report['final_decision']['confidence']:.1%}")
    print(f"Decision method:    {report['final_decision']['decision_method']}")
    print("-" * 72)
    print("Clinical explanation:")
    print(report['final_decision']['explanation'])
    print("=" * 72)


if __name__ == "__main__":
    run_demo()

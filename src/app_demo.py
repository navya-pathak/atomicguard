#!/usr/bin/env python3
"""
AtomicGuard Flask API Demo (Public Showcase)
============================================

This file shows the structure and design of the AtomicGuard web API.
It is a stripped public version that illustrates endpoint design,
request validation, and response format.

The full production implementation (with real model pipeline, visualizations,
and extended biomarker handling) is available on request for academic review.
"""

from flask import Flask, request, jsonify
import json
from pathlib import Path

from clinical_validation_postprocessing import ClinicalValidationEngine
from demo_clinical_rules import build_feature_vector

import numpy as np
import torch

app = Flask(__name__)

engine = ClinicalValidationEngine()

REQUIRED_FIELDS = ["age", "sex", "ethnicity"]

SIMULATED_LOGITS = torch.tensor(
    [0.35, 0.22, 0.18, 0.10, 0.05, 0.03, 0.07], dtype=torch.float32
)


def validate_patient(data: dict) -> list[str]:
    """Return list of missing required field names."""
    return [f for f in REQUIRED_FIELDS if not data.get(f)]


@app.route("/", methods=["GET"])
def index():
    """Health-check and capability summary."""
    return jsonify(
        {
            "service": "AtomicGuard Demo API",
            "version": "public-showcase",
            "endpoints": {
                "POST /api/assess": "Assess a single patient",
                "GET  /api/health": "Service health check",
            },
            "note": (
                "Full production API with real model, visualizations, and "
                "batch endpoints is available on request for academic review."
            ),
        }
    )


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "clinical_engine": "loaded"})


@app.route("/api/assess", methods=["POST"])
def assess():
    """
    Assess a single patient from JSON payload.

    Expected body fields:
        age       (int)    required
        sex       (str)    required  e.g. "M" or "F"
        ethnicity (str)    required
        biomarkers (dict)  optional  e.g. {"jo1": 0.10, "ck": 0.15, ...}

    Returns:
        JSON with model-layer prediction, final decision, confidence, and explanation.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No JSON payload provided"}), 400

    missing = validate_patient(data)
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    patient_id = data.get("patient_id", "ANON")

    # Build feature vector from biomarkers
    features = build_feature_vector(data)

    # In this public demo, logits are simulated.
    # In production, the real Option C transformer runs here.
    logits = SIMULATED_LOGITS

    report = engine.process_predictions(logits, features, case_id=patient_id)

    return jsonify(
        {
            "case_id": report["case_id"],
            "model_prediction": report["model_layer"]["prediction"],
            "model_confidence": round(report["model_layer"]["confidence"], 4),
            "final_decision": report["final_decision"]["disease"],
            "final_confidence": round(report["final_decision"]["confidence"], 4),
            "decision_method": report["final_decision"]["decision_method"],
            "explanation": report["final_decision"]["explanation"],
        }
    )


if __name__ == "__main__":
    print("AtomicGuard Demo API")
    print("Endpoints: GET / | GET /api/health | POST /api/assess")
    print()
    app.run(host="0.0.0.0", port=5000, debug=False)

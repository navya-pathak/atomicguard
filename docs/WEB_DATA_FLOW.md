# AtomicGuard Web Application - Data Flow Diagram

## User Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│ USER OPENS BROWSER                                              │
│ http://localhost:5000                                           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ WEB FORM LOADS (index.html)                                     │
│ ┌──────────────────────────────────────────────────────────────┐│
│ │ Patient Demographics     │  Quick Templates                   ││
│ │ • Age                    │  [Low Risk] [Active Myositis]      ││
│ │ • Sex                    │  [Treated]  [Elderly]              ││
│ │ • Ethnicity              │                                    ││
│ │ • Comorbidities          │  Assessment Form                   ││
│ │                          │  • Biomarkers (0-1 scale)         ││
│ │ Biomarkers              │  • Jo-1, CK, Myoglobin            ││
│ │ • Jo-1, CK              │  • ESR, CRP, LDH                   ││
│ │ • ESR, CRP              │  • Platelets, C3, C4               ││
│ │ • LDH, Aldolase         │                                    ││
│ │ • Optional: C3, C4      │  [Assess Patient] [Clear Form]     ││
│ │ • HLA Allele (optional) │                                    ││
│ └──────────────────────────────────────────────────────────────┘│
└────────────────────────┬────────────────────────────────────────┘
                         │ USER ENTERS DATA
                         │ (or clicks template)
                         │ CLICKS "Assess Patient"
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ HTTP POST REQUEST                                               │
│ Endpoint: /api/assess                                           │
│ Content-Type: application/json                                  │
│                                                                 │
│ {                                                               │
│   "age": 31,                                                    │
│   "sex": "M",                                                   │
│   "ethnicity": "South Asian",                                   │
│   "comorbidities": 1,                                           │
│   "jo1": 0.65,                                                  │
│   "ck": 0.32,                                                   │
│   "esr": 0.28,                                                  │
│   "crp": 0.22,                                                  │
│   ... (other biomarkers)                                        │
│ }                                                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ FLASK SERVER (app.py)                                           │
│ Route: @app.route('/api/assess', methods=['POST'])              │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ 1. Parse JSON request                                       ││
│ │ 2. Validate required fields                                 ││
│ │ 3. Convert numeric strings to floats                        ││
│ └─────────────────────────────────────────────────────────────┘│
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ FEATURE ENCODING (pre_vaccination_assessment.py)                │
│ PatientFeatureEncoder.encode_patient()                          │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ Input: Clinical data dict                                   ││
│ │                                                             ││
│ │ Processing:                                                 ││
│ │ • Normalize biomarkers to 0-1 scale                         ││
│ │ • Encode demographics (age, sex, ethnicity)                 ││
│ │ • Encode HLA alleles (risk factor = 0.8 for myositis)      ││
│ │ • Count comorbidities                                       ││
│ │ • Generate PROSE embeddings (simulated)                     ││
│ │ • Include AF3 structural features                           ││
│ │                                                             ││
│ │ Output: 346-dimensional numpy array                         ││
│ │ [biomarkers | demographics | HLA | PROSE | AF3]            ││
│ └─────────────────────────────────────────────────────────────┘│
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ MODEL INFERENCE (Option C Dual-Head Attention Transformer)      │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ Architecture: 256D hidden, 8 attention heads, 1,647,367     ││
│ │               parameters; two output heads (disease clf +   ││
│ │               severity regression)                          ││
│ │                                                             ││
│ │ 1. Project 346D feature vector → 256D embedding             ││
│ │ 2. Apply multi-head self-attention over feature groups      ││
│ │ 3. Classification head → logits for 7 disease classes       ││
│ │ 4. Softmax → per-disease probabilities                      ││
│ │                                                             ││
│ │ Output:                                                      ││
│ │ • Predicted disease (e.g., "GBS")                          ││
│ │ • Model confidence (e.g., 0.503)                           ││
│ │ • Probability for each of 7 diseases                       ││
│ └─────────────────────────────────────────────────────────────┘│
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ CLINICAL VALIDATION (clinical_validation_postprocessing.py)     │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ 1. Apply disease-specific biomarker rules                   ││
│ │    • Myositis: Jo-1 score + CK score + ESR score            ││
│ │    • GBS: Creatinine + weakness markers                     ││
│ │    • Lupus: ANA + complement levels                         ││
│ │    • Arthritis: Inflammatory markers                        ││
│ │                                                             ││
│ │ 2. Generate clinical scores (0-1 for each disease)          ││
│ │    • Myositis: 0.88 (strong signal from Jo-1)              ││
│ │    • GBS: 0.17 (weak signal)                               ││
│ │    • Lupus: 0.15                                            ││
│ │    • Arthritis: 0.22                                        ││
│ │                                                             ││
│ │ 3. Compare clinical vs model predictions                   ││
│ └─────────────────────────────────────────────────────────────┘│
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ DECISION LOGIC (Biomarker Dominance Check)                      │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ FIXED LOGIC (Feb 2026):                                     ││
│ │                                                             ││
│ │ IF clinical_confidence - model_confidence > 0.30            ││
│ │    AND clinical_confidence > 0.60:                          ││
│ │    THEN use clinical prediction                             ││
│ │    decision_method = "CLINICAL_BIOMARKER_DOMINANT"          ││
│ │                                                             ││
│ │ EXAMPLE:                                                    ││
│ │ Model predicts: GBS 50.3%                                  ││
│ │ Clinical shows: Myositis 88.0%                             ││
│ │ Difference: 0.88 - 0.503 = 0.377 > 0.30 ✓                 ││
│ │ Clinical confidence 0.88 > 0.60 ✓                          ││
│ │ → USE CLINICAL: Myositis 79.2%                             ││
│ │                                                             ││
│ │ This catches cases model misses!                           ││
│ └─────────────────────────────────────────────────────────────┘│
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ GENERATE CLINICAL DECISION                                      │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ disease: "Myositis"                                         ││
│ │ confidence: 0.792                                           ││
│ │                                                             ││
│ │ decision_method: "CLINICAL_BIOMARKER_DOMINANT"              ││
│ │                                                             ││
│ │ IF decision_method ALERT:                                   ││
│ │    decision = "ALERT"                                       ││
│ │    action = "HIGH RISK - Defer vaccination"                 ││
│ │                                                             ││
│ │ IF decision REASSURE:                                       ││
│ │    action = "LOW RISK - Safe to vaccinate"                  ││
│ │                                                             ││
│ │ IF decision MONITOR:                                        ││
│ │    action = "CONDITIONAL - Vaccinate with monitoring"       ││
│ └─────────────────────────────────────────────────────────────┘│
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ FORMAT OUTPUT                                                   │
│ ┌─────────────────────────────────────────────────────────────┐│
│ │ 1. Create JSON assessment object                            ││
│ │ 2. Generate human-readable text report                      ││
│ │ 3. Include all clinical scores                              ││
│ │ 4. Add recommendations                                      ││
│ │ 5. Timestamp assessment                                     ││
│ └─────────────────────────────────────────────────────────────┘│
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ HTTP RESPONSE (JSON)                                            │
│                                                                 │
│ {                                                               │
│   "success": true,                                              │
│   "patient_id": "PT-2026-001",                                  │
│   "assessment": {                                               │
│     "final_decision": {                                         │
│       "disease": "Myositis",                                    │
│       "confidence": 0.792,                                      │
│       "decision": "ALERT",                                      │
│       "action": "HIGH RISK - Defer vaccination",                │
│       "decision_method": "CLINICAL_BIOMARKER_DOMINANT"          │
│     },                                                          │
│     "clinical_validation": {                                    │
│       "scores": {                                               │
│         "Myositis": 0.88,                                       │
│         "GBS": 0.17,                                            │
│         "Lupus": 0.15,                                          │
│         "Arthritis": 0.22                                       │
│       }                                                         │
│     }                                                           │
│   },                                                            │
│   "report": "... detailed clinical text report ..."             │
│ }                                                               │
│                                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ BROWSER DISPLAYS RESULTS                                        │
│ ┌──────────────────────────────────────────────────────────────┐│
│ │ Assessment Results                                           ││
│ │ ═══════════════════════════════════════════════════════════ ││
│ │                                                             ││
│ │ ┌─────────────────────────────────────────────────────────┐ ││
│ │ │ Primary Risk:  Myositis                                 │ ││
│ │ │ Risk: 79.2%                                            │ ││
│ │ │ [ALERT] ← COLOR-CODED DECISION                         │ ││
│ │ └─────────────────────────────────────────────────────────┘ ││
│ │                                                             ││
│ │ Clinical Action:                                           ││
│ │ HIGH RISK - Defer vaccination. Refer to specialist.        ││
│ │                                                             ││
│ │ Validation Scores:                                         ││
│ │ • Myositis: 88.0% ✓ Strong                                ││
│ │ • GBS: 17.0% ✗ Weak                                       ││
│ │ • Lupus: 15.0% ✗ Weak                                     ││
│ │ • Arthritis: 22.0% ✗ Weak                                ││
│ │                                                             ││
│ │ Clinician Note:                                            ││
│ │ This patient shows clear evidence of myositis based on    ││
│ │ elevated Jo-1 antibodies and myositis-associated markers. ││
│ │ Vaccination should be deferred pending specialist review. ││
│ │                                                             ││
│ │ [Detailed Report]                                          ││
│ │ ─────────────────────────────────────────────────────────  ││
│ │ ATOMIC GUARD PRE-VACCINATION ASSESSMENT REPORT            ││
│ │ Patient ID: PT-2026-001                                   ││
│ │ Timestamp: 2026-01-31T10:30:45                           ││
│ │ ...                                                        ││
│ └──────────────────────────────────────────────────────────┘│
└────────────────────────────────────────────────────────────────┘
```

---

## API Endpoints Flow

```
BROWSER                          FLASK SERVER                PIPELINE
  │                                 │                           │
  ├─ GET /                          │                           │
  │  (page load)                    │                           │
  │◄──── index.html ────────────────┤                           │
  │                                 │                           │
  ├─ GET /api/health                │                           │
  │  (check server)                 │                           │
  │◄─── {"status": "ok"} ───────────┤                           │
  │                                 │                           │
  ├─ GET /api/templates             │                           │
  │  (load quick fill)              │                           │
  │◄─── {4 templates} ──────────────┤                           │
  │                                 │                           │
  ├─ GET /api/reference             │                           │
  │  (biomarker info)               │                           │
  │◄─── {reference data} ───────────┤                           │
  │                                 │                           │
  ├─ POST /api/assess               │                           │
  │  (submit form)                  │                           │
  │  {patient data}──────────────────├─ Encode features ────────┤
  │                                 │◄─ 346D vector ───────────┤
  │                                 │─ Run inference ──────────┤
  │                                 │◄─ Model prediction ──────┤
  │                                 │─ Validate clinically ────┤
  │                                 │◄─ Validation scores ─────┤
  │                                 │─ Decision logic ─────────┤
  │                                 │◄─ Final decision ────────┤
  │◄─── {assessment} ───────────────┤                           │
  │                                 │                           │
  ├─ POST /api/batch                │                           │
  │  (submit multiple)              │                           │
  │  {[patients]}─────────────────────├─ Loop through ─────────┤
  │                                 │  each patient           │
  │◄─── {[assessments]} ───────────┤                           │
```

---

## Batch Processing Flow

```
Input: 100 patients in JSON array
           │
           ▼
┌─────────────────────────┐
│ Flask receives batch    │
│ POST /api/batch         │
└────────────┬────────────┘
             │
             ▼
    ┌────────────────┐
    │ For each patient:
    │   1. Validate data
    │   2. Encode features
    │   3. Run inference
    │   4. Validate clinically
    │   5. Generate decision
    │   6. Store result
    └────────────┬───────┘
                 │
    ┌────────────▼────────────┐
    │ Aggregated Results      │
    │ • Total: 100            │
    │ • Processed: 100        │
    │ • Failed: 0             │
    │ • [individual results]  │
    └────────────┬────────────┘
                 │
                 ▼
    Response JSON with:
    • Summary statistics
    • Individual assessments
    • Error details if any
```

---

## Decision Tree

```
Patient Data
     │
     ▼
┌──────────────────────┐
│ Model Inference      │
│ (Euclidean Distance) │
└────────┬─────────────┘
         │
         ▼
    ┌─────────────────────────┐
    │ Clinical Validation     │
    │ (Biomarker Rules)       │
    └────────┬────────────────┘
             │
             ▼
    ┌────────────────────────────────────┐
    │ Compare Clinical vs Model          │
    └────────┬───────────────────────────┘
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
Clinical >> Model  Model >= Clinical
(diff > 0.30)      (diff <= 0.30)
      │             │
      ▼             ▼
┌────────────┐  ┌────────────────┐
│  USE       │  │ Decision based │
│ CLINICAL   │  │ on consensus   │
│ PREDICTION │  │                │
└────┬───────┘  └────────┬───────┘
     │                   │
     ▼                   ▼
CLINICAL_BIOMARKER    CONSENSUS
_DOMINANT             (strong/moderate/mild)
     │                   │
     └───────┬───────────┘
             │
             ▼
     ┌──────────────┐
     │ Final Disease│
     │ + Confidence │
     └──────┬───────┘
            │
            ▼
   ┌─────────────────────────┐
   │ Determine Decision:     │
   │ - ALERT (high risk)     │
   │ - MONITOR (conditional) │
   │ - REASSURE (low risk)   │
   └──────┬──────────────────┘
          │
          ▼
   Clinical Action
   & Report
```

---

## Real Example: High Jo-1 Patient

```
USER INPUTS:
- Age: 31, Sex: M, Ethnicity: South Asian
- Jo-1: 0.65 (HIGH), CK: 0.32, ESR: 0.28, CRP: 0.22

        │
        ▼
FEATURE ENCODING (346D):
- Biomarkers [0-22]: jo1=0.65, ck=0.32, esr=0.28, crp=0.22, ...
- Demographics [23-29]: age norm, sex, ethnicity, ...
- HLA [30-48]: DRB1*03:01 = 0.8 (myositis risk)
- PROSE [49-255]: clinical embeddings
- AF3 [306-345]: structural features

        │
        ▼
MODEL INFERENCE:
Distance to centroids:
- GBS centroid: dist=2.1 → confidence 50.3%
- Myositis centroid: dist=2.1 → confidence 50.1%
Model predicts: GBS (50.3%) [INDECISIVE!]

        │
        ▼
CLINICAL VALIDATION:
Myositis rules:
- Jo-1 = 0.65 → myositis_score += 0.6
- CK = 0.32 → myositis_score += 0.2
- ESR = 0.28 → myositis_score += 0.08
Total: 0.88 (STRONG)

GBS rules:
- Creatinine = 0.05 → gbs_score += 0.1
- No weakness markers → gbs_score += 0.07
Total: 0.17 (WEAK)

        │
        ▼
DECISION LOGIC:
Clinical diff = 0.88 - 0.503 = 0.377
Is diff > 0.30? YES ✓
Is clinical_confidence > 0.60? YES (0.88) ✓

DECISION: USE CLINICAL PREDICTION

        │
        ▼
FINAL OUTPUT:
Disease: Myositis
Confidence: 79.2%
Decision: ALERT ⚠️
Action: "HIGH RISK - Defer vaccination"
Decision Method: "CLINICAL_BIOMARKER_DOMINANT"

        │
        ▼
DISPLAY TO USER:
┌─────────────────────────────────────────┐
│ Primary Risk: Myositis                  │
│ Risk Confidence: 79.2%                  │
│ [ALERT]                                 │
│ Action: HIGH RISK - Defer vaccination   │
└─────────────────────────────────────────┘
```

---

## Summary

The web application:
1. ✅ Accepts patient data via HTML form
2. ✅ Submits to Flask backend via HTTP POST
3. ✅ Encodes 346-dimensional feature vector
4. ✅ Runs model inference (Euclidean distance)
5. ✅ Applies clinical validation rules
6. ✅ Compares clinical vs model predictions
7. ✅ Uses **biomarker-dominant logic** when strong clinical signal
8. ✅ Generates ALERT/MONITOR/REASSURE decision
9. ✅ Returns results as JSON
10. ✅ Displays in user-friendly format

**The key improvement**: When clinical biomarkers show a clear signal (e.g., 88% myositis) but the model is indecisive (50%-50% split), we now correctly trust the biomarker evidence!


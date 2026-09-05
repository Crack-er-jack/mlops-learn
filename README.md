# MLOpsHub: Production Quest ⚡
*Build it. Ship it. Break it. Diagnose it. Fix it.*

**MLOpsHub: Production Quest** is a playable, interactive educational MLOps simulation built for instructors and students to experience the end-to-end engineering discipline of shipping and operating a machine learning product.

Set at the fictional AI startup **NEONBYTE**, the platform revolves around **ChurnGuard**, a customer churn retention service powered by a CPU-friendly tabular classification pipeline.

---

## 🌟 The Core Philosophy

> **"MLOps is not a collection of tools. It is the engineering discipline required to reliably move ML from an experiment into a continuously changing production system."**

Rather than presenting isolated definitions, every mission confronts the player with an operational problem first:
- *Before DVC:* "Your teammate modified the dataset and your model score diverged. Can you reproduce yesterday's results?"
- *Before Feature Store:* "The model performs well in training, but behaves erratically in production. Investigate."
- *Before Observability:* "The server hasn't crashed (HTTP 200 OK), but customer retention is collapsing. What changed?"
- *Before Governance:* "The compliance officer asks: Which exact dataset trained this model, who approved it, and what are its known limitations?"

---

## 🎨 Dual Visual Worlds

The platform features two synchronized visual environments:
1. **World A: Real-World Roleplay**
   - Soft, pleasant, illustrated workplace desks.
   - 7 distinct roles: Data Analyst, Data Scientist, ML Engineer, DevOps/MLOps Engineer, Software Engineer, SRE / Incident Commander, and Engineering Lead.
2. **World B: MLOps Under-The-Hood**
   - Cyberpunk neon technical mode (`#00f5ff` cyan, `#ff007f` magenta, `#39ff14` neon green).
   - High-contrast, projector-friendly typography for classrooms.
   - Interactive terminal components with real copyable CLI commands and realistic execution logs.

---

## 🗺️ 21 Missions Curriculum

```
MISSION 01: Meet the Team & Problem Formulation (Data Analyst)
    ↓
MISSION 02: Understand & Clean the Data (Data Analyst)
    ↓
MISSION 03: Build the Baseline Model (Data Scientist)
    ↓
MISSION 04: The Reproducibility Trap & Seeds (Data Scientist)
    ↓
MISSION 05: Version the Data with DVC (ML Engineer)
    ↓
MISSION 06: Track Experiments with MLflow (Data Scientist)
    ↓
MISSION 07: Version the Model & Model Registry (ML Engineer)
    ↓
MISSION 08: Manage Features & Avoid Skew (ML Engineer)
    ↓
MISSION 09: Test the Pipeline with Pytest (ML Engineer)
    ↓
MISSION 10: Continuous Integration with GitHub Actions (DevOps / MLOps)
    ↓
MISSION 11: Continuous Delivery & Docker (DevOps / MLOps)
    ↓
MISSION 12: Deploy the Model to Production (Software / MLOps)
    ↓
MISSION 13: Observe Production & Detect Drift (MLOps / SRE)
    ↓
MISSION 14: Fairness & Subgroup Bias Audit (Responsible AI)
    ↓
MISSION 15: Model Explainability & Attribution (Data Scientist)
    ↓
MISSION 16: Model Governance & Model Cards (ML Lead)
    ↓
MISSION 17: The Silent Production Change (SRE / MLOps)
    ↓
MISSION 18: Incident INC-042: System Degraded (Incident Commander)
    ↓
MISSION 19: Root Cause Analysis & AI Graph (Incident Commander)
    ↓
MISSION 20: Remediate & Restore Service (Incident Commander)
    ↓
FINAL MISSION: Leadership Review & Future Horizon (Engineering Lead)
```

---

## 🎓 Persistent Instructor Control Panel

The sticky top control bar gives instructors total presentation flexibility:
- **Navigation Flow:** Start, Pause, Resume, Skip, Prev, and Reset Quest.
- **Track Selection:**
  - **30-Minute Fast Demo:** Curated 13 high-value milestone missions for short keynotes and executive demos.
  - **Full Hands-On:** Comprehensive 21-mission deep dive curriculum.
- **Student Mode Toggle:** Hides instructor notes, solutions, and root-cause candidates to challenge students.
- **Display Toggles:** Show/hide code, terminal, and instructor teaching notes.
- **Capabilities Tracker:** Dynamic checklist of unlocked MLOps competencies.

---

## 🕸️ Novel Layer: AI System Dependency Graph & Evidence RCA

In Mission 19, the simulation exposes an interactive dependency graph:
```
Raw Data ➔ Data Pipeline ➔ Feature Store ➔ Model Registry ➔ Serving API ➔ Prediction Stream ➔ Business KPI
```
When **Incident INC-042** strikes:
- Rather than a black-box guessing game, the engine calculates transparent **Root Cause Candidate Rankings** combining:
  1. Statistical distribution drift (PSI & KS tests)
  2. Temporal change proximity (Git commits & Airflow runs)
  3. Graph dependency impact weights
  4. Model artifact invariance checks

---

## 🚀 Quick Start & Installation

### Prerequisites
- Python 3.11 or 3.12
- No GPU or external cloud accounts needed (runs 100% locally on CPU).

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Automated Test Suite
```bash
pytest tests/ -v
```

### 3. Launch Application
```bash
streamlit run app.py
```
Open your browser at: `http://localhost:8501`

---

## 📁 Codebase Architecture

```
mlops/
├── app.py                          # Streamlit application entrypoint
├── requirements.txt                # Python package requirements
├── README.md                       # Documentation & presentation guide
├── .streamlit/
│   └── config.toml                 # Dark cyber theme configuration
├── src/
│   ├── theme.py                    # CSS styling for World A & World B
│   ├── state.py                    # Session state, progress, XP, badges
│   ├── data/
│   │   ├── generator.py            # Synthetic clean, dirty & drifted data
│   │   └── dvc_sim.py              # Simulated DVC CLI & version snapshots
│   ├── models/
│   │   ├── trainer.py              # Scikit-learn Logistic Regression & RF
│   │   ├── mlflow_sim.py           # MLflow tracking & model registry
│   │   └── explainability.py       # SHAP-style attribution & fairness metrics
│   ├── features/
│   │   └── feature_store.py        # Centralized feature catalog & skew detector
│   ├── testing/
│   │   └── test_suite.py           # Pytest unit, data, model & e2e test suite
│   ├── pipeline/
│   │   ├── ci_cd.py                # GitHub Actions workflow & Docker build
│   │   └── monitoring.py           # PSI and KS-test drift calculators
│   ├── incidents/
│   │   ├── incident_engine.py      # 5 deterministic failure scenarios (A-E)
│   │   ├── dependency_graph.py     # Interactive Plotly/NetworkX dependency DAG
│   │   └── rca_ranker.py           # Evidence-based candidate ranking engine
│   ├── missions/
│   │   ├── base_mission.py         # Standardized 9-panel pedagogical template
│   │   ├── registry.py             # Router mapping m01-m21
│   │   └── m01_roleplay.py ... m21_leadership.py
│   └── components/
│       ├── instructor_bar.py       # Persistent top HUD & control bar
│       ├── concept_map.py          # Dynamic MLOps Universe tree
│       ├── architecture_view.py    # Architectural blueprint
│       └── incident_lab.py         # Multi-incident sandbox
└── tests/
    └── test_simulation.py          # Automated verification test suite
```

---

## 📜 Compliance & Rules
- **PEP 8 Compliant:** All Python code strictly adheres to standard style guidelines.
- **Comprehensive Documentation:** Full docstrings, type annotations, and pedagogical commentary throughout.

"""
MLOpsHub: Production Quest - Technical Architecture View

This module renders the architectural blueprint of MLOpsHub:
Streamlit Presentation -> Learning Engine, Simulation Engine, Runtime Engine ->
Core MLOps Subsystems (DVC, MLflow, Feature Store, CI/CD, Monitoring) ->
Incident Forensics & RCA Engine.
"""

import streamlit as st


def render_architecture_view() -> None:
    """Render technical architecture diagram and subsystem inspector."""
    st.markdown("### 🏗️ Technical System Architecture")
    st.markdown(
        "MLOpsHub is architected as a zero-external-dependency, deterministic simulation runtime "
        "built entirely in Python and Streamlit. It runs locally on CPU with zero cloud costs."
    )

    arch_diagram_html = """
    <div style="background: #0d1322; border: 1px solid #00f5ff; border-radius: 12px; padding: 20px; font-family: monospace; white-space: pre; color: #00f5ff; line-height: 1.4; overflow-x: auto;">
                   <b style="color: #39ff14;">STREAMLIT USER EXPERIENCE LAYER (app.py)</b>
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        │                              │                              │
   <b>Learning Engine</b>               <b>Simulation Engine</b>           <b>Runtime Engine</b>
(9-Panel Mission Model)      (State & History Graph)       (Scikit-Learn / Scipy)
        │                              │                              │
        └──────────────────────────────┼──────────────────────────────┘
                                       │
                       <b style="color: #ff007f;">CORE MLOPS SUBSYSTEMS</b>
                                       │
     ┌───────────┬──────────────┬──────┴───────┬──────────────┬───────────┐
     │           │              │              │              │           │
 <b>DVC Sim</b>    <b>MLflow Sim</b>   <b>Feature Store</b>   <b>Pytest Suite</b>  <b>CI/CD Engine</b> <b>Monitoring</b>
(Data Hash)  (Runs & Reg)     (Anti-Skew)    (Quality Gate)   (Docker)     (PSI / KS)
     │           │              │              │              │           │
     └───────────┴──────────────┴──────┬───────┴──────────────┴───────────┘
                                       │
                                       ▼
                       <b style="color: #ff4444;">AI SYSTEM DEPENDENCY GRAPH</b>
               (NetworkX Topology: Raw ➔ ETL ➔ Feature ➔ Model ➔ API)
                                       │
                                       ▼
                       <b style="color: #ffbd2e;">EVIDENCE-BASED RCA RANKER</b>
                  (Multi-factor Causal Confidence Scoring)
                                       │
                                       ▼
                       <b style="color: #39ff14;">SERVICE RESTORATION RUNBOOK</b>
                     (1-Click Automated Rollback & Test)
    </div>
    """
    st.markdown(arch_diagram_html, unsafe_allow_html=True)

    st.markdown("#### 🔍 Inspect Subsystem Specifications:")
    subsystem = st.selectbox(
        "Select Subsystem to Review Internals:",
        [
            "DVC Simulation Engine (src/data/dvc_sim.py)",
            "MLflow Tracking & Registry (src/models/mlflow_sim.py)",
            "Feature Store & Anti-Skew (src/features/feature_store.py)",
            "Pytest Automated Quality Suite (src/testing/test_suite.py)",
            "CI/CD & Docker Packaging (src/pipeline/ci_cd.py)",
            "Production Drift Telemetry (src/pipeline/monitoring.py)",
            "AI Dependency Graph & RCA Ranker (src/incidents/)"
        ]
    )

    if "DVC" in subsystem:
        st.info("📦 **DVC Simulator:** Tracks lightweight `.dvc` YAML pointer files with MD5 hashes. Decouples heavy data from Git repository history.")
    elif "MLflow" in subsystem:
        st.info("📈 **MLflow Simulator:** Implements experiment run logging (params, metrics, tags, artifacts) and stage transitions (Staging -> Production -> Archived).")
    elif "Feature Store" in subsystem:
        st.info("🏪 **Feature Store:** Unifies offline SQL batch definitions with online low-latency serving keys, preventing training-serving skew.")
    elif "Pytest" in subsystem:
        st.info("🧪 **Pytest Suite:** Tests 4 layers: Unit, Data Contracts, Model Minimum Thresholds (F1 >= 0.70), and End-to-End Integration.")
    elif "CI/CD" in subsystem:
        st.info("⚙️ **CI/CD & Docker:** Simulates GitHub Actions runners and Docker multi-layer builds producing an immutable 184MB container.")
    elif "Monitoring" in subsystem:
        st.info("📡 **Drift Monitoring:** Computes Population Stability Index (PSI) and Kolmogorov-Smirnov 2-sample tests to detect distribution decay.")
    else:
        st.info("🕸️ **AI Dependency Graph & RCA:** Constructs a 7-node DAG connecting data sources to business KPIs, ranking root cause suspects using composite evidence scores.")

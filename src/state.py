"""
MLOpsHub: Production Quest - Session State & Simulation Manager

This module handles persistent simulation state, progress tracking,
XP gamification, badges, unlocked MLOps capabilities, and instructor/student
mode configuration.
"""

from typing import Any, Dict, List, Set
import streamlit as st


# Complete list of available missions in canonical order
ALL_MISSIONS = [
    {"id": "m01", "num": "01", "title": "Meet the Team & Problem Formulation", "role": "Data Analyst", "badge": "Data Steward"},
    {"id": "m02", "num": "02", "title": "Understand & Clean the Data", "role": "Data Analyst", "badge": "Data Quality Champion"},
    {"id": "m03", "num": "03", "title": "Build the Baseline Model", "role": "Data Scientist", "badge": "Baseline Builder"},
    {"id": "m04", "num": "04", "title": "The Reproducibility Trap", "role": "Data Scientist", "badge": "Deterministic Dev"},
    {"id": "m05", "num": "05", "title": "Version the Data with DVC", "role": "ML Engineer", "badge": "Data Versioner"},
    {"id": "m06", "num": "06", "title": "Track Experiments with MLflow", "role": "Data Scientist", "badge": "Experiment Scientist"},
    {"id": "m07", "num": "07", "title": "Version the Model & Registry", "role": "ML Engineer", "badge": "Model Guardian"},
    {"id": "m08", "num": "08", "title": "Manage Features & Avoid Skew", "role": "ML Engineer", "badge": "Feature Architect"},
    {"id": "m09", "num": "09", "title": "Test the Pipeline (Pytest)", "role": "ML Engineer", "badge": "Pipeline Tester"},
    {"id": "m10", "num": "10", "title": "Continuous Integration (CI)", "role": "DevOps / MLOps", "badge": "CI Automator"},
    {"id": "m11", "num": "11", "title": "Continuous Delivery & Docker", "role": "DevOps / MLOps", "badge": "Container Captain"},
    {"id": "m12", "num": "12", "title": "Deploy the Model to Production", "role": "Software / MLOps", "badge": "Deployment Engineer"},
    {"id": "m13", "num": "13", "title": "Observe Production & Detect Drift", "role": "MLOps / SRE", "badge": "Observability Sentinel"},
    {"id": "m14", "num": "14", "title": "Fairness & Bias Audit", "role": "Responsible AI", "badge": "Ethics Auditor"},
    {"id": "m15", "num": "15", "title": "Model Explainability (Attribution)", "role": "Data Scientist", "badge": "Explainability Expert"},
    {"id": "m16", "num": "16", "title": "Model Governance & Model Card", "role": "ML Lead", "badge": "Governance Leader"},
    {"id": "m17", "num": "17", "title": "The Silent Production Change", "role": "SRE / MLOps", "badge": "Production Scout"},
    {"id": "m18", "num": "18", "title": "Incident INC-042: System Degraded", "role": "Incident Commander", "badge": "First Responder"},
    {"id": "m19", "num": "19", "title": "Root Cause Analysis (AI Graph)", "role": "Incident Commander", "badge": "Root Cause Detective"},
    {"id": "m20", "num": "20", "title": "Remediate & Verify Service", "role": "Incident Commander", "badge": "Reliability Hero"},
    {"id": "m21", "num": "FINAL", "title": "Leadership Review & Future Horizon", "role": "Engineering Lead", "badge": "MLOps Architect"},
]

# Fast 30-Minute Demo Track (Subset of high-value milestone missions)
FAST_DEMO_IDS = ["m01", "m02", "m03", "m05", "m06", "m08", "m10", "m12", "m13", "m18", "m19", "m20", "m21"]

# Core MLOps Capabilities Checklist
ALL_CAPABILITIES = [
    {"key": "data_quality", "label": "Data Quality & Validation", "mission": "m02"},
    {"key": "reproducibility", "label": "Reproducibility & Seed Control", "mission": "m04"},
    {"key": "data_versioning", "label": "Data Versioning (DVC)", "mission": "m05"},
    {"key": "experiment_tracking", "label": "Experiment Tracking (MLflow)", "mission": "m06"},
    {"key": "model_registry", "label": "Model Registry & Lineage", "mission": "m07"},
    {"key": "feature_store", "label": "Feature Store (Anti-Skew)", "mission": "m08"},
    {"key": "ml_testing", "label": "Comprehensive ML Testing", "mission": "m09"},
    {"key": "ci_cd", "label": "Automated CI/CD Workflows", "mission": "m10"},
    {"key": "containerization", "label": "Docker Container Runtime", "mission": "m11"},
    {"key": "production_serving", "label": "Production Serving API", "mission": "m12"},
    {"key": "drift_monitoring", "label": "Statistical Drift Monitoring", "mission": "m13"},
    {"key": "fairness_audit", "label": "Fairness & Bias Mitigations", "mission": "m14"},
    {"key": "explainability", "label": "Local/Global Explainability", "mission": "m15"},
    {"key": "governance", "label": "Model Card & Governance", "mission": "m16"},
    {"key": "dependency_graph", "label": "AI System Dependency Graph", "mission": "m19"},
    {"key": "rca_remediation", "label": "Evidence-Based RCA & Fix", "mission": "m20"},
]


def init_session_state() -> None:
    """Initialize all simulation variables in st.session_state if not present."""
    defaults: Dict[str, Any] = {
        "current_mission_index": 0,
        "completed_missions": set(),
        "unlocked_capabilities": set(),
        "xp": 0,
        "badges": [],
        "demo_mode": "full",          # "full" or "fast"
        "instructor_mode": True,       # True: Instructor view, False: Student view
        "show_code": True,             # Show code panels
        "show_terminal": True,         # Show terminal component
        "show_notes": True,            # Show instructor pedagogical notes
        "active_incident": "A",        # Default incident is A (Feature drift)
        "simulation_paused": False,
        "selected_nav": "Missions",    # "Missions", "Universe", "Architecture", "IncidentLab"
        "custom_inputs": {},           # Stores sandbox interactive inputs
    }

    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def get_active_missions() -> List[Dict[str, str]]:
    """Return the list of missions based on current demo mode ('full' vs 'fast')."""
    if st.session_state.get("demo_mode") == "fast":
        return [m for m in ALL_MISSIONS if m["id"] in FAST_DEMO_IDS]
    return ALL_MISSIONS


def get_current_mission() -> Dict[str, str]:
    """Retrieve metadata dictionary for the currently active mission."""
    active = get_active_missions()
    idx = st.session_state.get("current_mission_index", 0)
    if idx >= len(active):
        idx = len(active) - 1
        st.session_state["current_mission_index"] = idx
    return active[idx]


def complete_mission(mission_id: str, xp_award: int = 100, badge_name: str = "") -> None:
    """
    Mark a mission as completed, unlock related capabilities, and award XP/badge.

    Args:
        mission_id: Identifier of the mission (e.g. 'm01').
        xp_award: Experience points awarded.
        badge_name: Badge title awarded upon completion.
    """
    if "completed_missions" not in st.session_state:
        st.session_state["completed_missions"] = set()
    st.session_state["completed_missions"].add(mission_id)

    # Unlock capabilities mapped to this mission
    for cap in ALL_CAPABILITIES:
        if cap["mission"] == mission_id:
            st.session_state["unlocked_capabilities"].add(cap["key"])

    # Award XP
    st.session_state["xp"] = st.session_state.get("xp", 0) + xp_award

    # Award Badge if unique
    if badge_name and badge_name not in st.session_state.get("badges", []):
        st.session_state["badges"].append(badge_name)


def advance_mission() -> None:
    """Move to the next mission in the current mission track."""
    active = get_active_missions()
    current_idx = st.session_state.get("current_mission_index", 0)
    if current_idx < len(active) - 1:
        st.session_state["current_mission_index"] = current_idx + 1


def previous_mission() -> None:
    """Move to the previous mission in the current mission track."""
    current_idx = st.session_state.get("current_mission_index", 0)
    if current_idx > 0:
        st.session_state["current_mission_index"] = current_idx - 1


def reset_simulation() -> None:
    """Reset the entire simulation state to pristine start."""
    st.session_state["current_mission_index"] = 0
    st.session_state["completed_missions"] = set()
    st.session_state["unlocked_capabilities"] = set()
    st.session_state["xp"] = 0
    st.session_state["badges"] = []
    st.session_state["custom_inputs"] = {}

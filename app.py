"""
MLOpsHub: Production Quest - Main Application Entrypoint

An interactive, browser-based educational MLOps simulation platform.
Fictional Startup: NEONBYTE
Product: ChurnGuard (AI Customer Retention Service)

This application guides instructors and students through the entire MLOps
lifecycle: Data Versioning (DVC), Experiment Tracking (MLflow), Feature Store,
Testing, CI/CD, Containerization (Docker), Production Serving, Observability,
Governance, Incidents, AI System Dependency Graphs, and Root Cause Analysis.
"""

import streamlit as st
from src.components.architecture_view import render_architecture_view
from src.components.concept_map import render_concept_universe
from src.components.incident_lab import render_incident_lab
from src.components.instructor_bar import render_instructor_bar
from src.missions.registry import MissionRegistry
from src.state import (
    get_active_missions,
    get_current_mission,
    init_session_state
)
from src.theme import inject_custom_css, render_neon_card


def setup_page_config() -> None:
    """Configure Streamlit browser window metadata, favicon, and wide layout."""
    st.set_page_config(
        page_title="MLOpsHub: Production Quest",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def render_sidebar_navigation() -> str:
    """
    Render sleek cybernetic sidebar with navigation tabs, mission selector,
    and simulation telemetry.

    Returns:
        String identifier of selected view.
    """
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="font-size: 2.2rem;">⚡</div>
            <div style="font-size: 1.3rem; font-weight: 900; color: #00f5ff; letter-spacing: 1px;">
                MLOpsHub
            </div>
            <div style="font-size: 0.85rem; color: #ff007f; font-weight: 700; letter-spacing: 0.5px;">
                PRODUCTION QUEST
            </div>
        </div>
        """, unsafe_allow_html=True)

        nav_choice = st.radio(
            "Navigation View:",
            ["🎯 Active Mission", "🌌 MLOps Universe", "🏗️ Architecture", "🔬 Incident Lab", "🏠 Home & Overview"],
            index=0
        )

        st.markdown("---")

        # Mission Quick-Selector
        active_missions = get_active_missions()
        current_idx = st.session_state.get("current_mission_index", 0)
        mission_options = [f"M{m['num']}: {m['title'][:22]}.." for m in active_missions]

        st.markdown("**Jump to Mission:**")
        selected_mission_idx = st.selectbox(
            "Select Mission:",
            range(len(active_missions)),
            format_func=lambda i: mission_options[i],
            index=min(current_idx, len(active_missions) - 1),
            label_visibility="collapsed"
        )
        if selected_mission_idx != current_idx:
            st.session_state["current_mission_index"] = selected_mission_idx
            st.rerun()

        st.markdown("---")

        # Team Telemetry Box
        st.markdown("""
        <div style="background: rgba(19, 27, 46, 0.8); border: 1px solid rgba(0, 245, 255, 0.3); border-radius: 8px; padding: 12px; font-size: 0.85rem;">
            <div style="color: #00f5ff; font-weight: 700; margin-bottom: 4px;">🏢 COMPANY: NEONBYTE</div>
            <div style="color: #d1d5db;">Product: <b>ChurnGuard v3</b></div>
            <div style="color: #d1d5db;">Active Role: <b>{role}</b></div>
            <div style="color: #39ff14; margin-top: 6px;">Status: <b>OPERATIONAL</b></div>
        </div>
        """.format(role=get_current_mission()["role"]), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("GNITS MLOps Education • Production Quest v1.0")

    return nav_choice


def render_home_hero() -> None:
    """Render high-impact hero landing page with story intro and launch buttons."""
    st.markdown("""
    <div style="text-align: center; padding: 30px 10px 20px 10px;">
        <div style="font-size: 3rem; font-weight: 900; color: #00f5ff; text-shadow: 0 0 20px rgba(0, 245, 255, 0.4); letter-spacing: 1px;">
            MLOpsHub: Production Quest
        </div>
        <div style="font-size: 1.4rem; color: #f0f6fc; margin-top: 10px; font-weight: 600;">
            Build it. Ship it. Break it. Diagnose it. Fix it.
        </div>
        <div style="color: #8b949e; max-width: 800px; margin: 15px auto; font-size: 1.05rem; line-height: 1.6;">
            A playable simulation of a real software and machine learning engineering team shipping
            an AI product at fictional startup <b>NEONBYTE</b>. Experience the full lifecycle across 7 engineering roles.
        </div>
    </div>
    """, unsafe_allow_html=True)

    cta_col1, cta_col2, cta_col3 = st.columns([1, 2, 1])
    with cta_col2:
        if st.button("🚀 START THE MISSION (Enter Quest)", type="primary", use_container_width=True):
            st.session_state["selected_nav"] = "🎯 Active Mission"
            st.session_state["current_mission_index"] = 0
            st.rerun()

    st.markdown("---")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class="roleplay-card">
            <h3 style="color: #79c0ff; margin-top: 0;">🏢 WORLD A: REAL-WORLD ROLEPLAY</h3>
            <p style="color: #d1d5db; line-height: 1.6;">
                Soft, pleasant workplace aesthetic. Embody 7 distinct roles across sprints:
            </p>
            <ul style="color: #f0f6fc; line-height: 1.8;">
                <li>📊 <b>Data Analyst:</b> Understand problem, explore data, identify leakage</li>
                <li>🔬 <b>Data Scientist:</b> Baseline models, reproducibility, experiment tracking</li>
                <li>🏛️ <b>ML Engineer:</b> Model registry, feature store, testing suites</li>
                <li>⚙️ <b>DevOps / MLOps:</b> Continuous Integration & Docker delivery</li>
                <li>🚀 <b>Software Engineer:</b> Production serving & lineage tracing</li>
                <li>🚨 <b>SRE / Incident Commander:</b> Triage, dependency graph, root-cause analysis</li>
                <li>🏆 <b>Engineering Lead:</b> Business ROI and leadership presentation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="neon-card">
            <h3 style="color: #00f5ff; margin-top: 0;">⚡ WORLD B: MLOPS UNDER-THE-HOOD</h3>
            <p style="color: #c9d1d9; line-height: 1.6;">
                Cyberpunk technical visualization mode with glowing cards, real code, and simulated CLIs:
            </p>
            <ul style="color: #f0f6fc; line-height: 1.8;">
                <li>📦 <b>DVC:</b> Data Version Control with immutable content hashes</li>
                <li>📈 <b>MLflow:</b> Real experiment leaderboards and artifact tracking</li>
                <li>🏪 <b>Feature Store:</b> Eliminating training-serving skew</li>
                <li>🧪 <b>Pytest:</b> Unit, data contract, and model quality gates</li>
                <li>🐳 <b>Docker & GitHub Actions:</b> Reproducible containerized runtimes</li>
                <li>📡 <b>Production Drift:</b> Real-time PSI and KS-test monitoring</li>
                <li>🕸️ <b>AI Dependency Graph:</b> Evidence-based causal root cause analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


def main() -> None:
    """Main application orchestrator."""
    setup_page_config()
    init_session_state()
    inject_custom_css()

    nav_view = render_sidebar_navigation()

    # Route according to navigation selection
    if nav_view == "🏠 Home & Overview":
        render_home_hero()
    elif nav_view == "🌌 MLOps Universe":
        render_instructor_bar()
        render_concept_universe()
    elif nav_view == "🏗️ Architecture":
        render_instructor_bar()
        render_architecture_view()
    elif nav_view == "🔬 Incident Lab":
        render_instructor_bar()
        render_incident_lab()
    else:  # "🎯 Active Mission"
        render_instructor_bar()
        current_meta = get_current_mission()
        mission_obj = MissionRegistry.get_mission(current_meta["id"])
        mission_obj.render()


if __name__ == "__main__":
    main()

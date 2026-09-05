"""
MLOpsHub: Production Quest - Incident Lab & Multi-Scenario Sandbox

This module allows instructors to test all 5 deterministic incident scenarios
(Incidents A through E) and trigger randomized production emergencies.
"""

import random
import streamlit as st
import pandas as pd
from src.incidents.incident_engine import IncidentEngine
from src.theme import render_neon_card


def render_incident_lab() -> None:
    """Render the multi-scenario Incident Lab sandbox."""
    st.markdown("### 🔬 Production Incident Simulation Lab")
    st.markdown(
        "Test your team's operational readiness across multiple deterministic failure scenarios. "
        "Select a specific scenario or roll for a **Random Incident** to test troubleshooting under pressure."
    )

    incidents_dict = IncidentEngine.INCIDENTS
    col_select, col_rand = st.columns([3, 1])

    with col_select:
        selected_key = st.selectbox(
            "Select Incident Scenario to Mount:",
            options=list(incidents_dict.keys()),
            format_func=lambda k: f"{incidents_dict[k]['id']}: {incidents_dict[k]['title']} [{incidents_dict[k]['type']}]",
            index=list(incidents_dict.keys()).index(st.session_state.get("active_incident", "A"))
        )

    with col_rand:
        st.write("")
        st.write("")
        if st.button("🎲 Random Incident", use_container_width=True):
            selected_key = random.choice(list(incidents_dict.keys()))
            st.session_state["active_incident"] = selected_key
            st.rerun()

    st.session_state["active_incident"] = selected_key
    inc = incidents_dict[selected_key]

    # Incident Overview Card
    st.markdown(f"""
    <div style="background: rgba(255, 68, 68, 0.12); border: 1px solid #ff4444; border-radius: 10px; padding: 16px; margin: 12px 0;">
        <h3 style="color: #ff6b6b; margin-top: 0;">🚨 {inc['id']} — {inc['title']}</h3>
        <p style="color: #f3f4f6;"><b>Type:</b> {inc['type']} | <b>Severity:</b> {inc['severity']} | <b>Started:</b> {inc['started_at']}</p>
        <p style="color: #d1d5db;"><b>Symptom:</b> {inc['symptom']}</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Pre-Incident F1", f"{inc['f1_before']:.2f}")
    c2.metric("Degraded F1", f"{inc['f1_after']:.2f}", delta=f"{inc['f1_after'] - inc['f1_before']:.2f}", delta_color="inverse")
    c3.metric("API Latency / Error", f"{inc['latency_ms']} | {inc['error_rate']}")

    st.markdown("#### 🔍 Telemetry & Evidence Logs:")
    for log in inc["evidence_logs"]:
        st.code(log, language="bash")

    st.markdown("#### ⚖️ Suspect Component Scoring:")
    st.dataframe(pd.DataFrame(inc["suspect_nodes"]), use_container_width=True)

    with st.expander("💡 Root Cause Analysis & Remediation Plan", expanded=False):
        st.markdown(f"**Root Cause Analysis:**\n{inc['root_cause_explanation']}")
        st.markdown("**Remediation Steps:**")
        for step in inc["remediation_plan"]:
            st.markdown(f"- {step}")

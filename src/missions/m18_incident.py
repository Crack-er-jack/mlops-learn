"""
MLOpsHub: Production Quest - Mission 18: Incident INC-042: System Degraded

Role: SRE / Incident Commander
Desk: Incident emergency room with red flashing beacon, live telemetry feeds, and Slack war room.
Teaches: Production incident triage, telemetry gathering, multi-dimensional diagnostic data.
"""

import streamlit as st
import pandas as pd
from src.incidents.incident_engine import IncidentEngine
from src.missions.base_mission import BaseMission
from src.theme import render_neon_card, render_terminal


class Mission18(BaseMission):
    """Mission 18 Implementation."""

    def __init__(self) -> None:
        super().__init__(
            mission_id="m18",
            number_str="18",
            title="Incident INC-042: System Degraded",
            role_name="Incident Commander",
            role_emoji="🚨",
            desk_desc="Incident emergency cockpit with flashing red strobe light, live PagerDuty alert monitors, and War Room whiteboard.",
            badge_name="First Responder",
            xp_award=160
        )

    def render(self) -> None:
        """Render Mission 18 UI components."""
        incident = IncidentEngine.get_incident("A")

        # Flashing emergency banner
        st.markdown(f"""
        <div class="incident-alert-banner">
            <div style="font-size: 1.5rem; font-weight: 900; color: #ff4444; letter-spacing: 1px;">
                🚨 CRITICAL SEVERITY INCIDENT: {incident['id']}
            </div>
            <div style="color: #ffffff; font-size: 1.05rem; margin-top: 6px;">
                <b>{incident['title']}</b> | Started: {incident['started_at']} | Severity: {incident['severity']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        story = (
            "**Thursday, 14:32 UTC — EMERGENCY WAR ROOM**<br>"
            "CEO Maya kicks open the war room door: *'The marketing lead just escalated an emergency. "
            "Our automated retention bot just dispatched frantic 40% discount apology emails to 8,000 of our most loyal "
            "enterprise customers who just renewed last week! Social media is asking if NEONBYTE is going bankrupt! "
            "The engineering dashboard says the server is at 99.9% uptime, but the model is throwing garbage!'*<br><br>"
            "As Incident Commander, you must lead the cross-functional response."
        )
        objective = (
            "Take command of Incident INC-042. Triage symptoms, review telemetry streams, "
            "examine audit logs, and isolate which layer of the system is malfunctioning."
        )
        self.render_standard_header(story, objective)

        self.render_instructor_notes(
            objective="Guide students through structured incident triage and show how earlier MLOps assets (versioning, tracking, monitoring) become investigative lifelines.",
            talking_points=[
                "The Panic Trap: When an AI incident occurs, non-technical leadership wants to immediately retrain the model or blame the data scientist.",
                "Structured Triage: 1. Assess blast radius, 2. Check infrastructure health (is it crashing?), 3. Check data feeds, 4. Check recent deployments, 5. Check model weights.",
                "Why the server status (HTTP 200) was deceiving: The model answered every request fast and without error, but the predictions were catastrophic."
            ],
            questions=[
                "Why shouldn't our first action be 'Retrain the model right now on today's data'?",
                "If the serving API latency is normal (18ms) and HTTP error rate is 0.0%, why did customer retention collapse?"
            ],
            expected_answers=[
                "If the incoming data is corrupted, retraining on corrupted data permanently ruins the model weights!",
                "The failure is semantic (wrong mathematical outputs), not operational infrastructure downtime."
            ],
            misconceptions=[
                "Assuming incidents in AI systems are always solved by retraining.",
                "Thinking you need complex AI to diagnose an incident before inspecting basic timestamps and git commits."
            ],
            deep_dive="Explain how PagerDuty severity levels (P1, P2, P3) dictate incident response escalation.",
            skip_tip="Click through the 4 investigative tabs below to gather evidence."
        )

        # Panel 4: Learn
        learn_html = """
        <b>The Incident Triage Protocol:</b><br>
        1. <b>Symptom Verification:</b> Confirm metric drop ($F1: 0.84 \rightarrow 0.68$).<br>
        2. <b>Infrastructure Health:</b> Verify HTTP status ($200$ OK) & latency ($18.4ms$).<br>
        3. <b>Change Audit:</b> Query Git commits, Airflow DAGs, and Model Registry changes in the last 6 hours.<br>
        4. <b>Telemetry Deep Dive:</b> Compare baseline feature distributions against live inference windows.
        """
        render_neon_card("4. LEARN: INCIDENT TRIAGE PLAYBOOK", learn_html, color_variant="purple")

        # Panel 5: Do
        st.markdown("#### 5. DO: Investigate Incident Telemetry & Evidence")

        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Metrics & F1 Degradation",
            "📜 Incident Timeline & Audit Logs",
            "🔍 Feature Distribution Shift",
            "🏷️ Model Registry Lineage"
        ])

        with tab1:
            c1, c2, c3 = st.columns(3)
            c1.metric("F1 Performance Score", f"{incident['f1_after']}", delta=f"{incident['f1_after'] - incident['f1_before']:.2f}", delta_color="inverse")
            c2.metric("Inference Latency", incident["latency_ms"], delta="Healthy")
            c3.metric("HTTP 500 Error Rate", incident["error_rate"], delta="Healthy")
            st.error(f"**Customer Blast Radius:** {incident['symptom']}")

        with tab2:
            st.markdown("**Chronological Incident Event Stream:**")
            for log_entry in incident["evidence_logs"]:
                st.code(log_entry, language="bash")

        with tab3:
            st.markdown("**Real-Time Feature Distribution Check (Current Window vs Baseline):**")
            drift_sample = [
                {"Feature": "monthly_spend", "Baseline Mean": "$87.20", "Live Prod Mean": "$214.80", "PSI Score": 0.42, "Status": "🔴 CRITICAL DRIFT"},
                {"Feature": "tenure", "Baseline Mean": "24.1 mo", "Live Prod Mean": "23.9 mo", "PSI Score": 0.03, "Status": "🟢 STABLE"},
                {"Feature": "support_calls", "Baseline Mean": "2.2 calls", "Live Prod Mean": "2.3 calls", "PSI Score": 0.04, "Status": "🟢 STABLE"},
                {"Feature": "usage_frequency", "Baseline Mean": "18.1 log/wk", "Live Prod Mean": "17.9 log/wk", "PSI Score": 0.02, "Status": "🟢 STABLE"},
            ]
            st.dataframe(pd.DataFrame(drift_sample), use_container_width=True)

        with tab4:
            st.markdown("**Active Production Model Verification:**")
            st.markdown("- **Model:** `ChurnGuard v3.0`")
            st.markdown("- **Artifact Checksum:** `sha256:d8c47f9a21b8` (Verified Unchanged)")
            st.markdown("- **Last Registry Promotion:** `3 weeks ago`")
            st.info("Notice: The model artifact itself has NOT changed. The code inside the Docker container is intact.")

        # Panel 6: Under the Hood
        if st.session_state.get("show_code", True):
            st.markdown("#### 6. UNDER THE HOOD: Incident Diagnostics Query")
            code_str = (
                "# SRE Diagnostic CLI query\n"
                "dvc status\n"
                "curl -s http://churnguard-prod:8501/metrics | grep 'churn_prediction'\n"
                "git log --since='6 hours ago' --oneline"
            )
            st.code(code_str, language="bash")

        # Panel 7: Result
        render_neon_card(
            "7. RESULT",
            "Triage complete: Infrastructure is 100% online. Model weights are unchanged. But <code>monthly_spend</code> distribution has surged from $87 to $214 right after PR #412 was merged!",
            color_variant="magenta"
        )

        # Panel 8: Why This Matters
        render_neon_card(
            "8. WHY THIS MATTERS",
            "Without MLOps observability and data tracking, the team would have spent 12 hours arguing over model weights or blaming the API server. <b>Evidence narrows the search space immediately.</b>",
            color_variant="cyan"
        )

        # Panel 9: Next
        st.info("🔜 **Next Mission:** Now we perform rigorous Root Cause Analysis (RCA) using the AI System Dependency Graph and Evidence Candidate Ranking!")
        self.render_navigation_footer()

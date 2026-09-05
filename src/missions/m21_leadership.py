"""
MLOpsHub: Production Quest - Mission 21: Leadership Review & Future Horizon

Role: Engineering Lead / Product Manager
Desk: Executive boardroom with presentation projector, financial KPIs, and architecture slides.
Teaches: Business ROI of MLOps, operational maturity, systemic reliability, future causal horizons.
"""

import streamlit as st
from src.missions.base_mission import BaseMission
from src.theme import render_neon_card, render_terminal


class Mission21(BaseMission):
    """Mission 21 Implementation (Final Mission)."""

    def __init__(self) -> None:
        super().__init__(
            mission_id="m21",
            number_str="FINAL",
            title="Leadership Review & Future Horizon",
            role_name="Engineering Lead",
            role_emoji="🏆",
            desk_desc="Executive boardroom with high-definition presentation projector, ROI charts, and congratulatory coffee mugs.",
            badge_name="MLOps Architect",
            xp_award=250
        )

    def render(self) -> None:
        """Render Mission 21 UI components."""
        story = (
            "**Friday, 9:00 AM — Executive Boardroom**<br>"
            "CEO Maya, CFO Marcus, and the Board of Directors sit around the polished glass table. "
            "Maya smiles: *'Yesterday, an upstream bug almost wrecked our customer retention program. "
            "In my previous company, that bug would have stayed hidden for 3 weeks and cost millions. "
            "Instead, your team caught it in minutes, traced it to the exact git commit, and rolled it back safely. "
            "Now tell the board: Why did our MLOps investment make all the difference?'*"
        )
        objective = (
            "Present the strategic business ROI of MLOps to executive leadership. "
            "Review the ChurnGuard Production Reliability Score, celebrate earned badges, "
            "and examine the next frontier: AI System Reliability & Causal Incident Diagnosis."
        )
        self.render_standard_header(story, objective)

        self.render_instructor_notes(
            objective="Synthesize the entire 20-mission curriculum into a cohesive mental model: MLOps is not a tool collection, but an engineering discipline.",
            talking_points=[
                "The core thesis: 'MLOps is what turns an isolated mathematical experiment into a resilient, continuously changing production system.'",
                "Why business leaders under-invest in MLOps: Infrastructure and testing are invisible until catastrophic failures occur.",
                "The ROI numbers: Mean Time to Detect (MTTD) and Mean Time to Recovery (MTTR) are the true business metrics of AI safety.",
                "The Next Frontier: Traditional MLOps monitors correlations; the next generation of AI systems requires causal diagnosis and automated self-healing."
            ],
            questions=[
                "How would you explain the value of DVC and MLflow to a non-technical CEO in one sentence?",
                "What is the difference between a company that trains models and a company that operates AI systems?"
            ],
            expected_answers=[
                "They are our company's insurance policy that guarantees any AI decision can be audited, reproduced, and trusted.",
                "A model trainer creates a static artifact; an AI operator maintains continuous feedback, monitoring, testing, and recovery over time."
            ],
            misconceptions=[
                "Thinking MLOps is finished once tools are installed (it is a continuous team engineering culture).",
                "Believing LLMs and Generative AI eliminate the need for MLOps (LLMs actually make testing, monitoring, and governance 10x more critical!)."
            ],
            deep_dive="Review the transition from heuristics to predictive models to agentic/causal reliability architectures.",
            skip_tip="Present the 'Without MLOps vs With MLOps' comparison table below to conclude the workshop."
        )

        # Panel 4: Learn
        learn_html = """
        <b>The Core Paradigm Shift:</b><br>
        • <b>Without MLOps:</b> <code>Experiment ➔ Model ➔ Deploy ➔ Breaks ➔ Chaos ➔ Days Lost</code>.<br>
        • <b>With MLOps:</b> <code>Version ➔ Test ➔ Track ➔ Deploy ➔ Monitor ➔ Detect ➔ Diagnose ➔ Remediate ➔ Verify</code>.<br>
        • <b>The Takeaway:</b> MLOps is the bridge between a notebook proof-of-concept and enterprise business value.
        """
        render_neon_card("4. LEARN: THE BUSINESS VALUE OF MLOPS", learn_html, color_variant="purple")

        # Panel 5: Do
        st.markdown("#### 5. DO: Executive Boardroom Presentation")

        st.markdown("##### ⚖️ Operational Transformation Breakdown:")
        col_comp1, col_comp2 = st.columns(2)
        with col_comp1:
            st.markdown("""
            <div style="background: rgba(255, 68, 68, 0.08); border: 1px solid #ff4444; border-radius: 8px; padding: 14px;">
                <h4 style="color: #ff6b6b; margin-top: 0;">❌ WITHOUT MLOPS</h4>
                <ul style="color: #d1d5db; font-size: 0.92rem; line-height: 1.6;">
                    <li><b>Reproducibility:</b> "Works on my laptop only" (Days lost)</li>
                    <li><b>Data Tracking:</b> <code>churn_final_v2_really_final.csv</code></li>
                    <li><b>Testing:</b> Zero tests; deploy and pray</li>
                    <li><b>Detection Time:</b> Weeks (until customers complain)</li>
                    <li><b>Root Cause Triage:</b> 16+ hours of stressful finger-pointing</li>
                    <li><b>Recovery (MTTR):</b> Manual hotfixes and weekend outages</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col_comp2:
            st.markdown("""
            <div style="background: rgba(57, 255, 20, 0.08); border: 1px solid #39ff14; border-radius: 8px; padding: 14px;">
                <h4 style="color: #39ff14; margin-top: 0;">✅ WITH MLOPS</h4>
                <ul style="color: #d1d5db; font-size: 0.92rem; line-height: 1.6;">
                    <li><b>Reproducibility:</b> 100% deterministic (Fixed seeds & Docker)</li>
                    <li><b>Data Tracking:</b> DVC immutable content-addressed hashes</li>
                    <li><b>Testing:</b> Automated Pytest + GitHub Actions CI gates</li>
                    <li><b>Detection Time:</b> 60 seconds via statistical PSI drift alerts</li>
                    <li><b>Root Cause Triage:</b> 12 minutes with AI Dependency Graph</li>
                    <li><b>Recovery (MTTR):</b> 1-click safe automated rollback</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("##### 🏆 ChurnGuard Production Reliability Scorecard:")
        score_cols = st.columns(4)
        score_cols[0].metric("Reproducibility", "10 / 10", delta="DVC + Seeds")
        score_cols[1].metric("Traceability", "10 / 10", delta="MLflow + Registry")
        score_cols[2].metric("Quality Gates", "10 / 10", delta="Pytest + CI/CD")
        score_cols[3].metric("Mean Time to Recover", "15 mins", delta="98% Faster")

        # Earned Badges
        st.markdown("##### 🎖️ Earned MLOps Badges Showcase:")
        badges = st.session_state.get("badges", [])
        if not badges:
            badges = ["Data Steward", "Experiment Scientist", "Model Guardian", "Feature Architect", "CI Automator", "Deployment Engineer", "Observability Sentinel", "Reliability Hero", "MLOps Architect"]

        badge_html = " ".join([f"<span class='badge-capsule badge-complete'>🏷️ {b}</span>" for b in badges])
        st.markdown(badge_html, unsafe_allow_html=True)

        # Panel 6: Under the Hood
        if st.session_state.get("show_code", True):
            st.markdown("#### 6. UNDER THE HOOD: The Complete Production Stack")
            code_str = (
                "# The End-to-End MLOps System Stack\n"
                "# Git          -> Code Versioning & Review\n"
                "# DVC          -> Large Dataset Artifact Tracking\n"
                "# MLflow       -> Experiment Tracking & Model Registry\n"
                "# Feast        -> Feature Store & Training-Serving Parity\n"
                "# Pytest       -> Data, Unit, Model, and Integration Tests\n"
                "# GitHub CI    -> Automated PR Testing & Verification Gates\n"
                "# Docker       -> Reproducible Containerized Runtimes\n"
                "# Scipy / PSI  -> Real-Time Feature & Concept Drift Monitoring\n"
                "# Fairlearn    -> Algorithmic Fairness & Disparate Impact Auditing\n"
                "# Model Cards  -> Governance, Intended Use, and Compliance\n"
                "# Graph & RCA  -> Evidence-Based Incident Diagnostics"
            )
            st.code(code_str, language="python")

        # Panel 7: Result
        render_neon_card(
            "7. RESULT: SYSTEM COMPLETE",
            "<h3>🚀 YOU JUST BUILT AN END-TO-END ML SYSTEM!</h3>"
            "From raw telemetry to baseline model, version control, experiment tracking, feature stores, "
            "testing, CI/CD, Docker deployment, production observability, and incident recovery—"
            "you have mastered the production lifecycle of machine learning.",
            color_variant="green"
        )

        # Panel 8: Why This Matters
        render_neon_card(
            "8. THE NEXT FRONTIER",
            "<h4>🔮 WHERE PRODUCTION AI GOES NEXT</h4>"
            "Traditional MLOps helped us operate the system and track metrics.<br><br>"
            "<b>The next grand challenge is Causal System Reliability:</b><br>"
            "When complex, multi-agent AI systems and foundation models interact with dynamic real-world environments, "
            "correlations alone are insufficient. We must engineer systems capable of automated causal reasoning, "
            "probabilistic fault localization, and self-healing resilience.<br><br>"
            "<i>Congratulations on completing MLOpsHub: Production Quest!</i>",
            color_variant="magenta"
        )

        st.balloons()
        st.success("🎓 QUEST COMPLETED! All 21 Missions and MLOps capabilities successfully unlocked.")

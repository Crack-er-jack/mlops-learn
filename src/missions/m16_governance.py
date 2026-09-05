"""
MLOpsHub: Production Quest - Mission 16: Model Governance & Model Card

Role: ML Lead / Governance Officer
Desk: Executive product desk with compliance binders, audit logs, and sign-off stamps.
Teaches: ML Model Cards, institutional accountability, intended vs prohibited use, auditability.
"""

import streamlit as st
from src.missions.base_mission import BaseMission
from src.theme import render_neon_card, render_terminal


class Mission16(BaseMission):
    """Mission 16 Implementation."""

    def __init__(self) -> None:
        super().__init__(
            mission_id="m16",
            number_str="16",
            title="Model Governance & Model Card",
            role_name="ML Lead",
            role_emoji="📋",
            desk_desc="Executive governance office with compliance charters, signed approval forms, and model card registers.",
            badge_name="Governance Leader",
            xp_award=130
        )

    def render(self) -> None:
        """Render Mission 16 UI components."""
        story = (
            "**Pre-Deployment Executive Review**<br>"
            "Vice President of Engineering Jordan calls the team: *'We have versioned data, tracked experiments, "
            "automated CI/CD, and tested fairness. But our legal, enterprise compliance, and risk teams are asking: "
            "Who owns this model? What are its known failure modes? What data trained it? What is its prohibited use?'*<br>"
            "Governance is not bureaucracy for bureaucracy's sake. It creates institutional accountability."
        )
        objective = (
            "Review and sign off on the official **ML Model Card** for ChurnGuard v3. "
            "Verify intended use cases, documented limitations, ethical considerations, and stakeholder sign-offs."
        )
        self.render_standard_header(story, objective)

        self.render_instructor_notes(
            objective="Teach the essential components of Model Cards (Mitchell et al.) and why ML governance is critical for enterprise safety.",
            talking_points=[
                "Model Cards are nutrition labels for AI models: They specify what ingredients went in, intended use cases, and toxic side-effects.",
                "Intended Use vs Prohibited Use: ChurnGuard is intended to prioritize customer success outreach; it is prohibited from being used to deny contract cancellations or automate punitive billing.",
                "Known Limitations: Every model has blind spots (e.g. accounts with < 14 days of history lack sufficient telemetry)."
            ],
            questions=[
                "If a marketing intern uses ChurnGuard to automatically cancel customer subscriptions without consent, whose fault is it?",
                "Why should business stakeholders (Product Manager, Legal) sign off on a Model Card alongside the ML Engineer?"
            ],
            expected_answers=[
                "The organization's! Clear prohibited use guidelines in the Model Card legally constrain unauthorized automation.",
                "To ensure shared accountability across engineering, business viability, and ethical compliance."
            ],
            misconceptions=[
                "Thinking Model Cards are only for external public relations.",
                "Assuming ML governance slows down development rather than preventing existential compliance lawsuits."
            ],
            deep_dive="Review the Google / Hugging Face Model Card standard schema.",
            skip_tip="Review the 4 sections of the ChurnGuard Model Card and click 'Sign Off & Approve'."
        )

        # Panel 4: Learn
        learn_html = """
        <b>The 5 Sections of a Production Model Card:</b><br>
        1. <b>Model Details:</b> Version, architecture, owners, release date.<br>
        2. <b>Intended Use:</b> Primary user personas and authorized operational contexts.<br>
        3. <b>Prohibited Use:</b> Explicit restrictions (no autonomous billing actions, no credit scoring).<br>
        4. <b>Training & Evaluation Data:</b> Exact DVC hashes, sample distributions, and slices.<br>
        5. <b>Quantitative Performance & Limitations:</b> Benchmark metrics, latency SLAs, and known edge-case failures.
        """
        render_neon_card("4. LEARN: WHAT IS AN ML MODEL CARD?", learn_html, color_variant="purple")

        # Panel 5: Do
        st.markdown("#### 5. DO: Review Official ChurnGuard v3 Model Card")

        model_card_html = """
        <div style="background: #111827; border: 2px solid #58a6ff; border-radius: 12px; padding: 18px; line-height: 1.6;">
            <div style="font-size: 1.25rem; font-weight: 800; color: #58a6ff; margin-bottom: 8px;">
                📄 MODEL CARD: ChurnGuard v3.0 (Production Candidate)
            </div>
            <p><b>Model Developer:</b> NEONBYTE Machine Learning Platform Team (Sarah, Alex, Marcus)</p>
            <p><b>Model Type:</b> Gradient Boosting Classifier (scikit-learn 1.4.0) | <b>Inference Latency:</b> 18.2ms</p>
            <hr style="border-color: #374151;">
            <p><b>🎯 Intended Use:</b> Identification of B2B SaaS accounts at imminent risk of non-renewal to guide human customer success outreach.</p>
            <p><b>🚫 Prohibited Use:</b> Autonomous billing adjustments, automated customer denial-of-service, or repurposing as a creditworthiness score.</p>
            <hr style="border-color: #374151;">
            <p><b>📊 Training Data Lineage:</b> <code>data/churn_v3_prod.csv</code> (DVC MD5: <code>c0d3e4fa6b78</code> | 1,200 validated customer records)</p>
            <p><b>📈 Benchmark Performance:</b> F1 Score: <b>0.818</b> | ROC-AUC: <b>0.884</b> | Precision: <b>0.835</b> | Recall: <b>0.802</b></p>
            <p><b>⚠️ Known Limitations:</b> Accuracy degrades on accounts with tenure &lt; 30 days due to sparse telemetry; does not account for macro market price wars.</p>
            <hr style="border-color: #374151;">
            <p><b>⚖️ Ethical & Fairness Audit:</b> Evaluated across 4 geographical regions; satisfies 4/5ths Disparate Impact rule following threshold calibration.</p>
        </div>
        """
        st.markdown(model_card_html, unsafe_allow_html=True)

        st.markdown("##### ✍️ Governance Sign-off & Audit Seal:")
        c1, c2, c3 = st.columns(3)
        s1 = c1.checkbox("✅ ML Lead Approval (Alex)")
        s2 = c2.checkbox("✅ Product Lead Approval (Maya)")
        s3 = c3.checkbox("✅ Responsible AI Seal (Elena)")

        if s1 and s2 and s3:
            st.success("🎉 **ALL GOVERNANCE CRITERIA APPROVED!** ChurnGuard v3 is cleared for mission-critical enterprise operations.")

        # Panel 6: Under the Hood
        if st.session_state.get("show_code", True):
            st.markdown("#### 6. UNDER THE HOOD: Automated Model Card Generator")
            code_str = (
                "from model_card_toolkit import ModelCardToolkit\n\n"
                "mct = ModelCardToolkit(output_dir='reports/model_cards')\n"
                "card = mct.scaffold_assets()\n"
                "card.model_details.name = 'ChurnGuard v3'\n"
                "card.model_details.version.name = 'v3.0'\n"
                "card.model_parameters.model_architecture = 'GradientBoostingClassifier'\n"
                "card.quantitative_analysis.performance_metrics = [{'f1_score': 0.818}]\n"
                "mct.update_model_card(card)\n"
                "mct.export_format(card, 'model_card.html')"
            )
            st.code(code_str, language="python")

        # Panel 7: Result
        render_neon_card(
            "7. RESULT",
            "Model Card generated, signed, and stamped. Complete governance record published to the compliance archive with immutable hashes.",
            color_variant="green"
        )

        # Panel 8: Why This Matters
        render_neon_card(
            "8. WHY THIS MATTERS",
            "<b>Accountability enables trust.</b> If an incident occurs, governance records provide the definitive baseline of what the system was tested to do and where its limits lie.",
            color_variant="cyan"
        )

        # Panel 9: Next
        st.info("🔜 **Next Mission:** Everything is running smoothly in production... until three weeks later, when an upstream change is deployed. The system begins to shift.")
        self.render_navigation_footer()

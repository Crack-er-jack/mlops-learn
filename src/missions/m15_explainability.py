"""
MLOpsHub: Production Quest - Mission 15: Model Explainability (Attribution)

Role: Data Scientist
Desk: Machine learning interpretability workstation with waterfall contribution charts.
Teaches: Local vs Global explainability, SHAP-style attribution, feature contributions, explanation vs causation.
"""

import streamlit as st
import pandas as pd
from src.missions.base_mission import BaseMission
from src.models.explainability import calculate_local_attribution
from src.theme import render_neon_card, render_terminal


class Mission15(BaseMission):
    """Mission 15 Implementation."""

    def __init__(self) -> None:
        super().__init__(
            mission_id="m15",
            number_str="15",
            title="Model Explainability (Attribution)",
            role_name="Data Scientist",
            role_emoji="🔍",
            desk_desc="Explainability lab with SHAP waterfall plots, feature importance rankings, and local interpretability cards.",
            badge_name="Explainability Expert",
            xp_award=130
        )

    def render(self) -> None:
        """Render Mission 15 UI components."""
        story = (
            "**Customer Success Review**<br>"
            "Customer Account Manager David calls Sarah: *'Customer #2048 (Acme Corp) was flagged as an 82% churn risk. "
            "Our account executive wants to reach out, but they need to know WHY. Did they have bad support tickets? "
            "Is the price too high? We can't offer an effective retention strategy without understanding the model's reasoning!'*<br>"
            "Black-box predictions are not actionable. You need local feature attribution."
        )
        objective = (
            "Deconstruct an individual churn prediction into additive feature contributions. "
            "Distinguish between Global Feature Importance and Local SHAP-style attribution. "
            "Learn why feature explanation does not imply real-world causation."
        )
        self.render_standard_header(story, objective)

        self.render_instructor_notes(
            objective="Demystify how black-box ML models arrive at specific individual decisions using additive feature attribution.",
            talking_points=[
                "Global Explainability: 'Across 10,000 customers, what features are generally most predictive?' (e.g. support_calls and contract_type).",
                "Local Explainability: 'For this specific person (Customer #2048), which exact features pushed their risk from 28% baseline up to 82%?'",
                "SHAP (SHapley Additive exPlanations): Grounded in cooperative game theory to fairly distribute prediction payoffs to features.",
                "Explanation != Causation: High support calls correlate with churn, but support calls don't 'cause' churn—poor software quality causes both!"
            ],
            questions=[
                "Why can't an account executive make a retention call with only an 82% probability number?",
                "If 'high support calls' increases churn risk, should we solve churn by turning off customer phone support?"
            ],
            expected_answers=[
                "They don't know whether to offer a discount, technical assistance, or an extended contract without feature explanations.",
                "Of course not! That confuses statistical correlation with real-world causation."
            ],
            misconceptions=[
                "Assuming explainability techniques prove causality.",
                "Thinking neural networks or ensemble models are forever unexplainable black boxes."
            ],
            deep_dive="Explain how TreeSHAP calculates exact Shapley values in polynomial time for decision tree ensembles.",
            skip_tip="Inspect Customer #2048's waterfall breakdown below."
        )

        # Panel 4: Learn
        learn_html = r"""
        <b>Global vs Local Interpretability:</b><br>
        • <b>Global:</b> Macro-level feature importance ranking across the entire population.<br>
        • <b>Local (SHAP):</b> Micro-level attribution for a single inference instance:
          $$\hat{y}(x) = \phi_0 + \sum_{i=1}^M \phi_i(x)$$
          where $\phi_0$ is baseline probability and $\phi_i$ is feature $i$'s positive or negative push.
        """
        render_neon_card("4. LEARN: LOCAL VS GLOBAL EXPLAINABILITY", learn_html, color_variant="purple")

        # Panel 5: Do
        st.markdown("#### 5. DO: Deconstruct Customer #2048's Churn Prediction")

        col_cust, col_pred = st.columns([2, 1])
        with col_cust:
            st.markdown("**Customer #2048 Profile:**")
            st.markdown("- **Tenure:** `6 months` (New customer)")
            st.markdown("- **Monthly Spend:** `$145.00` (High billing)")
            st.markdown("- **Support Calls (90d):** `5 calls` (Frustrated)")
            st.markdown("- **Contract:** `Month-to-month`")
            st.markdown("- **Usage:** `18 logins/week`")

        with col_pred:
            st.metric("Base Population Risk", "28.0%")
            st.metric("Customer #2048 Churn Risk", "82.0%", delta="+54.0% Risk", delta_color="inverse")

        st.markdown("##### 🔍 Local Feature Contributions Breakdown (SHAP Waterfall):")
        sample_cust = {
            "monthly_spend": 145.0,
            "support_calls": 5,
            "tenure": 6,
            "usage_frequency": 18,
            "contract_type": "Month-to-month"
        }
        contributions = calculate_local_attribution(sample_cust)

        st.dataframe(pd.DataFrame(contributions), use_container_width=True)

        st.info("💡 **Actionable Retention Strategy for Customer Success:** Reach out proactively to resolve open technical tickets (support calls = +0.255) and offer an annual contract discount (contract = +0.145) to secure retention!")

        # Real-World Perspectives
        self.render_perspectives(
            business_pov=(
                "<b>The 'Right to Explanation' & Customer Adoption:</b> Under GDPR Article 22, EU consumers "
                "have a legal right to meaningful information about the logic behind automated decisions. "
                "In enterprise software, customer success representatives refuse to use AI recommendations "
                "unless they can explain 'why' to a client: an unexplained churn probability breeds distrust and rejection."
            ),
            technical_pov=(
                r"<b>Game-Theoretic Shapley Attribution:</b> SHAP calculates the marginal contribution of feature $i$ "
                r"averaged over all possible feature subsets $S \subseteq F \setminus \{i\}$. It is the ONLY attribution "
                r"method that simultaneously satisfies 4 mathematical axioms: Efficiency (contributions sum to difference from base value), "
                r"Symmetry (identical features get equal attribution), Dummy (zero-impact features receive zero attribution), "
                r"and Additivity."
            ),
            real_world_case=(
                "When Apple Card launched, co-founder Steve Wozniak reported that he was offered 10x the credit limit "
                "of his wife despite identical assets. Goldman Sachs customer service couldn't explain the decision "
                "because the algorithmic model lacked explainability tooling, triggering a state regulatory probe."
            )
        )

        # Panel 6: Under the Hood
        if st.session_state.get("show_code", True):
            st.markdown("#### 6. UNDER THE HOOD: Production SHAP Explainability Engine")
            tab_waterfall, tab_global, tab_api = st.tabs([
                "🌊 Local Waterfall Plot (Single Customer)",
                "🐝 Global Summary & Beeswarm Plot",
                "⚡ Production REST API JSON Explanation"
            ])

            with tab_waterfall:
                st.code("""import shap

# 1. Initialize TreeExplainer on tree ensemble or LinearExplainer on Logistic Regression
explainer = shap.TreeExplainer(model=churnguard_model)

# 2. Compute local Shapley values for specific customer instance
shap_values = explainer(X_customer_2048)

# 3. Generate visual waterfall plot
shap.plots.waterfall(shap_values[0], max_display=7)

# Print base expectation and additive feature pushes
print(f"Base Value E[f(x)]: {explainer.expected_value:.3f}")
for name, val in zip(feature_names, shap_values[0].values):
    print(f"{name:25} -> Contribution: {val:+.3f}")""", language="python")

            with tab_global:
                st.code("""# Global Feature Importance across entire test population (N=10,000)
shap_population = explainer(X_test)

# Summary plot shows both magnitude and direction of feature effects
shap.plots.beeswarm(shap_population)

# Bar chart of mean absolute Shapley values (Global Ranking)
shap.plots.bar(shap_population)""", language="python")

            with tab_api:
                st.code("""# Production FastAPI serving with JSON explanation payload
@app.post("/v1/predict-with-explanation")
def predict_with_explanation(cust: CustomerPayload):
    features = cust.to_array()
    prob = float(model.predict_proba(features)[0, 1])
    shap_vals = explainer(features)[0].values

    top_drivers = sorted(
        [{"feature": f, "impact": round(float(v), 3)} for f, v in zip(feature_names, shap_vals)],
        key=lambda x: abs(x["impact"]),
        reverse=True
    )[:4]

    return {
        "churn_probability": prob,
        "risk_category": "HIGH" if prob > 0.5 else "LOW",
        "baseline_probability": float(explainer.expected_value),
        "primary_drivers": top_drivers
    }""", language="python")

        # Panel 7: Result
        render_neon_card(
            "7. RESULT",
            "Customer #2048's 82% churn probability is fully explained: High support calls (+0.255) and month-to-month contract (+0.145) were the top drivers.",
            color_variant="green"
        )

        # Panel 8: Why This Matters
        render_neon_card(
            "8. WHY THIS MATTERS",
            "<b>Predictions without explanations are rarely adopted by human operators.</b> Local attribution empowers front-line teams to take targeted, empathetic, and effective action.",
            color_variant="cyan"
        )

        # Panel 9: Next
        st.info("🔜 **Next Mission:** Before deploying models into customer-facing operations, how do we document their purpose, limitations, and approvals? Enter Governance & Model Cards.")
        self.render_navigation_footer()

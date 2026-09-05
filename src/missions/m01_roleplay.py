"""
MLOpsHub: Production Quest - Mission 01: Meet the Team & Problem Formulation

Role: Data Analyst
Desk: Analyst desk with laptop, spreadsheet, warm coffee, sticky notes, charts.
Teaches: Business problem formulation, training vs. inference, features vs. labels, data quality.
"""

import streamlit as st
import pandas as pd
from src.data.generator import generate_clean_dataset
from src.missions.base_mission import BaseMission
from src.theme import render_neon_card, render_terminal


class Mission01(BaseMission):
    """Mission 01 Implementation."""

    def __init__(self) -> None:
        super().__init__(
            mission_id="m01",
            number_str="01",
            title="Meet the Team & Problem Formulation",
            role_name="Data Analyst",
            role_emoji="📊",
            desk_desc="Analyst desk with dual monitors, spreadsheet tabs, warm mug of coffee, sticky notes, and customer churn charts.",
            badge_name="Data Steward",
            xp_award=100
        )

    def render(self) -> None:
        """Render Mission 01 UI components and interactive exploration."""
        story = (
            "**Monday, 9:12 AM at NEONBYTE HQ**<br>"
            "CEO Maya walks over to your desk: *'Customer churn is killing our SaaS growth. "
            "Leadership wants an AI solution called **ChurnGuard** to predict who will cancel "
            "before they leave. Before the data science team trains a single model, we need YOU "
            "to explore our raw customer telemetry and formulate the exact ML problem.'*"
        )
        objective = (
            "Formulate the business problem into a valid supervised ML task. "
            "Inspect raw customer features, identify the prediction target, and evaluate class balance."
        )
        self.render_standard_header(story, objective)

        # Instructor Guide
        self.render_instructor_notes(
            objective="Transition students from a vague business request to a rigorous ML problem formulation.",
            talking_points=[
                "Most failed ML projects fail in problem formulation, not algorithm selection.",
                "Distinguish between Supervised vs. Unsupervised vs. Heuristic approaches.",
                "Discuss Target Leakage: What data is known at prediction time versus after churn happens?"
            ],
            questions=[
                "Why can't we include 'cancellation_survey_response' as a feature to predict churn?",
                "What is the cost of a False Positive (offering discount to a happy user) vs False Negative (losing a customer)?"
            ],
            expected_answers=[
                "Cancellation survey is collected AFTER churn has already occurred (Target Leakage).",
                "False negatives directly cost customer lifetime value (LTV); False positives cost margin on unnecessary discounts."
            ],
            misconceptions=[
                "Students think ML starts with `model.fit()`. It starts with understanding data and business context.",
                "Assuming 90% accuracy is great when 95% of customers don't churn (class imbalance trap)."
            ],
            deep_dive="Explain how training data features must reflect the exact information available at the inference timestamp.",
            skip_tip="Spend 2 minutes exploring the data preview table and observing the 8 features."
        )

        # Panel 4: Learn
        learn_content = r"""
        <b>Supervised Classification Formulation:</b><br>
        • <b>Features ($X$):</b> Observable customer behaviors available prior to decision point (age, tenure, monthly_spend, support_calls).<br>
        • <b>Target ($y$):</b> Binary ground truth outcome (<code>churn = 1</code> if customer cancelled within 30 days, <code>0</code> otherwise).<br>
        • <b>Inference Objective:</b> Produce calibrated probability $\hat{p} = P(churn = 1 \mid X)$ to trigger retention workflows.
        """
        render_neon_card("4. LEARN: ML PROBLEM FORMULATION", learn_content, color_variant="purple")

        # Panel 5: Do
        st.markdown("#### 5. DO: Inspect Raw Customer Telemetry")
        df = generate_clean_dataset(n_samples=500, random_state=42)

        col1, col2 = st.columns([3, 1])
        with col1:
            st.dataframe(df.head(6), use_container_width=True)
        with col2:
            st.metric("Total Records", len(df))
            churn_rate = df["churn"].mean() * 100
            st.metric("Churn Base Rate", f"{churn_rate:.1f}%")
            st.metric("Features Count", len(df.columns) - 2)

        selected_feature = st.selectbox(
            "Select a feature to inspect distribution vs Churn:",
            ["monthly_spend", "support_calls", "tenure", "usage_frequency", "contract_type"]
        )
        if selected_feature:
            avg_by_churn = df.groupby("churn")[selected_feature].mean() if df[selected_feature].dtype != 'object' else df.groupby("churn")[selected_feature].value_counts(normalize=True)
            st.caption(f"Average {selected_feature} grouped by churn outcome (0 = Stayed, 1 = Churned):")
            st.write(avg_by_churn)

        # Panel 6: Under the Hood
        if st.session_state.get("show_code", True):
            st.markdown("#### 6. UNDER THE HOOD: EDA Script")
            code_snippet = (
                "import pandas as pd\n\n"
                "# Load raw telemetry dataset\n"
                "df = pd.read_csv('data/raw_telemetry.csv')\n\n"
                "# Inspect column data types and missing values\n"
                "print(df.info())\n"
                "print(df['churn'].value_counts(normalize=True))\n"
                "print(df.groupby('churn')[['monthly_spend', 'support_calls', 'tenure']].mean())"
            )
            st.code(code_snippet, language="python")

        if st.session_state.get("show_terminal", True):
            render_terminal("python -m src.data.inspect_telemetry", f"[SUCCESS] 500 rows loaded. Target balance: 74.2% Active, 25.8% Churned.\nIdentified 8 predictive features. Zero target leakage detected.")

        # Panel 7: Result
        render_neon_card(
            "7. RESULT",
            "✅ Telemetry verified. Clear separation observed: Churners exhibit higher support calls (>3.2) and lower tenure (<14 months). Supervised classification formulation is viable.",
            color_variant="green"
        )

        # Panel 8: Why This Matters
        render_neon_card(
            "8. WHY THIS MATTERS",
            "Defining features and target boundaries clearly prevents <b>Target Leakage</b>—a catastrophic error where future information leaks into training data, yielding 99% test accuracy but 0% real-world utility.",
            color_variant="cyan"
        )

        # Panel 9: Next
        st.info("🔜 **Next Mission:** The data engineering team just sent over the full production dump... but it has severe quality issues! Time to clean and validate the data.")
        self.render_navigation_footer()

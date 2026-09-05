"""
MLOpsHub: Production Quest - Mission 02: Understand & Clean the Data

Role: Data Analyst
Desk: Analyst desk with spreadsheet tabs and data quality checklist.
Teaches: Data quality, missing values, duplicates, negative values, automated validation checks.
"""

import streamlit as st
import pandas as pd
from src.data.generator import generate_dirty_dataset
from src.missions.base_mission import BaseMission
from src.theme import render_neon_card, render_terminal


class Mission02(BaseMission):
    """Mission 02 Implementation."""

    def __init__(self) -> None:
        super().__init__(
            mission_id="m02",
            number_str="02",
            title="Understand & Clean the Data",
            role_name="Data Analyst",
            role_emoji="🧹",
            desk_desc="Analyst workstation with data validation spreadsheets, red pen annotations, and coffee mug.",
            badge_name="Data Quality Champion",
            xp_award=120
        )

    def render(self) -> None:
        """Render Mission 02 UI components."""
        story = (
            "**Monday, 11:30 AM**<br>"
            "The data engineering pipeline delivered an initial export of 1,200 customer accounts. "
            "However, an automated alert didn't fire, and the export looks messy! "
            "You spot missing ages, duplicate rows, and impossible values like <code>monthly_spend = -$2,300.00</code>! "
            "If the data scientists train on this, the baseline model will be tainted."
        )
        objective = (
            "Identify data anomalies: missing values, duplicate records, negative billing spends, "
            "and inconsistent categorical casing. Run automated sanitization and establish data validation gates."
        )
        self.render_standard_header(story, objective)

        self.render_instructor_notes(
            objective="Demonstrate that raw data is inherently imperfect and automated validation is the first defense in MLOps.",
            talking_points=[
                "Silent failures: Scikit-learn will crash on NaNs, but it will silently learn from negative values like -$2300!",
                "Manual cleaning vs automated validation scripts (Great Expectations, Pydantic, Pytest).",
                "How dirty data pollutes downstream feature stores and model predictions."
            ],
            questions=[
                "What would happen if a customer had a monthly_spend of -$2,300 in a linear model with positive coefficient?",
                "Should we drop rows with missing values or impute them? What are the tradeoffs?"
            ],
            expected_answers=[
                "A negative spend would invert the prediction, predicting extreme retention when the user is actually anomalous.",
                "Dropping loses statistical power; imputation preserves sample size but can distort feature variance."
            ],
            misconceptions=[
                "Believing that modern neural networks or gradient boosters automatically handle bad or nonsensical data.",
                "Thinking data cleaning is a one-time notebook manual process instead of a repeatable pipeline."
            ],
            deep_dive="Explain Data Contracts: Formal agreements between data producers and ML consumers.",
            skip_tip="Click 'Execute Automated Data Cleaning' and examine before/after statistics."
        )

        # Panel 4: Learn
        learn_html = (
            "<strong>Core Data Hygiene Dimensions:</strong><br><br>"
            "1. <strong>Completeness:</strong> Missing/null values in key numerical features (age, spend).<br>"
            "2. <strong>Validity:</strong> Domain constraints (monthly_spend &ge; 0, 18 &le; age &le; 100).<br>"
            "3. <strong>Uniqueness:</strong> Duplicate customer IDs inflating sample weight.<br>"
            "4. <strong>Consistency:</strong> Categorical casing normalization ('month-to-month' vs 'Month-to-month')."
        )
        render_neon_card("4. LEARN: DATA VALIDATION DIMENSIONS", learn_html, color_variant="purple")

        # Panel 5: Do
        st.markdown("#### 5. DO: Inspect and Sanitize Tainted Data")
        df_dirty = generate_dirty_dataset(n_samples=600, random_state=42)

        col1, col2, col3, col4 = st.columns(4)
        null_count = int(df_dirty["age"].isnull().sum() + df_dirty["monthly_spend"].isnull().sum())
        dup_count = int(df_dirty.duplicated().sum())
        neg_count = int((df_dirty["monthly_spend"] < 0).sum())
        casing_count = int((df_dirty["contract_type"] == "month-to-month").sum())

        col1.metric("Missing Values", null_count, delta="Defect", delta_color="inverse")
        col2.metric("Duplicate Rows", dup_count, delta="Defect", delta_color="inverse")
        col3.metric("Negative Spends", neg_count, delta="Defect", delta_color="inverse")
        col4.metric("Casing Mismatches", casing_count, delta="Defect", delta_color="inverse")

        # Filter button
        clean_applied = st.button("✨ Run Automated Data Sanitization Pipeline", type="primary")

        if clean_applied:
            # Clean dataframe
            df_cleaned = df_dirty.copy()
            df_cleaned.drop_duplicates(inplace=True)
            df_cleaned["age"] = df_cleaned["age"].fillna(df_cleaned["age"].median())
            df_cleaned["monthly_spend"] = df_cleaned["monthly_spend"].apply(lambda x: abs(x) if pd.notnull(x) else df_cleaned["monthly_spend"].median())
            df_cleaned["contract_type"] = df_cleaned["contract_type"].str.capitalize()
            st.success("✅ Sanitization pipeline executed! 0 nulls, 0 duplicates, all spends positive, categorical strings normalized.")
            st.dataframe(df_cleaned.head(5), use_container_width=True)

        # Panel 6: Under the Hood
        if st.session_state.get("show_code", True):
            st.markdown("#### 6. UNDER THE HOOD: Data Sanitization Script")
            code_str = (
                "# Automated validation & sanitization\n"
                "df.drop_duplicates(inplace=True)\n"
                "df['age'] = df['age'].fillna(df['age'].median())\n"
                "df = df[df['monthly_spend'] >= 0]  # Filter out corrupt negative values\n"
                "df['contract_type'] = df['contract_type'].str.capitalize()\n\n"
                "# Validation assertions (Data Contracts)\n"
                "assert df['age'].between(18, 100).all(), 'Age out of reasonable bounds!'\n"
                "assert (df['monthly_spend'] >= 0).all(), 'Found negative monthly spend!'\n"
                "assert df['contract_type'].isin(['Month-to-month', 'One-year', 'Two-year']).all()"
            )
            st.code(code_str, language="python")

        if st.session_state.get("show_terminal", True):
            render_terminal(
                "pytest tests/test_data_quality.py",
                "tests/test_data_quality.py::test_null_bounds PASSED [ 33%]\n"
                "tests/test_data_quality.py::test_non_negative_spend PASSED [ 66%]\n"
                "tests/test_data_quality.py::test_categorical_contract PASSED [100%]\n"
                "======================== 3 passed in 0.42s ========================"
            )

        # Panel 7: Result
        render_neon_card(
            "7. RESULT",
            "Dataset v2.0-cleaned created. 100% rows validated against data contract schema. Zero negative spends, zero missing values.",
            color_variant="green"
        )

        # Panel 8: Why This Matters
        render_neon_card(
            "8. WHY THIS MATTERS",
            "ML models lack common sense. They don't know that spend cannot be negative or age cannot be 250. <b>Data testing prevents silent corruption before training begins.</b>",
            color_variant="cyan"
        )

        # Panel 9: Next
        st.info("🔜 **Next Mission:** Hand off clean data to Sarah, our Data Scientist, to train the first baseline churn prediction model!")
        self.render_navigation_footer()

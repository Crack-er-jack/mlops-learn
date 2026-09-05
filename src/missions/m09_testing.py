"""
MLOpsHub: Production Quest - Mission 09: Test the Pipeline (Pytest)

Role: ML Engineer
Desk: Engineering desk with test status lights, assertion specs, and terminal panels.
Teaches: ML test taxonomy (Unit, Data, Model, Integration), Pytest gates, intentional failures.
"""

import streamlit as st
from src.missions.base_mission import BaseMission
from src.testing.test_suite import MLTestSuite
from src.theme import render_neon_card, render_terminal


class Mission09(BaseMission):
    """Mission 09 Implementation."""

    def __init__(self) -> None:
        super().__init__(
            mission_id="m09",
            number_str="09",
            title="Test the Pipeline (Pytest)",
            role_name="ML Engineer",
            role_emoji="🧪",
            desk_desc="Automated test station with green and red LED indicator beacons and assertion test specs.",
            badge_name="Pipeline Tester",
            xp_award=130
        )

    def render(self) -> None:
        """Render Mission 09 UI components."""
        story = (
            "**Tuesday, 1:40 PM**<br>"
            "Alex is preparing the automated deployment pipeline. A junior developer opens a PR "
            "that changes a preprocessing normalization formula. Sarah asks: *'Are we sure this didn't break "
            "our feature pipeline? Did anyone test if the model still achieves 0.75 F1?'*<br>"
            "In traditional software, we test logic (`assert add(2, 2) == 4`). "
            "In MLOps, we must test **Code**, **Data**, **Model Quality**, and **End-to-End Integration**."
        )
        objective = (
            "Execute an automated ML test suite using Pytest. "
            "Evaluate unit tests, data contract checks, and model threshold gates. "
            "Experience an intentional failure when bad data attempts to slip through."
        )
        self.render_standard_header(story, objective)

        self.render_instructor_notes(
            objective="Deconstruct the 4 layers of testing in ML systems and emphasize that code tests alone are inadequate.",
            talking_points=[
                "Why ML systems fail silently: A compiler catches syntax errors; an ML pipeline can run to completion with 0 errors while producing gibberish predictions.",
                "Data Tests: Assertions on distributions, null counts, value ranges (e.g. spend >= 0).",
                "Model Tests: Minimum performance gates (assert F1 >= 0.75) and latency boundaries (assert latency < 50ms).",
                "Integration Tests: Ensuring the serializable artifact loads and returns valid probabilities on a test customer payload."
            ],
            questions=[
                "If our code compiles and has 100% test coverage, can our ML model still fail in production? Why?",
                "What is the difference between a unit test in standard software and a model quality test?"
            ],
            expected_answers=[
                "Yes! The code can execute perfectly on corrupt data, or the model might severely underperform due to bad weights or shifted data.",
                "Software unit tests check deterministic logic; model quality tests check statistical performance on held-out data."
            ],
            misconceptions=[
                "Believing Pytest is only for web servers and cannot be used for machine learning.",
                "Thinking that passing unit tests means the model is safe to deploy."
            ],
            deep_dive="Explain how Great Expectations and Pytest complement each other in production CI pipelines.",
            skip_tip="Toggle 'Inject Corrupted Data' and run the test suite to observe the simulated failure."
        )

        # Panel 4: Learn
        learn_html = r"""
        <b>The 4 Pillars of ML Testing:</b><br>
        1. <b>Unit Tests:</b> Feature transformation functions, one-hot encoders, imputation logic.<br>
        2. <b>Data Tests:</b> Value ranges ($spend \ge 0$), column existence, schema typing, zero nulls.<br>
        3. <b>Model Quality Tests:</b> Minimum performance bars (e.g. $F1 \ge 0.70$, $Latency \le 50ms$).<br>
        4. <b>Integration Tests:</b> End-to-end payload inference through serialization/deserialization.
        """
        render_neon_card("4. LEARN: THE 4 PILLARS OF ML TESTING", learn_html, color_variant="purple")

        # Panel 5: Do
        st.markdown("#### 5. DO: Execute Automated ML Test Suite")

        st.markdown("##### ⚙️ Interactive Pytest Lab")
        st.info("💡 **Mission:** Type `pytest tests/` to run the automated machine learning test suite.")
        inject_corruption = st.checkbox("⚠️ Deliberately Inject Corrupted Data (Negative spend -$2300, null ages)")
        
        test_cmd = st.text_input("Terminal Input:", placeholder="e.g. pytest tests/", key="pytest_lab_cmd")

        if st.button("▶️ Execute Command", type="primary"):
            test_cmd = test_cmd.strip()
            if "pytest" in test_cmd:
                all_passed, results, terminal_out = MLTestSuite.run_all_tests(use_corrupted_data=inject_corruption)

                # Show results cards
                st.markdown("**Test Suite Results:**")
                cols = st.columns(len(results))
                for i, r in enumerate(results):
                    status_icon = "✅ PASS" if r["passed"] else "❌ FAIL"
                    cols[i].metric(r["name"][:18] + "..", status_icon)

                if not all_passed:
                    st.error("🚨 **TEST SUITE FAILED!** Quality gate breached. Automated deployment blocked!")
                else:
                    st.success("🎉 **ALL TESTS PASSED!** Code, Data, Model, and Pipeline meet production criteria.")

                render_terminal(test_cmd, terminal_out)
            else:
                render_terminal(test_cmd, "Command not recognized. Try typing 'pytest tests/' to execute the test suite.")
        else:
            render_terminal("pytest tests/ -v", "pytest suite ready. Enter 'pytest tests/' to execute.")

        # Real-World Perspectives
        self.render_perspectives(
            business_pov=(
                "<b>Preventing Disastrous Silent Regressions:</b> Unlike web apps where bugs cause 404/500 crashes "
                "that immediately alert on-call engineers, machine learning bugs fail silently. A broken preprocessing formula "
                "or inverted sign will cause a model to output plausible-looking numbers with zero server errors, quietly "
                "costing millions in misclassified churners or fraudulent transactions before anyone realizes."
            ),
            technical_pov=(
                r"<b>The 4-Layer Testing Pyramid for ML:</b> Traditional software testing checks deterministic inputs "
                r"against deterministic outputs (`assert f(2) == 4`). ML testing requires: 1. Unit tests for deterministic "
                r"preprocessors, 2. Data contract tests using Great Expectations, 3. Model regression tests asserting "
                r"statistical metrics ($F1 \ge 0.75$, inference latency $\le 50ms$), and 4. Pipeline integration tests."
            ),
            real_world_case=(
                "Zillow's algorithmic home-buying business (Zillow Offers) was shut down in 2021 with a $500 million write-down "
                "and a 25% workforce layoff because their automated valuation models failed to test for shifting volatility "
                "and market dynamics, buying thousands of homes for far more than they could be sold for."
            )
        )

        # Panel 6: Under the Hood
        if st.session_state.get("show_code", True):
            st.markdown("#### 6. UNDER THE HOOD: Production ML Pytest & Great Expectations Arsenal")
            tab_pytest_code, tab_ge_code, tab_fixtures = st.tabs([
                "🧪 tests/test_model_pipeline.py",
                "📋 Great Expectations Data Contract",
                "🔧 conftest.py (Pytest Fixtures)"
            ])

            with tab_pytest_code:
                st.code("""import pytest
from src.models.trainer import ChurnModelTrainer
from src.data.generator import generate_clean_dataset

# 1. Data Contract Assertion Test
def test_data_non_negative_spend(clean_data):
    assert (clean_data['monthly_spend'] >= 0).all(), "Negative monthly spend detected!"

# 2. Performance Quality Gate Assertion
def test_model_minimum_f1_threshold(clean_data):
    trainer = ChurnModelTrainer(random_state=42)
    metrics = trainer.train_and_evaluate(clean_data)
    assert metrics['f1'] >= 0.75, f"Model F1 {metrics['f1']} below 0.75 threshold!"

# 3. Latency SLA Assertion (<50ms per customer)
def test_inference_latency_sla(clean_data):
    import time
    trainer = ChurnModelTrainer(random_state=42)
    trainer.train_and_evaluate(clean_data)
    sample = clean_data.iloc[0].to_dict()
    
    start = time.perf_counter()
    trainer.predict_single(sample)
    duration_ms = (time.perf_counter() - start) * 1000
    assert duration_ms < 50.0, f"Latency SLA violated: {duration_ms:.2f}ms > 50ms" """, language="python")

            with tab_ge_code:
                st.code("""import great_expectations as ge

# Declarative Great Expectations Suite
ge_df = ge.from_pandas(clean_data)

# Enforce Schema & Domain Boundaries
ge_df.expect_column_values_to_be_between("age", min_value=18, max_value=100)
ge_df.expect_column_values_to_be_between("monthly_spend", min_value=0.0, max_value=500.0)
ge_df.expect_column_values_to_not_be_null("customer_id")
ge_df.expect_column_values_to_be_in_set(
    "contract_type",
    ["Month-to-month", "One-year", "Two-year"]
)

validation_result = ge_df.validate()
assert validation_result.success, "Data contract validation failed!" """, language="python")

            with tab_fixtures:
                st.code("""# conftest.py - Shared Test Fixtures
import pytest
from src.data.generator import generate_clean_dataset

@pytest.fixture(scope="session")
def clean_data():
    \"\"\"Produce deterministic benchmark data fixture for testing.\"\"\"
    return generate_clean_dataset(n_samples=1000, random_state=42)""", language="python")

        # Panel 7: Result
        render_neon_card(
            "7. RESULT",
            "When negative spends are injected, the data test immediately catches the defect and halts the pipeline before any corrupted weights can be trained or promoted.",
            color_variant="green"
        )

        # Panel 8: Why This Matters
        render_neon_card(
            "8. WHY THIS MATTERS",
            "<b>Automated testing is the foundation of continuous delivery.</b> Without automated tests, every model deployment is an uncontrolled gamble with production users.",
            color_variant="cyan"
        )

        # Panel 9: Next
        st.info("🔜 **Next Mission:** Running tests manually in the terminal is fine, but how do we automate this on every single Git push? Enter Continuous Integration (CI).")
        self.render_navigation_footer()

"""
MLOpsHub: Production Quest - Mission 17: The Silent Production Change

Role: SRE / MLOps Engineer
Desk: Central incident command station with serene green dashboard suddenly showing subtle telemetry blips.
Teaches: Production lifecycle drift, upstream dependency changes, the calm before the storm.
"""

import streamlit as st
from src.missions.base_mission import BaseMission
from src.theme import render_neon_card, render_terminal


class Mission17(BaseMission):
    """Mission 17 Implementation."""

    def __init__(self) -> None:
        super().__init__(
            mission_id="m17",
            number_str="17",
            title="The Silent Production Change",
            role_name="SRE / MLOps",
            role_emoji="⏳",
            desk_desc="Reliability monitoring station with steady green status lights, coffee mugs, and operational peace.",
            badge_name="Production Scout",
            xp_award=120
        )

    def render(self) -> None:
        """Render Mission 17 UI components."""
        story = (
            "**Three Weeks Later: Thursday, 10:17 AM**<br>"
            "For 21 consecutive days, ChurnGuard v3 has been a triumph. "
            "Customer churn dropped by 14%, marketing campaign ROI doubled, and the executives are ecstatic. "
            "All production metrics read green across the board.<br><br>"
            "Meanwhile, in another part of the company, an upstream data engineering squad merges "
            "<b>Pull Request #412: 'Refactor billing spend currency conversion'</b>. "
            "The CI tests in their repository pass. The Airflow DAG executes cleanly with zero 500 errors. "
            "No alerts are triggered... yet."
        )
        objective = (
            "Review the healthy state of the production environment. "
            "Observe the deployment of an upstream modification and look for early subtle telemetry shifts."
        )
        self.render_standard_header(story, objective)

        self.render_instructor_notes(
            objective="Set the stage for a realistic production incident by showing that ML failures almost never start with a crashing server.",
            talking_points=[
                "Why ML systems are deeply coupled to upstream data pipelines: A change in an upstream database or billing service directly impacts model predictions.",
                "The illusion of health: A successful DAG run and HTTP 200 responses do NOT guarantee semantic correctness.",
                "Change correlation: Whenever an incident occurs, the first question is always: 'What changed in the upstream world in the last 24 hours?'"
            ],
            questions=[
                "If an upstream team changes the currency of a transaction column from USD to Cents without telling the ML team, will the model crash?",
                "What would happen to the predictions if values become 100x larger?"
            ],
            expected_answers=[
                "No! It will still be a floating point number. The model will run without syntax errors.",
                "The model will interpret 100x larger numbers as astronomical spending, wildly skewing probability outputs."
            ],
            misconceptions=[
                "Believing downstream models can protect themselves from undocumented upstream schema or semantic changes without data contracts.",
                "Thinking that only code bugs cause production incidents."
            ],
            deep_dive="Explain Data Contracts as programmatic agreements to prevent uncoordinated upstream schema and semantic shifts.",
            skip_tip="Observe the green production status board and advance to trigger the incident."
        )

        # Panel 4: Learn
        learn_html = """
        <b>The Upstream Dependency Web:</b><br>
        In modern enterprises, an ML model rarely reads raw user inputs. It consumes features produced by:<br>
        • Payment gateway webhooks ➔ Kafka streams ➔ Snowflake / Postgres ➔ Airflow ETL DAGs ➔ Feature Store ➔ Model.<br>
        • A seemingly harmless change at step 1 or 2 ripples downstream to distort the model's perception of reality.
        """
        render_neon_card("4. LEARN: THE UPSTREAM DEPENDENCY WEB", learn_html, color_variant="purple")

        # Panel 5: Do
        st.markdown("#### 5. DO: Inspect Production Status Board")

        c1, c2, c3 = st.columns(3)
        c1.metric("Service Accuracy", "84.2%", delta="Nominal")
        c2.metric("Feature Drift (PSI)", "0.04", delta="LOW (Stable)")
        c3.metric("API Latency", "18.2 ms", delta="Nominal")

        c4, c5, c6 = st.columns(3)
        c4.metric("Data Quality Gates", "PASS (100%)")
        c5.metric("Fairness Parity", "PASS (0.86)")
        c6.metric("Governance Seal", "APPROVED")

        st.markdown("##### 🔔 Upstream Event Stream (Last 60 Minutes):")
        event_logs = [
            "🟢 [09:30 UTC] Scheduled database backup completed.",
            "🔵 [10:17 UTC] PR #412 merged into data-pipeline: 'Refactor billing spend currency conversion' (Author: DataPlatform)",
            "🟢 [11:00 UTC] Airflow DAG `daily_feature_aggregation` executed successfully (0 errors).",
            "🟢 [11:05 UTC] Feature store sync completed."
        ]
        for e in event_logs:
            st.code(e, language="bash")

        # Panel 6: Under the Hood
        if st.session_state.get("show_code", True):
            st.markdown("#### 6. UNDER THE HOOD: Upstream PR #412 Git Diff")
            diff_str = (
                "diff --git a/pipelines/billing_transform.py b/pipelines/billing_transform.py\n"
                "--- a/pipelines/billing_transform.py\n"
                "+++ b/pipelines/billing_transform.py\n"
                "@@ -14,4 +14,5 @@ def transform_monthly_spend(raw_transactions):\n"
                "-    return raw_transactions.groupby('cust_id')['amount'].sum() / 30.0\n"
                "+    # Refactor currency conversion for multi-currency euro accounts\n"
                "+    converted = raw_transactions['amount'] * raw_transactions['eur_rate'] * 1.08\n"
                "+    return converted.groupby(raw_transactions['cust_id']).sum() / 30.0"
            )
            st.code(diff_str, language="diff")

        # Panel 7: Result
        render_neon_card(
            "7. RESULT",
            "PR #412 is deployed. The code executed cleanly with 0 exceptions. But in the background, a subtle mathematical transformation has altered the distribution of <code>monthly_spend</code>...",
            color_variant="green"
        )

        # Panel 8: Why This Matters
        render_neon_card(
            "8. WHY THIS MATTERS",
            "<b>Silent upstream transformations are the primary source of catastrophic model failure.</b> The infrastructure doesn't know anything is wrong until the business KPI starts collapsing.",
            color_variant="cyan"
        )

        # Panel 9: Next
        st.info("🔜 **Next Mission:** 🚨 RED ALERT! PagerDuty fires at 14:32 UTC. Incident INC-042 is officially declared. All hands on deck!")
        self.render_navigation_footer()

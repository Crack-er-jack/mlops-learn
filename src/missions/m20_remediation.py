"""
MLOpsHub: Production Quest - Mission 20: Remediate & Verify Service

Role: Incident Commander
Desk: Incident resolution control center with rollback switches and recovery verifiers.
Teaches: Service rollback, pipeline re-materialization, statistical validation, post-incident recovery.
"""

import streamlit as st
from src.missions.base_mission import BaseMission
from src.theme import render_neon_card, render_terminal


class Mission20(BaseMission):
    """Mission 20 Implementation."""

    def __init__(self) -> None:
        super().__init__(
            mission_id="m20",
            number_str="20",
            title="Remediate & Verify Service",
            role_name="Incident Commander",
            role_emoji="🛠️",
            desk_desc="Service restoration desk with automated rollback consoles, pipeline triggers, and canary traffic monitors.",
            badge_name="Reliability Hero",
            xp_award=180
        )

    def render(self) -> None:
        """Render Mission 20 UI components."""
        story = (
            "**Thursday, 15:40 UTC**<br>"
            "Armed with definitive root cause evidence, you order immediate remediation. "
            "CEO Maya watches closely: *'Can we fix this without taking down the website or causing "
            "further database corruption?'*<br>"
            "In a mature MLOps system, remediation is a structured, repeatable runbook—not frantic ad-hoc hacking."
        )
        objective = (
            "Execute the 5-step incident remediation runbook: "
            "1. Rollback upstream git commit, 2. Re-run ETL pipeline, 3. Materialize clean features, "
            "4. Validate feature distribution against training baseline, 5. Restore customer campaign automations."
        )
        self.render_standard_header(story, objective)

        self.render_instructor_notes(
            objective="Showcase how disciplined MLOps infrastructure makes service restoration fast, safe, and verifiable.",
            talking_points=[
                "Why we do NOT deploy hotfixes directly into production databases: Always fix at the source (Git) and roll forward through the pipeline.",
                "The 5-step recovery sequence: Revert ➔ Re-run pipeline ➔ Re-materialize features ➔ Statistical smoke test ➔ Restore service.",
                "Verification before un-pausing: Never assume a fix worked until statistical drift drops back below the 0.10 PSI safety threshold."
            ],
            questions=[
                "Why must we re-materialize the Feature Store after reverting the upstream Git commit?",
                "What would happen if we un-paused customer email campaigns before verifying feature drift?"
            ],
            expected_answers=[
                "The Feature Store's online Redis cache still holds the corrupted numbers until an active re-sync occurs.",
                "Customers would continue receiving erroneous high-churn discount emails."
            ],
            misconceptions=[
                "Thinking remediation is finished as soon as `git revert` is merged.",
                "Assuming you need to deploy a brand new model when the issue was upstream feature corruption."
            ],
            deep_dive="Explain how Automated Canary Deployments (e.g. Argo Rollouts) prevent incidents from impacting 100% of users.",
            skip_tip="Click 'Execute Automated Remediation Runbook' to observe the before/after recovery metrics."
        )

        # Panel 4: Learn
        learn_html = """
        <b>The 5-Step Incident Recovery Runbook:</b><br>
        1. <b>Source Code Rollback:</b> <code>git revert 7b2d8e1</code> (reverts PR #412 currency refactor).<br>
        2. <b>Pipeline Re-execution:</b> Trigger Airflow DAG to recalculate clean raw tables.<br>
        3. <b>Feature Materialization:</b> <code>feast materialize</code> updates online Redis key-values.<br>
        4. <b>Statistical Gate:</b> Verify feature PSI drops from $0.42$ back to $< 0.05$.<br>
        5. <b>Service Restoration:</b> Un-pause automated retention workflows and close incident.
        """
        render_neon_card("4. LEARN: PRODUCTION RECOVERY RUNBOOK", learn_html, color_variant="purple")

        # Panel 5: Do
        st.markdown("#### 5. DO: Execute Automated Remediation Runbook")

        run_remediation = st.button("⚡ Execute Automated Remediation Runbook", type="primary")

        if run_remediation:
            st.success("🎉 **REMEDIATION SEQUENCE EXECUTED SUCCESSFULLY!**")

            st.markdown("##### 📈 Before vs After Restoration Comparison:")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("###### 🚨 During Incident (INC-042)")
                st.metric("Model F1 Score", "0.68", delta="-0.16", delta_color="inverse")
                st.metric("monthly_spend PSI", "0.42", delta="HIGH DRIFT", delta_color="inverse")
                st.metric("False Positive Churners", "3,420 users", delta="Customer Trust Hurt", delta_color="inverse")

            with col2:
                st.markdown("###### 🟢 Post-Remediation (Restored)")
                st.metric("Model F1 Score", "0.82", delta="+0.14 (Nominal)")
                st.metric("monthly_spend PSI", "0.03", delta="STABLE (Clean)")
                st.metric("False Positive Churners", "42 users", delta="Baseline Rate")

            render_terminal(
                "git revert 7b2d8e1 && dvc repro && feast materialize-incremental",
                "[main 8f2a1b9] Revert 'Refactor billing spend currency conversion'\n"
                "Running Airflow pipeline: `daily_feature_aggregation` [SUCCESS]\n"
                "Materializing feature view `customer_billing_stats` to Redis...\n"
                "Validation smoke test: assert monthly_spend PSI == 0.03 < 0.10 [PASSED]\n"
                "Incident INC-042 officially CLOSED by Incident Commander at 15:44 UTC."
            )
        else:
            render_terminal("status --incident INC-042", "INCIDENT STATUS: ACTIVE\nRemediation pending operator confirmation.")

        # Panel 6: Under the Hood
        if st.session_state.get("show_code", True):
            st.markdown("#### 6. UNDER THE HOOD: Automated Rollback Script")
            code_str = (
                "# Incident Remediation Automation\n"
                "subprocess.run(['git', 'revert', '--no-edit', '7b2d8e1'], check=True)\n"
                "subprocess.run(['git', 'push', 'origin', 'main'], check=True)\n\n"
                "# Trigger Airflow recomputation\n"
                "airflow_client.trigger_dag('daily_feature_aggregation', reset_dagruns=True)\n\n"
                "# Materialize and assert statistical drift gate\n"
                "feast_client.materialize_incremental()\n"
                "psi = calculate_psi(baseline_spend, current_spend)\n"
                "assert psi < 0.05, f'Feature still exhibiting drift! PSI: {psi}'\n"
                "pagerduty.resolve_incident('INC-042')"
            )
            st.code(code_str, language="python")

        # Panel 7: Result
        render_neon_card(
            "7. RESULT",
            "Service fully restored! F1 score recovered from 0.68 to 0.82. Drift eliminated (PSI = 0.03). Customer retention campaign un-paused with zero customer data loss.",
            color_variant="green"
        )

        # Panel 8: Why This Matters
        render_neon_card(
            "8. WHY THIS MATTERS",
            "<b>Mean Time to Recovery (MTTR) is the ultimate metric of engineering maturity.</b> Because of versioned code, data, features, and models, an existential crisis was resolved in 20 minutes instead of days.",
            color_variant="cyan"
        )

        # Panel 9: Next
        st.info("🔜 **Final Mission:** The storm has passed! Now join the executive boardroom for the Leadership Review: Why MLOps investment matters and where production AI goes next.")
        self.render_navigation_footer()

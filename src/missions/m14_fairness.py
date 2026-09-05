"""
MLOpsHub: Production Quest - Mission 14: Fairness & Bias Audit

Role: Responsible AI / ML Lead
Desk: Ethics review desk with demographic breakdown tables and bias audit checklists.
Teaches: Subgroup disparity, Demographic Parity, Equal Opportunity, Disparate Impact, Responsible AI.
"""

import streamlit as st
import pandas as pd
from src.data.generator import generate_clean_dataset
from src.missions.base_mission import BaseMission
from src.models.explainability import evaluate_fairness_by_group
from src.theme import render_neon_card, render_terminal


class Mission14(BaseMission):
    """Mission 14 Implementation."""

    def __init__(self) -> None:
        super().__init__(
            mission_id="m14",
            number_str="14",
            title="Fairness & Bias Audit",
            role_name="Responsible AI",
            role_emoji="⚖️",
            desk_desc="Ethics and compliance workstation with demographic balance charts and fairness evaluation rubrics.",
            badge_name="Ethics Auditor",
            xp_award=130
        )

    def render(self) -> None:
        """Render Mission 14 UI components."""
        story = (
            "**Sprint Retrospective: Ethics Review**<br>"
            "NEONBYTE is expanding internationally into Latin America and Asia-Pacific. "
            "Elena, Head of Responsible AI, calls a meeting: *'Our overall F1 score across all 100,000 customers "
            "looks great at 82%. But when we slice performance by region, the model has an F1 of only 71% in Latin America "
            "and misclassifies loyal APAC users as high-risk churners at nearly double the rate of North American users!'*<br>"
            "An aggregate metric can hide unacceptable subgroup disparities."
        )
        objective = (
            "Audit ChurnGuard v3 across demographic regions. Evaluate subgroup metrics, "
            "assess Demographic Parity and Equal Opportunity, and review fairness mitigation techniques."
        )
        self.render_standard_header(story, objective)

        self.render_instructor_notes(
            objective="Help students understand that aggregate accuracy masks demographic harm and introduce standard algorithmic fairness definitions.",
            talking_points=[
                "The Simpson's Paradox of ML: High global accuracy can completely conceal poor performance on minority cohorts.",
                "Demographic Parity: P(Y_hat = 1 | Group A) = P(Y_hat = 1 | Group B) (Acceptance/selection rates should be equal).",
                "Equal Opportunity: P(Y_hat = 1 | Y = 1, Group A) = P(Y_hat = 1 | Y = 1, Group B) (True Positive Rates / Recall should be equal).",
                "The Impossibility Theorem of Fairness: Mathematically, you often cannot satisfy Demographic Parity, Equal Opportunity, and Predictive Parity simultaneously."
            ],
            questions=[
                "Why didn't our global train/test evaluation catch the 71% F1 score in Latin America?",
                "If we simply remove 'region' from the training features, does that eliminate regional bias?"
            ],
            expected_answers=[
                "Latin America is only 10% of the customer base; its poor performance was drowned out by the 70% North America + Europe majority.",
                "No! Redundant encodings and proxy features (e.g. currency, payment method, usage timezones) allow the model to infer region."
            ],
            misconceptions=[
                "Believing 'fairness through unawareness' (deleting the sensitive attribute) fixes bias.",
                "Assuming there is a single universal mathematical definition of fairness."
            ],
            deep_dive="Explain how Fairlearn or AIF360 apply post-processing threshold tuning across demographic slices.",
            skip_tip="Inspect the Subgroup Performance Breakdown table to compare Recall across regions."
        )

        # Panel 4: Learn
        learn_html = """
        <b>Two Foundational Fairness Criteria:</b><br>
        • <b>Demographic Parity:</b> Likelihood of receiving a positive prediction is equal across groups regardless of ground truth.<br>
        • <b>Equal Opportunity (Equal Recall):</b> Qualified individuals (actual churners) have equal probability of being identified across all groups.<br>
        • <b>Key Rule:</b> Fairness is contextual—different legal, ethical, and product domains require different definitions.
        """
        render_neon_card("4. LEARN: ALGORITHMIC FAIRNESS METRICS", learn_html, color_variant="purple")

        # Panel 5: Do
        st.markdown("#### 5. DO: Subgroup Disparity Audit")

        df = generate_clean_dataset(n_samples=1200, random_state=42)
        fairness_report = evaluate_fairness_by_group(df, group_col="region")

        st.dataframe(pd.DataFrame(fairness_report["subgroups"]), use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Demographic Parity Ratio", f"{fairness_report['demographic_parity_ratio']:.2f}", delta="Threshold >= 0.80 (4/5ths Rule)", delta_color="inverse")
        with col2:
            st.metric("Equal Opportunity Difference", f"{fairness_report['equal_opportunity_diff']:.2f}", delta="Disparity Flagged", delta_color="inverse")

        if st.button("🛠️ Apply Fairness Mitigation (Subgroup Threshold Rebalancing)", type="primary"):
            st.success("✅ Group-specific decision thresholds calibrated! Latin-America F1 raised from 0.71 to 0.80. Parity ratio restored to 0.86.")

        # Real-World Perspectives
        self.render_perspectives(
            business_pov=(
                "<b>Mitigating Legal & Reputational Catastrophe:</b> Under the EU AI Act, US EEOC guidelines, "
                "and FTC enforcement, algorithmic discrimination carries severe penalties up to 7% of global turnover. "
                "Furthermore, if an AI product systematically mistreats a demographic group, it destroys brand equity "
                "and invites devastating public relations backlash."
            ),
            technical_pov=(
                "<b>The Impossibility Theorem of Fairness:</b> Kleinberg et al. mathematically proved that "
                "unless base rates are identical, a model cannot simultaneously satisfy Demographic Parity, "
                "Equalized Odds, and Predictive Parity. Teams must deliberately choose their fairness constraint: "
                "e.g. <code>ThresholdOptimizer(constraints='equalized_odds')</code> post-processes raw probability outputs "
                "by finding group-specific cutoff thresholds."
            ),
            real_world_case=(
                "In 2019, an investigation into a major US healthcare risk algorithm revealed that Black patients "
                "had to be considerably sicker than White patients to receive the same risk score because the model "
                "used prior healthcare healthcare spend as a proxy for healthcare need (Obermeyer et al., Science)."
            )
        )

        # Panel 6: Under the Hood
        if st.session_state.get("show_code", True):
            st.markdown("#### 6. UNDER THE HOOD: Production Fairlearn Audit & Mitigation Suite")
            tab_audit, tab_mitigate, tab_assert = st.tabs([
                "📊 Fairlearn MetricFrame Audit",
                "🛠️ ThresholdOptimizer Mitigation",
                "🧪 Automated CI Fairness Gate"
            ])

            with tab_audit:
                st.code("""from fairlearn.metrics import MetricFrame, selection_rate, count
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# 1. Multi-metric evaluation sliced across protected demographic attribute
metric_frame = MetricFrame(
    metrics={
        "accuracy": accuracy_score,
        "precision": precision_score,
        "recall": recall_score,
        "f1": f1_score,
        "selection_rate": selection_rate,
        "sample_count": count
    },
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=test_regions
)

# 2. Extract group-level breakdown and disparities
print("Group Metrics:\\n", metric_frame.by_group)
print("Demographic Parity Difference:", metric_frame.difference(metric="selection_rate"))
print("Equal Opportunity Difference:", metric_frame.difference(metric="recall"))""", language="python")

            with tab_mitigate:
                st.code("""from fairlearn.postprocessing import ThresholdOptimizer

# Post-processing mitigation: Optimize group-specific decision boundaries
threshold_optimizer = ThresholdOptimizer(
    estimator=trained_base_model,
    constraints="equalized_odds",
    objective="balanced_accuracy_score",
    prefit=True,
    predict_method="predict_proba"
)

# Fit optimizer on validation split with sensitive features
threshold_optimizer.fit(X_val, y_val, sensitive_features=val_regions)

# Fair predictions in production
fair_predictions = threshold_optimizer.predict(X_prod, sensitive_features=prod_regions)
print("Fairness constraints satisfied across all demographic cohorts!")""", language="python")

            with tab_assert:
                st.code("""# CI Test: tests/test_fairness_contract.py
def test_demographic_parity_ratio_satisfies_four_fifths_rule():
    ratio = metric_frame.ratio(metric="selection_rate")
    # US EEOC 4/5ths (80%) disparate impact standard
    assert ratio >= 0.80, (
        f"Algorithmic Disparity Alert! Selection rate ratio is {ratio:.2f} < 0.80. "
        f"Deployment blocked by Responsible AI compliance gate."
    )""", language="python")

        # Panel 7: Result
        render_neon_card(
            "7. RESULT",
            "Disparity uncovered in Latin America and APAC due to underrepresented training samples. Threshold rebalancing brings all groups within the 80% parity compliance standard.",
            color_variant="green"
        )

        # Panel 8: Why This Matters
        render_neon_card(
            "8. WHY THIS MATTERS",
            "<b>A model that works for 80% of users while discriminating against 20% is not a successful product.</b> Fairness audits ensure inclusive, legally compliant, and ethical AI deployments.",
            color_variant="cyan"
        )

        # Panel 9: Next
        st.info("🔜 **Next Mission:** When a customer asks 'Why was my account flagged as high-risk?', how do we explain individual decisions? Enter Explainability.")
        self.render_navigation_footer()

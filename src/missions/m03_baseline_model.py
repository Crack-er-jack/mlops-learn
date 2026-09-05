"""
MLOpsHub: Production Quest - Mission 03: Build the Baseline Model

Role: Data Scientist
Desk: Research workstation with Jupyter notebook, math scratchpad, scikit-learn docs, and plots.
Teaches: Baseline modeling, train/test split, Precision vs Recall vs F1, Confusion Matrix, class imbalance.
"""

import streamlit as st
import pandas as pd
from src.data.generator import generate_clean_dataset
from src.missions.base_mission import BaseMission
from src.models.trainer import ChurnModelTrainer
from src.theme import render_neon_card, render_terminal


class Mission03(BaseMission):
    """Mission 03 Implementation."""

    def __init__(self) -> None:
        super().__init__(
            mission_id="m03",
            number_str="03",
            title="Build the Baseline Model",
            role_name="Data Scientist",
            role_emoji="🔬",
            desk_desc="Research desk with dual-pane Jupyter Notebook, statistical cheat-sheets, and a warm thermos.",
            badge_name="Baseline Builder",
            xp_award=120
        )

    def render(self) -> None:
        """Render Mission 03 UI components."""
        story = (
            "**Tuesday, 10:15 AM**<br>"
            "You are Sarah, Lead Data Scientist at NEONBYTE. "
            "Armed with clean tabular data, your task is to establish the first baseline benchmark model. "
            "The product manager is eager: *'Can we get 90% accuracy today?'* "
            "You know that in imbalanced customer churn data, accuracy alone is a dangerous trap."
        )
        objective = (
            "Split the dataset into training and testing sets, fit an interpretable baseline model "
            "(Logistic Regression), compute evaluation metrics (Accuracy, Precision, Recall, F1), "
            "and inspect the Confusion Matrix."
        )
        self.render_standard_header(story, objective)

        self.render_instructor_notes(
            objective="Teach students how to evaluate ML models beyond simple accuracy, focusing on Precision, Recall, and the Confusion Matrix.",
            talking_points=[
                "Why accuracy fails on imbalanced datasets: If 85% of users stay, a 'dummy' model predicting 0 for everyone gets 85% accuracy but catches zero churners!",
                "Precision vs Recall tradeoff: High precision means fewer false alarms; high recall means catching almost every churner.",
                "Why we build a simple baseline before jumping to complex neural networks or XGBoost."
            ],
            questions=[
                "If we send a $50 discount to anyone predicted to churn, which metric should we optimize?",
                "If our company has a high churn rate that threatens bankruptcy, should we favor Precision or Recall?"
            ],
            expected_answers=[
                "Precision (to avoid wasting expensive discounts on people who wouldn't have churned).",
                "Recall (we cannot afford to miss a single customer who is about to leave)."
            ],
            misconceptions=[
                "Believing accuracy is the default metric for all machine learning tasks.",
                "Evaluating on the training set instead of a pristine held-out test split."
            ],
            deep_dive="Explain F1 score as the harmonic mean of precision and recall: F1 = 2 * (P * R) / (P + R).",
            skip_tip="Train with Logistic Regression and observe the confusion matrix counts."
        )

        # Panel 4: Learn
        learn_html = """
        <b>The Evaluation Matrix for Retention:</b><br>
        • <b>True Positives (TP):</b> Correctly identified churners (we can intervene!).<br>
        • <b>False Positives (FP):</b> False alarms (wasted retention discounts).<br>
        • <b>False Negatives (FN):</b> Missed churners (lost customer revenue!).<br>
        • <b>F1 Score:</b> Harmonic balance between Precision and Recall.
        """
        render_neon_card("4. LEARN: METRICS BEYOND ACCURACY", learn_html, color_variant="purple")

        # Panel 5: Do
        st.markdown("#### 5. DO: Configure and Train Baseline Model")
        model_choice = st.radio(
            "Select Baseline Model Architecture:",
            ["Logistic Regression (Interpretable)", "Random Forest (Non-linear)"],
            horizontal=True
        )
        selected_model_type = "logistic_regression" if "Logistic" in model_choice else "random_forest"

        col_train_btn, col_info = st.columns([1, 2])
        train_clicked = col_train_btn.button("🚀 Train Model on Split", type="primary")

        # Execute training
        df = generate_clean_dataset(n_samples=1200, random_state=42)
        trainer = ChurnModelTrainer(model_type=selected_model_type, random_state=42)
        results = trainer.train_and_evaluate(df, test_size=0.25)

        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col1.metric("Accuracy", f"{results['accuracy'] * 100:.1f}%")
        m_col2.metric("Precision", f"{results['precision'] * 100:.1f}%")
        m_col3.metric("Recall", f"{results['recall'] * 100:.1f}%")
        m_col4.metric("F1 Score", f"{results['f1']:.3f}", delta="Baseline Anchor")

        # Confusion Matrix Display
        cm = results["confusion_matrix"]
        st.markdown("**Confusion Matrix (Held-out Test Split, N=300):**")
        cm_df = pd.DataFrame(
            cm,
            index=["Actual: Stayed (0)", "Actual: Churned (1)"],
            columns=["Predicted: Stayed (0)", "Predicted: Churned (1)"]
        )
        st.dataframe(cm_df, use_container_width=True)

        # Panel 6: Under the Hood
        if st.session_state.get("show_code", True):
            st.markdown("#### 6. UNDER THE HOOD: Training Script")
            code_text = (
                "from sklearn.model_selection import train_test_split\n"
                "from sklearn.linear_model import LogisticRegression\n"
                "from sklearn.metrics import classification_report, confusion_matrix\n\n"
                "# 1. Split features and target\n"
                "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)\n\n"
                "# 2. Initialize and fit baseline estimator\n"
                "model = LogisticRegression(max_iter=500)\n"
                "model.fit(X_train, y_train)\n\n"
                "# 3. Evaluate predictions on held-out test data\n"
                "y_pred = model.predict(X_test)\n"
                "print(classification_report(y_test, y_pred))\n"
                "print(confusion_matrix(y_test, y_pred))"
            )
            st.code(code_text, language="python")

        if st.session_state.get("show_terminal", True):
            render_terminal(
                "python train_baseline.py",
                f"Training set: 900 samples | Test set: 300 samples\n"
                f"Model: {selected_model_type.upper()}\n"
                f"Precision: {results['precision']:.3f} | Recall: {results['recall']:.3f} | F1: {results['f1']:.3f}\n"
                f"[SUCCESS] Model artifact saved to outputs/baseline_model.joblib"
            )

        # Panel 7: Result
        render_neon_card(
            "7. RESULT",
            f"Baseline model achieved an F1 score of <b>{results['f1']}</b>. It establishes our target threshold. Any future engineering change must beat this baseline.",
            color_variant="green"
        )

        # Panel 8: Why This Matters
        render_neon_card(
            "8. WHY THIS MATTERS",
            "Without an established baseline and clear evaluation metric (F1 score), engineering teams waste weeks building complex models without knowing if they are actually improving over a simple heuristic.",
            color_variant="cyan"
        )

        # Panel 9: Next
        st.info("🔜 **Next Mission:** Your colleague tries to run your script on their laptop... and gets totally different metrics! Welcome to the Reproducibility Trap.")
        self.render_navigation_footer()

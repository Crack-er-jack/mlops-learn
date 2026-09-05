"""
MLOpsHub: Production Quest - Mission 06: Track Experiments with MLflow

Role: Data Scientist
Desk: Research workstation with multiple monitor experiment leaderboards.
Teaches: Experiment tracking, MLflow runs, hyperparameter logging, metric logging, model artifacts.
"""

import streamlit as st
from src.missions.base_mission import BaseMission
from src.models.mlflow_sim import MLflowSimulator
from src.theme import render_neon_card, render_terminal


class Mission06(BaseMission):
    """Mission 06 Implementation."""

    def __init__(self) -> None:
        super().__init__(
            mission_id="m06",
            number_str="06",
            title="Track Experiments with MLflow",
            role_name="Data Scientist",
            role_emoji="📈",
            desk_desc="Data science desk with multiple experiment runs, model training loss curves, and MLflow UI.",
            badge_name="Experiment Scientist",
            xp_award=130
        )

    def render(self) -> None:
        """Render Mission 06 UI components."""
        story = (
            "**Thursday, 2:30 PM**<br>"
            "Sarah has trained 15 different models this week: Logistic Regression, Random Forest, "
            "and Gradient Boosting with different learning rates and max depths. "
            "Her notebook has 80 cells, and nobody remembers which hyperparameter set produced the 0.82 F1 score! "
            "*'Was it n_estimators=100 or 150? Which dataset version was it evaluated on?'*<br>"
            "Jupyter notebooks are great for exploration, but terrible for auditability."
        )
        objective = (
            "Integrate MLflow tracking into the training script. Log hyperparameters, evaluation metrics, "
            "and model artifacts. Compare candidate runs on a centralized experiment leaderboard."
        )
        self.render_standard_header(story, objective)

        self.render_instructor_notes(
            objective="Teach students the discipline of automated experiment tracking and why spreadsheets or notebook outputs fail at scale.",
            talking_points=[
                "The 'Notebook Amnesia' problem: Running cells out of order makes it impossible to know which exact parameters generated which metric.",
                "MLflow logs 4 core entities: Parameters (inputs), Metrics (outputs over time), Tags (metadata/author), Artifacts (weights/plots).",
                "Experiment Tracking vs Model Registry: Tracking records all attempts; the Registry governs only the selected production candidates."
            ],
            questions=[
                "Why shouldn't we just write down model hyperparameters and accuracy in an Excel sheet?",
                "What happens when a model trained 6 months ago breaks in production and you need to retrain it?"
            ],
            expected_answers=[
                "Manual spreadsheets are error-prone, quickly abandoned, and not programmatically linked to model artifacts or data hashes.",
                "Without tracking, you can't reproduce the exact environment, code commit, or parameter settings."
            ],
            misconceptions=[
                "Thinking MLflow is only for neural networks (it works for any Python script or sklearn model).",
                "Confusing logging metrics at run-time with production monitoring."
            ],
            deep_dive="Explain how MLflow automatically captures Git commit hash, user, and conda/pip environment.",
            skip_tip="Inspect the experiment leaderboard and compare F1 score vs inference latency."
        )

        # Panel 4: Learn
        learn_html = r"""
        <b>The 4 Pillars of MLflow Run Tracking:</b><br>
        • <b>Parameters:</b> Hyperparameters ($C$, $max\_depth$, $learning\_rate$, $n\_estimators$).<br>
        • <b>Metrics:</b> Quantitative evaluations ($Accuracy$, $F1$, $Precision$, $Latency$).<br>
        • <b>Tags:</b> Contextual metadata (Git commit, dataset hash, author, branch).<br>
        • <b>Artifacts:</b> Serialized model files (<code>model.pkl</code>), confusion matrix images, feature importance plots.
        """
        render_neon_card("4. LEARN: MLFLOW EXPERIMENT TRACKING", learn_html, color_variant="purple")

        # Panel 5: Do
        st.markdown("#### 5. DO: Interactive MLflow Experiment Leaderboard")
        df_runs = MLflowSimulator.get_runs_dataframe()
        st.dataframe(df_runs, use_container_width=True)

        selected_run = st.selectbox("Select a Run ID to Inspect Artifacts:", df_runs["Run ID"].tolist())
        run_meta = next(r for r in MLflowSimulator.DEFAULT_EXPERIMENTS if r["run_id"] == selected_run)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Hyperparameters (`{selected_run}`):**")
            st.json(run_meta["params"])
        with col2:
            st.markdown(f"**Artifacts & Lineage (`{selected_run}`):**")
            st.markdown(f"- 📦 **Artifact URI:** `{run_meta['artifact_uri']}`")
            st.markdown(f"- 📊 **Dataset Linked:** `{run_meta['dataset_version']}`")
            st.markdown(f"- 🔗 **Git Commit:** `{run_meta['git_commit']}`")

        # Real-World Perspectives
        self.render_perspectives(
            business_pov=(
                "<b>Stopping $100K+ Duplicate Experiments & Knowledge Drain:</b> When a data scientist leaves a company, "
                "their un-tracked Jupyter notebooks become unusable black boxes. Without centralized experiment tracking, "
                "incoming scientists unknowingly duplicate identical models, wasting hundreds of engineering hours "
                "and expensive GPU/cloud compute budgets."
            ),
            technical_pov=(
                "<b>Tracking Server Architecture:</b> MLflow separates metadata storage (PostgreSQL / SQLite backend store "
                "storing runs, params, metrics, tags) from artifact storage (AWS S3, Azure Blob, GCS storing serialized models, "
                "plots, conda envs). The MLflow Client communicates over REST API, making it language-agnostic across Python, R, and Java."
            ),
            real_world_case=(
                "A fintech unicorn discovered that three independent machine learning squads were training almost "
                "identical fraud detection models with slightly different learning rates, consuming $240,000 in redundant "
                "AWS compute because neither team had visibility into existing experiment runs."
            )
        )

        # Panel 6: Under the Hood
        if st.session_state.get("show_code", True):
            st.markdown("#### 6. UNDER THE HOOD: Production MLflow Tracking & Querying Suite")
            tab_track, tab_sig, tab_query, tab_mlflow_cli = st.tabs([
                "📈 Python Tracking Script",
                "✍️ Model Signature & Input Example",
                "🔍 Querying Runs via Python API",
                "💻 MLflow CLI Server Commands"
            ])

            with tab_track:
                st.code(MLflowSimulator.get_code_snippet(), language="python")

            with tab_sig:
                st.code("""from mlflow.models.signature import infer_signature
import mlflow.sklearn

# Infer strict input/output contract signature
signature = infer_signature(X_train, model.predict(X_train))

# Input example enables automatic REST schema generation
input_example = X_train.iloc[:2].to_dict(orient="split")

# Log model with full production metadata
mlflow.sklearn.log_model(
    sk_model=model,
    artifact_path="churn_model",
    signature=signature,
    input_example=input_example,
    registered_model_name="ChurnGuard"
)""", language="python")

            with tab_query:
                st.code("""from mlflow.tracking import MlflowClient

client = MlflowClient()

# Search and sort top runs by F1 score
runs = client.search_runs(
    experiment_ids=["1"],
    filter_string="metrics.f1_score > 0.75",
    order_by=["metrics.f1_score DESC"],
    max_results=5
)

for run in runs:
    print(f"Run ID: {run.info.run_id} | F1: {run.data.metrics['f1_score']:.4f}")""", language="python")

            with tab_mlflow_cli:
                st.code("""# 1. Launch production MLflow tracking server backed by Postgres & S3
mlflow server \\
  --backend-store-uri postgresql://mlflow:pass@db-prod:5432/mlflow \\
  --default-artifact-root s3://neonbyte-mlflow-artifacts \\
  --host 0.0.0.0 --port 5000

# 2. View runs and artifacts in terminal
mlflow runs list --experiment-id 1""", language="bash")

        if st.session_state.get("show_terminal", True):
            st.markdown("##### ⚙️ Interactive MLflow Lab")
            st.info("💡 **Mission:** Run `python train.py` to execute a training script that logs to MLflow, then type `mlflow ui` to launch the dashboard.")
            ml_cmd = st.text_input("Terminal Input:", placeholder="e.g. python train.py", key="mlflow_lab_cmd")
            if st.button("▶️ Execute Command", type="primary", key="mlflow_exec"):
                ml_cmd = ml_cmd.strip()
                if "train" in ml_cmd:
                    st.success("✅ Model trained! New run logged to MLflow.")
                    render_terminal(ml_cmd, "Training GradientBoosting model...\nLogging params (learning_rate=0.05, max_depth=6)\nLogging metrics (f1=0.818, val_loss=0.34)\nArtifact 'model.pkl' saved.\nRun ID: run-9c2b8x completed.")
                elif "ui" in ml_cmd:
                    st.success("✅ MLflow UI Server started! You could view it at http://127.0.0.1:5000")
                    render_terminal(ml_cmd, "[INFO] Starting MLflow Tracking Server on http://127.0.0.1:5000\n[INFO] Connected to backend store: sqlite:///mlflow.db\n[INFO] Found 3 runs in experiment 'churn_prediction_quest'.")
                else:
                    render_terminal(ml_cmd, "Command not recognized. Try 'python train.py' or 'mlflow ui'")
            else:
                render_terminal("mlflow ui --port 5000", "[INFO] Server idle. Ready for commands.")

        # Panel 7: Result
        render_neon_card(
            "7. RESULT",
            "Experiment <code>run-4e8f1a</code> (Gradient Boosting) leads the board with F1 = 0.818, but notice latency is 28.4ms vs 11.8ms for Random Forest. Every tradeoff is now auditable!",
            color_variant="green"
        )

        # Panel 8: Why This Matters
        render_neon_card(
            "8. WHY THIS MATTERS",
            "<b>Experiment tracking eliminates guesswork.</b> In a regulated industry or fast-moving startup, being able to trace any model artifact back to its code, data, and parameters is mandatory.",
            color_variant="cyan"
        )

        # Panel 9: Next
        st.info("🔜 **Next Mission:** Having 50 runs in MLflow is great, but which one gets promoted to production? Enter the Model Registry.")
        self.render_navigation_footer()

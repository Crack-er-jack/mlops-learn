"""
MLOpsHub: Production Quest - Mission 07: Version the Model & Model Registry

Role: ML Engineer
Desk: Engineering workstation with model artifact storage and stage transition gates.
Teaches: Model versioning vs experiment tracking, Model Registry stages, governance, lineage, rollback.
"""

import streamlit as st
import pandas as pd
from src.missions.base_mission import BaseMission
from src.models.mlflow_sim import MLflowSimulator
from src.theme import render_neon_card, render_terminal


class Mission07(BaseMission):
    """Mission 07 Implementation."""

    def __init__(self) -> None:
        super().__init__(
            mission_id="m07",
            number_str="07",
            title="Version the Model & Model Registry",
            role_name="ML Engineer",
            role_emoji="🏛️",
            desk_desc="MLOps command station with model deployment gates, stage badges, and lineage graphs.",
            badge_name="Model Guardian",
            xp_award=140
        )

    def render(self) -> None:
        """Render Mission 07 UI components."""
        story = (
            "**Friday, 10:00 AM**<br>"
            "Sarah trained a high-scoring model, but Alex warns: *'Wait! We can't just copy Sarah's `model.pkl` "
            "into the production web server! What if it's too slow? Who approved it? What if we need to rollback "
            "at 3:00 AM on a Sunday?'*<br>"
            "A model file sitting on a scientist's laptop is NOT a production asset. "
            "You need a centralized **Model Registry** with clear lifecycle stages."
        )
        objective = (
            "Register candidate models into the ChurnGuard Model Registry. "
            "Manage lifecycle stages: Development -> Staging -> Production -> Archived. "
            "Verify complete lineage (Data Hash -> Git Commit -> MLflow Run -> Registry Version)."
        )
        self.render_standard_header(story, objective)

        self.render_instructor_notes(
            objective="Distinguish between an ephemeral experiment run and a formal registered model artifact ready for production deployment.",
            talking_points=[
                "Why the highest metric model isn't automatically deployed: Latency limits, memory footprints, explainability requirements, edge runtime compatibility.",
                "Stages of a Model Registry: Development (experimental), Staging (under load & shadow testing), Production (serving live traffic), Archived (historical/rollback).",
                "Lineage: If an auditor asks 'What model made decision #9482 on March 15th?', can you reconstruct the exact weights and data?"
            ],
            questions=[
                "Why must the Model Registry enforce immutable version tags (v1, v2, v3) instead of overwriting 'latest.pkl'?",
                "If a model in production exhibits an unexpected bug, how does the Model Registry help?"
            ],
            expected_answers=[
                "Overwriting leads to silent breakage and impossible post-mortem debugging.",
                "Instant, zero-downtime rollback to the previously approved version (e.g. v3 -> v2)."
            ],
            misconceptions=[
                "Thinking the Model Registry trains models (it only stores, stages, and versions them).",
                "Assuming staging is only for traditional software, not ML systems."
            ],
            deep_dive="Explain Blue/Green and Canary deployment strategies enabled by model staging.",
            skip_tip="Click 'Promote v3 to Production' and observe the status transition."
        )

        # Panel 4: Learn
        learn_html = """
        <b>The Model Lifecycle Stages:</b><br>
        • <b>Development:</b> Unproven candidate models undergoing hyperparameter tuning.<br>
        • <b>Staging:</b> Candidate deployed to a staging environment for load testing and data contract verification.<br>
        • <b>Production:</b> The single active version answering live customer retention queries.<br>
        • <b>Archived:</b> Retired legacy versions preserved for instant rollback and regulatory compliance.
        """
        render_neon_card("4. LEARN: MODEL REGISTRY LIFECYCLE", learn_html, color_variant="purple")

        # Panel 5: Do
        st.markdown("#### 5. DO: Manage ChurnGuard Model Registry")

        # Session state for registry stages if not present
        if "registry_models" not in st.session_state:
            st.session_state["registry_models"] = [dict(m) for m in MLflowSimulator.INITIAL_REGISTRY]

        registry_df = pd.DataFrame(st.session_state["registry_models"])
        st.dataframe(registry_df[["model_name", "version", "stage", "owner", "registered_at", "data_lineage"]], use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            target_version = st.selectbox("Select Model Version to Promote/Transition:", ["v1", "v2", "v3"])
        with col2:
            new_stage = st.selectbox("Select New Stage:", ["Staging", "Production", "Archived", "Development"])

        if st.button("🏷️ Transition Model Stage", type="primary"):
            for m in st.session_state["registry_models"]:
                if m["version"] == target_version:
                    m["stage"] = new_stage
                elif new_stage == "Production" and m["stage"] == "Production":
                    # Demote previous prod model to Archived
                    m["stage"] = "Archived"
            st.success(f"Model {target_version} successfully transitioned to {new_stage}!")
            st.rerun()

        # Real-World Perspectives
        self.render_perspectives(
            business_pov=(
                "<b>Preventing Unauthorized Rogue Deployments:</b> In enterprise organizations, a model promotion "
                "directly impacts financial balance sheets and customer safety. The Model Registry acts as the legal and "
                "operational gatekeeper: models cannot reach production without explicit human review, automated audit stamps, "
                "and sign-offs from both data science and compliance leads."
            ),
            technical_pov=(
                "<b>Semantic Versioning & Stage Decoupling:</b> The Model Registry replaces hardcoded filepaths "
                "(`model_final_v3.pkl`) with dynamic URI aliases: `models:/ChurnGuard/Production` or `models:/ChurnGuard@champion`. "
                "Serving microservices dynamically load the production alias via REST or gRPC without requiring code redeployment. "
                "If an anomaly is detected, pointing the alias back to version 2 takes less than 1 second."
            ),
            real_world_case=(
                "A leading e-commerce retailer accidentally pushed an unvalidated experimental dynamic pricing model to production "
                "during Black Friday because a developer overwrote the `latest.pkl` file on an S3 bucket, discounting flagship "
                "electronics by 90% before the error was caught 4 hours later."
            )
        )

        # Panel 6: Under the Hood
        if st.session_state.get("show_code", True):
            st.markdown("#### 6. UNDER THE HOOD: Production Model Registry API Suite")
            tab_promote, tab_rollback, tab_client_load = st.tabs([
                "🏷️ Transition Stage with Audit Note",
                "⏪ 1-Click Instant Rollback Script",
                "⚡ Dynamic Client Serving URI"
            ])

            with tab_promote:
                st.code("""from mlflow.tracking import MlflowClient

client = MlflowClient()

# 1. Register candidate run as formal model version
model_version = client.create_model_version(
    name="ChurnGuard",
    source="s3://neonbyte-mlflow/artifacts/run-4e8f1a/model",
    run_id="run-4e8f1a",
    tags={"approved_by": "Alex (ML Lead)", "eval_f1": "0.818"}
)

# 2. Promote to Production and demote previous champion to Archived
client.transition_model_version_stage(
    name="ChurnGuard",
    version=model_version.version,
    stage="Production",
    archive_existing_versions=True
)
print(f"ChurnGuard v{model_version.version} is now LIVE in Production!")""", language="python")

            with tab_rollback:
                st.code("""# SRE Emergency Rollback Runbook: Instantly revert to version 2
client.transition_model_version_stage(
    name="ChurnGuard",
    version=2,
    stage="Production",
    archive_existing_versions=True
)
# Serving containers immediately resolve models:/ChurnGuard/Production to v2!""", language="python")

            with tab_client_load:
                st.code("""import mlflow.pyfunc

# Serving API loads model by stage URI without hardcoding file paths
model = mlflow.pyfunc.load_model("models:/ChurnGuard/Production")

# Predictions automatically run through active production version
predictions = model.predict(customer_features)""", language="python")

        if st.session_state.get("show_terminal", True):
            render_terminal(
                "mlflow models list --model-name ChurnGuard",
                "Model: ChurnGuard\n"
                "| Version | Stage      | Run ID     | Created             |\n"
                "|---------|------------|------------|---------------------|\n"
                "| 3       | Production | run-4e8f1a | 2026-03-20 10:15:00 |\n"
                "| 2       | Archived   | run-9c3e2f | 2026-03-12 16:45:00 |\n"
                "| 1       | Archived   | run-7a1b8c | 2026-03-05 14:20:00 |"
            )

        # Panel 7: Result
        render_neon_card(
            "7. RESULT",
            "ChurnGuard v3 is officially promoted to Production stage! Any client application requesting <code>models:/ChurnGuard/Production</code> will automatically resolve to this verified artifact.",
            color_variant="green"
        )

        # Panel 8: Why This Matters
        render_neon_card(
            "8. WHY THIS MATTERS",
            "<b>Separating experiment artifacts from production releases</b> prevents accidental overwrites and provides an immediate one-click rollback mechanism if a model malfunctions in production.",
            color_variant="cyan"
        )

        # Panel 9: Next
        st.info("🔜 **Next Mission:** A model is only as good as its features. But how do we ensure features calculated in batch training match real-time serving? Enter the Feature Store.")
        self.render_navigation_footer()

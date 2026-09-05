"""
MLOpsHub: Production Quest - Mission 12: Deploy the Model to Production

Role: Software / MLOps Engineer
Desk: Live production engineering station with active API metrics and customer request streams.
Teaches: Production inference serving, real-time prediction, latency SLAs, model lineage.
"""

import streamlit as st
from src.data.generator import generate_clean_dataset
from src.missions.base_mission import BaseMission
from src.models.trainer import ChurnModelTrainer
from src.theme import render_neon_card, render_terminal


class Mission12(BaseMission):
    """Mission 12 Implementation."""

    def __init__(self) -> None:
        super().__init__(
            mission_id="m12",
            number_str="12",
            title="Deploy the Model to Production",
            role_name="Software / MLOps",
            role_emoji="🚀",
            desk_desc="Production monitoring console with live customer query traffic and active inference endpoints.",
            badge_name="Deployment Engineer",
            xp_award=150
        )

    def render(self) -> None:
        """Render Mission 12 UI components."""
        story = (
            "**Friday, 2:00 PM**<br>"
            "The launch button is pressed! ChurnGuard is officially LIVE in production at NEONBYTE. "
            "Customer success agents and automated retention campaigns are querying the API in real time. "
            "Every prediction must return in under 50ms, and every inference must log its complete lineage: "
            "Model version, data snapshot, feature view, and Git commit hash."
        )
        objective = (
            "Interact with the live ChurnGuard production inference service. "
            "Enter customer profile telemetry, generate real-time churn predictions, "
            "and inspect the end-to-end lineage stamp attached to the inference response."
        )
        self.render_standard_header(story, objective)

        self.render_instructor_notes(
            objective="Connect all earlier MLOps building blocks into a single operational inference endpoint with complete traceability.",
            talking_points=[
                "Inference paradigms: Real-time request-response (FastAPI/gRPC) vs Batch inference (daily Airflow jobs) vs Streaming (Kafka/Flink).",
                "Why latency SLAs matter: If customer success agents have to wait 3 seconds for a screen to load, they will stop using the AI tool.",
                "Lineage: Why every single prediction should include a header with model_version, feature_store_version, and dvc_data_hash."
            ],
            questions=[
                "If a customer sues a bank over an automated AI credit decision, what must the engineering team prove?",
                "What is the difference between batch inference and real-time serving in terms of compute cost and complexity?"
            ],
            expected_answers=[
                "The exact model weights, input features, and training dataset version active at the precise second the decision was rendered.",
                "Batch is cheaper and simpler (scheduled queries); real-time requires high-availability 24/7 web services and caching."
            ],
            misconceptions=[
                "Assuming deploying a model is just running a Python script on a server.",
                "Believing MLOps ends once the model is deployed (deployment is only the halfway mark!)."
            ],
            deep_dive="Explain how Model Lineage headers enable distributed tracing through OpenTelemetry.",
            skip_tip="Adjust the sliders to simulate a high-risk customer and click 'Run Live Inference'."
        )

        # Panel 4: Learn
        learn_html = r"""
        <b>The Complete Model Lineage Chain:</b><br>
        <code>Raw Telemetry (DVC: c0d3e4f)</code> ➔ <code>Feature View (v3)</code><br>
        ➔ <code>Training Run (MLflow: run-4e8f1a)</code> ➔ <code>Model Registry (v3.0 Production)</code><br>
        ➔ <code>Container (Docker: v3.0.0)</code> ➔ <code>Live Prediction ($\hat{p} = 0.82$)</code>.
        """
        render_neon_card("4. LEARN: PRODUCTION SERVING & LINEAGE", learn_html, color_variant="purple")

        # Panel 5: Do
        st.markdown("#### 5. DO: Live ChurnGuard Production Serving Portal")

        # Live prediction form
        col_in1, col_in2, col_in3 = st.columns(3)
        with col_in1:
            age = st.slider("Customer Age:", 18, 75, 34)
            tenure = st.slider("Tenure (Months):", 1, 60, 8)
            monthly_spend = st.slider("Monthly Spend ($):", 20.0, 180.0, 125.0)

        with col_in2:
            support_calls = st.slider("Support Calls (90d):", 0, 10, 5)
            usage_freq = st.slider("Usage Frequency (Logins/wk):", 1, 40, 6)
            contract = st.selectbox("Contract Type:", ["Month-to-month", "One-year", "Two-year"])

        with col_in3:
            region = st.selectbox("Customer Region:", ["North-America", "Europe", "Asia-Pacific", "Latin-America"])
            segment = st.selectbox("Customer Segment:", ["Standard", "Premium", "Enterprise"])

        predict_btn = st.button("🔮 Run Live Production Inference", type="primary")

        # Train backing model on clean data
        df = generate_clean_dataset(n_samples=1000, random_state=42)
        trainer = ChurnModelTrainer(model_type="logistic_regression", random_state=42)
        trainer.train_and_evaluate(df)

        cust_payload = {
            "age": age,
            "tenure": tenure,
            "monthly_spend": monthly_spend,
            "support_calls": support_calls,
            "usage_frequency": usage_freq,
            "contract_type": contract,
            "region": region,
            "customer_segment": segment
        }
        pred_class, pred_prob = trainer.predict_single(cust_payload)

        # Result display
        st.markdown("##### 📡 Inference Output & Decision Stamp")
        res_col1, res_col2, res_col3 = st.columns(3)
        risk_label = "🔴 HIGH CHURN RISK" if pred_prob > 0.50 else "🟢 LOW CHURN RISK"
        res_col1.metric("Predicted Status", risk_label)
        res_col2.metric("Churn Probability", f"{pred_prob * 100:.1f}%")
        res_col3.metric("Latency", "18.2 ms", delta="SLA < 50ms")

        # Lineage Card
        lineage_html = """
        <div style="background: rgba(0, 245, 255, 0.08); border: 1px dashed #00f5ff; border-radius: 8px; padding: 12px; font-size: 0.88rem;">
            <strong>🔗 PRODUCTION LINEAGE STAMP (X-Model-Lineage):</strong><br>
            • <b>Model:</b> ChurnGuard v3.0 (Stage: Production | MLflow Run: <code>run-4e8f1a</code>)<br>
            • <b>Data Snapshot:</b> <code>data/churn_v3_prod.csv</code> (DVC Hash: <code>c0d3e4fa6b78</code>)<br>
            • <b>Feature Store View:</b> <code>customer_billing_stats:v3</code><br>
            • <b>Git SHA:</b> <code>commit 3c9f2a4</code> | <b>Runtime:</b> <code>docker://neonbyte/churnguard:v3.0.0</code>
        </div>
        """
        st.markdown(lineage_html, unsafe_allow_html=True)

        # Real-World Perspectives
        self.render_perspectives(
            business_pov=(
                "<b>Operational SLAs & Customer Contract Penalties:</b> In customer-facing AI applications, "
                "a 500ms delay in response time reduces conversion rates by up to 20%. Production serving contracts "
                "stipulate strict SLAs (e.g. 99.9% uptime, p99 latency < 50ms). Failing these SLAs incurs direct "
                "financial penalty credits payable back to enterprise clients."
            ),
            technical_pov=(
                "<b>Inference Optimization & Lineage Injection:</b> Production APIs require asynchronous ASGI frameworks "
                "(FastAPI / Uvicorn) with strict schema validation using Pydantic. Heavy matrix vectorization must occur "
                "outside the async event loop using thread pools (`run_in_threadpool`). Every response must inject standard "
                "tracing headers: `X-Model-Version`, `X-DVC-Hash`, and W3C `traceparent` for OpenTelemetry distributed tracing."
            ),
            real_world_case=(
                "Amazon found that every 100ms of additional webpage/API latency cost them 1% in retail sales, "
                "prompting machine learning infrastructure engineers to compress models from 800ms down to sub-15ms runtimes."
            )
        )

        # Panel 6: Under the Hood
        if st.session_state.get("show_code", True):
            st.markdown("#### 6. UNDER THE HOOD: Production Serving API & Client Contract")
            tab_fastapi, tab_pydantic, tab_loadtest = st.tabs([
                "⚡ main.py (FastAPI Production Endpoint)",
                "📋 schemas.py (Pydantic Request & Response)",
                "🔥 locustfile.py (Load Testing & SLA Benchmark)"
            ])

            with tab_fastapi:
                st.code("""from fastapi import FastAPI, Response, status
import time
from schemas import CustomerInferencePayload, PredictionResponse
import mlflow.pyfunc

app = FastAPI(title="ChurnGuard Production Serving API", version="3.0.0")

# Load champion model from registry at startup
model = mlflow.pyfunc.load_model("models:/ChurnGuard/Production")

@app.post("/v1/predict", response_model=PredictionResponse)
async def predict_churn(payload: CustomerInferencePayload, response: Response):
    start_time = time.perf_counter()
    
    # Extract validated features
    features = payload.to_numpy_array()
    
    # Compute inference probability
    prob = float(model.predict(features)[0])
    latency_ms = (time.perf_counter() - start_time) * 1000.0
    
    # Inject immutable lineage metadata headers
    response.headers["X-Model-Version"] = "ChurnGuard-v3.0"
    response.headers["X-Data-DVC"] = "c0d3e4fa6b78"
    response.headers["X-Inference-Latency-Ms"] = f"{latency_ms:.2f}"
    
    return PredictionResponse(
        customer_id=payload.customer_id,
        churn_risk=bool(prob > 0.50),
        churn_probability=round(prob, 4),
        latency_ms=round(latency_ms, 2)
    )

@app.get("/healthz", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "HEALTHY", "model_stage": "Production"}""", language="python")

            with tab_pydantic:
                st.code("""from pydantic import BaseModel, Field
from typing import Literal

class CustomerInferencePayload(BaseModel):
    customer_id: str = Field(..., example="CUST-10042")
    age: int = Field(..., ge=18, le=100)
    tenure: int = Field(..., ge=1, le=120)
    monthly_spend: float = Field(..., ge=0.0)
    support_calls: int = Field(..., ge=0)
    usage_frequency: int = Field(..., ge=0)
    contract_type: Literal["Month-to-month", "One-year", "Two-year"]
    region: Literal["North-America", "Europe", "Asia-Pacific", "Latin-America"]
    customer_segment: Literal["Standard", "Premium", "Enterprise"]

class PredictionResponse(BaseModel):
    customer_id: str
    churn_risk: bool
    churn_probability: float
    latency_ms: float""", language="python")

            with tab_loadtest:
                st.code("""# locustfile.py - Simulated 10,000 RPS Load Test
from locust import HttpUser, task, between

class ChurnGuardUser(HttpUser):
    wait_time = between(0.01, 0.05)

    @task
    def test_predict_sla(self):
        payload = {
            "customer_id": "CUST-10023",
            "age": 35,
            "tenure": 14,
            "monthly_spend": 85.0,
            "support_calls": 2,
            "usage_frequency": 18,
            "contract_type": "Month-to-month",
            "region": "North-America",
            "customer_segment": "Standard"
        }
        with self.client.post("/v1/predict", json=payload, catch_response=True) as response:
            if response.elapsed.total_seconds() > 0.050:
                response.failure(f"SLA breached! Latency: {response.elapsed.total_seconds()*1000}ms > 50ms")""", language="python")

        # Panel 7: Result
        render_neon_card(
            "7. RESULT",
            "ChurnGuard is successfully serving predictions with a response latency of 18.2ms and 100% auditable lineage metadata on every request.",
            color_variant="green"
        )

        # Panel 8: Why This Matters
        render_neon_card(
            "8. WHY THIS MATTERS",
            "<b>Lineage is your insurance policy.</b> When a customer asks why their account was flagged or an auditor demands proof of fairness, complete lineage allows exact reconstruction of the decision state.",
            color_variant="cyan"
        )

        # Panel 9: Next
        st.info("🔜 **Next Mission:** The model is deployed! But the real world is never static. How do we monitor requests and detect feature and data drift in production? Enter Observability.")
        self.render_navigation_footer()

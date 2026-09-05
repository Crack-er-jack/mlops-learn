"""
MLOpsHub: Production Quest - Mission 13: Observe Production & Detect Drift

Role: MLOps / SRE
Desk: Observability command center with Grafana drift dashboards and anomaly detectors.
Teaches: Statistical feature drift (PSI, KS test), concept drift, operational telemetry.
"""

import streamlit as st
import pandas as pd
from src.data.generator import generate_clean_dataset, generate_drifted_dataset
from src.missions.base_mission import BaseMission
from src.pipeline.monitoring import evaluate_feature_drift, get_production_telemetry
from src.theme import render_neon_card, render_terminal


class Mission13(BaseMission):
    """Mission 13 Implementation."""

    def __init__(self) -> None:
        super().__init__(
            mission_id="m13",
            number_str="13",
            title="Observe Production & Detect Drift",
            role_name="MLOps / SRE",
            role_emoji="📡",
            desk_desc="Reliability operations center with Prometheus gauges, Grafana heatmaps, and drift alarms.",
            badge_name="Observability Sentinel",
            xp_award=150
        )

    def render(self) -> None:
        """Render Mission 13 UI components."""
        story = (
            "**Two Weeks After Deployment**<br>"
            "Marcus looks at the DevOps dashboard: *'The HTTP server is rock-solid. Uptime is 99.98%, "
            "and latency is 18ms. But in machine learning, a system can be 100% online from a software perspective "
            "while being completely broken mathematically! If customer behavior shifts or external macroeconomics change, "
            "the distribution of incoming features will drift away from our training baseline.'*<br>"
            "You need continuous statistical drift monitoring."
        )
        objective = (
            "Establish production observability telemetry. Monitor requests, latency, and error rates. "
            "Calculate statistical drift metrics—Population Stability Index (PSI) and Kolmogorov-Smirnov (KS) test—"
            "across incoming customer features."
        )
        self.render_standard_header(story, objective)

        self.render_instructor_notes(
            objective="Distinguish between Software Monitoring (CPU, memory, latency, 500 errors) and ML Observability (data drift, concept drift, prediction drift).",
            talking_points=[
                "Why ML monitoring is unique: Traditional servers fail loud (500 Internal Server Error). ML models fail quietly (they return HTTP 200 with invalid predictions).",
                "Data Drift (Covariate Shift): P(X) changes while P(y|X) stays the same (e.g. inflation raises spend).",
                "Concept Drift: P(y|X) changes (e.g. during a competitor promo, customers with 0 support calls suddenly churn).",
                "Metrics: Population Stability Index (PSI < 0.1 stable, > 0.2 alert) and Kolmogorov-Smirnov 2-sample test."
            ],
            questions=[
                "If our serving API latency is 15ms and error rate is 0.0%, could our ML product still be losing millions of dollars? How?",
                "What is the difference between Feature Drift and Ground Truth Label Drift?"
            ],
            expected_answers=[
                "Yes! If the model is outputting inverted predictions due to drifted data, customers churn unmonitored while infrastructure looks 100% green.",
                "Feature drift can be measured immediately in real-time; label drift requires waiting weeks/months for actual churn to happen."
            ],
            misconceptions=[
                "Believing standard APM tools like Datadog or New Relic automatically monitor ML accuracy.",
                "Assuming a model only needs to be trained once and can run forever without retraining."
            ],
            deep_dive="Explain how Evidently AI or Whylogs compute rolling window PSI in production streaming architectures.",
            skip_tip="Toggle 'Simulate Upstream Shift' to watch the PSI score jump into red alert territory."
        )

        # Panel 4: Learn
        learn_html = r"""
        <b>The Hierarchy of ML Observability:</b><br>
        1. <b>Service Health:</b> Latency ($p99 < 50ms$), Uptime ($99.9\%$), Throughput (RPS).<br>
        2. <b>Data Quality:</b> Schema consistency, null rates, range violations.<br>
        3. <b>Feature Drift (PSI / KS):</b> Is current distribution $P_{prod}(X)$ deviating from baseline $P_{train}(X)$?<br>
        4. <b>Concept Drift:</b> Has the relationship between features and churn changed?
        """
        render_neon_card("4. LEARN: ML OBSERVABILITY VS TRADITIONAL APM", learn_html, color_variant="purple")

        # Panel 5: Do
        st.markdown("#### 5. DO: Real-Time Telemetry & Drift Analysis Dashboard")

        # Telemetry metrics
        telem = get_production_telemetry()
        t1, t2, t3, t4 = st.columns(4)
        t1.metric("24h Request Volume", f"{telem['total_requests_24h']:,}")
        t2.metric("Average Latency", f"{telem['average_latency_ms']} ms")
        t3.metric("API Error Rate", f"{telem['error_rate_pct']}%", delta="Healthy")
        t4.metric("Uptime", f"{telem['uptime_pct']}%")

        # Drift Simulation Toggle
        st.markdown("##### 🔬 Live Feature Distribution Drift Monitor")
        simulate_drift = st.toggle("Simulate Upstream Shift in Live Traffic (Sudden inflation / Spend Spike)")

        base_df = generate_clean_dataset(n_samples=1000, random_state=42)
        if simulate_drift:
            prod_df = generate_drifted_dataset(n_samples=500, drift_scenario="feature_drift", random_state=99)
        else:
            prod_df = generate_clean_dataset(n_samples=500, random_state=88)

        drift_results = evaluate_feature_drift(
            baseline_df=base_df,
            production_df=prod_df,
            features=["monthly_spend", "tenure", "support_calls", "usage_frequency"]
        )

        st.dataframe(pd.DataFrame(drift_results), use_container_width=True)

        if simulate_drift:
            st.error("🚨 **DRIFT ALARM:** `monthly_spend` distribution has severely drifted! PSI = 0.42 (Threshold 0.20). P-value < 0.001.")
        else:
            st.success("🟢 **SYSTEM HEALTHY:** All features within nominal statistical boundaries (PSI < 0.10).")

        # Real-World Perspectives
        self.render_perspectives(
            business_pov=(
                "<b>Preventing Ground-Truth Lag Blindsiding:</b> Ground truth churn labels take 30 to 90 days "
                "to materialize after an inference decision. If an e-commerce or SaaS company relies only on revenue "
                "or cancellation reports, the business will bleed customers for an entire fiscal quarter before "
                "anyone discovers the model was failing. Feature drift alerts detect decay on day 1."
            ),
            technical_pov=(
                r"<b>Statistical Distance Metrics:</b> 1. <b>Population Stability Index (PSI):</b> Quantifies difference "
                r"in binned frequency distributions: $\sum (P_i - Q_i) \cdot \ln(P_i / Q_i)$. Thresholds: $<0.1$ stable, "
                r"$0.1-0.2$ moderate shift, $\ge 0.2$ severe drift. 2. <b>Kolmogorov-Smirnov (KS):</b> Non-parametric test "
                r"measuring maximum vertical distance between empirical cumulative distribution functions (eCDFs) with p-value."
            ),
            real_world_case=(
                "During March 2020 (COVID-19 onset), automated inventory and supply chain forecasting models worldwide "
                "failed simultaneously because consumer purchase distributions shifted overnight. Companies with statistical "
                "drift monitoring detected the regime shift within 24 hours and switched to rule-based failovers."
            )
        )

        # Panel 6: Under the Hood
        if st.session_state.get("show_code", True):
            st.markdown("#### 6. UNDER THE HOOD: Production Observability & Drift Suite")
            tab_evidently, tab_psi_math, tab_pagerduty = st.tabs([
                "📊 Evidently AI Drift Report",
                "📐 PSI & KS Mathematical Engine",
                "🚨 PagerDuty Alert Webhook"
            ])

            with tab_evidently:
                st.code("""from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset

# Generate automated visual HTML drift report
report = Report(metrics=[
    DataDriftPreset(drift_share=0.25),
    TargetDriftPreset()
])

report.run(reference_data=baseline_training_df, current_data=production_serving_df)
report.save_html("reports/drift_report.html")
print("Drift report published to S3 monitoring bucket!")""", language="python")

            with tab_psi_math:
                st.code("""import numpy as np
from scipy import stats

def compute_psi(baseline: np.ndarray, target: np.ndarray, num_bins: int = 10) -> float:
    \"\"\"Compute Population Stability Index between baseline and current production.\"\"\"
    quantiles = np.linspace(0, 100, num_bins + 1)
    bins = np.percentile(baseline, quantiles)
    bins[0], bins[-1] = -np.inf, np.inf
    
    base_counts = np.histogram(baseline, bins=bins)[0]
    target_counts = np.histogram(target, bins=bins)[0]
    
    # Smooth to avoid division by zero
    base_pct = (base_counts + 1e-4) / (len(baseline) + 1e-4 * num_bins)
    target_pct = (target_counts + 1e-4) / (len(target) + 1e-4 * num_bins)
    
    return float(np.sum((target_pct - base_pct) * np.log(target_pct / base_pct)))""", language="python")

            with tab_pagerduty:
                st.code("""import requests

def send_pagerduty_drift_alert(feature_name: str, psi_score: float):
    payload = {
        "routing_key": "pd-service-key-retention-ml",
        "event_action": "trigger",
        "payload": {
            "summary": f"CRITICAL DATA DRIFT: Feature '{feature_name}' PSI={psi_score:.3f} exceeds threshold 0.20",
            "severity": "error",
            "source": "neonbyte-production-monitoring",
            "custom_details": {
                "metric": "PSI",
                "value": psi_score,
                "dashboard": "https://grafana.neonbyte.internal/d/churn-drift"
            }
        }
    }
    requests.post("https://events.pagerduty.com/v2/enqueue", json=payload)""", language="python")

        # Panel 7: Result
        render_neon_card(
            "7. RESULT",
            "Continuous statistical observability configured. The platform actively detects distribution shifts before customer churn spikes go unnoticed.",
            color_variant="green"
        )

        # Panel 8: Why This Matters
        render_neon_card(
            "8. WHY THIS MATTERS",
            "<b>Silent model decay is the most dangerous failure mode in AI.</b> By measuring PSI and KS-tests on incoming features, you detect problems days or weeks before true labels arrive.",
            color_variant="cyan"
        )

        # Panel 9: Next
        st.info("🔜 **Next Mission:** A model can perform well on average while failing marginalized subgroups. Let's perform an algorithmic fairness and bias audit.")
        self.render_navigation_footer()

"""
MLOpsHub: Production Quest - Mission 08: Manage Features & Avoid Skew

Role: ML Engineer
Desk: Data platform workstation with schema catalogs and real-time streaming dashboards.
Teaches: Feature Stores, Training-Serving Skew, point-in-time correctness, feature reuse.
"""

import streamlit as st
import pandas as pd
from src.features.feature_store import FeatureStore
from src.missions.base_mission import BaseMission
from src.theme import render_neon_card, render_terminal


class Mission08(BaseMission):
    """Mission 08 Implementation."""

    def __init__(self) -> None:
        super().__init__(
            mission_id="m08",
            number_str="08",
            title="Manage Features & Avoid Skew",
            role_name="ML Engineer",
            role_emoji="🏪",
            desk_desc="Data infrastructure desk with SQL consoles, Kafka stream meters, and feature catalog binders.",
            badge_name="Feature Architect",
            xp_award=140
        )

    def render(self) -> None:
        """Render Mission 08 UI components."""
        story = (
            "**Monday, 11:15 AM (Next Sprint)**<br>"
            "ChurnGuard is preparing for its production release. However, a customer reported a bizarre bug: "
            "she received an urgent email saying she was a '98% churn risk', even though she just logged in and upgraded! "
            "You investigate: In training, the data scientist wrote SQL that averaged spend over 30 days. "
            "In production, the backend engineering team re-implemented the feature in Java by multiplying the last 7 days of spend by 4. "
            "Because of a recent flash sale, the two calculations diverged by 68%! "
            "This is the silent killer of ML systems: **Training-Serving Skew**."
        )
        objective = (
            "Diagnose the training-serving discrepancy. Deploy a centralized Feature Store to ensure "
            "the EXACT same transformation logic is used for offline batch training and online low-latency inference."
        )
        self.render_standard_header(story, objective)

        self.render_instructor_notes(
            objective="Help students understand Training-Serving Skew and the critical role of a centralized Feature Store (Feast, Hopsworks, Tecton).",
            talking_points=[
                "Training-Serving Skew occurs when the feature engineering code in training differs from the code running in production.",
                "Why it happens: Data scientists write Python/Pandas in notebooks; software engineers re-write it in Java/Go/C++ for low-latency APIs.",
                "The dual interface of a Feature Store: Batch API (point-in-time SQL for model training) and Online API (Redis/Cassandra key-value lookup for <10ms serving)."
            ],
            questions=[
                "Why can't our production API just run pandas code to recalculate 3 years of transaction history on every user click?",
                "What is 'data leakage in time' (Point-in-Time correctness) and how does a feature store prevent it?"
            ],
            expected_answers=[
                "Latency! Recalculating raw logs in pandas takes seconds/minutes; online serving requires sub-20ms response times.",
                "Joining future features with past training records corrupts the model; feature stores provide time-travel joins."
            ],
            misconceptions=[
                "Thinking a Feature Store is just a standard SQL database (it solves point-in-time joins, entity keys, and dual online/offline access).",
                "Assuming data drift and feature skew are the same thing (skew is an implementation discrepancy; drift is real-world change)."
            ],
            deep_dive="Explain the Feast / Hopsworks architecture: Offline store (Parquet/Snowflake) + Online store (Redis/DynamoDB).",
            skip_tip="Examine the Training vs Serving Discrepancy comparison table below."
        )

        # Panel 4: Learn
        learn_html = """
        <b>The Feature Store Blueprint:</b><br>
        • <b>Single Source of Transformation Truth:</b> Features are defined once in code.<br>
        • <b>Offline Store:</b> High-throughput historical batch data for model training.<br>
        • <b>Online Store:</b> Low-latency key-value store (e.g., Redis) for millisecond inference.<br>
        • <b>Eliminates Skew:</b> The same feature definition serves both training and production.
        """
        render_neon_card("4. LEARN: WHAT IS A FEATURE STORE?", learn_html, color_variant="purple")

        # Panel 5: Do
        st.markdown("#### 5. DO: Inspect Feature Catalog & Diagnose Skew")

        tab_catalog, tab_skew = st.tabs(["📋 Centralized Feature Catalog", "⚠️ Training-Serving Skew Simulation"])

        with tab_catalog:
            st.dataframe(FeatureStore.list_features(), use_container_width=True)

        with tab_skew:
            skew_data = FeatureStore.simulate_skew_scenario()
            st.error(f"🚨 **Discrepancy Detected in Feature:** `{skew_data['feature_name']}`")
            st.markdown(f"**Training logic:** `{skew_data['training_definition']}`")
            st.markdown(f"**Production logic:** `{skew_data['serving_definition']}`")
            st.caption(skew_data["discrepancy_cause"])

            st.dataframe(pd.DataFrame(skew_data["samples"]), use_container_width=True)

            if st.button("🔗 Enforce Single Feature Store Transformation (Sync Code)", type="primary"):
                st.success("✅ Feature Store synchronization active! Production microservice now queries the unified online feature store. Discrepancy eliminated (0.0% skew)!")

        # Real-World Perspectives
        self.render_perspectives(
            business_pov=(
                "<b>Eliminating Silent Financial Hemorrhage:</b> Training-serving skew is the most common reason "
                "models that look brilliant in offline notebooks fail in production. When an e-commerce or SaaS model "
                "calculates features inconsistently in real-time, it can misprice goods, decline good credit cards, "
                "or spam loyal accounts with cancellation discounts, directly eroding customer lifetime value."
            ),
            technical_pov=(
                "<b>Dual Storage Architecture (Offline vs Online):</b> Feast decouples the storage layers. "
                "The <b>Offline Store</b> (Snowflake, BigQuery, Parquet) handles high-throughput point-in-time time-travel joins "
                "to prevent data leakage during training. The <b>Online Store</b> (Redis, DynamoDB, Cassandra) provides sub-5ms "
                "key-value lookup during live user inference. Both read from the same declarative Python feature definition."
            ),
            real_world_case=(
                "Uber developed Michelangelo (the original industry feature store) after discovering that over 30 teams "
                "were independently re-implementing <code>driver_acceptance_rate</code> in ad-hoc SQL, Python, and C++, "
                "causing massive prediction drift across ride-hailing dispatch systems."
            )
        )

        # Panel 6: Under the Hood
        if st.session_state.get("show_code", True):
            st.markdown("#### 6. UNDER THE HOOD: Production Feast Feature Store Code & Config")
            tab_yaml, tab_defs, tab_serving, tab_feast_cli = st.tabs([
                "📄 feature_store.yaml",
                "🐍 definitions.py (Feast Entities & Views)",
                "⚡ fetch_online.py (Live <5ms Serving)",
                "💻 Real Production CLI Runbook"
            ])

            with tab_yaml:
                st.code("""# feature_store.yaml - Feast Configuration
project: churnguard_feature_repo
registry: s3://neonbyte-mlops-artifacts/feast/registry.pb
provider: local
offline_store:
  type: file
online_store:
  type: redis
  connection_string: redis://prod-redis-cluster.internal:6379""", language="yaml")

            with tab_defs:
                st.code("""from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource, ValueType
from feast.types import Float64, Int64, String

# 1. Define Primary Entity Key
customer = Entity(
    name="customer_id",
    value_type=ValueType.STRING,
    description="Unique customer identifier"
)

# 2. Define Batch Data Source
billing_source = FileSource(
    path="data/churn_v3_prod.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp"
)

# 3. Define Feature View (Shared between Training & Serving)
customer_billing_stats = FeatureView(
    name="customer_billing_stats",
    entities=[customer],
    ttl=timedelta(days=90),
    schema=[
        Field(name="customer_monthly_spend", dtype=Float64),
        Field(name="avg_support_calls_90d", dtype=Int64),
        Field(name="contract_type", dtype=String),
    ],
    online=True,
    source=billing_source,
    tags={"team": "retention_ml", "tier": "tier-1"}
)""", language="python")

            with tab_serving:
                st.code("""from feast import FeatureStore

# Initialize Feature Store using remote registry
store = FeatureStore(repo_path=".")

# Ultra-low latency online lookup for serving (<5ms)
feature_vector = store.get_online_features(
    features=[
        "customer_billing_stats:customer_monthly_spend",
        "customer_billing_stats:avg_support_calls_90d",
        "customer_billing_stats:contract_type"
    ],
    entity_rows=[{"customer_id": "CUST-10023"}]
).to_dict()

print("Fetched Online Features:", feature_vector)""", language="python")

            with tab_feast_cli:
                st.code("""# 1. Register feature definitions into centralized registry
feast apply

# 2. Materialize historical records into online Redis store
feast materialize-incremental $(date -u +%Y-%m-%dT%H:%M:%S)

# 3. Inspect registered feature views and schemas via web UI
feast ui --port 8888""", language="bash")

        if st.session_state.get("show_terminal", True):
            render_terminal(
                "feast apply && feast materialize-incremental $(date -u +%Y-%m-%dT%H:%M:%S)",
                "Applying entity customer_id\n"
                "Applying feature view customer_billing_stats\n"
                "Materializing 4 feature views to online store (redis://prod-redis-cluster:6379)...\n"
                "[SUCCESS] 12,500 customer records materialized in 1.4s. Online serving ready."
            )

        # Panel 7: Result
        render_neon_card(
            "7. RESULT",
            "Centralized feature store registered. Training pipelines and live API endpoints now draw from the exact same feature definitions, completely preventing training-serving skew.",
            color_variant="green"
        )

        # Panel 8: Why This Matters
        render_neon_card(
            "8. WHY THIS MATTERS",
            "Training-serving skew is insidious because models don't crash when it happens—they simply output subtle, incorrect predictions that burn customer trust while metrics look fine on paper.",
            color_variant="cyan"
        )

        # Panel 9: Next
        st.info("🔜 **Next Mission:** Before deploying code and features, we must test them. How do we test an ML system beyond traditional unit tests? Enter ML Testing.")
        self.render_navigation_footer()

"""
MLOpsHub: Production Quest - Lightweight Feature Store Engine

This module implements an in-memory/SQLite feature store registry:
- Feature view definitions and schema metadata
- Point-in-time feature retrieval for training datasets
- Low-latency online feature retrieval for serving
- Training-serving skew detection and discrepancy calculation
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
import pandas as pd


class FeatureStore:
    """Lightweight educational Feature Store for ChurnGuard."""

    FEATURE_REGISTRY: List[Dict[str, Any]] = [
        {
            "feature_name": "customer_monthly_spend",
            "feature_view": "customer_billing_stats",
            "entity": "customer_id",
            "data_type": "Float64",
            "version": "v3",
            "owner": "Data Platform Team",
            "transformation": "AVG(daily_spend) * 30.0 (trailing 30 days)",
            "updated_at": "Today, 10:42 AM",
            "consumers": ["ChurnGuard v3", "UpsellRecommender v1"],
            "description": "Standardized average 30-day normalized billing spend."
        },
        {
            "feature_name": "avg_support_calls_90d",
            "feature_view": "customer_support_metrics",
            "entity": "customer_id",
            "data_type": "Int64",
            "version": "v2",
            "owner": "Customer Ops Analytics",
            "transformation": "COUNT(ticket_id) WHERE status IN ('resolved', 'closed')",
            "updated_at": "Today, 09:15 AM",
            "consumers": ["ChurnGuard v3"],
            "description": "Rolling 90-day volume of inbound customer service calls."
        },
        {
            "feature_name": "spend_to_tenure_ratio",
            "feature_view": "customer_engagement_ratios",
            "entity": "customer_id",
            "data_type": "Float64",
            "version": "v3",
            "owner": "ML Feature Team",
            "transformation": "monthly_spend / GREATEST(tenure, 1)",
            "updated_at": "Today, 10:42 AM",
            "consumers": ["ChurnGuard v3"],
            "description": "Ratio of spend velocity to customer relationship age."
        },
        {
            "feature_name": "is_high_risk_contract",
            "feature_view": "contract_policy_flags",
            "entity": "customer_id",
            "data_type": "Boolean",
            "version": "v1",
            "owner": "Risk & Compliance",
            "transformation": "CASE WHEN contract_type = 'Month-to-month' THEN 1 ELSE 0 END",
            "updated_at": "Yesterday, 17:00 PM",
            "consumers": ["ChurnGuard v2", "ChurnGuard v3"],
            "description": "Binary flag indicating flexible cancellation risk."
        }
    ]

    @staticmethod
    def list_features() -> pd.DataFrame:
        """Return feature registry overview as a pandas DataFrame."""
        rows = []
        for feat in FeatureStore.FEATURE_REGISTRY:
            rows.append({
                "Feature Name": feat["feature_name"],
                "Entity": feat["entity"],
                "Type": feat["data_type"],
                "Version": feat["version"],
                "Owner": feat["owner"],
                "Updated": feat["updated_at"],
                "Used By": ", ".join(feat["consumers"])
            })
        return pd.DataFrame(rows)

    @staticmethod
    def simulate_skew_scenario() -> Dict[str, Any]:
        """
        Simulate the Training-Serving Skew trap:
        Training calculates monthly_spend using calendar month average.
        Production ad-hoc script calculates it using last 7 days multiplied by 4.
        """
        sample_customers = [
            {"customer_id": "CUST-10023", "training_val": 84.50, "serving_val": 142.00, "skew_pct": 68.0},
            {"customer_id": "CUST-10045", "training_val": 110.00, "serving_val": 185.20, "skew_pct": 68.4},
            {"customer_id": "CUST-10088", "training_val": 45.20, "serving_val": 76.00, "skew_pct": 68.1},
            {"customer_id": "CUST-10112", "training_val": 95.00, "serving_val": 160.50, "skew_pct": 68.9},
        ]
        return {
            "feature_name": "customer_monthly_spend",
            "training_definition": "AVG(daily_spend) over past 30 days (Batch SQL)",
            "serving_definition": "SUM(past_7_days_spend) * 4.3 (Ad-hoc backend microservice)",
            "discrepancy_cause": "Black Friday promotional weekend distorted 7-day spend, causing serving to overestimate spend by ~68%!",
            "samples": sample_customers,
            "impact": "Model falsely flags healthy loyal customers as imminent churners due to inflated monthly spend."
        }

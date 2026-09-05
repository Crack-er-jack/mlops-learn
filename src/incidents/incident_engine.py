"""
MLOpsHub: Production Quest - Incident Simulation Engine

This module defines deterministic production incidents for ChurnGuard:
- Incident A (INC-042): Upstream feature transformation bug causing monthly_spend drift
- Incident B (INC-055): Upstream schema change (renamed column / type mismatch)
- Incident C (INC-071): Training-serving skew in feature calculation
- Incident D (INC-089): Unauthorized bad model promotion to production
- Incident E (INC-103): Data quality pipeline failure injecting corrupted negative values
"""

from typing import Any, Dict, List


class IncidentEngine:
    """Repository of production failure scenarios and incident metadata."""

    INCIDENTS: Dict[str, Dict[str, Any]] = {
        "A": {
            "id": "INC-042",
            "title": "Severe Prediction Accuracy Degradation in ChurnGuard v3",
            "type": "Feature Distribution Drift",
            "severity": "P1 - CRITICAL",
            "started_at": "14:32 UTC",
            "model_version": "ChurnGuard v3.0",
            "f1_before": 0.84,
            "f1_after": 0.68,
            "latency_ms": "18.4ms (Normal)",
            "error_rate": "0.02% (No 500 crashes!)",
            "symptom": (
                "Retention marketing team reports that ChurnGuard is suddenly flagging 3x more "
                "customers as high churn risk. Customers who just signed 2-year contracts are receiving "
                "frantic emergency discount emails. The API is returning HTTP 200 OK with low latency, "
                "but business KPI accuracy has plummeted."
            ),
            "evidence_logs": [
                "[10:17 UTC] PR #412 merged into data-pipeline: 'Refactor billing spend currency conversion' (Author: DataPlatform)",
                "[11:00 UTC] Airflow DAG `daily_feature_aggregation` executed successfully.",
                "[14:31 UTC] Monitoring detected sudden spike in `monthly_spend` (Mean shifted from $87.20 to $214.80).",
                "[14:32 UTC] Customer churn alert threshold triggered: F1 dropped from 0.84 to 0.68.",
                "[14:35 UTC] PagerDuty alert dispatched to SRE On-Call."
            ],
            "suspect_nodes": [
                {"name": "monthly_spend feature", "category": "Feature Store", "confidence": 0.92, "status": "CRITICAL"},
                {"name": "Data Pipeline (PR #412)", "category": "ETL Pipeline", "confidence": 0.78, "status": "SUSPICIOUS"},
                {"name": "Serving API Container", "category": "Deployment", "confidence": 0.14, "status": "HEALTHY"},
                {"name": "Model Weights v3", "category": "Model Registry", "confidence": 0.11, "status": "HEALTHY"},
                {"name": "Raw Database", "category": "Data Source", "confidence": 0.08, "status": "HEALTHY"}
            ],
            "root_cause_explanation": (
                "1. PR #412 refactored the currency calculation in the billing pipeline but accidentally "
                "multiplied European transactions twice by exchange rates (EUR to USD conversion applied double).\n"
                "2. As a result, `monthly_spend` distribution exploded upwards (PSI = 0.42, KS p-value < 0.001).\n"
                "3. Because high monthly spend strongly correlates with churn in the trained model weights, "
                "the model falsely flagged healthy customers as imminent churners."
            ),
            "remediation_plan": [
                "Revert PR #412 in Git repository (commit 7b2d8e1).",
                "Re-run feature engineering pipeline for `customer_monthly_spend`.",
                "Verify statistical distribution aligns with baseline training distribution (PSI < 0.05).",
                "Perform shadow validation against production traffic.",
                "Restore automated retention email triggers."
            ]
        },
        "B": {
            "id": "INC-055",
            "title": "Silent API Inference Failures Post Upstream Schema Migration",
            "type": "Upstream Schema Change",
            "severity": "P2 - HIGH",
            "started_at": "08:15 UTC",
            "model_version": "ChurnGuard v3.0",
            "f1_before": 0.84,
            "f1_after": 0.52,
            "latency_ms": "24.1ms",
            "error_rate": "12.4% (Unhandled Nulls)",
            "symptom": "Upstream database renamed column `support_calls` to `customer_tickets_count` without notice.",
            "evidence_logs": [
                "[08:00 UTC] DB Migration #89 completed on core postgres cluster.",
                "[08:15 UTC] Model imputing default 0 calls for missing column; predictions degraded."
            ],
            "suspect_nodes": [
                {"name": "Raw Data Schema", "category": "Data Source", "confidence": 0.88, "status": "CRITICAL"},
                {"name": "Data Pipeline", "category": "ETL Pipeline", "confidence": 0.72, "status": "SUSPICIOUS"},
                {"name": "Model Registry", "category": "Model Registry", "confidence": 0.10, "status": "HEALTHY"}
            ],
            "root_cause_explanation": "Column rename broke feature extractor contract; model defaulted to 0 support calls.",
            "remediation_plan": ["Deploy schema adapter in ETL pipeline", "Add contract validation in CI tests"]
        },
        "C": {
            "id": "INC-071",
            "title": "Online Inference Prediction Drift Due to Window Mismatch",
            "type": "Training-Serving Skew",
            "severity": "P1 - CRITICAL",
            "started_at": "11:20 UTC",
            "model_version": "ChurnGuard v3.0",
            "f1_before": 0.84,
            "f1_after": 0.61,
            "latency_ms": "16.2ms",
            "error_rate": "0.00%",
            "symptom": "Online service calculates 7-day spend while training used 30-day trailing averages.",
            "evidence_logs": [
                "[11:15 UTC] Microservice update deployed ad-hoc feature calculation script.",
                "[11:20 UTC] Massive divergence detected between offline benchmark and online serving."
            ],
            "suspect_nodes": [
                {"name": "Online Feature Service", "category": "Feature Store", "confidence": 0.94, "status": "CRITICAL"},
                {"name": "Model Weights", "category": "Model Registry", "confidence": 0.12, "status": "HEALTHY"}
            ],
            "root_cause_explanation": "Training-serving skew occurred because logic was duplicated across SQL and Python microservice.",
            "remediation_plan": ["Unify online and offline feature calculation via Feature Store", "Enforce point-in-time joins"]
        },
        "D": {
            "id": "INC-089",
            "title": "Premature Deployment of Unvalidated Experimental Model",
            "type": "Unauthorized Model Promotion",
            "severity": "P1 - CRITICAL",
            "started_at": "16:40 UTC",
            "model_version": "ChurnGuard v4-experimental",
            "f1_before": 0.84,
            "f1_after": 0.58,
            "latency_ms": "85.0ms (4x spike)",
            "error_rate": "1.2%",
            "symptom": "An unvalidated deep neural network was promoted directly to production bypassing CI gates.",
            "evidence_logs": [
                "[16:35 UTC] Manual tag update in Model Registry to 'Production' by junior intern.",
                "[16:40 UTC] High latency alarms fired across Kubernetes serving pods."
            ],
            "suspect_nodes": [
                {"name": "Model Registry Stage", "category": "Model Registry", "confidence": 0.96, "status": "CRITICAL"},
                {"name": "CI/CD Promotion Gate", "category": "DevOps", "confidence": 0.82, "status": "SUSPICIOUS"},
                {"name": "Data Pipeline", "category": "ETL Pipeline", "confidence": 0.05, "status": "HEALTHY"}
            ],
            "root_cause_explanation": "Manual override of model stage without passing automated CI/CD accuracy & latency gates.",
            "remediation_plan": ["Immediate rollback to ChurnGuard v3 in Model Registry", "Lock down stage transition RBAC permissions"]
        },
        "E": {
            "id": "INC-103",
            "title": "Negative Spends Injected from Unsanitized Partner Ingestion",
            "type": "Data Quality Corruption",
            "severity": "P2 - HIGH",
            "started_at": "06:10 UTC",
            "model_version": "ChurnGuard v3.0",
            "f1_before": 0.84,
            "f1_after": 0.65,
            "latency_ms": "19.0ms",
            "error_rate": "3.5%",
            "symptom": "New B2B partner feed introduced refunds as negative monthly spend (-$2300).",
            "evidence_logs": [
                "[06:00 UTC] Ingestion job pulled raw partner batch #2041.",
                "[06:10 UTC] Model predictions wildly unstable on enterprise customer accounts."
            ],
            "suspect_nodes": [
                {"name": "Raw Ingestion Feed", "category": "Data Source", "confidence": 0.91, "status": "CRITICAL"},
                {"name": "Data Quality Gates", "category": "Data Validation", "confidence": 0.85, "status": "SUSPICIOUS"}
            ],
            "root_cause_explanation": "Data quality test for non-negative spend was omitted from the partner ETL job.",
            "remediation_plan": ["Filter refund records into separate adjustments table", "Re-enable data validation assertions"]
        }
    }

    @staticmethod
    def get_incident(incident_key: str = "A") -> Dict[str, Any]:
        """Retrieve full incident report by key."""
        return IncidentEngine.INCIDENTS.get(incident_key, IncidentEngine.INCIDENTS["A"])

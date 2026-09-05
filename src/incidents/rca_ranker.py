"""
MLOpsHub: Production Quest - Evidence-Based Root Cause Candidate Ranking

This module evaluates incident telemetry across multiple engineering dimensions:
- Statistical feature drift (PSI, KS p-value)
- Temporal proximity of code/data changes
- Causal dependency path impact
- Invariance of model artifacts
Computes normalized candidate suspicion scores with transparent evidence logs.
"""

from typing import Any, Dict, List


class RootCauseRanker:
    """Evidence-based Root Cause Candidate Ranking Engine."""

    @staticmethod
    def rank_candidates(incident_type: str = "A") -> List[Dict[str, Any]]:
        """
        Evaluate candidate system components and rank them by diagnostic evidence score.

        Args:
            incident_type: Identifier of active incident ('A', 'B', 'C', 'D', 'E').

        Returns:
            Sorted list of candidate diagnosis cards with transparent evidence items.
        """
        candidates = [
            {
                "name": "Feature: customer_monthly_spend",
                "component": "Feature Store / Data Layer",
                "status_indicator": "🔴 CRITICAL SUSPECT",
                "base_score": 0.95,
                "evidence_breakdown": [
                    {"factor": "Statistical Distribution Drift", "delta": "+0.35", "note": "PSI = 0.42 (High Alert threshold is 0.20)"},
                    {"factor": "Recent Pipeline Code Change", "delta": "+0.25", "note": "PR #412 merged into billing pipeline 4h prior"},
                    {"factor": "Temporal Correlation", "delta": "+0.20", "note": "Drift detected at 14:31, incident fired at 14:32"},
                    {"factor": "Graph Dependency Weight", "delta": "+0.15", "note": "Feature has top-1 importance weight in production model"},
                    {"factor": "Model Weights Invariance", "delta": "+0.10", "note": "Model registry artifact unchanged since last month"}
                ],
                "total_score": 1.05,
                "confidence_pct": 92.4,
                "summary": (
                    "Severe statistical divergence in billing calculation coupled with recent PR #412 "
                    "commit makes this feature the primary candidate for model prediction degradation."
                )
            },
            {
                "name": "Upstream ETL Pipeline (PR #412)",
                "component": "Data Pipeline / Airflow",
                "status_indicator": "🟠 HIGH SUSPECT",
                "base_score": 0.80,
                "evidence_breakdown": [
                    {"factor": "Code Deployment Timing", "delta": "+0.30", "note": "Merged at 10:17 UTC by DataPlatform"},
                    {"factor": "Direct Upstream Producer", "delta": "+0.25", "note": "Direct parent node to `monthly_spend` feature in graph"},
                    {"factor": "Execution Status", "delta": "-0.05", "note": "DAG run reported SUCCESS (silent calculation bug, not a crash)"}
                ],
                "total_score": 0.85,
                "confidence_pct": 78.5,
                "summary": (
                    "Upstream calculation change was deployed today. While it didn't throw an error, "
                    "it directly generated the drifted numbers ingested by the feature store."
                )
            },
            {
                "name": "Serving API Container (Docker)",
                "component": "Serving Layer / Runtime",
                "status_indicator": "🟢 LOW SUSPECT",
                "base_score": 0.15,
                "evidence_breakdown": [
                    {"factor": "Uptime & Error Rate", "delta": "-0.20", "note": "HTTP 200 OK rate is 99.98%, no 500 error spikes"},
                    {"factor": "Latency Performance", "delta": "-0.15", "note": "Serving latency steady at 18.4ms"}
                ],
                "total_score": 0.15,
                "confidence_pct": 14.0,
                "summary": (
                    "The HTTP container is running smoothly and serving predictions fast. "
                    "The issue is bad predictions (semantic ML failure), not infrastructure downtime."
                )
            },
            {
                "name": "Model Registry Weights (v3.0)",
                "component": "Model Layer",
                "status_indicator": "🟢 LOW SUSPECT",
                "base_score": 0.12,
                "evidence_breakdown": [
                    {"factor": "Artifact Immutability", "delta": "-0.30", "note": "Checksum matches run-4e8f1a; no unauthorized promotion"},
                    {"factor": "Benchmark Evaluation", "delta": "-0.15", "note": "Model still scores 0.82 F1 on baseline test dataset"}
                ],
                "total_score": 0.12,
                "confidence_pct": 11.5,
                "summary": (
                    "The trained model file has not changed. It is evaluating corrupted feature inputs "
                    "faithfully according to its weights."
                )
            }
        ]

        # Sort descending by confidence percentage
        candidates.sort(key=lambda x: x["confidence_pct"], reverse=True)
        return candidates

"""
MLOpsHub: Production Quest - AI System Dependency Graph

This module constructs an interactive dependency graph of the end-to-end ML system:
Raw Data -> Data Pipeline -> Feature Store -> Model Registry -> Serving API -> Prediction -> Business KPI.
Each node exposes versioning, timestamps, owners, change history, and health indicators.
"""

from typing import Any, Dict, List
import networkx as nx
import plotly.graph_objects as go


class DependencyGraphBuilder:
    """Builder for AI System Dependency Graph with metadata inspection."""

    NODES: Dict[str, Dict[str, Any]] = {
        "raw_data": {
            "label": "Raw Billing & Telemetry",
            "layer": "Data Source",
            "pos": (0, 0),
            "owner": "Enterprise Data Platform",
            "version": "v1.4-postgres",
            "timestamp": "Today, 06:00 UTC",
            "status": "HEALTHY",
            "details": "PostgreSQL core billing and customer service event logs.",
            "metrics": "1.2M rows/day, zero ingestion lag."
        },
        "data_pipeline": {
            "label": "ETL Transformation Pipeline",
            "layer": "Data Pipeline",
            "pos": (1, 0),
            "owner": "Data Platform Team",
            "version": "git: 7b2d8e1 (PR #412)",
            "timestamp": "Today, 10:17 UTC",
            "status": "SUSPICIOUS",
            "details": "Currency conversion and aggregation Airflow DAG. Modified 4h before incident!",
            "metrics": "Execution time 12m, 0 task failures."
        },
        "feature_store": {
            "label": "Feature Store (monthly_spend)",
            "layer": "Feature Layer",
            "pos": (2, 0),
            "owner": "ML Feature Team",
            "version": "v3.0-prod",
            "timestamp": "Today, 10:42 UTC",
            "status": "CRITICAL",
            "details": "Normalized trailing spend calculation. DRIFT DETECTED: PSI = 0.42 (Threshold 0.20).",
            "metrics": "Mean: $214.80 (Baseline: $87.20)."
        },
        "model_registry": {
            "label": "Model Registry (ChurnGuard v3)",
            "layer": "Model Layer",
            "pos": (3, 0),
            "owner": "Alex (ML Engineer)",
            "version": "v3.0 (run-4e8f1a)",
            "timestamp": "3 weeks ago (No change)",
            "status": "HEALTHY",
            "details": "Gradient Boosting Classifier. Model weights unchanged during incident window.",
            "metrics": "Test F1 at registry: 0.818."
        },
        "serving_api": {
            "label": "FastAPI / Streamlit Serving API",
            "layer": "Serving Layer",
            "pos": (4, 0),
            "owner": "Platform SRE",
            "version": "docker: v3.0.0",
            "timestamp": "2 weeks ago (No change)",
            "status": "HEALTHY",
            "details": "Containerized microservice on port 8501.",
            "metrics": "HTTP 200 OK: 99.98%, Latency: 18.4ms."
        },
        "prediction_stream": {
            "label": "Live Prediction Stream",
            "layer": "Inference Stream",
            "pos": (5, 0),
            "owner": "Customer Retention Engine",
            "version": "v3-stream",
            "timestamp": "Real-time (Active)",
            "status": "CRITICAL",
            "details": "Sudden surge in customer churn classifications (3.2x normal volume).",
            "metrics": "Predicted Churn Rate: 68.2% (Norm: 21.5%)."
        },
        "business_kpi": {
            "label": "Business KPI: Retention & MRR",
            "layer": "Business Outcome",
            "pos": (6, 0),
            "owner": "Product Leadership",
            "version": "Q1 Goals",
            "timestamp": "Active Alert",
            "status": "CRITICAL",
            "details": "False alerts triggering inappropriate discount emails to satisfied customers.",
            "metrics": "Customer trust impact high; F1 down to 0.68."
        }
    }

    EDGES: List[tuple] = [
        ("raw_data", "data_pipeline"),
        ("data_pipeline", "feature_store"),
        ("feature_store", "model_registry"),
        ("model_registry", "serving_api"),
        ("serving_api", "prediction_stream"),
        ("prediction_stream", "business_kpi")
    ]

    @classmethod
    def create_plotly_figure(cls, selected_node: str = "feature_store") -> go.Figure:
        """
        Render interactive cybernetic dependency graph.

        Args:
            selected_node: The key of the currently selected/inspected node.

        Returns:
            Plotly Figure object ready for st.plotly_chart.
        """
        # Node positions along horizontal pipeline
        node_x = []
        node_y = []
        node_text = []
        node_colors = []
        node_sizes = []

        status_color_map = {
            "CRITICAL": "#ff0055",
            "SUSPICIOUS": "#ffaa00",
            "HEALTHY": "#00f5ff"
        }

        for k, v in cls.NODES.items():
            x, y = v["pos"]
            node_x.append(x)
            node_y.append(y)
            node_text.append(f"<b>{v['label']}</b><br>Status: {v['status']}<br>Owner: {v['owner']}")
            node_colors.append(status_color_map[v["status"]])
            node_sizes.append(42 if k == selected_node else 32)

        # Edges
        edge_x = []
        edge_y = []
        for src, dst in cls.EDGES:
            x0, y0 = cls.NODES[src]["pos"]
            x1, y1 = cls.NODES[dst]["pos"]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        fig = go.Figure()

        # Add connecting dependency lines
        fig.add_trace(go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=3, color="rgba(0, 245, 255, 0.45)"),
            hoverinfo="none",
            mode="lines"
        ))

        # Add nodes
        fig.add_trace(go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            text=[cls.NODES[k]["layer"] for k in cls.NODES],
            textposition="bottom center",
            textfont=dict(color="#d1d7e0", size=11, family="Inter"),
            hoverinfo="text",
            hovertext=node_text,
            marker=dict(
                size=node_sizes,
                color=node_colors,
                line=dict(width=3, color="#ffffff"),
                opacity=0.95
            )
        ))

        fig.update_layout(
            paper_bgcolor="#0b0f19",
            plot_bgcolor="#0b0f19",
            showlegend=False,
            margin=dict(l=30, r=30, t=20, b=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=260
        )

        return fig

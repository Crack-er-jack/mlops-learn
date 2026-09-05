"""
MLOpsHub: Production Quest - MLOps Universe Dynamic Concept Map

This module visualizes the interconnected tree of MLOps disciplines:
Data (Versioning, Quality, Features) -> Model (Tracking, Registry, Evaluation) ->
System (Testing, CI/CD, Deployment) -> Production (Monitoring, Governance) ->
Incidents -> RCA -> Remediation.
Nodes dynamically illuminate as missions are completed.
"""

import streamlit as st
import plotly.graph_objects as go


def render_concept_universe() -> None:
    """Render the MLOps Universe illuminated concept map."""
    st.markdown("### 🌌 The MLOps Universe")
    st.markdown(
        "MLOps is not a disconnected collection of tools. It is the engineering discipline "
        "required to reliably move ML from an experiment into a continuously changing production system. "
        "Nodes below **illuminate in neon cyan/green** as your team unlocks capabilities."
    )

    unlocked_caps = st.session_state.get("unlocked_capabilities", set())

    # Define concept nodes and their positions
    concepts = [
        {"id": "data_qual", "name": "Data Quality", "cap": "data_quality", "x": -2, "y": 2, "group": "DATA"},
        {"id": "data_ver", "name": "DVC Versioning", "cap": "data_versioning", "x": -2, "y": 1, "group": "DATA"},
        {"id": "feat_store", "name": "Feature Store", "cap": "feature_store", "x": -2, "y": 0, "group": "DATA"},

        {"id": "exp_track", "name": "MLflow Tracking", "cap": "experiment_tracking", "x": 0, "y": 2, "group": "MODEL"},
        {"id": "mod_reg", "name": "Model Registry", "cap": "model_registry", "x": 0, "y": 1, "group": "MODEL"},
        {"id": "fairness", "name": "Fairness & Explain", "cap": "fairness_audit", "x": 0, "y": 0, "group": "MODEL"},

        {"id": "testing", "name": "Pytest Quality", "cap": "ml_testing", "x": 2, "y": 2, "group": "SYSTEM"},
        {"id": "ci_cd", "name": "GitHub CI/CD", "cap": "ci_cd", "x": 2, "y": 1, "group": "SYSTEM"},
        {"id": "docker", "name": "Docker Packaging", "cap": "containerization", "x": 2, "y": 0, "group": "SYSTEM"},

        {"id": "serving", "name": "Production API", "cap": "production_serving", "x": 0, "y": -1.2, "group": "PROD"},
        {"id": "monitor", "name": "Drift Observability", "cap": "drift_monitoring", "x": -1.2, "y": -2.2, "group": "PROD"},
        {"id": "gov", "name": "Model Governance", "cap": "governance", "x": 1.2, "y": -2.2, "group": "PROD"},

        {"id": "graph", "name": "AI Dependency Graph", "cap": "dependency_graph", "x": -0.8, "y": -3.2, "group": "INCIDENT"},
        {"id": "rca", "name": "Evidence RCA & Fix", "cap": "rca_remediation", "x": 0.8, "y": -3.2, "group": "INCIDENT"},
    ]

    # Connections between concepts
    links = [
        ("data_qual", "data_ver"), ("data_ver", "feat_store"),
        ("exp_track", "mod_reg"), ("mod_reg", "fairness"),
        ("testing", "ci_cd"), ("ci_cd", "docker"),
        ("feat_store", "serving"), ("fairness", "serving"), ("docker", "serving"),
        ("serving", "monitor"), ("serving", "gov"),
        ("monitor", "graph"), ("graph", "rca")
    ]

    node_map = {c["id"]: c for c in concepts}

    edge_x = []
    edge_y = []
    for src_id, dst_id in links:
        s = node_map[src_id]
        d = node_map[dst_id]
        edge_x.extend([s["x"], d["x"], None])
        edge_y.extend([s["y"], d["y"], None])

    node_x = []
    node_y = []
    node_text = []
    node_colors = []

    for c in concepts:
        is_unlocked = c["cap"] in unlocked_caps
        node_x.append(c["x"])
        node_y.append(c["y"])
        status_txt = "🟢 UNLOCKED" if is_unlocked else "🔒 LOCKED (Complete Mission)"
        node_text.append(f"<b>{c['name']}</b><br>Group: {c['group']}<br>Status: {status_txt}")
        node_colors.append("#39ff14" if is_unlocked else "#374151")

    fig = go.Figure()

    # Edges
    fig.add_trace(go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(color="rgba(0, 245, 255, 0.3)", width=2),
        hoverinfo="none"
    ))

    # Nodes
    fig.add_trace(go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=[c["name"] for c in concepts],
        textposition="top center",
        textfont=dict(color="#f0f6fc", size=11, family="Inter"),
        hoverinfo="text",
        hovertext=node_text,
        marker=dict(
            size=30,
            color=node_colors,
            line=dict(color="#00f5ff", width=2),
            opacity=0.95
        )
    ))

    fig.update_layout(
        paper_bgcolor="#0b0f19",
        plot_bgcolor="#0b0f19",
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=520
    )

    st.plotly_chart(fig, use_container_width=True)

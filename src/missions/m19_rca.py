"""
MLOpsHub: Production Quest - Mission 19: Root Cause Analysis (AI Graph)

Role: Incident Commander
Desk: Root cause forensics center with interactive AI dependency graph and evidence ranker.
Teaches: AI System Dependency Graphs, Root Cause Candidate Ranking, multi-factor evidence synthesis.
"""

import streamlit as st
import pandas as pd
from src.incidents.dependency_graph import DependencyGraphBuilder
from src.incidents.rca_ranker import RootCauseRanker
from src.missions.base_mission import BaseMission
from src.theme import render_neon_card, render_terminal


class Mission19(BaseMission):
    """Mission 19 Implementation."""

    def __init__(self) -> None:
        super().__init__(
            mission_id="m19",
            number_str="19",
            title="Root Cause Analysis (AI Graph)",
            role_name="Incident Commander",
            role_emoji="🕸️",
            desk_desc="Diagnostic command station with illuminated system dependency graphs and evidence scoring consoles.",
            badge_name="Root Cause Detective",
            xp_award=170
        )

    def render(self) -> None:
        """Render Mission 19 UI components."""
        story = (
            "**Thursday, 15:05 UTC**<br>"
            "The executive team is demanding answers: *'Why did the model break? Was it the neural net? "
            "Was it the API? Who pushed what?'*<br>"
            "Modern AI systems are not isolated scripts; they are deeply interconnected dependency graphs. "
            "By mapping the end-to-end lineage from raw telemetry to business outcome, we can evaluate "
            "evidence across timestamps, code diffs, statistical drift, and dependency paths."
        )
        objective = (
            "Inspect the interactive AI System Dependency Graph. "
            "Examine candidate root causes ranked by the Evidence-Based Diagnostic Engine. "
            "Verify the exact causal mechanism connecting upstream PR #412 to customer churn false alarms."
        )
        self.render_standard_header(story, objective)

        self.render_instructor_notes(
            objective="Introduce students to systemic, evidence-based Root Cause Analysis for complex AI topologies.",
            talking_points=[
                "Why AI systems are harder to debug than microservices: The failure is often downstream from the change, separated by time and intermediate caches.",
                "The Dependency Graph: Raw Data ➔ Pipeline ➔ Feature ➔ Model ➔ API ➔ Prediction ➔ Business KPI.",
                "Evidence synthesis: Combining change timestamps (PR #412 at 10:17) + statistical drift (PSI=0.42 at 14:31) + model invariance = high diagnostic confidence.",
                "Transparency: We avoid claiming 'magic AI discovered the cause'. We present transparent candidate rankings backed by auditable evidence."
            ],
            questions=[
                "Why did the incident start at 14:32 if the breaking code was merged at 10:17?",
                "How does the dependency graph prevent us from wasting time debugging the Docker container or FastAPI code?"
            ],
            expected_answers=[
                "The ETL batch pipeline ran at 11:00, and it took several hours for active customer traffic to accumulate and trigger alerting thresholds.",
                "The graph shows the Serving API and Model nodes have zero recent changes and normal operational metrics."
            ],
            misconceptions=[
                "Assuming root cause analysis can be completely automated by a single black-box algorithm without human domain judgment.",
                "Confusing symptom (false positive churn emails) with root cause (upstream currency conversion multiplier bug)."
            ],
            deep_dive="Walk through the 5 diagnostic factors scored in the Evidence Breakdown table below.",
            skip_tip="Click on different nodes in the interactive graph to inspect their metadata."
        )

        # Panel 4: Learn
        learn_html = """
        <b>The AI System Dependency Topology:</b><br>
        • <b>Upstream:</b> Raw data sources and ETL pipelines (Airflow/Spark).<br>
        • <b>Intermediate:</b> Feature Store views and transformations.<br>
        • <b>Model:</b> Registered model weights and serialization artifacts.<br>
        • <b>Serving:</b> Container runtime and HTTP API endpoints.<br>
        • <b>Outcome:</b> Downstream business KPIs and automated action triggers.
        """
        render_neon_card("4. LEARN: AI TOPOLOGY & EVIDENCE RANKING", learn_html, color_variant="purple")

        # Panel 5: Do
        st.markdown("#### 5. DO: Interactive Dependency Graph & Candidate Ranking")

        st.markdown("##### 🕸️ AI System Dependency Graph (Click to Inspect Node):")
        selected_node = st.selectbox(
            "Select Graph Node to Inspect Lineage & Telemetry:",
            list(DependencyGraphBuilder.NODES.keys()),
            format_func=lambda k: f"{DependencyGraphBuilder.NODES[k]['label']} [{DependencyGraphBuilder.NODES[k]['status']}]"
        )

        fig = DependencyGraphBuilder.create_plotly_figure(selected_node=selected_node)
        st.plotly_chart(fig, use_container_width=True)

        # Node metadata card
        node_data = DependencyGraphBuilder.NODES[selected_node]
        node_status_color = {"CRITICAL": "#ff0055", "SUSPICIOUS": "#ffaa00", "HEALTHY": "#00f5ff"}[node_data["status"]]

        st.markdown(f"""
        <div style="background: #111827; border-left: 4px solid {node_status_color}; border-radius: 8px; padding: 14px; margin-bottom: 16px;">
            <div style="font-size: 1.1rem; font-weight: 700; color: #ffffff;">{node_data['label']}</div>
            <div style="font-size: 0.88rem; color: #9ca3af; margin-top: 4px;">
                <b>Layer:</b> {node_data['layer']} | <b>Owner:</b> {node_data['owner']} | <b>Version:</b> {node_data['version']}
            </div>
            <div style="font-size: 0.92rem; color: #d1d5db; margin-top: 6px;"><b>Health & Telemetry:</b> {node_data['details']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("##### 🔍 Evidence-Based Root Cause Candidate Ranking:")
        candidates = RootCauseRanker.rank_candidates()

        for c in candidates:
            with st.expander(f"{c['status_indicator']} — {c['name']} (Confidence: {c['confidence_pct']}%)", expanded=(c["confidence_pct"] > 80)):
                st.markdown(f"**Diagnostic Summary:** {c['summary']}")
                st.markdown("**Evidence Scoring Breakdown:**")
                st.dataframe(pd.DataFrame(c["evidence_breakdown"]), use_container_width=True)

        # Panel 6: Under the Hood
        if st.session_state.get("show_code", True):
            st.markdown("#### 6. UNDER THE HOOD: Causal Graph Diagnostic Engine")
            code_str = (
                "def evaluate_root_cause_candidates(graph, incident_telemetry):\n"
                "    candidates = []\n"
                "    for node in graph.nodes:\n"
                "        drift_score = compute_node_drift(node)\n"
                "        temporal_score = compute_time_proximity(node.last_change, incident.start_time)\n"
                "        dependency_weight = graph.get_downstream_impact_weight(node, 'business_kpi')\n"
                "        composite_score = (drift_score * 0.35) + (temporal_score * 0.30) + (dependency_weight * 0.20)\n"
                "        candidates.append({'node': node.id, 'score': composite_score})\n"
                "    return sorted(candidates, key=lambda x: x['score'], reverse=True)"
            )
            st.code(code_str, language="python")

        # Panel 7: Result
        render_neon_card(
            "7. RESULT",
            "Root cause isolated with 92.4% diagnostic confidence: <b>PR #412 in the upstream data pipeline introduced a currency conversion bug</b> that artificially doubled European monthly spend values, causing the feature store to deliver drifted inputs to an otherwise healthy model.",
            color_variant="green"
        )

        # Panel 8: Why This Matters
        render_neon_card(
            "8. WHY THIS MATTERS",
            "<b>AI systems fail at the boundaries between data engineering and machine learning.</b> A dependency graph turns chaotic war rooms into structured, evidence-backed scientific investigations.",
            color_variant="cyan"
        )

        # Panel 9: Next
        st.info("🔜 **Next Mission:** We know what broke! Now let's execute the remediation playbook: revert the commit, recompute features, verify drift, and restore service.")
        self.render_navigation_footer()

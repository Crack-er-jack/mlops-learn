"""
MLOpsHub: Production Quest - Base Mission Template & Renderer

Standardized 9-panel pedagogical architecture implemented across all 21 missions:
1. STORY (Workplace context and roleplay dialogue)
2. YOUR ROLE (Cute persona badge and desk visual)
3. YOUR MISSION (Concrete objective)
4. LEARN (Concise visual concept cards)
5. DO (Hands-on interactive task)
6. UNDER THE HOOD (Real code & simulated CLI execution)
7. RESULT (Telemetry, metrics, artifacts, logs)
8. WHY THIS MATTERS (Real-world production engineering insight)
9. NEXT (Narrative bridge to subsequent mission)
"""

from typing import Any, Callable, Dict, Optional
import streamlit as st
from src.state import advance_mission, complete_mission
from src.theme import render_neon_card, render_role_header, render_terminal


class BaseMission:
    """Base class for all pedagogical missions in MLOpsHub."""

    def __init__(
        self,
        mission_id: str,
        number_str: str,
        title: str,
        role_name: str,
        role_emoji: str,
        desk_desc: str,
        badge_name: str,
        xp_award: int = 100
    ) -> None:
        self.mission_id = mission_id
        self.number_str = number_str
        self.title = title
        self.role_name = role_name
        self.role_emoji = role_emoji
        self.desk_desc = desk_desc
        self.badge_name = badge_name
        self.xp_award = xp_award

    def render_instructor_notes(
        self,
        objective: str,
        talking_points: list,
        questions: list,
        expected_answers: list,
        misconceptions: list,
        estimated_time: str = "3–5 mins",
        teacher_dialogue: str = "",
        deep_dive: str = "",
        skip_tip: str = ""
    ) -> None:
        """
        Render expandable instructor guide notes with pedagogy hints.
        Hidden when student mode is active.
        """
        is_instructor_mode = st.session_state.get("instructor_mode", True)
        show_notes = st.session_state.get("show_notes", True)

        if not is_instructor_mode or not show_notes:
            return

        with st.expander(f"🎓 INSTRUCTOR PLAYBOOK (Est. Time: {estimated_time})", expanded=False):
            st.markdown(f"**🎯 Teaching Objective:** {objective}")

            if teacher_dialogue:
                st.markdown(f"""
                <div style="background: rgba(210, 153, 34, 0.15); border-left: 3px solid #d29922; padding: 10px 14px; border-radius: 6px; margin: 8px 0; font-size: 0.95rem;">
                    <b>🗣️ Scripted Dialogue (Say to class):</b><br>
                    <i>"{teacher_dialogue}"</i>
                </div>
                """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**💬 Suggested Talking Points:**")
                for tp in talking_points:
                    st.markdown(f"- {tp}")

                st.markdown("**❓ Question to Ask Students:**")
                for q in questions:
                    st.markdown(f"- *\"{q}\"*")

            with col2:
                st.markdown("**💡 Expected Student Answers:**")
                for a in expected_answers:
                    st.markdown(f"- {a}")

                st.markdown("**⚠️ Common Misconceptions:**")
                for m in misconceptions:
                    st.markdown(f"- {m}")

            if deep_dive:
                st.info(f"**🔬 Optional Deeper Dive:** {deep_dive}")
            if skip_tip:
                st.caption(f"⏱️ *Short on time?* {skip_tip}")

    def render_perspectives(
        self,
        business_pov: str,
        technical_pov: str,
        real_world_case: str = ""
    ) -> None:
        """
        Render dual-perspective panels:
        - Real-Life / Business Perspective (Financial, Risk, Customer, Team impact)
        - Deep Technical Perspective (Architecture, Protocols, Algorithms, Trade-offs)
        - Optional Real-World Industry War Story
        """
        st.markdown("#### 🌐 Real-World Perspective: Business vs Technical Deep-Dive")
        col_biz, col_tech = st.columns(2)

        with col_biz:
            st.markdown(
                f'<div style="background: rgba(88, 166, 255, 0.08); border: 1px solid #388bfd; border-radius: 10px; padding: 16px; min-height: 220px;">'
                f'<div style="color: #79c0ff; font-weight: 800; font-size: 1.05rem; margin-bottom: 8px;">💼 BUSINESS & STRATEGIC POV</div>'
                f'<div style="color: #d1d5db; font-size: 0.92rem; line-height: 1.6;">{business_pov}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        with col_tech:
            st.markdown(
                f'<div style="background: rgba(0, 245, 255, 0.08); border: 1px solid #00f5ff; border-radius: 10px; padding: 16px; min-height: 220px;">'
                f'<div style="color: #00f5ff; font-weight: 800; font-size: 1.05rem; margin-bottom: 8px;">⚙️ TECHNICAL & ENGINEERING POV</div>'
                f'<div style="color: #d1d5db; font-size: 0.92rem; line-height: 1.6;">{technical_pov}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        if real_world_case:
            st.markdown(
                f'<div style="background: rgba(255, 0, 127, 0.07); border-left: 4px solid #ff007f; border-radius: 8px; padding: 12px 16px; margin-top: 10px; font-size: 0.9rem; color: #f0f6fc;">'
                f'<b>💥 Real-World Industry Case Study:</b> {real_world_case}'
                f'</div>',
                unsafe_allow_html=True
            )

    def render_navigation_footer(self) -> None:
        """Render 'Next Mission' or 'Complete Step' button at the bottom of the mission."""
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            is_completed = self.mission_id in st.session_state.get("completed_missions", set())
            btn_label = "✅ Mission Completed! Advance to Next ➔" if is_completed else "🚀 Complete Mission & Advance ➔"

            if st.button(btn_label, use_container_width=True, type="primary"):
                complete_mission(self.mission_id, self.xp_award, self.badge_name)
                advance_mission()
                st.rerun()

    def render_standard_header(self, story_text: str, mission_objective: str) -> None:
        """Render standard top elements: Title, Role desk, Story, and Objective."""
        st.markdown(f"### MISSION {self.number_str}: {self.title}")

        # World A: Roleplay Header
        render_role_header(self.role_name, self.role_emoji, self.desk_desc)

        # Panel 1: Story
        render_neon_card("1. STORY & SITUATION", story_text, color_variant="cyan")

        # Panel 3: Mission
        render_neon_card("3. YOUR MISSION", f"**Objective:** {mission_objective}", color_variant="magenta")

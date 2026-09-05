"""
MLOpsHub: Production Quest - Persistent Instructor Control Panel

This module renders the top persistent control panel for instructors:
- Mission progress bar & completed count
- Unlocked MLOps capabilities tags
- Mode toggles: Instructor Mode vs. Student Mode, 30-Minute Demo vs. Full Hands-On
- Display toggles: Show/Hide Code, Terminal, Instructor Notes
- Simulation flow buttons: Start, Pause, Skip, Restart, Reset
"""

import streamlit as st
from src.state import (
    ALL_CAPABILITIES,
    advance_mission,
    get_active_missions,
    get_current_mission,
    previous_mission,
    reset_simulation
)


def render_instructor_bar() -> None:
    """Render top persistent control bar and pedagogical HUD."""
    active_missions = get_active_missions()
    current_idx = st.session_state.get("current_mission_index", 0)
    total_active = len(active_missions)
    completed_set = st.session_state.get("completed_missions", set())
    completed_count = len(completed_set)
    unlocked_caps = st.session_state.get("unlocked_capabilities", set())

    # Sticky/top container styling
    with st.container():
        st.markdown("""
        <div class="instructor-bar-container">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <div>
                    <span style="font-size: 1.3rem; font-weight: 900; color: #00f5ff; letter-spacing: 0.5px;">
                        ⚡ MLOpsHub: Production Quest
                    </span>
                    <span style="color: #8b949e; font-size: 0.85rem; margin-left: 10px;">
                        Company: <b>NEONBYTE</b> • Product: <b>ChurnGuard</b>
                    </span>
                </div>
                <div style="display: flex; align-items: center; gap: 14px;">
                    <span style="font-weight: 700; color: #39ff14; font-size: 0.95rem;">
                        XP: {xp}
                    </span>
                    <span style="font-weight: 700; color: #ff007f; font-size: 0.95rem;">
                        Mode: {mode_label}
                    </span>
                </div>
            </div>
        </div>
        """.format(
            xp=st.session_state.get("xp", 0),
            mode_label="🎓 Instructor" if st.session_state.get("instructor_mode", True) else "🎒 Student"
        ), unsafe_allow_html=True)

        # Progress bar
        progress_val = min(1.0, max(0.0, completed_count / float(total_active)))
        st.progress(progress_val, text=f"Mission Progress: {completed_count} / {total_active} completed ({int(progress_val * 100)}%)")

        # Control Row 1: Flow & Mode Actions
        ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4, ctrl_col5, ctrl_col6 = st.columns([1.2, 1.2, 1.2, 1.4, 1.4, 1.2])

        with ctrl_col1:
            if st.button("⏮️ Prev", use_container_width=True, disabled=(current_idx == 0)):
                previous_mission()
                st.rerun()

        with ctrl_col2:
            if st.button("⏭️ Skip / Next", use_container_width=True, disabled=(current_idx >= total_active - 1)):
                advance_mission()
                st.rerun()

        with ctrl_col3:
            is_paused = st.session_state.get("simulation_paused", False)
            btn_txt = "▶️ Resume" if is_paused else "⏸️ Pause"
            if st.button(btn_txt, use_container_width=True):
                st.session_state["simulation_paused"] = not is_paused
                st.rerun()

        with ctrl_col4:
            is_demo = st.session_state.get("demo_mode") == "fast"
            demo_label = "⚡ 30-Min Demo" if is_demo else "📚 Full Hands-On"
            if st.button(f"Track: {demo_label}", use_container_width=True, help="Toggle between 30-Minute Fast Demo and Full 21-Mission Deep Dive"):
                st.session_state["demo_mode"] = "full" if is_demo else "fast"
                st.session_state["current_mission_index"] = 0
                st.rerun()

        with ctrl_col5:
            is_inst = st.session_state.get("instructor_mode", True)
            inst_label = "🎓 Instructor Mode" if is_inst else "🎒 Student Mode"
            if st.button(inst_label, use_container_width=True, help="Toggle Student Mode (hides instructor notes & answers)"):
                st.session_state["instructor_mode"] = not is_inst
                st.rerun()

        with ctrl_col6:
            if st.button("🔄 Reset Quest", use_container_width=True, help="Reset simulation progress to Mission 01"):
                reset_simulation()
                st.rerun()

        # Collapsible Capabilities & Toggles Bar
        with st.expander("🛠️ MLOPS CAPABILITIES UNLOCKED & DISPLAY TOGGLES", expanded=False):
            t_col1, t_col2, t_col3 = st.columns(3)
            with t_col1:
                st.session_state["show_notes"] = st.toggle("Show Instructor Notes", value=st.session_state.get("show_notes", True))
            with t_col2:
                st.session_state["show_code"] = st.toggle("Show Implementation Code", value=st.session_state.get("show_code", True))
            with t_col3:
                st.session_state["show_terminal"] = st.toggle("Show Simulated Terminal", value=st.session_state.get("show_terminal", True))

            st.markdown("**Capabilities Tracker:**")
            cap_html = []
            for cap in ALL_CAPABILITIES:
                unlocked = cap["key"] in unlocked_caps
                badge_class = "badge-complete" if unlocked else "badge-pending"
                icon = "✓" if unlocked else "○"
                cap_html.append(f"<span class='badge-capsule {badge_class}'>{icon} {cap['label']}</span>")
            st.markdown("".join(cap_html), unsafe_allow_html=True)

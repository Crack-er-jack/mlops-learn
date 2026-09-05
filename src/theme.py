import textwrap
"""
MLOpsHub: Production Quest - Custom Theme & CSS Styling

This module provides custom CSS injection for the two visual worlds:
- World A (Cute Roleplay): Soft, pleasant workplace desk aesthetic.
- World B (MLOps Cyberpunk): Glowing cards, neon cyan/magenta/green accents,
  terminal displays, and projector-optimized high-contrast elements.
"""

import streamlit as st


def inject_custom_css() -> None:
    """
    Inject custom CSS rules into the Streamlit app.
    Provides responsive layout, dual-world visual styling, terminal boxes,
    and high-contrast typography for large screen presentations.
    """
    custom_css = """
    <style>
    /* =====================================================================
       GLOBAL PROJECTOR-FRIENDLY THEME & TYPOGRAPHY
       ===================================================================== */
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    code, pre, .terminal-text {
        font-family: 'Fira Code', monospace !important;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 96%;
    }

    /* =====================================================================
       PERSISTENT INSTRUCTOR BAR
       ===================================================================== */
    .instructor-bar-container {
        background: linear-gradient(135deg, rgba(19, 27, 46, 0.95), rgba(11, 15, 25, 0.95));
        border: 1px solid rgba(0, 245, 255, 0.35);
        border-radius: 12px;
        padding: 12px 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 245, 255, 0.15);
        backdrop-filter: blur(10px);
    }

    .badge-capsule {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-right: 6px;
        margin-bottom: 4px;
    }

    .badge-active {
        background: rgba(0, 245, 255, 0.2);
        color: #00f5ff;
        border: 1px solid #00f5ff;
    }

    .badge-complete {
        background: rgba(57, 255, 20, 0.15);
        color: #39ff14;
        border: 1px solid #39ff14;
    }

    .badge-pending {
        background: rgba(255, 255, 255, 0.05);
        color: #8b949e;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* =====================================================================
       WORLD A: REAL-WORLD ROLEPLAY (CUTE WORKPLACE DESK)
       ===================================================================== */
    .roleplay-card {
        background: linear-gradient(135deg, #1e2640 0%, #151c30 100%);
        border: 2px solid #58a6ff;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 18px;
        box-shadow: 0 8px 24px rgba(88, 166, 255, 0.12);
        transition: transform 0.2s ease;
    }

    .role-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #233054;
        color: #79c0ff;
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 0.95rem;
        font-weight: 700;
        border: 1px solid #388bfd;
    }

    .desk-visual {
        background: rgba(30, 41, 59, 0.7);
        border: 1px dashed rgba(121, 192, 255, 0.4);
        border-radius: 12px;
        padding: 14px;
        margin-top: 10px;
        font-size: 0.9rem;
        color: #d1d7e0;
    }

    /* =====================================================================
       WORLD B: MLOPS UNDER-THE-HOOD (CYBERPUNK NEON TECHNICAL MODE)
       ===================================================================== */
    .neon-card {
        background: #0d1322;
        border: 1px solid rgba(0, 245, 255, 0.4);
        border-radius: 14px;
        padding: 20px;
        margin: 14px 0;
        box-shadow: 0 0 15px rgba(0, 245, 255, 0.12);
        position: relative;
    }

    .neon-card-magenta {
        border-color: rgba(255, 0, 127, 0.5);
        box-shadow: 0 0 15px rgba(255, 0, 127, 0.15);
    }

    .neon-card-green {
        border-color: rgba(57, 255, 20, 0.5);
        box-shadow: 0 0 15px rgba(57, 255, 20, 0.15);
    }

    .neon-card-purple {
        border-color: rgba(176, 38, 255, 0.5);
        box-shadow: 0 0 15px rgba(176, 38, 255, 0.15);
    }

    .neon-title {
        color: #00f5ff;
        font-size: 1.3rem;
        font-weight: 800;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
        text-shadow: 0 0 8px rgba(0, 245, 255, 0.4);
    }

    /* =====================================================================
       AUTHENTIC TERMINAL WINDOW (SIMULATED CLI)
       ===================================================================== */
    .terminal-window {
        background-color: #050810;
        border: 1px solid #30363d;
        border-radius: 8px;
        margin: 12px 0;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
    }

    .terminal-header {
        background: #161b22;
        padding: 8px 12px;
        display: flex;
        align-items: center;
        gap: 6px;
        border-bottom: 1px solid #30363d;
        font-size: 0.8rem;
        color: #8b949e;
    }

    .terminal-circle {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        display: inline-block;
    }
    .circle-red { background: #ff5f56; }
    .circle-yellow { background: #ffbd2e; }
    .circle-green { background: #27c93f; }

    .terminal-body {
        padding: 14px;
        color: #39ff14;
        font-size: 0.92rem;
        line-height: 1.5;
        overflow-x: auto;
    }

    .terminal-prompt {
        color: #00f5ff;
        font-weight: bold;
    }

    .terminal-output {
        color: #c9d1d9;
    }

    /* =====================================================================
       INSTRUCTOR NOTES COLLAPSIBLE
       ===================================================================== */
    .instructor-notes-box {
        background: #1f1b0a;
        border: 2px solid #d29922;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 16px 0;
        color: #f0e6c8;
    }

    .incident-alert-banner {
        background: linear-gradient(90deg, rgba(255, 40, 40, 0.25), rgba(180, 0, 0, 0.1));
        border: 2px solid #ff4444;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 14px 0;
        box-shadow: 0 0 25px rgba(255, 68, 68, 0.3);
        animation: pulse-border 2s infinite ease-in-out;
    }

    @keyframes pulse-border {
        0% { box-shadow: 0 0 10px rgba(255, 68, 68, 0.2); }
        50% { box-shadow: 0 0 25px rgba(255, 68, 68, 0.5); }
        100% { box-shadow: 0 0 10px rgba(255, 68, 68, 0.2); }
    }
    </style>
    """
    st.markdown(textwrap.dedent(custom_css), unsafe_allow_html=True)


def render_terminal(command: str, output: str, title: str = "bash — 80x24") -> None:
    """
    Render an authentic, styled terminal component with window controls,
    prompt, input command, and simulated output.

    Args:
        command: The shell or python command executed.
        output: Terminal stdout/stderr content.
        title: Window header title.
    """
    terminal_html = f"""
    <div class="terminal-window">
        <div class="terminal-header">
            <span class="terminal-circle circle-red"></span>
            <span class="terminal-circle circle-yellow"></span>
            <span class="terminal-circle circle-green"></span>
            <span style="margin-left: 8px; font-weight: 600;">{title}</span>
        </div>
        <div class="terminal-body">
            <div><span class="terminal-prompt">neonbyte@prod-node:~$</span> {command}</div>
            <div class="terminal-output" style="white-space: pre-wrap; margin-top: 6px;">{output}</div>
        </div>
    </div>
    """
    st.markdown(textwrap.dedent(terminal_html), unsafe_allow_html=True)


def render_role_header(role_name: str, emoji: str, desk_desc: str) -> None:
    """
    Render World A: Cute workplace roleplay desk visual.

    Args:
        role_name: The title of the role (e.g., 'Data Analyst').
        emoji: Visual avatar icon for the role.
        desk_desc: Visual description of the role's workstation desk.
    """
    html_content = f"""
    <div class="roleplay-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div class="role-badge">
                <span style="font-size: 1.3rem;">{emoji}</span>
                <span>{role_name.upper()}</span>
            </div>
            <span style="color: #8b949e; font-size: 0.85rem; font-weight: 600;">
                🏢 NEONBYTE HQ • SPRINT 4
            </span>
        </div>
        <div class="desk-visual">
            <strong>🪑 Workplace Environment:</strong> {desk_desc}
        </div>
    </div>
    """
    st.markdown(textwrap.dedent(html_content), unsafe_allow_html=True)


def render_neon_card(title: str, content_html: str, color_variant: str = "cyan") -> None:
    """
    Render World B: Neon cyberpunk technical concept card.

    Args:
        title: Header text for the technical card.
        content_html: Inner HTML/Markdown content.
        color_variant: Neon accent ('cyan', 'magenta', 'green', 'purple').
    """
    variant_class = {
        "cyan": "neon-card",
        "magenta": "neon-card neon-card-magenta",
        "green": "neon-card neon-card-green",
        "purple": "neon-card neon-card-purple"
    }.get(color_variant, "neon-card")

    card_html = f"""
    <div class="{variant_class}">
        <div class="neon-title">{title}</div>
        <div style="color: #c9d1d9; font-size: 0.95rem; line-height: 1.55;">
            {content_html}
        </div>
    </div>
    """
    st.markdown(textwrap.dedent(card_html), unsafe_allow_html=True)

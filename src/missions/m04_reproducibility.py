"""
MLOpsHub: Production Quest - Mission 04: The Reproducibility Trap

Role: Data Scientist
Desk: Collaborative desk with two laptops side-by-side showing divergent metric plots.
Teaches: The Reproducibility crisis in ML, random seeds, environment isolation, parameter configs.
"""

import streamlit as st
import numpy as np
from src.data.generator import generate_clean_dataset
from src.missions.base_mission import BaseMission
from src.models.trainer import ChurnModelTrainer
from src.theme import render_neon_card, render_terminal


class Mission04(BaseMission):
    """Mission 04 Implementation."""

    def __init__(self) -> None:
        super().__init__(
            mission_id="m04",
            number_str="04",
            title="The Reproducibility Trap",
            role_name="Data Scientist",
            role_emoji="🔄",
            desk_desc="Paired programming desk with two laptops side-by-side displaying divergent terminal graphs.",
            badge_name="Deterministic Dev",
            xp_award=120
        )

    def render(self) -> None:
        """Render Mission 04 UI components."""
        story = (
            "**Wednesday, 2:00 PM**<br>"
            "You proudly commit your model code. Your teammate Alex pulls the branch onto his laptop "
            "and runs the exact same script. He messages you: *'Sarah, your model isn't hitting 84% accuracy. "
            "I'm getting 77% and my F1 is down by 0.12! Did you send me the wrong dataset?'*<br>"
            "Panic sets in. *'It worked on my machine!'*"
        )
        objective = (
            "Investigate why identical code produces non-deterministic results across machines. "
            "Diagnose sources of variation: random seeds, data shuffles, and unpinned dependencies. "
            "Lock the pipeline down with deterministic seed management and configuration files."
        )
        self.render_standard_header(story, objective)

        self.render_instructor_notes(
            objective="Demonstrate why traditional software version control (Git) alone is insufficient for Machine Learning.",
            talking_points=[
                "Software reproducibility: Code + Compiler = Binary.",
                "ML reproducibility: Code + Data + Hardware + Hyperparameters + Random Seeds = Model Artifact.",
                "The 'It works on my machine' nightmare is 10x worse in ML due to stochastic algorithms and split variance."
            ],
            questions=[
                "If we run train_test_split without specifying random_state, why do the metrics change on every run?",
                "Why can't we just commit our 20GB training dataset directly to a standard Git repository?"
            ],
            expected_answers=[
                "Without a seed, train_test_split picks a random subset of data each time; if lucky, the test set has easier examples.",
                "Git is designed for text diffs and bloats severely when handling large binary files (DVC solves this)."
            ],
            misconceptions=[
                "Assuming ML training is completely deterministic out of the box.",
                "Thinking setting random_state in Python solves hardware-level non-determinism (GPU/CPU thread scheduling)."
            ],
            deep_dive="Walk through the 5 vectors of ML reproducibility: Code, Data, Environment, Hardware, Seeds.",
            skip_tip="Toggle the 'Uncontrolled Seed' vs 'Locked Seed' sliders below to see variance disappear."
        )

        # Panel 4: Learn
        learn_html = """
        <b>The 5 Vectors of Machine Learning Reproducibility:</b><br>
        1. <b>Code:</b> Git commit SHA.<br>
        2. <b>Data:</b> Exact snapshot of rows, splits, and labels (Git doesn't do this!).<br>
        3. <b>Parameters & Config:</b> YAML/JSON config locking hyperparameters.<br>
        4. <b>Environment:</b> Pinned package dependencies (pip freeze / Docker).<br>
        5. <b>Randomness:</b> Explicitly initialized pseudorandom number generators (PRNG).
        """
        render_neon_card("4. LEARN: SOURCES OF NON-DETERMINISM", learn_html, color_variant="purple")

        # Panel 5: Do
        st.markdown("#### 5. DO: Experience the Seed Variance Experiment")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### 💻 Your Laptop (Seed = 42)")
            df = generate_clean_dataset(n_samples=1200, random_state=42)
            t_sarah = ChurnModelTrainer(random_state=42)
            res_sarah = t_sarah.train_and_evaluate(df)
            st.metric("Your Accuracy", f"{res_sarah['accuracy'] * 100:.1f}%")
            st.metric("Your F1 Score", f"{res_sarah['f1']:.3f}", delta="Published Claim")

        with col2:
            st.markdown("##### 💻 Alex's Laptop (Unpinned / Different Seed)")
            alex_seed = st.slider("Alex's Random Seed:", min_value=1, max_value=200, value=105)
            t_alex = ChurnModelTrainer(random_state=alex_seed)
            res_alex = t_alex.train_and_evaluate(df)
            f1_delta = round(res_alex['f1'] - res_sarah['f1'], 3)
            st.metric("Alex's Accuracy", f"{res_alex['accuracy'] * 100:.1f}%")
            st.metric("Alex's F1 Score", f"{res_alex['f1']:.3f}", delta=f"{f1_delta}", delta_color="inverse")

        lock_seeds = st.button("🔒 Apply Central Config: Lock Global Seed to 42", type="primary")
        if lock_seeds:
            st.success("Global seed config `config.yaml` established! All pipeline steps now share deterministic seed = 42.")

        # Panel 6: Under the Hood
        if st.session_state.get("show_code", True):
            st.markdown("#### 6. UNDER THE HOOD: config.yaml & Seed Seeding")
            code_str = (
                "# config.yaml - The Single Source of Truth\n"
                "seed: 42\n"
                "train_test_split: 0.25\n"
                "model:\n"
                "  type: LogisticRegression\n"
                "  max_iter: 500\n"
                "  C: 1.0\n\n"
                "# python reproducibility bootstrap\n"
                "import random, os, numpy as np\n"
                "def seed_everything(seed=42):\n"
                "    random.seed(seed)\n"
                "    os.environ['PYTHONHASHSEED'] = str(seed)\n"
                "    np.random.seed(seed)"
            )
            st.code(code_str, language="yaml")

        if st.session_state.get("show_terminal", True):
            render_terminal(
                "python train.py --config configs/base.yaml",
                "[INFO] Loading centralized config: configs/base.yaml\n"
                "[INFO] Global seed 42 set across NumPy and Scikit-Learn\n"
                "[REPRODUCED] Metrics match published benchmark exactly (F1: 0.736, Acc: 80.3%)!"
            )

        # Panel 7: Result
        render_neon_card(
            "7. RESULT",
            "With centralized configuration and fixed seeds, Alex's machine reproduces Sarah's results down to the 4th decimal place. But what happens when the underlying CSV dataset changes?",
            color_variant="green"
        )

        # Panel 8: Why This Matters
        render_neon_card(
            "8. WHY THIS MATTERS",
            "If your models cannot be reliably reproduced, you cannot debug production failures, pass compliance audits, or trust performance gains reported by your team.",
            color_variant="cyan"
        )

        # Panel 9: Next
        st.info("🔜 **Next Mission:** Locking seeds is great, but what about the data itself? How do we version 100MB+ CSV files without destroying Git? Enter DVC.")
        self.render_navigation_footer()

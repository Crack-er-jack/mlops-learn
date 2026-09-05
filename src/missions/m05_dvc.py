"""
MLOpsHub: Production Quest - Mission 05: Version the Data with DVC

Role: ML Engineer
Desk: Workstation with dual displays, terminal windows, storage drives, and Git branch diagram.
Teaches: Data Version Control (DVC), Git pointer files, MD5 checksums, remote storage, dataset lineage.
"""

import streamlit as st
from src.data.dvc_sim import DVCSimulator
from src.missions.base_mission import BaseMission
from src.theme import render_neon_card, render_terminal


class Mission05(BaseMission):
    """Mission 05 Implementation."""

    def __init__(self) -> None:
        super().__init__(
            mission_id="m05",
            number_str="05",
            title="Version the Data with DVC",
            role_name="ML Engineer",
            role_emoji="📦",
            desk_desc="Engineering command desk with terminal sessions, server rack stats, and DVC cheat-sheet.",
            badge_name="Data Versioner",
            xp_award=140
        )

    def render(self) -> None:
        """Render Mission 05 UI components."""
        story = (
            "**Thursday, 9:45 AM**<br>"
            "You are Alex, ML Engineer. Sarah comes to you in frustration: *'Someone updated `churn.csv` "
            "in our shared folder, and now my model accuracy dropped by 8%! Who changed the file? What was the previous version?'*<br>"
            "Nobody knows. Saving files as `churn_final_v2_really_final.csv` is amateur hour. "
            "You need production-grade Data Version Control (DVC)."
        )
        objective = (
            "Initialize DVC in the repository, track the customer dataset, commit the lightweight "
            "`.dvc` pointer metadata file to Git, and practice time-traveling between dataset versions."
        )
        self.render_standard_header(story, objective)

        self.render_instructor_notes(
            objective="Make students understand why Git cannot handle large datasets and how DVC bridges data artifacts to Git commits.",
            talking_points=[
                "Git was engineered for lightweight source text diffs. Storing a 5GB CSV or 10GB parquet file bloats Git repo size irreversibly.",
                "DVC philosophy: Git versions the tiny `.dvc` pointer file (MD5 hash + size). The real large data lives in S3/GCS/local cache.",
                "Lineage: When you checkout a Git commit, running `dvc checkout` synchronizes the exact data snapshot used by that commit."
            ],
            questions=[
                "Why shouldn't we push a 50GB dataset directly to GitHub?",
                "If we only commit `churn.csv.dvc` to Git, where does the real dataset file live?"
            ],
            expected_answers=[
                "GitHub has a 100MB file limit and Git repository cloning will become painfully slow.",
                "In DVC remote storage (such as AWS S3, Google Cloud Storage, Azure Blob, or MinIO)."
            ],
            misconceptions=[
                "Thinking DVC replaces Git (DVC works ALONGSIDE Git as a partner).",
                "Assuming DVC only tracks CSV files (it tracks audio, video, models, embeddings, directories)."
            ],
            deep_dive="Show the anatomy of a `.dvc` file: md5 hash, file size, relative path.",
            skip_tip="Click 'Execute DVC Setup Pipeline' and switch between versions v1, v2, and v3."
        )

        # Panel 4: Learn
        learn_html = """
        <b>How DVC Works in Tandem with Git:</b><br>
        1. <code>dvc add data/churn.csv</code> hashes the file (e.g. <code>b9e2c3d...</code>) and moves it to cache.<br>
        2. A lightweight pointer file <code>data/churn.csv.dvc</code> is created (~100 bytes).<br>
        3. Git tracks <code>churn.csv.dvc</code> and ignores the heavy <code>churn.csv</code>.<br>
        4. When a teammate checks out the Git commit, <code>dvc checkout</code> downloads the exact data.
        """
        render_neon_card("4. LEARN: DVC + GIT SYNERGY", learn_html, color_variant="purple")

        # Panel 5: Do
        st.markdown("#### 5. DO: Hands-on DVC Terminal & Version Time-Travel")

        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("##### ⚙️ Interactive DVC CLI Lab")
            st.info("💡 **Mission:** Initialize DVC (`dvc init`), track data (`dvc add data/churn.csv`), and check status (`dvc status`).")
            user_cmd = st.text_input(
                "Terminal Input:", 
                placeholder="type command here e.g., dvc init",
                key="dvc_lab_input"
            )
            run_cli = st.button("▶️ Execute Command", type="primary")

        with col2:
            st.markdown("##### 🕰️ Time-Travel Dataset Versions")
            ver_choice = st.radio(
                "Select Active Dataset Version to Mount:",
                ["v1 (Raw Untracked)", "v2 (Cleaned Baseline)", "v3 (Feature Engineered)"],
                horizontal=True
            )
            active_ver_key = ver_choice.split()[0]

        # Terminal output
        if run_cli and user_cmd:
            cmd = user_cmd.strip()
            # Try to map user input to simulated outputs or fallback
            if "init" in cmd:
                output, _ = DVCSimulator.execute_command("dvc init")
                render_terminal(cmd, output)
                st.success("✅ DVC repository initialized! Next: `dvc add data/churn.csv`")
            elif "add" in cmd and "churn.csv" in cmd:
                output, _ = DVCSimulator.execute_command("dvc add data/churn.csv")
                render_terminal(cmd, output)
                st.success("✅ Dataset tracked! A `.dvc` pointer file was created.")
            elif "status" in cmd:
                output, _ = DVCSimulator.execute_command("dvc status")
                render_terminal(cmd, output)
            elif "checkout" in cmd:
                output, _ = DVCSimulator.execute_command("dvc checkout v2")
                render_terminal(cmd, output)
            else:
                render_terminal(cmd, "Error: unrecognized or unsupported command in this simulation.\nTry 'dvc init', 'dvc add data/churn.csv', or 'dvc status'.")
        else:
            render_terminal("dvc status", "Data and pipelines are up to date.\ndata/churn.csv.dvc: up to date")

        # Active version inspection
        st.markdown(f"**Mounted Dataset Preview ({active_ver_key.upper()}):**")
        df_ver = DVCSimulator.get_dataset(active_ver_key)
        meta_ver = DVCSimulator.VERSIONS[active_ver_key]

        c_v1, c_v2, c_v3 = st.columns(3)
        c_v1.metric("Rows Count", meta_ver["rows"])
        c_v2.metric("MD5 Hash (DVC)", meta_ver["md5"][:12] + "...")
        c_v3.metric("Linked Git Commit", meta_ver["git_commit"].split(":")[0])

        st.dataframe(df_ver.head(4), use_container_width=True)

        # Real-World Perspectives
        self.render_perspectives(
            business_pov=(
                "<b>Auditability & Regulatory Survival:</b> In banking, healthcare, and enterprise SaaS, "
                "regulators require proof of which exact training examples influenced an AI decision. "
                "Without data versioning, retraining is an uncontrolled gamble: a silent change in an S3 bucket "
                "can degrade model performance, cause SLA breaches, or trigger compliance fines ($20M+ under EU AI Act)."
            ),
            technical_pov=(
                "<b>Content-Addressable Storage (CAS):</b> DVC computes an MD5 checksum of large artifacts "
                "and stores them in a content-addressed directory (`.dvc/cache/ab/12cd...`). It replaces heavy files "
                "with tiny 120-byte `.dvc` text pointers in Git. It uses reflinks, symlinks, or hardlinks on local filesystems "
                "to allow instant zero-copy checkout without duplicating gigabytes of disk space."
            ),
            real_world_case=(
                "A leading automated lending startup suffered a 14% surge in loan defaults when an engineer trained on "
                "an unversioned CSV containing temporary promotional records. Because the dataset wasn't version-controlled, "
                "it took forensic investigators 6 weeks to discover why the model mispriced credit risk."
            )
        )

        # Panel 6: Under the Hood
        if st.session_state.get("show_code", True):
            st.markdown("#### 6. UNDER THE HOOD: Production DVC Code & Pipeline Arsenal")
            tab_dvc_file, tab_dvc_yaml, tab_dvc_cli = st.tabs([
                "📄 churn.csv.dvc (Pointer File)",
                "⚙️ dvc.yaml (Reproducible Pipeline)",
                "💻 Real Production CLI Runbook"
            ])

            with tab_dvc_file:
                st.code(DVCSimulator.generate_dvc_file_content(active_ver_key), language="yaml")

            with tab_dvc_yaml:
                st.code("""# dvc.yaml - Declarative MLOps Pipeline Definition
stages:
  prepare:
    cmd: python src/data/prepare.py --input data/churn_raw.csv --output data/churn_clean.csv
    deps:
      - data/churn_raw.csv
      - src/data/prepare.py
    outs:
      - data/churn_clean.csv

  train:
    cmd: python src/models/train.py --data data/churn_clean.csv --params params.yaml
    deps:
      - data/churn_clean.csv
      - src/models/train.py
    params:
      - train.seed
      - train.learning_rate
    outs:
      - models/churn_model.joblib
    metrics:
      - metrics.json:
          cache: false""", language="yaml")

            with tab_dvc_cli:
                st.code("""# 1. Initialize DVC and configure remote S3 storage
dvc init
dvc remote add -d s3remote s3://neonbyte-mlops-artifacts/dvc-storage
dvc config core.autostage true

# 2. Track dataset and push bytes to remote cloud storage
dvc add data/churn.csv
git add data/churn.csv.dvc data/.gitignore
git commit -m "feat(data): Track ChurnGuard v3 clean training snapshot"
dvc push

# 3. Teammate pulls the exact dataset on a new machine
git pull origin main
dvc pull

# 4. Reproduce the complete end-to-end pipeline deterministically
dvc repro""", language="bash")

        # Panel 7: Result
        render_neon_card(
            "7. RESULT",
            f"DVC tracking enabled! You can seamlessly switch between raw (v1), clean (v2), and feature-engineered (v3) data snapshots with zero disk bloat in Git.",
            color_variant="green"
        )

        # Panel 8: Why This Matters
        render_neon_card(
            "8. WHY THIS MATTERS",
            "<b>Git tracks code changes; DVC tracks data changes.</b> Together, they guarantee that every model experiment is tied to the exact bytes of data it was trained on.",
            color_variant="cyan"
        )

        # Panel 9: Next
        st.info("🔜 **Next Mission:** Now that code and data are both versioned, how do we track dozens of experiments with different hyperparameters and metrics? Enter MLflow.")
        self.render_navigation_footer()

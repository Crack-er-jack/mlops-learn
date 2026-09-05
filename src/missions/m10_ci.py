"""
MLOpsHub: Production Quest - Mission 10: Continuous Integration (CI)

Role: DevOps / MLOps Engineer
Desk: Infrastructure monitoring desk with GitHub Actions pipelines and runner telemetry.
Teaches: Continuous Integration (CI), GitHub Actions YAML, automated PR checks, blocked merges.
"""

import streamlit as st
import pandas as pd
from src.missions.base_mission import BaseMission
from src.pipeline.ci_cd import CICDEngine
from src.theme import render_neon_card, render_terminal


class Mission10(BaseMission):
    """Mission 10 Implementation."""

    def __init__(self) -> None:
        super().__init__(
            mission_id="m10",
            number_str="10",
            title="Continuous Integration (CI)",
            role_name="DevOps / MLOps",
            role_emoji="⚙️",
            desk_desc="DevOps cockpit with cloud node monitors, GitHub Actions pipelines, and build status displays.",
            badge_name="CI Automator",
            xp_award=140
        )

    def render(self) -> None:
        """Render Mission 10 UI components."""
        story = (
            "**Wednesday, 10:30 AM**<br>"
            "Marcus, our Lead DevOps Engineer, joins the room: *'We have 4 data scientists and 2 engineers "
            "pushing code. Last night, someone pushed a broken transformation directly to main, and the nightly "
            "training job crashed for 6 hours. From now on, NO CODE MERGES TO MAIN without passing automated CI!'*<br>"
            "Continuous Integration automatically runs tests and quality gates on every Pull Request before human review."
        )
        objective = (
            "Inspect the GitHub Actions workflow definition (`.github/workflows/mlops.yml`). "
            "Simulate a CI pipeline execution on both clean code and a breaking commit. "
            "Observe how CI blocks buggy code from ever reaching the production branch."
        )
        self.render_standard_header(story, objective)

        self.render_instructor_notes(
            objective="Demonstrate how CI turns tests into automated quality gatekeepers that protect production from human error.",
            talking_points=[
                "CI is not just for unit tests: in MLOps, CI pulls data via DVC, runs data tests, validates model performance gates, and benchmarks latency.",
                "Why PR branches must be protected: Merge buttons should be disabled until GitHub Actions reports 100% green.",
                "The cost of fixing a bug in CI (5 minutes) vs fixing a silent data bug in production (weeks of lost revenue and customer trust)."
            ],
            questions=[
                "What happens if an engineer forgets to update the DVC hash before opening a pull request?",
                "Why do we run CI in an isolated cloud runner (ubuntu-latest) instead of on the developer's laptop?"
            ],
            expected_answers=[
                "The CI pipeline will fail when attempting to pull data or run tests against the mismatched hash.",
                "Cloud runners guarantee a pristine, reproducible environment free of local artifacts or uncommitted files."
            ],
            misconceptions=[
                "Thinking CI automatically deploys to production (that is Continuous Delivery / CD).",
                "Assuming ML models cannot be tested inside standard GitHub Actions runners (CPU tests run easily in <2 minutes)."
            ],
            deep_dive="Show how CML (Continuous Machine Learning) can publish markdown reports and confusion matrix plots directly as GitHub PR comments.",
            skip_tip="Trigger the 'Simulate Failing PR' button to see how the merge gate locks down."
        )

        # Panel 4: Learn
        learn_html = """
        <b>The ML Continuous Integration Pipeline:</b><br>
        <code>git push</code> ➔ <b>Runner Provisioned:</b> Ubuntu 22.04 LTS.<br>
        ➔ <b>Environment:</b> Python 3.11 + dependencies cached.<br>
        ➔ <b>DVC Pull:</b> Download test dataset from remote cache.<br>
        ➔ <b>Quality Gate:</b> Pytest executes (Data + Unit + Model F1 &ge; 0.75).<br>
        ➔ <b>Merge Decision:</b> 🟢 PASS = Merge Allowed | 🔴 FAIL = PR Blocked.
        """
        render_neon_card("4. LEARN: CONTINUOUS INTEGRATION ANATOMY", learn_html, color_variant="purple")

        # Panel 5: Do
        st.markdown("#### 5. DO: Trigger GitHub Actions CI Simulation")

        col1, col2 = st.columns(2)
        with col1:
            run_clean_ci = st.button("🚀 Push Clean Commit (PR #102: Optimized Trees)", type="primary")
        with col2:
            run_failing_ci = st.button("⚠️ Push Broken Commit (PR #103: Corrupt Preprocessor)")

        if run_failing_ci:
            status, steps = CICDEngine.simulate_ci_run(tests_pass=False)
            st.error("❌ **BUILD BLOCKED:** CI pipeline failed on step 'Run Pytest Quality Suite'. Model cannot be promoted or merged!")
            st.dataframe(pd.DataFrame(steps), use_container_width=True)
            render_terminal("git push origin feature/broken-preprocessor", "Enumerating objects: 6, done.\nremote: Running GitHub Actions workflow...\nremote: [FAIL] Step 5: Pytest assertion failed: test_data_non_negative_spend\nremote: Error: Process completed with exit code 1.\nTo github.com:neonbyte/churnguard.git\n ! [remote rejected] HEAD -> main (pre-receive hook declined: required status check failed)")
        else:
            status, steps = CICDEngine.simulate_ci_run(tests_pass=True)
            if run_clean_ci:
                st.success("🎉 **CI WORKFLOW PASSED:** All 7 stages completed in 47 seconds. Pull request approved for merge!")
            st.dataframe(pd.DataFrame(steps), use_container_width=True)
            render_terminal("git push origin feature/optimized-trees", "remote: Running GitHub Actions workflow...\nremote: [PASS] All checks succeeded (7/7 passed in 47s).\nremote: Branch protection check passed. Ready to merge.")

        # Real-World Perspectives
        self.render_perspectives(
            business_pov=(
                "<b>Velocity Without Russian Roulette:</b> In high-growth startups, engineering teams ship dozens "
                "of PRs weekly. Without automated CI gates, bad code inevitably leaks into production, requiring "
                "emergency all-hands war rooms, rollbacks, and downtime. CI enforces rigorous code quality standards "
                "automatically, saving thousands of engineering hours annually."
            ),
            technical_pov=(
                "<b>Automated Quality Gating:</b> GitHub Actions spins up ephemeral Ubuntu runners, fetches "
                "cached pip wheels, uses AWS/DVC credentials from GitHub Secrets to pull exact data splits, "
                "executes Pytest across multiple threads, and evaluates strict regression metrics. If any assertion fails, "
                "the runner exits with non-zero code `exit 1`, signaling the GitHub API to lock the Pull Request merge button."
            ),
            real_world_case=(
                "Knight Capital lost $440 million in 45 minutes in 2012 when an engineer manually deployed code to 7 out of 8 servers, "
                "leaving dead code active on the 8th server. The lack of automated CI/CD and deployment verification bankrupted "
                "the company before lunchtime."
            )
        )

        # Panel 6: Under the Hood
        if st.session_state.get("show_code", True):
            st.markdown("#### 6. UNDER THE HOOD: Production GitHub Actions Workflow Suite")
            tab_yaml, tab_cml, tab_rules = st.tabs([
                "📄 .github/workflows/mlops.yml",
                "🤖 CML Automated PR Report Step",
                "🛡️ GitHub Branch Protection Rules"
            ])

            with tab_yaml:
                st.code(CICDEngine.get_github_workflow_yaml(), language="yaml")

            with tab_cml:
                st.code("""# CML (Continuous Machine Learning) PR Comment Step
- name: Generate Model Evaluation Report
  env:
    REPO_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    # Run model benchmark and generate confusion matrix plot
    python src/models/eval_report.py
    
    # Post rich markdown report directly onto the GitHub PR
    echo "## 🚀 ChurnGuard Model Quality Gate Report" >> report.md
    echo "### Evaluation Metrics:" >> report.md
    cat metrics.md >> report.md
    echo "### Confusion Matrix:" >> report.md
    echo '![](./confusion_matrix.png "Confusion Matrix")' >> report.md
    
    cml comment create report.md""", language="yaml")

            with tab_rules:
                st.code("""# Branch Protection Policy for 'main':
# 1. Require a pull request before merging
# 2. Require status checks to pass before merging:
#    - test_and_validate / Run Pytest Quality Suite
#    - test_and_validate / Verify Model Quality Gate (F1 >= 0.75)
# 3. Require signed commits
# 4. Include administrators (no emergency overrides without audit log)""", language="yaml")

        # Panel 7: Result
        render_neon_card(
            "7. RESULT",
            "Automated CI safeguards the codebase. Defective code and degraded models are blocked by automated gates before they can ever reach the main branch.",
            color_variant="green"
        )

        # Panel 8: Why This Matters
        render_neon_card(
            "8. WHY THIS MATTERS",
            "<b>CI establishes team discipline.</b> Instead of relying on manual checklists, the repository enforces automated standards for every line of code and every model candidate.",
            color_variant="cyan"
        )

        # Panel 9: Next
        st.info("🔜 **Next Mission:** Our code is tested and merged! How do we package the application and model into a reproducible, deployable container? Enter Docker.")
        self.render_navigation_footer()

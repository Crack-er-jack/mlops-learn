"""
MLOpsHub: Production Quest - Mission 11: Continuous Delivery & Docker

Role: DevOps / MLOps Engineer
Desk: Container orchestration dashboard with Docker build terminals and image registry stats.
Teaches: Continuous Delivery (CD), Docker containers, layer caching, reproducible runtimes.
"""

import streamlit as st
from src.missions.base_mission import BaseMission
from src.pipeline.ci_cd import CICDEngine
from src.theme import render_neon_card, render_terminal


class Mission11(BaseMission):
    """Mission 11 Implementation."""

    def __init__(self) -> None:
        super().__init__(
            mission_id="m11",
            number_str="11",
            title="Continuous Delivery & Docker",
            role_name="DevOps / MLOps",
            role_emoji="🐳",
            desk_desc="Container operations station with Docker registry status, container stats, and deployment manifests.",
            badge_name="Container Captain",
            xp_award=140
        )

    def render(self) -> None:
        """Render Mission 11 UI components."""
        story = (
            "**Thursday, 9:00 AM**<br>"
            "Marcus explains the next challenge: *'We have tested the code, but deploying raw Python scripts "
            "directly to production servers is fragile. If the host OS upgrades Python from 3.11 to 3.12, "
            "or glibc versions drift, our scikit-learn binary wheels could crash at 2 AM. "
            "We must package the entire application, model, and dependencies into an immutable Docker image.'*<br>"
            "A container guarantees that what worked in CI will run identically in production."
        )
        objective = (
            "Review the production Dockerfile. Build an optimized, CPU-friendly Docker image "
            "for ChurnGuard (`neonbyte/churnguard:v3.0.0`), inspect layer caching, and verify container health."
        )
        self.render_standard_header(story, objective)

        self.render_instructor_notes(
            objective="Explain why containerization is the universal packaging standard for ML applications and reproducible runtimes.",
            talking_points=[
                "Difference between a Virtual Machine (heavy OS hypervisor) and a Docker Container (lightweight OS-level virtualization sharing the kernel).",
                "Why Docker layer caching matters: Copying `requirements.txt` before `COPY . .` ensures dependencies aren't re-downloaded on every minor code tweak.",
                "Container immutability: The image `churnguard:v3.0.0` will execute identically in 2026, 2028, or 2030."
            ],
            questions=[
                "Why shouldn't we use `FROM python:latest` in a production Dockerfile?",
                "What is the risk of installing Python packages directly on the host machine without Docker?"
            ],
            expected_answers=[
                "`latest` is mutable and changes over time, breaking reproducibility when upstream updates release.",
                "Dependency conflicts across different microservices and lack of rollback certainty."
            ],
            misconceptions=[
                "Thinking Docker requires Kubernetes (Docker containers can run on a single VM, AWS ECS, Google Cloud Run, or local servers).",
                "Assuming ML containers must be 10GB+ GPU behemoths (our CPU tabular container is only 184MB!)."
            ],
            deep_dive="Explain multi-stage Docker builds to strip out build compilers from the final runtime image.",
            skip_tip="Click 'Build Docker Image' to view the layered build output."
        )

        # Panel 4: Learn
        learn_html = """
        <b>The Packaging Lifecycle:</b><br>
        1. <b>Dockerfile:</b> Declarative blueprint specifying base OS, Python version, and system dependencies.<br>
        2. <b>Image:</b> Immutable binary snapshot stored in a registry (e.g., Docker Hub, ECR, GCR).<br>
        3. <b>Container:</b> Live running instance of the image isolated in its own namespace and cgroups.<br>
        4. <b>Zero-Downtime CD:</b> Rolling deployment swaps old container v2 with new container v3 without dropping requests.
        """
        render_neon_card("4. LEARN: CONTAINERIZATION ESSENTIALS", learn_html, color_variant="purple")

        # Panel 5: Do
        st.markdown("#### 5. DO: Build and Package ChurnGuard Image")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### 📦 Docker CLI Commands")
            selected_docker_cmd = st.selectbox(
                "Select Docker Action:",
                [
                    "docker build -t neonbyte/churnguard:v3.0.0 .",
                    "docker images",
                    "docker run -d -p 8501:8501 --name churnguard-prod neonbyte/churnguard:v3.0.0",
                    "docker ps"
                ]
            )
            exec_docker = st.button("🐳 Execute Docker Action", type="primary")

        with col2:
            st.markdown("##### 📊 Container Image Spec")
            st.markdown("- **Base Image:** `python:3.11-slim`")
            st.markdown("- **Final Image Size:** `184 MB` (CPU-optimized)")
            st.markdown("- **Exposed Port:** `8501 (HTTP)`")
            st.markdown("- **Target Architecture:** `linux/amd64`")

        if exec_docker:
            if "build" in selected_docker_cmd:
                render_terminal(selected_docker_cmd, CICDEngine.simulate_docker_build())
            elif "images" in selected_docker_cmd:
                render_terminal(
                    selected_docker_cmd,
                    "REPOSITORY               TAG       IMAGE ID       CREATED         SIZE\n"
                    "neonbyte/churnguard      v3.0.0    d8c47f9a21b8   2 minutes ago   184MB\n"
                    "neonbyte/churnguard      v2.0.0    9a4c1f7b8e21   1 week ago      182MB"
                )
            elif "run" in selected_docker_cmd:
                render_terminal(
                    selected_docker_cmd,
                    "a4f891c2b87431e67b2d8e09f5a43210 (container started)\n"
                    "Serving live on http://0.0.0.0:8501\n"
                    "[HEALTHCHECK] HTTP GET /_stcore/health -> 200 OK (Healthy)"
                )
            else:
                render_terminal(
                    selected_docker_cmd,
                    "CONTAINER ID   IMAGE                        COMMAND                  STATUS         PORTS\n"
                    "a4f891c2b874   neonbyte/churnguard:v3.0.0   'streamlit run app.py'   Up 3 minutes   0.0.0.0:8501->8501/tcp"
                )
        else:
            render_terminal("docker ps", "CONTAINER ID   IMAGE                        STATUS\na4f891c2b874   neonbyte/churnguard:v3.0.0   Up 45 minutes (healthy)")

        # Real-World Perspectives
        self.render_perspectives(
            business_pov=(
                "<b>Eliminating Environment Snowflakes & Cloud Overspending:</b> Before containerization, "
                "cloud virtual machines drifted into unique 'snowflake' environments as engineers manually installed "
                "different package versions. Containers reduce multi-cloud deployment friction, guarantee 100% environment "
                "parity, and slash cloud hosting costs by packaging lean, CPU-friendly microservices."
            ),
            technical_pov=(
                "<b>Linux Cgroups & Layer Immutability:</b> Docker leverages Linux kernel features: Namespaces "
                "(PID, mount, network isolation) and Control Groups (CPU & memory limits). Each Dockerfile directive creates "
                "an immutable read-only layer identified by a SHA256 hash. Multi-stage builds compile heavy build tools "
                "in stage 1, then copy only the pure runtime artifacts to stage 2, minimizing container attack surface."
            ),
            real_world_case=(
                "A self-driving vehicle simulation team spent 3 weeks debugging intermittent perception failures only to "
                "discover that Ubuntu had auto-updated an underlying C++ math library on 4 out of 20 cloud nodes. "
                "Adopting pinned immutable Docker images eliminated the issue permanently."
            )
        )

        # Panel 6: Under the Hood
        if st.session_state.get("show_code", True):
            st.markdown("#### 6. UNDER THE HOOD: Production Dockerfile & Container Architecture")
            tab_dockerfile, tab_dockerignore, tab_compose = st.tabs([
                "🐳 Production Multi-Stage Dockerfile",
                "🚫 .dockerignore (Build Context Optimization)",
                "🐙 docker-compose.yml (Local Cluster)"
            ])

            with tab_dockerfile:
                st.code(CICDEngine.get_dockerfile_content(), language="dockerfile")

            with tab_dockerignore:
                st.code("""# .dockerignore - Prevent Bloat in Docker Build Context
.git/
.dvc/cache/
.pytest_cache/
__pycache__/
*.pyc
*.pyo
*.pyd
.env
.venv/
data/*.csv
notebooks/*.ipynb
tests/""", language="dockerignore")

            with tab_compose:
                st.code("""version: '3.8'
services:
  churnguard-api:
    image: neonbyte/churnguard:v3.0.0
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8501:8501"
    environment:
      - MLFLOW_TRACKING_URI=http://mlflow-server:5000
      - REDIS_URL=redis://feature-store-redis:6379
    depends_on:
      - feature-store-redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 5s
      retries: 3

  feature-store-redis:
    image: redis:7-alpine
    ports:
      - "6379:6379" """, language="yaml")

        # Panel 7: Result
        render_neon_card(
            "7. RESULT",
            "Immutable deployment artifact created: <code>neonbyte/churnguard:v3.0.0</code>. It encapsulates code, model registry weights, and dependencies with zero host leakage.",
            color_variant="green"
        )

        # Panel 8: Why This Matters
        render_neon_card(
            "8. WHY THIS MATTERS",
            "<b>Containers solve the 'works on my machine' dilemma forever.</b> They make deployments predictable, automated, and platform-agnostic across laptops, staging clusters, and cloud environments.",
            color_variant="cyan"
        )

        # Panel 9: Next
        st.info("🔜 **Next Mission:** The container is built and shipped. Now let's see ChurnGuard live in production handling real customer queries with full lineage tracking!")
        self.render_navigation_footer()

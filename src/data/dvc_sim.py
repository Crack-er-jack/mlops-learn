"""
MLOpsHub: Production Quest - DVC Simulation Engine

This module simulates hands-on Data Version Control (DVC) workflows:
- Generates realistic .dvc pointer files with MD5 checksums.
- Simulates terminal commands (`dvc init`, `dvc add`, `git commit`, `dvc checkout`).
- Maintains dataset versions (v1 raw, v2 cleaned, v3 feature-engineered).
"""

import hashlib
from typing import Dict, List, Tuple
import pandas as pd
from src.data.generator import generate_clean_dataset, generate_dirty_dataset


class DVCSimulator:
    """Simulated DVC (Data Version Control) tracking engine."""

    VERSIONS: Dict[str, Dict[str, str]] = {
        "v1": {
            "tag": "v1.0-raw",
            "description": "Raw unvalidated telemetry data with dirty records and missing values.",
            "file": "data/churn_v1_raw.csv",
            "rows": 1215,
            "md5": "a8f3b2c1d4e567890123456789abcdef",
            "git_commit": "e4a1f9c: Track initial raw churn dataset via DVC",
            "created": "2026-03-01 09:30:00"
        },
        "v2": {
            "tag": "v2.0-cleaned",
            "description": "Validated and sanitized dataset: dropped duplicates, imputed nulls, filtered negative spends.",
            "file": "data/churn_v2_clean.csv",
            "rows": 1200,
            "md5": "b9e2c3d4e5f678901234567890abcdef",
            "git_commit": "7b2d8e1: Cleaned data and updated churn.csv.dvc pointer",
            "created": "2026-03-10 14:15:22"
        },
        "v3": {
            "tag": "v3.0-features",
            "description": "Feature-engineered production dataset: added spend_to_tenure ratio and risk buckets.",
            "file": "data/churn_v3_prod.csv",
            "rows": 1200,
            "md5": "c0d3e4f5a6b789012345678901abcdef",
            "git_commit": "3c9f2a4: Upgraded feature transforms for ChurnGuard v3",
            "created": "2026-03-18 11:45:10"
        }
    }

    @staticmethod
    def get_dataset(version: str = "v2") -> pd.DataFrame:
        """
        Load the DataFrame corresponding to a specific DVC tracked version.

        Args:
            version: 'v1', 'v2', or 'v3'.

        Returns:
            pd.DataFrame for the requested version.
        """
        if version == "v1":
            return generate_dirty_dataset(n_samples=1200, random_state=42)
        elif version == "v2":
            return generate_clean_dataset(n_samples=1200, random_state=42)
        else:  # v3
            df = generate_clean_dataset(n_samples=1200, random_state=42)
            # Add engineered features
            df["spend_to_tenure_ratio"] = np_ratio = np_round = (df["monthly_spend"] / df["tenure"]).round(2)
            df["is_high_risk_segment"] = ((df["support_calls"] > 3) & (df["contract_type"] == "Month-to-month")).astype(int)
            return df

    @staticmethod
    def generate_dvc_file_content(version: str) -> str:
        """
        Generate authentic YAML content of a `.dvc` tracking file.

        Args:
            version: Dataset version identifier ('v1', 'v2', 'v3').

        Returns:
            YAML string formatted as a standard DVC pointer file.
        """
        meta = DVCSimulator.VERSIONS.get(version, DVCSimulator.VERSIONS["v2"])
        return f"""# churn.csv.dvc (Tracked by Git, dataset stored in remote storage)
outs:
- md5: {meta['md5']}
  size: 78420
  hash: md5
  path: churn.csv
"""

    @staticmethod
    def execute_command(command: str) -> Tuple[str, str]:
        """
        Simulate the terminal output of authentic DVC commands.

        Args:
            command: Shell command string.

        Returns:
            Tuple of (formatted_output, status).
        """
        cmd = command.strip()
        if cmd == "dvc init":
            return (
                "Initializing DVC in current Git repository...\n"
                "+ .dvc/config\n"
                "+ .dvc/.gitignore\n"
                "+ .dvcignore\n\n"
                "You can now start adding files to track with 'dvc add <file>'!",
                "success"
            )
        elif cmd.startswith("dvc add"):
            return (
                "100% Adding... [##############################] 1/1\n"
                "Saving 'data/churn.csv' to storage '.dvc/cache'...\n"
                "Saving information to 'data/churn.csv.dvc'\n\n"
                "To track the changes with git, run:\n"
                "    git add data/churn.csv.dvc data/.gitignore",
                "success"
            )
        elif "git commit" in cmd:
            return (
                "[main 7b2d8e1] Track churn dataset pointer via DVC\n"
                " 2 files changed, 6 insertions(+)\n"
                " create mode 100644 data/churn.csv.dvc",
                "success"
            )
        elif cmd.startswith("dvc checkout"):
            target = cmd.split()[-1] if len(cmd.split()) > 2 else "latest"
            return (
                f"Checking out '{target}' from DVC cache...\n"
                "M       data/churn.csv\n"
                "Checkout completed successfully (1 file updated).",
                "success"
            )
        elif cmd == "dvc status":
            return (
                "Data and pipelines are up to date.\n"
                "data/churn.csv.dvc: up to date",
                "success"
            )
        else:
            return (f"Command not recognized: {command}", "error")

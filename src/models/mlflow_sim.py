"""
MLOpsHub: Production Quest - MLflow Tracking & Model Registry Engine

This module simulates MLflow tracking and centralized Model Registry:
- Logging parameters, metrics, tags, and scikit-learn artifacts.
- Multi-run experiment comparison UI (Logistic Regression vs. Random Forest vs. Gradient Boosting).
- Model Registry lifecycle transitions: Development -> Staging -> Production -> Archived.
- Model lineage tracing (Run ID -> Git Commit -> DVC Data Hash -> Registry Version).
"""

from typing import Any, Dict, List
import pandas as pd


class MLflowSimulator:
    """Simulation engine for MLflow Tracking Server and Model Registry."""

    DEFAULT_EXPERIMENTS: List[Dict[str, Any]] = [
        {
            "run_id": "run-7a1b8c",
            "run_name": "logreg_baseline",
            "model_type": "LogisticRegression",
            "params": {"C": 1.0, "max_iter": 500, "solver": "lbfgs", "seed": 42},
            "metrics": {"accuracy": 0.8033, "precision": 0.7619, "recall": 0.7111, "f1": 0.7356, "latency_ms": 4.2},
            "dataset_version": "v2.0-cleaned (dvc: b9e2c3d)",
            "git_commit": "7b2d8e1",
            "artifact_uri": "s3://neonbyte-mlflow/artifacts/run-7a1b8c/model.pkl",
            "status": "FINISHED"
        },
        {
            "run_id": "run-9c3e2f",
            "run_name": "rf_tuned_depth5",
            "model_type": "RandomForest",
            "params": {"n_estimators": 100, "max_depth": 5, "min_samples_split": 4, "seed": 42},
            "metrics": {"accuracy": 0.8433, "precision": 0.8205, "recall": 0.7805, "f1": 0.8000, "latency_ms": 11.8},
            "dataset_version": "v2.0-cleaned (dvc: b9e2c3d)",
            "git_commit": "7b2d8e1",
            "artifact_uri": "s3://neonbyte-mlflow/artifacts/run-9c3e2f/model.pkl",
            "status": "FINISHED"
        },
        {
            "run_id": "run-4e8f1a",
            "run_name": "gradient_boosting_v1",
            "model_type": "GradientBoosting",
            "params": {"n_estimators": 150, "learning_rate": 0.08, "max_depth": 4, "seed": 42},
            "metrics": {"accuracy": 0.8567, "precision": 0.8351, "recall": 0.8020, "f1": 0.8182, "latency_ms": 28.4},
            "dataset_version": "v3.0-features (dvc: c0d3e4f)",
            "git_commit": "3c9f2a4",
            "artifact_uri": "s3://neonbyte-mlflow/artifacts/run-4e8f1a/model.pkl",
            "status": "FINISHED"
        }
    ]

    INITIAL_REGISTRY: List[Dict[str, Any]] = [
        {
            "model_name": "ChurnGuard",
            "version": "v1",
            "source_run": "run-7a1b8c",
            "stage": "Archived",
            "description": "Baseline logistic regression model on initial clean tabular features.",
            "data_lineage": "data/churn_v1.csv (dvc: a8f3b2c)",
            "owner": "Sarah (Data Scientist)",
            "registered_at": "2026-03-05 14:20:00"
        },
        {
            "model_name": "ChurnGuard",
            "version": "v2",
            "source_run": "run-9c3e2f",
            "stage": "Staging",
            "description": "Random forest classifier with optimized tree depth and fast inference latency.",
            "data_lineage": "data/churn_v2.csv (dvc: b9e2c3d)",
            "owner": "Alex (ML Engineer)",
            "registered_at": "2026-03-12 16:45:00"
        },
        {
            "model_name": "ChurnGuard",
            "version": "v3",
            "source_run": "run-4e8f1a",
            "stage": "Production",
            "description": "Production model: Gradient boosting classifier coupled with v3 feature store.",
            "data_lineage": "data/churn_v3.csv (dvc: c0d3e4f)",
            "owner": "Marcus (MLOps Lead)",
            "registered_at": "2026-03-20 10:15:00"
        }
    ]

    @staticmethod
    def get_runs_dataframe() -> pd.DataFrame:
        """Return experiment runs as a clean pandas DataFrame for display."""
        rows = []
        for run in MLflowSimulator.DEFAULT_EXPERIMENTS:
            rows.append({
                "Run ID": run["run_id"],
                "Model": run["model_type"],
                "Accuracy": run["metrics"]["accuracy"],
                "Precision": run["metrics"]["precision"],
                "Recall": run["metrics"]["recall"],
                "F1 Score": run["metrics"]["f1"],
                "Latency": f"{run['metrics']['latency_ms']} ms",
                "Dataset": run["dataset_version"],
                "Git Hash": run["git_commit"]
            })
        return pd.DataFrame(rows)

    @staticmethod
    def get_code_snippet() -> str:
        """Return authentic MLflow python logging snippet."""
        return """import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

# Set experiment name
mlflow.set_experiment("churn_prediction_quest")

with mlflow.start_run(run_name="rf_tuned_depth5"):
    # 1. Log Hyperparameters
    mlflow.log_param("model_family", "RandomForest")
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 5)
    mlflow.log_param("data_version", "v2.0-cleaned")

    # 2. Train Model
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    # 3. Log Performance Metrics
    f1 = f1_score(y_test, model.predict(X_test))
    mlflow.log_metric("f1_score", f1)

    # 4. Log Model Artifact to Registry
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="churn_model",
        registered_model_name="ChurnGuard"
    )
print("Run successfully logged to MLflow Tracking Server!")"""

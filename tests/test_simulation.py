"""
MLOpsHub: Production Quest - Core Simulation Test Suite

This module runs automated unit tests on:
- Synthetic dataset generation (clean, dirty, drifted)
- DVC command execution and version retrieval
- Scikit-learn model training and metric computation
- Feature store catalog and training-serving skew detection
- Automated ML test runner (pass and intentional failure modes)
- Drift calculations (Population Stability Index, KS-test)
- AI dependency graph structure and root cause candidate ranking
- Mission registry routing for all 21 missions
"""

import numpy as np
import pytest
from src.data.dvc_sim import DVCSimulator
from src.data.generator import (
    generate_clean_dataset,
    generate_dirty_dataset,
    generate_drifted_dataset
)
from src.features.feature_store import FeatureStore
from src.incidents.dependency_graph import DependencyGraphBuilder
from src.incidents.incident_engine import IncidentEngine
from src.incidents.rca_ranker import RootCauseRanker
from src.missions.registry import MissionRegistry
from src.models.mlflow_sim import MLflowSimulator
from src.models.trainer import ChurnModelTrainer
from src.pipeline.monitoring import calculate_psi, evaluate_feature_drift
from src.testing.test_suite import MLTestSuite


def test_clean_data_generation() -> None:
    """Verify that clean data generation produces valid columns and target balance."""
    df = generate_clean_dataset(n_samples=500, random_state=42)
    assert len(df) == 500
    assert "churn" in df.columns
    assert df["churn"].isin([0, 1]).all()
    assert df["monthly_spend"].min() >= 0
    assert df["age"].min() >= 18
    assert df.isnull().sum().sum() == 0


def test_dirty_data_generation() -> None:
    """Verify that dirty data contains intentional defects (NaNs, negative values, duplicates)."""
    df_dirty = generate_dirty_dataset(n_samples=500, random_state=42)
    assert df_dirty.isnull().sum().sum() > 0
    assert (df_dirty["monthly_spend"] < 0).any()
    assert df_dirty.duplicated().sum() > 0


def test_dvc_simulator() -> None:
    """Verify DVC version retrieval, command simulation, and pointer file content."""
    df_v2 = DVCSimulator.get_dataset("v2")
    assert len(df_v2) == 1200

    out, status = DVCSimulator.execute_command("dvc init")
    assert status == "success"
    assert "Initializing DVC" in out

    dvc_yaml = DVCSimulator.generate_dvc_file_content("v2")
    assert "md5:" in dvc_yaml
    assert "path: churn.csv" in dvc_yaml


def test_model_training_and_inference() -> None:
    """Verify scikit-learn model training, metric evaluation, and single inference."""
    df = generate_clean_dataset(n_samples=600, random_state=42)
    trainer = ChurnModelTrainer(model_type="logistic_regression", random_state=42)
    metrics = trainer.train_and_evaluate(df)

    assert 0.0 <= metrics["accuracy"] <= 1.0
    assert 0.0 <= metrics["f1"] <= 1.0
    assert len(metrics["confusion_matrix"]) == 2

    # Single customer inference
    sample_cust = {
        "age": 35,
        "tenure": 12,
        "monthly_spend": 75.5,
        "support_calls": 2,
        "usage_frequency": 14,
        "contract_type": "Month-to-month",
        "region": "North-America",
        "customer_segment": "Standard"
    }
    pred, prob = trainer.predict_single(sample_cust)
    assert pred in [0, 1]
    assert 0.0 <= prob <= 1.0


def test_feature_store_and_skew() -> None:
    """Verify feature registry listing and training-serving skew simulation."""
    feat_df = FeatureStore.list_features()
    assert len(feat_df) >= 4
    assert "customer_monthly_spend" in feat_df["Feature Name"].values

    skew = FeatureStore.simulate_skew_scenario()
    assert skew["feature_name"] == "customer_monthly_spend"
    assert len(skew["samples"]) > 0


def test_ml_test_suite_runner() -> None:
    """Verify that MLTestSuite passes on clean data and detects injected corruptions."""
    # Clean data pass
    all_pass, results, _ = MLTestSuite.run_all_tests(use_corrupted_data=False)
    assert all_pass is True

    # Dirty data failure
    all_pass_dirty, results_dirty, stdout_dirty = MLTestSuite.run_all_tests(use_corrupted_data=True)
    assert all_pass_dirty is False
    assert "FAILURES" in stdout_dirty


def test_drift_calculation_psi() -> None:
    """Verify that PSI detects distribution drift between clean and drifted data."""
    base = np.random.normal(100, 15, 1000)
    identical = np.random.normal(100, 15, 1000)
    drifted = np.random.normal(180, 25, 1000)

    psi_stable = calculate_psi(base, identical)
    psi_drifted = calculate_psi(base, drifted)

    assert psi_stable < 0.10
    assert psi_drifted > 0.20


def test_incident_engine_and_rca_ranker() -> None:
    """Verify incident repository and candidate ranking ordering."""
    inc = IncidentEngine.get_incident("A")
    assert inc["id"] == "INC-042"
    assert inc["f1_after"] < inc["f1_before"]

    candidates = RootCauseRanker.rank_candidates("A")
    assert len(candidates) >= 3
    # Top suspect should be the monthly_spend feature
    assert "monthly_spend" in candidates[0]["name"]
    assert candidates[0]["confidence_pct"] > 80.0


def test_dependency_graph_construction() -> None:
    """Verify that the AI system dependency graph builds correctly."""
    fig = DependencyGraphBuilder.create_plotly_figure(selected_node="feature_store")
    assert fig is not None
    assert len(DependencyGraphBuilder.NODES) == 7
    assert len(DependencyGraphBuilder.EDGES) == 6


def test_all_21_missions_instantiation() -> None:
    """Verify that all 21 mission classes can be loaded from the registry."""
    for i in range(1, 22):
        mid = f"m{i:02d}"
        mission = MissionRegistry.get_mission(mid)
        assert mission is not None
        assert mission.mission_id == mid
        assert len(mission.title) > 0
        assert len(mission.role_name) > 0

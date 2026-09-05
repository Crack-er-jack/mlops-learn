"""
MLOpsHub: Production Quest - Synthetic Data Generator for ChurnGuard

This module generates realistic tabular customer retention data:
- Clean baseline data for training
- Dirty dataset for data validation exercises (nulls, duplicates, negative values)
- Drifted dataset for production monitoring and incident simulations
- Subgroup skewed data for fairness and bias analysis
"""

import numpy as np
import pandas as pd


def generate_clean_dataset(n_samples: int = 1200, random_state: int = 42) -> pd.DataFrame:
    """
    Generate clean, production-grade tabular customer data for ChurnGuard.

    Args:
        n_samples: Number of synthetic customer records to produce.
        random_state: Seed for deterministic reproducibility.

    Returns:
        pd.DataFrame containing features and binary churn target.
    """
    rng = np.random.RandomState(random_state)

    customer_ids = [f"CUST-{10000 + i}" for i in range(n_samples)]
    ages = rng.randint(18, 70, size=n_samples)
    tenures = rng.randint(1, 60, size=n_samples)
    monthly_spends = np.round(rng.uniform(25.0, 150.0, size=n_samples), 2)
    support_calls = rng.poisson(lam=2.2, size=n_samples)
    usage_frequency = np.clip(rng.normal(loc=18.0, scale=6.0, size=n_samples).astype(int), 1, 40)

    contract_types = rng.choice(["Month-to-month", "One-year", "Two-year"], size=n_samples, p=[0.55, 0.28, 0.17])
    regions = rng.choice(["North-America", "Europe", "Asia-Pacific", "Latin-America"], size=n_samples, p=[0.40, 0.30, 0.20, 0.10])
    segments = rng.choice(["Standard", "Premium", "Enterprise"], size=n_samples, p=[0.60, 0.30, 0.10])

    # Calculate calibrated log-odds of churn based on realistic business factors
    # High support calls, month-to-month contracts, low tenure, and high spend increase churn
    contract_penalty = np.where(contract_types == "Month-to-month", 1.3, -0.9)
    noise = rng.normal(0, 1.25, size=n_samples)
    log_odds = (
        -0.6
        + (support_calls * 0.70)
        - (tenures * 0.065)
        + (monthly_spends * 0.018)
        - (usage_frequency * 0.06)
        + contract_penalty
        + noise
    )

    # Convert to probability and sample binary churn
    probabilities = 1.0 / (1.0 + np.exp(-log_odds))
    churns = (probabilities > 0.50).astype(int)

    df = pd.DataFrame({
        "customer_id": customer_ids,
        "age": ages,
        "tenure": tenures,
        "monthly_spend": monthly_spends,
        "support_calls": support_calls,
        "usage_frequency": usage_frequency,
        "contract_type": contract_types,
        "region": regions,
        "customer_segment": segments,
        "churn": churns
    })

    return df


def generate_dirty_dataset(n_samples: int = 1200, random_state: int = 42) -> pd.DataFrame:
    """
    Generate an intentionally corrupted dataset for the Data Quality mission.
    Contains missing values, duplicate rows, negative spends, and casing inconsistencies.

    Args:
        n_samples: Number of records.
        random_state: Seed for reproducibility.

    Returns:
        pd.DataFrame with realistic data hygiene defects.
    """
    df = generate_clean_dataset(n_samples=n_samples, random_state=random_state)
    rng = np.random.RandomState(random_state)

    # 1. Introduce missing values (NaNs) in age and monthly_spend
    nan_age_idx = rng.choice(df.index, size=45, replace=False)
    df.loc[nan_age_idx, "age"] = np.nan

    nan_spend_idx = rng.choice(df.index, size=30, replace=False)
    df.loc[nan_spend_idx, "monthly_spend"] = np.nan

    # 2. Introduce invalid negative values (e.g., -2300, -50)
    neg_spend_idx = rng.choice(df.index, size=8, replace=False)
    df.loc[neg_spend_idx, "monthly_spend"] = [-2300.0, -150.0, -45.0, -99.99, -500.0, -12.0, -350.0, -88.0]

    # 3. Introduce duplicate rows
    dup_rows = df.iloc[:15].copy()
    df = pd.concat([df, dup_rows], ignore_index=True)

    # 4. Inconsistent categorical strings ('month-to-month' vs 'Month-to-month')
    inconsistent_idx = rng.choice(df[df["contract_type"] == "Month-to-month"].index, size=40, replace=False)
    df.loc[inconsistent_idx, "contract_type"] = "month-to-month"

    return df


def generate_drifted_dataset(
    n_samples: int = 600,
    drift_scenario: str = "feature_drift",
    random_state: int = 99
) -> pd.DataFrame:
    """
    Generate production inference data exhibiting statistical drift or schema errors
    for incident simulations (Incident INC-042).

    Args:
        n_samples: Number of production requests.
        drift_scenario: Type of drift ('feature_drift', 'schema_change', 'skew').
        random_state: Seed.

    Returns:
        pd.DataFrame containing drifted production inference requests.
    """
    rng = np.random.RandomState(random_state)
    df = generate_clean_dataset(n_samples=n_samples, random_state=random_state)

    if drift_scenario == "feature_drift":
        # Upstream transformation altered currency or calculation: spend shifted higher
        # Mean shifted from ~$87 to ~$215
        df["monthly_spend"] = np.round(df["monthly_spend"] * 2.4 + rng.normal(15, 10, size=n_samples), 2)
        # Usage frequency dropped
        df["usage_frequency"] = np.clip((df["usage_frequency"] * 0.45).astype(int), 1, 40)
    elif drift_scenario == "schema_change":
        # Upstream team renamed 'monthly_spend' to 'billing_amount'
        df.rename(columns={"monthly_spend": "billing_amount"}, inplace=True)
    elif drift_scenario == "skew":
        # Missing support_calls default in production
        df["support_calls"] = 0

    return df

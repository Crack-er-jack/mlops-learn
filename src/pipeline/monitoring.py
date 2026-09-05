"""
MLOpsHub: Production Quest - Production Observability & Drift Monitoring

This module computes statistical drift metrics between baseline training
distributions and live production inference requests:
- Population Stability Index (PSI)
- Kolmogorov-Smirnov (KS) two-sample test
- Mean / Median distribution shifts
- Production serving telemetry (latency, request count, error rate)
"""

from typing import Any, Dict, List, Tuple
import numpy as np
import pandas as pd
from scipy import stats


def calculate_psi(baseline: np.ndarray, target: np.ndarray, num_buckets: int = 10) -> float:
    """
    Compute Population Stability Index (PSI) between baseline and target distributions.
    Rule of thumb:
      PSI < 0.10: No significant shift (Stable)
      0.10 <= PSI < 0.20: Moderate shift (Warning)
      PSI >= 0.20: Significant distribution drift (Alert)

    Args:
        baseline: Reference array (e.g., training feature values).
        target: Live production inference array.
        num_buckets: Number of quantile bins.

    Returns:
        PSI float metric.
    """
    # Defensive check against empty arrays
    if len(baseline) == 0 or len(target) == 0:
        return 0.0

    # Determine quantile breakpoints from baseline
    quantiles = np.linspace(0, 100, num_buckets + 1)
    bins = np.percentile(baseline, quantiles)
    bins[0] = -np.inf
    bins[-1] = np.inf

    # Bucket counts
    base_counts = np.histogram(baseline, bins=bins)[0]
    target_counts = np.histogram(target, bins=bins)[0]

    # Convert to fractions with Laplace smoothing
    base_pct = (base_counts + 0.0001) / (len(baseline) + 0.0001 * num_buckets)
    target_pct = (target_counts + 0.0001) / (len(target) + 0.0001 * num_buckets)

    # Calculate PSI summation
    psi_value = np.sum((target_pct - base_pct) * np.log(target_pct / base_pct))
    return float(np.round(psi_value, 4))


def evaluate_feature_drift(
    baseline_df: pd.DataFrame,
    production_df: pd.DataFrame,
    features: List[str]
) -> List[Dict[str, Any]]:
    """
    Evaluate statistical drift across multiple numerical features.

    Args:
        baseline_df: Reference training dataset.
        production_df: Current production serving window dataset.
        features: List of numeric feature column names.

    Returns:
        List of drift evaluation dictionaries.
    """
    drift_reports = []

    for feat in features:
        if feat not in baseline_df.columns or feat not in production_df.columns:
            continue

        base_vals = baseline_df[feat].dropna().values
        prod_vals = production_df[feat].dropna().values

        # 1. PSI Calculation
        psi_score = calculate_psi(base_vals, prod_vals)

        # 2. Kolmogorov-Smirnov Test
        ks_res = stats.ks_2samp(base_vals, prod_vals)
        ks_stat = float(np.round(ks_res.statistic, 4))
        p_val = float(np.round(ks_res.pvalue, 5))

        # 3. Mean Shift
        base_mean = float(np.mean(base_vals))
        prod_mean = float(np.mean(prod_vals))
        mean_shift_pct = float(np.round(((prod_mean - base_mean) / (base_mean + 1e-6)) * 100, 2))

        # Status categorization
        if psi_score >= 0.20 or p_val < 0.01:
            status = "🔴 HIGH DRIFT"
            recommendation = "Investigate feature transformation & trigger alert."
        elif psi_score >= 0.10:
            status = "🟡 MODERATE DRIFT"
            recommendation = "Monitor distribution; retrain candidate model."
        else:
            status = "🟢 STABLE"
            recommendation = "Distribution within baseline boundaries."

        drift_reports.append({
            "feature": feat,
            "baseline_mean": round(base_mean, 2),
            "production_mean": round(prod_mean, 2),
            "mean_shift_pct": mean_shift_pct,
            "psi_score": psi_score,
            "ks_statistic": ks_stat,
            "p_value": p_val,
            "status": status,
            "recommendation": recommendation
        })

    return drift_reports


def get_production_telemetry() -> Dict[str, Any]:
    """Return production serving telemetry metrics for ChurnGuard."""
    return {
        "uptime_pct": 99.98,
        "total_requests_24h": 142850,
        "average_latency_ms": 18.4,
        "p99_latency_ms": 42.1,
        "error_rate_pct": 0.02,
        "active_model_version": "ChurnGuard v3.0",
        "active_container": "docker://neonbyte/churnguard:v3.0.0",
        "data_lineage": "dvc: c0d3e4f (v3.0-features)"
    }

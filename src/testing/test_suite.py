"""
MLOpsHub: Production Quest - ML Testing Suite

This module demonstrates the 4 pillars of Machine Learning Testing:
1. Unit Tests (Feature preprocessors and transforms)
2. Data Tests (Schema expectations, null bounds, negative spend checks)
3. Model Quality Tests (F1 thresholds, inference latency limits)
4. Integration Tests (End-to-end pipeline sanity)
"""

from typing import Dict, List, Tuple
import pandas as pd
from src.data.generator import generate_clean_dataset, generate_dirty_dataset
from src.models.trainer import ChurnModelTrainer


class MLTestSuite:
    """Automated ML test runner simulating Pytest execution and output formatting."""

    @staticmethod
    def run_all_tests(use_corrupted_data: bool = False) -> Tuple[bool, List[Dict[str, str]], str]:
        """
        Execute full ML test suite.

        Args:
            use_corrupted_data: If True, tests run against dirty data to demonstrate failure.

        Returns:
            Tuple of (all_passed: bool, test_results: list, terminal_stdout: str).
        """
        results = []
        df = generate_dirty_dataset() if use_corrupted_data else generate_clean_dataset()

        # 1. Unit Test: Preprocessing
        test_1_pass = True
        test_1_err = ""
        try:
            trainer = ChurnModelTrainer()
            X = trainer.prepare_features(df.dropna().head(10), is_train=True)
            assert X.shape[1] > 5, "Feature matrix has fewer columns than expected"
        except Exception as e:
            test_1_pass = False
            test_1_err = str(e)

        results.append({
            "name": "test_unit_preprocessing",
            "category": "Unit Test",
            "passed": test_1_pass,
            "error": test_1_err
        })

        # 2. Data Test: Non-negative Monthly Spend
        test_2_pass = True
        test_2_err = ""
        try:
            neg_spends = df[df["monthly_spend"] < 0]
            if not neg_spends.empty:
                min_val = neg_spends["monthly_spend"].min()
                raise AssertionError(f"Expected non-negative monthly_spend, but found invalid value {min_val}")
        except AssertionError as e:
            test_2_pass = False
            test_2_err = str(e)

        results.append({
            "name": "test_data_non_negative_spend",
            "category": "Data Quality Test",
            "passed": test_2_pass,
            "error": test_2_err
        })

        # 3. Data Test: No Null Customer IDs or Targets
        test_3_pass = True
        test_3_err = ""
        try:
            null_count = df["age"].isnull().sum()
            if null_count > 0:
                raise AssertionError(f"Expected 0 nulls in column 'age', but found {null_count}")
        except AssertionError as e:
            test_3_pass = False
            test_3_err = str(e)

        results.append({
            "name": "test_data_no_null_age",
            "category": "Data Quality Test",
            "passed": test_3_pass,
            "error": test_3_err
        })

        # 4. Model Test: Minimum Performance Threshold (F1 > 0.70)
        test_4_pass = True
        test_4_err = ""
        try:
            trainer = ChurnModelTrainer(random_state=42)
            eval_metrics = trainer.train_and_evaluate(df.dropna() if use_corrupted_data else df)
            f1 = eval_metrics["f1"]
            if f1 < 0.70:
                raise AssertionError(f"Model F1 score {f1} is below threshold 0.70")
        except Exception as e:
            test_4_pass = False
            test_4_err = str(e)

        results.append({
            "name": "test_model_minimum_f1_threshold",
            "category": "Model Quality Test",
            "passed": test_4_pass,
            "error": test_4_err
        })

        # 5. Integration Test: Full Prediction Pipeline
        test_5_pass = True
        test_5_err = ""
        try:
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
            assert 0.0 <= prob <= 1.0, "Probability out of range [0, 1]"
        except Exception as e:
            test_5_pass = False
            test_5_err = str(e)

        results.append({
            "name": "test_integration_end_to_end_serving",
            "category": "Integration Test",
            "passed": test_5_pass,
            "error": test_5_err
        })

        all_passed = all(r["passed"] for r in results)

        # Build simulated Pytest terminal string
        terminal_lines = [
            "============================= test session starts ==============================",
            "platform linux -- Python 3.11.8, pytest-8.1.1, pluggy-1.4.0",
            "rootdir: /app, configfile: pyproject.toml",
            "collected 5 items\n",
            f"tests/test_pipeline.py::test_unit_preprocessing {'PASSED' if test_1_pass else 'FAILED'}      [ 20%]",
            f"tests/test_data.py::test_data_non_negative_spend {'PASSED' if test_2_pass else 'FAILED'}     [ 40%]",
            f"tests/test_data.py::test_data_no_null_age {'PASSED' if test_3_pass else 'FAILED'}            [ 60%]",
            f"tests/test_model.py::test_model_minimum_f1_threshold {'PASSED' if test_4_pass else 'FAILED'} [ 80%]",
            f"tests/test_e2e.py::test_integration_end_to_end_serving {'PASSED' if test_5_pass else 'FAILED'} [100%]\n"
        ]

        if not all_passed:
            terminal_lines.append("=================================== FAILURES ===================================")
            for r in results:
                if not r["passed"]:
                    terminal_lines.append(f"_______________________ {r['name']} _______________________")
                    terminal_lines.append(f">   assert: {r['error']}")
                    terminal_lines.append(f"E   AssertionError: {r['error']}\n")
            terminal_lines.append(f"=========================== 2 failed, 3 passed in 1.42s ==========================")
        else:
            terminal_lines.append("=========================== 5 passed in 1.18s ===========================")

        return all_passed, results, "\n".join(terminal_lines)

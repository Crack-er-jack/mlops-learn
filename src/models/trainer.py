"""
MLOpsHub: Production Quest - Scikit-Learn Model Training & Evaluation Engine

This module trains lightweight CPU-friendly classification models
(Logistic Regression and Random Forest) for ChurnGuard, computing
essential metrics: Accuracy, Precision, Recall, F1 score, and Confusion Matrix.
"""

from typing import Any, Dict, List, Tuple
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler


class ChurnModelTrainer:
    """End-to-end model trainer for ChurnGuard retention models."""

    FEATURE_NUMERIC = ["age", "tenure", "monthly_spend", "support_calls", "usage_frequency"]
    FEATURE_CATEGORICAL = ["contract_type", "region", "customer_segment"]
    TARGET = "churn"

    def __init__(self, model_type: str = "logistic_regression", random_state: int = 42) -> None:
        """
        Initialize trainer with specified algorithm and random seed.

        Args:
            model_type: 'logistic_regression' or 'random_forest'.
            random_state: Reproducibility seed.
        """
        self.model_type = model_type
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
        self.feature_names: List[str] = []

        if model_type == "random_forest":
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=5,
                random_state=random_state
            )
        else:
            self.model = LogisticRegression(
                C=1.0,
                max_iter=500,
                random_state=random_state
            )

    def prepare_features(self, df: pd.DataFrame, is_train: bool = True) -> np.ndarray:
        """
        Transform raw DataFrame into scaled, one-hot encoded numeric matrix.

        Args:
            df: Input customer DataFrame.
            is_train: If True, fits encoders; if False, transforms.

        Returns:
            Processed numpy feature array.
        """
        # Clean any missing values defensively
        df_clean = df.copy()
        for col in self.FEATURE_NUMERIC:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].fillna(df_clean[col].median())

        num_data = df_clean[self.FEATURE_NUMERIC].values
        cat_data = df_clean[self.FEATURE_CATEGORICAL].values

        if is_train:
            scaled_num = self.scaler.fit_transform(num_data)
            encoded_cat = self.encoder.fit_transform(cat_data)
            cat_names = self.encoder.get_feature_names_out(self.FEATURE_CATEGORICAL)
            self.feature_names = list(self.FEATURE_NUMERIC) + list(cat_names)
        else:
            scaled_num = self.scaler.transform(num_data)
            encoded_cat = self.encoder.transform(cat_data)

        return np.hstack([scaled_num, encoded_cat])

    def train_and_evaluate(
        self,
        df: pd.DataFrame,
        test_size: float = 0.25
    ) -> Dict[str, Any]:
        """
        Fit model on train split and compute full evaluation metrics on test split.

        Args:
            df: Input dataset.
            test_size: Fraction of samples reserved for testing.

        Returns:
            Dictionary containing metrics, confusion matrix, and feature importances.
        """
        X = self.prepare_features(df, is_train=True)
        y = df[self.TARGET].values

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state, stratify=y
        )

        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        y_prob = self.model.predict_proba(X_test)[:, 1]

        acc = float(accuracy_score(y_test, y_pred))
        prec = float(precision_score(y_test, y_pred, zero_division=0))
        rec = float(recall_score(y_test, y_pred, zero_division=0))
        f1 = float(f1_score(y_test, y_pred, zero_division=0))
        auc = float(roc_auc_score(y_test, y_prob))
        cm = confusion_matrix(y_test, y_pred).tolist()

        # Compute feature importance / weights
        if hasattr(self.model, "feature_importances_"):
            importances = self.model.feature_importances_
        else:
            importances = np.abs(self.model.coef_[0])

        feature_imp_dict = dict(zip(self.feature_names, [float(x) for x in importances]))
        sorted_imp = sorted(feature_imp_dict.items(), key=lambda item: item[1], reverse=True)[:8]

        return {
            "model_type": self.model_type,
            "random_state": self.random_state,
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1": round(f1, 4),
            "roc_auc": round(auc, 4),
            "confusion_matrix": cm,
            "top_features": sorted_imp,
            "n_train": len(X_train),
            "n_test": len(X_test)
        }

    def predict_single(self, customer_dict: Dict[str, Any]) -> Tuple[int, float]:
        """
        Inference on a single customer record.

        Args:
            customer_dict: Mapping of feature names to values.

        Returns:
            Tuple of (predicted_class, churn_probability).
        """
        df_single = pd.DataFrame([customer_dict])
        X_single = self.prepare_features(df_single, is_train=False)
        pred = int(self.model.predict(X_single)[0])
        prob = float(self.model.predict_proba(X_single)[0, 1])
        return pred, prob

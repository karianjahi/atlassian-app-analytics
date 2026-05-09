import joblib
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from .models import CustomerHealth


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "churn_model.joblib"

FEATURE_COLUMNS = [
    "usage_score",
    "feature_adoption_score",
    "reliability_score",
    "support_score",
    "company_size",
]


def build_training_dataframe():
    records = CustomerHealth.objects.select_related("customer").all()

    data = []

    for record in records:
        data.append(
            {
                "usage_score": record.usage_score,
                "feature_adoption_score": record.feature_adoption_score,
                "reliability_score": record.reliability_score,
                "support_score": record.support_score,
                "company_size": record.customer.company_size,
                "did_churn": int(record.did_churn),
            }
        )

    return pd.DataFrame(data)


def train_churn_model():
    df = build_training_dataframe()

    if df.empty:
        return None

    if df["did_churn"].nunique() < 2:
        return None

    X = df[FEATURE_COLUMNS]
    y = df["did_churn"]

    if len(df) < 5:
        model = LogisticRegression(max_iter=1000)
        model.fit(X, y)

        joblib.dump(model, MODEL_PATH)

        return {
            "model": model,
            "accuracy": None,
        }

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    joblib.dump(model, MODEL_PATH)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    return {
        "model": model,
        "accuracy": round(accuracy * 100, 2),
    }


def load_trained_model():
    if not MODEL_PATH.exists():
        return None

    return joblib.load(MODEL_PATH)


def get_or_train_model():
    model = load_trained_model()

    if model is not None:
        return model

    result = train_churn_model()

    if result is None:
        return None

    return result["model"]


def build_feature_row(customer_health):
    return [[
        customer_health.usage_score,
        customer_health.feature_adoption_score,
        customer_health.reliability_score,
        customer_health.support_score,
        customer_health.customer.company_size,
    ]]


def predict_churn_probability(customer_health: CustomerHealth):
    model = get_or_train_model()

    if model is None:
        return None

    features = build_feature_row(customer_health)

    probability = model.predict_proba(features)[0][1]

    return round(probability * 100, 2)


def update_ml_churn_probability(customer_health):
    probability = predict_churn_probability(customer_health)

    if probability is None:
        return None

    customer_health.ml_churn_probability = probability
    customer_health.save(update_fields=["ml_churn_probability"])

    return probability


def update_all_ml_churn_probabilities():
    model = get_or_train_model()

    if model is None:
        return 0

    records = CustomerHealth.objects.select_related("customer").all()

    updated = 0

    for record in records:
        features = build_feature_row(record)
        probability = model.predict_proba(features)[0][1]

        record.ml_churn_probability = round(probability * 100, 2)
        record.save(update_fields=["ml_churn_probability"])

        updated += 1

    return updated


def get_model_feature_importance():
    result = train_churn_model()

    if result is None:
        return None

    model = result["model"]
    coefficients = model.coef_[0]

    importance = [
        {
            "feature": feature,
            "coefficient": round(coef, 4),
        }
        for feature, coef in zip(FEATURE_COLUMNS, coefficients)
    ]

    return importance
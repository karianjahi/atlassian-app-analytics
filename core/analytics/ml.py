import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from .models import CustomerHealth


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

    # Create features (X) and target (y)
    X = df[
        [
            "usage_score",
            "feature_adoption_score",
            "reliability_score",
            "support_score",
            "company_size",
        ]
    ]
    y = df["did_churn"]
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    return model


def predict_churn_probability(customer_health):
    model = train_churn_model()

    if model is None:
        return None

    features = [
        [
            customer_health.usage_score,
            customer_health.feature_adoption_score,
            customer_health.reliability_score,
            customer_health.support_score,
            customer_health.customer.company_size,
        ]
    ]
    
    probability = model.predict_proba(features)[0][1] # [first customer][churn probability]
    return round(probability * 100, 2)

def update_ml_churn_probability(customer_health):
    probability = predict_churn_probability(customer_health)
    if probability is None:
        return None
    customer_health.ml_churn_probability = probability
    customer_health.save(update_fields=["ml_churn_probability"])
    return probability

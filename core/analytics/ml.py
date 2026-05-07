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
    X = df[["usage_score", "feature_adoption_score", "reliability_score", "support_score", "support_score", "company_size"]]
    print(X)
    y = df["did_churn"]
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    return model

    
from rest_framework import serializers
from .models import Customer, CustomerHealth, UsageEvent

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

class CustomerHealthSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(
        source = "customer.company_name",
        read_only = True
    )
    class Meta:
        model = CustomerHealth
        fields = [
            "id",
            "customer",
            "customer_name",
            "usage_score",
            "feature_adoption_score",
            "reliability_score",
            "support_score",
            "health_score",
            "churn_risk",
            "risk_label",
            "calculated_at",
        ]

class UsageEventSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(
        source = "customer.company_name",
        read_only = True
    )
    
    class Meta:
        model = UsageEvent
        fields = [
            "id",
            "customer",
            "customer_name",
            "event_type",
            "timestamp",
            "metadata",
            "created_at",
        ]
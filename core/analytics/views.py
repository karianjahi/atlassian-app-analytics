from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Avg
from django.db.models.functions import TruncDate

from .models import Customer, CustomerHealth
from analytics.services import (
    generate_risk_reasons,
    generate_recommended_actions,
)

# for api
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import (
    CustomerSerializer,
    CustomerHealthSerializer,
    UsageEventSerializer,
)


def landing_page(request):
    return render(request, "analytics/landing_page.html")


def dashboard(request):
    return render(request, "analytics/dashboard.html")


def customer_detail(request, customer_id):
    return render(request, "analytics/customer_detail.html")


"""
API Endpoints
"""


@api_view(["GET"])
def customer_list_api(request):
    "Get request → fetch customers → serialize → return JSON"
    customers = Customer.objects.all()
    country = request.GET.get("country")
    if country:
        customers = Customer.objects.filter(country__iexact=country)
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def customer_detail_api(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    serializer = CustomerSerializer(customer)
    return Response(serializer.data)


@api_view(["GET"])
def customer_health_api(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    health = getattr(customer, "health", None)

    if not health:
        return Response({"detail": "No health data found"}, status=404)

    serializer = CustomerHealthSerializer(health)
    return Response(serializer.data)


@api_view(["GET"])
def customer_events_api(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    events = customer.usage_events.all()
    serializer = UsageEventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def customer_health_list_api(request):
    health_records = CustomerHealth.objects.select_related("customer").all()
    risk_label = request.GET.get(
        "risk_label"
    )  # captures the term 'risk_label' from the incoming request

    # filtering by risk
    if risk_label:
        health_records = health_records.filter(risk_label=risk_label)

    # ordering
    ordering = request.GET.get("ordering")
    if ordering:
        health_records = health_records.order_by(ordering)

    serializer = CustomerHealthSerializer(health_records, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def summary_api(request):
    total_customers = Customer.objects.count()

    avg_health = (
        CustomerHealth.objects.aggregate(Avg("health_score"))["health_score__avg"] or 0
    )

    healthy = CustomerHealth.objects.filter(risk_label="healthy").count()
    watch = CustomerHealth.objects.filter(risk_label="watch").count()
    high_risk = CustomerHealth.objects.filter(risk_label="high_risk").count()

    data = {
        "total_customers": total_customers,
        "average_health_score": round(avg_health, 1),
        "healthy": healthy,
        "watch": watch,
        "high_risk": high_risk,
    }

    return Response(data)


@api_view(["GET"])
def dashboard_data_api(request):
    health_records = CustomerHealth.objects.select_related("customer").all()

    data = {
        "summary": {
            "total_customers": Customer.objects.count(),
            "healthy": health_records.filter(risk_label="healthy").count(),
            "watch": health_records.filter(risk_label="watch").count(),
            "high_risk": health_records.filter(risk_label="high_risk").count(),
            "average_health_score": round(
                health_records.aggregate(Avg("health_score"))["health_score__avg"] or 0,
                2,
            ),
        },
        "customers": [
            {
                "id": record.customer.id,
                "company_name": record.customer.company_name,
                "app_name": record.customer.app_name,
                "health_score": record.health_score,
                "churn_risk": record.churn_risk,
                "ml_churn_probability": record.ml_churn_probability,
                "risk_label": record.get_risk_label_display(),
            }
            for record in health_records
        ],
    }

    return Response(data)


@api_view(["GET"])
def customer_detail_data_api(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    health = getattr(customer, "health", None)
    events = customer.usage_events.all()

    event_distribution = (
        events.values("event_type").annotate(count=Count("id")).order_by("event_type")
    )

    events_over_time = (
        events.annotate(event_date=TruncDate("timestamp"))
        .values("event_date")
        .annotate(count=Count("id"))
        .order_by("event_date")
    )
    # print(event_distribution)
    data = {
        "customer": {
            "id": customer_id,
            "company_name": customer.company_name,
            "country": customer.country,
            "company_size": customer.company_size,
            "license_tier": customer.get_license_tier_display(),
            "app_name": customer.app_name,
            "installed_at": customer.installed_at,
        },
        "health": 
            None
            if not health
            else {
                "usage_score": health.usage_score,
                "feature_adoption_score": health.feature_adoption_score,
                "reliability_score": health.reliability_score,
                "support_score": health.support_score,
                "health_score": health.health_score,
                "churn_risk": health.churn_risk,
                "ml_churn_probability": health.ml_churn_probability,
                "risk_label": health.get_risk_label_display(),
            },
            "events": [
                {
                    "event_type": event.event_type,
                    "timestamp": event.timestamp,
                    "metadata": event.metadata,
                }
                for event in events[:20]
            ],
            "event_distribution": {
                "labels": [item["event_type"] for item in event_distribution],
                "counts": [item["count"] for item in event_distribution]
            },
            "events_over_time": {
                "labels": [item["event_date"].strftime("%Y-%m-%d") for item in events_over_time],
                "counts": [item["count"] for item in events_over_time]
            },
            "risk_reasons": generate_risk_reasons(customer),
            "recommended_actions":generate_recommended_actions(customer),
        
    }
    return Response(data)


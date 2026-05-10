import json
from datetime import timedelta
from math import ceil

import pandas as pd

from django.contrib import messages
from django.core.management import call_command
from django.db.models import Avg, Count
from django.db.models.functions import TruncDate
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import CSVUploadForm
from .models import Customer, CustomerHealth, CSVUploadLog, UsageEvent
from .serializers import (
    CustomerHealthSerializer,
    CustomerSerializer,
    UsageEventSerializer,
)

from analytics.ml import get_model_feature_importance, train_churn_model
from analytics.services import (
    forecast_next_health_score,
    generate_customer_alerts,
    generate_health_insights,
    generate_recommended_actions,
    generate_risk_reasons,
)


def landing_page(request):
    return render(request, "analytics/landing_page.html")


def dashboard(request):
    return render(request, "analytics/dashboard.html")


def customer_detail(request, customer_id):
    return render(request, "analytics/customer_detail.html")


def upload_csv(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)

        if form.is_valid():
            csv_file = form.cleaned_data["csv_file"]

            try:
                df = pd.read_csv(csv_file, sep=",", quotechar='"')
            except Exception as error:
                messages.error(request, f"Could not read CSV file: {error}")
                return redirect("upload_csv")

            required_columns = [
                "company_name",
                "app_name",
                "country",
                "company_size",
                "license_tier",
                "installed_at",
                "event_type",
                "timestamp",
                "metadata",
            ]

            missing_columns = [
                column for column in required_columns
                if column not in df.columns
            ]

            if missing_columns:
                messages.error(
                    request,
                    f"Missing required columns: {', '.join(missing_columns)}",
                )
                return redirect("upload_csv")

            customers_created = 0
            events_created = 0
            duplicates_skipped = 0
            invalid_rows_skipped = 0

            for _, row in df.iterrows():
                try:
                    installed_at_datetime = parse_datetime(str(row["installed_at"]))
                    event_timestamp = parse_datetime(str(row["timestamp"]))

                    if installed_at_datetime is None or event_timestamp is None:
                        invalid_rows_skipped += 1
                        continue

                    installed_at = installed_at_datetime.date()

                    metadata = {}
                    if pd.notna(row["metadata"]) and str(row["metadata"]).strip():
                        metadata = json.loads(row["metadata"])

                    customer, created = Customer.objects.get_or_create(
                        company_name=row["company_name"],
                        app_name=row["app_name"],
                        defaults={
                            "country": row["country"],
                            "company_size": int(row["company_size"]),
                            "license_tier": row["license_tier"],
                            "installed_at": installed_at,
                        },
                    )

                    if created:
                        customers_created += 1

                    event_exists = UsageEvent.objects.filter(
                        customer=customer,
                        event_type=row["event_type"],
                        timestamp=event_timestamp,
                    ).exists()

                    if event_exists:
                        duplicates_skipped += 1
                        continue

                    UsageEvent.objects.create(
                        customer=customer,
                        event_type=row["event_type"],
                        timestamp=event_timestamp,
                        metadata=metadata,
                    )

                    events_created += 1

                except Exception:
                    invalid_rows_skipped += 1

            call_command("update_customer_health")
            call_command("update_ml_churn")

            CSVUploadLog.objects.create(
                file_name=csv_file.name,
                events_created=events_created,
                customers_created=customers_created,
                duplicates_skipped=duplicates_skipped,
                invalid_rows_skipped=invalid_rows_skipped,
            )

            messages.success(
                request,
                (
                    f"Upload complete. "
                    f"Imported {events_created} events. "
                    f"Created {customers_created} customers. "
                    f"Skipped {duplicates_skipped} duplicate events. "
                    f"Skipped {invalid_rows_skipped} invalid rows. "
                    "Analytics and ML predictions refreshed."
                ),
            )

            return redirect("upload_csv")
    else:
        form = CSVUploadForm()
    upload_logs = CSVUploadLog.objects.order_by("-uploaded_at")[:20]
    return render(request, "analytics/upload_csv.html", {"form": form, "upload_logs": upload_logs,})


@api_view(["GET"])
def customer_list_api(request):
    customers = Customer.objects.all()

    country = request.GET.get("country")
    if country:
        customers = customers.filter(country__iexact=country)

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

    risk_label = request.GET.get("risk_label")
    if risk_label:
        health_records = health_records.filter(risk_label=risk_label)

    ordering = request.GET.get("ordering")
    if ordering:
        health_records = health_records.order_by(ordering)

    serializer = CustomerHealthSerializer(health_records, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def summary_api(request):
    avg_health = (
        CustomerHealth.objects.aggregate(Avg("health_score"))["health_score__avg"] or 0
    )

    data = {
        "total_customers": Customer.objects.count(),
        "average_health_score": round(avg_health, 1),
        "healthy": CustomerHealth.objects.filter(risk_label="healthy").count(),
        "watch": CustomerHealth.objects.filter(risk_label="watch").count(),
        "high_risk": CustomerHealth.objects.filter(risk_label="high_risk").count(),
    }

    return Response(data)


@api_view(["GET"])
def dashboard_data_api(request):
    health_records = CustomerHealth.objects.select_related("customer").all()

    page = int(request.GET.get("page", 1))
    page_size = int(request.GET.get("page_size", 20))

    total_records = health_records.count()
    total_pages = ceil(total_records / page_size) if total_records else 1

    start = (page - 1) * page_size
    end = start + page_size

    paginated_health_records = health_records.order_by("-churn_risk")[start:end]
    top_risk_customers = health_records.order_by("-ml_churn_probability")[:5]
    top_rule_based_risk_customers = health_records.order_by("-churn_risk")[:5]

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
            for record in paginated_health_records
        ],
        "risk_rankings": {
            "top_ml_risk": [
                {
                    "id": record.customer.id,
                    "company_name": record.customer.company_name,
                    "app_name": record.customer.app_name,
                    "ml_churn_probability": record.ml_churn_probability,
                    "health_score": record.health_score,
                }
                for record in top_risk_customers
            ],
            "top_rule_based_risk": [
                {
                    "id": record.customer.id,
                    "company_name": record.customer.company_name,
                    "app_name": record.customer.app_name,
                    "churn_risk": record.churn_risk,
                    "health_score": record.health_score,
                }
                for record in top_rule_based_risk_customers
            ],
        },
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_records": total_records,
            "total_pages": total_pages,
        },
    }

    return Response(data)


@api_view(["GET"])
def customer_detail_data_api(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    health = getattr(customer, "health", None)
    events = customer.usage_events.all()

    selected_range = request.GET.get("range", "30")
    if selected_range != "all":
        days = int(selected_range)
        start_date = timezone.now() - timedelta(days=days)
        events = events.filter(timestamp__gte=start_date)

    event_distribution = (
        events.values("event_type")
        .annotate(count=Count("id"))
        .order_by("event_type")
    )

    events_over_time = (
        events.annotate(event_date=TruncDate("timestamp"))
        .values("event_date")
        .annotate(count=Count("id"))
        .order_by("event_date")
    )

    data = {
        "customer": {
            "id": customer.id,
            "company_name": customer.company_name,
            "country": customer.country,
            "company_size": customer.company_size,
            "license_tier": customer.get_license_tier_display(),
            "app_name": customer.app_name,
            "installed_at": customer.installed_at,
        },
        "health": (
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
            }
        ),
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
            "counts": [item["count"] for item in event_distribution],
        },
        "events_over_time": {
            "labels": [
                item["event_date"].strftime("%Y-%m-%d")
                for item in events_over_time
            ],
            "counts": [item["count"] for item in events_over_time],
        },
        "risk_reasons": generate_risk_reasons(customer),
        "recommended_actions": generate_recommended_actions(customer),
        "health_insights": generate_health_insights(customer),
        "alerts": generate_customer_alerts(customer),
        "forecast": {
            "next_health_score": forecast_next_health_score(customer),
        },
    }

    return Response(data)


@api_view(["GET"])
def ml_model_metrics_api(request):
    result = train_churn_model()

    if result is None:
        return Response({"detail": "Not enough data to train model"}, status=400)

    return Response({"accuracy": result["accuracy"]})


@api_view(["GET"])
def ml_feature_importance_api(request):
    importance = get_model_feature_importance()

    if importance is None:
        return Response(
            {"detail": "Not enough data to train model"},
            status=400,
        )

    return Response({"feature_importance": importance})


@api_view(["GET"])
def customer_health_history_api(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    snapshots = customer.health_snapshots.all().order_by("created_at")

    data = {
        "labels": [
            snapshot.created_at.strftime("%Y-%m-%d %H:%M")
            for snapshot in snapshots
        ],
        "health_scores": [snapshot.health_score for snapshot in snapshots],
        "churn_risks": [snapshot.churn_risk for snapshot in snapshots],
        "ml_churn_probabilities": [
            snapshot.ml_churn_probability
            for snapshot in snapshots
        ],
    }

    return Response(data)
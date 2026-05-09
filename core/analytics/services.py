from datetime import timedelta

from django.utils import timezone

from .models import Customer, CustomerHealth, CustomerHealthSnapshot


ALPHA = 0.4
BETA = 0.25
GAMMA = 0.20
DELTA = 0.15

DAYS_FOR_RECENT_ACTIVITY = 30

FEATURE_EVENTS = [
    "created_clone",
    "used_dashboard_filter",
    "connected_external_data_source",
]

HEALTHY_THRESHOLD = 80
WATCH_THRESHOLD = 50
HIGH_RISK_CHURN_THRESHOLD = 40


def calculate_customer_health(customer: Customer) -> CustomerHealth:
    now = timezone.now()
    last_30_days = now - timedelta(days=DAYS_FOR_RECENT_ACTIVITY)

    events = customer.usage_events.all()
    recent_events = events.filter(timestamp__gte=last_30_days)

    total_recent_events = recent_events.count()
    error_count = recent_events.filter(event_type="sync_failed").count()
    support_count = recent_events.filter(event_type="opened_support_ticket").count()

    unique_features_used = (
        recent_events.filter(event_type__in=FEATURE_EVENTS)
        .values("event_type")
        .order_by()
        .distinct()
        .count()
    )

    usage_score = min(total_recent_events * 5, 100)
    feature_adoption_score = (unique_features_used / len(FEATURE_EVENTS)) * 100
    reliability_score = max(100 - error_count * 15, 0)
    support_score = max(100 - support_count * 20, 0)

    health_score = (
        ALPHA * usage_score
        + BETA * feature_adoption_score
        + GAMMA * reliability_score
        + DELTA * support_score
    )

    if health_score >= HEALTHY_THRESHOLD:
        risk_label = "healthy"
    elif health_score >= WATCH_THRESHOLD:
        risk_label = "watch"
    else:
        risk_label = "high_risk"

    did_churn = health_score < HIGH_RISK_CHURN_THRESHOLD
    churn_risk = 100 - health_score

    customer_health, _ = CustomerHealth.objects.update_or_create(
        customer=customer,
        defaults={
            "usage_score": round(usage_score, 2),
            "feature_adoption_score": round(feature_adoption_score, 2),
            "reliability_score": round(reliability_score, 2),
            "support_score": round(support_score, 2),
            "health_score": round(health_score, 2),
            "churn_risk": round(churn_risk, 2),
            "risk_label": risk_label,
            "did_churn": did_churn,
        },
    )

    create_customer_health_snapshot(customer_health)

    return customer_health


def calculate_customer_health_for_all_customers():
    customers = Customer.objects.all()

    results = []

    for customer in customers:
        customer_health = calculate_customer_health(customer)
        results.append(customer_health)

    return results


def generate_risk_reasons(customer: Customer):
    health = getattr(customer, "health", None)

    if not health:
        return ["No health score has been calculated yet."]

    reasons = []

    if health.usage_score < 50:
        reasons.append("Low recent product usage")

    if health.feature_adoption_score < 50:
        reasons.append("Limited feature adoption")

    if health.reliability_score < 70:
        reasons.append("High number of failed or error events")

    if health.support_score < 70:
        reasons.append("High support activity")

    if health.churn_risk >= 50:
        reasons.append("Overall churn risk is elevated")

    if not reasons:
        reasons.append("Customer appears healthy based on current signals")

    return reasons


def generate_recommended_actions(customer: Customer):
    health = getattr(customer, "health", None)

    if not health:
        return ["Calculate customer health before recommending actions."]

    actions = []

    if health.usage_score < 50:
        actions.append("Send onboarding or re-engagement email.")

    if health.feature_adoption_score < 50:
        actions.append("Suggest a short feature walkthrough or documentation.")

    if health.reliability_score < 70:
        actions.append("Investigate recent failed events and technical errors.")

    if health.support_score < 70:
        actions.append("Review open support tickets and follow up proactively.")

    if health.churn_risk >= 50:
        actions.append("Schedule a customer check-in before renewal.")

    if not actions:
        actions.append("No immediate action needed. Continue monitoring.")

    return actions


def create_customer_health_snapshot(customer_health: CustomerHealth):
    return CustomerHealthSnapshot.objects.create(
        customer=customer_health.customer,
        usage_score=customer_health.usage_score,
        feature_adoption_score=customer_health.feature_adoption_score,
        reliability_score=customer_health.reliability_score,
        support_score=customer_health.support_score,
        health_score=customer_health.health_score,
        churn_risk=customer_health.churn_risk,
        ml_churn_probability=customer_health.ml_churn_probability,
        risk_label=customer_health.risk_label,
    )


def generate_health_insights(customer: Customer):
    snapshots = customer.health_snapshots.order_by("created_at")

    if snapshots.count() < 2:
        return ["Not enough historical data to generate insights."]

    first = snapshots.first()
    latest = snapshots.last()

    insights = []

    health_change = latest.health_score - first.health_score

    if health_change > 0:
        insights.append(
            f"Health score improved by {round(health_change, 2)} points over time."
        )
    elif health_change < 0:
        insights.append(
            f"Health score declined by {round(abs(health_change), 2)} points over time."
        )
    else:
        insights.append("Health score remained stable over time.")

    ml_change = latest.ml_churn_probability - first.ml_churn_probability

    if ml_change > 0:
        insights.append(
            f"ML churn probability increased by {round(ml_change, 2)}%."
        )
    elif ml_change < 0:
        insights.append(
            f"ML churn probability decreased by {round(abs(ml_change), 2)}%."
        )

    if latest.health_score < HIGH_RISK_CHURN_THRESHOLD:
        insights.append("Customer is currently in a high-risk health range.")

    return insights


def generate_customer_alerts(customer: Customer):
    snapshots = customer.health_snapshots.order_by("created_at")

    if snapshots.count() < 2:
        return []

    first = snapshots.first()
    latest = snapshots.last()

    alerts = []

    health_drop = first.health_score - latest.health_score

    if health_drop >= 15:
        alerts.append(f"Health score dropped by {round(health_drop, 2)} points.")

    ml_increase = latest.ml_churn_probability - first.ml_churn_probability

    if ml_increase >= 20:
        alerts.append(
            f"ML churn probability increased by {round(ml_increase, 2)}%."
        )

    if latest.health_score < HIGH_RISK_CHURN_THRESHOLD:
        alerts.append("Customer is currently classified as high risk.")

    if latest.ml_churn_probability >= 80:
        alerts.append("ML model predicts extremely high churn probability.")

    return alerts


def forecast_next_health_score(customer: Customer):
    snapshots = customer.health_snapshots.order_by("created_at")

    if snapshots.count() < 2:
        return None

    recent_snapshots = list(snapshots.order_by("-created_at")[:5])[::-1]

    if len(recent_snapshots) < 2:
        return None

    first = recent_snapshots[0]
    latest = recent_snapshots[-1]

    score_change = latest.health_score - first.health_score
    number_of_steps = len(recent_snapshots) - 1
    average_change = score_change / number_of_steps

    forecast = latest.health_score + average_change
    forecast = max(0, min(100, forecast))

    return round(forecast, 2)
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import timedelta
from django.utils import timezone

# for api
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CustomerSerializer

from .models import Customer, CustomerHealth
from analytics.services import calculate_customer_health_for_all_customers, generate_risk_reasons, generate_recommended_actions

def landing_page(request):
    return render(request, "analytics/landing_page.html")
def dashboard(request):
    
    total_customers = Customer.objects.count()
    health_records = CustomerHealth.objects.select_related("customer")
    
    healthy_count = health_records.filter(risk_label="healthy").count()
    watch_count = health_records.filter(risk_label="watch").count()
    high_risk_count = health_records.filter(risk_label="high_risk").count()
    
    average_health_score = 0
    if total_customers > 0:
        total_health_score = sum([record.health_score for record in health_records])
        average_health_score = total_health_score/len(health_records)
    
    context = {
        "total_customers": total_customers,
        "healthy_count": healthy_count,
        "watch_count": watch_count,
        "high_risk_count": high_risk_count,
        "average_health_score": round(average_health_score, 2),
        "health_records": health_records
    }
    
    return render(request, "analytics/dashboard.html", context)
    

def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    
    # In case selection based on date/dates
    selected_range = request.GET.get("range", "30")
    events = customer.usage_events.all()
    if selected_range != "all":
        days = int(selected_range)
        start_date = timezone.now() - timedelta(days=days)
        events = events.filter(timestamp__gte=start_date)
    
    health = getattr(customer, "health", None) # dotting also works if you know the attribute by name. This one is meant for dynamic variables
    recent_events = events[:20]
    
    event_distribution = (
        events
        .values("event_type")
        .annotate(count=Count("id"))
        .order_by("event_type")
    )
    event_labels = [item["event_type"] for item in event_distribution]
    event_counts = [item["count"] for item in event_distribution]
    
    events_over_time = (
        events
        .annotate(event_date=TruncDate("timestamp"))
        .values("event_date")
        .annotate(count=Count("id"))
        .order_by("event_date")
    )
    
    time_labels = [item["event_date"] for item in events_over_time]
    time_counts = [item["count"] for item in events_over_time]
    
    risk_reasons = generate_risk_reasons(customer)
    recommended_actions = generate_recommended_actions(customer)
    
    context = {
        "customer": customer,
        "health": health,
        "recent_events": recent_events,
        "event_labels": event_labels,
        "event_counts": event_counts,
        "time_labels": time_labels,
        "time_counts": time_counts,
        "selected_range": selected_range,
        "risk_reasons": risk_reasons,
        "recommended_actions": recommended_actions,
    }
    return render(request, "analytics/customer_detail.html", context)
    
@api_view(["GET"])
def customer_list_api(request):
    "Get request → fetch customers → serialize → return JSON"
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)
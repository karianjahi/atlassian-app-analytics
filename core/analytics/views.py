from django.shortcuts import render, get_object_or_404
from .models import Customer, CustomerHealth
from analytics.services import calculate_customer_health_for_all_customers

def dashboard(request):
    calculate_customer_health_for_all_customers()
    
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
    health = getattr(customer, "health", None) # dotting also works if you know the attribute by name. This one is meant for dynamic variables
    recent_events = customer.usage_events.all()[:20]
    context = {
        "customer": customer,
        "health": health,
        "recent_events": recent_events
    }
    return render(request, "analytics/customer_detail.html", context)
    
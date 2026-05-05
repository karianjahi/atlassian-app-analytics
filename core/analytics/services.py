# We need to calculate customer health from the data available in the database

from datetime import timedelta 
from django.utils import timezone
from .models import Customer, CustomerHealth, UsageEvent

ALPHA = 0.4 # usage
BETA = 0.25 # feature adoption
GAMMA = 0.20 # reliability
DELTA = 0.15 # support

FEATURE_EVENTS = [
    "created_clone",
    "used_dashboard_filter",
    "connected_external_data_source",
]

def calculate_customer_health(customer: Customer) -> CustomerHealth:
    # Get the earliest date to consider (last 30 days)
    now = timezone.now()
    last_30_days = now - timedelta(days=30)
    
    # Get all events associated with this customer
    events = customer.usage_events.all()
    
    # only events in the last 30 days
    recent_events = events.filter(timestamp__gte=last_30_days)
    total_recent_events = recent_events.count()
    error_count = recent_events.filter(event_type="sync_failed").count()
    support_count = recent_events.filter(event_type="opened_support_ticket").count()
    
    # Lets get the unique features used based on usage events for this customer
    unique_features_used = (
        recent_events
        .filter(event_type__in=FEATURE_EVENTS)
        .values("event_type")
        .order_by() # this removes ordering before calling distinct
        .distinct()
        .count()
        )
    
    # Get the scores
    usage_score = min(total_recent_events * 5, 100) # usage is no of events x 5 or 100 whichever is smaller
    feature_adoption_score = (unique_features_used/len(FEATURE_EVENTS)) * 100
    reliability_score = max(100 - error_count * 15, 0) # Penalizes fails
    support_score = max(100 - support_count * 20, 0) # if no support, then perfect. if support, magnify the problem
    
    # calculate health score for this customer
    health_score = (
        ALPHA * usage_score
        + BETA * feature_adoption_score
        + GAMMA * reliability_score
        + DELTA * support_score
    )
    
    # Determine the risk label
    if health_score >= 80:
        risk_label = "healthy"
    elif health_score >= 50:
        risk_label = "watch"
    else:
        risk_label = "high_risk"
        
    # What is the churn risk for this customer
    churn_risk = 100 - health_score # higher churn risk for low customer health
    
    # Update the customer health model (table)
    customer_health, created = CustomerHealth.objects.update_or_create(
        customer=customer,
        defaults={
            "usage_score": round(usage_score, 2),
            "feature_adoption_score": round(feature_adoption_score, 2),
            "reliability_score": round(reliability_score, 2),
            "support_score": round(support_score, 2),
            "health_score": round(health_score, 2),
            "churn_risk": round(churn_risk, 2),
            "risk_label": risk_label,
        }
    )
    return customer_health
  
  # Calculate customer health for all customers
  
def calculate_customer_health_for_all_customers():
    # Get all customers (as in the whole customer table)
    customers = Customer.objects.all()
    results = []
    for customer in customers:
        customer_health = calculate_customer_health(customer)
        results.append(customer_health)
    return results
        

def generate_risk_reasons(customer:Customer):
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
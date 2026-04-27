from datetime import timedelta
from django.utils import timezone
from .models import Customer, CustomerHealth

ALPHA = 0.40 # usage
BETA = 0.25 # feature adoption
GAMMA = 0.20 # reliability
DELTA = 0.15 # support

FEATURE_EVENTS = [
    "created_clone",
    "used_dashboard_filter",
    "connected_external_data_source"
]

def calculate_customer_health(customer: Customer) -> CustomerHealth: # takes a customer object and returns a CustomerHealth object
    now = timezone.now()
    last_30_days = now - timedelta(days=30)   
    
    events = customer.usage_events.all()
    recent_events = events.filter(timestamp__gte=last_30_days) # timestamp greater or equal to translated by database
    
    total_recent_events = recent_events.count()
    error_count = recent_events.filter(event_type="sync_failed").count()
    support_count = recent_events.filter(event_type="opened_support_ticket").count()
    
    unique_features_used = (
        recent_events.filter(event_type__in=FEATURE_EVENTS).order_by().values("event_type").distinct().count()
    )
    
    usage_score = min(total_recent_events * 5, 100) # score between 0 and 100 -> 20 events = 100 score. more events, still select the max 100.
    feature_adoption_score = (unique_features_used / len(FEATURE_EVENTS)) * 100
    reliability_score = max(100-error_count * 15, 0) # Each error should reduce reliability by 15 points. Errors are considered very costly
    support_score = max(100 - support_count * 20, 0) ## too much support reflects friction
    
    health_score = (
        ALPHA * usage_score + BETA * feature_adoption_score + GAMMA * reliability_score + DELTA * support_score
    )
    
    if health_score >= 80:
        risk_label = "healthy"
    elif health_score >= 50:
        risk_label = "watch"
    else:
        risk_label = "high_risk"
    
    churn_risk = 100 - health_score
    
    
    
    
   
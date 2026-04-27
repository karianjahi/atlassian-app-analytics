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
    
    
    
   
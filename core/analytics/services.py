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

def calculate_customer_health(customer: Customer):
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
    
    
    
    
    
    
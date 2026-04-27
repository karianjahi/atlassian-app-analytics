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
   
    
    
   
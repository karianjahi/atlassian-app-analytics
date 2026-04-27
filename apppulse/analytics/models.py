from django.db import models

# Create your models here.
class Customer(models.Model):
    company_name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    company_size = models.IntegerField()
    
    LICENSE_CHOICES = [
        ("free", "Free"),
        ("standard", "Standard"),
        ("premium", "Premium"),
    ]
    
    license_tier = models.CharField(max_length=20, 
                                    choices=LICENSE_CHOICES, 
                                    default="free")
    
    app_name = models.CharField(max_length=255)
    installed_at = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.company_name} ({self.app_name})"

class UsageEvent(models.Model):
    EVENT_CHOICES = [
        ("installed_app", "Installed App"),
        ("configured_app", "Configured App"),
        ("created_clone", "Created Clone"),
        ("used_dashboard_filter", "Used Dashboard Filter"),
        ("connected_external_data_source", "Connected External Data Source"),
        ("sync_failed", "Sync Failed"),
        ("opened_support_ticket", "Opened Support Ticket"),
        ("subscription_cancelled", "Subscription Cancelled")
    ]
    
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE, 
        related_name="usage_events"
    )
    
    event_type = models.CharField(
        max_length=100,
        choices=EVENT_CHOICES
    )
    
    timestamp = models.DateTimeField()
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-timestamp"]
    def __str__(self):
        return f"{self.customer.company_name} - {self.event_type}"
    

class CustomerHealth(models.Model):
    RISK_LABEL_CHOICES = [
        ("healthy", "Healthy"),
        ("watch", "Watch"),
        ("high_risk", "High Risk")
    ]
    
    customer = models.OneToOneField(
        Customer, 
        on_delete=models.CASCADE,
        related_name="health"
    )
    
    usage_score = models.FloatField(default=0)
    feature_adoption_score = models.FloatField(default=0)
    reliability_score = models.FloatField(default=0)
    support_score = models.FloatField(default=0)
    
    health_score = models.FloatField(default=0)
    churn_risk = models.FloatField(default=0)
    
    risk_label = models.CharField(
        max_length=20,
        choices=RISK_LABEL_CHOICES,
        default="watch"
    )
    
    calculated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-health_score"]
    
    def __str__(self):
        return f"{self.customer.company_name} - {self.risk_label}"
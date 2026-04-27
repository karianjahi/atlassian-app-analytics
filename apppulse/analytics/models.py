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
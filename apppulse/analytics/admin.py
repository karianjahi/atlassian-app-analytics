from django.contrib import admin
from .models import Customer, UsageEvent, CustomerHealth

# Register your models here.
admin.site.register(Customer)
admin.site.register(UsageEvent)
admin.site.register(CustomerHealth)

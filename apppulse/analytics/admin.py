from django.contrib import admin
from .models import Customer, UsageEvent

# Register your models here.
admin.site.register(Customer)
admin.site.register(UsageEvent)

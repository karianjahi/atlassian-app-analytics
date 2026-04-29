from django.contrib import admin
from .models import Customer, UsageEvent

admin.site.register(Customer)
admin.site.register(UsageEvent)

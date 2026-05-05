from django.core.management.base import BaseCommand
from analytics.models import Customer
from analytics.services import calculate_customer_health

class Command(BaseCommand):
    help = "Update health scores for all customers"
    
    def handle(self, *args, **kwargs):
        customers = Customer.objects.all()
        for customer in customers:
            calculate_customer_health(customer)
        self.stdout.write(self.style.SUCCESS("Customer health updated successfully"))
from random import choice, randint
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from analytics.models import Customer, UsageEvent


class Command(BaseCommand):
    help = "Generate demo usage events for existing customers"

    def handle(self, *args, **kwargs):
        customers = Customer.objects.all()

        if not customers.exists():
            self.stdout.write(
                self.style.ERROR("No customers found. Run generate_customers first.")
            )
            return

        event_types = [
            "installed_app",
            "configured_app",
            "created_clone",
            "used_dashboard_filter",
            "connected_external_data_source",
            "sync_failed",
            "opened_support_ticket",
            "subscription_cancelled",
        ]

        created = 0

        for customer in customers:
            number_of_events = randint(10, 80)

            for _ in range(number_of_events):
                event_type = choice(event_types)

                UsageEvent.objects.create(
                    customer=customer,
                    event_type=event_type,
                    timestamp=timezone.now() - timedelta(days=randint(0, 180)),
                    metadata={
                        "source": "demo_generator",
                        "app_name": customer.app_name,
                        "license_tier": customer.license_tier,
                    },
                )

                created += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {created} usage events.")
        )
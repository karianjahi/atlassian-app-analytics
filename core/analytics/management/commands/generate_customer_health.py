from random import uniform
from django.core.management.base import BaseCommand

from analytics.models import Customer, CustomerHealth


class Command(BaseCommand):
    help = "Generate random customer health scores"

    def handle(self, *args, **kwargs):
        customers = Customer.objects.all()

        if not customers.exists():
            self.stdout.write(
                self.style.ERROR("No customers found. Run generate_customers first.")
            )
            return

        created = 0

        for customer in customers:
            # Random component scores (0–100)
            usage_score = uniform(0, 100)
            feature_adoption_score = uniform(0, 100)
            reliability_score = uniform(0, 100)
            support_score = uniform(0, 100)

            # Health score formula
            health_score = (
                usage_score * 0.4
                + feature_adoption_score * 0.25
                + reliability_score * 0.2
                + support_score * 0.15
            )

            # Churn risk (inverse of health)
            churn_risk = 100 - health_score

            # Risk label
            if health_score >= 80:
                risk_label = "Healthy"
            elif health_score >= 50:
                risk_label = "Watch"
            else:
                risk_label = "High Risk"

            # Create or update
            CustomerHealth.objects.update_or_create(
                customer=customer,
                defaults={
                    "usage_score": usage_score,
                    "feature_adoption_score": feature_adoption_score,
                    "reliability_score": reliability_score,
                    "support_score": support_score,
                    "health_score": health_score,
                    "churn_risk": churn_risk,
                    "risk_label": risk_label,
                },
            )

            created += 1

        self.stdout.write(
            self.style.SUCCESS(f"Generated health data for {created} customers.")
        )
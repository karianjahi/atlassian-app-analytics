from django.core.management.base import BaseCommand

from analytics.ml import update_all_ml_churn_probabilities


class Command(BaseCommand):
    help = "Update ML churn probabilities for all customers"

    def handle(self, *args, **kwargs):
        updated_count = update_all_ml_churn_probabilities()

        self.stdout.write(
            self.style.SUCCESS(
                f"Updated ML churn probability for {updated_count} customers"
            )
        )
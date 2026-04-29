from random import choice, randint
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from analytics.models import Customer


class Command(BaseCommand):
    help = "Generate 50 demo customers"

    def handle(self, *args, **kwargs):
        countries = [
            "Kenya", "Uganda", "Tanzania", "Rwanda", "Ethiopia",
            "Ghana", "Nigeria", "South Africa", "Egypt", "Morocco",
            "Germany", "France", "United Kingdom", "Canada", "United States",
            "India", "Australia", "Brazil", "Japan", "Netherlands",
        ]

        company_prefixes = [
            "Alpha", "Blue", "Nova", "Cloud", "Prime", "Data", "Sync",
            "Atlas", "Bright", "Future", "Digital", "Smart", "Core",
            "Next", "Vision", "Rapid", "Global", "Metro", "Vertex", "Apex",
        ]

        company_suffixes = [
            "Tech", "Systems", "Logistics", "Analytics", "Solutions",
            "Labs", "Consulting", "Networks", "Software", "Group",
            "Digital", "Cloud", "Ventures", "Industries", "Apps",
        ]

        app_names = [
            "Jira", "Confluence", "Jira Service Management",
            "Bitbucket", "Trello"
        ]

        license_tiers = ["standard", "premium", "free"]

        created = 0

        for _ in range(50):
            company_name = f"{choice(company_prefixes)} {choice(company_suffixes)} {randint(10, 999)}"

            Customer.objects.create(
                company_name=company_name,
                country=choice(countries),
                company_size=randint(5, 5000),
                license_tier=choice(license_tiers),
                app_name=choice(app_names),
                installed_at=date.today() - timedelta(days=randint(1, 365)),
            )

            created += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {created} customers.")
        )
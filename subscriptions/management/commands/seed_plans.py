from django.core.management.base import BaseCommand
from subscriptions.models import SubscriptionPlan

class Command(BaseCommand):
    help = 'Seeds initial subscription plans for BU-MARKET'

    def handle(self, *args, **options):
        plans_data = [
            {
                'name': SubscriptionPlan.PlanType.BASIC,
                'monthly_fee': 0.00,
                'max_active_listings': 2,
                'badge': SubscriptionPlan.BadgeType.NONE,
                'has_promoted_ads': False,
            },
            {
                'name': SubscriptionPlan.PlanType.SILVER,
                'monthly_fee': 10000.00,
                'max_active_listings': 10,
                'badge': SubscriptionPlan.BadgeType.SILVER,
                'has_promoted_ads': True,
            },
            {
                'name': SubscriptionPlan.PlanType.GOLD,
                'monthly_fee': 25000.00,
                'max_active_listings': 50,
                'badge': SubscriptionPlan.BadgeType.GOLD,
                'has_promoted_ads': True,
            },
        ]

        for plan_info in plans_data:
            plan, created = SubscriptionPlan.objects.get_or_create(
                name=plan_info['name'],
                defaults=plan_info
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created plan: {plan.get_name_display()}"))
            else:
                self.stdout.write(self.style.WARNING(f"Plan already exists: {plan.get_name_display()}"))
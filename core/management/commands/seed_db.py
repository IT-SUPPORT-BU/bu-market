from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from subscriptions.models import SubscriptionPlan
from marketplace.models import Category

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds default categories, subscription plans, and an admin superuser.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # 1. Seed Subscription Plans
        plans = [
            {
                'name': SubscriptionPlan.PlanType.BASIC,
                'monthly_fee': 20000.00,
                'max_active_listings': 2,
                'badge': SubscriptionPlan.BadgeType.NONE,
                'has_promoted_ads': False,
            },
            {
                'name': SubscriptionPlan.PlanType.SILVER,
                'monthly_fee': 30000.00,
                'max_active_listings': 5,
                'badge': SubscriptionPlan.BadgeType.SILVER,
                'has_promoted_ads': True,
            },
            {
                'name': SubscriptionPlan.PlanType.GOLD,
                'monthly_fee': 50000.00,
                'max_active_listings': 10,
                'badge': SubscriptionPlan.BadgeType.GOLD,
                'has_promoted_ads': True,
            },
        ]

        for plan_data in plans:
            plan, created = SubscriptionPlan.objects.update_or_create(
                name=plan_data['name'],
                defaults={
                    'monthly_fee': plan_data['monthly_fee'],
                    'max_active_listings': plan_data['max_active_listings'],
                    'badge': plan_data['badge'],
                    'has_promoted_ads': plan_data['has_promoted_ads'],
                }
            )
            if created:
                self.stdout.write(f'Created plan: {plan.name}')
            else:
                self.stdout.write(f'Updated plan: {plan.name}')

        # 2. Seed Categories
        categories = [
            ('Electronics', 'bi-laptop'),
            ('Phones', 'bi-phone'),
            ('Clothing', 'bi-gender-ambiguous'),
            ('Kitchen', 'bi-cup-hot'),
            ('Furniture', 'bi-door-closed'),
            ('Books', 'bi-book'),
            ('Hostel Items', 'bi-house-door'),
            ('Services', 'bi-tools'),
            ('Jobs', 'bi-briefcase'),
            ('Vehicles', 'bi-car-front'),
            ('Others', 'bi-grid'),
        ]

        for cat_name, cat_icon in categories:
            cat, created = Category.objects.update_or_create(
                name=cat_name,
                defaults={
                    'slug': slugify(cat_name),
                    'icon': cat_icon,
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(f'Created category: {cat.name}')
            else:
                self.stdout.write(f'Updated category: {cat.name}')

        # 3. Seed Admin Superuser
        admin_username = 'admin'
        admin_email = 'admin@bumarket.com'
        admin_password = 'admin123'

        if not User.objects.filter(username=admin_username).exists():
            admin_user = User.objects.create_superuser(
                username=admin_username,
                email=admin_email,
                password=admin_password,
                role=User.Role.ADMIN
            )
            self.stdout.write(self.style.SUCCESS(f'Superuser "{admin_username}" created with role {admin_user.role}.'))
        else:
            admin_user = User.objects.get(username=admin_username)
            admin_user.role = User.Role.ADMIN
            admin_user.is_superuser = True
            admin_user.is_staff = True
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f'Superuser "{admin_username}" verified and role set to ADMIN.'))

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))

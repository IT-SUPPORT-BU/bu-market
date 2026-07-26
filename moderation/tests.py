from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from marketplace.models import Category, Listing
from subscriptions.models import SubscriptionPlan, SellerSubscription
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class ListingModerationTestCase(TestCase):
    def setUp(self):
        self.password = 'password123'

        # Create Users
        self.seller = User.objects.create_user(username='seller', password=self.password, role=User.Role.SELLER)
        self.moderator = User.objects.create_user(username='moderator', password=self.password, role=User.Role.MODERATOR)
        self.buyer = User.objects.create_user(username='buyer', password=self.password, role=User.Role.BUYER)

        # Create Category
        self.category = Category.objects.create(name='Electronics', icon='bi-laptop')

        # Create active SellerSubscription (so Listing validation clean() passes)
        self.plan = SubscriptionPlan.objects.create(
            name=SubscriptionPlan.PlanType.BASIC,
            monthly_fee=20000.00,
            max_active_listings=2,
            badge=SubscriptionPlan.BadgeType.NONE,
            has_promoted_ads=False
        )
        self.sub = SellerSubscription.objects.create(
            seller=self.seller,
            plan=self.plan,
            amount_paid=20000.00,
            payment_reference="REF123456",
            status=SellerSubscription.Status.APPROVED,
            expires_at=timezone.now() + timedelta(days=30)
        )

        # Create listing (defaults to PENDING status)
        self.listing = Listing.objects.create(
            seller=self.seller,
            category=self.category,
            title='Test Laptop',
            price=150000.00,
            image='laptop.jpg'
        )

    def test_listing_starts_as_pending(self):
        self.assertEqual(self.listing.status, Listing.Status.PENDING)

    def test_moderator_approval_flow(self):
        approve_url = reverse('moderation:approve_listing', kwargs={'pk': self.listing.pk})
        reject_url = reverse('moderation:reject_listing', kwargs={'pk': self.listing.pk})

        # 1. Non-moderator cannot approve
        self.client.login(username='buyer', password=self.password)
        response = self.client.post(approve_url)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        # 2. Moderator rejects listing
        self.client.login(username='moderator', password=self.password)
        response = self.client.post(reject_url)
        self.assertEqual(response.status_code, 302) # Redirect to moderator dashboard
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.status, Listing.Status.REJECTED)
        self.client.logout()

        # Reset to pending for approval test
        self.listing.status = Listing.Status.PENDING
        self.listing.save()

        # 3. Moderator approves listing
        self.client.login(username='moderator', password=self.password)
        response = self.client.post(approve_url)
        self.assertEqual(response.status_code, 302)
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.status, Listing.Status.ACTIVE)
        self.client.logout()

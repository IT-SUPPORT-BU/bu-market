from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import SubscriptionPlan, SellerSubscription, BuyerMembership

User = get_user_model()

class SubscriptionApprovalTestCase(TestCase):
    def setUp(self):
        self.password = 'password123'
        
        # Create users
        self.seller = User.objects.create_user(username='seller', password=self.password, role=User.Role.SELLER)
        self.buyer = User.objects.create_user(username='buyer', password=self.password, role=User.Role.BUYER)
        self.accountant = User.objects.create_user(username='accountant', password=self.password, role=User.Role.ACCOUNTANT)
        self.other_user = User.objects.create_user(username='other', password=self.password, role=User.Role.BUYER)

        # Create subscription plan
        self.plan = SubscriptionPlan.objects.create(
            name=SubscriptionPlan.PlanType.BASIC,
            monthly_fee=20000.00,
            max_active_listings=2,
            badge=SubscriptionPlan.BadgeType.NONE,
            has_promoted_ads=False
        )

    def test_seller_subscription_approval_flow(self):
        # 1. Create a pending SellerSubscription
        sub = SellerSubscription.objects.create(
            seller=self.seller,
            plan=self.plan,
            amount_paid=20000.00,
            payment_reference="REF12345",
            receipt_image="test_receipt.jpg", # Mock path
            status=SellerSubscription.Status.PENDING
        )

        approve_url = reverse('subscriptions:approve_seller', kwargs={'pk': sub.pk})
        reject_url = reverse('subscriptions:reject_seller', kwargs={'pk': sub.pk})

        # 2. Non-accountant is denied approval access
        self.client.login(username='seller', password=self.password)
        response = self.client.post(approve_url)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        # 3. Accountant rejects subscription
        self.client.login(username='accountant', password=self.password)
        response = self.client.post(reject_url)
        self.assertEqual(response.status_code, 302) # Redirect to accountant dashboard
        sub.refresh_from_db()
        self.assertEqual(sub.status, SellerSubscription.Status.REJECTED)
        self.assertEqual(sub.approved_by, self.accountant)
        self.client.logout()

        # Reset status to pending for testing approval
        sub.status = SellerSubscription.Status.PENDING
        sub.save()

        # 4. Accountant approves subscription
        self.client.login(username='accountant', password=self.password)
        response = self.client.post(approve_url)
        self.assertEqual(response.status_code, 302)
        sub.refresh_from_db()
        self.assertEqual(sub.status, SellerSubscription.Status.APPROVED)
        self.assertEqual(sub.approved_by, self.accountant)
        self.assertIsNotNone(sub.approved_at)
        self.assertIsNotNone(sub.expires_at)
        # Expiration should be roughly 30 days from now
        self.assertTrue(sub.expires_at > timezone.now() + timedelta(days=29))
        self.client.logout()

    def test_buyer_membership_approval_flow(self):
        # 1. Create a pending BuyerMembership
        mem = BuyerMembership.objects.create(
            buyer=self.buyer,
            amount_paid=20000.00,
            receipt_image="test_receipt.jpg", # Mock path
            status=BuyerMembership.Status.PENDING
        )

        approve_url = reverse('subscriptions:approve_buyer', kwargs={'pk': mem.pk})
        reject_url = reverse('subscriptions:reject_buyer', kwargs={'pk': mem.pk})

        # 2. Non-accountant is denied approval access
        self.client.login(username='buyer', password=self.password)
        response = self.client.post(approve_url)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        # 3. Accountant rejects membership
        self.client.login(username='accountant', password=self.password)
        response = self.client.post(reject_url)
        self.assertEqual(response.status_code, 302) # Redirect to accountant dashboard
        mem.refresh_from_db()
        self.assertEqual(mem.status, BuyerMembership.Status.EXPIRED)
        self.assertEqual(mem.approved_by, self.accountant)
        self.client.logout()

        # Reset status to pending for testing approval
        mem.status = BuyerMembership.Status.PENDING
        mem.save()

        # 4. Accountant approves membership
        self.client.login(username='accountant', password=self.password)
        response = self.client.post(approve_url)
        self.assertEqual(response.status_code, 302)
        mem.refresh_from_db()
        self.assertEqual(mem.status, BuyerMembership.Status.ACTIVE)
        self.assertEqual(mem.approved_by, self.accountant)
        self.assertIsNotNone(mem.approved_at)
        self.client.logout()

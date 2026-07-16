from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from .models import Category, Listing
from subscriptions.models import SubscriptionPlan, SellerSubscription

User = get_user_model()

class ListingLimitsTestCase(TestCase):
    def setUp(self):
        # 1. Setup default subscription plans
        self.basic_plan, _ = SubscriptionPlan.objects.get_or_create(
            name=SubscriptionPlan.PlanType.BASIC,
            defaults={
                'monthly_fee': 20000.00,
                'max_active_listings': 2,
                'badge': SubscriptionPlan.BadgeType.NONE,
                'has_promoted_ads': False
            }
        )
        self.silver_plan, _ = SubscriptionPlan.objects.get_or_create(
            name=SubscriptionPlan.PlanType.SILVER,
            defaults={
                'monthly_fee': 30000.00,
                'max_active_listings': 5,
                'badge': SubscriptionPlan.BadgeType.SILVER,
                'has_promoted_ads': True
            }
        )

        # 2. Setup Category
        self.category = Category.objects.create(name="Electronics", icon="bi-laptop")

        # 3. Create Users
        self.seller = User.objects.create_user(
            username='seller_test', 
            email='seller@test.com', 
            password='pass', 
            role=User.Role.SELLER
        )
        self.buyer = User.objects.create_user(
            username='buyer_test', 
            email='buyer@test.com', 
            password='pass', 
            role=User.Role.BUYER
        )

    def test_listing_requires_seller_role(self):
        # Attempt to create a listing under a buyer account.
        listing = Listing(
            seller=self.buyer,
            category=self.category,
            title="Cool Gadget",
            price=50000.00,
            image="test_image.jpg"
        )
        with self.assertRaises(ValidationError):
            listing.clean()

    def test_listing_requires_active_subscription(self):
        # Seller has no subscription yet
        listing = Listing(
            seller=self.seller,
            category=self.category,
            title="Laptop",
            price=800000.00,
            image="laptop.jpg"
        )
        with self.assertRaises(ValidationError):
            listing.clean()

    def test_basic_plan_listing_limits(self):
        # Assign basic plan to seller
        sub = SellerSubscription.objects.create(
            seller=self.seller,
            plan=self.basic_plan,
            amount_paid=20000.00,
            payment_reference="REF123",
            status=SellerSubscription.Status.APPROVED,
            expires_at=timezone.now() + timedelta(days=30)
        )

        # Create listing 1 (should succeed)
        l1 = Listing.objects.create(
            seller=self.seller,
            category=self.category,
            title="Item 1",
            price=100.00,
            status=Listing.Status.ACTIVE,
            image="item1.jpg"
        )
        l1.clean() # Verify clean passes

        # Create listing 2 (should succeed)
        l2 = Listing.objects.create(
            seller=self.seller,
            category=self.category,
            title="Item 2",
            price=200.00,
            status=Listing.Status.ACTIVE,
            image="item2.jpg"
        )
        l2.clean() # Verify clean passes

        # Create listing 3 (should fail validation because BASIC cap is 2)
        l3 = Listing(
            seller=self.seller,
            category=self.category,
            title="Item 3",
            price=300.00,
            status=Listing.Status.ACTIVE,
            image="item3.jpg"
        )
        with self.assertRaises(ValidationError):
            l3.clean()

    def test_promoted_ads_limits(self):
        # Assign basic plan to seller
        sub = SellerSubscription.objects.create(
            seller=self.seller,
            plan=self.basic_plan,
            amount_paid=20000.00,
            payment_reference="REF456",
            status=SellerSubscription.Status.APPROVED,
            expires_at=timezone.now() + timedelta(days=30)
        )

        # Attempt to create promoted ad under BASIC plan (should fail clean)
        listing = Listing(
            seller=self.seller,
            category=self.category,
            title="Promoted Item",
            price=50.00,
            is_promoted=True,
            image="promo.jpg"
        )
        with self.assertRaises(ValidationError):
            listing.clean()


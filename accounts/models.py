from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        BUYER = 'BUYER', 'Buyer'
        SELLER = 'SELLER', 'Seller'
        ACCOUNTANT = 'ACCOUNTANT', 'Accountant'
        MODERATOR = 'MODERATOR', 'Moderator'
        ADMIN = 'ADMIN', 'Admin'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.BUYER
    )

    @property
    def is_buyer(self):
        return self.role == self.Role.BUYER

    @property
    def is_seller(self):
        return self.role == self.Role.SELLER

    @property
    def is_accountant(self):
        return self.role == self.Role.ACCOUNTANT

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    @property
    def active_subscription(self):
        from subscriptions.models import SellerSubscription
        from django.utils import timezone
        return SellerSubscription.objects.filter(
            seller=self,
            status=SellerSubscription.Status.APPROVED,
            expires_at__gt=timezone.now()
        ).order_by('-approved_at').first()

    @property
    def has_active_subscription(self):
        return self.active_subscription is not None

    @property
    def max_allowed_active_listings(self):
        sub = self.active_subscription
        if sub:
            return sub.plan.max_active_listings
        return 0

    @property
    def is_verified_buyer(self):
        if self.is_superuser or self.role in [self.Role.ADMIN, self.Role.MODERATOR, self.Role.ACCOUNTANT]:
            return True
        try:
            return self.buyer_membership.status == 'ACTIVE'
        except AttributeError:
            return False

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"



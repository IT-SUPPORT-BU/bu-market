from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.conf import settings
from core.validators import validate_file_size

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    icon = models.CharField(max_length=50, help_text="Bootstrap icon class name, e.g. bi-phone")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Listing(models.Model):
    class Condition(models.TextChoices):
        NEW = 'NEW', 'New'
        USED = 'USED', 'Used'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending Moderation'
        ACTIVE = 'ACTIVE', 'Active'
        SOLD = 'SOLD', 'Sold'
        REJECTED = 'REJECTED', 'Rejected'

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='listings'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='listings'
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    condition = models.CharField(
        max_length=10,
        choices=Condition.choices,
        default=Condition.USED
    )
    location = models.CharField(max_length=100, default='Bugema University Main Campus')
    image = models.ImageField(
        upload_to='listings/',
        validators=[validate_file_size]
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING
    )
    is_promoted = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    phone_number = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        help_text="Phone number for calls (e.g. +256700000000)"
    )
    whatsapp_number = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        help_text="WhatsApp number (e.g. +256700000000)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def whatsapp_url(self):
        if not self.whatsapp_number:
            return None
        cleaned = "".join(c for c in self.whatsapp_number if c.isdigit())
        if cleaned.startswith('0'):
            cleaned = '256' + cleaned[1:]
        return f"https://wa.me/{cleaned}"

    @property
    def tel_url(self):
        if not self.phone_number:
            return None
        cleaned = "".join(c for c in self.phone_number if c.isdigit() or c == '+')
        return f"tel:{cleaned}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Listing.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def clean(self):
        # 1. Enforce seller role
        if not self.seller.is_seller:
            raise ValidationError("Only users with the SELLER role can post listings.")

        # 2. Enforce active subscription
        if not self.seller.has_active_subscription:
            raise ValidationError("You must have an active approved subscription to post listings.")

        # 3. Enforce active listing limits (Only when listing is ACTIVE or PENDING)
        if self.status in [self.Status.ACTIVE, self.Status.PENDING]:
            max_limit = self.seller.max_allowed_active_listings
            # Count other active/pending listings for this seller
            current_active_count = Listing.objects.filter(
                seller=self.seller,
                status__in=[self.Status.ACTIVE, self.Status.PENDING]
            ).exclude(id=self.id).count()

            if current_active_count >= max_limit:
                raise ValidationError(
                    f"Your current subscription plan limits you to {max_limit} active listings. "
                    f"You currently have {current_active_count} active/pending listings."
                )

        # 4. Enforce promoted flag (only SILVER and GOLD allowed)
        if self.is_promoted:
            sub = self.seller.active_subscription
            if sub and not sub.plan.has_promoted_ads:
                raise ValidationError("Only Silver and Gold subscription plans support promoted ads.")

    def __str__(self):
        return self.title


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
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Community(models.Model):
    class HubType(models.TextChoices):
        CAMPUS = 'CAMPUS', 'University / College Campus'
        TOWN = 'TOWN', 'Town / Suburb / Commercial Center'

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    hub_type = models.CharField(max_length=20, choices=HubType.choices, default=HubType.CAMPUS)
    region = models.CharField(max_length=50, default='Central Region')
    icon = models.CharField(max_length=50, default='bi-mortarboard-fill', help_text="Bootstrap icon class")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Communities"
        ordering = ['order', 'name']

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
        REMOVED = 'REMOVED', 'Removed by Admin'

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
    condition = models.CharField(max_length=10, choices=Condition.choices, default=Condition.NEW)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    sold_at = models.DateTimeField(null=True, blank=True)
    removal_reason = models.TextField(blank=True, null=True)
    # ... any other fields you already have (views_count, created_at, etc.)
    community = models.ForeignKey(
        Community,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='listings'
    )
    location = models.CharField(max_length=100, default='Bugema University Main Campus')
    image = models.ImageField(
        upload_to='listings/',
        validators=[validate_file_size]
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    removal_reason = models.TextField(blank=True, null=True)
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


    is_quick_sale = models.BooleanField(default=False)
    quick_sale_expires_at = models.DateTimeField(null=True, blank=True)

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


# this is the hostel thing for the database 

class Hostel(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending Moderation'
        ACTIVE = 'ACTIVE', 'Active'
        REJECTED = 'REJECTED', 'Rejected'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hostels'
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    community = models.ForeignKey(
        Community,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='hostels'
    )
    location = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Optional extra info about the hostel"
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    removal_reason = models.TextField(blank=True, null=True)
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

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Hostel.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def clean(self):
        if not self.owner.is_seller:
            raise ValidationError("Only users with the SELLER role can post hostels.")
        if not self.owner.has_active_subscription:
            raise ValidationError("You must have an active approved subscription to post a hostel.")

    def __str__(self):
        return self.name


class HostelImage(models.Model):
    hostel = models.ForeignKey(
        Hostel,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='hostels/',
        validators=[validate_file_size]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.hostel_id:
            existing_count = HostelImage.objects.filter(hostel=self.hostel).exclude(pk=self.pk).count()
            if existing_count >= 4:
                raise ValidationError("A hostel can have a maximum of 4 images.")

    def __str__(self):
        return f"Image for {self.hostel.name}"





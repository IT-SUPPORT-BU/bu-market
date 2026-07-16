from django.contrib import admin
from .models import SubscriptionPlan, SellerSubscription, BuyerMembership

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'monthly_fee', 'max_active_listings', 'badge', 'has_promoted_ads']
    list_filter = ['badge', 'has_promoted_ads']

@admin.register(SellerSubscription)
class SellerSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['seller', 'plan', 'amount_paid', 'status', 'submitted_at', 'expires_at']
    list_filter = ['status', 'plan']
    search_fields = ['seller__username', 'payment_reference']

@admin.register(BuyerMembership)
class BuyerMembershipAdmin(admin.ModelAdmin):
    list_display = ['buyer', 'fee', 'amount_paid', 'status', 'submitted_at']
    list_filter = ['status']
    search_fields = ['buyer__username']


from django.contrib import admin
from .models import Category, Listing

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'is_active']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'category', 'price', 'condition', 'status', 'is_promoted', 'views_count', 'created_at']
    list_filter = ['status', 'is_promoted', 'condition', 'category']
    search_fields = ['title', 'description', 'seller__username']
    prepopulated_fields = {'slug': ('title',)}


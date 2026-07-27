from django.urls import path
from .views import (
    dashboard_home,
    seller_dashboard,
    seller_listings,
    create_listing,
    edit_listing,
    accountant_dashboard,
    moderator_dashboard,
    admin_dashboard
)

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard_home, name='home'),
    path('seller/', seller_dashboard, name='seller_dashboard'),
    path('seller/listings/', seller_listings, name='seller_listings'),
    path('seller/listings/create/', create_listing, name='create_listing'),
    path('seller/listings/edit/<slug:slug>/', edit_listing, name='edit_listing'),
    path('accountant/', accountant_dashboard, name='accountant_dashboard'),
    path('moderator/', moderator_dashboard, name='moderator_dashboard'),
    path('admin/', admin_dashboard, name='admin_dashboard'),
]

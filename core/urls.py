from django.urls import path
from .views import HomeView, BrowseView, ListingDetailView, seller_profile

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('browse/', BrowseView.as_view(), name='browse'),
    path('listing/<slug:slug>/', ListingDetailView.as_view(), name='listing_detail'),
    path('seller/<str:username>/', seller_profile, name='seller_profile'),
]

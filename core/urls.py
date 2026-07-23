from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('browse/', views.BrowseView.as_view(), name='browse'),
    path('listing/<slug:slug>/', views.ListingDetailView.as_view(), name='listing_detail'),
    path('listing/<slug:slug>/mark-sold/', views.mark_as_sold, name='mark_as_sold'),
    path('seller/<str:username>/', views.seller_profile, name='seller_profile'),
]
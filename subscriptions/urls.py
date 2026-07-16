from django.urls import path
from .views import (
    apply_seller,
    apply_buyer,
    approve_seller_subscription,
    reject_seller_subscription,
    approve_buyer_membership,
    reject_buyer_membership
)

app_name = 'subscriptions'

urlpatterns = [
    path('apply/seller/', apply_seller, name='apply_seller'),
    path('apply/buyer/', apply_buyer, name='apply_buyer'),
    path('approve/seller/<int:pk>/', approve_seller_subscription, name='approve_seller'),
    path('reject/seller/<int:pk>/', reject_seller_subscription, name='reject_seller'),
    path('approve/buyer/<int:pk>/', approve_buyer_membership, name='approve_buyer'),
    path('reject/buyer/<int:pk>/', reject_buyer_membership, name='reject_buyer'),
]

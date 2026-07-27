from django.urls import path
from .views import (
    apply_seller,
    approve_seller_subscription,
    reject_seller_subscription,
)

app_name = 'subscriptions'

urlpatterns = [
    path('apply/seller/', apply_seller, name='apply_seller'),
    path('approve/seller/<int:pk>/', approve_seller_subscription, name='approve_seller'),
    path('reject/seller/<int:pk>/', reject_seller_subscription, name='reject_seller'),
]

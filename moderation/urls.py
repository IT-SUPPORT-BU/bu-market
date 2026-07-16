from django.urls import path
from .views import approve_listing, reject_listing

app_name = 'moderation'

urlpatterns = [
    path('approve/<int:pk>/', approve_listing, name='approve_listing'),
    path('reject/<int:pk>/', reject_listing, name='reject_listing'),
]

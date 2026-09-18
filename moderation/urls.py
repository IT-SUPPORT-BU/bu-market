from django.urls import path
from .views import approve_listing, reject_listing, approve_hostel, reject_hostel
app_name = 'moderation'

urlpatterns = [
    path('approve/<int:pk>/', approve_listing, name='approve_listing'),
    path('reject/<int:pk>/', reject_listing, name='reject_listing'),
    path('approve-hostel/<int:pk>/', approve_hostel, name='approve_hostel'),
    path('reject-hostel/<int:pk>/', reject_hostel, name='reject_hostel'),
]

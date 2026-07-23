from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('start/<int:listing_id>/', views.start_conversation, name='start_conversation'),
    path('<int:pk>/', views.conversation_detail, name='conversation_detail'),
    path('', views.inbox, name='inbox'),
]
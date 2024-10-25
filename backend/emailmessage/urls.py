from django.urls import path
from .views import create_email_message

urlpatterns = [
    path('email/', create_email_message, name='create_email_message'),
]

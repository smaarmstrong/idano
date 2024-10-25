from django.urls import path
from .views import create_email_message, get_email_message, delete_email_message

urlpatterns = [
    path("email/", create_email_message, name="create_email_message"),
    path("email/<int:id>/", get_email_message, name="email_detail"),  # For reading
    path(
        "email/<int:id>/delete/", delete_email_message, name="delete_email_message"
    ),  # For deleting
]

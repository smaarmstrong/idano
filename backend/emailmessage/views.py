from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import EmailMessage
from django.core.exceptions import ValidationError
import re

# Create your views here.


@api_view(["POST"])
def create_email_message(request):
    name = request.data.get("name")
    email = request.data.get("email")
    subject = request.data.get("subject")
    message = request.data.get("message")

    # Validate email format
    if not is_valid_email(email):
        return Response(
            {"error": "Invalid email format."}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        email_message = EmailMessage.objects.create(
            name=name, email=email, subject=subject, message=message
        )
        return Response(
            {"message": "Email message created successfully.", "id": email_message.id},
            status=status.HTTP_201_CREATED,
        )
    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def is_valid_email(email):
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(regex, email) is not None

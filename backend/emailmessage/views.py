from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import EmailMessage
from .serializer import EmailMessageSerializer
import re

# Create your views here.


@api_view(["POST"])
def create_email_message(request):
    serializer = EmailMessageSerializer(data=request.data)

    if serializer.is_valid():
        email_message = serializer.save()
        return Response(
            {"message": "Email message created successfully.", "id": email_message.id},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_email_message(request, id):
    try:
        email_message = EmailMessage.objects.get(id=id)
        serializer = EmailMessageSerializer(email_message)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except EmailMessage.DoesNotExist:
        return Response(
            {"error": "Email message not found."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["DELETE"])
def delete_email_message(request, id):
    try:
        email_message = EmailMessage.objects.get(id=id)
        email_message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except EmailMessage.DoesNotExist:
        return Response(
            {"error": "Email message not found."}, status=status.HTTP_404_NOT_FOUND
        )


def is_valid_email(email):
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(regex, email) is not None

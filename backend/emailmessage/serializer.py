from rest_framework import serializers
from .models import EmailMessage


class EmailMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailMessage
        fields = [
            "id",
            "name",
            "email",
            "subject",
            "message",
            "created_at",
            "responded",
        ]

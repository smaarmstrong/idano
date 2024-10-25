from django.test import TestCase
from emailmessage.models import EmailMessage
from datetime import datetime
from django.core.exceptions import ValidationError

class EmailMessageModelTest(TestCase):
    def setUp(self):
        # Create a test email message
        self.email_message = EmailMessage.objects.create(
            name="Sean Armstrong",
            email="sean@example.com",
            subject="Inquiry about the portfolio",
            message="Hi, I'm interested in your projects!",
        )

    def test_email_message_creation(self):
        """Test that the email message is created with all fields populated"""
        self.assertEqual(self.email_message.name, "Sean Armstrong")
        self.assertEqual(self.email_message.email, "sean@example.com")
        self.assertEqual(self.email_message.subject, "Inquiry about the portfolio")
        self.assertTrue(self.email_message.message.startswith("Hi, I'm interested"))

    def test_email_message_auto_timestamp(self):
        """Test that created_at is automatically set on creation"""
        self.assertIsNotNone(self.email_message.created_at)
        self.assertTrue(
            isinstance(self.email_message.created_at, datetime),
            "created_at should be a datetime instance",
        )

    def test_default_responded_value(self):
        """Test that the responded field defaults to False"""
        self.assertFalse(self.email_message.responded)

    def test_email_message_str_representation(self):
        """Test the string representation of the email message"""
        self.assertEqual(
            str(self.email_message),
            "Email from Sean Armstrong (sean@example.com) - Inquiry about the portfolio"
        )

    def test_invalid_email_format(self):
        """Test that invalid email format raises an error"""
        email_message = EmailMessage(
            name="Jane Doe",
            email="invalid-email",
            subject="Invalid email test",
            message="This email should raise an error due to invalid format.",
        )
        with self.assertRaises(ValidationError):
            email_message.full_clean()  # This will validate the fields before saving
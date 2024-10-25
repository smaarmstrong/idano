from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from emailmessage.models import EmailMessage
from django.contrib.auth.models import User

class EmailMessageControllerTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

    def test_create_email_message(self):
        response = self.client.post(
            reverse("create_email_message"),
            {
                "name": "Jane Doe",
                "email": "jane@example.com",
                "subject": "Test Subject",
                "message": "This is a test message.",
            },
        )
        self.assertEqual(response.status_code, 201)  # Created status
        self.assertTrue(EmailMessage.objects.filter(email="jane@example.com").exists())

    def test_create_email_message_invalid_email(self):
        response = self.client.post(
            reverse("create_email_message"),
            {
                "name": "Jane Doe",
                "email": "invalid-email",
                "subject": "Test Subject",
                "message": "This email should raise an error due to invalid format.",
            },
        )
        self.assertEqual(response.status_code, 400)  # Bad request status
        self.assertIn("error", response.data)

    def test_create_email_message_missing_fields(self):
        response = self.client.post(
            reverse("create_email_message"),
            {
                "name": "Jane Doe",
                "email": "jane@example.com",
                # Provide default values for subject and message
                "subject": "",  # or some default value
                "message": "",  # or some default value
            },
        )
        self.assertEqual(response.status_code, 400)  # Bad request status
        self.assertIn("error", response.data)

    def test_read_email_message(self):
        email_message = EmailMessage.objects.create(
            name="John Doe",
            email="john@example.com",
            subject="Hello",
            message="This is a test message."
        )
        response = self.client.get(reverse("email_detail", args=[email_message.id]))
        self.assertEqual(response.status_code, 200)  # OK status
        self.assertContains(response, "Hello")  # Check if the subject is in the response

    def test_delete_email_message(self):
        email_message = EmailMessage.objects.create(
            name="Jane Doe",
            email="jane@example.com",
            subject="Test Subject",
            message="This is a test message.",
        )
        response = self.client.delete(reverse("delete_email_message", args=[email_message.id]))
        self.assertEqual(response.status_code, 204)  # No Content status
        self.assertFalse(EmailMessage.objects.filter(id=email_message.id).exists())

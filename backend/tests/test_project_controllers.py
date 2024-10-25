from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from project.models import Project
from django.contrib.auth.models import User


class ProjectControllerTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

        self.project = Project.objects.create(
            title="Test Project",
            description="This is a test project.",
            company="Test Company",
            tech_stack="Python, Django",
            website="https://www.testproject.com",
        )

    def test_create_project(self):
        response = self.client.post(
            reverse("project-list"),
            {
                "title": "New Project",
                "description": "Description of the new project.",
                "company": "New Company",
                "tech_stack": "JavaScript",
                "website": "https://www.newproject.com",
            },
        )
        self.assertEqual(response.status_code, 201)  # Created status
        self.assertTrue(Project.objects.filter(title="New Project").exists())

    def test_read_project(self):
        response = self.client.get(reverse("project-detail", args=[self.project.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Project")

    def test_update_project(self):
        response = self.client.put(
            reverse("project-detail", args=[self.project.id]),
            {
                "title": "Updated Project",
                "description": "Updated description.",
                "company": "Updated Company",
                "tech_stack": "Updated Tech Stack",
                "website": "https://www.updatedproject.com",
            },
        )
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Updated Project")
        self.assertEqual(response.status_code, 200)  # OK status

    def test_delete_project(self):
        response = self.client.delete(reverse("project-detail", args=[self.project.id]))
        self.assertEqual(response.status_code, 204)  # No Content status
        self.assertFalse(Project.objects.filter(id=self.project.id).exists())

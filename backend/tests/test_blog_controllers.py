from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from blog.models import BlogPost
from django.contrib.auth.models import User
from datetime import date


class BlogPostControllerTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

        self.blog_post = BlogPost.objects.create(
            title="Test Blog Post",
            content="This is a test blog post.",
            date_published=date(2024, 10, 10),
            author=self.author,
            category="Test Category",
        )

    def test_create_blog_post(self):
        response = self.client.post(
            reverse("blogpost-list"),
            {
                "title": "New Blog Post",
                "content": "Content of the new blog post.",
                "date_published": "2024-10-11",
                "category": "New Category",
            },
        )
        self.assertEqual(response.status_code, 201)  # Created status
        self.assertTrue(BlogPost.objects.filter(title="New Blog Post").exists())

    def test_read_blog_post(self):
        response = self.client.get(reverse("blogpost-detail", args=[self.blog_post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Blog Post")

    def test_update_blog_post(self):
        response = self.client.put(
            reverse("blogpost-detail", args=[self.blog_post.id]),
            {
                "title": "Updated Blog Post",
                "content": "Updated content.",
                "date_published": "2024-10-12",
                "category": "Updated Category",
            },
        )
        self.blog_post.refresh_from_db()
        self.assertEqual(self.blog_post.title, "Updated Blog Post")
        self.assertEqual(response.status_code, 200)  # OK status

    def test_delete_blog_post(self):
        response = self.client.delete(
            reverse("blogpost-detail", args=[self.blog_post.id])
        )
        self.assertEqual(response.status_code, 204)  # No Content status
        self.assertFalse(BlogPost.objects.filter(id=self.blog_post.id).exists())

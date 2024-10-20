from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from blog.models import BlogPost
from project.models import Project
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
        response = self.client.post(reverse('blogpost-list'), {
            'title': 'New Blog Post',
            'content': 'Content of the new blog post.',
            'date_published': '2024-10-11',
            'category': 'New Category',
        })
        self.assertEqual(response.status_code, 201)  # Created status
        self.assertTrue(BlogPost.objects.filter(title='New Blog Post').exists())

    def test_read_blog_post(self):
        response = self.client.get(reverse('blogpost-detail', args=[self.blog_post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Blog Post")

    def test_update_blog_post(self):
        response = self.client.put(reverse('blogpost-detail', args=[self.blog_post.id]), {
            'title': 'Updated Blog Post',
            'content': 'Updated content.',
            'date_published': '2024-10-12',
            'category': 'Updated Category',
        })
        self.blog_post.refresh_from_db()
        self.assertEqual(self.blog_post.title, 'Updated Blog Post')
        self.assertEqual(response.status_code, 200)  # OK status

    def test_delete_blog_post(self):
        response = self.client.delete(reverse('blogpost-detail', args=[self.blog_post.id]))
        self.assertEqual(response.status_code, 204)  # No Content status
        self.assertFalse(BlogPost.objects.filter(id=self.blog_post.id).exists())


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
        response = self.client.post(reverse('project-list'), {
            'title': 'New Project',
            'description': 'Description of the new project.',
            'company': 'New Company',
            'tech_stack': 'JavaScript',
            'website': 'https://www.newproject.com',
        })
        self.assertEqual(response.status_code, 201)  # Created status
        self.assertTrue(Project.objects.filter(title='New Project').exists())

    def test_read_project(self):
        response = self.client.get(reverse('project-detail', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Project")

    def test_update_project(self):
        response = self.client.put(reverse('project-detail', args=[self.project.id]), {
            'title': 'Updated Project',
            'description': 'Updated description.',
            'company': 'Updated Company',
            'tech_stack': 'Updated Tech Stack',
            'website': 'https://www.updatedproject.com',
        })
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, 'Updated Project')
        self.assertEqual(response.status_code, 200)  # OK status

    def test_delete_project(self):
        response = self.client.delete(reverse('project-detail', args=[self.project.id]))
        self.assertEqual(response.status_code, 204)  # No Content status
        self.assertFalse(Project.objects.filter(id=self.project.id).exists())

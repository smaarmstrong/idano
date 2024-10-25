from django.test import TestCase
from blog.models import BlogPost
from django.contrib.auth.models import User
from datetime import date


class BlogPostModelTest(TestCase):
    def setUp(self):
        # Create a test user (author)
        self.author = User.objects.create_user(
            username="seanarmstrong", password="password123"
        )

        # Create a test blog post
        self.blog_post = BlogPost.objects.create(
            title="Mark Twain's Commentary on Society",
            content="""All right, then, I'll go to hell! — The Adventures of Huckleberry Finn, where Huck wrestles with his conscience about helping Jim.""",
            date_published=date(2024, 10, 10),
            author=self.author,
            category="Literature",
        )

    def test_blog_post_creation_with_all_fields(self):
        """Test that the blog post is created with the correct fields"""
        self.assertEqual(self.blog_post.title, "Mark Twain's Commentary on Society")
        self.assertTrue(
            self.blog_post.content.startswith("All right, then, I'll go to hell")
        )
        self.assertEqual(self.blog_post.date_published, date(2024, 10, 10))
        self.assertEqual(self.blog_post.author.username, "seanarmstrong")
        self.assertEqual(self.blog_post.category, "Literature")

    def test_blog_post_creation_without_category(self):
        """Test blog post creation without a category (if it’s optional)"""
        post = BlogPost.objects.create(
            title="Mark Twain and the Mississippi River",
            content="It was the river that controlled all — The Adventures of Tom Sawyer.",
            date_published=date(2024, 10, 15),
            author=self.author,
        )
        self.assertEqual(post.title, "Mark Twain and the Mississippi River")
        self.assertEqual(
            post.content,
            "It was the river that controlled all — The Adventures of Tom Sawyer.",
        )
        self.assertEqual(post.author.username, "seanarmstrong")
        self.assertIsNone(
            post.category
        )  # Assuming category is optional and allows null values

    def test_author_relationship(self):
        """Test that the author is correctly linked to the blog post"""
        self.assertEqual(self.blog_post.author, self.author)

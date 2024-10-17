from django.test import TestCase
from project.models import Project, Screenshot, TechStack
from blog.models import BlogPost
from django.contrib.auth.models import User
from datetime import date


class ProjectModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Portfolio",
            description="Create your own project/blog portfolio.",
            price="Free",
            company="Idano",
            tech_stack="JavaScript, Python",
            website="https://www.idano.xyz",
        )

    def test_project_creation_with_optional_fields(self):
        self.assertEqual(self.project.title, "Portfolio")
        self.assertEqual(self.project.company, "Idano")
        self.assertEqual(self.project.tech_stack, "JavaScript, Python")
        self.assertEqual(self.project.website, "https://www.idano.xyz")

    def test_project_creation_without_optional_fields(self):
        project = Project.objects.create(
            title="Simple Project", description="A project without optional fields."
        )
        self.assertEqual(project.title, "Simple Project")
        self.assertIsNone(project.company)
        self.assertIsNone(project.tech_stack)
        self.assertIsNone(project.website)


class ScreenshotModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Portfolio", description="Create your own project/blog portfolio."
        )

    def test_screenshot_creation(self):
        screenshot = Screenshot.objects.create(
            project=self.project, image="screenshots/test_screenshot.png"
        )
        self.assertEqual(screenshot.project.title, "Portfolio")
        self.assertEqual(screenshot.image, "screenshots/test_screenshot.png")

    def test_multiple_screenshots(self):
        Screenshot.objects.create(
            project=self.project, image="screenshots/test_screenshot1.png"
        )
        Screenshot.objects.create(
            project=self.project, image="screenshots/test_screenshot2.png"
        )
        screenshots = self.project.screenshot_set.all()
        self.assertEqual(screenshots.count(), 2)
        self.assertEqual(screenshots[0].image, "screenshots/test_screenshot1.png")
        self.assertEqual(screenshots[1].image, "screenshots/test_screenshot2.png")


class TechStackModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Portfolio", description="Create your own project/blog portfolio."
        )

    def test_tech_stack_creation(self):
        tech_stack = TechStack.objects.create(
            project=self.project,
            name="JavaScript",
            logo="tech_stack/javascript_logo.png",
        )
        self.assertEqual(tech_stack.project.title, "Portfolio")
        self.assertEqual(tech_stack.name, "JavaScript")
        self.assertEqual(tech_stack.logo, "tech_stack/javascript_logo.png")

    def test_multiple_tech_stack_entries(self):
        TechStack.objects.create(
            project=self.project,
            name="JavaScript",
            logo="tech_stack/javascript_logo.png",
        )
        TechStack.objects.create(
            project=self.project, name="Python", logo="tech_stack/python_logo.png"
        )
        tech_stacks = self.project.techstack_set.all()
        self.assertEqual(tech_stacks.count(), 2)
        self.assertEqual(tech_stacks[0].name, "JavaScript")
        self.assertEqual(tech_stacks[1].name, "Python")


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

from django.test import TestCase
from project.models import Project, Screenshot, TechStack


class ProjectModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Portfolio",
            description="Create your own project/blog idano.",
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
            title="Portfolio", description="Create your own project/blog idano."
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
            title="Portfolio", description="Create your own project/blog idano."
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

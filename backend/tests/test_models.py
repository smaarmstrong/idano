from django.test import TestCase
from project.models import Project, Screenshot, TechStack


class ProjectModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="CrateNFC",
            description="Create musical NFC cards.",
            price="Free",
            company="Lil Robo",
            tech_stack="Swift, Python",
            website="https://www.cratenfc.com",
        )

    def test_project_creation_with_optional_fields(self):
        self.assertEqual(self.project.title, "CrateNFC")
        self.assertEqual(self.project.company, "Lil Robo")
        self.assertEqual(self.project.tech_stack, "Swift, Python")
        self.assertEqual(self.project.website, "https://www.cratenfc.com")

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
            title="CrateNFC", description="Create musical NFC cards."
        )

    def test_screenshot_creation(self):
        screenshot = Screenshot.objects.create(
            project=self.project, image="screenshots/test_screenshot.png"
        )
        self.assertEqual(screenshot.project.title, "CrateNFC")
        self.assertEqual(screenshot.image, "screenshots/test_screenshot.png")

    def test_multiple_screenshots(self):
        screenshot1 = Screenshot.objects.create(
            project=self.project, image="screenshots/test_screenshot1.png"
        )
        screenshot2 = Screenshot.objects.create(
            project=self.project, image="screenshots/test_screenshot2.png"
        )
        screenshots = self.project.screenshot_set.all()
        self.assertEqual(screenshots.count(), 2)
        self.assertEqual(screenshots[0].image, "screenshots/test_screenshot1.png")
        self.assertEqual(screenshots[1].image, "screenshots/test_screenshot2.png")


class TechStackModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="CrateNFC", description="Create musical NFC cards."
        )

    def test_tech_stack_creation(self):
        tech_stack = TechStack.objects.create(
            project=self.project, name="Swift", logo="tech_stack/swift_logo.png"
        )
        self.assertEqual(tech_stack.project.title, "CrateNFC")
        self.assertEqual(tech_stack.name, "Swift")
        self.assertEqual(tech_stack.logo, "tech_stack/swift_logo.png")

    def test_multiple_tech_stack_entries(self):
        tech_stack1 = TechStack.objects.create(
            project=self.project, name="Swift", logo="tech_stack/swift_logo.png"
        )
        tech_stack2 = TechStack.objects.create(
            project=self.project, name="Python", logo="tech_stack/python_logo.png"
        )
        tech_stacks = self.project.techstack_set.all()
        self.assertEqual(tech_stacks.count(), 2)
        self.assertEqual(tech_stacks[0].name, "Swift")
        self.assertEqual(tech_stacks[1].name, "Python")

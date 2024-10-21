from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.CharField(
        max_length=255, blank=True, null=True
    )  # Optional company field
    tech_stack = models.TextField(blank=True, null=True)  # Optional tech stack field
    website = models.URLField(
        blank=True, null=True
    )  # Optional link field for external website

    def __str__(self):
        return self.title


class Screenshot(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="screenshots/")

    def __str__(self):
        return f"Screenshot for {self.project.title}"


class TechStack(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="tech_stack/", blank=True, null=True)

    def __str__(self):
        return f"{self.name} for {self.project.title}"

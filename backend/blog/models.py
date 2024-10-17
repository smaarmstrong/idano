# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_published = models.DateField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.title

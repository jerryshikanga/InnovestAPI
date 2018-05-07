from django.db import models
from django.utils import  timezone


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    picture = models.ImageField()
    date = models.DateTimeField(default=timezone.now)
    summary = models.CharField(max_length=100)

    def __str__(self):
        return self.name


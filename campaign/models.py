from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from category.models import Category


# Create your models here.
class Campaign(models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    summary = models.CharField(max_length=100)
    description = models.TextField()
    amount = models.IntegerField()
    picture = models.ImageField(upload_to='campaign', default='default.jpg')
    start = models.DateTimeField(default=timezone.now)
    end = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='campaigns')

    def __str__(self):
        return self.name
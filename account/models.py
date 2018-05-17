from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from category.models import Category
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='account',)
    picture = models.ImageField(upload_to='account', default="account/default_profile.jpg")
    interests = models.ManyToManyField(Category)
    balance = models.IntegerField(default=0)
    telephone = models.BigIntegerField(default=0)

    def __str__(self):
        return self.user.username

    def deposit(self, amount):
        self.balance += amount
        self.save()
        return True

    def withdraw(self, amount):
        if self.balance >= amount :
            self.balance -= amount
            self.save()
            return True
        return False

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_account(sender, instance=None, created=False, **kwargs):
    if created :
        account = Account.objects.create(user=instance)
        account.save()

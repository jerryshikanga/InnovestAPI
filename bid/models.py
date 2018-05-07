from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from campaign.models import Campaign
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    amount = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='bids')

    def __str__(self):
        return str(self.amount)

    class Meta :
        ordering = ['date', 'amount']


@receiver(post_save, sender=Bid)
def charge_user_for_bid(sender, instance=None, created=False, **kwargs):
    if created:
        account = instance.user.account
        account.balance -= instance.amount
        account.save()

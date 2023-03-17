from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass


class Listings(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    list_value = models.DecimalField(max_digits=11, decimal_places=2)
    description = models.TextField(max_length=1000)
    item_image = models.URLField(max_length=250, default=None, null=True, blank=True)
    category = models.CharField(max_length=20, default=None, null=True,blank=True)
    status = models.BooleanField(default=True)
    current_value = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.item_name} for £{self.list_value}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.current_value = self.list_value
        super(Listings, self).save(*args, **kwargs)

class Bids(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bid_value = models.DecimalField(max_digits=11, decimal_places=2)
    
class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    watched_item = models.ForeignKey('Listings', on_delete=models.CASCADE)


class Comments(models.Model):
    pass
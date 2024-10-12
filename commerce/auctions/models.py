from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

""" TODO:
Create a Model for auctions, bids and comments
Watchlists"""

class Auction(models.Model):
    owner = models.ForeignKey(User, related_name="owned_auctions", on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=512)
    starting_bit = models.FloatField()
    img_link = models.CharField(blank=True, max_length=256)
    # wishlisted_by = models.ManyToManyField(User, default=None)

    ended = models.BooleanField(default=False)
    won_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions_won", default=None, null=True)


    def __str__(self):
        return f"{self.title}: {self.description} Starting bit is {self.starting_bit} - {"has image" if self.img_link else "no image"}"
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, related_name="wishlist", on_delete=models.CASCADE)
    auctions = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="wishlisted_by")

class Bid(models.Model):
    pass

class Comment(models.Model):
    pass
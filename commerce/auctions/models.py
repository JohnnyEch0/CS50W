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
    bit = models.DecimalField(max_digits=6, decimal_places=2, default=1)
    img_link = models.CharField(blank=True, max_length=256, null=True)
    # wishlisted_by = models.ManyToManyField(User, default=None)

    ended = models.BooleanField(default=False)
    won_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions_won", default=None, blank=True, null=True)
    


    def __str__(self):
        return f"{self.title}: {self.description} hightest bit is {self.bit} - {"has image" if self.img_link else "no image"}"
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, related_name="wishlist", on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="wishlisted_by")

    def __str__(self):
        return f"{self.auction.title} wishlisted by {self.user}"

class Bid(models.Model):
    pass

class Comment(models.Model):
    pass
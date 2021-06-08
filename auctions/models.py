from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    pass

class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    highest_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name="my_listings", null=True  )
    created_date = models.DateTimeField(auto_now_add=True)
    current_winner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="my_leadings", null=True)
    winner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="my_winnings", null=True)
    image = models.URLField(max_length=100000)
    category = models.CharField(max_length=64, null=True)
    watchlist = models.ManyToManyField(User, related_name="my_watchlist", blank=True)
    ## when user clicks on watchlist button, adds a user to the auction.watchlist 



class Bid(models.Model):
    listing = models.ForeignKey(Auction, on_delete=models.CASCADE, null=True)
    bid = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE , null=True)



class Comments(models.Model):
    listing = models.ForeignKey(Auction, on_delete=models.CASCADE, null=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE )

class Categories(models.Model):
    category = models.CharField(max_length=64)
    listing = models.ForeignKey(Auction, on_delete=models.CASCADE, null=True)
# Model for auction listings, bids and comments made on auction listingsa
#No point of repeating, forgein key is just to link two models together. 
from django.contrib import admin
from .models import Auction, Bid, Comments, Categories
# Register your models here.
class AuctionAdmin(admin.ModelAdmin):
    filter_horizontal = ("watchlist",)
    
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid)
admin.site.register(Comments)
admin.site.register(Categories)
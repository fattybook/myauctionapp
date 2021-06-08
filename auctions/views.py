from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auction, Bid, Comments


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["bid"]
        image = request.POST["image"]
        category = request.POST["category"]
        creator = User.objects.get(id = request.user.id)
        try:
            listing = Auction.objects.create(title = title, description = description, starting_bid = bid, highest_bid = bid, image=image, category=category, creator = creator)
            
        except IntegrityError:
            return render(request, "auctions/create_listing.html", {
                "message": "Title already taken"
            })
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_listing.html")

def listing(request, listing_id):
    listing = Auction.objects.get(id = listing_id)
    user = User.objects.get(id = request.user.id)
    comments = Comments.objects.all()
    if request.method == "POST":
        current_bid = request.POST["bid"]
        if int(current_bid) > int(listing.highest_bid):
            print('valid bid')
            bid = Bid.objects.create(listing = listing, bid= current_bid, user = user)
            listing.highest_bid = bid.bid
            listing.current_winner = bid.user
            listing.save()
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "user": user,
                "comments": comments
            })
        else:
            print('invalid bid')
            return render(request, "auctions/listing.html", {
                "listing": listing, 
                "error": "Bid must be more than the current bid",
                "user": user,
                "comments": comments
            })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "user": user,
            "comments": comments
        })

def add_to_watchlist(request, listing_id):
    listing = Auction.objects.get(id=listing_id)
    user = User.objects.get(id = request.user.id)
    comments = Comments.objects.all()
    if user in listing.watchlist.all():
        listing.watchlist.remove(user)
        listing.save()
    else:
        listing.watchlist.add(user)
        listing.save()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "user": user,
        "comments": comments
    })

def close_listing(request, listing_id):
    listing = Auction.objects.get(id=listing_id)
    listing.winner = listing.current_winner
    listing.save()
    return HttpResponseRedirect(reverse("index"))

def my_winnings(request):
    user = User.objects.get(id = request.user.id)
    listings = Auction.objects.filter(winner = user)
    return render(request, "auctions/my_winnings.html", {
        "listings": listings
    })

def add_comment(request, listing_id):
    listing = Auction.objects.get(id=listing_id)
    user = User.objects.get(id=request.user.id)
    all_comments = Comments.objects.all()
    if request.method == "POST":
        new_comment = request.POST["comment"]
        comment = Comments.objects.create(listing=listing, comment=new_comment, user=user)
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "user": user,
            "comments": all_comments,            
        })
    else:
        return render(request, "auctions/listing.html", {
        "listing": listing,
        "user": user,
        "comments": all_comments
    })
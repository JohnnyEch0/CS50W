from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from auctions.forms import *

import auctions.helpers
from .models import *


def index(request):

    return render(request, "auctions/index.html", {"auctions": Auction.objects.filter(ended=False).all})


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

def error(request, message):
    return render(request, "auctions/error.html", {'message': message})

@login_required
def create_auction(request):
    if request.method == "POST":
        form = AuctionCreationForm(request.POST)
        
        if form.is_valid():
            print(form.cleaned_data)
            model_proto = form.instance
            model_proto.owner = request.user
            img_path = auctions.helpers.download_image(model_proto.img_link)
            
            if not img_path:
                model_proto.img_link = None
            else:
                model_proto.img_link = img_path
            
            try:
                model_proto.save()
                return HttpResponseRedirect(reverse("index"))
            except Exception as e:
                print(e)
                return HttpResponseRedirect(reverse("error", kwargs={"message": "Something didn't quite work out"}))
        
        else:
            form.error_class=DivErrorList
            return render(request, "auctions/create_auction.html", {'form': form})


            
    else:
        form = AuctionCreationForm()
        return render(request, "auctions/create_auction.html", {'form': form})
    
def listing(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    if not request.user.is_authenticated:
        is_wishlisted = False
    else:
        is_wishlisted = Wishlist.objects.filter(user=request.user, auction=auction).exists()
    

    return render(request, "auctions/listing.html", {"auction": auction, "is_wishlisted": is_wishlisted})

def place_bid(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    return HttpResponseRedirect(reverse("error", args=["bid placing coming soon"]))

@login_required
def add_to_wishlist(request, auction_id):
    try:
        auction = Auction.objects.get(pk=auction_id)
        if Wishlist.objects.filter(user=request.user, auction=auction).exists():
            return HttpResponseRedirect(reverse("error", kwargs={"message": "auction already on wishlist"}))
        
        wishlisted = Wishlist(user=request.user, auction=auction)
        wishlisted.save()
        return HttpResponseRedirect(reverse("listing", args=[auction_id]))
    
    except Exception as e:
        print(e)
        return HttpResponseRedirect(reverse("error", kwargs={"message": "Something didn't quite work out"}))

def remove_from_wishlist(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    db_check = Wishlist.objects.filter(user=request.user, auction=auction)
    if db_check.exists():
        db_check.delete()
        return HttpResponseRedirect(reverse("listing", args=[auction_id]))

    
    return HttpResponseRedirect(reverse("error", kwargs={"message": "Something didn't quite work out"}))
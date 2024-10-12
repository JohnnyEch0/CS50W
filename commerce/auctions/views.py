from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from auctions.forms import *

import auctions.helpers
from .models import User, Auction


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
    return render(request, "auctions/error.html", {"message": message})

@login_required
def create_auction(request):
    if request.method == "POST":
        form = AuctionCreationForm(request.POST)
        
        if form.is_valid():
            print(form.cleaned_data)
            model_proto = form.instance
            model_proto.owner = request.user
            img_internal_link = auctions.helpers.download_image(model_proto.img_link)
            
            if not img_internal_link:
                model_proto.img_link = None
            
            try:
                model_proto.save()
            except Exception as e:
                print(e)
                return HttpResponseRedirect(reverse("error"), message="We couldn't save the auction!")


            return HttpResponseRedirect(reverse("index"))
            
    else:
        form = AuctionCreationForm()
        return render(request, "auctions/create_auction.html", {'form': form})
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.forms import ModelForm
from auctions.models import Listings

from .models import User, Listings, Bids, Comments, Watchlist

class NewListingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewListingForm, self).__init__(*args, **kwargs)
        # change item image URL to be optional
        self.fields["item_image"].required = False
        self.fields["category"].required = False
        
    class Meta:
        model = Listings
        fields = ['item_name', 'description', 'item_image', 'category', 'list_value',]
        widgets = {
            'item_name': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.Textarea(attrs={"class":"form-control", "rows":"3"}),
            'item_image': forms.URLInput(attrs={"class":"form-control"}),
            'category': forms.TextInput(attrs={"class": "form-control"}),
            'list_value': forms.NumberInput(attrs={"class":"form-control"}),
        }

def index(request):
    auctions = Listings.objects.exclude(status=False).all()
    return render(request, "auctions/index.html", {
        "auctions": auctions,
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
        form = NewListingForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.seller = request.user
            save_form.save()
            return redirect("index")
            
    else:
        return render(request, "auctions/listitem.html", {
            "NewListingForm": NewListingForm,
        })
        
def listing_view(request, listing_id):
    listing = Listings.objects.get(pk=listing_id)
    if request.method == "POST" and 'watchlist_add' in request.POST:
        user = request.user
        item = Listings.objects.get(pk=listing_id)
        # check if already in watchlist
        watchlist_check = Watchlist.objects.filter(user=request.user).filter(watched_item=item).all()
        if watchlist_check:
            return render(request, "auctions/listing.html", {
                "warning": "Already in watchlist",
                "listing": listing,
            })
            # save to sql
        sv = Watchlist(user=user, watched_item=item)
        sv.save()            
        return redirect("watchlist")
    # submit bid
    if request.method == "POST" and "submit_bid" in request.POST:
        pass

    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
        })
    
def categories(request):
    all_categories = Listings.objects.values_list("category", flat=True)
    category = sorted(set(all_categories), key=lambda x: (x is None, x))
    return render(request, "auctions/categories.html", {
        "category": category,
    })
    
def category(request, category):
    cat_items = Listings.objects.filter(category=category).all()
    return render(request, "auctions/category.html", {
        "category": cat_items,
        "cat_name": category,
    })
    
def watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user).all() 
    value = "0"
    if request.method == "POST":
        value = request.POST.get("remove_watch", "")
        entry = Watchlist.objects.filter(pk=value).all()
        entry.delete()
        
    return render(request, "auctions/watchlist.html", {
        "watching": watchlist,
        "test": value,
    })
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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
        
class BidForm(ModelForm):
    class Meta:
        model = Bids
        fields = ["bid_value"]
        widgets = {
            "bid_value": forms.NumberInput(attrs={"class":"form-control"}),
        }
        
class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ["comment_text"]
        widgets = {
            "comment_text": forms.Textarea(attrs={"class":"form-control", "rows":"2"})
        }

def index(request):
    # Show active listings
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
   
   
@login_required 
def create_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.seller = request.user
            save_form.save()
            return redirect("listing", save_form.id)
            
    else:
        return render(request, "auctions/listitem.html", {
            "NewListingForm": NewListingForm,
        })
        
        
def listing_view(request, listing_id):
    # empty warnings
    warning = ""
    bidwarning = ""
    listing = Listings.objects.get(pk=listing_id)
    comment_list = Comments.objects.filter(comment_item=listing_id)
    bid_no = len(Bids.objects.filter(bid_item=listing_id).all())
    # add to watchlist
    if request.method == "POST" and 'watchlist_add' in request.POST:
        user = request.user
        item = Listings.objects.get(pk=listing_id)
        # check if already in watchlist
        watchlist_check = Watchlist.objects.filter(user=request.user).filter(watched_item=item).all()
        if not watchlist_check:
            sv = Watchlist(user=user, watched_item=item)
            sv.save()            
            return redirect("watchlist")
        warning = "Already in watchlist"
    # submit bid
    if request.method == "POST" and "submit_bid" in request.POST:
        form = BidForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit=False)
            last_bid = Bids.objects.filter(bid_item=listing).last()
            if not last_bid:
                last_bid = 0.00
            else:
                last_bid = last_bid.bid_value
            if save_form.bid_value >= listing.current_value and save_form.bid_value > last_bid:
                save_form.bidder = request.user
                save_form.bid_item = listing
                # change current value
                listing.current_value = save_form.bid_value
                save_form.save()
                listing.save()
            else:
                bidwarning = "Bid is too low"
    # submit comment
    if request.method == "POST" and "submit_comment" in request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.commenter = request.user
            save_form.comment_item = listing
            save_form.save()
    # close auction
    if request.method == "POST" and "close_auction" in request.POST:
        listing.status = False
        if bid_no > 0:
            winning_bid = Bids.objects.filter(bid_item=listing).last()
            listing.winner = winning_bid.bidder
        # save all changes
        listing.save()
            
    test = Bids.objects.filter(bid_item=listing).last()
    return render(request, "auctions/listing.html", {
        "warning": warning,
        "listing": listing,
        "bidno": bid_no,
        "bidform": BidForm,
        "bidwarning": bidwarning,
        "commentform": CommentForm,
        "comment_list": comment_list,
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


@login_required    
def watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user).all() 
    value = "0"
    if request.method == "POST":
        value = request.POST.get("remove_watch", "")
        entry = Watchlist.objects.filter(pk=value).all()
        entry.delete()
        
    return render(request, "auctions/watchlist.html", {
        "watching": watchlist,
    })
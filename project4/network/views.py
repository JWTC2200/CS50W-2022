from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import User, Posts, Follows


def index(request):
    all_posts = Posts.objects.all()
    paginator_all = Paginator(all_posts, 3)
    page_number = 1
    if request.GET.get("page") != None:
        page_number = request.GET.get("page")
    return render(request, "network/index.html", {
        "all_posts": paginator_all.page(page_number),
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def user(request):
    if request.method == "POST":
        post_content = request.POST["post-content"]
        if len(post_content) > 0:
            Posts(user=request.user, content=post_content).save()
    
    username = request.user.username
    user = User.objects.get(username=username)
    user_posts = Posts.objects.filter(user=user)
    

    return render(request, "network/user.html", {
        "user_posts": user_posts,
    })    
        
@login_required
def following(request):
    return render(request, "network/following.html")

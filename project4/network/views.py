from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

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
def user(request, profile):
    user_profile = User.objects.get(username=profile)
    user_posts = Posts.objects.filter(user=user_profile)
    
    # check if user is already followed
    follow_btn = ""
    if user_profile != request.user:
        if request.user in user_profile.followers.all():
            follow_btn = "UNFOLLOW"
        else:
            follow_btn = "FOLLOW"
            
    # user following and follower counts
    follow_count = user_profile.follows_count()
    follower_count = user_profile.followers_count()
    
    return render(request, "network/user.html", {
        "user_posts": user_posts,
        "profile_name": profile,
        "follow_btn": follow_btn,
        "follow_count": follow_count,
        "follower_count": follower_count,
    })    

@login_required
def new_post(request):
    if request.method == "POST":
        post_content = request.POST["post-content"]
        if len(post_content) > 0:
            Posts(user=request.user, content=post_content).save()
    
    return render(request, "network/newpost.html")
    
        
@login_required
def following(request):
    return render(request, "network/following.html")

@csrf_exempt
@login_required
def likepost(request):

    data = json.loads(request.body)
    post_id = data.get("id")
    post = Posts.objects.get(pk=post_id)
    liker = User.objects.get(username=request.user.username)

    if post.likes.filter(username=liker):
        post.likes.remove(liker)
    else:
        post.likes.add(liker)
    
    return JsonResponse({"count": post.LikeCount()}, safe=True)

@csrf_exempt
@login_required
def following(request):
    
    follow_status = ""
    
    data = json.loads(request.body)
    to_follow = data.get("to_follow")
    target_account = User.objects.get(username=to_follow)
    
    if request.user in target_account.followers.all():
        target_account.followers.remove(request.user)
        follow_status = "FOLLOW"
    else:
        target_account.followers.add(request.user)
        follow_status = "UNFOLLOW"

    follower_count = target_account.followers_count()
    print(f"{target_account.followers.all()}")
    
    return JsonResponse(
        {"follow_status": follow_status,
         "follow_count": follower_count, 
        }, safe=True)
    
    
    
                


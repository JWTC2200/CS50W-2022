from django.db import IntegrityError
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse


from .models import User


# Create your views here.

def index(request):
    return render(request, "calculator/index.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "calculator/login.html", {
                "message": "Invalid username and/or password"
            })
    else:
        return render(request, "calculator/login.html")

def logout_view(request):
    logout(request)
    return redirect("index")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if not username:
            return render(request, "calculator/register.html",  {
                "message": "Please enter a username"
            })
        if not email:
            return render(request, "calculator/register.html",  {
                "message": "Please enter a email"
            })
        if not password:
            return render(request, "calculator/register.html",  {
                "message": "Please enter a password"
            })
        if password != confirmation:
            return render(request, "calculator/register.html",  {
                "message": "Passwords must match"
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "calculator/register.html", {
                "messsage": "Username alreader taken"
            })
        login(request, user)
        return redirect("index")
    else: 
        return render(request, "calculator/register.html")

@login_required    
def artifacts(request):
    return render(request, "calculator/artifacts.html")
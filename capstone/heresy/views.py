from django.db import IntegrityError
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse


from .models import User, Infantry, Weapons


# Create your views here.

def index(request):
    return render(request, "heresy/index.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "heresy/login.html", {
                "message": "Invalid username and/or password"
            })
    else:
        return render(request, "heresy/login.html")

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
            return render(request, "heresy/register.html",  {
                "message": "Please enter a username"
            })
        if not email:
            return render(request, "heresy/register.html",  {
                "message": "Please enter a email"
            })
        if not password:
            return render(request, "heresy/register.html",  {
                "message": "Please enter a password"
            })
        if password != confirmation:
            return render(request, "heresy/register.html",  {
                "message": "Passwords must match"
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "heresy/register.html", {
                "messsage": "Username alreader taken"
            })
        login(request, user)
        return redirect("index")
    else: 
        return render(request, "heresy/register.html")
    
@login_required
def builder(request):
    all_units = Infantry.objects.all()
    troops = Infantry.objects.filter(force_org = "Troops")
    elites = Infantry.objects.filter(force_org = "Elites")
    heavysupport = Infantry.objects.filter(force_org = "Heavy Support")
    tac = Infantry.objects.get(name = "Legion Heavy Support Squad").split_weapons()
    print(tac["Lascannon"])
    
    
    context = {
        "troops": troops,
        "elites": elites,
        "heavysupport": heavysupport,
        "all_units": all_units,
        }
    
    return render(request, "heresy/builder.html", context)


@login_required
def unit_total(request):
    if request.method == "PUT":
        unit_id = json.loads(request.body).get("unit_pk")
        unit = Infantry.objects.get(pk = unit_id).split_weapons()
        squad_value = Infantry.objects.get(pk = unit_id).unit_cost
        return JsonResponse({
            "list": unit,
            "squad":squad_value,
            }, safe=True)
    
    return HttpResponse(403)
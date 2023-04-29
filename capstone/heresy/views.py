from django.db import IntegrityError
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from fractions import Fraction
from decimal import Decimal


from .models import User, Infantry, Weapons, ArmyLists, ListBlocks
from .calculations import attack_calculations 


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
    fastattack = Infantry.objects.filter(force_org = "Fast Attack")
    hq = Infantry.objects.filter(force_org = "HQ")
    tac = Infantry.objects.get(name = "Legion Heavy Support Squad").split_weapons()
    print(tac["Lascannon"])
    
    
    context = {
        "troops": troops,
        "elites": elites,
        "heavysupport": heavysupport,
        "fastattack": fastattack,
        "hq": hq,
        "all_units": all_units,
        }
    
    return render(request, "heresy/builder.html", context)


@login_required
def unit_total(request):
    if request.method == "PUT":
        unit_id = json.loads(request.body).get("unit_pk")
        model = Infantry.objects.get(pk = unit_id)
        return JsonResponse({
            "name": model.name,
            "list": model.split_weapons(),
            "squad":model.unit_cost,
            "force_org": model.force_org,
            "members": model.squad_size,
            }, safe=True)
    
    return HttpResponse(403)

@login_required
def list_name_check(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        try:
            ArmyLists.objects.filter(user=request.user).get(name = data.get("newname"))                  
            return JsonResponse({"warning":"List with that name already exists 55."}) 
        
        except ObjectDoesNotExist:
            print("does not exist")
            if not data.get("newname"):
                return JsonResponse({"warning":"Please enter a list name"})
            return HttpResponse(200)
                
    return HttpResponse(403)

@login_required
def savelist(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        if not data:
            return JsonResponse({"warning": "Not a valid list."})
        # create army list and check for existing name
        army_name = data.get("list_name")
        try:
            ArmyLists.objects.filter(user = request.user).get(name = army_name)
        except ObjectDoesNotExist:
            ArmyLists(user = request.user, name = army_name, points = data["list_points"]).save()
            
        raw_name = data["unit_name"].split("(")
        unit_name = raw_name[0].strip()
        unit_members = raw_name[1].strip().replace(")","")
        unit_weapons = data["unit_weapons"]
        force_org = Infantry.objects.get(name=unit_name).force_org
        unit_points = data["unit_points"]
        
        ListBlocks(
            armylist = ArmyLists.objects.filter(user = request.user).get(name = army_name),
            force_org = force_org,
            unit_name = unit_name,
            unit_points = unit_points,
            unit_weapons = unit_weapons,
            unit_members = unit_members,
            ).save()
        
        print("success")
        return JsonResponse({"warning": "success"})
        
        
    return HttpResponse(403)

@login_required
def list_view(request):
    lists = ArmyLists.objects.filter(user = request.user)
    
    if request.method == "PUT":
        data = json.loads(request.body)
        list_id = data["list_id"]
        listcheck = ArmyLists.objects.filter(name = list_id).get(user = request.user)
        list_blocks = listcheck.list_units()
        print(list_blocks)
        return JsonResponse({"warning": "success"})
    
    if request.method == "GET":
        context = {
            "lists": lists,
        }
        return render(request, "heresy/listview.html", context)
    
    return redirect("index")



@login_required
def damage_page(request):

    return render(request, "heresy/damagepage.html")
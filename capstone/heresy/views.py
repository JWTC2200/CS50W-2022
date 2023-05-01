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
            ArmyLists(user = request.user, name = data.get("newname"), points = data["list_points"]).save()
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
        force_org, unit_name, unit_points, unit_weapons, unit_members = ([] for i in range(5))
        for block in list_blocks:            
            force_org.append(block.force_org)
            unit_name.append(block.unit_name)
            unit_points.append(block.unit_points)
            unit_weapons.append(block.unit_weapons)
            unit_members.append(block.unit_members)
            
            
        return JsonResponse({
            "force_org": force_org,
            "unit_name": unit_name,
            "unit_points": unit_points,
            "unit_weapons": unit_weapons,
            "unit_members": unit_members,
            })
        
    if request.method == "GET":
        context = {
            "lists": lists,
        }
        return render(request, "heresy/listview.html", context)    
    return redirect("index")



@login_required
def damage_page(request):
    user_lists = ArmyLists.objects.filter(user = request.user)

    context = {
        "user_lists": user_lists,
    }
    if request.method == "PUT":
        data = json.loads(request.body)
        if data["page"] == "damage":
            print("damage")
        if data["page"] == "link":
            print("link")
    return render(request, "heresy/damagepage.html", context)

@login_required
def damage_list(request):
    data = json.loads(request.body)
    list_name = data["list_name"]
    army_list = ArmyLists.objects.filter(user = request.user).get(name = list_name)
    list_units = ListBlocks.objects.filter(armylist = army_list)
    units_dict = {}
    for unit in list_units:
        weapons = unit.unit_weapons
        replacelist = ["[", ",", "]", "'"]
        for item in replacelist:
            weapons = weapons.replace(item, "")
        units_dict[unit.pk] = weapons
        
    unit_json = json.dumps(units_dict)
    unit_json = json.loads(unit_json)
    
    return JsonResponse(unit_json)

@login_required
def damage_unit_pk(request):
    data = json.loads(request.body)
    unit_pk = data["unit_pk"]
    name = ListBlocks.objects.get(pk = unit_pk).unit_name
    return JsonResponse({"name": name})
    
@login_required
def damage_load_unit_stats(request):
    data = json.loads(request.body)
    unit_name = ListBlocks.objects.get(pk = data["unit_id"].replace("xyz", "")).unit_name
    unit_stat = Infantry.objects.get(name = unit_name)
       
    print(unit_stat)
    
    return JsonResponse({
        "M": unit_stat.movement,
        "WS": unit_stat.weapon_skill,
        "BS": unit_stat.ballistic_skill,
        "S": unit_stat.strength,
        "T": unit_stat.toughness,
        "W": unit_stat.wounds,
        "I": unit_stat.initiative,
        "A": unit_stat.attacks,
        "Ld": unit_stat.leadership,
        "Sv": unit_stat.armour_save,
        "Inv": unit_stat.inv_save
    })

   
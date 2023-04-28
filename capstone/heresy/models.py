from django.db import models
from django.contrib.auth.models import AbstractUser
import re
from django.core.exceptions import ValidationError


# validators

def validate_force_org(value):
    slotlist = [
        "HQ", "Elites", "Troops", "Fast Attack", "Heavy Support",
    ]
    if value not in slotlist:
        raise ValidationError(
            "Must be one of: HQ, Elites, Troops, Fast Attack, Heavy Support"
        )


# Create your models here.


class User(AbstractUser):
    def saved_armylists(self):
        return ArmyLists.objects.filter(user = self)
    
    def __str__(self):
        return f"{self.saved_armylists()}"
    
    
class Infantry(models.Model):
    name = models.CharField(max_length=50)
    force_org = models.CharField(max_length=50, default="Troops", validators=[validate_force_org])
    movement = models.IntegerField(default=7)
    weapon_skill = models.IntegerField(default=4)
    ballistic_skill = models.IntegerField(default=4)
    strength = models.IntegerField(default=4)
    toughness = models.IntegerField(default=4)
    wounds = models.IntegerField(default=1)
    initiative = models.IntegerField(default=4)
    attacks = models.IntegerField(default=1)
    leadership = models.IntegerField(default=7)
    armour_save = models.IntegerField(default=3)
    inv_save = models.IntegerField(default=0)
    weapon_list= models.TextField(blank=True, default="")
    equipment = models.TextField(blank=True, default="")
    unit_cost = models.IntegerField(default=0)
    member_cost = models.IntegerField(default=0)
    squad_size = models.IntegerField(default=5)
    squad_add = models.IntegerField(default=0)
    squad_max = models.IntegerField(default=5)
                   
    def split_weapons(self):
        raw_list = self.weapon_list.split(",")
        end_list = {}
        for item in raw_list:
            split_list = re.split('(\d+)', item)
            end_list.update({split_list[0].strip():split_list[1].strip()})
        return end_list
    
    
    
    class Meta:
        ordering = ['force_org']
        
    def __str__(self):
        return f"{self.force_org} - {self.name}: {self.split_weapons()}"
    
    
class Weapons(models.Model):
    name = models.CharField(max_length=50)
    distance = models.IntegerField(default=24)
    strength = models.IntegerField(default=4)
    armour_pen = models.IntegerField(default=0)
    effects = models.TextField(blank=True, default="")
    
    def effects_list(self):
        return self.effects.split(",")
        
    
    def __str__(self):
        return f"{self.name}: Range{self.distance} Str{self.strength} AP{self.armour_pen} Effects:{self.effects_list()}"
    

class ArmyLists(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['name']
        
    def list_units(self):
        return ListBlocks.objects.filter(armylist = self)
        
    def __str__(self):
        return f"{self.name}"


class ListBlocks(models.Model):
    armylist = models.ForeignKey(ArmyLists, on_delete=models.CASCADE)
    force_org = models.CharField(max_length=50, validators=[validate_force_org])
    unit_name = models.CharField(max_length=50)
    unit_points = models.IntegerField(default=0)
    unit_weapons = models.TextField(blank=True, default="")
    unit_members = models.IntegerField(default=1)
    
    def split_weaponsns(self):
        pass
    
    def __str__(self):
        return f"{self.unit_name}: {self.unit_points}"
    
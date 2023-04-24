from django.db import models
from django.contrib.auth.models import AbstractUser
import re

# Create your models here.


class User(AbstractUser):
    
    def __str__(self):
        return f"{self.username}"
    
    
class Infantry(models.Model):
    name = models.CharField(max_length=50)
    force_org = models.CharField(max_length=50, default="Troops")
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
    
    def split_weapons(self):
        raw_list = self.weapon_list.split(",")
        end_list = {}
        for item in raw_list:
            split_list = re.split('(\d+)', item)
            end_list.update({split_list[0].rstrip().lstrip():split_list[1].rstrip().lstrip()})
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
    
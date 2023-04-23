from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    artifacts = models.ManyToManyField("Artifact", symmetrical=False, blank=True)
    characters = models.ManyToManyField("Characters", symmetrical=False, blank=True)
    weapons = models.ManyToManyField("Weapons", symmetrical=False, blank=True)
    
    def __str__(self):
        return f"{self.username}"
    
    def artifact_count(self):
        return self.artifacts.count()
    
    def characters_count(self):
        return self.characters.count()
    
    def weapons_count(self):
        return self.weapons.count()

class Artifact(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    slot = models.CharField(max_length=10)
    set = models.ForeignKey("Artifact_Set", on_delete=models.CASCADE)
    base_stat = models.CharField(max_length=50)
    base_value = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    attack = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    attackper = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    defence = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    defenceper = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    health = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    healthper = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    elemental_mastery = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    crit_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    crit_damage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    healing_bonus = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    energy_recharge = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    bonus_anemo = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    bonus_cryo = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    bonus_dendro = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    bonus_electro = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    bonus_geo = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    bonus_hydro = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    bonus_physical = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    bonus_pyro = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    class Meta:
        ordering = ["-datetime"]
        
    def __str__(self):
        return f"{self.pk} {self.slot}, {self.set}"
    
class Artifact_Set(models.Model):
    set_name = models.CharField(max_length=50)
    bonus_two = models.CharField(max_length=50)
    bonus_value = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    bonus_full = models.TextField()
    
    def __str__(self):
        return f"{self.set_name}: {self.bonus_two} +{self.bonus_value}%"
    
    
    
class Characters(models.Model):
    
    pass
    
class Weapons(models.Model):
    pass
    
    
    
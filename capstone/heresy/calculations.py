from fractions import Fraction
from decimal import Decimal
from .models import Infantry, Weapons
import re


def attack_calculations(BS, attack, target):
    full_results = {}
    # convert target into dict
    target = target.split("-")
    target = {"toughness": target[0],
        "wounds": target[1],
        "armour": target[2],
        "inv": target[3]}
    remove = ["[", "]", "'"]
    for r in remove:
        attack = attack.replace(r, "")
    attacks = attack.split(",")
    list = {}
    for a in attacks:
        split_list = re.split('(\d+)', a)
        list.update({split_list[2].strip(): split_list[1].strip()})
    for wp, atk in list.items():
        # wp = weapon name, atk = number of weapons
        strength = Weapons.objects.get(name=wp).strength
        apen = Weapons.objects.get(name=wp).armour_pen
        raw_effects = Weapons.objects.get(name=wp).effects
        raw_effects = raw_effects.split(",")
        eff_list = {}
        for eff in raw_effects:
            spl_eff = re.split('(\d+)', eff)
            eff_list.update({spl_eff[0].strip(): spl_eff[1].strip()})
   
        # RESULT
        result = attack_to_hit(BS, eff_list)
        result *= attack_to_wound(strength, target["toughness"], target["wounds"], eff_list, apen, target["armour"], target["inv"]) 
        result *= int(atk)
        
        if "Heavy" in eff_list.keys():
            result *= int(eff_list["Heavy"])
        if "Pistol" in eff_list.keys():
            result *= int(eff_list["Pistol"])
                
        full_results[wp] = format(float(result), '.2f')
    return full_results
    

def attack_to_hit(BS, effects):
    odds = Fraction(BS, 6)
    if "Twin-linked" in effects.keys():
        rerolls = Fraction(6-BS, 6)
        rerolls *= odds
        odds += rerolls
    print(f"odds {odds}")
    return odds

def attack_to_wound(S, T, W, effects, AP, AV, INV):
    
    S = int(S)
    T = int(T)
    W = int(W)
    odds = 0
    if S == T:
        odds = Fraction(1,2)
    if (S - T) > 0:
        odds = Fraction(2,3)
    if (S - T) > 1:
        odds = Fraction(5,6)
    if (S - T) < 0:
        odds = Fraction(1,3)
    if (S - T) < -1:
        odds = Fraction(1,6)
    
    # check for effects    
    eff_check = ["Rending", "Breaching"]
    effect_mod = 0
    for eff in eff_check:
        if eff in effects.keys():
            eff_rate = Fraction(7-int(effects[eff]), 6)
            # check vs wound roll
            if odds > eff_rate:
                odds -= eff_rate
                effect_mod = eff_rate * attack_inv(INV)
            if odds <= eff_rate:
                effect_mod = odds * attack_inv(INV)
                odds = 0
    print(odds)
    odds *= attack_armour(AP, AV, effects, INV)
    print(odds, effect_mod)

    odds += effect_mod    
    # check for double strength instant death
    if (S / T) >= 2:
        odds *= W
    return odds

def attack_armour(AP, AV, effects, INV):
    odds = Fraction(int(AV)-1, 6)
    AP = int(AP)
    AV = int(AV)
    if AP == 0:
        return odds
    if AP > AV:
        return odds
    return attack_inv(INV)

def attack_inv(INV):
    INV = int(INV)
    odds = Fraction(7-INV, 6)
    if INV == 0:
        return 1
    return odds
    
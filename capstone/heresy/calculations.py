from fractions import Fraction
from decimal import Decimal
from .models import Infantry, Weapons
import re


def attack_calculations(BS, attack, target):
    # convert target into dict
    target = target.split("-")
    target = {"toughness": target[0],
        "wounds": target[1],
        "armour": target[2],
        "inv": target[3]}
    print(target)
    remove = ["[", "]", "'"]
    for r in remove:
        attack = attack.replace(r, "")
    attacks = attack.split(",")
    list = {}
    for a in attacks:
        split_list = re.split('(\d+)', a)
        list.update({split_list[2].strip(): split_list[1].strip()})
    for wp, atk in list.items():
        print(wp, atk)
        strength = Weapons.objects.get(name=wp).strength
        apen = Weapons.objects.get(name=wp).armour_pen
        
        # RESULT
        result = attack_to_hit(BS) * attack_to_wound(strength, target["toughness"], target["wounds"]) * attack_armour(apen, target["armour"]) * attack_inv(target["inv"])
        print(f"result {result}")
    

def attack_to_hit(BS):
    odds = Fraction(BS, 6)
    print(f"tohit {odds}")
    return odds

def attack_to_wound(S, T, W):
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
    if (S / T) >= 2:
        odds *= W
    print(f"to wound {odds}")
    return odds

def attack_armour(AP, AV):
    odds = Fraction(7-AP, 6)
    print(f"save: {odds}")
    AP = int(AP)
    AV = int(AV)
    if AP == 0:
        return odds
    if AP > AV:
        return odds
    return 1

def attack_inv(INV):
    INV = int(INV)
    odds = Fraction(7-INV, 6)
    if INV == 0:
        return 1
    return odds
    
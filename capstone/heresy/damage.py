from fractions import Fraction
from decimal import Decimal



bskill = 1

hit_roll = Fraction(6-(6-bskill), 6)

toughness = 4

strength = 6

if strength >= toughness + 2:
    wound_roll = Fraction(5/6)
    



print(hit_roll)


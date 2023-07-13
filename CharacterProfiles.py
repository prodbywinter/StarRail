# character data is stored here
from Statics import *


class Character:
    def __init__(self, name, maxEnergy, basicEnergy, skillEnergy, ultEnergy, options, attacksWith):
        self.name = name
        self.maxEnergy = maxEnergy
        self.basicEnergy = basicEnergy
        self.skillEnergy = skillEnergy
        self.ultEnergy = ultEnergy
        self.options = options  # buffs available to the character
        self.attacksWith = attacksWith  # does character attack an enemy with [SKILL, ULT]


Asta = Character('ASTA', 120, 20, 36, 5, [1, 2, 5, 6, 9], [1, 0])  # Asta E1 gives skill 6 more energy
Bailu = Character('BAILU', 100, 20, 30, 5, [1, 2, 3, 4, 6], [0, 0])
Natasha = Character('NATASHA', 90, 20, 30, 5, [1, 2, 3, 4, 6], [0, 0])
SilverWolf = Character('SILVER WOLF', 110, 20, 30, 5, [1, 2, 6, 7, 8], [1, 1])
Tingyun = Character('TINGYUN', 130, 25, 35, 5, [1, 2, 6, 9], [0, 0])  # Tingyun A6 gives 5 energy on turn start
Pela = Character('PELA', 110, 20 + PELA_TALENT, 30 + PELA_TALENT, 5 + PELA_TALENT, [1, 2, 6, 8], [1, 1])
Serval = Character('SERVAL', 100, 20, 30, 5, [1, 2, 6], [1, 1])
DanHeng = Character('DAN HENG', 100, 20, 30, 5, [1, 2, 6, 7], [1, 1])
Gepard = Character('GEPARD', 100, 20, 30, 5, [1, 2, 6], [1, 0])

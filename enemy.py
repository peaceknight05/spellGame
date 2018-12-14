import random
import json

ENEMY_HEALTH = [100, 110, 120, 150]
ENEMY_MANA = [10, 15, 20, 25]

class Enemy:
    health = 0
    mana = 0
    tier = 0
    attribute = ""

    def __init__(self):
        global ENEMY_HEALTH
        global ENEMY_MANA

        ran = random.randint(0,3)
        if (ran == 0):
            self.attribute = "fire"
        elif (ran == 1):
            self.attribute = "water"
        elif (ran == 2):
            self.attribute = "earth"
        else:
            self.attribute = "air"

        self.tier = random.randint(0,4)
        self.health = ENEMY_HEALTH[self.tier]
        self.mana = ENEMY_MANA[self.tier]
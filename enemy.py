import random
import json

ENEMY_HEALTH = [100, 110, 120, 150]
ENEMY_MANA = [10, 15, 20, 25]

class Enemy:
    VALID_SPELLS = ["small_fireball", "water_bullet", "cutting_wind", "rock_smash", "healing_drop", "minor_pheonix_heal", "nourishing_mud", "refreshing_air"]
    SPELL_DATA = {}

    health = 0
    mana = 0
    tier = 0
    effects = set()
    defensePoints = 0
    defensePercentage = 0
    attribute = ""

    maxHealth = 0
    maxMana = 0

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

        for spell in self.VALID_SPELLS:
            with open("spells/" + spell + ".json", "r") as spellFile:
                data = json.load(spellFile)
                self.SPELL_DATA[spell] = data

        self.tier = random.randint(0,4)
        self.health = ENEMY_HEALTH[self.tier]
        self.mana = ENEMY_MANA[self.tier]
        self.maxHealth = ENEMY_HEALTH[self.tier]
        self.maxMana = ENEMY_MANA[self.tier]

    def getusedSpells(self):
        return self.usedSpells

    def getAttribute(self):
        return self.attribute

    def isCastableSpell(self, spellName):
        return ((self.tier >= self.SPELL_DATA[spellName]["tier"]) & (self.attribute == self.SPELL_DATA[spellName]["attribute"]))
    
    def isMasteredSpell(self, spellName):
        return spellName in self.masteredSpells

    def hasEffect(self, effectName):
        for effect in self.effects:
            if (effect[0] == effectName):
                return True

        return False

    def addusedSpell(self, spellName):
        if (spellName in self.usedSpells):
            return
        self.usedSpells.append(spellName)

    def addMasteredSpell(self, spellName):
        if (spellName in self.masteredSpells):
            return
        self.masteredSpells.append(spellName)

    def addEffect(self, effectName):
        if (self.hasEffect(effectName)):
            print("Enemy already has effect \"" + effectName + "\"")
        else:
            if ((effectName == "burn") & (self.hasEffect("abestos"))):
                print("Enemy has abestos!")
                return
            elif ((effectName == "poison") & (self.hasEffect("immunity"))):
                print("Enemy has immunity!")
                return
            self.effects.add([effectName, 3])
            print("Enemy has just been given the \"" + effectName + "\" effect")

    def turnEnd(self):
        if (self.mana != self.maxMana):
            self.mana += random.randint(1,3)
            if (self.mana > self.maxMana):
                self.mana = self.maxMana
        self.processEffects()
import random
import json

class Player:
    VALID_SPELLS = ["small_fireball", "water_bullet", "cutting_wind", "rock_smash"]
    SPELL_DATA = {}

    unlockedSpells = []
    masteredSpells = []
    health = 100
    attribute = ""
    tier = 0
    mana = 10

    def __init__(self):
        rand = random.randint(0,3)
        if (rand == 0):
            self.attribute = "air"
        elif (rand == 1):
            self.attribute = "water"
        elif (rand == 2):
            self.attribute = "earth"
        else:
            self.attribute = "fire"

        possibleFirstSpells = []

        for spell in self.VALID_SPELLS:
            with open("spells/" + spell + ".json", "r") as spellFile:
                data = json.load(spellFile)
                self.SPELL_DATA[spell] = data
                if ((self.SPELL_DATA[spell]["tier"] == 0) & (self.SPELL_DATA[spell]["attribute"] == self.attribute)):
                    possibleFirstSpells.append(spell)

        rand = random.randint(0, len(possibleFirstSpells) - 1)
        self.unlockedSpells.append(possibleFirstSpells[rand])

        print("Your attribute is: " + self.attribute)
        print("You have unlocked: " + self.SPELL_DATA[self.unlockedSpells[0]]["game_name"] + " (Tier: 0)")

    def getHealth():
        return self.health

    def getAttribute():
        return self.attribute

    def getTier():
        return self.tier

    def getMana():
        return self.mana

    def inUnlockedSpell(spellName):
        return spellName in self.unlockedSpells
    
    def isMasteredSpells(spellName):
        return spellName in self.masteredSpells

    def addUnlockedSpells(spellName):
        if (spellName in self.unlockedSpells):
            return
        self.unlockedSpells.append(spellName)

    def addMasteredSPells(spellName):
        if (spellName in self.masteredSpells):
            return
        self.masteredSpells.append(spellName)
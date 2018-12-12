import random
import json

class Player:
    VALID_SPELLS = ["small_fireball", "water_bullet", "cutting_wind", "rock_smash"]
    SPELL_DATA = {}

    encounteredSpells = []
    masteredSpells = []
    health = 100
    attribute = ""
    tier = 0
    mana = 10
    effects = []
    defensePoints = 0
    defensePercentage = 0
    tierUpgradeProgress = 0
    tierUpgradeRequirements = [5, 10, 20]

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
        self.encounteredSpells.append(possibleFirstSpells[rand])

        print("Your attribute is: " + self.attribute)
        print("You have encountered: " + self.SPELL_DATA[self.encounteredSpells[0]]["game_name"] + " (Tier: 0)")

    def getHealth(self):
        return self.health

    def getAttribute(self):
        return self.attribute

    def getTier(self):
        return self.tier

    def getMana(self):
        return self.mana

    def getEncounteredSpells(self):
        return self.encounteredSpells

    def isCastableSpell(self, spellName):
        return ((self.tier >= self.SPELL_DATA[spellName]["tier"]) & (self.attribute == self.SPELL_DATA[spellName]["attribute"]))
    
    def isMasteredSpell(self, spellName):
        return spellName in self.masteredSpells

    def addEncounteredSpell(self, spellName):
        if (spellName in self.encounteredSpells):
            return
        self.encounteredSpells.append(spellName)

    def addMasteredSpell(self, spellName):
        if (spellName in self.masteredSpells):
            return
        self.masteredSpells.append(spellName)

    def addEffect(self, effectName):
        self.effects.append(effectName)

    def setHealth(self, health):
        self.health = health

    def setMana(self, mana):
        self.mana = mana

    def statsReset(self):
        self.mana = 10
        self.health = 100
        self.effect = []

    #method to deduct health, defense points etc
    #def processAttack(spellName):
    
    #method to process good/bad effects
    #def processEffects():

    def processSpell(self, spellName):
        self.mana -= self.SPELL_DATA[spellName]["mana_consumption"]
        if (self.SPELL_DATA[spellName]["type"] == "offense"):
            if not (self.isMasteredSpell(spellName)):
                rand = random.randint(0,99)
                if (rand > self.SPELL_DATA[spellName]["master_percentage"]):
                    self.addMasteredSpell(spellName)
                    print("You have mastered " + self.SPELL_DATA[spellName]["game_name"] + " (Tier: " + str(self.SPELL_DATA[spellName]["tier"]) + ")")
                    return
                
                rand = random.randint(0,99)
                if (rand > self.SPELL_DATA[spellName]["backfire_chance"]):
                    temp = self.health
                    self.health -= self.SPELL_DATA[spellName]["damage"]
                    print(self.SPELL_DATA[spellname] + " backfired!")
                    print("Health dropped from " + str(temp) + " to " + str(self.health))
        elif (self.SPELL_DATA[spellName]["type"] == "defense"):
            if not (self.isMasteredSpell(spellName)):
                rand = random.randint(0,99)
                if (rand > self.SPELL_DATA[spellName]["master_percentage"]):
                    self.addMasteredSpell(spellName)
                    print("You have mastered " + self.SPELL_DATA[spellName]["game_name"] + " (Tier: " + str(self.SPELL_DATA[spellName]["tier"]) + ")")
                else:
                    rand = random.randint(0,99)
                    if (rand > self.SPELL_DATA[spellName]["backfire_chance"]):
                        print(self.SPELL_DATA[spellname] + " backfired!")
                    else:
                        if (self.SPELL_DATA[spellName]["defense_class"] == 1):
                            self.defensePoints += self.SPELL_DATA[spellName]["defense_value"]
                        else:
                            self.defensePercentage += self.SPELL_DATA[spellName]["defense_value"]
                            if (self.defensePercentage > 100):
                                self.defensePercentage = 100
            else:
                if (self.SPELL_DATA[spellName]["defense_class"] == 1):
                    self.defensePoints += self.SPELL_DATA[spellName]["defense_value"]
                else:
                    self.defensePercentage += self.SPELL_DATA[spellName]["defense_value"]
                    if (self.defensePercentage > 100):
                        self.defensePercentage = 100
        else:
            if not (self.isMasteredSpell(spellName)):
                rand = random.randint(0,99)
                if (rand > self.SPELL_DATA[spellName]["master_percentage"]):
                    self.addMasteredSpell(spellName)
                    print("You have mastered " + self.SPELL_DATA[spellName]["game_name"] + " (Tier: " + str(self.SPELL_DATA[spellName]["tier"]) + ")")
                else:
                    rand = random.randint(0,99)
                    if (rand > self.SPELL_DATA[spellName]["backfire_chance"]):
                        print(self.SPELL_DATA[spellname] + " backfired!")
                        if (self.SPELL_DATA[spellName]["support_class"] == 1):
                            temp = self.health
                            self.health -= self.SPELL_DATA[spellName]["heal_value"]
                            print("Health dropped from " + str(temp) + " to " + str(self.health))
                        elif (self.SPELL_DATA[spellName]["support_class"] == 3):
                            self.addEffect(self.SPELL_DATA[spellName]["effect"])
                    else:
                        if (self.SPELL_DATA[spellName]["support_class"] == 1):
                            temp = self.health
                            self.health -= self.SPELL_DATA[spellName]["heal_value"]
                            print("Health rose from " + str(temp) + " to " + str(self.health))
                        elif (self.SPELL_DATA[spellName]["support_class"] == 2):
                            self.addEffect(self.SPELL_DATA[spellName]["effect"])
            else:
                if (self.SPELL_DATA[spellName]["support_class"] == 1):
                    temp = self.health
                    self.health -= self.SPELL_DATA[spellName]["heal_value"]
                    print("Health rose from " + str(temp) + " to " + str(self.health))
                elif (self.SPELL_DATA[spellName]["support_class"] == 2):
                    self.addEffect(self.SPELL_DATA[spellName]["effect"])
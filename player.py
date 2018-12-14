import random
import json

class Player:
    VALID_SPELLS = ["small_fireball", "water_bullet", "cutting_wind", "rock_smash"]
    SPELL_DATA = {}

    usedSpells = []
    masteredSpells = []
    health = 100
    attribute = ""
    tier = 0
    maxHealth = 100
    maxMana = 10
    mana = 10
    effects = set()
    defensePoints = 0
    defensePercentage = 0
    tierUpgradeProgress = 0
    tierUpgradeRequirements = [5, 10, 20]
    PLAYER_MANA = [10, 15, 20, 25]
    PLAYER_HEALTH = [100, 110, 120, 150]

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
                if ((self.SPELL_DATA[spell]["tier"] == 0) & (self.SPELL_DATA[spell]["attribute"] == self.attribute) & (self.SPELL_DATA[spell]["type"] == "offense")):
                    possibleFirstSpells.append(spell)

        rand = random.randint(0, len(possibleFirstSpells) - 1)
        self.usedSpells.append(possibleFirstSpells[rand])

        print("Your attribute is: " + self.attribute)
        print("You have encountered: " + self.SPELL_DATA[self.usedSpells[0]]["game_name"] + " (Tier: 0)")

    def getHealth(self):
        return self.health

    def getAttribute(self):
        return self.attribute

    def getTier(self):
        return self.tier

    def getMana(self):
        return self.mana

    def getusedSpells(self):
        return self.usedSpells

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
            print("Player already has effect \"" + effectName + "\"")
        else:
            if ((effectName == "burn") & (self.hasEffect("abestos"))):
                print("Player has abestos!")
                return
            elif ((effectName == "poison") & (self.hasEffect("immunity"))):
                print("Player has immunity!")
                return
            self.effects.add([effectName, 3])
            print("Player has just been given the \"" + effectName + "\" effect")

    def setHealth(self, health):
        self.health = health

    def setMana(self, mana):
        self.mana = mana

    def statsReset(self):
        self.mana = 10
        self.health = 100
        self.effect = []

    def fightEnd(self):
        self.mana = self.maxMana
        self.effect = []

    def turnEnd(self):
        if (self.mana != self.maxMana)
            self.mana += 1
        self.processEffects()

        if ((self.tier != 4) & (self.tierUpgradeProgress == self.tierUpgradeRequirements[tier])):
            self.levelUp()

    def levelUp(self):
        self.tier += 1
        print("Player has just gained a tier and is now tier " + str(self.tier))
        tempH = self.maxHealth
        tempM = self.maxMana
        self.maxHealth = self.PLAYER_HEALTH[tier]
        self.maxMana = self.PLAYER_MANA[tier]
        self.health = ((self.health / tempH) * 100) * self.maxHealth
        self.mana = ((self.mana / tempM) * 100) * self.maxMana
        self.tierUpgradeProgress = 0

    #method to deduct health, defense points etc
    def processAttack(self, spellName, caster):
        tempP = self.defensePoints
        tempPe = self.defensePercentage

        attack = self.SPELL_DATA[spellName]["damage"]
        attack -= self.defensePoints
        if (attack < 0):
            self.defensePoints += attack * -1
            attack = 0
        attack = (attack / 100) * (100 - self.defensePercentage)

        if (tempP != self.defensePoints):
            print("Player's defense points have dropped from " + str(tempD) + " to " + str(self.defensePoints))
        if (tempPe != self.defensePercentage):
            print("Player's defense percentage has dropped from " + str(tempPe) + " to " + str(self.defensePercentage))

        multiplier = 1
        if not ((self.hasEffect("elemental_equality")) | (caster.hasEffect("elemental_equality"))):
            if ((caster.getAttribute() == "fire") & (self.attribute == "water")):
                multiplier /= 2
            elif ((caster.getAttribute() == "water") & (self.attribute == "fire")):
                multiplier *= 2
            elif ((caster.getAttribute() == "water") & (self.attribute == "earth")):
                multiplier /= 2
            elif ((caster.getAttribute() == "earth") & (self.attribute == "water")):
                multiplier *= 2
            elif ((caster.getAttribute() == "earth") & (self.attribute == "air")):
                multiplier /= 2
            elif ((caster.getAttribute() == "air") & (self.attribute == "earth")):
                multiplier *= 2
            elif ((caster.getAttribute() == "air") & (self.attribute == "fire")):
                multiplier /= 2
            elif ((caster.getAttribute() == "fire") & (self.attribute == "air")):
                multiplier *= 2
        elif ((self.hasEffect("elemental_dominance")) | (caster.hasEffect("elemental_dominance"))):
            if ((caster.getAttribute() == "fire") & (self.attribute == "water")):
                multiplier /= 4
            elif ((caster.getAttribute() == "water") & (self.attribute == "fire")):
                multiplier *= 4
            elif ((caster.getAttribute() == "water") & (self.attribute == "earth")):
                multiplier /= 4
            elif ((caster.getAttribute() == "earth") & (self.attribute == "water")):
                multiplier *= 4
            elif ((caster.getAttribute() == "earth") & (self.attribute == "air")):
                multiplier /= 4
            elif ((caster.getAttribute() == "air") & (self.attribute == "earth")):
                multiplier *= 4
            elif ((caster.getAttribute() == "air") & (self.attribute == "fire")):
                multiplier /= 4
            elif ((caster.getAttribute() == "fire") & (self.attribute == "air")):
                multiplier *= 4
        elif ((self.hasEffect("elemental_dominance")) & (caster.hasEffect("elemental_dominance"))):
            if ((caster.getAttribute() == "fire") & (self.attribute == "water")):
                multiplier /= 8
            elif ((caster.getAttribute() == "water") & (self.attribute == "fire")):
                multiplier *= 8
            elif ((caster.getAttribute() == "water") & (self.attribute == "earth")):
                multiplier /= 8
            elif ((caster.getAttribute() == "earth") & (self.attribute == "water")):
                multiplier *= 8
            elif ((caster.getAttribute() == "earth") & (self.attribute == "air")):
                multiplier /= 8
            elif ((caster.getAttribute() == "air") & (self.attribute == "earth")):
                multiplier *= 8
            elif ((caster.getAttribute() == "air") & (self.attribute == "fire")):
                multiplier /= 8
            elif ((caster.getAttribute() == "fire") & (self.attribute == "air")):
                multiplier *= 8

        if (caster.hasEffect("weakness")):
            multiplier /= 2
        elif (caster.hasEffect("strength")):
            multiplier *= 2
        
        temp = self.health
        self.health -= attack * multiplier

        if (temp == self.health):
            print("Player's health remained the same")
        else:
            print("Player's health dropped from " + str(temp) + " to " + str(self.health))
    
    #method to process bad effects
    def processEffects(self):
        for effect in self.effects:
            if (effect[1] == 0):
                self.effects.remove(effect)

            if (effect[0] == "burn"):
                if (self.hasEffect("abestos")):
                    print("\"burn\" was nullified by player's \"abestos\"")
                else:
                    self.health -= self.SPELL_DATA[effect[0]]["effect_value"]
                    print("Player's health dropped from " + str(self.SPELL_DATA[effect[0]]["effect_value"] + self.health) + " to " + str(self.health))
            elif (effect[0] == "poison"):
                if (self.hasEffect("immunity")):
                    print("\"burn\" was nullified by player's \"immunity\"")
                else:
                    self.health -= self.SPELL_DATA[effect[0]]["effect_value"]
                    print("Player's health dropped from " + str(self.SPELL_DATA[effect[0]]["effect_value"] + self.health) + " to " + str(self.health))
            effect[1] -= 1

    def processSpell(self, spellName):
        if not (spellName in self.usedSpells):
            self.usedSpells.append(spellName)

        self.mana -= self.SPELL_DATA[spellName]["mana_consumption"]

        multiplier = 1
        if (self.hasEffect("strength")):
            multiplier *= 2
        if (self.hasEffect("weakness")):
            multiplier /= 2

        if (self.SPELL_DATA[spellName]["type"] == "offense"):
            if not (self.isMasteredSpell(spellName)):
                rand = random.randint(0,99)
                if (rand > self.SPELL_DATA[spellName]["master_percentage"]):
                    self.addMasteredSpell(spellName)
                    print("You have mastered " + self.SPELL_DATA[spellName]["game_name"] + " (Tier: " + str(self.SPELL_DATA[spellName]["tier"]) + ")")
                else:
                    rand = random.randint(0,99)
                    if (rand > self.SPELL_DATA[spellName]["backfire_chance"]):
                        temp = self.health
                        self.health -= self.SPELL_DATA[spellName]["damage"] * multiplier
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
                            temp = self.defensePoints
                            self.defensePoints += self.SPELL_DATA[spellName]["defense_value"]
                            print("Player's defense points increased from " + str(temp) + " to " + str(self.defensePoints))
                        else:
                            temp = self.defensePercentage
                            self.defensePercentage += self.SPELL_DATA[spellName]["defense_value"]
                            if (self.defensePercentage > 100):
                                self.defensePercentage = 100
                                print("Player's defense percentage is at 100%! The next attack will be nullified!")
                            elif (temp == self.defensePercentage):
                                print("Player's defense percentage is already at 100%! The next attack will be nullified!")
                            else:
                                print("Player's defense percentage has risen from " + str(temp) + " to " + str(self.defensePercentage))
            else:
                if (self.SPELL_DATA[spellName]["defense_class"] == 1):
                    temp = self.defensePoints
                    self.defensePoints += self.SPELL_DATA[spellName]["defense_value"]
                    print("Player's defense points increased from " + str(temp) + " to " + str(self.defensePoints))
                else:
                    temp = self.defensePercentage
                    self.defensePercentage += self.SPELL_DATA[spellName]["defense_value"]
                    if (self.defensePercentage > 100):
                        self.defensePercentage = 100
                        print("Player's defense percentage is at 100%! The next attack will be nullified!")
                    elif (temp == self.defensePercentage):
                        print("Player's defense percentage is already at 100%! The next attack will be nullified!")
                    else:
                        print("Player's defense percentage has risen from " + str(temp) + " to " + str(self.defensePercentage))
        else:
            if not (self.isMasteredSpell(spellName)):
                rand = random.randint(0,99)
                if (rand > self.SPELL_DATA[spellName]["master_percentage"]):
                    self.addMasteredSpell(spellName)
                    print("You have mastered " + self.SPELL_DATA[spellName]["game_name"] + " (Tier: " + str(self.SPELL_DATA[spellName]["tier"]) + ")")
                    if (self.SPELL_DATA[spellName]["support_class"] == 1):
                        if (self.health == self.maxHealth):
                            print("Already at max health!")
                            else:
                                temp = self.health
                                self.health += self.SPELL_DATA[spellName]["heal_value"]
                                if (self.health > self.maxHealth):
                                    self.health = self.maxHealth
                                print("Health rose from " + str(temp) + " to " + str(self.health))
                    elif (self.SPELL_DATA[spellName]["support_class"] == 2):
                        self.addEffect(self.SPELL_DATA[spellName]["effect"])
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
                            if (self.health == self.maxHealth):
                                print("Already at max health!")
                            else:
                                temp = self.health
                                self.health += self.SPELL_DATA[spellName]["heal_value"]
                                if (self.health > self.maxHealth):
                                    self.health = self.maxHealth
                                print("Health rose from " + str(temp) + " to " + str(self.health))
                        elif (self.SPELL_DATA[spellName]["support_class"] == 2):
                            self.addEffect(self.SPELL_DATA[spellName]["effect"])
            else:
                if (self.SPELL_DATA[spellName]["support_class"] == 1):
                    if (self.health == self.maxHealth):
                                print("Already at max health!")
                            else:
                                temp = self.health
                                self.health += self.SPELL_DATA[spellName]["heal_value"]
                                if (self.health > self.maxHealth):
                                    self.health = self.maxHealth
                                print("Health rose from " + str(temp) + " to " + str(self.health))
                elif (self.SPELL_DATA[spellName]["support_class"] == 2):
                    self.addEffect(self.SPELL_DATA[spellName]["effect"])
        
        self.tierUpgradeProgress += 1
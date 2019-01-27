import random
import json

ENEMY_HEALTH = [100, 110, 120, 150]
ENEMY_MANA = [10, 15, 20, 25]

class Enemy:
    VALID_SPELLS = ["small_fireball", "water_bullet", "cutting_wind", "rock_smash", "healing_drop", "minor_phoenix_heal", "nourishing_mud", "refreshing_air"]
    SPELL_DATA = {}
    ARSENAL = []

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
                if ((data["tier"] <= self.tier) & (data["attribute"] == self.attribute)):
                    self.ARSENAL.append(spell)

        self.tier = random.randint(0,3)
        self.health = ENEMY_HEALTH[self.tier]
        self.mana = ENEMY_MANA[self.tier]
        self.maxHealth = ENEMY_HEALTH[self.tier]
        self.maxMana = ENEMY_MANA[self.tier]

    def getAttribute(self):
        return self.attribute

    def getHealth(self):
        return self.health

    def hasEffect(self, effectName):
        for effect in self.effects:
            if (effect[0] == effectName):
                return True

        return False

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
            self.mana += random.randint(1,2 + self.tier)
            if (self.mana > self.maxMana):
                self.mana = self.maxMana
        self.processEffects()

    def processAttack(self, spellName, caster):
        tempP = self.defensePoints
        tempPe = self.defensePercentage

        attack = self.SPELL_DATA[spellName]["damage"]
        attack -= self.defensePoints
        if (attack < 0):
            self.defensePoints += attack
            attack = 0
        attack = (attack / 100) * (100 - self.defensePercentage)

        if (tempP != self.defensePoints):
            print("Enemy's defense points have dropped from " + str(tempD) + " to " + str(self.defensePoints))
        if (tempPe != self.defensePercentage):
            print("Enemy's defense percentage has dropped from " + str(tempPe) + " to " + str(self.defensePercentage))

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
            print("Enemy's health remained the same")
        else:
            print("Enemy's health dropped from " + str(temp) + " to " + str(self.health))

    def processEffects(self):
        for effect in self.effects:
            if (effect[1] == 0):
                self.effects.remove(effect)

            if (effect[0] == "burn"):
                if (self.hasEffect("abestos")):
                    print("\"burn\" was nullified by Enemy's \"abestos\"")
                else:
                    self.health -= self.SPELL_DATA[effect[0]]["effect_value"]
                    print("Enemy's health dropped from " + str(self.SPELL_DATA[effect[0]]["effect_value"] + self.health) + " to " + str(self.health))
            elif (effect[0] == "poison"):
                if (self.hasEffect("immunity")):
                    print("\"burn\" was nullified by Enemy's \"immunity\"")
                else:
                    self.health -= self.SPELL_DATA[effect[0]]["effect_value"]
                    print("Enemy's health dropped from " + str(self.SPELL_DATA[effect[0]]["effect_value"] + self.health) + " to " + str(self.health))
            effect[1] -= 1

    def chooseSpell(self):
        #basic spell choosing
        return random.choice(self.ARSENAL)

    def processSpell(self, spellName):
        self.mana -= self.SPELL_DATA[spellName]["mana_consumption"]

        multiplier = 1
        if (self.hasEffect("strength")):
            multiplier *= 2
        if (self.hasEffect("weakness")):
            multiplier /= 2

        if (self.SPELL_DATA[spellName]["type"] == "offense"):
            rand = random.randint(0,99)
            if (rand > self.SPELL_DATA[spellName]["backfire_chance"]):
                temp = self.health
                self.health -= self.SPELL_DATA[spellName]["damage"] * multiplier
                print(self.SPELL_DATA[spellName] + " backfired!")
                print("Health dropped from " + str(temp) + " to " + str(self.health))
        elif (self.SPELL_DATA[spellName]["type"] == "defense"):
            rand = random.randint(0,99)
            if (rand > self.SPELL_DATA[spellName]["backfire_chance"]):
                print(self.SPELL_DATA[spellName] + " backfired!")
            else:
                if (self.SPELL_DATA[spellName]["defense_class"] == 1):
                    temp = self.defensePoints
                    self.defensePoints += self.SPELL_DATA[spellName]["defense_value"]
                    print("Enemy's defense points increased from " + str(temp) + " to " + str(self.defensePoints))
                else:
                    temp = self.defensePercentage
                    self.defensePercentage += self.SPELL_DATA[spellName]["defense_value"]
                    if (self.defensePercentage > 100):
                        self.defensePercentage = 100
                        print("Enemy's defense percentage is at 100%! The next attack will be nullified!")
                    elif (temp == self.defensePercentage):
                        print("Enemy's defense percentage is already at 100%! The next attack will be nullified!")
                    else:
                        print("Enemy's defense percentage has risen from " + str(temp) + " to " + str(self.defensePercentage))
        else:
            rand = random.randint(0,99)
            if (rand > self.SPELL_DATA[spellName]["backfire_chance"]):
                print(self.SPELL_DATA[spellName] + " backfired!")
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
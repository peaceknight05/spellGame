#IMPORTS
import random
import time
import json
import speech_recognition as sr
from player import Player
from enemy import Enemy

#SHORTHANDS
recognizer = sr.Recognizer()
microphone = sr.Microphone()

#each spell has its own json file
"""
FORMAT:
game_name -> string
atrribute (aka element) -> string (fire, water, air, earth)
tier -> int (0-4)
type -> string (offense, defense, support)
damage -> int (ignored if not offense type)
defense_class -> int (1-2, 1 = subtraction, 2 = percentage, nullification is percentage but 100%, ignored if not defense type)
defense_value -> int (value to divide or subtract by, ignored if not defense type)
support_class -> int (1-3, 1 = healing, 2 = good effects, 3 = bad effects, ignored if type is not support)
heal_value -> int (ignored if not support class 1)
effect -> string (ignored if not good or bad effect support class)
effect_value -> int (ignored if not support class or not needed)
backfire_chance -> int (chance to backfire if not yet mastered)
master_percentage -> int (chance to be mastered upon use)
mana_consumption -> int (amount of mana consumed)
"""

#list of effect
"""
GOOD:
elemental_equality -> lessens attribute effects
immunity -> immune to poison
strength -> multiplies damage done
abestos -> immune to burn
BAD:
burn -> does fire damage over time
poison -> does damage over time
weakness -> reduces damage done
elemental_dominance -> maximises attribute effects
"""

#GLOBAL VARIABLES
VALID_SPELLS = ["small_fireball", "water_bullet", "cutting_wind", "rock_smash", "healing_drop", "minor_phoenix_heal", "nourishing_mud", "refreshing_air"]
SPELL_DATA = {}
THE_PLAYER = Player()

#FUNCTION FOR GETTING A SPOKEN SPELL
def getSpokenSpell():
    rawSpeech = ""

    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Ready")
            audio = recognizer.listen(source)

        rawSpeech = recognizer.recognize_google(audio).split(" ")        
    except:
        print("Sorry, I couldn't get what you said. Please try again.")
        getSpokenSpell()

    for word in rawSpeech:
        rawSpeech[rawSpeech.index(word)] = word.lower()

    #pronunced grim-muah
    if (" ".join(rawSpeech) == "open grimoire"):
        for spell in THE_PLAYER.getusedSpells():
            print(SPELL_DATA[spell]["game_name"] + " (Tier: " + str(SPELL_DATA[spell]["tier"]) + ")")
        time.sleep(5)
        getSpokenSpell()

    spellName = "_".join(rawSpeech)
        
    if not (spellName in VALID_SPELLS):
        print(spellName + " is not a valid spell. Please try again.")
        getSpokenSpell()
    elif (THE_PLAYER.isCastableSpell(spellName)):
        return spellName
    else:
        print("You have not unlocked " + SPELL_DATA[spellName]["game_name"] + " (Tier: " + str(SPELL_DATA[spellName]["tier"]) + ")" + " yet. Please try again.")
        getSpokenSpell()

def castSpell(spellName, caster, target = THE_PLAYER):
    if (caster == THE_PLAYER):
        print("You cast: " + SPELL_DATA[spellName]["game_name"] + " (Tier: " + str(SPELL_DATA[spellName]["tier"]) + ")")
        THE_PLAYER.processSpell(spellName)
        if (target == None):
            return
        else:
            target.processAttack(spellName, caster)
    else:
        print("Opponent cast: " + SPELL_DATA[spellName]["game_name"] + " (Tier: " + str(SPELL_DATA[spellName]["tier"]) + ")")
        caster.processSpell(spellName)
        THE_PLAYER.processAttack(spellName, caster)

#LOADING SPELLS
for spell in VALID_SPELLS:
    with open("spells/" + spell + ".json", "r") as spellFile:
        data = json.load(spellFile)
        SPELL_DATA[spell] = data

#TUTORIAL
print("Greetings, young mage.")
time.sleep(1)
print("Try casting a spell.")
time.sleep(1)
print("Do wait for the word \"Ready\" to pop up first.")
castedSpell = getSpokenSpell()
castSpell(castedSpell, THE_PLAYER, None)
THE_PLAYER.statsReset()
time.sleep(1)
print("Well then, I think I'm done here so I'll be off.")
time.sleep(1)
print("Try to tier up as quick as possible to be able to use more spells.")
time.sleep(1)
print("Feel free to copy your opponent's spells if you are of a higher or equal tier and share the same attribute.")
time.sleep(1)
print("Beware of backfires though, at best you will waste your mana, at worse you will be severely inflicted by your own spell!")
time.sleep(1)
print("Don't forget, you can always use \"Open Grimoire\" (grim-muah) to get a list of spells you've used before")
time.sleep(10)
print("Good luck!")

#GAME
enemyCount = 0
points = 0
while (THE_PLAYER.getHealth() > 0):
    THE_ENEMY = Enemy()
    enemyCount += 1
    while ((THE_PLAYER.getHealth() > 0) & (THE_ENEMY.getHealth() > 0)):
        
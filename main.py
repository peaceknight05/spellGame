#IMPORTS
import random
import time
import json
import os
import speech_recognition as sr
from player import Player

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
effect_value -> int (ignored if not good or bad effect support class)
backfire_chance -> int (chance to backfire if not yet mastered)
master_percentage -> int (chance to be mastered upon use)
mana_consumption -> int (amount of mana consumed)
"""

#GLOBAL VARIABLES
VALID_SPELLS = ["small_fireball", "water_bullet", "cutting_wind", "rock_smash"]
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
        
    if not ("_".join(rawSpeech) in VALID_SPELLS):
        print(" ".join(rawSpeech) + " is not a valid spell. Please try again.")
        getSpokenSpell()
    elif (THE_PLAYER.inUnlockedSpell("_".join(rawSpeech))):
        return "_".join(rawSpeech)
    else:
        print("You have not unlocked " + SPELL_DATA["_".join(rawSpeech)]["game_name"] + " (Tier " + str(SPELL_DATA["_".join(rawSpeech)]["tier"]) + ")" + " yet. Please try again.")
        getSpokenSpell()

#LOADING SPELLS
for spell in VALID_SPELLS:
    with open("spells/" + spell + ".json", "r") as spellFile:
        data = json.load(spellFile)
        SPELL_DATA[spell] = data

spokenSpell = getSpokenSpell()
spellName = SPELL_DATA[spokenSpell]["game_name"]
spellTier = SPELL_DATA[spokenSpell]["tier"]
print("\nYOU CAST:")
print(spellName + " (Tier " + str(spellTier) + ")")
os.system("say you cast " + spellName)
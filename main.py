from characters import get_character, char_to_prompt
from engine import ask, validate
from chat import chat
from context import create_context
from world import jujutsu

char_select = input("WHO IS PRESENT?\n").split(",")
user_char = input("WHO ARE YOU?\n")
scene = input("WHAT IS THE SCENE?")

with open("jujutsu.txt", "r") as f:
    world_rules = f.read()


characters = [get_character(name) for name in char_select]
world_rules = jujutsu
context = create_context(characters = characters, user_character = user_char, scene = scene, world_rules= world_rules)
chat(context)
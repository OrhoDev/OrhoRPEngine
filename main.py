from characters import get_character, char_to_prompt
from engine import ask, validate
from chat import chat
from context import create_context
from world import jujutsu_world

char_select = input("WHO IS PRESENT?\n").split(",")
user_char = input("WHO ARE YOU?\n")
scene = input("WHAT IS THE SCENE?\n")


characters = [get_character(name.strip()) for name in char_select]
world_rules = jujutsu_world
context = create_context(characters = characters, user_character = user_char, scene = scene, world_rules= jujutsu_world)
chat(context)
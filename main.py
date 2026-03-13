from characters import characters, get_character, char_to_prompt
from chat import chat
from context import create_context
from world import JUJUTSU_WORLD

mode = input("MODE? (local/api)\n").strip().lower()

if mode == "api":
    from engine_groq import ask, validate
else:
    from engine_local import ask, validate

char_select = input("WHO IS PRESENT?\n").split(",")
user_char = input("WHO ARE YOU?\n")
scene = input("WHAT IS THE SCENE?\n")

characters = [get_character(name.strip()) for name in char_select]
user_character = get_character(user_char.strip())
if user_character and user_character not in characters:
    characters.append(user_character)

world_rules = JUJUTSU_WORLD
context = create_context(characters = characters, user_character = user_char, scene = scene, world_rules= JUJUTSU_WORLD)
chat(context)
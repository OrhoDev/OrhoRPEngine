import sys
import os
from pathlib import Path


sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "engine"))

from engine.state_manager import StateManager
from engine.context import create_context
from engine.chat import chat

def boot_sequence():
    print("RPG ENGINE")
    world_select = input("LOAD WORLD (default: jjk): \n").strip().lower() or "jjk"
    

    state = StateManager(world_name=world_select)
    if not state.world_rules:
        print(f"World '{world_select}' not found or missing world.json.")
        return

    mode = input("MODE? (local/api) [default: api]: \n").strip().lower() or "api"
    
    char_select = input("WHO IS PRESENT? (comma separated): \n").split(",")
    user_char = input("WHO ARE YOU?: \n").strip()
    scene = input("WHAT IS THE SCENE?: \n").strip()


    active_characters =[]
    for name in char_select:
        if not name.strip():
            continue
            
        char_data = state.get_character(name)
        if char_data:
            active_characters.append(char_data)
        else:
            print(f"Character '{name.strip()}' not found in {world_select} database.")

    user_character_data = state.get_character(user_char)
    if user_character_data and user_character_data not in active_characters:
        active_characters.append(user_character_data)

    
    context = create_context(
        state_manager=state,
        characters=active_characters,
        user_character=user_char,
        scene=scene,
        mode=mode
    )
    
    print("\n")
    chat(context)

if __name__ == "__main__":
    boot_sequence()
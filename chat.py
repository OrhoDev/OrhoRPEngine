# --- IN chat.py ---
import re
from context import add_to_pinned, create_context, add_to_history, build_prompt, get_active_character, save_session, load_session, unpin
from characters import characters as characters_db
from techniques import TECHNIQUES_DB

# Dynamic engine import based on mode
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from engine_groq import ask, validate
    ENGINE_MODE = "api"
except ImportError:
    from engine_local import ask, validate
    ENGINE_MODE = "local"

def is_combat_move(user_input):
    clean_input = user_input.lower().replace("!", "").replace(".", "").strip()
    clean_input = clean_input.strip("*").strip('"')
    
    # Try to extract technique name from quotes first
    import re
    quoted_match = re.search(r'"([^"]+)"', user_input)
    if quoted_match:
        extracted_tech = quoted_match.group(1).strip().lower()
        for tech_name in TECHNIQUES_DB.keys():
            if tech_name.lower() == extracted_tech:
                return True, tech_name
    
    # If no quotes found, try exact match with cleaned input
    for tech_name in TECHNIQUES_DB.keys():
        if tech_name.lower() == clean_input.strip().lower():
            return True, tech_name
            
    return False, None

def is_technique_allowed(tech_name, character):
    """Checks if the technique exists in either base or unlocked lists."""
    if character is None:
        return False
    
    # Ensure character has the required structure
    base_techniques = character.get("base_techniques", [])
    state = character.get("state", {})
    unlocked_techniques = state.get("unlocked_techniques", [])
    
    # Combine both lists so the Referee knows both are valid
    all_allowed = base_techniques + unlocked_techniques
    
    # Use exact case-insensitive matching for the "Activation Phrase"
    if any(tech.lower() == tech_name.lower() for tech in all_allowed):
        return True
    return False


def _resolve_character(name):
    """Resolve name to a character from the full database (by key or by character name)."""
    if not name:
        return None
    name = name.strip()
    key = name.lower()
    if key in characters_db:
        return characters_db[key]
    for c in characters_db.values():
        if c["name"].lower() == key:
            return c
    return None


def chat(context):
    while True:
        user_input = input("\nUser: ")
        
        # If user just hits enter, trigger an "Engine Tick"
        if not user_input.strip():
            user_input = "[NPC_TURN_TICK]"
        
        if user_input.startswith("/"):
            result = handle_command(user_input, context)
            if isinstance(result, dict):
                context = result
            elif result is True:
                break
            continue

        # --- THE REFEREE LAYER ---
        is_combat, tech_name = is_combat_move(user_input)
        
        if is_combat:
            active_char = get_active_character(context, context['user_character'])
            if active_char is None:
                print(f"\n[Referee]: Character '{context['user_character']}' not found in scene.")
                continue
            if not is_technique_allowed(tech_name, active_char):
                print(f"\n[Referee]: ACCESS DENIED. {active_char['name']} has not unlocked '{tech_name}'.")
                continue # Kills the turn here, LLM never sees the illegal move

        # --- THE RENDERER LAYER (LLM) ---
        prompt = build_prompt(context, user_input)
        raw_response = ask(prompt, context["system"])
        print(f"\n--- DEBUG: RAW RESPONSE ---\n{raw_response}\n---------------------------") # ADD THIS
        
        analysis_match = re.search(r"<analysis>(.*?)</analysis>", raw_response, re.DOTALL)
        narration_match = re.search(r"<narration>(.*?)</narration>", raw_response, re.DOTALL)
        world_update_match = re.search(r"<world_update>(.*?)</world_update>", raw_response, re.DOTALL)

        # Parse world state updates
        if world_update_match:
            world_update = world_update_match.group(1).strip()
            if world_update and world_update.lower() != "none":
                if context["world_state"]:
                    context["world_state"] += f"\n{world_update}"
                else:
                    context["world_state"] = world_update

        # NEW: Always print the Engine's internal logic so you can monitor it
        if analysis_match:
            print(f"\n[ENGINE LOGIC]:\n{analysis_match.group(1).strip()}")

        # Tightened check: Only look at verdict line
        verdict_match = re.search(r"Verdict:\s*(VALID|INVALID)", analysis_match.group(1)) if analysis_match else None
        if not verdict_match or verdict_match.group(1) != "VALID":
            print("\n[Engine] Blocked: action ruled INVALID.")
            continue

        if narration_match:
            final_output = narration_match.group(1).strip()
        else:
            final_output = "(No narration block returned.)"

        print(f"\n[NARRATION]:\n{final_output}")
        add_to_history(context, user_input)
        add_to_history(context, final_output)
        

def handle_command(user_input, context):
    parts = user_input.split(" ", 1)
    command = parts[0]
    rest = parts[1].strip() if len(parts) > 1 else ""
    arg_parts = rest.split(" ", 1)
    arg1 = arg_parts[0] if arg_parts else None
    arg2 = arg_parts[1] if len(arg_parts) > 1 else None

    if command == "/add":
        char = _resolve_character(rest)
        if char is None:
            print(f"Unknown character: {rest}")
            return
        if get_active_character(context, char["name"]):
            print(f"{char['name']} is already in the scene.")
            return
        context["characters"].append(char)
        print(f"Added {char['name']} to the scene.")
        return
    if command == "/remove":
        char = _resolve_character(rest)
        if char is None:
            print(f"Unknown character: {rest}")
            return
        existing = get_active_character(context, char["name"])
        if not existing:
            print(f"{char['name']} is not in the scene.")
            return
        context["characters"].remove(existing)
        print(f"Removed {char['name']} from the scene.")
        return
    if command == "/scene":
        context["scene"] = rest or ""
        print("Scene updated.")
        return

    if command == "/unlock":
        character = get_active_character(context, arg2)
        if character and arg1 not in character["state"]["unlocked_techniques"]:
            character["state"]["unlocked_techniques"].append(arg1)
            print(f"Unlocked {arg1} for {character['name']}!")
        elif character:
            print(f"{character['name']} already has that technique.")
        else:
            print("Character not in scene.")
    elif command == "/condition":
        character = get_active_character(context, arg2)
        if character:
            character["state"]["conditions"].append(arg1)
    elif command == "/length":
        context["response_length"] = arg1
        print(f"Response length set to: {arg1}")
    elif command == "/exit":
        print("Bye!")
        return True
    elif command == "/save":
        save_session(context)
    elif command == "/load":
        return load_session()
    elif command == "/pin":
        add_to_pinned(context, rest)
    elif command == "/unpin":
        if context["important"]:
            removed = context["important"].pop()
            print(f"Unpinned {removed}")



        

# --- IN chat.py ---
import re
from context import add_to_pinned, create_context, add_to_history, build_prompt, get_active_character, save_session, load_session, unpin
from engine import ask
from characters import characters as characters_db
from techniques import TECHNIQUES_DB

def is_combat_move(user_input):
    """Checks if the user input contains any technique name from the DB."""
    for tech_name in TECHNIQUES_DB.keys():
        if tech_name.lower() in user_input.lower():
            return True, tech_name
    return False, None

def is_technique_allowed(tech_name, character):
    """Checks if the technique exists in the character's unlocked list."""
    allowed = character["state"]["unlocked_techniques"]
    # We check if the technique found in the input is in the unlocked list
    if tech_name in allowed:
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
            if not is_technique_allowed(tech_name, active_char):
                print(f"\n[Referee]: ACCESS DENIED. {active_char['name']} has not unlocked '{tech_name}'.")
                continue # Kills the turn here, LLM never sees the illegal move

        # --- THE RENDERER LAYER (LLM) ---
        prompt = build_prompt(context, user_input)
        raw_response = ask(prompt, context["system"])

        analysis_match = re.search(r"<analysis>(.*?)</analysis>", raw_response, re.DOTALL)
        narration_match = re.search(r"<narration>(.*?)</narration>", raw_response, re.DOTALL)

        if not analysis_match or "VALID" not in analysis_match.group(1):
            print("\n[Engine] Blocked: analysis did not contain VALID. Turn not applied.")
            if analysis_match:
                print(f"[Analysis]: {analysis_match.group(1).strip()[:200]}...")
            continue

        if narration_match:
            final_output = narration_match.group(1).strip()
        else:
            final_output = "(No narration block returned.)"

        print(f"\n{final_output}")
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



        

import re
from context import (add_to_pinned, add_to_history,
                     build_prompt, build_decision_prompt,
                     save_session, load_session, unpin, SYSTEM_PROMPTS,
                     _detect_tier, _update_seen_techniques)

import sys
import os

try:
    from engine_groq import ask, validate
    ENGINE_MODE = "api"
except ImportError:
    from engine_local import ask, validate
    ENGINE_MODE = "local"

def is_combat_move(user_input, context):
    state = context["state_manager"]
    clean_input = user_input.lower().replace("!", "").replace(".", "").strip()
    clean_input = clean_input.strip("*").strip('"')

    quoted_match = re.search(r'"([^"]+)"', user_input)
    if quoted_match:
        extracted_tech = quoted_match.group(1).strip().lower()
        for tech_name in state.techniques.keys():
            if tech_name.lower() == extracted_tech:
                return True, tech_name

    for tech_name in state.techniques.keys():
        if tech_name.lower() in clean_input:
            return True, tech_name

    return False, None

def is_technique_allowed(tech_name, character):
    if character is None:
        return False
    base_techniques = character.get("base_techniques",[])
    unlocked_techniques = character.get("state", {}).get("unlocked_techniques",[])
    all_allowed = base_techniques + unlocked_techniques
    return any(tech.lower() == tech_name.lower() for tech in all_allowed)

def chat(context):
    state = context["state_manager"]
    
    while True:
        user_input = input("\nUser: ")

        if not user_input.strip():
            user_input = "[NPC_TURN_TICK]"

        if user_input.startswith("/"):
            result = handle_command(user_input, context)
            if isinstance(result, dict):
                context = result
            elif result is True:
                break
            continue

        is_combat, tech_name = is_combat_move(user_input, context)
        if is_combat:
            active_char = state.get_character(context['user_character'])
            if active_char is None:
                print(f"\n[Referee]: Character '{context['user_character']}' not found in scene.")
                continue
            if not is_technique_allowed(tech_name, active_char):
                print(f"\n[Referee]: ACCESS DENIED. {active_char['name']} has not unlocked '{tech_name}'.")
                continue


        referee_prompt = build_prompt(context, user_input) + \
            "\n\n[LOGIC CHECK]: Analyze mechanical validity of user's action against provided rules. Do not narrate. Output VALID or INVALID: [Reason]."
        verdict = ask(referee_prompt, "You are a logic engine. Output only VALID or INVALID followed by a reason.")

        if "INVALID" in verdict.upper():
            failure_prompt = build_prompt(context, user_input) + \
                f"\n[INSTRUCTION]: The user's action is mechanically impossible. Narrate the attempt and failure only. Technical reason: {verdict}"
            response = ask(failure_prompt, context["system"])
        else:
        
            npc_decisions = ask(
                build_decision_prompt(context, user_input),
                SYSTEM_PROMPTS["decision"]
            )


            tier = _detect_tier(user_input, context)
            few_shot = state.examples.get(tier)
            narration_prompt = build_prompt(context, user_input, npc_decisions=npc_decisions)
            response = ask(narration_prompt, context["system"], few_shot=few_shot)

        narration_match = re.search(r"<narration>(.*?)</narration>", response, re.DOTALL)
        world_update_match = re.search(r"<world_update>(.*?)</world_update>", response, re.DOTALL)

        if world_update_match:
            world_update = world_update_match.group(1).strip()
            if world_update and world_update.lower() != "none":
                context["world_state"] = (context["world_state"] + "\n" + world_update).strip()

        final_output = narration_match.group(1).strip() if narration_match else "(No narration block returned.)"
        print(f"\n[NARRATION]:\n{final_output}")

        _update_seen_techniques(user_input, context)
        add_to_history(context, user_input)
        add_to_history(context, final_output)

def handle_command(user_input, context):
    state = context["state_manager"]
    parts = user_input.split(" ", 1)
    command = parts[0]
    rest = parts[1].strip() if len(parts) > 1 else ""
    arg_parts = rest.split(" ", 1)
    arg1 = arg_parts[0] if arg_parts else None
    arg2 = arg_parts[1] if len(arg_parts) > 1 else None

    if command == "/add":
        char = state.get_character(rest)
        if char is None:
            print(f"Unknown character: {rest} in world '{state.world_name}'")
            return
        

        if any(c["name"].lower() == char["name"].lower() for c in context["characters"]):
            print(f"{char['name']} is already in the scene.")
            return
            
        context["characters"].append(char)
        print(f"Added {char['name']} to the scene.")
        return
        
    elif command == "/remove":
        char = state.get_character(rest)
        if char is None:
            print(f"Unknown character: {rest}")
            return
            
        for c in context["characters"]:
            if c["name"].lower() == char["name"].lower():
                context["characters"].remove(c)
                print(f"Removed {char['name']} from the scene.")
                return
        print(f"{char['name']} is not in the scene.")
        return
        
    elif command == "/scene":
        context["scene"] = rest or ""
        print("Scene updated.")
        return
        
    elif command == "/unlock":
        character = state.get_character(arg2)
        if character:
     
            for c in context["characters"]:
                if c["name"].lower() == character["name"].lower():
                    if arg1 not in c["state"]["unlocked_techniques"]:
                        c["state"]["unlocked_techniques"].append(arg1)
                        print(f"Unlocked {arg1} for {c['name']}!")
                    else:
                        print(f"{c['name']} already has that technique.")
                    return
        print("Character not in scene.")
        
    elif command == "/condition":
        character = state.get_character(arg2)
        if character:
            for c in context["characters"]:
                if c["name"].lower() == character["name"].lower():
                    c["state"]["conditions"].append(arg1)
                    print(f"Added condition '{arg1}' to {c['name']}.")
                    return
                    
    elif command == "/length":
        context["response_length"] = arg1
        print(f"Response length set to: {arg1}")
        
    elif command == "/exit":
        print("Shutting down engine...")
        return True
        
    elif command == "/save":
        save_session(context)
        print("Session saved.")
        
    elif command == "/load":
        print("Session loaded.")
        return load_session()
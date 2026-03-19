import json
import re
from context import (add_to_pinned, add_to_history,
                     build_prompt, build_decision_prompt, get_active_character,
                     save_session, load_session, unpin, SYSTEM_PROMPTS,
                     _detect_tier, _update_seen_techniques)

import sys
import os
from engine_local import ask as ask_local

try:
    from engine_groq import ask, validate
    ENGINE_MODE = "api"
except ImportError:
    from engine_local import ask, validate
    ENGINE_MODE = "local"


def clean_json_output(raw_string):
    """Strips markdown formatting and parses JSON safely."""
    clean_str = raw_string.strip()
    if clean_str.startswith("```json"):
        clean_str = clean_str[7:]
    if clean_str.startswith("```"):
        clean_str = clean_str[3:]
    if clean_str.endswith("```"):
        clean_str = clean_str[:-3]
    try:
        return json.loads(clean_str.strip())
    except json.JSONDecodeError:
        return None

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


def calculate_tech_cost(tech_name, character, config):
    math_cfg = config.get("system_math", {})
    tiers = math_cfg.get("ability_tiers",[])
    
    cost, cd = 0, 0
    lower_tech = tech_name.lower()
  
    for tier in tiers:
        triggers = tier.get("triggers",[])
        if not triggers or "" in triggers: 
            cost = tier.get("cost", 10)
            cd = tier.get("cooldown", 0)
            break
        if any(t.lower() in lower_tech for t in triggers):
            cost = tier.get("cost", 10)
            cd = tier.get("cooldown", 0)
            break
            
    # 2. Apply character-specific trait multipliers (e.g. Six Eyes = 0 cost)
    all_techs = character.get("base_techniques", []) + character.get("state", {}).get("unlocked_techniques",[])
    overrides = math_cfg.get("trait_overrides", {})
    multiplier = 1.0
    for tech in all_techs:
        if tech in overrides:
            multiplier *= overrides[tech].get("energy_multiplier", 1.0)
            
    return int(cost * multiplier), cd

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
        math_cfg = state.config.get("system_math", {})
        e_name = math_cfg.get("energy_stat", "MP")

        # --- SAFE COMBAT MATH CHECK ---
        is_combat, tech_name = is_combat_move(user_input, context)
        if is_combat:
            active_char = get_active_character(context, context['user_character'])
            
            # CRITICAL FIX 1: Check if the character exists BEFORE checking their stats!
            if active_char is None:
                print(f"\n[Referee]: Character '{context['user_character']}' not found in scene.")
                continue
                
            if not is_technique_allowed(tech_name, active_char):
                print(f"\n[Referee]: ACCESS DENIED. {active_char['name']} has not unlocked '{tech_name}'.")
                continue

            cost, cd = calculate_tech_cost(tech_name, active_char, state.config)
            cooldowns = active_char["state"]["cooldowns"]
            stats = active_char["state"]["stats"]
            current_statuses = active_char["state"].get("status_effects", {})
            # Add 'incapacitated' to the blockers list
            blockers =["stunned", "burnout", "paralyzed", "unconscious", "frozen", "incapacitated"]
            active_blockers = [s for s in current_statuses if s.lower() in blockers]

            if active_blockers:
                print(f"\n[Referee]: ACCESS DENIED. {active_char['name']} is {active_blockers[0]} and cannot act.")
                continue

            if cooldowns.get(tech_name, 0) > 0:
                print(f"\n[Referee]: ACCESS DENIED. '{tech_name}' is on cooldown for {cooldowns[tech_name]} more turns.")
                continue
                
            if stats["energy"] < cost:
                print(f"\n[Referee]: ACCESS DENIED. '{tech_name}' requires {cost} {e_name}. You only have {stats['energy']}.")
                continue
                
            # Valid! Deduct cost and apply cooldown
            stats["energy"] -= cost
            if cd > 0:
                cooldowns[tech_name] = cd

        # --- INIT TOKEN TRACKERS ---
        context.setdefault("total_prompt_tokens", 0)
        context.setdefault("total_completion_tokens", 0)
        turn_p_tokens = 0
        turn_c_tokens = 0

        # --- CRITICAL FIX 3: TOKEN EFFICIENT VALIDATION ---
        # Instead of sending the 5000-token mechanics block to the Referee, we just send a list of the user's moves!
        user_char_val = get_active_character(context, context['user_character'])
        if user_char_val:
            user_techs = user_char_val.get("base_techniques",[]) + user_char_val.get("state", {}).get("unlocked_techniques",[])
            user_tech_summary = ", ".join(user_techs) if user_techs else "Basic Melee"
        else:
            user_tech_summary = "None"
            
        world_rules_str = json.dumps(state.world_rules)

        # CRITICAL FIX 2: Safely unpack the tuple!
        verdict, v_p, v_c = validate(user_input, world_rules_str, context["scene"], user_tech_summary)
        turn_p_tokens += v_p
        turn_c_tokens += v_c

        if "INVALID" in verdict.upper():
            failure_prompt = build_prompt(context, user_input) + \
                f"\n[INSTRUCTION]: The user's action is mechanically impossible. Narrate the attempt and failure only. Technical reason: {verdict}"
            response, p, c = ask(failure_prompt, context["system"])
            turn_p_tokens += p; turn_c_tokens += c
            
            npc_decisions = "" # No NPC actions if user failed
        else:
            npc_decisions_raw, p, c = ask(
                build_decision_prompt(context, user_input),
                SYSTEM_PROMPTS["decision"]
            )
            turn_p_tokens += p; turn_c_tokens += c

            parsed_decisions = clean_json_output(npc_decisions_raw)
            if not parsed_decisions:
                print("\n[SYSTEM WARNING]: Decision Engine output malformed JSON. Defaulting to passive state.")
                npc_decisions = "NPCs hold their positions and observe."
            else:
                npc_decisions = json.dumps(parsed_decisions, indent=2)
                for npc_name, decision in parsed_decisions.items():
                    if npc_name == "environment_event": continue
                    npc_char = get_active_character(context, npc_name)
                    if npc_char and "action" in decision:
                        npc_is_combat, npc_tech = is_combat_move(decision["action"], context)
                        if npc_is_combat and npc_tech:
                            cost, cd = calculate_tech_cost(npc_tech, npc_char, state.config)
                            npc_char["state"]["stats"]["energy"] -= cost
                            if cd > 0:
                                npc_char["state"]["cooldowns"][npc_tech] = cd

            tier = _detect_tier(user_input, context)
            few_shot = state.examples.get(tier)
            narration_prompt = build_prompt(context, user_input, npc_decisions=npc_decisions)
            
            response, p, c = ask(narration_prompt, context["system"], few_shot=few_shot)
            turn_p_tokens += p; turn_c_tokens += c

        # --- UPDATE SESSION TOKENS ---
        context["total_prompt_tokens"] += turn_p_tokens
        context["total_completion_tokens"] += turn_c_tokens
        print(f"\n[TOKEN STATS] Turn Cost: {turn_p_tokens} P / {turn_c_tokens} C | Session Total: {context['total_prompt_tokens'] + context['total_completion_tokens']}")

        narration_match = re.search(r"<narration>(.*?)</narration>", response, re.DOTALL)
        world_update_match = re.search(r"<world_update>(.*?)</world_update>", response, re.DOTALL)

        scene_update_match = re.search(r"<scene_update>(.*?)</scene_update>", response, re.DOTALL)
        if scene_update_match:
            new_scene = scene_update_match.group(1).strip()
            if new_scene and new_scene.lower() != "none":
                context["scene"] = new_scene
                print(f"\n[SCENE SHIFT]: {new_scene}")


        if world_update_match:
            world_update_raw = world_update_match.group(1).strip()
            
            if world_update_raw and world_update_raw.lower() != "none":
  
                context["world_state"] = (context["world_state"] + "\n" + world_update_raw).strip()

      
                updates = re.split(r'[\n.]', world_update_raw)
                for update in updates:
                    if ":" in update:
                        parts = update.split(":", 1)
                        char_name = parts[0].strip()
                        new_condition = parts[1].strip()

                        if char_name and new_condition:
                            target_char = get_active_character(context, char_name)
                            if target_char:
                                if new_condition not in target_char["state"]["conditions"]:
                                    target_char["state"]["conditions"].append(new_condition)
                                    print(f"  [+] MEMORY INJECTED: {target_char['name']} -> '{new_condition}'")

        


    
        context["turn_count"] += 1
        
        if context["turn_count"] % 4 == 0 and len(context["world_state"].split('\n')) > 3:
            print("\n[SYSTEM LOG]: World State bloated. Triggering Local Memory Compactor...")
            
            compactor_system = """You are a background data-compression engine for a simulation. 
Your job is to read a list of world updates and compress them into a single, dense, factual paragraph.
RULES:
1. Remove redundancies.
2. Consolidate character statuses.
3. Do not write a story. Write a clinical status report.
4. Output ONLY the compressed summary."""

            compactor_prompt = f"CURRENT RAW STATE LOG:\n{context['world_state']}\n\nCompress this data."
            
            try:
                compressed_state, p, c = ask_local(compactor_prompt, compactor_system)
                context["total_prompt_tokens"] += p
                context["total_completion_tokens"] += c
                if compressed_state and "error" not in compressed_state.lower():
                    context["world_state"] = compressed_state.strip()
            except Exception as e:
                print(f"  >[SYSTEM LOG]: Local compactor unavailable, skipping compression. Error: {e}")

        # --- AGENTIC COMMANDS (ROBUST CATCH) ---
        # Catches standard [SYS_COMMAND: /cmd args]
        sys_command_matches = re.findall(r"\[SYS_COMMAND:\s*(.*?)\]", response)
        
        # Failsafe: Catches rogue unbracketed commands like "/damage 30 Geto" floating in the text
        # Tightened regex to stop before brackets or trailing punctuation
        rogue_matches = re.findall(r"(/(?:damage|heal|spawn|condition|scene|add|remove)\s+[0-9a-zA-Z_: ]+)", response)
        
        all_commands = sys_command_matches + rogue_matches
        
        if all_commands:
            print("\n[AI SYSTEM EVENT DETECTED]")
            for cmd in all_commands:
                # Clean up any trailing punctuation from rogue matches
                clean_cmd = cmd.strip(' .,"\'')
                print(f"  > Executing Agent Command: {clean_cmd}")
                handle_command(clean_cmd, context)

        final_output = narration_match.group(1).strip() if narration_match else "(No narration block returned.)"

        # --- THE LOOPBACK GLITCH FIX ---
        # Scrub both formats from the final narration so they don't print or enter history
        final_output = re.sub(r"\[SYS_COMMAND:\s*.*?\]", "", final_output)
        final_output = re.sub(r"/(?:damage|heal|spawn|condition|scene|add|remove)\s+[^\n<\[]+", "", final_output).strip()

        clean_lines = []
        for line in final_output.split('\n'):
            line = line.strip()
            if line:
                clean_line = re.sub(r"^BEAT\s*\d+:\s*", "", line)
                clean_lines.append(clean_line)
        
        formatted_output = "\n\n".join(clean_lines)

        print(f"\n[NARRATION]:\n{formatted_output}")

        _update_seen_techniques(user_input, context)
        add_to_history(context, user_input)
        add_to_history(context, formatted_output)

        for char in context["characters"]:
            # 1. Tick Cooldowns (already have this)
            cds = char["state"].get("cooldowns", {})
            for tech in list(cds.keys()):
                cds[tech] -= 1
                if cds[tech] <= 0: del cds[tech]

            # 2. Tick Status Effects
            statuses = char["state"].get("status_effects", {})
            for effect in list(statuses.keys()):
                # Apply Tick Damage (Modular)
                dot_effects = {"bleeding": 5, "poisoned": 10, "burning": 15}
                if effect.lower() in dot_effects:
                    dmg = dot_effects[effect.lower()]
                    char["state"]["stats"]["hp"] -= dmg
                    print(f"  [STATUS DMG] {char['name']} takes {dmg} from {effect}! (HP: {char['state']['stats']['hp']})")
                
                # Lower duration
                statuses[effect] -= 1
                if statuses[effect] <= 0:
                    print(f"  [STATUS END] {char['name']} is no longer {effect}.")
                    del statuses[effect]

def handle_command(user_input, context):
    state = context["state_manager"]
    parts = user_input.split(" ", 1)
    command = parts[0]
    rest = parts[1].strip() if len(parts) > 1 else ""
    arg_parts = rest.rsplit(" ", 1)
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
        character = get_active_character(context, arg2)
        if character:
            if arg1 not in character["state"]["unlocked_techniques"]:
                character["state"]["unlocked_techniques"].append(arg1)
                print(f"Unlocked {arg1} for {character['name']}!")
            else:
                print(f"{character['name']} already has that technique.")
        else:
            print(f"Character '{arg2}' not in scene.")
            
    elif command == "/condition":
        character = get_active_character(context, arg2)
        if character:
            character["state"]["conditions"].append(arg1)
            print(f"Added condition '{arg1}' to {character['name']}.")
                    
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
        loaded_context = load_session()

        loaded_context["state_manager"] = context["state_manager"] 
        return loaded_context

    elif command in ["/damage", "/heal"]:
        math_parts = rest.split(" ", 1)
        if len(math_parts) == 2:
            try:
                amt = int(math_parts[0])
                target = get_active_character(context, math_parts[1])
                if target:
                    stats = target["state"]["stats"]
                    h_name = state.config.get("system_math", {}).get("health_stat", "HP")
                    
                    if command == "/damage":
                        stats["hp"] -= amt
                        if stats["hp"] <= 0:
                            stats["hp"] = 0
                            # Automatically add the 'Incapacitated' condition
                            if "Incapacitated" not in target["state"]["conditions"]:
                                target["state"]["conditions"].append("Incapacitated")
                            print(f"  [!] CRITICAL: {target['name']} has been defeated.")
                    else:
                        stats["hp"] = min(stats["max_hp"], stats["hp"] + amt)
            except ValueError:
                pass
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
        

    elif command == "/spawn":

        match = re.search(r'"([^"]+)"', rest)
        if match:
            char_name = match.group(1)
        else:
            char_name = rest.strip()
            
        char = state.get_character(char_name)
        if char:
    
            if not any(c["name"].lower() == char["name"].lower() for c in context["characters"]):
                context["characters"].append(char)
                # Silent success - no debug output
            else:
                # Silent failure - no debug output
                pass
        return

    elif command == "/damage_all":
   
        try:
            amt = int(rest.strip())
            h_name = state.config.get("system_math", {}).get("health_stat", "HP")
            for target in context["characters"]:
        
                if target["name"].lower() != context["user_character"].lower():
                    stats = target["state"]["stats"]
                    stats["hp"] -= amt
                    print(f"  [AOE MATH] {target['name']} took {amt} damage! ({h_name}: {stats['hp']})")
        except ValueError:
            pass
        return

    elif command == "/condition":
        match = re.search(r'"([^"]+)"\s+(\d+)\s+(.+)', rest)
        if match:
            effect_name = match.group(1)
            duration = int(match.group(2))
            target_name = match.group(3)
            
            target = get_active_character(context, target_name)
            if target:
                # Store as a dict with a timer
                target["state"].setdefault("status_effects", {})
                target["state"]["status_effects"][effect_name] = duration
                print(f"  [STATUS] {target['name']} afflicted with {effect_name} for {duration} turns.")
        return


        
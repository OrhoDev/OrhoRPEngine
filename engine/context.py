import json
from pathlib import Path


BASE = Path(__file__).parent.parent

def load_system_prompts():
    with open(BASE / "system_prompts.json", "r", encoding="utf-8") as f:
        return json.load(f)

SYSTEM_PROMPTS = load_system_prompts()

def create_context(state_manager, characters=[], response_length="medium", user_character="", scene="", mode="api"):
    system = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS.get("api"))
    return {
        "state_manager": state_manager,
        "system": system,
        "mode": mode,
        "history": [],
        "max_his_size": 5,
        "important":[],
        "characters": characters,
        "response_length": response_length,
        "world_state": "",
        "scene": scene,
        "user_character": user_character,
        "seen_techniques": []
    }

def add_to_history(context, message):
    context["history"].append(message)
    if len(context["history"]) > context["max_his_size"]:
        context["history"].pop(0)

def add_to_pinned(context, message):
    context["important"].append(message)

def unpin(context, message):
    context["important"].remove(message)

def save_session(context, filename="session.json"):
    with open(filename, "w", encoding="utf-8") as f:
    
        save_data = {k: v for k, v in context.items() if k != "state_manager"}
        json.dump(save_data, f)

def _char_to_narrator_block(character):
    condition_text = ", ".join(character.get('state', {}).get('conditions',[])) or 'none'
    base_techniques = ", ".join(character.get('base_techniques',[])) or 'none'
    unlocked_techniques = ", ".join(character.get('state', {}).get('unlocked_techniques',[])) or 'none'
    return f"""## {character['name']}
**Base Techniques:** {base_techniques}
**Unlocked Techniques:** {unlocked_techniques}
**Conditions:** {condition_text}
**Form:** {character.get('state', {}).get('form', 'base')}"""

def _detect_tier(user_input, context):
    lower = user_input.lower()
    state = context["state_manager"]
    
    tier1_keywords = ["domain expansion", "domain expand", "bankai", "ultimate"] 
    if any(k in lower for k in tier1_keywords):
        return "tier1"

    seen = context.get("seen_techniques",[])
    for tech_name in state.techniques.keys():
        if tech_name.lower() in lower and tech_name not in seen:
            return "tier1"

    tier2_keywords =["attack", "hit", "strike", "slash", "blast", "fire", "throw", "punch", "kick", "deploy", "activate", "counter", "block", "dodge"]
    if any(k in lower for k in tier2_keywords):
        return "tier2"

    return "tier3"

def _update_seen_techniques(user_input, context):
    state = context["state_manager"]
    seen = context.get("seen_techniques",[])
    lower = user_input.lower()
    for tech_name in state.techniques.keys():
        if tech_name.lower() in lower and tech_name not in seen:
            seen.append(tech_name)
    context["seen_techniques"] = seen

def build_decision_prompt(context, user_input):
    user = context["user_character"].lower()
    npcs =[c for c in context["characters"] if c["name"].lower() != user]

    if not npcs:
        return ""

    npc_blocks =[]
    for npc in npcs:
        goals = ", ".join(npc.get("goals",[])) or "none"
        enemies = ", ".join(npc.get("enemies",[])) or "none"
        base_techniques = ", ".join(npc.get("base_techniques",[])) or "none"
        unlocked_techniques = ", ".join(npc.get("state", {}).get("unlocked_techniques",[])) or "none"

        npc_blocks.append(f"""## {npc["name"]}
**Goals:** {goals}
**Enemies:** {enemies}
**Psychology:** {npc.get("psychology_and_rp", npc.get("personality", "none"))}
**Combat Behavior:** {npc.get("combat_behavior", "none")}
**Available Techniques:** {base_techniques}, {unlocked_techniques}""")

    npc_text = "\n\n".join(npc_blocks)
    npc_names = [c["name"] for c in npcs]

    json_template = "{{\n  \"environment_event\": \"...\",\n" + ",\n".join([
        f'  "{name}": {{\n    "action": "...",\n    "dialogue": "...",\n    "target": "..."\n  }}'
        for name in npc_names
    ]) + "\n}}"

    return f"""<scene>\n{context["scene"]}\n</scene>\n
<user_action>\n{context["user_character"]}: "{user_input}"\n</user_action>\n
<npcs>\n{npc_text}\n</npcs>\n
Decide what each NPC does this turn in direct response to the user's action. Output ONLY raw JSON. No preamble. No explanation.\n
{json_template}\n
RULES:
- You are deciding actions for NPCs ONLY. 
- ESCALATION MANDATE: If there is a threat, a mystery, or a lull, NPCs MUST take a proactive physical action (draw weapon, investigate).
- ENVIRONMENT CONTROL: You control the world and unnamed entities. Use "environment_event" to describe their reactions.
- action: A concrete technique or movement.
- dialogue: One line maximum. Match Psychology. Empty string if silent.
"""

def build_prompt(context, user_input, npc_decisions=""):
    state = context["state_manager"]
    active = context["characters"]

    char_text = "\n\n".join([_char_to_narrator_block(c) for c in active])

    technique_names = set()
    for c in active:
        technique_names.update(c.get("base_techniques",[]))
        technique_names.update(c.get("state", {}).get("unlocked_techniques",[]))
    mechanics_block = state.get_technique_details(list(technique_names))


    world_briefing =[]
    search_text = (user_input + " " + context['scene'] + " " + npc_decisions).lower()
    
    if state.world_rules:

        keys = list(state.world_rules.keys())
        if keys:
            world_briefing.append(state.world_rules[keys[0]])
            
   
        for key in keys[1:]:
      
            keywords = key.split("_")
            if any(k in search_text for k in keywords):
                world_briefing.append(state.world_rules[key])
                
    world_text = "\n".join(world_briefing)

    npc_names = [c["name"] for c in active if c["name"].lower() != context["user_character"].lower()]
    npc_string = ", ".join(npc_names) if npc_names else "None"

    resolved_block = f"""<resolved_npc_actions>\n{npc_decisions}\n</resolved_npc_actions>""" if npc_decisions else ""

    return f"""<engine_data>
# WORLD RULES
{world_text}

# WORLD STATE
{context['world_state'] or 'Nominal'}

# CURRENT SCENE
{context['scene']}

# ACTIVE COMBATANTS
{char_text}

# RELEVANT MECHANICS
{mechanics_block}
</engine_data>

<history>
{chr(10).join(context['history'][-context['max_his_size']:]) or 'No previous actions.'}
</history>

<user_action>
{context['user_character']} action: "{user_input}"
</user_action>

{resolved_block}

[SYSTEM COMMAND: EXECUTE SIMULATION TICK]
ALLOWED TO ACT/SPEAK: {npc_string}
FORBIDDEN TO ACT/SPEAK: {context['user_character']}
INSTRUCTION: The <resolved_npc_actions> block contains exactly what each NPC decided to do this turn. Narrate those decisions using the technique mechanics above. Do not invent new actions. Do not override the decisions.
CRITICAL: The <narration> block must NEVER describe {context['user_character']}'s body, movements, eyes, hands, or internal state. Begin narration with environmental or mechanical consequence of the action only.
Task: Start your response immediately with <analysis>. Do not write any text before the <analysis> tag.
"""
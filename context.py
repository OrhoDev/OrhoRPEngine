from characters import char_to_prompt
import json
from techniques import get_technique_details
from world import JUJUTSU_WORLD
from pathlib import Path

BASE = Path(__file__).parent

def load_system_prompts():
    with open(BASE / "system_prompts.json", "r") as f:
        return json.load(f)

SYSTEM_PROMPTS = load_system_prompts()


def create_context(characters=[], response_length="medium", user_character="", world_rules="", scene="", mode = "local"):
    system = SYSTEM_PROMPTS[mode]
    return {
        "system": system,
        "mode": mode,
        "history":[],
        "max_his_size": 15, 
        "important":[],
        "characters": characters,
        "response_length": response_length,
        "world_rules": world_rules,
        "world_state": "",
        "scene": scene,
        "user_character": user_character
    }

def add_to_history(context, message):
    context["history"].append(message)
    if len(context["history"]) > context["max_his_size"]:
        context["history"].pop(0)

def add_to_pinned(context, message):
    context["important"].append(message)

def unpin(context, message):
    context["important"].remove(message)

def save_session(context, filename = "session.json"):
    with open(filename, "w") as f:
        json.dump(context, f)

def load_session(filename = "session.json"):
    with open (filename, "r") as f:
        return json.load(f)
 
def build_prompt(context, user_input):
    mode = context.get("mode", "local")
    active = context["characters"]
    char_text = "\n\n".join([char_to_prompt(c, mode) for c in active])

    technique_names = set()
    for c in active:
        technique_names.update(c.get("base_techniques",[]))
        technique_names.update(c.get("state", {}).get("unlocked_techniques",[]))
    mechanics_block = get_technique_details(list(technique_names), mode = mode)

    world_briefing =[JUJUTSU_WORLD["physics"]]
    combat_keywords =["attack", "domain", "expand", "hit", "kill", "fight", "technique"]
    if any(k in user_input.lower() or k in context['scene'].lower() for k in combat_keywords):
        world_briefing.append(JUJUTSU_WORLD["barriers"])
        world_briefing.append(JUJUTSU_WORLD["advanced_operations"])
    else:
        world_briefing.append(JUJUTSU_WORLD["vows"])
        
    if any(loc in context['scene'].lower() for loc in["shibuya", "high", "tombs", "headquarters"]):
        world_briefing.append(JUJUTSU_WORLD["locations"])
    world_text = "\n".join(world_briefing)

    npc_names = [c["name"] for c in active if c["name"].lower() != context["user_character"].lower()]
    npc_string = ", ".join(npc_names) if npc_names else "None"

    prompt = f"""<engine_data>
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
{"\n".join(context['history'][-5:]) or 'No previous actions.'}
</history>

<user_action>
{context['user_character']} action: "{user_input}"
</user_action>

[SYSTEM COMMAND: EXECUTE SIMULATION TICK]
ALLOWED TO ACT/SPEAK: {npc_string}
FORBIDDEN TO ACT/SPEAK: {context['user_character']}
REQUIRED: Each NPC listed above MUST take proactive action this turn - either executing a technique, making a significant movement, or engaging in meaningful dialogue.
CRITICAL: The <narration> block must NEVER describe {context['user_character']}'s body, movements, eyes, hands, or internal state. Begin narration with environmental or mechanical consequence of the action only.
Task: Start your response immediately with <analysis>. Do not write any text before the <analysis> tag.
"""
    return prompt

def get_active_character(context, name):
    for character in context["characters"]:
        # Check for exact match first
        if character["name"].lower() == name.lower():
            return character
        # Check if search name is part of character name
        if name.lower() in character["name"].lower():
            return character
        # Check if character name is part of search name
        if character["name"].lower() in name.lower():
            return character
    return None

def get_technique_summary(context):
  summary = []
  for character in context["characters"]:
    techniques = []
    for key in character["base_techniques"]:
        techniques.append(key)
    for key in character["state"]["unlocked_techniques"]:
        techniques.append(key)
    technique_text = ", ".join(techniques)
    summary.append(f"{character['name']} can only use: {technique_text}")
  return "\n".join(summary)



    

    
    


from characters import char_to_prompt
import json
from techniques import get_technique_details
from world import JUJUTSU_WORLD
from pathlib import Path

BASE = Path(__file__).parent

def load_system_prompts():
    with open(BASE / "system_prompts.json", "r") as f:
        return json.load(f)

def load_examples():
    with open(BASE / "examples.json", "r") as f:
        return json.load(f)

SYSTEM_PROMPTS = load_system_prompts()
EXAMPLES = load_examples()


def create_context(characters=[], response_length="medium", user_character="", world_rules="", scene="", mode="local"):
    system = SYSTEM_PROMPTS[mode]
    return {
        "system": system,
        "mode": mode,
        "history":[],
        "max_his_size": 5,  # OPTIMIZED: Reduced from 15 to 5 to save massive tokens
        "important":[],
        "characters": characters,
        "response_length": response_length,
        "world_rules": world_rules,
        "world_state": "",
        "scene": scene,
        "user_character": user_character,
        "seen_techniques":[]
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
    with open(filename, "w") as f:
        json.dump(context, f)

def load_session(filename="session.json"):
    with open(filename, "r") as f:
        return json.load(f)


def _char_to_narrator_block(character):
    condition_text = ", ".join(character['state']['conditions']) or 'none'
    base_techniques = ", ".join(character['base_techniques']) or 'none'
    unlocked_techniques = ", ".join(character['state']['unlocked_techniques']) or 'none'
    return f"""## {character['name']}
**Base Techniques:** {base_techniques}
**Unlocked Techniques:** {unlocked_techniques}
**Conditions:** {condition_text}
**Form:** {character['state'].get('form', 'base')}"""


def _detect_tier(user_input, context):
    lower = user_input.lower()
    tier1_keywords = ["domain expansion", "domain expand"]
    if any(k in lower for k in tier1_keywords):
        return "tier1"

    from techniques import load_db
    mode = context.get("mode", "local")
    db = load_db(mode)
    seen = context.get("seen_techniques",[])
    for tech_name in db.keys():
        if tech_name.lower() in lower and tech_name not in seen:
            return "tier1"

    tier2_keywords =["attack", "hit", "strike", "slash", "blast", "fire", "throw",
                      "punch", "kick", "deploy", "activate", "counter", "block", "dodge"]
    if any(k in lower for k in tier2_keywords):
        return "tier2"

    return "tier3"


def _update_seen_techniques(user_input, context):
    from techniques import load_db
    mode = context.get("mode", "local")
    db = load_db(mode)
    seen = context.get("seen_techniques",[])
    lower = user_input.lower()
    for tech_name in db.keys():
        if tech_name.lower() in lower and tech_name not in seen:
            seen.append(tech_name)
    context["seen_techniques"] = seen


def build_decision_prompt(context, user_input):
    user = context["user_character"].lower()
    npcs = [c for c in context["characters"] if c["name"].lower() != user]

    if not npcs:
        return ""

    npc_blocks = []
    for npc in npcs:
        goals = ", ".join(npc.get("goals",[])) or "none"
        enemies = ", ".join(npc.get("enemies",[])) or "none"
        base_techniques = ", ".join(npc.get("base_techniques",[])) or "none"
        unlocked_techniques = ", ".join(npc.get("state", {}).get("unlocked_techniques",[])) or "none"

        # OPTIMIZED: We only send psychological and combat data. No appearance or full techniques.
        npc_blocks.append(f"""## {npc["name"]}
**Goals:** {goals}
**Enemies:** {enemies}
**Psychology:** {npc.get("psychology_and_rp", npc.get("personality", "none"))}
**Combat Behavior:** {npc.get("combat_behavior", "none")}
**Available Techniques:** {base_techniques}, {unlocked_techniques}""")

    npc_text = "\n\n".join(npc_blocks)
    npc_names = [c["name"] for c in npcs]

    # Added the environment_event to the JSON template
    json_template = "{{\n  \"environment_event\": \"...\",\n" + ",\n".join([
        f'  "{name}": {{\n    "action": "...",\n    "dialogue": "...",\n    "target": "..."\n  }}'
        for name in npc_names
    ]) + "\n}}"

    return f"""<scene>
{context["scene"]}
</scene>

<user_action>
{context["user_character"]}: "{user_input}"
</user_action>

<npcs>
{npc_text}
</npcs>

Decide what each NPC does this turn in direct response to the user's action.
Output ONLY raw JSON. No preamble. No explanation.

{json_template}

RULES:
- You are deciding actions for NPCs ONLY. 
- ESCALATION MANDATE: If there is a threat, a mystery, or a lull, NPCs MUST take a proactive physical action (draw weapon, investigate).
- ENVIRONMENT CONTROL: You control the world and unnamed entities. Use "environment_event" to describe their reactions.
- action: A concrete technique or movement.
- dialogue: One line maximum. Match Psychology. Empty string if silent.
"""


def build_prompt(context, user_input, npc_decisions=""):
    mode = context.get("mode", "local")
    active = context["characters"]

    char_text = "\n\n".join([_char_to_narrator_block(c) for c in active])

    technique_names = set()
    for c in active:
        technique_names.update(c.get("base_techniques",[]))
        technique_names.update(c.get("state", {}).get("unlocked_techniques",[]))
    mechanics_block = get_technique_details(list(technique_names), mode=mode)

    # OPTIMIZED: World Physics RAG
    world_briefing =[JUJUTSU_WORLD["physics"], JUJUTSU_WORLD["soul"]]
    search_text = (user_input + context['scene'] + npc_decisions).lower()
    
    if any(k in search_text for k in ["domain", "barrier", "simple domain", "hollow wicker", "clash", "sure-hit"]):
        world_briefing.append(JUJUTSU_WORLD["barriers"])
    if any(k in search_text for k in["rct", "reverse", "burnout", "heal", "brain"]):
        world_briefing.append(JUJUTSU_WORLD["advanced_operations"])
    if any(k in search_text for k in ["vow", "contract", "sacrifice", "reveal"]):
        world_briefing.append(JUJUTSU_WORLD["vows"])
    if any(k in search_text for k in ["black flash", "zone", "heavenly restriction"]):
        world_briefing.append(JUJUTSU_WORLD["phenomena"])
    if any(loc in search_text for loc in ["shibuya", "high", "tombs", "headquarters"]):
        world_briefing.append(JUJUTSU_WORLD.get("locations", ""))
        
    world_text = "\n".join(world_briefing)

    npc_names = [c["name"] for c in active if c["name"].lower() != context["user_character"].lower()]
    npc_string = ", ".join(npc_names) if npc_names else "None"

    resolved_block = f"""<resolved_npc_actions>
{npc_decisions}
</resolved_npc_actions>""" if npc_decisions else ""

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

def get_active_character(context, name):
    for character in context["characters"]:
        if character["name"].lower() == name.lower():
            return character
        if name.lower() in character["name"].lower():
            return character
        if character["name"].lower() in name.lower():
            return character
    return None
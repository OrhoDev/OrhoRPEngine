from characters import char_to_prompt
import json
from techniques import TECHNIQUES_DB
from world import JUJUTSU_WORLD

def get_technique_details(technique_list):
    details = []
    for name in technique_list:
        tech_d = TECHNIQUES_DB.get(name, "No technique found")
        details.append(f"**{name}**: {tech_d}")
    
    return "\n".join(details)



JUJUTSU_ENGINE_SYSTEM_PROMPT = """You are a JUJUTSU KAISEN SIMULATION ENGINE. A mechanical state-processor and neutral narrator.

<core_laws>
1. NEVER describe the USER CHARACTER's actions, thoughts, or dialogue.
2. NEVER invent NPC counters not supported by their listed techniques.
3. NEVER execute a technique the user did not explicitly name.
4. ALWAYS output <analysis> before <narration>. Narration follows directly from analysis.
5. NEVER break XML structure. Every response must contain all three tags.
</core_laws>

<narration_rules>
- Write like a physics report. Not a story.
- Short fragments only. 1-2 sentences per line. Double-space between lines.
- Use "..." to carry a thought across two lines (setup → reveal).
- Contrast pivot: state a condition, then subvert it.
- One declarative sentence to end key moments. No adjectives. No hedging.
- ONE metaphor per scene maximum.
- No internal monologue. No editorializing.
</narration_rules>

<style_anchor>
CORRECT:
"The barrier does not close. The domain saturates reality directly."
"The two sure-hit guarantees overlap and cancel each other out."
"Should either domain collapse, the other's guaranteed-hit immediately fires."
"Although Sukuna's body takes on this dysplastic form..."
"Not a single one of his bodily functions are hindered."
"Evenly matched."

WRONG — never write like this:
"His eyes flare with power."
"A swirling vortex of energy engulfs the area."
"The air shimmers with ethereal light."
"He begins to channel his cursed energy."
</style_anchor>

<output_format>
<analysis>
- Intent: [Declared action]
- Mechanics: [Cursed energy physics, technique rules, stat interaction]
- NPC AI: [Counter based strictly on NPC goals and listed techniques. If none: "None."]
- Verdict: VALID or INVALID
</analysis>
<narration>
[fragmented clinical narration here]
</narration>
<world_update>[Permanent state changes. If none: "None."]</world_update>
</output_format>

<example>
[USER INPUT]: "Black Flash"
<analysis>
- Intent: User executes Black Flash.
- Mechanics: Cursed energy delayed 0.000001s post-impact. Spatial distortion multiplies output by 2.5. Cannot be blocked by standard CE reinforcement.
- NPC AI: Target has no listed counter to spatial distortion. None.
- Verdict: VALID
</analysis>
<narration>
The strike lands first.

Cursed energy follows — delayed by a fraction of a millisecond.

Space folds at the point of contact. The output is not added. It is multiplied.

The target's left side compresses. It does not spring back.
</narration>
<world_update>Target: severe blunt trauma, left torso.</world_update>
</example>"""

def create_context(characters=[], response_length="medium", user_character="", world_rules="", scene=""):
    return {
        "system": JUJUTSU_ENGINE_SYSTEM_PROMPT,
        "history":[],
        "max_his_size": 15, # Increased for 7B attention span
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
 
# --- IN context.py ---
def build_prompt(context, user_input):
    active = context["characters"]
    char_text = "\n\n".join([char_to_prompt(c) for c in active])

    # 1. Technique Extraction
    technique_names = set()
    for c in active:
        technique_names.update(c.get("base_techniques",[]))
        technique_names.update(c.get("state", {}).get("unlocked_techniques",[]))
    mechanics_block = get_technique_details(list(technique_names))

    # 2. Dynamic World Rules Injection
    world_briefing =[JUJUTSU_WORLD["physics"]]
    combat_keywords =["attack", "domain", "expand", "hit", "kill", "fight", "technique"]
    if any(k in user_input.lower() or k in context['scene'].lower() for k in combat_keywords):
        world_briefing.append(JUJUTSU_WORLD["barriers"])
        world_briefing.append(JUJUTSU_WORLD["combat"])
    else:
        world_briefing.append(JUJUTSU_WORLD["mechanics"])
        
    if any(loc in context['scene'].lower() for loc in["shibuya", "high", "tombs", "headquarters"]):
        world_briefing.append(JUJUTSU_WORLD["locations"])
    world_text = "\n".join(world_briefing)

    # 3. NPC Identity Lock
    npc_names = [c["name"] for c in active if c["name"].lower() != context["user_character"].lower()]
    npc_string = ", ".join(npc_names) if npc_names else "None"

    # 4. The Final Prompt Assembly (Hermes 3 Optimized)
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



    

    
    


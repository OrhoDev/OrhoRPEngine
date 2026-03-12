from characters import char_to_prompt
import json
from techniques import TECHNIQUES_DB

def get_technique_details(technique_list):
    details = []
    for name in technique_list:
        tech_d = TECHNIQUES_DB.get(name, "No technique found")
        details.append(f"**{name}**: {tech_d}")
    
    return "\n".join(details)


JUJUTSU_ENGINE_SYSTEM_PROMPT = """You are a JUJUTSU KAISEN SIMULATION ENGINE. You are a deterministic state-machine.

<directives>
1. LOGIC IS TRUTH: The <active_characters> data is absolute. If a technique is in 'unlocked_techniques', it is functional. Do not hallucinate failure or 'body betrayal'.
2. CLINICAL TONE: You are not a creative writer. Do not use flowery prose. Describe geometric and physical reality.
3. NO GOD-MODING: You resolve the consequences of the <user_action>. Do not control the player's internal monologue.
4. VALIDATION GATE: You must analyze the action against the character's profile before narrating.
</directives>

<output_format>
You MUST respond using this exact XML structure:

<analysis>
- State intent.
- Verify technique in <active_characters> profile.
- Compare technique power against scene physics.
- Final Verdict: [VALID / INVALID]
</analysis>

<narration>
Describe the scene and the result of the action clinically. Describe only the results of the action. Stop immediately after NPC reactions.
</narration>
</output_format>"""


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
 
def build_prompt(context, user_input):
    # context['characters'] is the dynamic subset of characters active in the scene
    active = context["characters"]
    char_text = "\n\n".join([char_to_prompt(c) for c in active])

    # Collect technique names only from characters currently in context; deduplicate
    technique_names = set()
    for c in active:
        technique_names.update(c.get("base_techniques", []))
        technique_names.update(c.get("state", {}).get("unlocked_techniques", []))
    mechanics_block = get_technique_details(list(technique_names))

    prompt = f"""<simulation_rules>
Logic is truth. Active character data is absolute. Clinical tone. No god-moding. Validate before narrating. Output <analysis> then <narration> with Final Verdict: VALID or INVALID.
</simulation_rules>

<active_characters>
{char_text}
</active_characters>

<available_techniques>
{mechanics_block}
</available_techniques>

<current_scene>
{context['scene']}
</current_scene>

<history>
{"\n".join(context['history']) or 'none'}
</history>

<user_action>
{user_input}
</user_action>"""
    return prompt

def get_active_character(context, name):
    for character in context["characters"]:
        if character["name"].lower() == name.lower():
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



    

    
    


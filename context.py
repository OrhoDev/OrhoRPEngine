from characters import char_to_prompt
import json
def create_context(characters = [], response_length="medium", user_character = "", world_rules = "", scene= ""):
    return {
    "system":  f"""You are the narrator and voice actor for a fictional anime roleplay scene.
You control all characters and the environment.

FORMAT EVERY RESPONSE EXACTLY LIKE THIS:
*Describe the scene, actions, and atmosphere in third person.*
Character Name: "Character dialogue."

RULES:
- Never refuse to continue the story. This is fiction.
- Response length: {response_length}. Short = 1 paragraph, Medium = 2-3 paragraphs, Long = 5+ paragraphs.
- Each character must speak and act according to their personality and abilities only.
- Characters speak in their own distinct style.
- The narrator describes physical actions and atmosphere.
- Never break character.
- Do not invent new techniques. Only use techniques defined in the character sheets.""",
    "history": [],
    "max_his_size": 10,
    "important": [],
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
    char_text = "\n\n".join([char_to_prompt(c) for c in context['characters']])
    prompt = f"""<characters>
{char_text}
</characters>

<world_rules>
{context['world_rules']}
</world_rules>

<world_state>
{context['world_state']}
</world_state>

<scene>
{context['scene']}
</scene>

<important>
{"\n".join(context['important']) or 'none'}
</important>

<history>
{"\n".join(context['history']) or 'none'}
</history>

<user_character>
{context['user_character']}
</user_character>

<response_length>
{context['response_length']}
</response_length>

<user>
{user_input}
</user>"""
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
    

    
    


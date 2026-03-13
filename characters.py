import json
from pathlib import Path

BASE = Path(__file__).parent

def load_characters():
    with open(BASE / "characters.json", "r") as f:
        return json.load(f)

characters = load_characters()

def get_character(name):
    return characters[name.lower().strip()]

def char_to_prompt(character, mode="local"):
    if mode == "local":
        condition_text = ", ".join(character['state']['conditions']) or 'none'
        return f"""## {character['name']}
**Goals:** {', '.join(character.get('goals', [])) or 'none'}
**Enemies:** {', '.join(character.get('enemies', [])) or 'none'}
**Base Techniques:** {', '.join(character['base_techniques']) or 'none'}
**Unlocked Techniques:** {', '.join(character['state']['unlocked_techniques']) or 'none'}
**Conditions:** {condition_text}"""

    condition_text = ", ".join(character['state']['conditions']) or 'none'
    relationships = [f"{k}: {v}" for k, v in character["state"]["relationships"].items()]
    return f"""## {character['name']}
**Age:** {character['age']}
**Appearance:** {character['appearance']}
**Personality:** {character['personality']}
**Goals:** {', '.join(character.get('goals', [])) or 'none'}
**Enemies:** {', '.join(character.get('enemies', [])) or 'none'}
**Base Techniques:** {', '.join(character['base_techniques']) or 'none'}
**Unlocked Techniques:** {', '.join(character['state']['unlocked_techniques']) or 'none'}
**Conditions:** {condition_text}
**Relationships:** {', '.join(relationships) or 'none'}
**Form:** {character['state']['form']}
**Awakening:** {character['state']['awakening'] or 'none'}"""
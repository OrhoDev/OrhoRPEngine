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
    condition_text = ", ".join(character['state']['conditions']) or 'none'
    base_techniques = ", ".join(character['base_techniques']) or 'none'
    unlocked_techniques = ", ".join(character['state']['unlocked_techniques']) or 'none'

    if mode == "local":
        # Local
        return f"""## {character['name']}
**Base Techniques:** {base_techniques}
**Unlocked Techniques:** {unlocked_techniques}
**Conditions:** {condition_text}
**Combat Behavior:** {character.get('combat_behavior', 'none')}"""

    # API 
    relationships = [f"{k}: {v}" for k, v in character.get('relationships', {}).items()]
    return f"""## {character['name']}
**Age:** {character.get('age', 'unknown')}
**Appearance:** {character.get('appearance', 'none')}
**Goals:** {', '.join(character.get('goals', [])) or 'none'}
**Enemies:** {', '.join(character.get('enemies', [])) or 'none'}
**Relationships:** {', '.join(relationships) or 'none'}
**Base Techniques:** {base_techniques}
**Unlocked Techniques:** {unlocked_techniques}
**Conditions:** {condition_text}
**Form:** {character['state']['form']}
**Psychology:** {character.get('psychology_and_rp', 'none')}
**Combat Behavior:** {character.get('combat_behavior', 'none')}"""
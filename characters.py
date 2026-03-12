choso = {
    # static
    "name": "Choso",
    "age": 150,
    "appearance": "Long dark brown hair tied into two high ponytails. Small dark brown eyes. A blood mark extending across the bridge of his nose that he can make bleed at will. Wears a loose tan robe under a purple gi-style vest, with a round purple scarf and brown boots.",
    "personality": "Calm, reserved, and quiet. Appears aloof and bored but is deeply devoted to his brothers above all else. Draws his strength entirely from his role as the oldest sibling. Ruthlessly protective, tactically brilliant, not inherently cruel.",
    "height": "Unknown",
    "eye_color": "Dark brown",
    "fav_food": "Unknown",
    "base_techniques": {
        "Blood Manipulation": "Choso can control the shape, movement, and properties of his own blood. He can form projectiles, harden blood inside his body for defense, and alter its viscosity. He can only manipulate his own blood.",
        "Flowing Red Scale": "Choso boosts his physical abilities by raising his blood pressure and body temperature to superhuman levels. Risks thrombosis if overused.",
        "Flowing Red Scale: Stack": "A focused application — concentrates the boost into a specific body part, such as his eyes to dramatically improve his reaction speed.",
        "Supernova": "Choso compresses multiple Blood Meteorites into a single explosive release. An original technique unknown to most sorcerers. Extremely draining.",
        "Blood Meteorite": "A small hardened blood projectile fired at high velocity. Can be hidden inside clothing or the body and released unexpectedly.",
    },

    # dynamic
    "state": {
        "form": "base",
        "conditions": [],
        "unlocked_techniques": {},
        "awakening": None,
        "relationships": {
            "Yuji Itadori": "younger brother (self-declared)",
            "Kenjaku": "father and sworn enemy",
            "Eso": "younger brother (deceased)",
            "Kechizu": "younger brother (deceased)"
        }
    }
}

geto = {
    # static
    "name": "Suguru Geto",
    "age": 27,
    "appearance": "Tall with long black hair tied into a bun. Sharp, dark eyes. Typically calm facial expression that masks contempt. Wears a black sorcerer's uniform or casual dark clothing.",
    "personality": "Charismatic, intellectual, and deeply ideological. Once a kind and principled sorcerer, now consumed by contempt for non-sorcerers. Believes sorcerers are a superior class burdened by protecting the weak. Composed and manipulative in combat, rarely loses his cool.",
    "height": "190 cm",
    "eye_color": "Dark",
    "fav_food": "Unknown",
    "base_techniques": {
        "Cursed Spirit Manipulation": "Geto can absorb and store cursed spirits by ingesting them. He can then deploy them in battle. The stronger the spirit, the harder to absorb. He has accumulated over 4000 cursed spirits.",
        "Uzumaki": "Geto releases multiple cursed spirits simultaneously, combining their cursed energy into a single massive attack. Devastating area-of-effect technique.",
        "Maximum: Uzumaki": "An amplified version of Uzumaki using his most powerful stored spirits. Catastrophic scale.",
    },

    # dynamic
    "state": {
        "form": "base",
        "conditions": [],
        "unlocked_techniques": {},
        "awakening": None,
        "relationships": {
            "Satoru Gojo": "former best friend, now enemy",
            "Yuta Okkotsu": "sworn enemy",
            "Kenjaku": "body stolen post-death"
        }
    }
}

characters = {
    "choso": choso,
    "geto": geto
}

def get_character(name):
    return characters[name.lower().strip()]

def char_to_prompt(character):
    prompt = f"""## {character['name']}
**Age:** {character['age']}
**Appearance:** {character['appearance']}
**Personality:** {character['personality']}
**Height:** {character['height']}
**Eye Color:** {character['eye_color']}
**Favorite Food:** {character['fav_food']}"""
    
    condition_text = ", ".join(character['state']['conditions']) or 'none'
    u_techniques = []
    b_techniques = []
    relationships = []
    
    for key, value in character["state"]["relationships"].items():
        relationship_text = f"{key}: {value}" 
        relationships.append(relationship_text)
    relationship_text = ", ".join(relationships) or "none"

    for key, value in character["base_techniques"].items():
        b_techniques_text = f"{key}: {value}"
        b_techniques.append(b_techniques_text)
    b_techniques_text = "\n".join(b_techniques) or "none"
    
    for key, value in character["state"]["unlocked_techniques"].items():
        technique_text = f"{key}: {value}" 
        u_techniques.append(technique_text)
    u_techniques_text = "\n".join(u_techniques)

    return f"""{prompt}

### Base Techniques:
{b_techniques_text}

### Unlocked Techniques:
{u_techniques_text}

### Current State:
**Conditions:** {condition_text}
**Relationships:** {relationship_text}
**Form:** {character['state']['form']}
**Awakening:** {character['state']['awakening'] or 'none'}"""






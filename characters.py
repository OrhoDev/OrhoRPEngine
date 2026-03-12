# --- START OF FILE characters.py ---

choso = {
    "name": "Choso",
    "age": 150,
    "appearance": "Long dark brown hair tied into two high ponytails. Small dark brown eyes. A blood mark extending across the bridge of his nose that he can make bleed at will. Wears a loose tan robe under a purple gi-style vest, with a round purple scarf and brown boots.",
    "personality": "Calm, reserved, and quiet. Appears aloof and bored but is deeply devoted to his brothers above all else. Draws his strength entirely from his role as the oldest sibling. Ruthlessly protective, tactically brilliant, not inherently cruel.",
    "height": "Unknown",
    "eye_color": "Dark brown",
    "fav_food": "Unknown",
    "base_techniques":["Blood Manipulation", "Flowing Red Scale", "Flowing Red Scale: Stack", "Supernova", "Blood Meteorite"],
    "state": {
        "form": "base",
        "conditions":[],
        "unlocked_techniques":[],
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
    "name": "Suguru Geto",
    "age": 27,
    "appearance": "Tall with long black hair tied into a bun. Sharp, dark eyes. Typically calm facial expression that masks contempt. Wears a black sorcerer's uniform or casual dark clothing.",
    "personality": "Charismatic, intellectual, and deeply ideological. Once a kind and principled sorcerer, now consumed by contempt for non-sorcerers. Believes sorcerers are a superior class burdened by protecting the weak. Composed and manipulative in combat, rarely loses his cool.",
    "height": "190 cm",
    "eye_color": "Dark",
    "fav_food": "Unknown",
    "base_techniques":["Cursed Spirit Manipulation", "Uzumaki", "Maximum: Uzumaki"],
    "state": {
        "form": "base",
        "conditions": [],
        "unlocked_techniques":[],
        "awakening": None,
        "relationships": {
            "Satoru Gojo": "former best friend, now enemy",
            "Yuta Okkotsu": "sworn enemy",
            "Kenjaku": "body stolen post-death"
        }
    }
}

hiroto = {
    "name": "Hiroto Akagi",
    "age": 18,
    "appearance": "Tall and lean with long limbs. Sharp cheekbones and narrow, dark eyes giving a naturally hostile expression. Perpetually tired or irritated facial posture. Wears Tokyo Jujutsu High uniform.",
    "personality": "Controlled hostility. Stoic, blunt, brutally honest, and impatient with incompetence. Deeply self-sacrificial and violently protective of his younger sister, Aiko. Hates weakness inwardly because it forces others to suffer.",
    "height": "183 cm",
    "eye_color": "Dark, narrow",
    "fav_food": "Unknown",
    "base_techniques":["Legend Manifestation Technique", "Command Hierarchy", "Technique Synergy", "Below-Average Close Quarters Combat"],
    "state": {
        "form": "base",
        "conditions":["Requires prior subjugation to bind entities", "Shikigami destroyed in combat are lost permanently"],
        "unlocked_techniques":["Domain Expansion: Mythological Convergence Field", "Technique Convergence"],
        "awakening": None,
        "relationships": {
            "Aiko Akagi": "Younger sister / sole surviving family (primary protectee)",
            "Tokyo Jujutsu High Students": "Kept at a distance through silent intimidation"
        }
    }
}

gojo = {
    "name": "Satoru Gojo",
    "age": 28,
    "appearance": "Very tall with spiky white hair. Wears a high-collared black jacket and matching pants. Keeps his eyes constantly covered by a black blindfold or dark sunglasses.",
    "personality": "Playful, arrogant, and extremely confident in his overwhelming power. Deeply hates the conservative jujutsu higher-ups and acts as a shield for the younger generation. Underneath his aloof demeanor lies a cold, calculating tactician.",
    "height": "190 cm",
    "eye_color": "Striking, glowing light blue",
    "fav_food": "Sweets",
    "base_techniques":["Limitless", "Infinity", "Cursed Technique Lapse: Blue", "Cursed Technique Reversal: Red", "Hollow Technique: Purple", "Six Eyes"],
    "state": {
        "form": "base",
        "conditions": ["Blindfolded"],
        "unlocked_techniques": ["Domain Expansion: Unlimited Void"],
        "awakening": "Mastered Reverse Cursed Technique and automated Infinity after nearly dying.",
        "relationships": {
            "Suguru Geto": "One and only best friend (deceased)",
            "Megumi Fushiguro": "Adoptive ward / student",
            "Yuji Itadori": "Student whom he fiercely protects",
            "Ryomen Sukuna": "Ultimate rival"
        }
    }
}

yuji = {
    "name": "Yuji Itadori",
    "age": 15,
    "appearance": "Muscular, athletic build with spiky pink hair undercut with black. Has a distinct scar beneath his left eye. Typically wears a customized Jujutsu High uniform featuring a red hood.",
    "personality": "Deeply empathetic, selfless, and driven by his grandfather's dying wish. Cheerful and goofy demeanor, but possesses an unbreakable will and ruthlessness toward curses.",
    "height": "173 cm",
    "eye_color": "Light brown",
    "fav_food": "Rice bowls and noodles",
    "base_techniques":["Superhuman Physicals", "Divergent Fist", "Black Flash"],
    "state": {
        "form": "base",
        "conditions":["Vessel of Sukuna (formerly)"],
        "unlocked_techniques":["Blood Manipulation", "Shrine", "Soul Strike"],
        "awakening": "Unlocked fully realized cursed technique and advanced soul perception.",
        "relationships": {
            "Megumi Fushiguro": "Best friend and comrade",
            "Satoru Gojo": "Mentor",
            "Ryomen Sukuna": "Sworn enemy / former parasitic tenant",
            "Choso": "Older brother"
        }
    }
}

megumi = {
    "name": "Megumi Fushiguro",
    "age": 15,
    "appearance": "Slim but athletic build with spiky, unruly black hair. Usually holds a highly serious and stoic facial expression.",
    "personality": "Pragmatic, logical, and highly secretive. Believes sorcerers are merely a tool to ensure good people live. Harbors a deep well of self-sacrificial tendencies and hidden ruthlessness.",
    "height": "175 cm",
    "eye_color": "Dark Blue",
    "fav_food": "Food that pairs well with ginger",
    "base_techniques":["Ten Shadows Technique", "Divine Dogs", "Nue", "Rabbit Escape", "Shadow Manipulation"],
    "state": {
        "form": "base",
        "conditions": [],
        "unlocked_techniques":["Domain Expansion: Chimera Shadow Garden", "Eight-Handled Sword Divergent Sila Divine General Mahoraga"],
        "awakening": None,
        "relationships": {
            "Yuji Itadori": "Best friend",
            "Satoru Gojo": "Guardian/Teacher",
            "Toji Fushiguro": "Father (deceased)",
            "Tsumiki Fushiguro": "Older step-sister"
        }
    }
}

sukuna = {
    "name": "Ryomen Sukuna",
    "age": 1000,
    "appearance": "Massive four-armed, two-faced demon. When possessing a vessel, he manifests intricate black tribal tattoos and extra eyes.",
    "personality": "Absolute hedonism. Exceptionally arrogant, highly intelligent, and purely evil. Views all other lifeforms as insects.",
    "height": "Variable",
    "eye_color": "Red",
    "fav_food": "Human flesh",
    "base_techniques":["Shrine", "Dismantle", "Cleave", "Furnace (Divine Flame)", "Reverse Cursed Technique"],
    "state": {
        "form": "incarnated",
        "conditions": ["Requires a vessel"],
        "unlocked_techniques":["Domain Expansion: Malevolent Shrine", "World-Cutting Slash"],
        "awakening": "Fully incarnated into his original Heian-era body.",
        "relationships": {
            "Yuji Itadori": "Former prison / despised vessel",
            "Megumi Fushiguro": "Targeted vessel",
            "Uraume": "Loyal servant",
            "Satoru Gojo": "Worthy opponent"
        }
    }
}

yuta = {
    "name": "Yuta Okkotsu",
    "age": 17,
    "appearance": "Lanky teenager with messy black hair and heavy bags under his eyes. Wears a loose white Jujutsu High uniform. Carries a katana.",
    "personality": "Polite, timid, and anxious, but possesses a terrifyingly cold, ruthless demeanor when friends are threatened. Has severe self-worth issues mitigated by protecting others.",
    "height": "175 cm",
    "eye_color": "Dark blue",
    "fav_food": "Salted cabbage",
    "base_techniques":["Rika", "Copy", "Immense Cursed Energy", "Reverse Cursed Technique Output"],
    "state": {
        "form": "base",
        "conditions": ["Requires Ring for 5-minute Rika connection"],
        "unlocked_techniques": ["Domain Expansion: Authentic Mutual Love"],
        "awakening": "Released Rika from her original curse.",
        "relationships": {
            "Rika Orimoto": "Childhood friend / spirit companion",
            "Satoru Gojo": "Teacher",
            "Maki Zenin": "Close classmate",
            "Suguru Geto": "Sworn enemy"
        }
    }
}

maki = {
    "name": "Maki Zenin",
    "age": 16,
    "appearance": "Athletic build, heavily scarred across her face and arms due to burn injuries, short cropped hair.",
    "personality": "Fierce, headstrong, and determined to crush the oppressive Zenin clan. Blunt and aggressive, but deeply protective of her younger classmates.",
    "height": "170 cm",
    "eye_color": "Hazel",
    "fav_food": "Junk food",
    "base_techniques":["Heavenly Restriction (Incomplete)", "Master Weapons Specialist"],
    "state": {
        "form": "awakened",
        "conditions": ["0 Cursed Energy"],
        "unlocked_techniques":["Heavenly Restriction (Complete)", "Domain Immunity"],
        "awakening": "Mai's death completed her Heavenly Restriction.",
        "relationships": {
            "Mai Zenin": "Twin sister (deceased)",
            "Toji Fushiguro": "Physical parallel",
            "Yuta Okkotsu": "Close classmate",
            "Zenin Clan": "Sworn enemies (annihilated)"
        }
    }
}

characters = {
    "choso": choso,
    "geto": geto,
    "hiroto": hiroto,
    "gojo": gojo,
    "yuji": yuji,
    "megumi": megumi,
    "sukuna": sukuna,
    "yuta": yuta,
    "maki": maki
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
    b_techniques_text = ", ".join(character["base_techniques"]) or "none"
    u_techniques_text = ", ".join(character["state"]["unlocked_techniques"]) or "none"
    
    relationships =[f"{key}: {value}" for key, value in character["state"]["relationships"].items()]
    relationship_text = ", ".join(relationships) or "none"

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
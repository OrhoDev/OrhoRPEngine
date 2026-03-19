import json
from pathlib import Path


BASE = Path(__file__).parent.parent

def load_system_prompts():
    with open(BASE / "system_prompts.json", "r", encoding="utf-8") as f:
        return json.load(f)

SYSTEM_PROMPTS = load_system_prompts()

def create_context(state_manager, characters=[], response_length="medium", user_character="", scene="", mode="api"):
    system = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS.get("api"))
    
    config = state_manager.config
    
    system = system.replace("{system_directive}", config.get("system_directive", "You are a roleplay engine."))
    system = system.replace("{narrator_style}", config.get("narrator_style", "Be descriptive and objective."))
    
    forbidden_list = "\n- ".join(config.get("forbidden_words", []))
    system = system.replace("{forbidden_words}", forbidden_list)
    
    system = system.replace("{magic_system}", config.get("terminology", {}).get("magic_system", "magic"))
    system = system.replace("{ultimate_move}", config.get("terminology", {}).get("ultimate_move", "ultimate attack"))
    
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
        "seen_techniques": [],
        "turn_count": 0
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

def load_session(filename="session.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def _char_to_narrator_block(character):
    condition_text = ", ".join(character.get('state', {}).get('conditions',[])) or 'none'
    base_techniques = ", ".join(character.get('base_techniques',[])) or 'none'
    unlocked_techniques = ", ".join(character.get('state', {}).get('unlocked_techniques',[])) or 'none'
    return f"""## {character['name']}
**Base Techniques:** {base_techniques}
**Unlocked Techniques:** {unlocked_techniques}
**Conditions:** {condition_text}
**Form:** {character.get('state', {}).get('form', 'base')}"""


def _build_combat_status_block(context):
    math_cfg = context["state_manager"].config.get("system_math", {})
    h_name = math_cfg.get("health_stat", "HP")
    e_name = math_cfg.get("energy_stat", "MP")
    
    res_blocks = []
    for c in context["characters"]:
        stats = c.get("state", {}).get("stats", {"hp": 100, "energy": 100})
        cds = c.get("state", {}).get("cooldowns", {})
        
        statuses = c.get("state", {}).get("status_effects", {})
        status_str = ", ".join([f"{k}[{v}T]" for k, v in statuses.items()]) or "Healthy"
        
        cd_str = ", ".join([f"{k}({v}T)" for k, v in cds.items()]) or "None"
        
        res_blocks.append(
            f"{c['name']} | {h_name}: {stats['hp']} | {e_name}: {stats['energy']} | "
            f"Status: {status_str} | CDs: {cd_str}"
        )
    
    return "<combat_status>\n" + "\n".join(res_blocks) + "\n</combat_status>"

def _detect_tier(user_input, context):
    lower = user_input.lower()
    state = context["state_manager"]
    
    tier1_keywords = ["domain expansion", "domain expand", "bankai", "ultimate", "maximum", "overdrive", "special attack", "field expansion"] 
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

    relationship_lines = []
    for char in npcs:
        rels = char.get("state", {}).get("relationships", {})
        # Only list relationships with people actually present in the scene
        present_rels = {k: v for k, v in rels.items() if any(c["name"].lower() == k.lower() for c in npcs)}
        
        if present_rels:
            rel_str = ", ".join([f"{k} ({v})" for k, v in present_rels.items()])
            relationship_lines.append(f"- {char['name']} sees: {rel_str}")
    
    social_map = "\n".join(relationship_lines) if relationship_lines else "No established relationships."

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

    combat_status_text = _build_combat_status_block(context)

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

{combat_status_text}

[SPAWNABLE ENTITIES]
The following entities exist in the database and can be summoned using [SYS_COMMAND: /spawn "Name"]:
spirit_swarm, divine_dog_totality, nue, rabbit_escape

[RELATIONSHIP INSTRUCTIONS]
- REFER TO <social_map>: Do not attack characters listed as allies, family, or friends unless NPC's Goals/Psychology explicitly demand betrayal.
- CHECK COMBAT STATE: If any character has taken damage or used energy, the scene is in COMBAT. NPCs must act tactically.
- TARGETING: If a character has the 'Incapacitated' condition, they are DEFEATED. NPCs must stop attacking them and pivot to the next enemy or check on allies.
- PROGRESSION: Do not repeat 'approaching' or 'closing in' for multiple turns. If an NPC was 'closing in' last turn, they MUST land their strike or perform their technique this turn.
- Output ONLY raw JSON matching this structure:
{json_template}
"""

def get_active_character(context, name):
    if not name:
        return None
    name = name.strip()
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

def build_prompt(context, user_input, npc_decisions=""):
    state = context["state_manager"]
    active = context["characters"]

    char_text = "\n\n".join([_char_to_narrator_block(c) for c in active])

    all_known_techs = set()
    for c in active:
        all_known_techs.update(c.get("base_techniques",[]))
        all_known_techs.update(c.get("state", {}).get("unlocked_techniques",[]))
        
    search_text = (user_input + " " + npc_decisions).lower()
    
    # Only load mechanics if the name is mentioned in the text
    active_techs = [t for t in all_known_techs if t.lower() in search_text]
    
    # Always load passive traits that change fundamental physics
    passives =[
        "Six Eyes", "Limitless", "Immense Cursed Energy", "Soul Strike", 
        "Heavenly Restriction (Complete)", "Heavenly Restriction (Incomplete)", 
        "Domain Immunity", "Master Weapons Specialist", "Below-Average Close Quarters Combat"
    ]
    active_techs +=[t for t in all_known_techs if t in passives]
    
    mechanics_block = state.get_technique_details(list(set(active_techs)))

    # --- THE SEMANTIC RAG FIX ---
    rule_triggers = {
        "physics":["ce", "cursed energy", "reinforcement", "output"],
        "soul":["soul", "incarnation", "vessel", "heal"],
        "vows":["vow", "binding", "contract", "promise", "pact"],
        "advanced_operations":["rct", "reverse", "burnout", "brain"],
        "barriers":["domain", "barrier", "simple domain", "hwb", "sure-hit"],
        "phenomena":["black flash", "zone", "heavenly restriction", "zero ce"]
    }
    
    world_briefing =[]
    search_text = (user_input + " " + context['scene'] + " " + npc_decisions).lower()
    
    if state.world_rules:
        if "physics" in state.world_rules:
            world_briefing.append(state.world_rules["physics"])
        for key, triggers in rule_triggers.items():
            if key in state.world_rules and any(t in search_text for t in triggers):
                if key != "physics":
                    world_briefing.append(state.world_rules[key])
                
    world_text = "\n".join(world_briefing)

    npc_names = [c["name"] for c in active if c["name"].lower() != context["user_character"].lower()]
    npc_string = ", ".join(npc_names) if npc_names else "None"

    resolved_block = f"""<resolved_npc_actions>\n{npc_decisions}\n</resolved_npc_actions>""" if npc_decisions else ""
    
    # GET COMBAT STATUS
    combat_status_text = _build_combat_status_block(context)
    
    pinned_text = ""
    if context["important"]:
        pinned_text = "\n<pinned_memory>\n" + "\n".join(context["important"]) + "\n</pinned_memory>\n"

    return f"""<engine_data>
# WORLD RULES
{world_text}

# WORLD STATE
{context['world_state'] or 'Nominal'}

# CURRENT SCENE
{context['scene']}

# ACTIVE COMBATANTS
{char_text}

{combat_status_text}
</engine_data>{pinned_text}

<history>
{chr(10).join(context['history'][-context['max_his_size']:]) or 'No previous actions.'}
</history>

<user_action>
{context['user_character']} action: "{user_input}"
</user_action>

{resolved_block}

[RELEVANT MECHANICS - MANDATORY ADHERENCE]
{mechanics_block}

ALLOWED TO ACT/SPEAK: {npc_string}
FORBIDDEN TO ACT/SPEAK: {context['user_character']}
INSTRUCTION: Resolve every action declared in <user_action> and <resolved_npc_actions> to its final physical conclusion. 
CRITICAL RULES:
1. NO STALLING: Do not use verbs of 'attempt' or 'beginning'. A projectile must either IMPACT a target, MISS, or be DEFLECTED. 
2. COLLISION PHYSICS: Use the 'Mechanics' below to determine if a defense stops an attack.
3. RESULT FIRST: Start each beat with the physical result, then describe the proportional trauma.
4. NO USER DESCRIPTION: Never describe {context['user_character']}'s body, intent, or speech. 
AGENTIC HOOKS (MUST USE EXACT BRACKET SYNTAX): 
- If a hit lands, output EXACTLY: [SYS_COMMAND: /damage 20 CharacterName] (10=light, 30=heavy, 50=massive).
- SUMMATIVE DAMAGE: Calculate the total HP loss for each character from ALL sources this turn (e.g., User attack + NPC ally follow-up). 
- Output EXACTLY one [SYS_COMMAND: /damage total_value Target] per wounded character at the end of the narration.
- If Character A kicks Character C and Character B pierces him, Character C should take the sum of both (e.g., 30 + 10 = 40).
- If the environment changes, output EXACTLY: <scene_update>New Scene Description</scene_update>
Task: Start immediately with <analysis>.
"""
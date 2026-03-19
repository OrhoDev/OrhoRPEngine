#!/usr/bin/env python3
"""
Token Usage Analyzer for RPG Engine
Measures actual token usage for prompts and context construction
"""

import json
import os
import sys
from pathlib import Path

# Add the engine directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'engine'))

try:
    import tiktoken
except ImportError:
    print("Installing tiktoken...")
    os.system("pip install tiktoken")
    import tiktoken

def load_world_data(world_name="jjk"):
    """Load all world data files"""
    base_path = Path("worlds") / world_name
    
    data = {}
    for filename in ["characters.json", "techniques.json", "world.json", "config.json", "examples.json"]:
        file_path = base_path / filename
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data[filename.replace('.json', '')] = json.load(f)
        else:
            print(f"Warning: {filename} not found")
            data[filename.replace('.json', '')] = {}
    
    return data

def simulate_context_building(data, active_characters=["maki", "geto"], user_character="megumi"):
    """Simulate the context building process"""
    characters = data.get('characters', {})
    techniques = data.get('techniques', {})
    world = data.get('world', {})
    
    # Build character blocks
    char_blocks = []
    for char_name in active_characters + [user_character]:
        if char_name in characters:
            char = characters[char_name]
            condition_text = ", ".join(char.get('state', {}).get('conditions', [])) or 'none'
            base_techniques = ", ".join(char.get('base_techniques', [])) or 'none'
            unlocked_techniques = ", ".join(char.get('state', {}).get('unlocked_techniques', [])) or 'none'
            
            char_block = f"""## {char['name']}
**Base Techniques:** {base_techniques}
**Unlocked Techniques:** {unlocked_techniques}
**Conditions:** {condition_text}
**Form:** {char.get('state', {}).get('form', 'base')}"""
            char_blocks.append(char_block)
    
    char_text = "\n\n".join(char_blocks)
    
    # Build techniques block
    tech_names = set()
    for char_name in active_characters + [user_character]:
        if char_name in characters:
            tech_names.update(characters[char_name].get('base_techniques', []))
            tech_names.update(characters[char_name].get('state', {}).get('unlocked_techniques', []))
    
    tech_blocks = []
    for tech_name in tech_names:
        if tech_name in techniques:
            tech_desc = techniques[tech_name]  # It's a string, not an object
            tech_block = f"### {tech_name}\n{tech_desc}\n"
            tech_blocks.append(tech_block)
    
    mechanics_block = "\n".join(tech_blocks)
    
    # Semantic RAG for world rules
    rule_triggers = {
        "physics": ["ce", "cursed energy", "reinforcement", "output"],
        "soul": ["soul", "incarnation", "vessel", "heal"],
        "vows": ["vow", "binding", "contract", "promise", "pact"],
        "advanced_operations": ["rct", "reverse", "burnout", "brain"],
        "barriers": ["domain", "barrier", "simple domain", "hwb", "sure-hit"],
        "phenomena": ["black flash", "zone", "heavenly restriction", "zero ce"]
    }
    
    # Simulate user input and scene
    user_input = "Megumi uses Divine Dog: Totality to attack Geto"
    scene = "Tokyo streets at night, rain falling"
    npc_decisions = 'Geto: {"action": "Maximum Uzumaki", "dialogue": "You dare bring dogs to a curse fight?", "target": "Megumi"}'
    
    search_text = (user_input + " " + scene + " " + npc_decisions).lower()
    
    world_briefing = []
    if "physics" in world:
        world_briefing.append(world["physics"])
    
    for key, triggers in rule_triggers.items():
        if key in world and any(t in search_text for t in triggers):
            if key != "physics":
                world_briefing.append(world[key])
    
    world_text = "\n".join(world_briefing)
    
    # Build combat status
    combat_blocks = []
    for char_name in active_characters + [user_character]:
        if char_name in characters:
            char = characters[char_name]
            stats = char.get('state', {}).get('stats', {"hp": 100, "energy": 100})
            cds = char.get('state', {}).get('cooldowns', {})
            statuses = char.get('state', {}).get('status_effects', {})
            
            status_str = ", ".join([f"{k}[{v}T]" for k, v in statuses.items()]) or "Healthy"
            cd_str = ", ".join([f"{k}({v}T)" for k, v in cds.items()]) or "None"
            
            combat_block = f"{char['name']} | HP: {stats['hp']} | Energy: {stats['energy']} | Status: {status_str} | CDs: {cd_str}"
            combat_blocks.append(combat_block)
    
    combat_status = "<combat_status>\n" + "\n".join(combat_blocks) + "\n</combat_status>"
    
    # Build history
    history = [
        "Maki: Spin attack with spear",
        "Geto: Blocks with cursed energy reinforcement", 
        "Megumi: Summons Divine Dog: Totality",
        "Narrator: The shikigami materializes with a growl, spectral energy coalescing into wolf form",
        "Geto: Curse manipulation creates smaller spirits",
        "Maki: Dodges and repositions",
        "Narrator: Combatants circle each other in the rain-slicked street",
        "Megumi: Directs shikigami to flank",
        "Geto: Prepares domain expansion",
        "Maki: Throws cursed tool",
        "Narrator: Metal shuriken spin through the air",
        "Geto: Deflects with barrier technique"
    ]
    
    history_text = "\n".join(history[-12:])  # Last 12 turns
    
    # Build final prompt
    prompt = f"""<engine_data>
# WORLD RULES
{world_text}

# WORLD STATE
Combat engaged - moderate cursed energy signatures detected

# CURRENT SCENE
{scene}

# ACTIVE COMBATANTS
{char_text}

{combat_status}

# RELEVANT MECHANICS
{mechanics_block}
</engine_data>

<history>
{history_text}
</history>

<user_action>
{user_character} action: "{user_input}"
</user_action>

<resolved_npc_actions>
{npc_decisions}
</resolved_npc_actions>

[SYSTEM COMMAND: EXECUTE SIMULATION TICK]
ALLOWED TO ACT/SPEAK: {', '.join(active_characters)}
FORBIDDEN TO ACT/SPEAK: {user_character}
INSTRUCTION: The <resolved_npc_actions> block contains exactly what each NPC decided to do this turn. Narrate those decisions using the technique mechanics above. Do not invent new actions. Do not override the decisions.
CRITICAL: The <narration> block must NEVER describe {user_character}'s body, movements, eyes, hands, or internal state. Begin narration with environmental or mechanical consequence of the action only.
AGENTIC HOOKS: 
- If an attack lands and damages someone, output[SYS_COMMAND: /damage 20 CharacterName] (Value: 10 for light, 30 for heavy, 50+ for fatal).
- If someone heals, output [SYS_COMMAND: /heal 20 CharacterName].
- If an entity is summoned, output [SYS_COMMAND: /spawn "EntityName"].
- If the environment changes significantly (e.g., a building collapses, moving outside), output <scene_update>New Scene Description</scene_update>.
Task: Start your response immediately with <analysis>. Do not write any text before the <analysis> tag.
"""
    
    return prompt, world_text, mechanics_block, char_text, combat_status, history_text

def build_decision_prompt(data, active_characters=["geto"], user_character="megumi"):
    """Build the decision prompt"""
    characters = data.get('characters', {})
    
    # Build NPC blocks for decision
    npc_blocks = []
    for npc_name in active_characters:
        if npc_name in characters:
            npc = characters[npc_name]
            goals = ", ".join(npc.get('goals', []))
            enemies = ", ".join(npc.get('enemies', []))
            psychology = npc.get('psychology_and_rp', npc.get('personality', 'none'))
            combat_behavior = npc.get('combat_behavior', 'none')
            base_techniques = ", ".join(npc.get('base_techniques', []))
            unlocked_techniques = ", ".join(npc.get('state', {}).get('unlocked_techniques', []))
            
            npc_block = f"""## {npc_name}
**Goals:** {goals}
**Enemies:** {enemies}
**Psychology:** {psychology}
**Combat Behavior:** {combat_behavior}
**Available Techniques:** {base_techniques}, {unlocked_techniques}"""
            npc_blocks.append(npc_block)
    
    npc_text = "\n\n".join(npc_blocks)
    
    # JSON template
    json_template = "{\n  \"environment_event\": \"...\",\n"
    for name in active_characters:
        json_template += f'  "{name}": {{\n    "action": "...",\n    "dialogue": "...",\n    "target": "..."\n  }},\n'
    json_template = json_template.rstrip(',\n') + "\n}"
    
    decision_prompt = f"""<scene>
Tokyo streets at night, rain falling
</scene>

<user_action>
{user_character}: "Megumi uses Divine Dog: Totality to attack Geto"
</user_action>

<npcs>
{npc_text}
</npcs>

Decide what each NPC does this turn in direct response to the user's action. Output ONLY raw JSON. No preamble. No explanation.

{json_template}

RULES:
- You are deciding actions for NPCs ONLY. 
- ACTION ECONOMY: Only 1 or 2 NPCs may take aggressive physical action this turn. The rest MUST observe, reposition, or guard. Do not crowd the initiative.
- ENVIRONMENT CONTROL: You control the world and unnamed entities. Use "environment_event" to describe their reactions.
- action: A concrete technique or movement.
- dialogue: One line maximum. Match Psychology. Empty string if silent.
"""
    
    return decision_prompt

def count_tokens(text, model="gpt-3.5-turbo"):
    """Count tokens using tiktoken"""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # Fallback to cl100k_base (works for most modern models)
        encoding = tiktoken.get_encoding("cl100k_base")
    
    return len(encoding.encode(text))

def analyze_token_usage():
    """Main analysis function"""
    print("🔍 RPG Engine Token Usage Analyzer")
    print("=" * 50)
    
    # Load data
    print("Loading world data...")
    data = load_world_data()
    
    # Load system prompts
    try:
        with open('system_prompts.json', 'r', encoding='utf-8') as f:
            system_prompts = json.load(f)
    except FileNotFoundError:
        print("Warning: system_prompts.json not found")
        system_prompts = {}
    
    # Build prompts
    print("Building prompts...")
    narration_prompt, world_text, mechanics_block, char_text, combat_status, history_text = simulate_context_building(data)
    decision_prompt = build_decision_prompt(data)
    
    # Get system prompt
    system_prompt = system_prompts.get('api', '')
    
    # Count tokens
    print("\n📊 Token Analysis")
    print("-" * 30)
    
    # Narration prompt breakdown
    print("\n🎭 NARRATION PROMPT:")
    narration_tokens = count_tokens(narration_prompt)
    print(f"Total: {narration_tokens:,} tokens")
    
    breakdown = {
        "World Rules (Semantic RAG)": count_tokens(world_text),
        "Character Data": count_tokens(char_text),
        "Techniques": count_tokens(mechanics_block),
        "Combat Status": count_tokens(combat_status),
        "History (12 turns)": count_tokens(history_text),
        "Template/Instructions": narration_tokens - count_tokens(world_text) - count_tokens(char_text) - count_tokens(mechanics_block) - count_tokens(combat_status) - count_tokens(history_text)
    }
    
    for component, tokens in breakdown.items():
        percentage = (tokens / narration_tokens) * 100
        print(f"  {component}: {tokens:,} tokens ({percentage:.1f}%)")
    
    # Decision prompt
    print(f"\n🧠 DECISION PROMPT:")
    decision_tokens = count_tokens(decision_prompt)
    print(f"Total: {decision_tokens:,} tokens")
    
    # System prompt
    print(f"\n⚙️  SYSTEM PROMPT:")
    system_tokens = count_tokens(system_prompt)
    print(f"Total: {system_tokens:,} tokens")
    
    # Total per turn
    total_tokens = narration_tokens + decision_tokens + system_tokens
    print(f"\n💰 TOTAL PER TURN:")
    print(f"Narration: {narration_tokens:,} tokens")
    print(f"Decision: {decision_tokens:,} tokens") 
    print(f"System: {system_tokens:,} tokens")
    print(f"Combined: {total_tokens:,} tokens")
    
    # Context window analysis
    print(f"\n🪟 CONTEXT WINDOW ANALYSIS:")
    common_limits = {
        "GPT-3.5-turbo": 4096,
        "GPT-4": 8192,
        "GPT-4-turbo": 128000,
        "Claude-3-haiku": 200000,
        "Claude-3-sonnet": 200000,
        "Claude-3-opus": 200000,
        "Llama-2-70b": 4096,
        "Mixtral-8x7b": 32768
    }
    
    for model, limit in common_limits.items():
        usage_pct = (total_tokens / limit) * 100
        status = "✅" if usage_pct < 50 else "⚠️" if usage_pct < 80 else "❌"
        print(f"{status} {model}: {total_tokens:,}/{limit:,} ({usage_pct:.1f}%)")
    
    # Optimization suggestions
    print(f"\n💡 OPTIMIZATION INSIGHTS:")
    if breakdown["History (12 turns)"] > 500:
        print("- History is using significant tokens. Consider compression.")
    if breakdown["Character Data"] > 1000:
        print("- Character data is large. Consider selective field loading.")
    if breakdown["Techniques"] > 800:
        print("- Techniques are verbose. Consider condensing descriptions.")
    
    # Simulate different scenarios
    print(f"\n🎭 SCENARIO COMPARISON:")
    scenarios = [
        ("2 characters (current)", ["maki", "geto"]),
        ("3 characters", ["maki", "geto", "yuta"]),
        ("4 characters", ["maki", "geto", "yuta", "panda"]),
        ("5 characters", ["maki", "geto", "yuta", "panda", "toge"])
    ]
    
    for desc, chars in scenarios:
        prompt, _, _, _, _, _ = simulate_context_building(data, active_characters=chars)
        tokens = count_tokens(prompt)
        print(f"{desc}: {tokens:,} tokens")

if __name__ == "__main__":
    analyze_token_usage()

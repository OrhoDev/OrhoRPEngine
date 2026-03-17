import requests


TEMPERATURE = 0.30
TOP_K = 40


def ask(prompt, system=""):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "prompt": prompt,
            "model": "qwen2.5:7b",
            "system": system,
            "stream": False,
            "options": {
                "num_ctx": 4096,
                "temperature": TEMPERATURE,
                "top_k": TOP_K,
                "repeat_penalty": 1.1,
            },
        },
    )
    
    response_data = response.json()
    
    return response_data["response"]

def validate(response, world_rules, scene, technique_summary):
    prompt = f"""You are a strict rule validator for a roleplay system.

<world_rules>
{world_rules}
</world_rules>

<scene>
{scene}
</scene>

<available_abilities>
{technique_summary}
</available_abilities>

<examples>
VIOLATION: "Character A summoned a wall of fire" (when not in their abilities list) → YES
VIOLATION: "Character B dodged at the speed of light" (defying world rules) → YES
NON-VIOLATION: "Character C hardened their armor and blocked the strike" (using listed ability) → NO
</examples>

<response_to_validate>
{response}
</response_to_validate>

Does the response violate the world rules, scene constraints, or use abilities a character doesn't have? Answer only YES or NO.
Your answer:"""
    return ask(prompt)
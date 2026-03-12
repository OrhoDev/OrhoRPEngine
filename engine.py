import requests

# Deterministic state-machine: low temperature and top_k for logical consistency
TEMPERATURE = 0.1
TOP_K = 20


def ask(prompt, system=""):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "prompt": prompt,
            "model": "qwen2.5:7b",
            "system": system,
            "stream": False,
            "options": {
                "temperature": TEMPERATURE,
                "top_k": TOP_K,
                "repeat_penalty": 1.1,
            },
        },
    )
    
    # Debug: Print the actual response structure
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

<techniques>
{technique_summary}
</techniques>

<examples>
VIOLATION: "Choso summoned a wall of fire" → YES
VIOLATION: "Choso used Geto's Uzumaki" → YES
NON-VIOLATION: "Choso hardened his blood and blocked the punch" → NO
</examples>

<response_to_validate>
{response}
</response_to_validate>

Does the response violate the world rules, scene constraints, or use techniques a character doesn't have? Answer only YES or NO.
Your answer:"""
    return ask(prompt)
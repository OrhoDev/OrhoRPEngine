import requests
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

TEMPERATURE = 0.4

def ask(prompt, system="", few_shot=None):
    messages =[{"role": "system", "content": system}]

    if few_shot:
        messages.append({"role": "user", "content": few_shot["input"]})
        messages.append({"role": "assistant", "content": few_shot["output"]})

    messages.append({"role": "user", "content": prompt})

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",  
            "messages": messages,
            "temperature": TEMPERATURE,
            "max_tokens": 1024,
        }
    )
    response_json = response.json()
    
    if "choices" not in response_json:
        print(f"ERROR: Rate Limit or API Error. Full response: {response_json}")
        return f"API Error: {response_json}"
    
    return response_json["choices"][0]["message"]["content"]

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
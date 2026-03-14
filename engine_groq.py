import requests
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

TEMPERATURE = 0.5

def ask(prompt, system="", few_shot=None):
    messages = [{"role": "system", "content": system}]

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
    return response.json()["choices"][0]["message"]["content"]

def validate(response, world_rules, scene, technique_summary):
    prompt = f"""You are a strict rule validator for a roleplay system.
<response_to_validate>{response}</response_to_validate>
Does this response violate world rules or use techniques a character doesn't have? Answer YES or NO only."""
    return ask(prompt)
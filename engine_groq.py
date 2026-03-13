import requests
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

TEMPERATURE = 0.8

def ask(prompt, system=""):
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
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
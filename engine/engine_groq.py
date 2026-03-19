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
        return f"API Error: {response_json}", 0, 0
    
    content = response_json["choices"][0]["message"]["content"]
    usage = response_json.get("usage", {})
    
    return content, usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0)

def validate(response, world_rules, scene, technique_summary):
    prompt = f"""You are a strict logic engine.
<world_rules>\n{world_rules}\n</world_rules>
<scene>\n{scene}\n</scene>
<available_abilities>\n{technique_summary}\n</available_abilities>

Evaluate the user's intended action. Does it violate physics, or use a technique they do not possess?
Output EXACTLY one of these two formats. No other text:
VALID
INVALID: [State the exact mechanical reason why it fails]

User Action: {response}"""
    
    # Because ask() returns (content, p_tokens, c_tokens), 
    # validate() will seamlessly return that same tuple back to chat.py!
    return ask(prompt, system="You are a strict referee. Output only VALID or INVALID: [reason].")
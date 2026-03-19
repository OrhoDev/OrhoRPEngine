import requests

TEMPERATURE = 0.30
TOP_K = 40

def ask(prompt, system="", few_shot=None):
    if few_shot:
        system += f"\n\nExample Output Pattern:\n{few_shot['output']}"
        prompt = f"Example Action:\n{few_shot['input']}\n\nNow process this action:\n{prompt}"

    try:
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
        response.raise_for_status()
        response_data = response.json()
        
        content = response_data["response"]
        p_tokens = response_data.get("prompt_eval_count", 0)
        c_tokens = response_data.get("eval_count", 0)
        
        return content, p_tokens, c_tokens
    except requests.exceptions.RequestException as e:
        print(f"\n[ENGINE ERROR]: Local AI failed to respond (Is Ollama running?). Detail: {e}")
        return "(Local engine error.)", 0, 0

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
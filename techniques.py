import json
from pathlib import Path

BASE = Path(__file__).parent

def load_db(mode="local"):
    filename = "techniques_api.json" if mode == "api" else "techniques_local.json"
    with open(BASE / filename, "r") as f:
        return json.load(f)

def get_technique_details(technique_list, mode="local"):
    db = load_db(mode)
    details = []
    for name in technique_list:

        tech_d = db.get(name, "No technique found")
        details.append(f"**{name}**: {tech_d}")
    return "\n".join(details)
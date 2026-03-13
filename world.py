import json
from pathlib import Path

BASE = Path(__file__).parent

def load_world():
    with open(BASE / "world.json", "r") as f:
        return json.load(f)

JUJUTSU_WORLD = load_world()
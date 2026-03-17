

import json
from pathlib import Path


ROOT_DIR = Path(__file__).parent.parent

class StateManager:
    def __init__(self, world_name="jjk"):
        self.world_name = world_name
        self.world_path = ROOT_DIR / "worlds" / world_name
        

        self.characters = self._load_json("characters.json")
        self.techniques = self._load_json("techniques.json")
        self.world_rules = self._load_json("world.json")
        self.examples = self._load_json("examples.json")
        self.config = self._load_json("config.json")
        self.examples = self._load_json("examples.json")

    def _load_json(self, filename):
        file_path = self.world_path / filename
        if not file_path.exists():
            return {}
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_character(self, name):
        """Retrieve a character by exact or partial name."""
        name = name.lower().strip()
        if name in self.characters:
            return self.characters[name]
        
        for key, char_data in self.characters.items():
            if name in char_data["name"].lower():
                return char_data
        return None

    def get_technique_details(self, technique_list):
        """Fetch mechanics for a list of techniques, ignoring missing ones."""
        details =[]
        for name in technique_list:
            tech_d = self.techniques.get(name, None)
            if tech_d:
                details.append(f"**{name}**: {tech_d}")
        return "\n".join(details)
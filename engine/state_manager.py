

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

    def _load_json(self, filename):
        file_path = self.world_path / filename
        if not file_path.exists():
            return {}
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_character(self, name):
        """Retrieve a character by exact or partial name."""
        name = name.lower().strip()
        found_char = None
        
        if name in self.characters:
            found_char = self.characters[name]
        else:
            for key, char_data in self.characters.items():
                if name in char_data["name"].lower():
                    found_char = char_data
                    break

        if found_char:
            if "stats" not in found_char.setdefault("state", {}):
                math_cfg = self.config.get("system_math", {})
                max_hp = math_cfg.get("base_max_health", 100)
                max_energy = math_cfg.get("base_max_energy", 100)
                
                all_techs = found_char.get("base_techniques", []) + found_char["state"].get("unlocked_techniques",[])
                overrides = math_cfg.get("trait_overrides", {})
                
                for tech in all_techs:
                    if tech in overrides:
                        max_hp = overrides[tech].get("max_health", max_hp)
                        max_energy = overrides[tech].get("max_energy", max_energy)
                        
                found_char["state"]["stats"] = {
                    "hp": max_hp, "max_hp": max_hp,
                    "energy": max_energy, "max_energy": max_energy
                }
                found_char["state"]["cooldowns"] = {}
                
        return found_char

    def get_technique_details(self, technique_list):
        """Fetch mechanics for a list of techniques, ignoring missing ones."""
        details =[]
        for name in technique_list:
            tech_d = self.techniques.get(name, None)
            if tech_d:
                details.append(f"**{name}**: {tech_d}")
        return "\n".join(details)
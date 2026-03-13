import json
from techniques import TECHNIQUES_DB_LOCAL, TECHNIQUES_DB_API
from characters import characters
from world import JUJUTSU_WORLD

# Dump techniques
with open("techniques_local.json", "w") as f:
    json.dump(TECHNIQUES_DB_LOCAL, f, indent=2)

with open("techniques_api.json", "w") as f:
    json.dump(TECHNIQUES_DB_API, f, indent=2)

# Dump characters
with open("characters.json", "w") as f:
    json.dump(characters, f, indent=2)

# Dump world
with open("world.json", "w") as f:
    json.dump(JUJUTSU_WORLD, f, indent=2)

print("Done. Check your JSON files.")
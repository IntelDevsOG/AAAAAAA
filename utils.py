import json
import os

USERMAP_PATH = "data/usermap.json"

def load_usermap():
    if not os.path.exists(USERMAP_PATH):
        return {}
    with open(USERMAP_PATH, "r") as f:
        return json.load(f)

def save_usermap(data):
    with open(USERMAP_PATH, "w") as f:
        json.dump(data, f, indent=2)
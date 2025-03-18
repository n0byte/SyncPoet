import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
jsoninput_dir = os.path.join(current_dir, "information.json")

# Sicherstellen, dass information.json existiert; ansonsten erstellen
if not os.path.exists(jsoninput_dir):
    with open(jsoninput_dir, 'w') as file:
        json.dump({}, file, indent=4)

def read_json():
    with open(jsoninput_dir, 'r') as file:
        data = json.load(file)
    return data
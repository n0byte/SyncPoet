import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

modeInfo_dir = os.path.join(current_dir, 'modeInfo.json')
sidebarInfo_dir = os.path.join(current_dir, 'sidebarInfo.json')

cache_dir = os.path.join(current_dir, 'cache')

def ensure_json_file():
    print(f"Checking if {modeInfo_dir} and {sidebarInfo_dir} exists...")
    if os.path.exists(modeInfo_dir) and os.path.exists(sidebarInfo_dir):
        print(f"{modeInfo_dir} and {sidebarInfo_dir} exist.")
    else:
        print(f"{modeInfo_dir} and {sidebarInfo_dir} do not exist. Creating them...")
        with open(modeInfo_dir, 'w') as f:
            json.dump({}, f)
        with open(sidebarInfo_dir, 'w') as f:
            json.dump([], f)
        print(f"{modeInfo_dir} and {sidebarInfo_dir} created.")

def ensure_cache_dir():
    print(f"Checking if {cache_dir} exists...")
    if os.path.exists(cache_dir):
        print(f"{cache_dir} exists.")
    else:
        print(f"{cache_dir} does not exist. Creating it...")
        os.makedirs(cache_dir)
        print(f"{cache_dir} created.")

def ensure():
    ensure_json_file()
    ensure_cache_dir()
    return True
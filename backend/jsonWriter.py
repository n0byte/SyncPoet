import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

modeInfo_dir = os.path.join(current_dir, 'modeInfo.json')
sidebarInfo_dir = os.path.join(current_dir, 'sidebarInfo.json')

def writeUserPlaceHolderInformation():
     with open(sidebarInfo_dir, 'w') as f:
        status = "Sending"
        filename = "cache"
        data = [
            {"filename": filename, "status": status}
        ]
        json.dump(data, f, indent=4)
        print(f"Status written successfully. Status: {status} and Placeholder name: {filename}")

def writeModeInformation(data):
    print("Writing mode info into the modeInfo.json file...")
    with open(modeInfo_dir, "w") as file:
        json.dump(data, file, indent=4)
    print("Mode info written successfully.")
import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

modeInfo_dir = os.path.join(current_dir, 'modeInfo.json')
sidebarInfo_dir = os.path.join(current_dir, 'sidebarInfo.json')

cache_dir = os.path.join(current_dir, 'cache')

def GETmode():
    print("Get Mode from modeInfo.json...")
    with open(modeInfo_dir, 'r') as f:
        data = json.load(f)
        mode = data.get('mode', 'undefined')
    print(f"Mode successfully read from modeInfo.json: {mode}")
    return mode


def GETsettings():
    print("Get settings from modeInfo.json...")
    with open(modeInfo_dir, 'r') as f:
        data = json.load(f)
        settings = data.get('settings', {})
    
    # Format each setting for better readability
    formatted_settings = "\n".join([
        f"{key} = {value}"
        for key, value in settings.items()
    ])
    
    print("\nSettings successfully read from modeInfo.json:")
    print("-" * 50)
    print(formatted_settings)
    print("-" * 50)

    return settings

# !?
def GETsidebar():
    print("Get sidebar Information from sidebarInfo.json...")
    with open (sidebarInfo_dir, 'r') as f:
        data = json.load(f)
        sidebarInfo = data.get('sidebar', {})
    print(f"Sidebar Information successfully read from sidebarInfo.json: {sidebarInfo}")
    return sidebarInfo


def GETdate():
    print("Get date and howmany from modeInfo.json...")
    with open(modeInfo_dir, 'r') as f:
        data = json.load(f)
        date = data.get('date', 'undefined')
        howMany = data.get('howMany', 'undefined')
    dateResult = f"{date} {howMany}"
    print(f"Date and howmany successfully read from modeInfo.json: {dateResult}")
    return dateResult


def GETsingleModeInfos():
    print("Get singleModeInfos from modeInfo.json...")
    try:
        with open(modeInfo_dir, 'r') as f:
            data = json.load(f)
            singleMode = data.get('singleMode', {})
            user_info = data.get('user', {})
            emails = user_info.get('emails', [])
            names = user_info.get('names', [])

        singleResult = {
            'singleMode': singleMode,
            'emails': emails,
            'names': names
        }

        print(f"Mode Information:")
        print(f"Single Mode: {singleMode}")    
        print("User information:")
        print(f"Emails: {emails}")
        print(f"Names: {names}")
        print(f"\nReturn value: {singleResult}")
        
        return singleResult
    except FileNotFoundError:
        print(f"Error: File {modeInfo_dir} not found")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON format")
        return None
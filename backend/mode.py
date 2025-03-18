import json
import os
import time
from config import read_json  # Neuer Import aus config.py
import sys


sys.stdout.reconfigure(encoding='utf-8')

def extract_single_mode_data():
    data = read_json()
    keys_single = ["singleMode", "date", "howMany", "howManySynchronize", "user"]
    single_data = {key: data.get(key) for key in keys_single}
    
    # Einstellungen auslesen und den Header-String in ein Dictionary umwandeln
    settings = data.get("settings", {})
    if "CRMHeader" in settings and isinstance(settings["CRMHeader"], str):
        try:
            settings["CRMHeader"] = json.loads(settings["CRMHeader"])
        except json.JSONDecodeError:
            settings["CRMHeader"] = {}
    single_data["settings"] = settings
    return single_data

def extract_other_mode_data():
    data = read_json()
    keys_other = ["date", "howMany"]
    other_data = {key: data.get(key) for key in keys_other}
    
    settings = data.get("settings", {})
    if "CRMHeader" in settings and isinstance(settings["CRMHeader"], str):
        try:
            settings["CRMHeader"] = json.loads(settings["CRMHeader"])
        except json.JSONDecodeError:
            settings["CRMHeader"] = {}
    other_data["settings"] = settings
    return other_data

# Direkt beim Laden des Moduls die Konfigurationswerte ausgeben:
print("Single Mode Werte:")
print(extract_single_mode_data())
print("\nAndere Modi Werte:")
print(extract_other_mode_data())

# Weitere Funktionsdefinitionen, die im Hauptprogramm zur Ausführung kommen:
def single_mode():
    print("Processing single mode...")
    time.sleep(10)  # Simuliere Arbeit
    return {
        "status": "completed",
        "message": "Single mode processing completed",
        "processId": "single"
    }

def c2m_mode():
    print("Processing c2m mode...")
    # Der Import erfolgt hier innerhalb der Funktion, um zirkuläre Importe zu vermeiden.
    from GET_CRM import get_all_crm_data
    config = read_json()
    # Zeitraum aus der Konfiguration (z.B. "date" in der JSON)
    date_value = config.get("date", "days 90")
    # Settings aus der Konfiguration
    settings = config.get("settings", {})
    print("Executing CRM mode with date_value:", date_value)
    crm_data = get_all_crm_data(date_value=date_value, custom_settings=settings)
    print("CRM mode data retrieved:")
    print(crm_data)
    
    # Kombiniere beide Ergebnisse in einem Dictionary
    return {
        "crm_data": crm_data,
        "status": "completed",
        "message": "CRM to MailPoet sync completed",
        "processId": "c2m"
    }


def m2c_mode():
    print("Processing m2c mode...")
    time.sleep(10)  # Simuliere Arbeit
    return {
        "status": "completed",
        "message": "MailPoet to CRM sync completed",
        "processId": "m2c"
    }

def all_mode():
    print("Processing all modes...")
    time.sleep(10)  # Simuliere Arbeit
    return {
        "status": "completed",
        "message": "All synchronization completed",
        "processId": "all"
    }

# Optional: Direkt beim Laden des Moduls den CRM Mode ausführen:
#c2m_mode()
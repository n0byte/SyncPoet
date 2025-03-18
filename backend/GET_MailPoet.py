# ==========================================================
#                         GET MailPoet
# ==========================================================
# Author: Melvin Paul Hanns
# Date: 2025.02.25
# Version: 1.0
# Description: This script will get the MailPoet data from the
#              MailPoet database and return it to the user.
# ==========================================================

# -------------------------------
#          Import Libraries
import requests
import msgpack
import json
import os
# -------------------------------

# -------------------------------
#          Global Variables
MAILPOET_API_BASE = "https://staging4.ketmarket.eu/wp-json/custom-mailpoet/v1"

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)
# -------------------------------

# -------------------------------
#          Helper Functions
def save_to_cache(data, artificial_id):
    cache_file = os.path.join(CACHE_DIR, f"{artificial_id}mailpoet.msgpack")
    with open(cache_file, "wb") as f:
        msgpack.pack(data, f)

def process_mailpoet_data(data, artificial_id, name_filters=None, email_filters=None):
    processed_data = []
    for item in data:
        name = str(item.get("name", "Kein Name")).strip()
        email = str(item.get("email", "Keine E-Mail")).strip()
        
        if not email or email.lower() == "none":
            email = "email@istnicht.vorhanden"
        
        if name_filters and not any(name_filter in name for name_filter in name_filters):
            continue
        
        if email_filters and not any(email_filter in email for email_filter in email_filters):
            continue
        
        save_to_cache({"name": name, "email": email}, artificial_id)
        processed_data.append(item)
        artificial_id += 1
    return processed_data, artificial_id
# -------------------------------

# -------------------------------
#          Main Functions
def get_subscribers():
    url = f"{MAILPOET_API_BASE}/get-subscribers/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("[Fehler] API-Fehler:", e)
        return None

def get_all_mailpoet_data():
    data = get_subscribers()
    if data is None:
        print("❌ Keine Daten abgerufen.")
        return []

    artificial_id = 0
    processed_data, artificial_id = process_mailpoet_data(data, artificial_id)

    if processed_data:
        print("✅ Erfolgreich alle Abonnenten gespeichert!")
        for entry in processed_data:
            print(f"Name: {entry.get('name', 'Kein Name')}, Email: {entry.get('email', 'Keine E-Mail')}")
    else:
        print("❌ Keine Abonnenten gespeichert oder Daten existieren nicht.")

    return processed_data

def get_specific_mailpoet_data(name_filters=None, email_filters=None):
    data = get_subscribers()
    if data is None:
        print("❌ Keine Daten abgerufen.")
        return []

    artificial_id = 0
    processed_data, artificial_id = process_mailpoet_data(data, artificial_id, name_filters, email_filters)

    if processed_data:
        print("✅ Erfolgreich gefilterte Abonnenten gespeichert!")
        for entry in processed_data:
            print(f"Name: {entry.get('name', 'Kein Name')}, Email: {entry.get('email', 'Keine E-Mail')}")
    else:
        print("❌ Keine gefilterten Abonnenten gespeichert oder Daten existieren nicht.")

    return processed_data
# -------------------------------
# ==========================================================
#                         POST CRM
# ==========================================================
# Author: Melvin Paul Hanns
# Date: 2025.02.25
# Version: 1.0
# Description: this script is used to create a new entry in the CRM
#              system. It sends a POST request to the CRM API
#              endpoint with the required data.
# ==========================================================

# -------------------------------
#          Import Libraries
from jsonReader import cache_dir
import requests
import msgpack
import json
import os
# -------------------------------

# -------------------------------
#          Global Variables
CACHE_DIR = cache_dir
# -------------------------------

# -------------------------------
#          Helper Functions
def load_cached_data():
    cached_files = [f for f in os.listdir(CACHE_DIR) if f.endswith('mailpoet.msgpack')]
    all_data = []
    for file in cached_files:
        with open(os.path.join(CACHE_DIR, file), "rb") as f:
            data = msgpack.unpack(f)
            all_data.append(data)
    return all_data

def prepare_payload(data):
    payloads = []
    for item in data:
        payload = {
            "name": item.get("name", "Test Name"),
            "email": item.get("email", "test@example.com"),
            "client": 0,    # Kein Kunde
            "prospect": 1,  # Interessent
            "supplier": 0   # Kein Lieferant
        }
        payloads.append(payload)
    return payloads
# -------------------------------

# -------------------------------
#          Main Functions
def post_all_crm_data(custom_settings):
    data = load_cached_data()
    payloads = prepare_payload(data)

    crm_url = custom_settings.get("CRMUrl")
    try:
        crm_headers = json.loads(custom_settings.get("CRMHeader", "{}"))
    except json.JSONDecodeError:
        crm_headers = {}

    for payload in payloads:
        response = requests.post(crm_url, headers=crm_headers, json=payload)
        if response.status_code in [200, 201]:
            print("✅ Eintrag erfolgreich erstellt!")
        else:
            print(f"❌ Fehler {response.status_code}: {response.text}")
# -------------------------------
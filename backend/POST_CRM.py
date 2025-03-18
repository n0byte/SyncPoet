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
import requests
import msgpack
import json
import os
# -------------------------------

# -------------------------------
#          Global Variables
api_url = "https://erp.ketmarket.eu/api/index.php/thirdparties"
headers = {
    "DOLAPIKEY": "31782J51I0s3ZFZZbpqZbCTWxcpPi8jv",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

CACHE_DIR = "cache"
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

def filter_data(data, name_filters=None, email_filters=None):
    filtered_data = []
    for item in data:
        name = item.get("name", "").strip()
        email = item.get("email", "").strip()
        
        if name_filters and not any(name_filter in name for name_filter in name_filters):
            continue
        
        if email_filters and not any(email_filter in email for email_filter in email_filters):
            continue
        
        filtered_data.append(item)
    return filtered_data
# -------------------------------

# -------------------------------
#          Main Functions
def post_crm(payload):
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code in [200, 201]:
        print("✅ Eintrag erfolgreich erstellt!")
    else:
        print(f"❌ Fehler {response.status_code}: {response.text}")

def post_all_crm_data():
    data = load_cached_data()
    payloads = prepare_payload(data)
    for payload in payloads:
        post_crm(payload)

def post_specific_crm_data(name_filters=None, email_filters=None):
    data = load_cached_data()
    filtered_data = filter_data(data, name_filters, email_filters)
    payloads = prepare_payload(filtered_data)
    for payload in payloads:
        post_crm(payload)
# -------------------------------

# -------------------------------
#          Main Execution
if __name__ == "__main__":
    choice = input("Geben Sie 1 ein, um alle Daten abzurufen, oder 2, um spezifische Daten abzurufen: ")

    if choice == "1":
        post_all_crm_data()
    elif choice == "2":
        post_specific_crm_data(
            name_filters=["John"],
            email_filters=["example@example.com"]
        )
    else:
        print("Ungültige Eingabe. Bitte geben Sie 1 oder 2 ein.")
# -------------------------------
# -------------------------------
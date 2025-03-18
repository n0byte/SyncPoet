# ==========================================================
#                         POST MailPoet
# ==========================================================
# Author: Melvin Paul Hanns
# Date: 2025.02.25
# Version: 1.0
# Description: This script will post a new subscriber to the
#              MailPoet database and return the result to the user.
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
#          Main Functions
def post_subscriber(email, first_name="", last_name=""):
    url = f"{MAILPOET_API_BASE}/post-subscriber/"
    payload = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        json_response = response.json()

        # Falls Fehler 500, aber der User wurde hinzugefügt, trotzdem als Erfolg werten
        if response.status_code == 500 and json_response.get("status") == "warning":
            print("[INFO] Fehler 500 ignoriert, weil User erfolgreich hinzugefügt wurde!")
            return json_response
        
        response.raise_for_status()
        return json_response

    except requests.exceptions.RequestException as e:
        print("[Fehler] API-Fehler:", e)
        return None

#--------------------------------

# -------------------------------
#          Main Execution
if __name__ == "__main__":
    print("Neuen Abonnenten hinzufügen...")
    result = post_subscriber("test@example.com", "Max", "Mustermann")
    print(result)
# -------------------------------
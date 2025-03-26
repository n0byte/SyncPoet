# ==========================================================
#                         POST MailPoet
# ==========================================================
# Author: Melvin Paul Hanns
# Date: 2025.02.25
# Version: 1.1
# Description: This script will post subscribers to the
#              MailPoet database by reading cached data.
# ==========================================================

# -------------------------------
#          Import Libraries
from ensure import cache_dir
import requests
import msgpack
import os
# -------------------------------

# -------------------------------
#          Global Variables

CACHE_DIR = cache_dir

# -------------------------------

# -------------------------------
#          Main Function
def post_subscriber(custom_settings):
    if not custom_settings:
        raise ValueError("❌ Es wurden keine custom_settings übergeben!")

    mailpoet_url = custom_settings.get("MailPoetUrl")
    if not mailpoet_url:
        raise ValueError("❌ MailPoetUrl fehlt in den custom_settings!")

    headers = {"Content-Type": "application/json"}

    # Debugging: Start processing cache directory
    print(f"[DEBUG] Verarbeite Cache-Verzeichnis: {CACHE_DIR}")

    # Process only files ending with 'crm.msgpack'
    for file_name in os.listdir(CACHE_DIR):
        if not file_name.endswith("crm.msgpack"):
            print(f"[DEBUG] Überspringe Datei: {file_name} (nicht relevant)")
            continue

        cache_file = os.path.join(CACHE_DIR, file_name)
        print(f"[DEBUG] Verarbeite Datei: {cache_file}")

        try:
            with open(cache_file, "rb") as f:
                data = msgpack.unpack(f)

            # Debugging: Show loaded data
            print(f"[DEBUG] Geladene Daten: {data}")

            payload = {
                "email": data.get("email"),
                "first_name": data.get("name", ""),
                "last_name": "",
                "status": "subscribed"
            }
            url = f"{mailpoet_url}/post-subscriber/"

            # Debugging: Show payload and URL
            print(f"[DEBUG] Sende Anfrage an URL: {url} mit Payload: {payload}")

            response = requests.post(url, json=payload, headers=headers, timeout=10)
            json_response = response.json()

            if response.status_code == 500 and json_response.get("status") == "warning":
                print(f"[INFO] Fehler 500 ignoriert für {data.get('email')}, weil User erfolgreich hinzugefügt wurde!")
            else:
                response.raise_for_status()

            print(f"✅ Erfolgreich hinzugefügt: {data.get('email')}")

        except requests.RequestException as e:
            print(f"[Fehler] Fehler beim Hinzufügen von {data.get('email')}: {e}")
        except Exception as e:
            print(f"[Fehler] Fehler beim Verarbeiten der Datei {cache_file}: {e}")

    print("[INFO] Verarbeitung abgeschlossen.")
# -------------------------------
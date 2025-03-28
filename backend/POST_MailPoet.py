# ==========================================================
#                         POST MailPoet
# ==========================================================
# Author: Melvin Paul Hanns
# Date: 2025.02.25
# Version: 1.2
# Description:
#     This script posts subscribers to the MailPoet list 3
#     by reading CRM-cached data in msgpack format.
# ==========================================================

import os
import requests
import msgpack
from ensure import cache_dir

# -------------------------------
#          Global Variables
CACHE_DIR = cache_dir
HEADERS = {"Content-Type": "application/json"}
MAILPOET_ENDPOINT = "POSTmailpoet-list3"
# -------------------------------

def post_subscriber(custom_settings):
    if not custom_settings:
        raise ValueError("❌ Keine custom_settings übergeben!")

    mailpoet_base = custom_settings.get("MailPoetUrl")
    if not mailpoet_base:
        raise ValueError("❌ MailPoetUrl fehlt in den custom_settings!")

    mailpoet_url = mailpoet_base.rstrip("/") + f"/{MAILPOET_ENDPOINT}"
    print(f"[INFO] Ziel-URL für POST: {mailpoet_url}")

    print(f"[INFO] Lese Cache-Verzeichnis: {CACHE_DIR}")
    for file_name in os.listdir(CACHE_DIR):
        if not file_name.endswith("crm.msgpack"):
            print(f"[DEBUG] ➔ Überspringe {file_name} (nicht relevant)")
            continue

        file_path = os.path.join(CACHE_DIR, file_name)
        print(f"[INFO] ➔ Verarbeite: {file_path}")

        try:
            with open(file_path, "rb") as f:
                data = msgpack.unpack(f)

            # Zusammenbauen des Payloads
            payload = {
                "email": data.get("email"),
                "first_name": data.get("name", ""),
                "last_name": ""
            }

            print(f"[DEBUG]   → Payload: {payload}")

            response = requests.post(mailpoet_url, json=payload, headers=HEADERS, timeout=10)

            try:
                response_data = response.json()
            except Exception:
                response_data = {"text": response.text}

            if response.status_code in [200, 201]:
                print(f"[✅] Hinzugefügt: {payload['email']}")
            elif response.status_code == 500 and response_data.get("status") == "warning":
                print(f"[⚠️] Fehler 500 ignoriert: {payload['email']} (vermutlich erfolgreich)")
            else:
                print(f"[❌] Fehler bei {payload['email']}: {response.status_code} – {response_data}")

        except Exception as e:
            print(f"[ERROR] Fehler bei Datei {file_name}: {e}")

    print("[INFO] ✅ Verarbeitung abgeschlossen.")
    # --------------------------------
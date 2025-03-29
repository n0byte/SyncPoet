from jsonReader import cache_dir
import requests
import msgpack
import os

CACHE_DIR = cache_dir

def mailpoet_email_exists(base_url, email):
    check_url = f"{base_url}/CHECK-MailPoet-list3"
    try:
        response = requests.get(check_url, params={"email": email}, timeout=5)
        return response.json().get("status") == "exists"
    except Exception as e:
        print(f"[WARN] Existenzprüfung fehlgeschlagen: {e}")
        return False
    

def post_subscriber_into_mailpoet(custom_settings):
    # Checks if custom_settings is provided
    if not custom_settings:
        raise ValueError("❌ Keine custom_settings übergeben!")

    # Checks MailPoetUrl
    mailpoet_base = custom_settings.get("MailPoetUrl")
    if not mailpoet_base:
        raise ValueError("❌ MailPoetUrl fehlt in den custom_settings!")

    target_url = f"{mailpoet_base}/POST-MailPoet-list3"
    print(f"[INFO] Ziel-URL für POST: {target_url}")

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

            # Check if email already exists before processing
            if mailpoet_email_exists(mailpoet_base, payload["email"]):
                print(f"[SKIP] {payload['email']} existiert bereits – übersprungen.")
                continue

            print(f"[DEBUG]   → Payload: {payload}")

            response = requests.post(target_url, json=payload, timeout=10)

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
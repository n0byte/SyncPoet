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

def crm_email_exists(crm_url, crm_headers, email):
    check_url = f"{crm_url}?sqlfilters=(email:=:'{email}')"
    try:
        response = requests.get(check_url, headers=crm_headers, timeout=5)
        results = response.json()
        return len(results) > 0
    except Exception as e:
        print(f"[WARN] CRM-Check fehlgeschlagen: {e}")
        return False
# -------------------------------

# -------------------------------
#          Main Functions
def post_subscriber_into_crm(custom_settings):
    data = load_cached_data()
    payloads = prepare_payload(data)

    crm_url = custom_settings.get("CRMUrl")
    try:
        crm_headers = json.loads(custom_settings.get("CRMHeader", "{}"))
    except json.JSONDecodeError:
        crm_headers = {}

    for payload in payloads:
        if crm_email_exists(crm_url, crm_headers, payload["email"]):
            print(f"[SKIP] {payload['email']} existiert bereits im CRM – übersprungen.")
            continue
        
        response = requests.post(crm_url, headers=crm_headers, json=payload)
        if response.status_code in [200, 201]:
            print(f"✅ Eintrag erfolgreich erstellt: {payload['email']}")
        else:
            print(f"❌ Fehler {response.status_code} bei {payload['email']}: {response.text}")
# -------------------------------
# ==========================================================
#                         GET CRM
# ==========================================================
# Author: Melvin Paul Hanns
# Version: 1.5 (angepasst für direkte Übergabe der Settings und Fallback bei 'undefined')
# ==========================================================

from datetime import datetime, timedelta
import requests
import msgpack
import os
import json

# -------------------------------
#          Global Variables
CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# -------------------------------
#          Helper Functions
def parse_date_value(date_value):
    parts = date_value.split()
    if len(parts) == 1:
        # Falls nur die Einheit übergeben wird, Standardwert (z.B. 10 Tage) verwenden
        unit = parts[0]
        value = 14
    elif len(parts) == 2:
        unit, value = parts
        # Falls der Wert nicht definiert oder nicht konvertierbar ist, Standardwert 10 verwenden
        if value == "undefined":
            value = 14
        else:
            try:
                value = int(value)
            except ValueError:
                value = 14
    else:
        raise ValueError("Invalid date format")
    
    now = datetime.now()
    if unit == "days":
        start_date = now - timedelta(days=value)
    elif unit == "months":
        start_date = now - timedelta(days=value * 30)
    elif unit == "years":
        start_date = now - timedelta(days=value * 365)
    else:
        raise ValueError("Invalid date unit")
    return start_date.strftime("%Y-%m-%d")

def fetch_crm_data(page, limit, start_date, crm_url, crm_headers):
    params = {
        "limit": limit,
        "page": page,
    }
    # Falls start_date vorhanden ist, wird ein Filter angewendet.
    if start_date is not None:
        params["sqlfilters"] = f"(t.datec:>=:'{start_date}')"
    print(f"Fetching data with params: {params}")  # Debugging-Ausgabe
    response = requests.get(crm_url, headers=crm_headers, params=params)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()

def save_to_cache(data, artificial_id):
    cache_file = os.path.join(CACHE_DIR, f"{artificial_id}crm.msgpack")
    with open(cache_file, "wb") as f:
        msgpack.pack(data, f)

def process_crm_data(data, artificial_id, name_filters=None, email_filters=None):
    processed_data = []
    for item in data:
        name = str(item.get("name", "Kein Name")).strip()
        email = str(item.get("email", "Keine E-Mail")).strip()
        creation_date = item.get("creation_date")
        
        # Debugging-Ausgabe zum Prüfen des Erstellungsdatums
        print(f"Processing item with creation_date: {creation_date}")

        if not email or email.lower() == "none":
            email = "email@istnicht.vorhanden"

        # Filter: Falls Name- oder E-Mail-Filter gesetzt sind, 
        # wird der Datensatz nur bei Übereinstimmung übernommen.
        if name_filters or email_filters:
            match = False
            if name_filters and any(nf in name for nf in name_filters):
                match = True
            if email_filters and any(ef in email for ef in email_filters):
                match = True
            if not match:
                continue

        save_to_cache({"name": name, "email": email, "creation_date": creation_date}, artificial_id)
        processed_data.append(item)
        artificial_id += 1
    return processed_data, artificial_id

# -------------------------------
#          Main Functions
def get_all_crm_data(date_value, custom_settings):
    """
    Holt alle CRM-Daten basierend auf date_value und übergebenen Einstellungen.
    """
    if not custom_settings:
        raise ValueError("❌ Es wurden keine custom_settings übergeben!")
    
    # Einstellungen aus dem übergebenen Dictionary verwenden
    crm_url = custom_settings.get("CRMUrl")
    try:
        crm_headers = json.loads(custom_settings.get("CRMHeader", "{}"))
    except json.JSONDecodeError:
        crm_headers = {}
    mailpoet_url = custom_settings.get("MailPoetUrl")  # aktuell ungenutzt

    page = 0
    limit = 200
    all_entries = []
    artificial_id = 0

    if date_value.lower() == "all":
        start_date = None
    else:
        start_date = parse_date_value(date_value)

    while True:
        try:
            data = fetch_crm_data(page, limit, start_date, crm_url, crm_headers)
        except requests.RequestException as e:
            print(f"Fehler beim Abrufen der CRM Daten: {e}")
            break

        if data is None or not data:
            break

        processed_data, artificial_id = process_crm_data(data, artificial_id)
        all_entries.extend(processed_data)
        page += 1

    if all_entries:
        print("✅ Erfolgreich alle Pakete gespeichert!")
        for entry in all_entries:
            print(f"Name: {entry.get('name', 'Kein Name')}, Email: {entry.get('email', 'Keine E-Mail')}")
    else:
        print("❌ Keine Pakete gespeichert oder Daten existieren nicht.")

    return all_entries

def get_specific_crm_data(date_value, custom_settings, name_filters=None, email_filters=None, max_items=10):
    """
    Holt spezifische CRM-Daten basierend auf Filtern und übergebenen Einstellungen.
    """
    if not custom_settings:
        raise ValueError("❌ Es wurden keine custom_settings übergeben!")
    
    crm_url = custom_settings.get("CRMUrl")
    try:
        crm_headers = json.loads(custom_settings.get("CRMHeader", "{}"))
    except json.JSONDecodeError:
        crm_headers = {}
    
    page = 0
    limit = 200
    all_entries = []
    artificial_id = 0

    if date_value.lower() == "all":
        start_date = None
    else:
        start_date = parse_date_value(date_value)

    while True:
        try:
            data = fetch_crm_data(page, limit, start_date, crm_url, crm_headers)
        except requests.RequestException as e:
            print(f"Fehler beim Abrufen der CRM Daten: {e}")
            break

        if data is None or not data:
            break

        processed_data, artificial_id = process_crm_data(data, artificial_id, name_filters, email_filters)
        all_entries.extend(processed_data)
        if len(all_entries) >= max_items:
            all_entries = all_entries[:max_items]
            break
        page += 1

    if all_entries:
        print("✅ Erfolgreich alle Pakete gespeichert!")
        for entry in all_entries:
            print(f"Name: {entry.get('name', 'Kein Name')}, Email: {entry.get('email', 'Keine E-Mail')}")
    else:
        print("❌ Keine Pakete gespeichert oder Daten existieren nicht.")

    return all_entries
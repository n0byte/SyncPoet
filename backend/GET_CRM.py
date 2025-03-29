# -------------------------------
#          Import Libraries
from datetime import datetime, timedelta
from jsonReader import cache_dir
import requests
import logging
import msgpack
import json
import os

# -------------------------------
#          Global Variables & Logging Setup
CACHE_DIR = cache_dir

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------------
#          Helper Functions
def parse_date_value(date_value: str) -> str:
    parts = date_value.split()
    if len(parts) == 1:
        unit = parts[0]
        value = 14
    elif len(parts) == 2:
        unit, value = parts
        try:
            value = int(value) if value != "undefined" else 14
        except ValueError:
            value = 14
    else:
        raise ValueError("Ungültiges Datumsformat.")
    now = datetime.now()
    if unit == "days":
        start_date = now - timedelta(days=value)
    elif unit == "months":
        start_date = now - timedelta(days=value * 30)
    elif unit == "years":
        start_date = now - timedelta(days=value * 365)
    else:
        raise ValueError("Ungültige Datumseinheit.")
    return start_date.strftime("%Y-%m-%d")


def fetch_crm_data(page: int, limit: int, start_date: str, crm_url: str, crm_headers: dict):
    params = {"limit": limit, "page": page}
    if start_date is not None:
        params["sqlfilters"] = f"(t.datec:>=:'{start_date}')"
    logging.info(f"Fetching data with params: {params}")
    response = requests.get(crm_url, headers=crm_headers, params=params)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


def save_to_cache(data, artificial_id: int) -> None:
    cache_file = os.path.join(CACHE_DIR, f"{artificial_id}crm.msgpack")
    with open(cache_file, "wb") as f:
        msgpack.pack(data, f)
    logging.debug(f"Data saved to cache file: {cache_file}")


def process_crm_data(data, artificial_id: int, name_filters=None, email_filters=None):
    processed_data = []
    for item in data:
        name = str(item.get("name", "Kein Name")).strip()
        email = str(item.get("email", "Keine E-Mail")).strip()
        creation_date = item.get("creation_date")
        
        logging.debug(f"Processing item with creation_date: {creation_date}")
        
        if not email or email.lower() == "none":
            email = "email@istnicht.vorhanden"
        
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
def get_all_crm_data(date_value: str, custom_settings: dict):
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

    start_date = None if date_value.lower() == "all" else parse_date_value(date_value)
    
    while True:
        try:
            data = fetch_crm_data(page, limit, start_date, crm_url, crm_headers)
        except requests.RequestException as e:
            logging.error(f"Fehler beim Abrufen der CRM Daten: {e}")
            break

        if not data:
            break

        processed_data, artificial_id = process_crm_data(data, artificial_id)
        all_entries.extend(processed_data)
        page += 1

    if all_entries:
        logging.info("✅ Erfolgreich alle Pakete gespeichert!")
        for entry in all_entries:
            logging.info(f"Name: {entry.get('name', 'Kein Name')}, Email: {entry.get('email', 'Keine E-Mail')}")
    else:
        logging.error("❌ Keine Pakete gespeichert oder Daten existieren nicht.")

    return all_entries


def get_specific_crm_data(custom_settings: dict, name_filters=None, email_filters=None, max_items=10):
    if not custom_settings:
        raise ValueError("❌ Es wurden keine custom_settings übergeben!")
    
    crm_url = custom_settings.get("CRMUrl")
    try:
        crm_headers = json.loads(custom_settings.get("CRMHeader", "{}"))
    except json.JSONDecodeError:
        crm_headers = {}

    # Kein Datum-Filter in dieser Funktion
    start_date = None
    
    page = 0
    limit = 200
    all_entries = []
    artificial_id = 0

    while True:
        try:
            data = fetch_crm_data(page, limit, start_date, crm_url, crm_headers)
        except requests.RequestException as e:
            logging.error(f"Fehler beim Abrufen der CRM Daten: {e}")
            break

        if not data:
            break

        processed_data, artificial_id = process_crm_data(data, artificial_id, name_filters, email_filters)
        all_entries.extend(processed_data)
        if len(all_entries) >= max_items:
            all_entries = all_entries[:max_items]
            break
        page += 1

    if all_entries:
        logging.info("✅ Erfolgreich alle Pakete gespeichert!")
        for entry in all_entries:
            logging.info(f"Name: {entry.get('name', 'Kein Name')}, Email: {entry.get('email', 'Keine E-Mail')}")
    else:
        logging.error("❌ Keine Pakete gespeichert oder Daten existieren nicht.")

    return all_entries
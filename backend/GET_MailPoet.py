from datetime import datetime, timedelta
from jsonReader import cache_dir
import requests
import msgpack
import os

CACHE_DIR = cache_dir

def parse_date_value(date_value):
    parts = date_value.split()
    if len(parts) == 1:
        unit = parts[0]
        value = 14
    elif len(parts) == 2:
        unit, value = parts
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

def save_to_cache(data, artificial_id):
    cache_file = os.path.join(CACHE_DIR, f"{artificial_id}mailpoet.msgpack")
    with open(cache_file, "wb") as f:
        msgpack.pack(data, f)

def process_mailpoet_data(data, artificial_id, name_filters=None, email_filters=None, start_date=None):
    processed_data = []
    for item in data:
        # Kombiniere first_name und last_name zum Namen
        first_name = str(item.get("first_name", "")).strip()
        last_name = str(item.get("last_name", "")).strip()
        name = (first_name + " " + last_name).strip() or "Kein Name"
        email = str(item.get("email", "Keine E-Mail")).strip()
        created = item.get("created_at")

        if not email or email.lower() == "none":
            email = "email@istnicht.vorhanden"

        # Filtere nach Namen, wenn Filter gesetzt sind
        if name_filters and not any(name_filter.lower() in name.lower() for name_filter in name_filters):
            continue
        # Filtere nach Email, wenn Filter gesetzt sind
        if email_filters and not any(email_filter.lower() in email.lower() for email_filter in email_filters):
            continue

        # Filtere nach Datum, falls gesetzt und vorhanden
        if start_date and created:
            try:
                created_date = datetime.strptime(created[:10], "%Y-%m-%d")
                filter_date = datetime.strptime(start_date, "%Y-%m-%d")
                if created_date < filter_date:
                    continue
            except Exception:
                pass

        save_to_cache({"name": name, "email": email}, artificial_id)
        processed_data.append(item)
        artificial_id += 1
    return processed_data, artificial_id

def get_all_mailpoet_data(date_value, custom_settings):
    if not custom_settings:
        raise ValueError("Es wurden keine custom_settings übergeben!")

    mailpoet_url = custom_settings.get("MailPoetUrl")
    if not mailpoet_url:
        raise ValueError("MailPoetUrl fehlt in den Einstellungen!")

    # Verwende den korrekten GET-Endpunkt
    url = f"{mailpoet_url}/GET-MailPoet-list3"
    
    params = {}
    # Wenn kein spezifischer Filter (E-Mail/Name) gewünscht ist, kann der Datumfilter gesetzt werden
    if date_value.lower() != "all":
        params['date'] = parse_date_value(date_value)

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Hole nur die Abonnenten
        subscribers = data.get("subscribers", [])
    except requests.exceptions.RequestException as e:
        print("[Fehler] API-Fehler:", e)
        return []

    artificial_id = 0
    processed_data, _ = process_mailpoet_data(subscribers, artificial_id, start_date=params.get('date'))

    if processed_data:
        print("Erfolgreich alle Abonnenten gespeichert!")
        for entry in processed_data:
            name = (entry.get("first_name", "") + " " + entry.get("last_name", "")).strip()
            print(f"Name: {name}, Email: {entry.get('email')}")
    else:
        print("Keine Abonnenten gefunden.")

    return processed_data

def get_specific_mailpoet_data(date_value, custom_settings, name_filters=None, email_filters=None, max_items=10):
    if not custom_settings:
        raise ValueError("Es wurden keine custom_settings übergeben!")

    mailpoet_url = custom_settings.get("MailPoetUrl")
    if not mailpoet_url:
        raise ValueError("MailPoetUrl fehlt in den Einstellungen!")

    # Verwende denselben GET-Endpunkt
    url = f"{mailpoet_url}/GET-MailPoet-list3"
    
    params = {}
    if email_filters:
        # Übergebe den ersten E-Mail-Filterwert (für Tests)
        params['email'] = email_filters[0]
    elif name_filters:
        params['name'] = name_filters[0]
    # Wenn weder E-Mail noch Name gesetzt sind und ein Datum gefordert ist, setze den Datumfilter
    if not params and date_value.lower() != "all":
        params['date'] = parse_date_value(date_value)

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        subscribers = data.get("subscribers", [])
    except requests.exceptions.RequestException as e:
        print("[Fehler] API-Fehler:", e)
        return []

    artificial_id = 0
    processed_data, _ = process_mailpoet_data(
        subscribers, 
        artificial_id, 
        name_filters, 
        email_filters, 
        params.get('date')
    )
    processed_data = processed_data[:max_items]

    if processed_data:
        print("Erfolgreich gefilterte Abonnenten gespeichert!")
        for entry in processed_data:
            name = (entry.get("first_name", "") + " " + entry.get("last_name", "")).strip()
            print(f"Name: {name}, Email: {entry.get('email')}")
    else:
        print("Keine passenden Abonnenten gefunden.")

    return processed_data
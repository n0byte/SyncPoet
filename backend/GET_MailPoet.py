from datetime import datetime, timedelta
from ensure import cache_dir
import requests
import msgpack
import os
import json

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
        name = str(item.get("name", "Kein Name")).strip()
        email = str(item.get("email", "Keine E-Mail")).strip()
        created = item.get("created")

        if not email or email.lower() == "none":
            email = "email@istnicht.vorhanden"

        if name_filters and not any(name_filter in name for name_filter in name_filters):
            continue
        if email_filters and not any(email_filter in email for email_filter in email_filters):
            continue

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
        raise ValueError("❌ Es wurden keine custom_settings übergeben!")

    mailpoet_url = custom_settings.get("MailPoetUrl")
    if not mailpoet_url:
        raise ValueError("❌ MailPoetUrl fehlt in den Einstellungen!")

    url = f"{mailpoet_url}/get-subscribers/"
    if date_value.lower() == "all":
        start_date = None
    else:
        start_date = parse_date_value(date_value)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print("[Fehler] API-Fehler:", e)
        return []

    artificial_id = 0
    processed_data, _ = process_mailpoet_data(data, artificial_id, start_date=start_date)

    if processed_data:
        print("✅ Erfolgreich alle Abonnenten gespeichert!")
        for entry in processed_data:
            print(f"Name: {entry.get('name')}, Email: {entry.get('email')}")
    else:
        print("❌ Keine Abonnenten gefunden.")

    return processed_data


def get_specific_mailpoet_data(date_value, custom_settings, name_filters=None, email_filters=None, max_items=10):
    if not custom_settings:
        raise ValueError("❌ Es wurden keine custom_settings übergeben!")

    mailpoet_url = custom_settings.get("MailPoetUrl")
    if not mailpoet_url:
        raise ValueError("❌ MailPoetUrl fehlt in den Einstellungen!")

    url = f"{mailpoet_url}/get-subscribers/"
    if date_value.lower() == "all":
        start_date = None
    else:
        start_date = parse_date_value(date_value)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print("[Fehler] API-Fehler:", e)
        return []

    artificial_id = 0
    processed_data, _ = process_mailpoet_data(data, artificial_id, name_filters, email_filters, start_date)
    processed_data = processed_data[:max_items]

    if processed_data:
        print("✅ Erfolgreich gefilterte Abonnenten gespeichert!")
        for entry in processed_data:
            print(f"Name: {entry.get('name')}, Email: {entry.get('email')}")
    else:
        print("❌ Keine passenden Abonnenten gefunden.")

    return processed_data
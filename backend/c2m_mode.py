from jsonReader import GETsettings, GETdate
from jsonReader import sidebarInfo_dir
from GET_CRM import get_all_crm_data
from jsonWriter import writeUserPlaceHolderInformation
import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

def c2m_mode():
    print("Processing c2m mode...")

    # This gives the User a Simple View of the Status of the Data and Shows that the Process Successfully Started
    writeUserPlaceHolderInformation()

    # Gets the Date and Settings from the JSON File
    raw_date = GETdate()                            # Example: "days:30"
    date_value = raw_date.replace(":", " ")         # Convert to: "days 30" for compatibility with GET_CRM
    settings = GETsettings()

    # Gets the CRM Data 
    print("Getting CRM data with date_value:", date_value)
    crm_data = get_all_crm_data(date_value=date_value, custom_settings=settings)
    print(f"CRM data retrieved: {crm_data}")

    # Posting into MAilPoet

    print("Processing done.")
    print("Successfully completed C2M mode.")
from jsonWriter import writeUserPlaceHolderInformation
from jsonReader import GETsettings, GETdate, cache_dir
from POST_CRM import post_subscriber_into_crm
from GET_MailPoet import get_all_mailpoet_data
import time
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

def m2c_mode():
    print("Processing m2c mode...")

    # This gives the User a Simple View of the Status of the Data and Shows that the Process Successfully Started
    writeUserPlaceHolderInformation()

    # Gets the Date and Settings from the JSON File
    raw_date = GETdate()                            # Example: "days:30"
    date_value = raw_date.replace(":", " ")         # Convert to: "days 30" for compatibility with GET_CRM
    settings = GETsettings()

    # GET MailPoet data
    print("Getting MailPoet data with date_value:", date_value)
    mailpoet_data = get_all_mailpoet_data(date_value=date_value, custom_settings=settings)
    print(f"MailPoet data retrieved: {mailpoet_data}")

    # Posting into CRM
    print("Posting MailPoet data into CRM...")
    posting_mailpoet_data = post_subscriber_into_crm(custom_settings=settings)
    print(f"MailPoet data posted: {posting_mailpoet_data}")
    
    time.sleep(1)
    # Clear cache directory
    for file in os.listdir(cache_dir):
        file_path = os.path.join(cache_dir, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f'Error: {e}')
        
    time.sleep(1)
    print("Processing done.")
    print("Successfully completed M2C mode.")
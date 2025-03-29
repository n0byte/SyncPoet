from GET_CRM import get_specific_crm_data
from GET_MailPoet import get_specific_mailpoet_data
from POST_CRM import post_subscriber_into_crm
from POST_MailPoet import post_subscriber_into_mailpoet
from jsonReader import GETsettings, GETsingleModeInfos, cache_dir
import time
import os

def single_mode():

    print("Reading json file...")
    singleMode = GETsingleModeInfos()
    print(f"Readed SingleMode: {singleMode}")

    if singleMode == "c2m":
        print("c2m mode selected in SingleModo.")
        singleC2M_mode()
    elif singleMode == "m2c":
        print("m2c mode selected in SingleModo.")
        singleM2C_mode()
    else:
        print("Invalid mode selected.")     
    


def singleC2M_mode():
    print("Processing SingleC2M mode...")

    print("Reading json file...")
    settings = GETsettings()
    single_infos = GETsingleModeInfos()
    emails = single_infos.get("emails", [])
    names = single_infos.get("names", [])
    print(f"Readed SingleMode infos: {settings} \n {emails} \n {names}")

    # Gets the CRM Data 
    print("Getting Spezific CRM data...")
    crm_data = get_specific_crm_data(custom_settings=settings, email_filters=emails, name_filters=names)
    print(f"CRM data retrieved: {crm_data}")

    # Posting into MAilPoet
    print("Posting CRM data into MailPoet...")
    posting_crm_data = post_subscriber_into_mailpoet(custom_settings=settings)
    print(f"CRM data posted: {posting_crm_data}")
    

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
    print("Successfully completed SingleC2M Mode.")



def singleM2C_mode():
    print("Processing SingleM2C mode...")

    print("Reading json file...")
    settings = GETsettings()
    single_infos = GETsingleModeInfos()
    emails = single_infos.get("emails", [])
    names = single_infos.get("names", [])
    print(f"Readed SingleMode infos: {settings} \n {emails} \n {names}")

    # Gets the CRM Data 
    print("Getting Spezific MailPoet data...")
    mailpoet_data = get_specific_mailpoet_data("all", custom_settings=settings, email_filters=emails, name_filters=names)
    print(f"CRM data retrieved: {mailpoet_data}")

    # Posting into MAilPoet
    print("Posting MailPoet data into CRM...")
    posting_mailpoet_data = post_subscriber_into_crm(custom_settings=settings)
    print(f"CRM data posted: {posting_mailpoet_data}")
    

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
    print("Successfully completed SingleM2C Mode.")
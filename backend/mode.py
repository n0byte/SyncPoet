from single_mode import single_mode as sm
from c2m_mode import c2m_mode as cm
from m2c_mode import m2c_mode as mm
from all_mode import all_mode as am

def single_mode():
    print("Single mode selected.")
    print("Starting single mode...")
    sm()  # ruft die Funktion aus single_mode.py auf
    print("Single mode finished.")

def c2m_mode():
    print("C2M mode selected.")
    print("Starting c2m mode...")
    cm()  # ruft die Funktion aus c2m_mode.py auf
    print("C2M mode finished.")

def m2c_mode():
    print("M2C mode selected.")
    print("Starting m2c mode...")
    mm()  # ruft die Funktion aus m2c_mode.py auf
    print("M2C mode finished.")

def all_mode():
    print("All mode selected.")
    print("Starting all mode...")
    am()  # ruft die Funktion aus all_mode.py auf
    print("All mode finished.")
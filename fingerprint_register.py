import serial
import adafruit_fingerprint
import pandas as pd
from datetime import datetime

# Setup Fingerprint Scanner (via CP2102)
uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

EXCEL_FILE = "team_members.xlsx"

def enroll_fingerprint():
    print("Enrolling fingerprint... Place your finger on the scanner.")
    while finger.get_fpdata(location=finger.FINGERPRINT_CHARBUFFER1) != adafruit_fingerprint.OK:
        pass
    finger.create_model()
    finger.store_model(finger.library_size + 1)  
    user_id = str(finger.library_size)
    print(f"Fingerprint saved with ID: {user_id}")
    return user_id

def register_new_user():
    user_id = enroll_fingerprint()
    name = input("Enter Name: ")
    branch = input("Enter Branch: ")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        df = pd.read_excel(EXCEL_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Name", "User ID", "Branch", "Timestamp"])

    new_entry = pd.DataFrame({"Name": [name], "User ID": [user_id], "Branch": [branch], "Timestamp": [timestamp]})
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)

    print(f"New user '{name}' registered successfully!")

if __name__ == "__main__":
    register_new_user()
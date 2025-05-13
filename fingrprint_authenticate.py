import serial
import adafruit_fingerprint
import requests
import pandas as pd
from datetime import datetime

uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

API_ENDPOINT = "http://_:5000/store_attendance" #change

EXCEL_FILE = "team_members.xlsx" #change

def load_existing_users():
    try:
        df = pd.read_excel(EXCEL_FILE)
        return df.set_index("ID").to_dict(orient="index")  
    except FileNotFoundError:
        return {}

def authenticate_fingerprint():
    print("Place your finger for authentication...")
    if finger.fingerprint_search() != adafruit_fingerprint.OK:
        print("Fingerprint not recognized. Please register first.")
        return None
    user_id = str(finger.finger_id)
    print(f"Authenticated! User ID: {user_id}")
    return user_id

def send_attendance(user_id, user_info):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = {
        "user_id": user_id,
        "name": user_info["Name"],
        "branch": user_info["Branch"],
        "degree": user_info["Degree"],
        "timestamp": timestamp
    }
    response = requests.post(API_ENDPOINT, json=payload)
    print("Attendance recorded:", response.text)

if __name__ == "__main__":
    users = load_existing_users()
    user_id = authenticate_fingerprint()

    if user_id and user_id in users:
        send_attendance(user_id, users[user_id])
    else:
        print("User not found in records. Please register first.")
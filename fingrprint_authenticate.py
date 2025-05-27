import time
import requests
from pyfingerprint.pyfingerprint import PyFingerprint

API_AUTH_URL = "http://YOUR_PC_IP:5000/authenticate_fingerprint"
API_UPDATE_URL = "http://YOUR_PC_IP:5000/update_fingerprint"

## Initialize fingerprint sensor
try:
    f = PyFingerprint('/dev/ttyAMA0', 57600, 0xFFFFFFFF, 0x00000000)

    if not f.verifyPassword():
        raise ValueError("The given fingerprint sensor password is wrong!")

except Exception as e:
    print("The fingerprint sensor could not be initialized!")
    print("Exception message:", str(e))
    exit(1)

print("Currently used templates:", f.getTemplateCount(), "/", f.getStorageCapacity())

## Authenticate or enroll fingerprint
try:
    print("Waiting for finger...")

    while not f.readImage():
        pass

    f.convertImage(0x01)

    result = f.searchTemplate()
    positionNumber = result[0]

    ## Step 1: Check if fingerprint exists on PC
    response = requests.post(API_AUTH_URL, json={"Template Position": positionNumber})

    if response.status_code == 200:
        auth_data = response.json()
        if auth_data.get("authenticated"):
            user_info = auth_data.get("user")
            print(f"Authentication successful! Welcome {user_info['Name']} (ID: {user_info['ID']})")
            exit(0)
        else:
            print("Fingerprint not found! Proceeding with enrollment...")

    ## Step 2: Enroll new fingerprint if not found
    print("Remove finger...")
    time.sleep(2)

    print("Waiting for same finger again...")

    while not f.readImage():
        pass

    f.convertImage(0x02)

    if f.compareCharacteristics() == 0:
        raise Exception("Fingers do not match")

    f.createTemplate()
    positionNumber = f.storeTemplate()
    print("Finger enrolled successfully!")
    print("New template position #", positionNumber)

    ## Step 3: Prompt user for details and send data to PC
    user_data = {
        "Name": input("Enter your Name: "),
        "ID": input("Enter your ID: "),
        "Branch": input("Enter your Branch: "),
        "Year": input("Enter your Year: "),
        "Template Position": positionNumber
    }

    response = requests.post(API_UPDATE_URL, json=user_data)

    if response.status_code == 200:
        print("Fingerprint data updated successfully on PC!")
    else:
        print("Failed to update fingerprint data:", response.text)

except Exception as e:
    print("Operation failed!")
    print("Exception message:", str(e))
    exit()
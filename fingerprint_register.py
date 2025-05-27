import time
import pandas as pd
from pyfingerprint.pyfingerprint import PyFingerprint

## Initialize fingerprint sensor
try:
    f = PyFingerprint('/dev/ttyAMA0', 57600, 0xFFFFFFFF, 0x00000000)

    if not f.verifyPassword():
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message:', str(e))
    exit(1)

print('Currently used templates:', f.getTemplateCount(), '/', f.getStorageCapacity())

## Enroll new fingerprint
try:
    print('Waiting for finger...')

    while not f.readImage():
        pass

    f.convertImage(0x01)

    result = f.searchTemplate()
    positionNumber = result[0]

    if positionNumber >= 0:
        print('Template already exists at position #', positionNumber)
        exit(0)

    print('Remove finger...')
    time.sleep(2)

    print('Waiting for same finger again...')

    while not f.readImage():
        pass

    f.convertImage(0x02)

    if f.compareCharacteristics() == 0:
        raise Exception('Fingers do not match')

    f.createTemplate()
    positionNumber = f.storeTemplate()
    print('Finger enrolled successfully!')
    print('New template position #', positionNumber)

    ## Prompt user for details
    name = input("Enter your Name: ")
    user_id = input("Enter your ID: ")
    branch = input("Enter your Branch: ")
    year = input("Enter your Year: ")

    ## Create data dictionary
    data = {'Name': [name], 'ID': [user_id], 'Branch': [branch], 'Year': [year], 'Template Position': [positionNumber]}

    ## Load existing data or create new Excel file
    try:
        df_existing = pd.read_excel('fingerprint_data.xlsx')
        df_new = pd.DataFrame(data)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    except FileNotFoundError:
        df_combined = pd.DataFrame(data)

    ## Save to Excel file
    df_combined.to_excel('fingerprint_data.xlsx', index=False)
    print('User details saved successfully!')

except Exception as e:
    print('Operation failed!')
    print('Exception message:', str(e))
    exit()
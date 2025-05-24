import serial.tools.list_ports

def check_fingerprint_sensor():
    ports = serial.tools.list_ports.comports()
    sensor_found = False

    print("Scanning available ports...")
    for port in ports:
        print(f"Found: {port.device}")
        if "USB" in port.device or "ttyUSB" in port.device or "ttyS" in port.device:
            sensor_found = True

    if sensor_found:
        print("Fingerprint sensor detected!")
    else:
        print("No fingerprint sensor detected. Check connections.")

if __name__ == "__main__":
    check_fingerprint_sensor()
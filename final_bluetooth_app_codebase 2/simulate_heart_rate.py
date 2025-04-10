import random
from bleak import BleakGATTCharacteristic

def simulate_heart_rate(client):
    """
    Simulate a heart rate measurement (e.g., 60-100 bpm).
    Updates the client with the simulated heart rate.
    """
    heart_rate = random.randint(60, 100)  # Simulate heart rate between 60-100 bpm
    print(f"Simulated Heart Rate: {heart_rate} bpm")
    
    # Assuming BleakClient or custom client has an `add_characteristic` method:
    heart_rate_char = BleakGATTCharacteristic('00002a37-0000-1000-8000-00805f9b34fb', value=bytes([heart_rate]))
    client.add_characteristic(heart_rate_char)

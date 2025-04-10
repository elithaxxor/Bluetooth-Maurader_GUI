import random

def simulate_battery_level(client):
    """
    Simulate a battery level for a Bluetooth device (0-100%).
    Updates the client with the simulated battery level.
    """
    battery_level = random.randint(0, 100)  # Simulate battery level as a random integer between 0 and 100
    print(f"Simulated Battery Level: {battery_level}%")
    
    # Assuming BleakClient or custom client has an `add_characteristic` method:
    battery_char = BleakGATTCharacteristic('00002a19-0000-1000-8000-00805f9b34fb', value=bytes([
    client.add_characteristic(battery_char)   
    

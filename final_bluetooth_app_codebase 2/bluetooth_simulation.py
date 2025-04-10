import subprocess
import random
import asyncio
from bleak import BleakClient, BleakGATTCharacteristic

# Function to start advertising a Bluetooth device
def start_advertising(ssid, service_uuid):
    """
    Simulate advertising a Bluetooth device with the given SSID and service UUID.
    """
    try:
        # Example command to start advertising with specific UUID and SSID
        command = f"sudo hcitool -i hci0 cmd 0x08 0x0008 0x00 0x00 {service_uuid}"
        subprocess.run(command, shell=True, check=True)
        print(f"Advertising started with SSID: {ssid} and Service UUID: {service_uuid}")
    except subprocess.CalledProcessError as e:
        print(f"Error starting advertising: {e}")

# Function to simulate pairing with a Bluetooth device
def simulate_pairing(device_mac):
    """
    Simulate pairing with a Bluetooth device using bluetoothctl.
    """
    try:
        commands = [
            f"echo -e 'agent on' | bluetoothctl",  # Enable the agent for pairing
            f"echo -e 'scan on' | bluetoothctl",  # Start scanning for devices
            f"echo -e 'pair {device_mac}' | bluetoothctl",  # Pair with the device
            f"echo -e 'trust {device_mac}' | bluetoothctl",  # Trust the device
            f"echo -e 'connect {device_mac}' | bluetoothctl"  # Connect to the device
        ]
        
        # Execute pairing commands
        for command in commands:
            subprocess.run(command, shell=True, check=True)

        print(f"Pairing with device {device_mac} simulated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during pairing: {e}")

# Function to simulate a battery level for a Bluetooth device (0-100%)
def simulate_battery_level(client):
    """
    Simulate a battery level for a Bluetooth device.
    """
    battery_level = random.randint(0, 100)  # Simulate battery level as a random integer between 0 and 100
    print(f"Simulated Battery Level: {battery_level}%")
    
    # Update the characteristic on the GATT server
    battery_char = BleakGATTCharacteristic('00002a19-0000-1000-8000-00805f9b34fb', value=bytes([battery_level]))
    client.add_characteristic(battery_char)

# Function to simulate a heart rate measurement (e.g., 60-100 bpm)
def simulate_heart_rate(client):
    """
    Simulate a heart rate measurement for a Bluetooth device.
    """
    heart_rate = random.randint(60, 100)  # Simulate heart rate between 60-100 bpm
    print(f"Simulated Heart Rate: {heart_rate} bpm")
    
    # Update the characteristic on the GATT server
    heart_rate_char = BleakGATTCharacteristic('00002a37-0000-1000-8000-00805f9b34fb', value=bytes([heart_rate]))
    client.add_characteristic(heart_rate_char)

# Asynchronous function to periodically update characteristics (e.g., battery level, heart rate)
async def periodic_updates(client):
    """
    Periodically simulate data changes for battery level, heart rate, etc.
    The updates are triggered every 5 seconds.
    """
    while True:
        simulate_battery_level(client)  # Simulate battery level
        simulate_heart_rate(client)     # Simulate heart rate
        await asyncio.sleep(5)  # Update every 5 seconds

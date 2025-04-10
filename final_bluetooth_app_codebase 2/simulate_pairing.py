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

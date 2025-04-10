**Purpose of the Repository**  
This repository appears to focus on simulating Bluetooth device functionalities such as advertising, pairing, and GATT service updates. It is designed to serve as a comprehensive tool for testing and simulating Bluetooth behaviors, possibly for development or debugging purposes. The README explains how to set up the environment using PyQt6 and Qt Designer for a frontend connected to backend functionalities.

**Features and Technologies**  
The repository uses Python alongside PyQt6 for its user interface and BlueZ tools for Bluetooth operations. Key features include:
- Starting BLE advertising using `hcitool`.
- Simulating pairing with devices using `bluetoothctl`.
- Generating random values to simulate battery levels and heart rate characteristics.
- Periodic updates of simulated GATT services using asynchronous programming (`asyncio`).  
The repository integrates these backend functionalities with a PyQt6-based GUI for user interaction, enabling actions like advertising and pairing through UI controls.

# 🔵 Bluetooth-Marauder GUI

<div align="center">
  <img src="https://img.shields.io/badge/Bluetooth-Simulation-blue?style=for-the-badge&logo=bluetooth&logoColor=white" alt="Bluetooth Simulation"/>
  <img src="https://img.shields.io/badge/Python-3.x-yellow?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.x"/>
  <img src="https://img.shields.io/badge/PyQt6-GUI-green?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt6 GUI"/>
  <img src="https://img.shields.io/badge/BlueZ-Tools-purple?style=for-the-badge&logo=linux&logoColor=white" alt="BlueZ Tools"/>
</div>

<p align="center">
  <img src="https://raw.githubusercontent.com/elithaxxor/Bluetooth-Maurader_GUI/main/assets/bluetooth_marauder_logo.png" alt="Bluetooth Marauder Logo" width="300"/>
</p>

> 📡 **Bluetooth-Marauder GUI**: A comprehensive toolkit for simulating, testing, and analyzing Bluetooth Low Energy device behaviors.

---

## 📋 Table of Contents

- [🌟 Overview](#-overview)
- [✨ Key Features](#-key-features)
- [🖥️ Screenshots](#️-screenshots)
- [🔧 Requirements](#-requirements)
- [🚀 Installation](#-installation)
- [🎮 Usage Guide](#-usage-guide)
- [📡 Bluetooth Simulation](#-bluetooth-simulation)
- [🔌 GATT Services](#-gatt-services)
- [🔄 Periodic Updates](#-periodic-updates)
- [🔐 Pairing Simulation](#-pairing-simulation)
- [📱 Fake Access Point](#-fake-access-point)
- [⚙️ Configuration](#️-configuration)
- [🧩 Module Breakdown](#-module-breakdown)
- [🛠️ Troubleshooting](#️-troubleshooting)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)

---

## 🌟 Overview

**Bluetooth-Marauder GUI** is a powerful Python-based application designed to simulate and test various Bluetooth Low Energy (BLE) functionalities. Built with PyQt6 for the frontend and leveraging BlueZ tools for backend operations, this toolkit allows developers, security researchers, and IoT enthusiasts to simulate BLE advertising, pairing processes, and GATT service updates in a controlled environment.

Whether you're developing BLE applications, testing device compatibility, or exploring Bluetooth security, Bluetooth-Marauder provides an intuitive interface to simulate real-world Bluetooth scenarios without requiring multiple physical devices.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 📡 **BLE Advertising** | Simulate device advertising with custom SSIDs and service UUIDs |
| 🔄 **GATT Simulation** | Generate and update simulated GATT services like Battery Level and Heart Rate |
| 🔌 **Pairing Process** | Test pairing and connection workflows with virtual or real devices |
| 📱 **Fake Access Point** | Create simulated Bluetooth access points for testing and development |
| ⏱️ **Periodic Updates** | Automatically update simulated characteristics at configurable intervals |
| 🎛️ **Customizable Parameters** | Configure all aspects of the Bluetooth simulation |
| 📊 **Real-time Monitoring** | Track and visualize Bluetooth activities and connections |
| 🔍 **Debugging Tools** | Analyze Bluetooth communications and troubleshoot connectivity issues |
| 📝 **Comprehensive Logging** | Detailed logs of all Bluetooth operations and events |
| 🎨 **Intuitive GUI** | User-friendly interface built with PyQt6 and Qt Designer |

---

## 🖥️ Screenshots

<div align="center">
  <img src="https://raw.githubusercontent.com/elithaxxor/Bluetooth-Maurader_GUI/main/assets/main_interface.png" alt="Main Interface" width="48%"/>
  <img src="https://raw.githubusercontent.com/elithaxxor/Bluetooth-Maurader_GUI/main/assets/gatt_simulation.png" alt="GATT Simulation" width="48%"/>
</div>

<div align="center">
  <img src="https://raw.githubusercontent.com/elithaxxor/Bluetooth-Maurader_GUI/main/assets/advertising_panel.png" alt="Advertising Panel" width="48%"/>
  <img src="https://raw.githubusercontent.com/elithaxxor/Bluetooth-Maurader_GUI/main/assets/fake_ap_settings.png" alt="Fake AP Settings" width="48%"/>
</div>

---

## 🔧 Requirements

### System Requirements

- 💻 Linux-based operating system (Ubuntu, Debian, Raspberry Pi OS recommended)
- 📡 Bluetooth adapter with BLE support
- 🔑 Root/sudo privileges for Bluetooth operations

### Software Dependencies

- 🐍 Python 3.6+
- 🔷 PyQt6
- 🔵 BlueZ tools (bluetoothctl, hcitool)
- 📚 Additional Python libraries (see requirements.txt)

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/elithaxxor/Bluetooth-Maurader_GUI.git
cd Bluetooth-Maurader_GUI/final_bluetooth_app_codebase\ 2/
```

### Step 2: Install System Dependencies

```bash
# For Debian/Ubuntu/Raspberry Pi OS
sudo apt update
sudo apt install -y python3-pip python3-dev bluez bluez-tools
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Permissions

```bash
# Allow Python to access Bluetooth without sudo
sudo setcap 'cap_net_raw,cap_net_admin+eip' $(which python3)
```

### Step 5: Launch the Application

```bash
python3 main.py
```

---

## 🎮 Usage Guide

### Main Interface

The application features a clean, intuitive interface with several tabs for different Bluetooth simulation functions:

1. **Advertising**: Configure and start BLE advertising
2. **GATT Services**: Simulate and update GATT characteristics
3. **Pairing**: Test device pairing and connection processes
4. **Fake AP**: Create simulated Bluetooth access points
5. **Settings**: Configure application and simulation parameters

### Quick Start Guide

1. **Start Advertising**:
   - Navigate to the Advertising tab
   - Enter your desired SSID and Service UUID
   - Click "Start Advertising"

2. **Simulate GATT Services**:
   - Go to the GATT Services tab
   - Select which services to simulate (Battery, Heart Rate, etc.)
   - Click "Start Simulation"

3. **Test Pairing**:
   - Enter the MAC address of a device
   - Click "Simulate Pairing"
   - Watch the pairing process in the log window

4. **Enable Periodic Updates**:
   - Configure update interval in Settings
   - Toggle "Periodic Updates" to ON
   - Service values will automatically update at the specified interval

---

## 📡 Bluetooth Simulation

The core of Bluetooth-Marauder is its ability to simulate various Bluetooth behaviors:

### BLE Advertising

```python
def start_advertising(ssid, service_uuid):
    """
    Start BLE advertising with the specified SSID and Service UUID.
    
    Args:
        ssid (str): The name to advertise
        service_uuid (str): The service UUID to include in advertisements
        
    Returns:
        bool: True if advertising started successfully, False otherwise
    """
    try:
        cmd = f"sudo hcitool -i hci0 cmd 0x08 0x0008 1E 02 01 06 03 03 {service_uuid} 0A 09 {ssid.encode().hex()}"
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        logging.info(f"Advertising started with SSID: {ssid}, UUID: {service_uuid}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to start advertising: {e}")
        return False
```

This function uses the BlueZ `hcitool` command to send advertising packets with your specified SSID and service UUID, allowing you to simulate any Bluetooth device.

---

## 🔌 GATT Services

Bluetooth-Marauder can simulate various GATT services and periodically update their values:

### Battery Level Simulation

```python
def simulate_battery_level(client):
    """
    Simulate a battery level reading and update the GATT characteristic.
    
    Args:
        client: The Bluetooth client connection
        
    Returns:
        int: The simulated battery level (0-100)
    """
    battery_level = random.randint(0, 100)
    battery_uuid = "00002a19-0000-1000-8000-00805f9b34fb"
    
    try:
        client.write_gatt_char(battery_uuid, bytes([battery_level]))
        logging.info(f"Battery level updated: {battery_level}%")
        return battery_level
    except Exception as e:
        logging.error(f"Failed to update battery level: {e}")
        return None
```

### Heart Rate Simulation

```python
def simulate_heart_rate(client):
    """
    Simulate a heart rate measurement and update the GATT characteristic.
    
    Args:
        client: The Bluetooth client connection
        
    Returns:
        int: The simulated heart rate (60-100 BPM)
    """
    heart_rate = random.randint(60, 100)
    hr_uuid = "00002a37-0000-1000-8000-00805f9b34fb"
    
    try:
        # Format according to Heart Rate Measurement characteristic format
        hr_data = bytes([0x00, heart_rate])  # 0x00 indicates format is uint8
        client.write_gatt_char(hr_uuid, hr_data)
        logging.info(f"Heart rate updated: {heart_rate} BPM")
        return heart_rate
    except Exception as e:
        logging.error(f"Failed to update heart rate: {e}")
        return None
```

---

## 🔄 Periodic Updates

To simulate real-world device behavior, Bluetooth-Marauder can automatically update GATT characteristics at regular intervals:

```python
async def periodic_updates(client, interval=5):
    """
    Periodically update simulated GATT characteristics.
    
    Args:
        client: The Bluetooth client connection
        interval (int): Time between updates in seconds
        
    Returns:
        None
    """
    while True:
        try:
            simulate_battery_level(client)
            simulate_heart_rate(client)
            await asyncio.sleep(interval)
        except Exception as e:
            logging.error(f"Error in periodic updates: {e}")
            break
```

This asynchronous function runs in the background, continuously updating the simulated characteristics to provide a realistic testing environment.

---

## 🔐 Pairing Simulation

Test the pairing process with real or virtual Bluetooth devices:

```python
def simulate_pairing(device_mac):
    """
    Simulate the pairing process with a Bluetooth device.
    
    Args:
        device_mac (str): MAC address of the target device
        
    Returns:
        bool: True if pairing was successful, False otherwise
    """
    try:
        # Create a script of bluetoothctl commands
        commands = [
            "agent on",
            "default-agent",
            "scan on",
            f"pair {device_mac}",
            f"trust {device_mac}",
            f"connect {device_mac}",
            "quit"
        ]
        
        # Execute the commands
        cmd = "echo '" + "
".join(commands) + "' | bluetoothctl"
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        
        # Check if pairing was successful
        if "successful" in result.stdout:
            logging.info(f"Successfully paired with device: {device_mac}")
            return True
        else:
            logging.warning(f"Pairing process completed but success not confirmed: {device_mac}")
            return False
            
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to pair with device {device_mac}: {e}")
        return False
```

---

## 📱 Fake Access Point

Create simulated Bluetooth access points for testing applications or security research:

```python
def create_fake_ap(ap_name, mac_address=None):
    """
    Create a fake Bluetooth access point.
    
    Args:
        ap_name (str): Name of the access point
        mac_address (str, optional): Custom MAC address for the AP
        
    Returns:
        bool: True if AP was created successfully, False otherwise
    """
    try:
        # Stop any existing advertising
        subprocess.run("sudo hciconfig hci0 noleadv", shell=True, check=True)
        
        # Set custom MAC if provided
        if mac_address:
            subprocess.run(f"sudo hciconfig hci0 down", shell=True, check=True)
            subprocess.run(f"sudo hciconfig hci0 hw {mac_address}", shell=True, check=True)
            subprocess.run(f"sudo hciconfig hci0 up", shell=True, check=True)
        
        # Configure and start the fake AP
        subprocess.run(f"sudo hciconfig hci0 name '{ap_name}'", shell=True, check=True)
        subprocess.run("sudo hciconfig hci0 leadv 3", shell=True, check=True)
        
        logging.info(f"Fake AP '{ap_name}' created successfully")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to create fake AP: {e}")
        return False
```

---

## ⚙️ Configuration

Bluetooth-Marauder uses a JSON configuration file (`settings.json`) to store application preferences and simulation parameters:

```json
{
  "bluetooth": {
    "default_interface": "hci0",
    "default_service_uuid": "180F",
    "scan_duration": 10,
    "update_interval": 5
  },
  "gui": {
    "theme": "dark",
    "log_level": "info",
    "auto_start_services": false,
    "show_advanced_options": false
  },
  "simulation": {
    "battery_level_range": [20, 100],
    "heart_rate_range": [60, 100],
    "temperature_range": [36.0, 37.5],
    "enable_random_disconnects": false
  }
}
```

---

## 🧩 Module Breakdown

Bluetooth-Marauder is organized into several Python modules, each handling specific functionality:

| Module | Description |
|--------|-------------|
| `main.py` | Application entry point and GUI initialization |
| `bluetooth_simulation.py` | Core Bluetooth simulation functions |
| `start_advertising.py` | BLE advertising functionality |
| `simulate_pairing.py` | Device pairing simulation |
| `simulate_battery_level.py` | Battery service simulation |
| `simulate_heart_rate.py` | Heart rate service simulation |
| `periodic_updates.py` | Asynchronous update scheduler |
| `fake_ap_window.py` | Fake access point creation interface |
| `backend.py` | Backend logic connecting GUI to Bluetooth functions |
| `ui_main.ui` | Qt Designer UI definition file |

---

## 🛠️ Troubleshooting

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| 🔴 **Permission Denied** | Run with sudo or set capabilities with `setc




pip install PyQt6


	2.	Open UI File in Qt Designer:
	•	Once you have Qt Designer installed, you can open the ui_main.ui file you downloaded from here:
Download ui_main.ui
	•	Open it using Qt Designer to view the layout and make further customizations.


```markdown

Explanation of Each Function:

	1.	start_advertising(ssid, service_uuid):
		•	This function starts BLE advertising using hcitool (a tool from BlueZ) with the specified SSID and Service 			UUID.
		•	It uses the sudo hcitool command to send advertising packets to simulate a Bluetooth device.
		* The function logs the result, or an error message if the advertising fails.
	2.	simulate_pairing(device_mac):
	•	This function simulates pairing and connection with a Bluetooth device using bluetoothctl commands.
	•	It runs several commands to enable pairing (agent on), scan for devices (scan on), pair with a device, and trust
		connect the device using its MAC address.
	•	The function assumes that the MAC address of the device is passed as an argument.
	3.	simulate_battery_level(client):
		•	This function simulates the battery level of a Bluetooth device by randomly generating a number between 0 			and 100.
		•	It then updates the Battery Level characteristic on the Bluetooth device.
		•	The UUID for the Battery Level characteristic is 00002a19-0000-1000-8000-00805f9b34fb, which is used to 			write the simulated value to the GATT server.
	4.	simulate_heart_rate(client):
		•	This function simulates the heart rate measurement for a Bluetooth device by generating a random number 			between 60 and 100.
		•	The Heart Rate Measurement characteristic is updated with this value.
		•	The UUID for the Heart Rate Measurement characteristic is 00002a37-0000-1000-8000-00805f9b34fb.
	5.	periodic_updates(client):
		•	This function runs asynchronously and periodically simulates updates for the battery level and heart rate 			every 5 seconds.
		•	The asyncio.sleep(5) call introduces a 5-second delay between each update, so that the simulated data is 			updated in real-time.

⸻

Usage:
	•	To use these functions, you would need to call them from your frontend (PyQt6) code, which has access to Bluetooth devices and the required information (such as SSID, device MAC address, and UUID).
	•	The periodic_updates function runs in the background and will continue to update the characteristics as long as the simulation is active.
	•	Advertising and Pairing can be triggered by user interactions (like pressing buttons or entering a MAC address in the UI).

Integration with Frontend:

The backend logic should be connected to buttons and fields in your PyQt6 frontend. For example:
	•	The Start Advertising button can call start_advertising(ssid, service_uuid).
	•	The Simulate Pairing button can call simulate_pairing(device_mac).
	•	The Simulate GATT Services button can call the simulate_battery_level and simulate_heart_rate functions.
	•	The Start Periodic Updates button can trigger periodic_updates(client).

```

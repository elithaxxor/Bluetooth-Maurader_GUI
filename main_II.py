
import sys
import subprocess
import asyncio
import logging
import json
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QStatusBar, QVBoxLayout, QSpinBox, QPushButton, QTextEdit, QLabel, QComboBox, QGroupBox, QRadioButton, QFormLayout, QTabWidget, QSplitter
from bleak import BleakScanner, BleakClient, _logger
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Example UUIDs for different services
HEART_RATE_SERVICE_UUID = "0000180D-0000-1000-8000-00805f9b34fb"
HEART_RATE_MEASUREMENT_CHAR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
BATTERY_SERVICE_UUID = "0000180F-0000-1000-8000-00805f9b34fb"
BATTERY_LEVEL_CHAR_UUID = "00002a19-0000-1000-8000-00805f9b34fb"
VOLUME_CONTROL_SERVICE_UUID = "0000f000-0000-1000-8000-00805f9b34fb"  # Hypothetical UUID for volume control (depends on device)

# Hardcoded device services and UUIDs
DEVICE_CHOICES = {
    "Heart Rate Monitor": {
        "service_uuid": HEART_RATE_SERVICE_UUID,
        "characteristic_uuid": HEART_RATE_MEASUREMENT_CHAR_UUID,
        "description": "Simulating Heart Rate Measurement",
        "characteristics": ["Heart Rate Measurement"],
    },
    "iPhone": {
        "service_uuid": BATTERY_SERVICE_UUID,
        "characteristic_uuid": BATTERY_LEVEL_CHAR_UUID,
        "description": "Simulating iPhone Battery Level",
        "characteristics": ["Battery Level"],
    },
    "Samsung": {
        "service_uuid": BATTERY_SERVICE_UUID,
        "characteristic_uuid": BATTERY_LEVEL_CHAR_UUID,
        "description": "Simulating Samsung Battery Level",
        "characteristics": ["Battery Level"],
    },
    "Bose Headphones": {
        "service_uuid": BATTERY_SERVICE_UUID,
        "characteristic_uuid": BATTERY_LEVEL_CHAR_UUID,
        "description": "Simulating Bose Headphones Battery Level",
        "characteristics": ["Battery Level", "Volume Control"],
    },
    "Beats Headphones": {
        "service_uuid": BATTERY_SERVICE_UUID,
        "characteristic_uuid": BATTERY_LEVEL_CHAR_UUID,
        "description": "Simulating Beats Headphones Battery Level",
        "characteristics": ["Battery Level", "Volume Control"],
    }
}

class FakeAPWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui_main.ui', self)  # Load the UI created with Qt Designer

        # Initialize variables for Bluetooth and settings
        self.available_devices = []
        self.device_selector = self.device_selector_combo
        self.noise_level_input = self.noise_level_spinbox
        self.verbose_log = self.verbose_log_textedit
        self.status_bar = self.statusbar()

        # Customizing the UI components
        self.status_bar.showMessage('Ready')

        # Button connections
        self.start_button.clicked.connect(self.start_fake_ap)
        self.stop_button.clicked.connect(self.stop_fake_ap)
        self.scan_button.clicked.connect(self.scan_for_devices)

        # Load user settings (e.g., last device, noise level)
        self.load_settings()

        # Bluetooth visualization setup
        self.fig, self.ax = plt.subplots()
        self.x_vals, self.y_vals = [], []

    def start_fake_ap(self):
        # Start the Fake AP based on the selected options
        ssid = self.ssid_input.text()
        channel = self.channel_selector.currentText()
        self.interface = self.interface_selector.currentText()

        if not ssid:
            self.status_bar.showMessage("Error: SSID cannot be empty!", 3000)
            return

        self.status_bar.showMessage(f"Starting Fake AP '{ssid}' on {self.interface}...", 3000)

        # Placeholder: Implement Fake AP logic here
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_fake_ap(self):
        # Stop the Fake AP and all related processes
        self.status_bar.showMessage("Stopping Fake AP...", 3000)
        
        # Placeholder: Implement logic to stop Fake AP here
        subprocess.run(["pkill", "airbase-ng"])  # Placeholder for process termination

        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def scan_for_devices(self):
        # Scan for nearby Bluetooth devices and populate the dropdown list
        self.status_bar.showMessage("Scanning for devices...")
        
        # Scanning for devices
        scanner = BleakScanner()
        devices = asyncio.run(scanner.discover())
        self.available_devices = devices

        # Update the dropdown list with device names
        device_names = [device.name if device.name else "Unnamed Device" for device in devices]
        self.device_selector.clear()
        self.device_selector.addItems(device_names)

        self.status_bar.showMessage(f"Found {len(devices)} devices.", 3000)

    def log_event(self, event):
        # Log events to the verbose log panel
        self.verbose_log.append(event)

    def calculate_distance(self, rssi, A=-59, n=2):
        # Calculate distance using the RSSI and the path loss model
        try:
            distance = 10 ** ((A - rssi) / (10 * n))
            return distance
        except Exception as e:
            logging.error(f"Error calculating distance: {str(e)}")
            return None

    def update_distance(self, client):
        # Update the distance based on RSSI and the user-specified path loss exponent
        rssi_value = client.rssi
        noise_level = self.noise_level_input.value()  # Get user-selected path loss exponent
        
        # Calculate the estimated distance
        distance = self.calculate_distance(rssi_value, n=noise_level)
        
        # Log the calculated distance in the verbose log
        if distance is not None:
            self.log_event(f"Estimated Distance from Device: {distance:.2f} meters (RSSI: {rssi_value} dBm)")

    async def replicate_services(self, device):
        # Replicate Bluetooth GATT services using pybluez and calculate distance from RSSI
        self.status_bar.showMessage(f"Simulating GATT Service for {device.name}...", 3000)

        # Example: Simulating GATT services from the device
        # Use BleakClient or another library to interact with the device's services
        async with BleakClient(device) as client:
            try:
                services = await client.get_services()
                for service in services:
                    self.log_event(f"Service: {service.uuid}")

                    if service.uuid == BATTERY_SERVICE_UUID:
                        battery_level = await client.read_gatt_char(BATTERY_LEVEL_CHAR_UUID)
                        self.log_event(f"Battery Level: {battery_level[0]}%")
                        self.update_distance(client)
                        await asyncio.sleep(5)  # Real-time updates

                    if service.uuid == HEART_RATE_SERVICE_UUID:
                        heart_rate = await client.read_gatt_char(HEART_RATE_MEASUREMENT_CHAR_UUID)
                        self.log_event(f"Heart Rate: {heart_rate[0]}")
                        self.update_distance(client)
                        await asyncio.sleep(5)  # Real-time updates

            except Exception as e:
                self.log_event(f"Error: {str(e)}")
                self.status_bar.showMessage(f"Error: {str(e)}", 3000)

    def save_settings(self):
        # Save user settings like last connected device and noise level
        settings = {
            'last_device': self.device_selector.currentText(),
            'noise_level': self.noise_level_input.value()
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

    def load_settings(self):
        # Load user settings from the saved configuration file
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.device_selector.setCurrentText(settings.get('last_device', ''))
                self.noise_level_input.setValue(settings.get('noise_level', 2))
        except FileNotFoundError:
            pass

    def plot_data(self):
        # Plot real-time data from Bluetooth devices (e.g., Battery level, Heart rate)
        def update(frame):
            self.x_vals.append(frame)
            self.y_vals.append(self.get_battery_level())  # Fetch real-time data
            self.ax.clear()
            self.ax.plot(self.x_vals, self.y_vals)

        ani = FuncAnimation(self.fig, update, frames=range(100), interval=1000)
        plt.show()

    def get_battery_level(self):
        # Placeholder for real battery level data fetching
        return 50  # Simulate a static value for now

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FakeAPWindow()
    window.show()
    sys.exit(app.exec())

import sys
import subprocess
import asyncio
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QRadioButton, QGroupBox, QFormLayout, QTabWidget, QStatusBar, QTextEdit, QSpinBox, QSlider

from bleak import BleakScanner, BleakClient, _logger

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

class FakeAPWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fake Access Point - EvilAP")
        self.setWindowIcon(QIcon("icon.png"))  # Use a mac-style icon here
        self.setGeometry(100, 100, 800, 600)

        self.interface = "wlan0"  # Default, change as needed
        self.ss_id = ""
        self.channel = 6
        self.mode = "discovery"  # Default mode
        self.available_devices = []

        self.init_ui()

    def init_ui(self):
        # Layouts
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()
        controls_layout = QHBoxLayout()

        # Mode selector
        self.mode_group = QGroupBox("Select Mode")
        self.discovery_radio = QRadioButton("Discovery Mode")
        self.persistent_radio = QRadioButton("Persistent Mode")
        self.discovery_radio.setChecked(True)  # Default to Discovery Mode
        self.discovery_radio.toggled.connect(self.toggle_mode)
        
        mode_layout = QVBoxLayout()
        mode_layout.addWidget(self.discovery_radio)
        mode_layout.addWidget(self.persistent_radio)
        self.mode_group.setLayout(mode_layout)

        # SSID Input
        self.ssid_input = QLineEdit(self)
        self.ssid_input.setPlaceholderText("Enter Fake AP SSID")
        form_layout.addRow("SSID: ", self.ssid_input)

        # Channel Selector
        self.channel_selector = QComboBox(self)
        self.channel_selector.addItems([str(i) for i in range(1, 15)])  # 1-14 channels
        self.channel_selector.setCurrentText("6")  # Default channel
        form_layout.addRow("Channel: ", self.channel_selector)

        # Interface Selector
        self.interface_selector = QComboBox(self)
        self.interface_selector.addItems(self.get_wireless_interfaces())
        form_layout.addRow("Interface: ", self.interface_selector)

        # Noise (Path Loss Exponent) Input
        self.noise_level_input = QSpinBox(self)
        self.noise_level_input.setRange(2, 6)
        self.noise_level_input.setValue(2)  # Default to 2 (Free space)
        self.noise_level_input.setSuffix(' (n)')
        form_layout.addRow("Path Loss Exponent (n): ", self.noise_level_input)

        # Start/Stop Buttons
        self.start_button = QPushButton("Start Fake AP")
        self.start_button.clicked.connect(self.start_fake_ap)
        
        self.stop_button = QPushButton("Stop Fake AP")
        self.stop_button.clicked.connect(self.stop_fake_ap)
        self.stop_button.setEnabled(False)  # Initially disabled

        controls_layout.addWidget(self.start_button)
        controls_layout.addWidget(self.stop_button)

        # Simulation Tab for GATT Services
        self.simulation_tab = QWidget()
        self.simulation_tab_layout = QVBoxLayout()

        self.simulation_radio_group = QGroupBox("Choose Simulation Type")
        self.device_selector = QComboBox(self)  # Dropdown for selecting device
        self.device_selector.setPlaceholderText("Detecting Devices...")
        self.simulation_radio_group.setLayout(QVBoxLayout())
        self.simulation_radio_group.layout().addWidget(self.device_selector)

        self.simulation_button = QPushButton("Start Simulation")
        self.simulation_button.clicked.connect(self.start_simulation)

        # Buttons for Real-Time Updates Control
        self.pause_button = QPushButton("Pause Updates")
        self.pause_button.clicked.connect(self.toggle_real_time_updates)
        self.pause_button.setEnabled(False)  # Initially disabled
        self.resume_button = QPushButton("Resume Updates")
        self.resume_button.clicked.connect(self.toggle_real_time_updates)
        self.resume_button.setEnabled(False)  # Initially disabled

        self.simulation_tab_layout.addWidget(self.simulation_radio_group)
        self.simulation_tab_layout.addWidget(self.simulation_button)
        self.simulation_tab_layout.addWidget(self.pause_button)
        self.simulation_tab_layout.addWidget(self.resume_button)

        # Verbose Log Text Area
        self.verbose_log = QTextEdit(self)
        self.verbose_log.setReadOnly(True)
        self.simulation_tab_layout.addWidget(QLabel("Verbose Log"))
        self.simulation_tab_layout.addWidget(self.verbose_log)

        # Clear Log Button
        self.clear_log_button = QPushButton("Clear Log")
        self.clear_log_button.clicked.connect(self.clear_log)
        self.simulation_tab_layout.addWidget(self.clear_log_button)

        # Log Display Section
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(self.simulation_tab)
        splitter.addWidget(QLabel("Service Logs"))
        splitter.addWidget(self.verbose_log)

        # Tab Widget
        self.tabs = QTabWidget()
        self.tabs.addTab(splitter, "Simulation & Replication")
        self.tabs.addTab(QWidget(), "Fake AP")

        # Status Bar
        self.status_bar = QStatusBar(self)
        self.status_bar.showMessage("Ready")

        # Adding widgets to main layout
        main_layout.addWidget(self.tabs)
        main_layout.addWidget(self.status_bar)
        self.setLayout(main_layout)

        # Start scanning for devices
        self.scan_for_devices()

    def toggle_mode(self):
        """Toggle between discovery and persistent modes."""
        if self.discovery_radio.isChecked():
            self.mode = "discovery"
        else:
            self.mode = "persistent"

    def get_wireless_interfaces(self):
        """Retrieve available wireless interfaces."""
        return ["wlan0", "wlan1"]  # Dummy example

    def calculate_distance(self, rssi, A=-59, n=2):
        """
        Calculate distance using the RSSI and the path loss model.
        
        :param rssi: RSSI value in dBm.
        :param A: Reference RSSI at 1 meter (default is -59 for many Bluetooth devices).
        :param n: Path loss exponent (default is 2 for line-of-sight).
        :return: Estimated distance in meters.
        """
        try:
            distance = 10 ** ((A - rssi) / (10 * n))
            return distance
        except Exception as e:
            print(f"Error calculating distance: {str(e)}")
            return None

    async def scan_for_devices(self):
        """Scan for BLE devices and populate the dropdown list."""
        self.status_bar.showMessage("Scanning for devices...", 3000)
        
        # Scanning for devices
        scanner = BleakScanner()
        devices = await scanner.discover()
        self.available_devices = devices

        # Update the dropdown list with device names
        device_names = [device.name if device.name else "Unnamed Device" for device in devices]
        self.device_selector.clear()
        self.device_selector.addItems(device_names)

        self.status_bar.showMessage(f"Found {len(devices)} devices.", 3000)

    def toggle_real_time_updates(self):
        """Pause or resume real-time updates for device characteristics."""
        if self.pause_button.isEnabled():
            self.pause_button.setEnabled(False)
            self.resume_button.setEnabled(True)
        else:
            self.pause_button.setEnabled(True)
            self.resume_button.setEnabled(False)

    def start_simulation(self):
        """Start simulation based on user selection."""
        selected_device_name = self.device_selector.currentText()

        # Find the device object based on the name
        selected_device = next((device for device in self.available_devices if device.name == selected_device_name), None)

        if selected_device:
            self.status_bar.showMessage(f"Simulating services for {selected_device_name}...", 3000)
            asyncio.create_task(self.replicate

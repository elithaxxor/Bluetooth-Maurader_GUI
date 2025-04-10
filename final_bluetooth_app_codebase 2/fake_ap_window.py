import sys
import asyncio
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QRadioButton, QGroupBox, QFormLayout, QTabWidget, QStatusBar, QTextEdit, QSpinBox, QSplitter

from bluetooth_simulation import start_advertising, simulate_pairing, simulate_battery_level, simulate_heart_rate, periodic_updates

class FakeAPWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bluetooth Device Simulation")
        self.setWindowIcon(QIcon("icon.png"))  # Use a mac-style icon here
        self.setGeometry(100, 100, 800, 600)

        self.interface = "wlan0"  # Default interface
        self.mode = "discovery"  # Default mode
        self.device_mac = ""
        self.available_devices = []

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()
        controls_layout = QHBoxLayout()

        # Mode selector for Fake AP
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

        # Service UUID Input (for Bluetooth advertising)
        self.service_uuid_input = QLineEdit(self)
        self.service_uuid_input.setPlaceholderText("Enter Bluetooth Service UUID")
        form_layout.addRow("Service UUID: ", self.service_uuid_input)

        # Channel Selector for Fake AP
        self.channel_selector = QComboBox(self)
        self.channel_selector.addItems([str(i) for i in range(1, 15)])
        self.channel_selector.setCurrentText("6")  # Default channel
        form_layout.addRow("Channel: ", self.channel_selector)

        # Interface Selector
        self.interface_selector = QComboBox(self)
        self.interface_selector.addItems(self.get_wireless_interfaces())
        form_layout.addRow("Interface: ", self.interface_selector)

        # Path Loss Exponent (n) Input for Distance Calculation
        self.noise_level_input = QSpinBox(self)
        self.noise_level_input.setRange(2, 6)
        self.noise_level_input.setValue(2)
        self.noise_level_input.setSuffix(' (n)')
        form_layout.addRow("Path Loss Exponent (n): ", self.noise_level_input)

        # Start/Stop Buttons for Fake AP
        self.start_button = QPushButton("Start Fake AP")
        self.start_button.clicked.connect(self.start_fake_ap)
        
        self.stop_button = QPushButton("Stop Fake AP")
        self.stop_button.clicked.connect(self.stop_fake_ap)
        self.stop_button.setEnabled(False)  # Initially disabled

        controls_layout.addWidget(self.start_button)
        controls_layout.addWidget(self.stop_button)

        # Simulation Tab for Bluetooth GATT Services
        self.simulation_tab = QWidget()
        self.simulation_tab_layout = QVBoxLayout()

        self.device_selector = QComboBox(self)
        self.device_selector.setPlaceholderText("Detecting Devices...")

        self.simulation_button = QPushButton("Start Simulation")
        self.simulation_button.clicked.connect(self.start_simulation)

        self.simulation_tab_layout.addWidget(QLabel("Simulate Device"))
        self.simulation_tab_layout.addWidget(self.device_selector)
        self.simulation_tab_layout.addWidget(self.simulation_button)

        # Buttons for Real-Time Updates Control
        self.update_button = QPushButton("Start Periodic Updates")
        self.update_button.clicked.connect(self.toggle_periodic_updates)
        self.update_button.setEnabled(False)  # Initially disabled

        self.simulation_tab_layout.addWidget(self.update_button)

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
        splitter.addWidget(self.verbose_log)

        # Tab Widget for organizing Fake AP and Simulation
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

    def start_fake_ap(self):
        """Start the Fake AP based on the selected options."""
        ssid = self.ssid_input.text()
        channel = self.channel_selector.currentText()
        self.interface = self.interface_selector.currentText()

        if not ssid:
            self.status_bar.showMessage("Error: SSID cannot be empty!", 3000)
            return

        self.status_bar.showMessage(f"Starting {self.mode.capitalize()} Fake AP with SSID '{ssid}' on {self.interface}...", 3000)

        if self.mode == "discovery":
            self.start_discovery_mode(ssid, channel)
        else:
            self.start_persistent_mode(ssid, channel)

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_fake_ap(self):
        """Stop the Fake AP and all related processes."""
        self.status_bar.showMessage("Stopping Fake AP...", 3000)
        
        subprocess.run(["pkill", "airbase-ng"])

        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def start_discovery_mode(self, ssid, channel):
        """Start airbase-ng in discovery mode."""
        subprocess.Popen(["airbase-ng", "-e", ssid, "-c", str(channel), self.interface])

    def start_persistent_mode(self, ssid, channel):
        """Start hostapd and dnsmasq for persistent mode."""
        subprocess.Popen(["hostapd", "/tmp/hostapd.conf"])
        subprocess.Popen(["dnsmasq", "-C", "/tmp/dnsmasq.conf"])

    def start_simulation(self):
        """Start simulation based on user selection."""
        selected_device_name = self.device_selector.currentText()

        if selected_device_name:
            self.status_bar.showMessage(f"Simulating services for {selected_device_name}...", 3000)
            asyncio.create_task(self.replicate_services(selected_device_name))
        else:
            self.status_bar.showMessage("Error: No device selected!", 3000)

    async def replicate_services(self, device_name):
        """Simulate Bluetooth GATT services."""
        self.status_bar.showMessage(f"Simulating GATT Service for {device_name}...", 3000)
        # Add Bluetooth GATT characteristics simulation here

    def toggle_periodic_updates(self):
        """Start or stop periodic updates for simulated GATT characteristics."""
        if self.update_button.text() == "Start Periodic Updates":
            self.update_button.setText("Stop Periodic Updates")
            self.status_bar.showMessage("Periodic updates started.")
            # Start periodic updates
            device_mac = self.device_mac_input.text()  # Assuming there's a device MAC input
            if device_mac:
                asyncio.create_task(periodic_updates(device_mac))  # Trigger periodic updates
            else:
                self.status_bar.showMessage("Error: Please provide a device MAC address", 3000)
        else:
            self.update_button.setText("Start Periodic Updates")
            self.status_bar.showMessage("Periodic updates stopped.")
            # Stop periodic updates by canceling tasks or stopping them manually
            # This would require maintaining a reference to the task if needed for stopping.

    def clear_log(self):
        """Clear the log output."""
        self.verbose_log.clear()

    def scan_for_devices(self):
        """Scan for Bluetooth devices and populate the dropdown list."""
        self.status_bar.showMessage("Scanning for devices...", 3000)
        
        # Example: Simulate device scan
        # Replace with actual scanning logic with BleakScanner if required
        self.available_devices = ["Device 1", "Device 2", "Device 3"]  # Simulated devices
        device_names = self.available_devices

        self.device_selector.clear()
        self.device_selector.addItems(device_names)
        self.status_bar.showMessage(f"Found {len(self.available_devices)} devices.", 3000)

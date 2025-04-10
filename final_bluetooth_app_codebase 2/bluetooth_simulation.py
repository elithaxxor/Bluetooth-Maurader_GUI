import sys
import subprocess
import asyncio
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QRadioButton, QGroupBox, QFormLayout, QTabWidget, QStatusBar, QTextEdit, QSpinBox, QSlider
from bluetooth_simulation import start_advertising, simulate_pairing, simulate_battery_level, simulate_heart_rate, periodic_updates

class FakeAPWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bluetooth Simulation")
        self.setWindowIcon(QIcon("icon.png"))  # Use a mac-style icon here
        self.setGeometry(100, 100, 800, 600)

        self.interface = "wlan0"
        self.mode = "discovery"  # Default mode

        self.init_ui()

    def init_ui(self):
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
        self.channel_selector.addItems([str(i) for i in range(1, 15)])
        self.channel_selector.setCurrentText("6")  # Default channel
        form_layout.addRow("Channel: ", self.channel_selector)

        # Interface Selector
        self.interface_selector = QComboBox(self)
        self.interface_selector.addItems(self.get_wireless_interfaces())
        form_layout.addRow("Interface: ", self.interface_selector)

        # Noise (Path Loss Exponent) Input
        self.noise_level_input = QSpinBox(self)
        self.noise_level_input.setRange(2, 6)
        self.noise_level_input.setValue(2)
        self.noise_level_input.setSuffix(' (n)')
        form_layout.addRow("Path Loss Exponent (n): ", self.noise_level_input)

        # Start/Stop Buttons
        self.start_button = QPushButton("Start Fake AP")
        self.start_button.clicked.connect(self.start_fake_ap)
        
        self.stop_button = QPushButton("Stop Fake AP")
        self.stop_button.clicked.connect(self.stop_fake_ap)
        self.stop_button.setEnabled(False)

        controls_layout.addWidget(self.start_button)
        controls_layout.addWidget(self.stop_button)

        # Simulation Tab for GATT Services
        self.simulation_tab = QWidget()
        self.simulation_tab_layout = QVBoxLayout()

        self.simulation_radio_group = QGroupBox("Choose Simulation Type")
        self.device_selector = QComboBox(self)
        self.device_selector.setPlaceholderText("Detecting Devices...")
        self.simulation_radio_group.setLayout(QVBoxLayout())
        self.simulation_radio_group.layout().addWidget(self.device_selector)

        self.simulation_button = QPushButton("Start Simulation")
        self.simulation_button.clicked.connect(self.start_simulation)

        # Buttons for Real-Time Updates Control
        self.pause_button = QPushButton("Pause Updates")
        self.pause_button.clicked.connect(self.toggle_real_time_updates)
        self.pause_button.setEnabled(False)
        self.resume_button = QPushButton("Resume Updates")
        self.resume_button.clicked.connect(self.toggle_real_time_updates)
        self.resume_button.setEnabled(False)

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

    def start_simulation(self):
        """Start simulation based on user selection."""
        selected_device_name = self.device_selector.currentText()

        # Find the device object based on the name
        selected_device = next((device for device in self.available_devices if device.name == selected_device_name), None)

        if selected_device:
            self.status_bar.showMessage(f"Simulating services for {selected_device_name}...", 3000)
            asyncio.create_task(self.replicate_services(selected_device))
        else:
            self.status_bar.showMessage("Error: No device selected!", 3000)

    async def replicate_services(self, device):
        """Simulate Bluetooth GATT services using pybluez and calculate distance from RSSI."""
        self.status_bar.showMessage(f"Simulating GATT Service for {device.name}...", 3000)

        async with BleakClient(device) as client:
            try:
                services = await client.get_services()
                for service in services:
                    self.log_event(f"Service: {service.uuid}")

                    if service.uuid == BATTERY_SERVICE_UUID:
                        battery_level = await client.read_gatt_char(BATTERY_LEVEL_CHAR_UUID)
                        self.log_event(f"Battery Level: {battery_level[0]}%")
                        self.update_distance(client)
                        await asyncio.sleep(5)

                    if service.uuid == HEART_RATE_SERVICE_UUID:
                        heart_rate = await client.read_gatt_char(HEART_RATE_MEASUREMENT_CHAR_UUID)
                        self.log_event(f"Heart Rate: {

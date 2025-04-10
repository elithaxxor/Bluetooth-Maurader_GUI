
# BLE Scanner GUI App with Real-Time Charts and Analytics

import asyncio
import threading
import sqlite3
import time
from datetime import datetime
from bleak import BleakScanner
from PyQt5 import QtWidgets, QtCore
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# SQLite Helper Class
class BLEDatabase:
    def __init__(self, db_file='ble_data.db'):
        self.db_file = db_file
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS devices (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        mac TEXT,
                        rssi INTEGER,
                        timestamp TEXT
                    )''')
        conn.commit()
        conn.close()

    def log_device(self, name, mac, rssi):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("INSERT INTO devices (name, mac, rssi, timestamp) VALUES (?, ?, ?, ?)",
                  (name, mac, rssi, datetime.now().isoformat()))
        conn.commit()
        conn.close()

    def get_latest_devices(self, limit=50):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT name, mac, rssi, timestamp FROM devices ORDER BY timestamp DESC LIMIT ?", (limit,))
        data = c.fetchall()
        conn.close()
        return data

# BLE Scanner Thread
class BLEScanner(QtCore.QThread):
    device_found = QtCore.pyqtSignal(str, str, int)

    def __init__(self):
        super().__init__()
        self.running = True

    async def scan(self):
        def detection_callback(device, advertisement_data):
            if device.name:
                self.device_found.emit(device.name, device.address, device.rssi)

        scanner = BleakScanner(detection_callback)
        await scanner.start()
        await asyncio.sleep(10)
        await scanner.stop()

    def run(self):
        while self.running:
            asyncio.run(self.scan())

    def stop(self):
        self.running = False

# Matplotlib Chart Widget
class RSSIChart(FigureCanvas):
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)
        self.ax.set_title("Real-Time RSSI Chart")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("RSSI")
        self.device_data = {}

    def update_chart(self, name, rssi):
        timestamp = datetime.now().strftime("%H:%M:%S")
        if name not in self.device_data:
            self.device_data[name] = {'times': [], 'rssis': []}
        self.device_data[name]['times'].append(timestamp)
        self.device_data[name]['rssis'].append(rssi)

        self.ax.clear()
        for device, data in self.device_data.items():
            self.ax.plot(data['times'][-10:], data['rssis'][-10:], label=device)
        self.ax.set_title("Real-Time RSSI Chart")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("RSSI")
        self.ax.legend(loc='upper right')
        self.draw()

# Main GUI Application
class BLEApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BLE Scanner with Real-Time Analytics")
        self.resize(800, 600)
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.chart = RSSIChart()
        self.layout.addWidget(self.chart)

        self.device_log = QtWidgets.QTextEdit()
        self.layout.addWidget(self.device_log)

        self.start_button = QtWidgets.QPushButton("Start Scan")
        self.stop_button = QtWidgets.QPushButton("Stop Scan")
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.start_button)
        btn_layout.addWidget(self.stop_button)
        self.layout.addLayout(btn_layout)

        self.db = BLEDatabase()
        self.scanner = BLEScanner()
        self.scanner.device_found.connect(self.on_device_found)

        self.start_button.clicked.connect(self.start_scan)
        self.stop_button.clicked.connect(self.stop_scan)

    def start_scan(self):
        self.device_log.append("Scanning started...")
        self.scanner.start()

    def stop_scan(self):
        self.device_log.append("Scanning stopped.")
        self.scanner.stop()

    def on_device_found(self, name, mac, rssi):
        entry = f"{datetime.now().strftime('%H:%M:%S')} - Found {name} ({mac}) RSSI: {rssi}"
        self.device_log.append(entry)
        self.db.log_device(name, mac, rssi)
        self.chart.update_chart(name, rssi)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = BLEApp()
    window.show()
    app.exec_()

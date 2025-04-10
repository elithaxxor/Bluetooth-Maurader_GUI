import sys
from PyQt6.QtWidgets import QApplication
from fake_ap_window import FakeAPWindow  # Import the main window class

# Entry point for the application
if __name__ == "__main__":
    # Initialize the application
    app = QApplication(sys.argv)  # Create the application

    # Create an instance of the main window (FakeAPWindow)
    window = FakeAPWindow()

    # Show the window
    window.show()

    # Enter the application's main event loop
    sys.exit(app.exec())  # Start the event loop and handle events until the application closes

from typing import Optional
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, QLabel,
                             QLineEdit, QComboBox, QCheckBox, QPushButton,
                             QStatusBar, QMessageBox)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QColor, QDoubleValidator
from pytxr import Txr
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Debug logging for troubleshooting
logger = logging.getLogger(__name__)

class TxrGUI(QMainWindow):
    """GUI for controlling an S-band transceiver using the pytxr package."""

    def __init__(self, port: Optional[str] = None):
        """Initialize the GUI and connect to the transceiver.

        Args:
            port (Optional[str]): Serial port for the transceiver. If None, autodetect.
        """
        super().__init__()
        self.txr: Optional[Txr] = None
        self.init_transceiver(port)
        self.init_ui()
        self.refresh_settings()
        self.start_polling()

    def init_transceiver(self, port: Optional[str]) -> None:
        """Initialize the Txr object and handle connection errors."""
        try:
            self.txr = Txr(port)
            logger.info("Transceiver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize transceiver: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", f"Failed to connect to transceiver: {e}")
            sys.exit(1)

    def init_ui(self) -> None:
        """Set up the GUI layout and widgets."""
        self.setWindowTitle("S-Band Transceiver Control (ADF4351)")
        self.setGeometry(100, 100, 400, 300)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout(central_widget)

        # Frequency (in GHz)
        self.freq_label = QLabel("Frequency (GHz):")
        self.freq_input = QLineEdit()
        self.freq_input.setPlaceholderText("0.035–4.4")
        self.freq_input.setValidator(QDoubleValidator(0.035, 4.4, 6))  # Restrict to 35 MHz–4400 MHz
        self.freq_input.setText("2.4")  # Default to 2.4 GHz
        layout.addWidget(self.freq_label, 0, 0)
        layout.addWidget(self.freq_input, 0, 1)

        # Attenuation
        self.atten_label = QLabel("Attenuation (0-31):")
        self.atten_input = QLineEdit()
        self.atten_input.setPlaceholderText("0-31")
        layout.addWidget(self.atten_label, 1, 0)
        layout.addWidget(self.atten_input, 1, 1)

        # Phase
        self.phase_label = QLabel("Phase (degrees):")
        self.phase_input = QLineEdit()
        self.phase_input.setPlaceholderText("0-360")
        layout.addWidget(self.phase_label, 2, 0)
        layout.addWidget(self.phase_input, 2, 1)

        # ADC Mode
        self.adc_label = QLabel("ADC Mode:")
        self.adc_combo = QComboBox()
        self.adc_combo.addItems(["tx", "rx", "diff"])
        layout.addWidget(self.adc_label, 3, 0)
        layout.addWidget(self.adc_combo, 3, 1)

        # RF Enable
        self.rf_enable_check = QCheckBox("RF Enable")
        layout.addWidget(self.rf_enable_check, 4, 0, 1, 2)

        # TX Amplifier
        self.tx_amp_check = QCheckBox("TX Amplifier")
        layout.addWidget(self.tx_amp_check, 5, 0, 1, 2)

        # RX Amplifier
        self.rx_amp_check = QCheckBox("RX Amplifier")
        layout.addWidget(self.rx_amp_check, 6, 0, 1, 2)

        # Lock Detect
        self.ld_label = QLabel("Lock Detect:")
        self.ld_status = QLabel("Unknown")
        self.ld_status.setStyleSheet("background-color: gray; color: white; padding: 5px;")
        layout.addWidget(self.ld_label, 7, 0)
        layout.addWidget(self.ld_status, 7, 1)

        # Buttons
        self.apply_button = QPushButton("Apply Settings")
        self.apply_button.clicked.connect(self.apply_settings)
        layout.addWidget(self.apply_button, 8, 0, 1, 2)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_settings)
        layout.addWidget(self.refresh_button, 9, 0, 1, 2)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def start_polling(self) -> None:
        """Start a timer to periodically check lock detect status."""
        self.polling_timer = QTimer()
        self.polling_timer.timeout.connect(self.update_lock_detect)
        self.polling_timer.start(1000)  # Poll every 1 second

    def update_lock_detect(self) -> None:
        """Update the lock detect status indicator."""
        try:
            ld_status = self.txr.ld
            self.ld_status.setText("Locked" if ld_status else "Unlocked")
            self.ld_status.setStyleSheet(
                "background-color: green; color: white; padding: 5px;" if ld_status
                else "background-color: red; color: white; padding: 5px;"
            )
        except Exception as e:
            logger.error(f"Error reading lock detect: {e}", exc_info=True)
            self.status_bar.showMessage(f"Error reading lock detect: {e}")
            self.ld_status.setText("Error")
            self.ld_status.setStyleSheet("background-color: gray; color: white; padding: 5px;")

    def refresh_settings(self) -> None:
        """Refresh GUI with current transceiver settings."""
        try:
            # Frequency in GHz
            logger.debug("Refreshing frequency")
            self.freq_input.setText(str(self.txr.freq / 1_000_000_000))  # Hz to GHz
            logger.debug("Refreshing attenuation")
            self.atten_input.setText(str(self.txr.atten))
            logger.debug("Refreshing phase")
            self.phase_input.setText(str(self.txr.phase))
            # ADC mode is not queried as it returns a float (ADC value), not mode
            logger.debug("Refreshing RF enable")
            self.rf_enable_check.setChecked(self.txr.rfenable)
            logger.debug("Refreshing TX amplifier")
            self.tx_amp_check.setChecked(self.txr.txamp)
            logger.debug("Refreshing RX amplifier")
            self.rx_amp_check.setChecked(self.txr.rxamp)
            logger.debug("Updating lock detect")
            self.update_lock_detect()
            self.status_bar.showMessage("Settings refreshed")
        except Exception as e:
            logger.error(f"Error refreshing settings: {e}", exc_info=True)
            self.status_bar.showMessage(f"Error refreshing settings: {e}")
            QMessageBox.warning(self, "Error", f"Failed to refresh settings: {e}")

    def apply_settings(self) -> None:
        """Apply user-entered settings to the transceiver."""
        try:
            # Frequency (convert GHz to Hz)
            logger.debug("Applying frequency")
            try:
                freq_ghz = float(self.freq_input.text())
                if freq_ghz < 0.035 or freq_ghz > 4.4:
                    raise ValueError("Frequency must be between 0.035 and 4.4 GHz.")
                freq_hz = int(freq_ghz * 1_000_000_000)  # GHz to Hz
                self.txr.freq = freq_hz
            except ValueError as e:
                raise ValueError(f"Invalid frequency value: {e}")

            # Attenuation
            logger.debug("Applying attenuation")
            try:
                atten = int(self.atten_input.text())
                self.txr.atten = atten
            except ValueError:
                raise ValueError("Invalid attenuation value. Must be 0-31.")

            # Phase
            logger.debug("Applying phase")
            try:
                phase = float(self.phase_input.text())
                self.txr.phase = phase
            except ValueError:
                raise ValueError("Invalid phase value. Must be a number.")

            # ADC Mode
            logger.debug("Applying ADC mode")
            self.txr.adc = self.adc_combo.currentText()

            # RF Enable
            logger.debug("Applying RF enable")
            self.txr.rfenable = self.rf_enable_check.isChecked()

            # TX Amplifier
            logger.debug("Applying TX amplifier")
            self.txr.txamp = self.tx_amp_check.isChecked()

            # RX Amplifier
            logger.debug("Applying RX amplifier")
            self.txr.rxamp = self.rx_amp_check.isChecked()

            self.status_bar.showMessage("Settings applied successfully")
        except Exception as e:
            logger.error(f"Error applying settings: {e}", exc_info=True)
            self.status_bar.showMessage(f"Error applying settings: {e}")
            QMessageBox.warning(self, "Error", f"Failed to apply settings: {e}")

    def closeEvent(self, event) -> None:
        """Handle window close event to ensure transceiver is closed."""
        if self.txr:
            try:
                self.txr.close()
                logger.info("Transceiver closed")
            except Exception as e:
                logger.warning(f"Error closing transceiver: {e}", exc_info=True)
        event.accept()

def main():
    """Run the GUI application."""
    app = QApplication(sys.argv)
    gui = TxrGUI()
    gui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
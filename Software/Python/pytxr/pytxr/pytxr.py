from typing import Optional, Union, List
import logging
from serial import Serial
from serial.tools.list_ports import comports
import time

# Constants
BAUD_RATE: int = 115200
TIMEOUT: float = 1.0
VID: int = 1027
PID: int = 24597
PHASE_RESOLUTION: float = 1.4

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Txr:
    """A class to control an S-band transceiver board via a serial interface.

    This class provides methods to configure and query the transceiver's frequency,
    attenuation, phase, RF enable, amplifiers, and ADC settings.

    Attributes:
        port (str): The serial port used for communication.
        ser (Optional[Serial]): The serial connection object.
    """

    def __init__(self, port: Optional[str] = None) -> None:
        """Initialize the Txr object.

        Args:
            port (Optional[str]): The serial port to use. If None, attempts to autodetect.

        Raises:
            ValueError: If no port is provided and autodetection fails.
            RuntimeError: If the serial port cannot be opened.
        """
        self._port: Optional[str] = port if port else self.autodetect_port()
        self._ser: Optional[Serial] = None
        self.open()
        logger.info(f"Initialized Txr on port {self._port}")

    def __enter__(self) -> "Txr":
        """Support for context manager to ensure the serial port is opened."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Ensure the serial port is closed when exiting the context."""
        self.close()

    def autodetect_port(self) -> str:
        """Autodetect the serial port of the transceiver.

        Returns:
            str: The detected port name.

        Raises:
            ValueError: If no device or multiple devices are detected.
        """
        ports = comports()
        devices: List[str] = [p.device for p in ports if p.vid == VID and p.pid == PID]

        if not devices:
            raise ValueError("No S-band transceiver detected. Is the device plugged in?")
        if len(devices) > 1:
            raise ValueError(f"Multiple devices detected: {devices}. Please specify a port.")
        return devices[0]

    def open(self) -> None:
        """Open the serial connection to the transceiver.

        Raises:
            RuntimeError: If the connection is already open or fails to open.
        """
        if self._ser is not None:
            raise RuntimeError("Serial connection already open.")
        try:
            self._ser = Serial(port=self._port, baudrate=BAUD_RATE, timeout=TIMEOUT)
        except Exception as e:
            raise RuntimeError(f"Failed to open serial port {self._port}: {e}")
        logger.debug(f"Opened serial connection on {self._port}")

    def close(self) -> None:
        """Close the serial connection if open."""
        if self._ser is not None:
            try:
                self._ser.close()
            except Exception as e:
                logger.warning(f"Error closing serial port {self._port}: {e}")
            finally:
                self._ser = None
            logger.debug(f"Closed serial connection on {self._port}")

    def write(self, command: str) -> None:
        """Write a command to the serial port.

        Args:
            command (str): The command to send.

        Raises:
            RuntimeError: If the serial connection is not open or write fails.
        """
        if self._ser is None:
            raise RuntimeError("Serial connection is not open.")
        try:
            self._ser.write(f"{command}\r\n".encode("utf-8"))
        except Exception as e:
            raise RuntimeError(f"Failed to write command '{command}': {e}")

    def read(self) -> str:
        """Read a response from the serial port.

        Returns:
            str: The decoded response.

        Raises:
            RuntimeError: If the serial connection is not open or read fails.
        """
        if self._ser is None:
            raise RuntimeError("Serial connection is not open.")
        try:
            return self._ser.readline().decode("utf-8").strip()
        except Exception as e:
            raise RuntimeError(f"Failed to read response: {e}")

    def query(self, command: str) -> str:
        """Send a command and read the response.

        Args:
            command (str): The command to send.

        Returns:
            str: The response from the device.

        Raises:
            RuntimeError: If the query fails.
        """
        self.write(command)
        return self.read()

    @property
    def freq(self) -> int:
        """Get or set the transceiver frequency in Hz.

        Returns:
            int: The current frequency in Hz.

        Raises:
            ValueError: If the frequency is invalid or response is malformed.
        """
        try:
            freq_khz = int(self.query("freq?"))
            return freq_khz * 1000
        except ValueError as e:
            raise ValueError("Invalid frequency response from device") from e

    @freq.setter
    def freq(self, value: int) -> None:
        """Set the frequency in Hz.

        Args:
            value (int): The frequency in Hz.

        Raises:
            ValueError: If the frequency is negative.
        """
        if value < 0:
            raise ValueError("Frequency must be non-negative.")
        freq_khz = value // 1000
        self.write(f"freq {freq_khz}")

    @property
    def atten(self) -> int:
        """Get or set the attenuation level (0-31).

        Returns:
            int: The current attenuation level.

        Raises:
            ValueError: If the response is malformed.
        """
        try:
            return int(self.query("atten?"))
        except ValueError as e:
            raise ValueError("Invalid attenuation response from device") from e

    @atten.setter
    def atten(self, value: int) -> None:
        """Set the attenuation level.

        Args:
            value (int): Attenuation level (0-31).

        Raises:
            ValueError: If the attenuation is out of range.
        """
        if not 0 <= value <= 31:
            raise ValueError("Attenuation must be between 0 and 31.")
        self.write(f"atten {value}")

    @property
    def phase(self) -> float:
        """Get or set the phase in degrees.

        Returns:
            float: The current phase in degrees.

        Raises:
            ValueError: If the phase response is invalid.
        """
        try:
            phase_bits = int(self.query("phase?"))
            # Reverse bits and convert to degrees
            phase_bits_reversed = int(f"{phase_bits:08b}"[::-1], 2)
            return phase_bits_reversed * PHASE_RESOLUTION
        except ValueError as e:
            raise ValueError("Invalid phase response from device") from e

    @phase.setter
    def phase(self, value: float) -> None:
        """Set the phase in degrees.

        Args:
            value (float): Phase in degrees (0-360).

        Raises:
            ValueError: If the phase is invalid.
        """
        value = value % 360  # Normalize to 0-360 degrees
        phase_bits = int(value / PHASE_RESOLUTION) & 0xFF
        phase_bits_reversed = int(f"{phase_bits:08b}"[::-1], 2)
        self.write(f"phase {phase_bits_reversed}")

    @property
    def rfenable(self) -> bool:
        """Get or set the RF enable state.

        Returns:
            bool: True if RF is enabled, False otherwise.

        Raises:
            ValueError: If the response is invalid.
        """
        try:
            return bool(int(self.query("rfenable?")))
        except ValueError as e:
            raise ValueError("Invalid RF enable response from device") from e

    @rfenable.setter
    def rfenable(self, value: bool) -> None:
        """Set the RF enable state.

        Args:
            value (bool): True to enable RF, False to disable.

        Raises:
            ValueError: If the value is not a boolean.
        """
        if not isinstance(value, bool):
            raise ValueError("RF enable must be True or False.")
        self.write(f"rfenable {1 if value else 0}")

    @property
    def ld(self) -> bool:
        """Get the lock detect status.

        Returns:
            bool: True if locked, False otherwise.

        Raises:
            ValueError: If the response is invalid.
        """
        try:
            return bool(int(self.query("ld?")))
        except ValueError as e:
            raise ValueError("Invalid lock detect response from device") from e

    @property
    def txamp(self) -> bool:
        """Get or set the transmit amplifier state.

        Returns:
            bool: True if enabled, False otherwise.

        Raises:
            ValueError: If the response is invalid.
        """
        try:
            return bool(int(self.query("txamp?")))
        except ValueError as e:
            raise ValueError("Invalid TX amplifier response from device") from e

    @txamp.setter
    def txamp(self, value: bool) -> None:
        """Set the transmit amplifier state.

        Args:
            value (bool): True to enable, False to disable.

        Raises:
            ValueError: If the value is not a boolean.
        """
        if not isinstance(value, bool):
            raise ValueError("TX amplifier enable must be True or False.")
        self.write(f"txamp {1 if value else 0}")

    @property
    def rxamp(self) -> bool:
        """Get or set the receive amplifier state.

        Returns:
            bool: True if enabled, False otherwise.

        Raises:
            ValueError: If the response is invalid.
        """
        try:
            return bool(int(self.query("rxamp?")))
        except ValueError as e:
            raise ValueError("Invalid RX amplifier response from device") from e

    @rxamp.setter
    def rxamp(self, value: bool) -> None:
        """Set the receive amplifier state.

        Args:
            value (bool): True to enable, False to disable.

        Raises:
            ValueError: If the value is not a boolean.
        """
        if not isinstance(value, bool):
            raise ValueError("RX amplifier enable must be True or False.")
        self.write(f"rxamp {1 if value else 0}")

    @property
    def adc(self) -> float:
        """Get or set the ADC mode and value.

        Returns:
            float: The current ADC value.

        Raises:
            ValueError: If the response is invalid.
        """
        try:
            return float(self.query("adc?"))
        except ValueError as e:
            raise ValueError("Invalid ADC response from device") from e

    @adc.setter
    def adc(self, mode: str) -> None:
        """Set the ADC mode.

        Args:
            mode (str): One of 'tx', 'rx', or 'diff'.

        Raises:
            ValueError: If the mode is invalid.
        """
        valid_modes = ["tx", "rx", "diff"]
        if mode not in valid_modes:
            raise ValueError(f"ADC mode must be one of {valid_modes}.")
        self.write(f"adc {mode}")

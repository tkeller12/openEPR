import numpy as np
from serial import Serial
from serial.tools.list_ports import comports
import time


BAUD_RATE = 115200
TIMEOUT = 1.

VID = 1027
PID = 24597

PHASE_RESOLUTION = 1.4

class Txr:
    '''
    '''

    def __init__(self, port = None):

        if port == None:
            port = self.autodetect_port()
#        self.ser = serial.Serial(port, baudrate = BAUD_RATE, timeout = TIMEOUT)
        self._port = port
        self._ser = None

        self.open()


    def autodetect_port(self):
        ports = comports()

        devices_list = []
        for p in ports:
            if (p.vid == VID) and (p.pid == PID):
                devices_list.append(p.device)

        if len(devices_list) == 0:
            raise ValueError('Could not detect serial port. Is the device plugged in?')
        elif len(devices_list) == 1:
            return devices_list[0]
        else:
            raise ValueError('Multiple devices detected. Please manually select serial port: %s'%devices_list)


    def __del__(self):
        self.close()

    def close(self):
        if self._ser is not None:
            self._ser.close()
            self._ser = None

    def open(self):
        if self._ser is not None:
            raise RuntimeError('Device connection already open')
        self._ser = Serial(port = self._port, baudrate = BAUD_RATE, timeout = TIMEOUT)


    def write(self, command):
        command += '\r\n'
        self._ser.write(command.encode('utf-8'))

    def read(self):
        return self._ser.readline().decode('utf-8').strip()

    def query(self, command):
        self.write(command)
        return self.read()

    
    def freq(self, freq = None):
        '''Set frequency in Hz
        '''

        if freq == None:
            command = 'freq?'
            freq_string = self.query(command)
            freq_kHz = int(freq_string)
            freq = freq_kHz * 1000
            return freq

        freq_kHz = freq / 1000.
        command = 'freq %i'%freq_kHz
        self.write(command)


    def atten(self, atten = None):
        '''
        '''

        if atten == None:
            command = 'atten?'
            atten_string = self.query(command)
            atten = int(atten_string)
            return atten

        elif (atten >= 0) and (atten <= 31):
            command = 'atten %i'%atten
            self.write(command)

        else:
            raise ValueError('Attenuation out of range. Attenuation must be between 0 and 31')

    def phase(self, phase = None):
        '''
        '''

        if phase == None:
            command = 'phase?'
            phase_string = self.query(command)

            phase = int(phase_string)
            phase = int('{:08b}'.format(phase)[::-1], 2) # reverse bits

            phase *= PHASE_RESOLUTION

            return phase
        else:
            phase = (phase % 360)
            phase_bits = int(phase / PHASE_RESOLUTION)
            phase_bits &= 0xff
            phase_bits_reversed = int('{:08b}'.format(phase_bits)[::-1], 2) # reverse bits
            command = 'phase %i'%phase_bits_reversed
            self.write(command)

            
    def rfenable(self, enable = None):
        '''
        '''
        if enable == None:
            command = 'rfenable?'
            enable_string = self.query(command)
            enable = int(enable_string)
            return enable

        elif (enable == 0) or (enable == 1):
            command = 'rfenable %i'%enable
            self.write(command)

        else:
            raise ValueError('RF enable not valid, must be 1 or 0')

    def ld(self):
        '''
        '''
        command = 'ld?'
        lock_detect_string = self.query(command)
        lock_detect = int(lock_detect_string)
        return lock_detect

    def txamp(self, enable = None):
        if enable == None:
            command = 'txamp?'
            enable_string = self.query(command)
            enable = int(enable_string)
            return enable
        
        elif (enable == 0) or (enable == 1):
            command = 'txamp %i'%enable
            self.write(command)
        else:
            raise ValueError('Tx Enable must be 0 or 1')


    def rxamp(self, enable = None):
        if enable == None:
            command = 'rxamp?'
            enable_string = self.query(command)
            enable = int(enable_string)
            return enable
        
        elif (enable == 0) or (enable == 1):
            command = 'rxamp %i'%enable
            self.write(command)
        else:
            raise ValueError('Tx Enable must be 0 or 1')


    def adc(self, mode = None):
        '''
        '''
        if mode == None:
            command = 'adc?'
            adc_string = self.query(command)
            adc_value = float(adc_string)
            return adc_value
        elif (mode in ['tx', 'rx', 'diff']):
            command = 'adc %s'%mode
            self.write(command)


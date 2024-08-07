import serial
from serial.tools.list_ports import comports
import numpy as np
import time

from matplotlib.pylab import *

ports = comports()

port = None
for p in ports:
    if (p.vid == 1027) and (p.pid == 24597):
        port = p.device


#port = 'COM6'
#baud = 9600
baud = 115200
ser = serial.Serial(port, baudrate = baud, timeout = 1.)



def freq(freq = None): # in kHz
    if freq == None:
        command = 'freq?\n'
        ser.write(command.encode('utf-8'))
        raw_bytes = ser.readline()
        my_string = raw_bytes.decode('utf-8')
        return my_string

    else:
        if (freq < 35000) or (freq > 4400000):
            raise ValueError('Frequency out of range')
        command = 'freq %i\n'%freq
        ser.write(command.encode('utf-8'))

def adc(mode = None): # in kHz
    if mode == None:
        command = 'adc?\n'
        ser.write(command.encode('utf-8'))
        raw_bytes = ser.readline()
        my_string = raw_bytes.decode('utf-8')
        return my_string

    else:
        if (mode not in ['tx', 'rx', 'diff']):
            raise ValueError('Mode not valid')
        command = 'adc %s\n'%mode
        ser.write(command.encode('utf-8'))


def power(power = None):
    if power == None:
        command = 'power?\n'
        ser.write(command.encode('utf-8'))
        raw_bytes = ser.readline()
        my_string = raw_bytes.decode('utf-8')
        return my_string

    else:
        command = 'power %i\n'%power
        ser.write(command.encode('utf-8'))

def atten(atten = None):
    if atten == None:
        command = 'atten?\n'
        ser.write(command.encode('utf-8'))
        raw_bytes = ser.readline()
        my_string = raw_bytes.decode('utf-8')
        return my_string

    else:
        command = 'atten %i\n'%atten
        ser.write(command.encode('utf-8'))

def phase(phase = None):
    '''Phase in degrees'''

    phase_resolution = 1.4 # degrees

    if phase == None:
        command = 'phase?\n'
        ser.write(command.encode('utf-8'))
        raw_bytes = ser.readline()
        my_string = raw_bytes.decode('utf-8')

        phase = int(my_string)
        phase = int('{:08b}'.format(phase)[::-1], 2) # reverse bits

        phase *= phase_resolution

        return phase

    else:
        phase = (phase % 360)
        phase_bits = int(phase / phase_resolution)
        phase_bits &= 0xff
        phase_bits_reversed = int('{:08b}'.format(phase_bits)[::-1], 2) # reverse bits
        command = 'phase %i\n'%phase_bits_reversed
        ser.write(command.encode('utf-8'))


def rfenable(rfenable = None):
    if rfenable == None:
        command = 'rfenable?\n'
        ser.write(command.encode('utf-8'))
        raw_bytes = ser.readline()
        my_string = raw_bytes.decode('utf-8')
        return my_string

    else:
        command = 'rfenable %i\n'%rfenable
        ser.write(command.encode('utf-8'))

def ld():
    command = 'ld?\n'
    ser.write(command.encode('utf-8'))
    raw_bytes = ser.readline()
    my_string = raw_bytes.decode('utf-8')
    return my_string

def read():
    raw_bytes = ser.readline()
    my_string = raw_bytes.decode('utf-8')
    return my_string

def txamp(enable = None):
    if enable == None:
        command = 'txamp?\n'
        ser.write(command.encode('utf-8'))
        raw_bytes = ser.readline()
        my_string = raw_bytes.decode('utf-8')
        return my_string

    else:
        command = 'txamp %i\n'%enable
        ser.write(command.encode('utf-8'))

def rxamp(enable = None):
    if enable == None:
        command = 'rxamp?\n'
        ser.write(command.encode('utf-8'))
        raw_bytes = ser.readline()
        my_string = raw_bytes.decode('utf-8')
        return my_string

    else:
        command = 'rxamp %i\n'%enable
        ser.write(command.encode('utf-8'))



def sweep_freq(start_freq,stop_freq, points = 1000, dwell_time = 10e-3):
    freq_list = np.linspace(start_freq, stop_freq, points)
#    freq_list = np.r_[start_freq:stop_freq:step]

    start_time = time.time()
    ix = 0
    for freq_value in freq_list:
#        print(ix)
        print('Setting freq: %0.03f'%freq_value)
        freq(freq_value)
#        time.sleep(dwell_time)
        ix+=1
    stop_time = time.time()
    total_time = stop_time - start_time
    print('Total Sweep Time: %0.01fs'%total_time)

def sweep_adc(points = 100, dwell_time = 1e-3):
    start_time = time.time()
    ix = 0
    for ix in range(points):
        print(adc())
        time.sleep(dwell_time)
        ix+=1
    stop_time = time.time()
    total_time = stop_time - start_time
    print('Total Sweep Time: %0.01fs'%total_time)

def sweep_freq_adc(start_freq = 1000000,stop_freq = 3000000, points = 100, dwell_time = 1e-3):
    freq_list = np.linspace(start_freq, stop_freq, points)
#    freq_list = np.r_[start_freq:stop_freq:step]

    start_time = time.time()
    ix = 0
    adc_list = []
    for freq_value in freq_list:
#        print(ix)
        print('Setting freq: %0.03f'%freq_value)
        freq(freq_value)
        time.sleep(dwell_time)
        adc_list.append(float(adc()))
        ix+=1
    stop_time = time.time()
    total_time = stop_time - start_time
    print('Total Sweep Time: %0.01fs'%total_time)
    adc_array = np.array(adc_list)

    figure()
    plot(freq_list,-1*adc_array)


#sweep_freq(35000,45000,200)
freq(2000000)
atten(10)
adc('diff')
txamp(0)
rxamp(0)
#power(0)
#sweep_freq_adc()
#atten(31)
txamp(0)
rxamp(0)
#ser.close()

#for ix2 in range(100):
for ix in range(360):
    time.sleep(0.001)
    phase(ix)
show()

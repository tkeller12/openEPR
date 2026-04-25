import os
import sys
sys.path.append('../pytxr/pytxr')
sys.path.append('../../../../openEPR_nanoDAQ_python/openepr')
import pytxr
import nano_daq
import time
import numpy as np
from matplotlib.pylab import *

DELAY = 0.5

txr = pytxr.Txr('COM3')
print(txr)

daq = nano_daq.NanoDAQ('COM4')
daq.selectADC(1)
print(daq)


time.sleep(1)
print('ADC value',daq.readADC())
#freq_hz = int(freq_MHz * 1e6)  # MHz to Hz
#txr.freq = freq_hz

freq_array = np.r_[100:200:101j]
freq_Hz = int(freq_array[0] * 1e6)  # MHz to Hz
txr.freq = freq_Hz
txr.rfenable = True
txr.txamp = False
txr.rxamp = False
voltage_list = []

for ix_freq, freq_MHz in enumerate(freq_array):
    print(ix_freq, freq_MHz)
    freq_Hz = int(freq_MHz * 1e6)  # MHz to Hz
    txr.freq = freq_Hz
    time.sleep(DELAY)
    voltage = daq.readADC()
    print(voltage)
    voltage_list.append(voltage)

daq.close()
txr.rfenable = False
txr.close()

figure()
plot(freq_array, voltage_list)
xlabel('Frequency (MHz)')
ylabel('Voltage (mV)')
show()




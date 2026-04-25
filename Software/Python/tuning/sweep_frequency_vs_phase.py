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
daq.setDAC(1, 0)
print(daq)


time.sleep(1)
print('ADC value',daq.readADC())
#freq_hz = int(freq_MHz * 1e6)  # MHz to Hz
#txr.freq = freq_hz

#DAC_array = np.r_[2.3:2.5:10j]
DAC_array = np.r_[0:4.9:21j]

freq_array = np.r_[140:160:51j]
freq_Hz = int(freq_array[0] * 1e6)  # MHz to Hz
txr.freq = freq_Hz
txr.rfenable = True
txr.txamp = False
txr.rxamp = False

for ix_dac, voltage_dac in enumerate(DAC_array):
    print('-'*50)
    print(ix_dac, voltage_dac)
    print('-'*50)
    daq.setDAC(1, voltage_dac)
    time.sleep(0.5)
    voltage_list = []

    for ix_freq, freq_MHz in enumerate(freq_array):
        print(ix_freq, freq_MHz)
        freq_Hz = int(freq_MHz * 1e6)  # MHz to Hz
        txr.freq = freq_Hz
        time.sleep(DELAY)
        voltage = daq.readADC()
        print(voltage)
        voltage_list.append(voltage)


    figure('Frequency Sweep')
    plot(freq_array, voltage_list, label = 'DAC: %0.03f V'%voltage_dac)
    legend()
    xlabel('Frequency (MHz)')
    ylabel('Voltage (mV)')
    tight_layout()

daq.close()
txr.rfenable = False
txr.close()

show()




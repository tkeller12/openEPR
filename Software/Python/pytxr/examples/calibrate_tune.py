import pytxr
import numpy as np
from matplotlib.pylab import *
import time

txr = pytxr.Txr()


dwell_time = 0.010 # seconds
pts = 1000.
freq_array = np.r_[35e6:4400e6:1j*pts]

#cal_mode = 'tx'
cal_mode = 'rx'
#cal_mode = 'diff'
#save_filename = cal_mode + '_cpl_cal.csv'
save_filename = cal_mode + '_cpl_data.csv'

txr.txamp(1)
txr.atten(0)
txr.adc(cal_mode)
#txr.adc('tx')
#txr.adc('rx')
#txr.adc('diff')

v = txr.adc()
v_list = []

for freq_ix, freq in enumerate(freq_array):
    print(freq)
    txr.freq(freq)
    time.sleep(dwell_time)
#    v_list.append(-1*txr.adc())
    v_list.append(txr.adc())

txr.txamp(0)
txr.rxamp(0)
txr.atten(30)
    
v_array = np.array(v_list)

save_array = np.vstack((freq_array, v_array)).T

figure('Tune')
#plot(freq_array, v_array / 50)
plot(freq_array, v_array)

np.savetxt(save_filename, save_array, delimiter = ',')

txr.close()
show()


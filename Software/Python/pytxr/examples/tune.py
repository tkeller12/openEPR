import pytxr
import numpy as np
from matplotlib.pylab import *
import time

txr = pytxr.Txr()


dwell_time = 0.010 # seconds
pts = 100.
freq_array = np.r_[800e6:1000e6:1j*pts]


#txr.txamp(1)
#txr.atten(10)
#txr.adc('tx')
#txr.adc('rx')
txr.adc('diff')

v = txr.adc()
v_list = []

for freq_ix, freq in enumerate(freq_array):
    print(freq)
    txr.freq(freq)
    time.sleep(dwell_time)
    v_list.append(-1*txr.adc())
    
v_array = np.array(v_list)

figure('Tune')
plot(freq_array, v_array / 50)
#txr.close()
show()


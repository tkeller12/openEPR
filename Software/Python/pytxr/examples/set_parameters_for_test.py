import pytxr
import numpy as np
from matplotlib.pylab import *
import time

txr = pytxr.Txr()

#txr.freq(880e6)
txr.freq(1399e6)
#txr.phase(65 - 70)

txr.txamp(0)
txr.rxamp(0)
txr.atten(0)

#txr.txamp(0)
#txr.rxamp(0)
#txr.atten(31)

txr.adc('diff')

txr.close()


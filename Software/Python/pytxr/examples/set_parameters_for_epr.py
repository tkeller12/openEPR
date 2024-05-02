import pytxr
import numpy as np
from matplotlib.pylab import *
import time

txr = pytxr.Txr()

txr.freq(880e6)
txr.phase(65)

txr.txamp(1)
txr.rxamp(1)
txr.atten(0)

txr.adc('diff')

txr.close()


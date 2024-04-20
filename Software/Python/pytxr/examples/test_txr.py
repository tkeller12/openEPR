import pytxr

tx = pytxr.Txr()


tx.freq(2e9)
print(tx.freq())


tx.phase()
tx.phase(0)
tx.txamp(0)
tx.rxamp(0)
tx.atten(30)
print(tx.atten())
print(tx.txamp())
print(tx.rxamp())

tx.adc()

tx.adc('diff')
for ix in range(100):
    print(tx.adc())


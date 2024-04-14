import pytxr

tx = pytxr.Txr()


start_phase = tx.phase()
tx.phase(65)
stop_phase = tx.phase()

print('start_phase:', start_phase)
print('stop_phase:', stop_phase)

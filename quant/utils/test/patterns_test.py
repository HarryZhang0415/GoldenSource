from quant.utils.patterns import TimeIt
import time
#TO-DO
with TimeIt(
    on_exit=lambda t: print("Total Time Taken: " + str(t))):
    time.sleep(3)

with TimeIt(tag='Running risk instruments'):
    time.sleep(3)
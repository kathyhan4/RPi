import ReadTempRhCurrent
import time

for i in range(400):
	ReadTempRhCurrent.getTRHCurrent(i,400,"testing",48)
	time.sleep(1)

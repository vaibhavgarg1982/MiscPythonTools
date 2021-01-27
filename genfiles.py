import time
import os
from numpy.random import randint
for i in range(100):
    for year in range(2018,2022):
        for month in range(1,13):
            for date in range(1,29):
                filepath = os.path.join("testdir", str(year)+format(month,"02")+format(date,"02")+str(time.time_ns())+".txt")
                #time.sleep(0.001)
                print(filepath)
                with open(filepath, mode='a') as f:
                    f.write(filepath)

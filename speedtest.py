
import os
import json
import time


for _ in range(100):
    cmd = 'speedtest.exe -f json-pretty >speedtest.txt'
    os.system(cmd)
    with open("speedtest.txt") as f:
        data = f.read()
    data = json.loads(data)
    with open("speedtracker.csv", mode='a') as f:
        string = data["timestamp"] + ","+ str(data["download"]['bandwidth']/1024/1024*8) + "," + str(data["upload"]['bandwidth']/1024/1024*8)+"\n"
        f.write(string)
    print(str(_) + string)
    time.sleep(900)





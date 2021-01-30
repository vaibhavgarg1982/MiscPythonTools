import cv2
import numpy as np
import matplotlib.pyplot as plt

avgs = []
cap= cv2.VideoCapture('C:\\Users\\vaibh\\Pictures\\Camera Roll\\WIN_20201007_12_16_55_Pro.mp4')
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    else:
        avgs.append(np.mean(frame[:,:,2]))
 
fr = cap.get(cv2.CAP_PROP_FPS)
print  (f"frame rate {fr}")
cap.release()
cv2.destroyAllWindows()

plt.plot(avgs[20:-20])


avgs1 = avgs[20:-20]
avgs1 = np.convolve(avgs1, np.ones(3))[3:-3]/3
plt.plot(avgs1)
plt.show()
a = np.diff(np.sign(np.diff(avgs1))).nonzero()[0] + 1 # local min+max
b = (np.diff(np.sign(np.diff(avgs1))) > 0).nonzero()[0] + 1 # local min
c = (np.diff(np.sign(np.diff(avgs1))) < 0).nonzero()[0] + 1 # local max

valid = np.diff(b)
#valid = [x for x in valid if 14>x>8]
print (b)
print(60/(np.array(valid)/fr))

plt.plot(np.absolute(np.fft.fft(avgs1-np.mean(avgs1))))
plt.show()
fftmags = (np.absolute(np.fft.fft(avgs1-np.mean(avgs1))))
fftmags = fftmags[0:(len(fftmags)//2)]
print(fftmags.argsort()[-10:])
print([x*fr/len(avgs1)*60 for x in fftmags.argsort()[-10:] if 50 < x*fr/len(avgs1)*60 < 170])
pass
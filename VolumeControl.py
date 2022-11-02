import time
import cv2 as cv
import numpy as np
from handTrackers import handDetector
import math

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()

volume_Range =volume.GetVolumeRange()
minVol = volume_Range[0]
maxVol = volume_Range[1]

cap = cv.VideoCapture(0)
wcam ,hcam = 640 , 480
cap.set(3,wcam)
cap.set(4,wcam)
ptime =0

detector = handDetector(detectionCon=0.7,maxHands=1)
while True:
    success , imag = cap.read()
    img = detector.findHands(imag)
    lmlist = detector.findPosition(img,draw=False)

    if len(lmlist) !=0:
        #print(lmlist[4],lmlist[8])
        x1,y1 = lmlist[4][1] , lmlist[4][2]
        x2,y2 = lmlist[8][1] , lmlist[8][2]
        
        midX ,midY = (x1+x2) //2 ,(y1+y2)//2
        cv.circle(img,(x1,y1),10,(0,0,0),-1)
        cv.circle(img,(x2,y2),10,(0,0,0),-1)
        cv.circle(img,(midX,midY),10,(0,0,0),-1)
        cv.line(img,(x1,y1),(x2,y2),(255,0,0),2)

        length = math.hypot(x2-x1 , y2-y1)
        vol = np.interp(length,[50,250],[minVol,maxVol])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)
        if length<50:
            cv.circle(img, (midX, midY), 10, (255, 0, 0), -1)


    ctime = time.time()
    fps =1/(ctime-ptime)
    ptime = ctime
    cv.putText(img,str(int(fps)),(20,50),cv.FONT_HERSHEY_DUPLEX,2 , (0,0,255))
    
    cv.flip(imag,1)
    cv.imshow('Volume Control',imag)
    if cv.waitKey(1) & 0xFF == ord('q'):
            break


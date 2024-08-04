import math
import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam,hCam=640,480

pTime=0
cTime=0

cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

detector=htm.handDetector()


devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(
    IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume=cast(interface,POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()
#print(volume.GetVolumeRange())

#print(volume.GetVolumeRange())
minVol=int(volRange[0])
maxVol=int(volRange[1])
vol=0
volbar=400


while True:
    isTrue,img=cap.read()
    detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    if len(lmList)!=0:
        #print(lmList[4],lmList[8])

        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2

        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
        dist=math.hypot(x2-x1,y2-y1)
        print(dist)

        #Hand Range  25-250
        #Volume Range -63 - 0

        vol=np.interp(dist,[25,250],[minVol,maxVol])
        volbar = np.interp(dist, [25, 250], [400,100])
        #print(vol)
        volume.SetMasterVolumeLevel(vol, None)


    cv2.rectangle(img,(50,100),(85,400),(0,255,0),3)
    cv2.rectangle(img, (50, int(volbar)), (85, 400), (0, 255, 0),cv2.FILLED)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    cv2.imshow('View',img)

    cv2.waitKey(1)
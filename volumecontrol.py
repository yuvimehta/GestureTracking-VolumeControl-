from operator import length_hint
import cv2
import mediapipe
import numpy as np
import handtracking_module as htm
import math
from subprocess import call


################################
wCam, hCam = 640, 480
################################
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handTracker()

def volumecontol(value):
    call(["amixer", "-D", "pulse", "sset", "Master", str(value)+"%"])


while True:
    success, img = cap.read()
    img = detector.handsFinder(img)
    lmList = detector.positionFinder(img,draw = False)
    if len(lmList) != 0:
        #print(lmList[4], lmList[8])

        x1,y1 = lmList[4][1], lmList[4][2]
        x2,y2 = lmList[8][1], lmList[8][2]
        mx,my = (x1+x2)//2 , (y1+y2)//2
        cv2.circle(img,(x1,y1),15, (255,0,255), cv2.FILLED)
        cv2.circle(img,(x2,y2),15, (255,0,255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255.0,255),3)
        cv2.circle(img,(mx,my),9, (255,0,255), cv2.FILLED)
        length = math.hypot(x2-x1, y2-y1)
        length = int(length)
        
        vol = np.interp(length,[34,220], [0,100])
        vol = int(vol)
        #print(vol)
        #print(length)
        volumecontol(vol)


        if length < 34:
            cv2.circle(img,(mx,my),15, (255,0,0), cv2.FILLED)

    
    cv2.imshow("img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# max = 290 ,min = 30 
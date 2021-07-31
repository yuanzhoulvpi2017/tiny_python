import math

import cv2
import time
import numpy as np

import HandTrackingModule as htm
from ctypes import cast, POINTER

# from comtypes import CLSCTX_ALL
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

##############################################################
wCam, hCam = 640, 480


##############################################################

def main():
    # devices = AudioUtilities.GetSpeakers()
    # interface = devices.Activate(
    #     IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    # volume = cast(interface, POINTER(IAudioEndpointVolume))
    # volume.GetMute()
    # volume.GetMasterVolumeLevel()
    # volRange = volume.GetVolumeRange()
    # minVol = volRange[0]
    # maxVol = volRange[1]

    # volume.SetMasterVolumeLevel(-30.0, None)

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    pTime = 0

    detector = htm.handDetector()
    volBar = 400
    volPer = 0
    vol = 0
    while True:
        success, img = cap.read()
        img = detector.findhands(img=img)

        lmlist = detector.findPosition(img=img, draw=False)
        if len(lmlist) != 0:
            # print(lmlist[4], lmlist[8])
            x1, y1 = lmlist[4][1], lmlist[4][2]
            x2, y2 = lmlist[8][1], lmlist[8][2]

            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.circle(img=img, center=(x1, y1), radius=15, color=(255, 0, 255), thickness=cv2.FILLED)
            cv2.circle(img=img, center=(x2, y2), radius=15, color=(255, 0, 255), thickness=cv2.FILLED)
            cv2.circle(img=img, center=(cx, cy), radius=15, color=(255, 0, 255), thickness=cv2.FILLED)
            cv2.line(img=img, pt1=(x1, y1), pt2=(x2, y2), color=(255, 0, 255), thickness=3)

            length = math.hypot(x2 - x1, y2 - y1)

            # vol = np.interp(length, [50, 300], [minVol, maxVol])
            volBar = np.interp(length, [50, 300], [400, 150])
            volPer = np.interp(length, [50, 300], [0, 100])

            # print(int(length), int(vol))
            # Hand range 50 - 300
            # Volume Range -65 - 0
            # change Volume
            # volume.SetMasterVolumeLevel(vol, None)

        cv2.rectangle(img=img, pt1=(50, 150), pt2=(85, 400), color=(255, 0, 0), thickness=3)
        cv2.rectangle(img=img, pt1=(50, int(volBar)), pt2=(85, 400), color=(255, 0, 0), thickness=cv2.FILLED)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, f'FPS: {int(fps)} ', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
        cv2.putText(img, f'{int(volPer):3} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

        cv2.imshow("Img", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()

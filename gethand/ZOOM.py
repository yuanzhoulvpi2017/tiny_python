import cv2
import numpy as np
import mediapipe as mp
from HandTrackModel3 import HandDetector


class Zoom(object):
    def __init__(self, lmlist):
        self.lmlist = lmlist
        self.niehe = False
        self.standdistance = 0
        self.zoomvalue = 0

    def cal_distince(self, point1, point2):
        value = np.array(point2) - np.array(point1)
        value = value[1:]
        return np.sqrt(np.sum(value ** 2))

    def cal_data(self):
        #
        self.distance_2_5 = self.cal_distince(self.lmlist[2], self.lmlist[5])

        #
        self.distance_4_8 = self.cal_distince(self.lmlist[4], self.lmlist[8])

        if self.distance_4_8 < self.distance_2_5 / 3:
            self.niehe = True
        else:
            self.niehe = False

        self.standdistance = np.mean([self.cal_distince(self.lmlist[5], self.lmlist[9]),
                                      self.cal_distince(self.lmlist[9], self.lmlist[13]),
                                      self.cal_distince(self.lmlist[13], self.lmlist[17]),
                                      ])

        val_data = 6
        if self.distance_4_8 <= self.standdistance:
            self.zoomvalue = 0
        elif self.standdistance < self.distance_4_8 < self.standdistance * val_data:
            self.zoomvalue = self.distance_4_8 / (self.standdistance * val_data) * 100

        else:
            self.zoomvalue = 100

    def __call__(self, *args, **kwargs):
        self.cal_data()


def main():
    cap = cv2.VideoCapture(0)

    detector = HandDetector(detectionCon=0.7, trackCon=0.7)

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)

        if success:
            img = detector.findhands(img)

            firsthand_lmlist = detector.findposition(handno=0)

            if len(firsthand_lmlist) == 21:
                zoom_dict = Zoom(lmlist=firsthand_lmlist)
                zoom_dict()
                print(f"是否拿捏: {zoom_dict.niehe} 缩放比例：{zoom_dict.zoomvalue:.2f}")

        cv2.imshow(winname="pose", mat=img)
        cv2.waitKey(1)

    cap.release()


if __name__ == '__main__':
    main()

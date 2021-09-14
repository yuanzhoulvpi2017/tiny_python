import cv2
import mediapipe as mp
import time


class HandDetector(object):
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.h = None
        self.w = None
        self.c = None

    def findhands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.h, self.w, self.c = img.shape

        self.results = self.hands.process(image=img_rgb)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image=img, landmark_list=handLms,
                                               connections=self.mpHands.HAND_CONNECTIONS)

        return img

    def findposition(self, handno=0):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handno]

            for id, lm in enumerate(myHand.landmark):
                # h, w, c = img.shape
                cx, cy = int(lm.x * self.w), int(lm.y * self.h)
                lmList.append([id, cx, cy])

        return lmList


def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    while True:
        success, img = cap.read()

        img = detector.findhands(img)
        lm_list = detector.findposition()

        if len(lm_list) != 0:
            print(lm_list[4])

        cv2.imshow(winname="test", mat=img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()

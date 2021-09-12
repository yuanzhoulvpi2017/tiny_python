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

    def findhands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(image=img_rgb)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image=img, landmark_list=handLms,
                                               connections=self.mpHands.HAND_CONNECTIONS)

        return img

    def findposition(self, img, handno=0, draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handno]

            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                lmList.append([id, cx, cy])

                if draw:
                    cv2.circle(img, (cx, cy), 2, (255, 0, 0), cv2.FILLED)

        return lmList


def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    while True:
        success, img = cap.read()

        img = detector.findhands(img)
        lm_list = detector.findposition(img=img, draw=False)

        if len(lm_list) != 0:
            print(lm_list[4])

        cv2.imshow(winname="test", mat=img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()

import cv2
import mediapipe as mp
import time





cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = cap.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(image=imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)
                if id in [4, 8]:
                    cv2.circle(img=img, center=(cx, cy), radius=20, color=(255, 0, 255), thickness=cv2.FILLED)
            mpDraw.draw_landmarks(image=img, landmark_list=handLms, connections=mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = time.time()

    cv2.putText(img=img, text=f"FPS: {int(fps)}", org=(10, 70), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2,
                color=(255, 0, 0), thickness=3)

    cv2.imshow("image", img)
    cv2.waitKey(1)

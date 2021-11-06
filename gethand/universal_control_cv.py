import cv2
import numpy as np

def main():
    # init cv
    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        print(img.shape)
        print(
            f"width: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}, height: {cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}, fps: {cap.get(cv2.CAP_PROP_FPS)}")
        cv2.rectangle(img=img, pt1=(100, 100), pt2=(100 + 600, 100 + 500), color=(0, 0, 0), thickness=2)
        cv2.imshow(winname="universal control", mat=img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()

import time

import cv2
import mediapipe as mp
import numpy as np

from HandTrackModel2 import HandDetector


# def show_single_char(img, start=(200, 200), width=100, height=100):
#     x, y = start
#
#     sub_img = img[y:(y + height), x:(x + width)]
#     white_rect = np.full(shape=sub_img.shape, fill_value=255, dtype=np.uint8)
#
#     res = cv2.addWeighted(sub_img, 0.5, white_rect, 0.5, 1.0)
#     img[y:(y + height), x:(x + width)] = res
#     return img


class KeyBorad(object):

    def __init__(self, rect_start=(100, 100), width=60, height=60, gap=10):
        self.letter__ = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
                         ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
                         ['Z', 'X', 'C', 'V', 'B', 'N', 'M']]
        self.rect_start_x_init = rect_start[0]
        self.rect_start_y_init = rect_start[1]
        self.width = width
        self.height = height
        self.gap = gap
        self.rect_start_x_list = [rect_start[0] + int(width / 2 * i) for i in range(len(self.letter__))]
        self.rect_start_y_list = [rect_start[1] + int((height + gap) * i) for i in range(len(self.letter__))]
        self.rect_data = None
        self.letter_data = None

    def cal_rect_data(self):
        self.rect_data = [[(self.rect_start_x_list[i] + (self.width + self.gap) * j, self.rect_start_y_list[i]) for j in
                           range(len(self.letter__[i]))] for i in range(len(self.letter__))]

    def cal_letter_data(self):
        self.letter_data = [[(self.rect_start_x_list[i] + (self.width + self.gap) * j,  # + int(self.width / 2),
                              self.rect_start_y_list[i] + int(self.height / 2)) for j in
                             range(len(self.letter__[i]))] for i in range(len(self.letter__))]

    def add_keyboard(self, img):
        for i_index, i_value in enumerate(self.rect_data):
            for j_index, j_value in enumerate(i_value):
                sub_img = img[j_value[1]:(j_value[1] + self.height), j_value[0]:(j_value[0] + self.width)]
                white_rect = np.full(shape=sub_img.shape, fill_value=255, dtype=np.uint8)
                res = cv2.addWeighted(sub_img, 0.5, white_rect, 0.5, 1.0)
                img[j_value[1]:(j_value[1] + self.height), j_value[0]:(j_value[0] + self.width)] = res

                cv2.putText(img=img, text=self.letter__[i_index][j_index],
                            org=(self.letter_data[i_index][j_index][0], self.letter_data[i_index][j_index][1]),
                            fontFace=cv2.FONT_HERSHEY_PLAIN,
                            fontScale=3, color=(0, 0, 0), thickness=2)

        return img

    def detector_figure_on_keyboard(self, img, figure_position):
        cx, cy = figure_position[1], figure_position[2]
        for i_index, i_value in enumerate(self.rect_data):
            for j_index, j_value in enumerate(i_value):
                if (j_value[0] <= cx <= (j_value[0] + self.width)) and (j_value[1] <= cy <= (j_value[1] + self.height)):
                    print(f'-----> detection letter: {self.letter__[i_index][j_index]}')
                    cv2.rectangle(img=img, pt1=(j_value[0], j_value[1]),
                                  pt2=(j_value[0] + self.width, j_value[1] + self.height),
                                  color=(204, 102, 0), thickness=2)

    def __call__(self, *args, **kwargs):
        self.cal_rect_data()
        self.cal_letter_data()


def main():
    # init keyboard
    keyboard = KeyBorad(rect_start=(100, 100), width=70, height=70, gap=10)
    keyboard()

    # init cv
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 40)

    # init detector
    detector = HandDetector(detectionCon=0.8)

    while True:
        success, img = cap.read()

        if img is not None:

            img = keyboard.add_keyboard(img)

            img = detector.findhands(img)
            lm_list = detector.findposition(img=img, draw=False)

            if len(lm_list) != 0:
                # print(lm_list[4])
                # print(lm_list[8])
                cv2.circle(img=img, center=(lm_list[4][1], lm_list[4][2]), radius=5, color=(0, 0, 0),
                           thickness=cv2.FILLED)
                cv2.circle(img=img, center=(lm_list[8][1], lm_list[8][2]), radius=5, color=(204, 102, 0),  # bgr
                           thickness=cv2.FILLED)
                keyboard.detector_figure_on_keyboard(img=img, figure_position=lm_list[8])

            cv2.imshow(winname="test", mat=img)
            cv2.waitKey(1)


if __name__ == '__main__':
    main()

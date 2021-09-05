import time

import cv2
import mediapipe as mp
import numpy as np
import datetime
from HandTrackModel2 import HandDetector
from collections import deque


def caldistince(first, second):
    data = np.sqrt(np.sum((np.array(first[:2]) - second[:2]) ** 2))
    # print(data)
    return data


# class ResultData(object):
#     def __init__(self):
#         self.text = deque(maxlen=4)
#
#     def add_text(self, text):
#         self.text.append(text)
#
#


class KeyBorad(object):

    def __init__(self, rect_start=(100, 100), width=60, height=60, gap=10):
        self.letter__ = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
                         ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
                         ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ' ', 'cl']]
        self.rect_start_x_init = rect_start[0]
        self.rect_start_y_init = rect_start[1]
        self.width = width
        self.height = height
        self.gap = gap
        self.rect_start_x_list = [rect_start[0] + int(width / 2 * i) for i in range(len(self.letter__))]
        self.rect_start_y_list = [rect_start[1] + int((height + gap) * i) for i in range(len(self.letter__))]
        self.rect_data = None
        self.letter_data = None
        # 检验是否点击
        self.distint_data = None
        # 检验是否点击成功
        self.click_success = False
        # 返回键盘输出的结果
        self.output_letter = deque(maxlen=20)
        self.output_status = False

        # 这里是缓冲区，用来识别手指在虚拟键盘的位置
        self.figure_8_x = deque(maxlen=10)
        self.figure_8_y = deque(maxlen=10)

        # 这里是缓冲区，用来记录点击键盘的字母和时间

        self.click_letter = deque(maxlen=3)
        self.click_datetime = deque(maxlen=3)

    def smoothdata(self, cx, cy):
        self.figure_8_x.append(cx)
        self.figure_8_y.append(cy)

        smooth_x = np.median(list(self.figure_8_x))
        smooth_y = np.median(list(self.figure_8_y))

        return smooth_x, smooth_y

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

    def detector_figure_on_keyboard(self, img, figure_position, lm_list):
        # cx, cy = figure_position[1], figure_position[2]

        cx, cy = self.smoothdata(figure_position[1], figure_position[2])
        for i_index, i_value in enumerate(self.rect_data):
            for j_index, j_value in enumerate(i_value):
                if (j_value[0] <= cx <= (j_value[0] + self.width)) and (j_value[1] <= cy <= (j_value[1] + self.height)):
                    self.distint_data = caldistince(first=lm_list[4], second=lm_list[12])
                    self.click_success = self.distint_data is not None and self.distint_data <= 100

                    if self.click_success:
                        self.output_status = False
                        self.click_letter.append(self.letter__[i_index][j_index])
                        self.click_datetime.append(datetime.datetime.now())
                    cv2.drawMarker(img=img, position=(int(cx), int(cy)), color=(255, 0, 0),
                                   markerType=cv2.MARKER_TILTED_CROSS, markerSize=20)
                    cv2.rectangle(img=img, pt1=(j_value[0], j_value[1]),
                                  pt2=(j_value[0] + self.width, j_value[1] + self.height),
                                  color=(204, 102, 0), thickness=2)
                else:
                    cv2.circle(img=img, center=(int(cx), int(cy)), radius=5, color=(204, 102, 0),  # bgr
                               thickness=cv2.FILLED)

    def finalletter(self):
        letter_list = list(self.click_letter)
        if self.click_success and len(letter_list) != 0:
            time.sleep(0.16)
            print(f"---> letter: {letter_list[-1]}")
            if letter_list[-1] == 'cl':
                try:
                    self.output_letter.pop()
                except Exception as e:
                    print('已经清除完毕')
                    pass
            else:
                self.output_letter.append(letter_list[-1])
            print(f"---> all letter: {list(self.output_letter)}")

    def show_result(self, img):
        cv2.putText(img=img, text=' '.join(list(self.output_letter)),
                    org=(100, 490),
                    fontFace=cv2.FONT_HERSHEY_PLAIN,
                    fontScale=3, color=(255, 0, 127), thickness=3)
        cv2.line(img=img, pt1=(100, 500), pt2=(1200, 500), color=(0, 0, 0), thickness=2, lineType=cv2.LINE_4)

    def __call__(self, *args, **kwargs):
        self.cal_rect_data()
        self.cal_letter_data()


def main():
    # init text
    # click_text = ResultData()

    # init keyboard
    keyboard = KeyBorad(rect_start=(100, 100), width=65, height=65, gap=5)
    keyboard()

    # init cv
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1200)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 700)
    cap.set(cv2.CAP_PROP_FPS, 20)

    # init detector
    detector = HandDetector(detectionCon=0.7, trackCon=0.9)

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)

        if img is not None:
            img = detector.findhands(img)  # 这个时候，已经计算好手在图像中的所有位置数据了。
            img = keyboard.add_keyboard(img)  # 显示键盘

            lm_list = detector.findposition(img=img, draw=False)

            if len(lm_list) != 0:
                # print(lm_list[4])
                # print(lm_list[8])
                # cv2.circle(img=img, center=(lm_list[4][1], lm_list[4][2]), radius=5, color=(0, 0, 0),
                #            thickness=cv2.FILLED)
                # cv2.circle(img=img, center=(lm_list[8][1], lm_list[8][2]), radius=5, color=(204, 102, 0),  # bgr
                #            thickness=cv2.FILLED)
                keyboard.detector_figure_on_keyboard(img=img, figure_position=lm_list[8], lm_list=lm_list)
                keyboard.finalletter()

                keyboard.show_result(img=img)

                # if keyboard.output_status:
                #     click_text.add_text(keyboard.output_letter)
                #     print(list(click_text.text))

            cv2.imshow(winname="get letter", mat=img)
            cv2.waitKey(1)


if __name__ == '__main__':
    main()

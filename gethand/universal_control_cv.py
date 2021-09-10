import cv2
import numpy as np


class PanelLayout(object):
    def __init__(self, cap):
        self.cv2_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.cv2_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.cv2_fps = cap.get(cv2.CAP_PROP_FPS)

        self.start_width = None
        self.start_height = None
        self.monitor_width = None
        self.monitor_height = None

        self.monitor_pt1 = None
        self.monitor_pt2 = None


    def draw_data(self, start_width_per=0.06, start_height_per=0.1, monitor_width_per=0.7, monitor_height_per=0.8):

        self.start_width = int(self.cv2_width * start_width_per)
        self.start_height = int(self.cv2_height * start_height_per)
        self.monitor_width = int(self.cv2_width * monitor_width_per)
        self.monitor_height = int(self.cv2_height * monitor_height_per)

        self.monitor_pt1 = (self.start_width, self.start_height)
        self.monitor_pt2 = (self.start_width+self.monitor_width, self.start_height+self.monitor_height)

    def draw_act(self, img):
        sub_img = img[self.start_height:(self.start_height+self.monitor_height), self.start_width:(self.start_width+self.monitor_width)]
        white_rect = np.full(shape=sub_img.shape, fill_value=255, dtype=np.uint8)
        res = cv2.addWeighted(sub_img, 0.5, white_rect, 0.5, 1.0)
        img[self.start_height:(self.start_height+self.monitor_height), self.start_width:(self.start_width+self.monitor_width)] = res

        cv2.rectangle(img=img, pt1=self.monitor_pt1, pt2=self.monitor_pt2, color=(0, 0, 0), thickness=2)

        # print(f"fps: {self.cv2_fps}")


    # def __call__(self, *args, **kwargs):
    #     self.draw_data()


def main():
    # init cv
    cap = cv2.VideoCapture(0)
    panellayout = PanelLayout(cap=cap)
    panellayout.draw_data()

    while cap.isOpened():
        success, img = cap.read()
        img = cv2.flip(img,flipCode=1)
        panellayout.draw_act(img=img)
        cv2.imshow(winname="universal control", mat=img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()

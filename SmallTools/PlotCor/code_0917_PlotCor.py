"""
绘制变量的cor的小工具
小demo 一个小时左右完成的，代码有些粗糙～
"""
import sys

import matplotlib.pyplot as plt
import pandas as pd

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel, QFileDialog, QComboBox, QMessageBox
import seaborn as sns
from datetime import datetime
import matplotlib
from pathlib import Path

matplotlib.use('Qt5Agg')


class PlotCor(QWidget):
    def __init__(self):
        super(PlotCor, self).__init__()
        self.plot_data_ = None
        self._path_filename = None
        self.x_label = None
        self.y_label = None
        self.initUI()

    def initUI(self):
        self.resize(300, 48)
        self.setWindowTitle("Plot scatter")
        # layout
        label_title_list = [QLabel(i)
                            for i in ['选择文件', 'x轴变量', 'y轴变量', '生成图片']]

        grid = QGridLayout()
        grid.setSpacing(1)
        for index, temp_label in enumerate(label_title_list):
            grid.addWidget(temp_label, index, 0)

        # 选择文件按钮
        select_file_b1 = QPushButton(text="选择文件")
        select_file_b1.setChecked(True)
        select_file_b1.clicked[bool].connect(self.select_file)

        # 设置x轴
        self.select_x_label = QComboBox()
        self.select_x_label.addItem('none')
        self.select_x_label.currentIndexChanged[str].connect(self.get_x_label_value)
        self.select_x_label.highlighted[str].connect(self.get_x_label_value)

        # 设置y轴按钮

        self.select_y_label = QComboBox()
        self.select_y_label.addItem('none')
        self.select_y_label.currentIndexChanged[str].connect(self.get_y_label_value)

        self.select_y_label.highlighted[str].connect(self.get_y_label_value)

        # 生成模型
        self.save_fig_button = QPushButton('生成图像')
        self.save_fig_button.setChecked(True)
        self.save_fig_button.clicked.connect(self.save_fig_func)
        # self.save_fig_button.clicked[bool].connect(self.save_fig_func)
        # list
        inter_button_list = [select_file_b1, self.select_x_label, self.select_y_label, self.save_fig_button]

        for index, temp_button in enumerate(inter_button_list):
            grid.addWidget(temp_button, index, 1)

        self.setLayout(grid)

        self.show()

    def save_fig_func(self):
        # data
        data = self.plot_data_
        x_label = self.x_label
        y_label = self.y_label

        if data is None:
            QMessageBox.warning(self, "警告⚠️", "请务必选择一个数据!!!", QMessageBox.Cancel)
        else:
            if x_label is None or y_label is None or x_label == 'none' or y_label == 'none':
                QMessageBox.warning(self, "警告⚠️", "请务必设置好x轴和y轴标签", QMessageBox.Cancel)
            else:
                if x_label == y_label:
                    QMessageBox.warning(self, "警告⚠️", "x轴标签和y轴标签不可以相等哦～", QMessageBox.Cancel)
                else:
                    dir_name = self._path_filename.parent
                    save_png_path = dir_name.joinpath(f'test2{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.png')
                    g = sns.jointplot(x=x_label, y=y_label, data=data, kind="reg", truncate=False)
                    g.savefig(save_png_path)
                    QMessageBox.information(self, "通知", "文件已经生成 保存到文件夹中(数据所在的文件夹下)",
                                            QMessageBox.Ok | QMessageBox.Close, QMessageBox.Close)

        # plot

    def select_file(self):
        """
        打开一个文件夹，选中一个文件
        :return:
        """
        file_filter_ = "All Files (*);;Text Files (*.csv);;Excel Files(*.xlsx)"
        filename, file_type = QFileDialog.getOpenFileName(caption="选择数据",
                                                          directory="",
                                                          filter=file_filter_)

        if filename is not None or filename != '':

            self._path_filename = Path(filename)
            if self._path_filename.suffix == '.csv':
                self.plot_data_ = pd.read_csv(filename)
            elif self._path_filename.suffix in ['.xlsx', '.xls']:
                self.plot_data_ = pd.read_excel(filename)
            else:
                self.plot_data_ = None
                QMessageBox.warning(self, "警告⚠️", "选中的文件非csv文本格式、非Excel格式", QMessageBox.Cancel)

            if self.plot_data_ is not None:

                col_name = self.plot_data_.columns.tolist()
                if len(col_name) < 2:
                    QMessageBox.warning(self, "警告⚠️", "选中的数据不足两列,请尝试别的数据～", QMessageBox.Cancel)
                else:

                    if self.select_x_label.count() > 0:
                        for _ in range(self.select_x_label.count()):
                            self.select_x_label.removeItem(0)
                    self.select_x_label.addItems(col_name)

                    if self.select_y_label.count() > 0:
                        for _ in range(self.select_y_label.count()):
                            self.select_y_label.removeItem(0)
                    self.select_y_label.addItems(col_name)

    def get_x_label_value(self, i):
        self.x_label = i

    def get_y_label_value(self, i):
        self.y_label = i


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pc = PlotCor()
    sys.exit(app.exec())

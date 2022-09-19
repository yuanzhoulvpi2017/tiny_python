"""
批量修改文件名称的小工具
"""

import sys

import pandas as pd
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QGridLayout, QPushButton,
                             QLabel, QFileDialog,
                             QProgressBar, QMessageBox)
from datetime import datetime
import os
from pathlib import Path
import shutil


class RenameFile(QWidget):
    def __init__(self):
        super(RenameFile, self).__init__()
        self.bad_file_dir_path = None
        self.map_file_path = None
        self.map_file_data = None
        self.batch_progressbar = None
        self.initUI()

    def initUI(self):
        self.resize(300, 100)
        self.setWindowTitle("批量修改文件名称")

        grid = QGridLayout()
        grid.setSpacing(1)

        label_title_list = [QLabel(i) for i in ['文件所在的文件夹', '名称对照表', '开始处理']]

        for index, temp_label in enumerate(label_title_list):
            grid.addWidget(temp_label, index, 0)

        select_dir_b1 = QPushButton(text="选择文件夹")
        select_dir_b1.setChecked(True)
        select_dir_b1.clicked[bool].connect(self.select_dir)

        select_map_file_b2 = QPushButton(text="选择名称对照表")
        select_map_file_b2.setChecked(True)
        select_map_file_b2.clicked[bool].connect(self.select_map_file)

        select_start2run_b3 = QPushButton(text="开始运行")
        select_start2run_b3.setChecked(True)
        select_start2run_b3.clicked[bool].connect(self.start2run)

        button_list = [select_dir_b1, select_map_file_b2, select_start2run_b3]

        for index, temp_button in enumerate(button_list):
            grid.addWidget(temp_button, index, 1)

        self.batch_progressbar = QProgressBar()
        self.batch_progressbar.setFormat('%p%')

        # self.statusbar = QStatusBar()
        # self.statusbar.setObjectName('进度条')
        # self.statusbar.addPermanentWidget(self.batch_progressbar, stretch=10)
        # self.setStatusBar(self.statusbar)

        grid.addWidget(self.batch_progressbar, len(label_title_list), 0, 1, 2)

        self.setLayout(grid)

        self.show()

    def select_dir(self):
        bad_file_dir = QFileDialog.getExistingDirectory(caption='选择所在的文件夹')

        if bad_file_dir is not None and bad_file_dir != '':
            bad_file_dir_path = Path(bad_file_dir)
            self.bad_file_dir_path = bad_file_dir_path

    def select_map_file(self):
        file_filter_ = "Excel Files(*.xls);;Text Files (*.csv);;Excel Files(*.xlsx)"
        file_name, file_type = QFileDialog.getOpenFileName(caption="名称对照表",
                                                           directory="",
                                                           filter=file_filter_)

        if file_name is not None and file_name != '':
            self.map_file_path = Path(file_name)

            if self.map_file_path.suffix == '.csv':
                self.map_file_data = pd.read_csv(file_name)
            elif self.map_file_path.suffix in ['.xlsx', '.xls']:
                self.map_file_data = pd.read_excel(file_name)

            value = 0

            for i in ['旧文件名称', '新文件名称']:
                if i not in self.map_file_data.columns.tolist():
                    QMessageBox.warning(self,
                                        '警告',
                                        f'名称对照表必须有表头{i},请完善表格的表头', QMessageBox.Cancel)
                else:
                    value += 1

            if value == 2:
                self.map_file_data = self.map_file_data[['旧文件名称', '新文件名称']]
                self.batch_progressbar.setMaximum(self.map_file_data.shape[0])
                # print(self.map_file_data)

    def start2run(self):

        curdate_dir = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        if self.bad_file_dir_path is not None \
                and self.map_file_data is not None:

            new_folder = self.bad_file_dir_path.parent.joinpath(curdate_dir)
            if new_folder.exists():
                shutil.rmtree(path=new_folder)
            else:
                os.makedirs(name=new_folder, exist_ok=True)

            self.map_file_data = self.map_file_data.pipe(
                lambda x: x.assign(
                    **{'old_full_path': x['旧文件名称'].apply(lambda x: self.bad_file_dir_path.joinpath(x)),
                       'new_full_path': x['新文件名称'].apply(lambda x: new_folder.joinpath(x))})
            )
            # self.map_file_data = self.map_file_data.head(3)
            for index, row in self.map_file_data.iterrows():
                if row['old_full_path'].exists():
                    os.rename(src=row['old_full_path'], dst=row['new_full_path'])
                    self.batch_progressbar.setValue(index + 1)
                else:
                    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pc = RenameFile()
    sys.exit(app.exec())
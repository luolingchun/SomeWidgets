# -*- coding: utf-8 -*-
# @Author  : llc
# @Email   : luolingchun.com@gmail.com
# @Time    : 2019/8/25 16:08
# @File    : test_progress_dialog.py
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QPushButton,QCommonStyle

from SomeWidgets import SProgressDialog


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.resize(500, 500)
        pushbutton = QPushButton('test', self)
        pushbutton.clicked.connect(self.show_progress)

    def show_progress(self):
        self.spd = SProgressDialog(self, label_text='loading...')
        self.spd.setModal(True)
        # 隐藏取消按钮
        # self.spd.hide_cancel_button()
        # 获取标签文本
        print(self.spd.label_text)
        # 获取取消那妞
        cancel_button = self.spd.cancel_button
        print(cancel_button)
        # 获取Qss
        print(self.spd.qss)
        self.spd.show()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(50)

    def update_progress(self):
        self.spd.value = self.spd.value + 1
        if self.spd.value == 100:
            self.timer.stop()
            self.spd.close()


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()

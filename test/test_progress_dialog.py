# -*- coding: utf-8 -*-
# @Author  : llc
# @Email   : luolingchun.com@gmail.com
# @Time    : 2019/8/25 16:08
# @File    : test_progress_dialog.py
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QPushButton

from SomeWidgets import SProgressDialog


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.resize(500, 300)
        pushbutton = QPushButton('test', self)
        pushbutton.clicked.connect(self.show_progress)

    def show_progress(self):
        self.spd = SProgressDialog(self, label_text='loading...')
        self.spd.setModal(True)
        # 标签文本
        print(self.spd.label_text)
        # 取消按钮
        cancel_button = self.spd.cancel_button
        # 隐藏取消按钮
        # cancel_button.hide()
        # 取消阴影
        # self.spd.hide_shadow()
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

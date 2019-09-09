# -*- coding: utf-8 -*-
# @Time    : 2019/9/9 9:01
# @Author  : llc
# @File    : test_media_slider.py
import os

from PyQt5.QtWidgets import QMainWindow

from SomeWidgets import SMediaSlider


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setStyleSheet("""
        QMainWindow{
            background-color:rgba(39, 40, 34,100);
        }
        """)

        max_time = '2:19:03'
        h, m, s = max_time.split(':')
        max_value = int(h) * 3600 + int(m) * 60 + int(s)
        print(max_value)

        self.sms = SMediaSlider(max_value, parent=self)
        self.sms.move(0, 50)
        self.sms.setFixedWidth(600)
        self.sms.valueChanged.connect(self.update_time)

        self.resize(600, 150)

        self.sms.left = '0:00:00'
        self.sms.right = max_time

    def update_time(self, v):
        s = v % 60
        m = v // 60
        if m >= 60:
            h = m // 60
            m = m % 60
        else:
            h = 0
        self.sms.left = f'{h}:{m:02}:{s:02}'


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    window = Window()
    window.show()

    # from pyqss import Qss
    #
    # qss = Qss(window)
    # qss.show()

    app.exec_()

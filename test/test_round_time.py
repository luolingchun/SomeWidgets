# -*- coding: utf-8 -*-
# @Time    : 2019/10/21 16:18
# @Author  : llc
# @File    : test_round_time.py
from PyQt5.QtWidgets import QWidget

from SomeWidgets import SRoundTime


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.resize(700, 700)

        srt = SRoundTime(self)
        srt.move(50, 50)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()

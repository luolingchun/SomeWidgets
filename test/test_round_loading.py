# -*- coding: utf-8 -*-
# @Time    : 2019/10/14 14:39
# @Author  : llc
# @File    : test_line_loading.py
from PyQt5.QtCore import QEasingCurve
from PyQt5.QtWidgets import QWidget, QPushButton

from SomeWidgets import SRoundLoading


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.resize(500, 200)
        self.pushbutton = QPushButton('start', self)

        sll1 = SRoundLoading(parent=self)
        sll1.resize(90, 90)
        sll1.move(50, 50)

        sll2 = SRoundLoading(ball_radius=5, ball_color=(200, 100, 100), parent=self)
        sll2.resize(90, 90)
        sll2.move(150, 50)

        sll3 = SRoundLoading(ball_radius=6, ball_color=(100, 100, 200), parent=self)
        sll3.resize(90, 90)
        sll3.move(250, 50)

        sll4 = SRoundLoading(ball_radius=7, ball_colour=True, parent=self)
        sll4.resize(90, 90)
        sll4.move(350, 50)

        def start():
            sll1.start()
            sll2.start()
            sll3.start()
            sll4.start()

        self.pushbutton.clicked.connect(start)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()

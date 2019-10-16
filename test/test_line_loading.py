# -*- coding: utf-8 -*-
# @Time    : 2019/10/14 14:39
# @Author  : llc
# @File    : test_line_loading.py
from PyQt5.QtWidgets import QWidget, QPushButton

from SomeWidgets import SLineLoading


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.resize(800, 500)
        self.pushbutton = QPushButton('start', self)

        sll1 = SLineLoading(ball_radius=5, duration=3000, duration_pause=150, parent=self)
        sll1.resize(800, 100)
        sll1.move(0, 50)

        sll2 = SLineLoading(ball_radius=5, ball_color=(200, 100, 100), duration=3000, duration_pause=150, parent=self)
        sll2.resize(800, 100)
        sll2.move(0, 150)

        sll3 = SLineLoading(ball_radius=5, ball_color=(100, 100, 200), duration=3000, duration_pause=150, parent=self)
        sll3.resize(800, 100)
        sll3.move(0, 250)

        sll4 = SLineLoading(ball_radius=5, ball_colour=True, duration=3000, duration_pause=150, parent=self)
        sll4.resize(800, 100)
        sll4.move(0, 350)

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

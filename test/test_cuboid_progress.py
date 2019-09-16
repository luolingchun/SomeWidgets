# -*- coding: utf-8 -*-
# @Author  : llc
# @Email   : luolingchun.com@gmail.com
# @Time    : 2019/9/13 12:06
# @File    : test_cuboid_progress.py
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QPushButton, QDialog, QSlider

from SomeWidgets import SCuboidProgress


class Window(QDialog):
    def __init__(self):
        super(Window, self).__init__()
        self.resize(600, 400)

        self.setStyleSheet("""background-color:#515151""")

        button1 = QPushButton('start1', self)
        button1.setStyleSheet("""color:white""")
        button1.clicked.connect(self.start1)

        button2 = QPushButton('start2', self)
        button2.move(100, 0)
        button2.setStyleSheet("""color:white""")
        button2.clicked.connect(self.start2)

        slider = QSlider(self)
        slider.setOrientation(Qt.Horizontal)
        slider.move(200, 0)
        slider.valueChanged.connect(self.slider_valueChanged)

        self.scp1 = SCuboidProgress(color1=QColor(254, 154, 227), parent=self)
        self.scp1.move(100, 100)
        self.scp1.resize(300, 50)

        self.scp2 = SCuboidProgress(color1=QColor(174, 255, 126), parent=self)
        self.scp2.move(100, 200)
        self.scp2.resize(300, 50)

        self.scp3 = SCuboidProgress(color1=QColor(165, 217, 255), parent=self)
        self.scp3.move(100, 300)
        self.scp3.resize(300, 50)

        slider.setValue(50)

    def start1(self):
        self.timer = QTimer()
        self.timer.start(10)
        self.timer.timeout.connect(self.update_progress1)

    def start2(self):
        self.timer = QTimer()
        self.timer.start(10)
        self.timer.timeout.connect(self.update_progress2)

    def update_progress1(self):
        if self.scp1.value <= 99:
            self.scp1.value += 1
            self.scp2.value += 1
            self.scp3.value += 1
        else:
            self.timer.stop()

    def update_progress2(self):
        if self.scp1.value >= 1:
            self.scp1.value -= 1
            self.scp2.value -= 1
            self.scp3.value -= 1
        else:
            self.timer.stop()

    def slider_valueChanged(self, v):
        print(v)
        o = v / 100
        self.scp1.opacity = o
        self.scp2.opacity = o
        self.scp3.opacity = o


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()

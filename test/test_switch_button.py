# -*- coding: utf-8 -*-
# @Time    : 2019/9/3 13:06
# @Author  : llc
# @File    : test_switch_button.py
from PyQt5.QtCore import QEasingCurve
from PyQt5.QtWidgets import QWidget

from SomeWidgets import SSwitchButton


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        animation = [QEasingCurve.Linear, QEasingCurve.BezierSpline, QEasingCurve.OutElastic, QEasingCurve.OutBack,
                     QEasingCurve.OutExpo, QEasingCurve.OutBounce, QEasingCurve.OutInBack, QEasingCurve.InBack,
                     QEasingCurve.InOutBack
                     ]

        count = 0
        for x in range(3):
            for y in range(3):
                # ssb = SSwitchButton(self, animation=animation[count])
                width, height, margin = 100, 50, 5
                ssb = SSwitchButton(self, width=width, height=height, margin=margin, animation=animation[count])
                ssb.ActiveChanged.connect(lambda opened: print(opened))
                ssb.move(x * (width + 5) + 100, y * (height + 10) + 100)
                count += 1


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()

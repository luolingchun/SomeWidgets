# -*- coding: utf-8 -*-
# @Time    : 2019/9/3 9:47
# @Author  : llc
# @File    : switch.py
from PyQt5.QtCore import pyqtSignal, QPoint, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QLabel, QStyleOption, QStyle


class SSwitchButton(QWidget):
    ActiveChanged = pyqtSignal(bool)

    def __init__(self, parent=None, animation=QEasingCurve.OutBack):
        super(SSwitchButton, self).__init__(parent)
        self.setObjectName('SSwitchButton')

        self.opened = False
        self._start_point = QPoint(3, 3)
        self._end_point = QPoint(33, 3)

        self.setMinimumSize(60, 30)
        self.setMaximumSize(60, 30)
        self.resize(60, 30)

        self._label = QLabel(self)
        self._label.setObjectName('SButton')
        self._label.resize(24, 24)
        self._label.move(self._start_point)

        self._animation = QPropertyAnimation(self)
        self._animation.setTargetObject(self._label)
        self._animation.setPropertyName(b'pos')
        self._animation.setEasingCurve(animation)
        self._animation.setDuration(300)

        self.setStyleSheet(
            """
            #SSwitchButton{
                border:0px solid #dadada;
                border-radius:15px;
                background-color: #dadada;
            }
            #SButton{
                border:0px;
                border-radius:12px;
                background-color: white;
            }
            """
        )

    def mousePressEvent(self, event):
        if self._label.pos() == QPoint(3, 3):
            self._animation.setStartValue(self._start_point)
            self._animation.setEndValue(self._end_point)
            self._animation.start()
            self.opened = True
            self.setStyleSheet(
                """
                #SSwitchButton{
                    border:0px solid #dadada;
                    border-radius:15px;
                    background-color: #00EE00;
                }
                #SButton{
                    border:0px;
                    border-radius:12px;
                    background-color: white;
                }
                """
            )
        elif self._label.pos() == QPoint(33, 3):
            self._animation.setStartValue(self._end_point)
            self._animation.setEndValue(self._start_point)
            self._animation.start()
            self.opened = False
            self.setStyleSheet(
                """
                #SSwitchButton{
                    border:0px solid #dadada;
                    border-radius:15px;
                    background-color: #dadada;
                }
                #SButton{
                    border:0px;
                    border-radius:12px;
                    background-color: white;
                }
                """
            )
        else:
            return

        self.ActiveChanged.emit(self.opened)

    def paintEvent(self, event):
        super(SSwitchButton, self).paintEvent(event)
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QWidget

    app = QApplication([])
    window = QWidget()
    window.resize(500, 500)
    ssb = SSwitchButton(window)
    ssb.move(200, 200)
    window.show()

    # from pyqss import Qss
    #
    # qss = Qss(window)
    # qss.show()

    app.exec_()

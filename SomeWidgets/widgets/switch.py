# -*- coding: utf-8 -*-
# @Time    : 2019/9/3 9:47
# @Author  : llc
# @File    : switch.py
from PyQt5.QtCore import pyqtSignal, QPoint, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QLabel, QStyleOption, QStyle


class SSwitchButton(QWidget):
    ActiveChanged = pyqtSignal(bool)

    def __init__(self, parent=None, width=60, height=30, margin=3, animation=QEasingCurve.OutBack):
        super(SSwitchButton, self).__init__(parent)
        self.setObjectName('SSwitchButton')

        self._width = width
        self._height = height
        self._margin = margin

        self.opened = False
        self._ball_size = height - 2 * margin
        self._start_point = QPoint(margin, margin)
        self._end_point = QPoint(width - self._ball_size - margin, margin)

        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)
        self.resize(width, height)

        self._label = QLabel(self)
        self._label.setObjectName('SButton')
        self._label.resize(self._ball_size, self._ball_size)
        self._label.move(self._start_point)

        self._animation = QPropertyAnimation(self)
        self._animation.setTargetObject(self._label)
        self._animation.setPropertyName(b'pos')
        self._animation.setEasingCurve(animation)
        self._animation.setDuration(300)

        self.setStyleSheet(
            f"""
            #SSwitchButton{{
                border:0px solid #dadada;
                border-radius:{self._height / 2}px;
                background-color: #dadada;
            }}
            #SButton{{
                border:0px;
                border-radius:{self._ball_size / 2}px;
                background-color: white;
            }}
            """
        )

    def mousePressEvent(self, event):
        if self._label.pos() == self._start_point:
            self._animation.setStartValue(self._start_point)
            self._animation.setEndValue(self._end_point)
            self._animation.start()
            self.opened = True
            self.setStyleSheet(
                f"""
                #SSwitchButton{{
                    border:0px solid #dadada;
                    border-radius:{self._height / 2}px;
                    background-color: #00EE00;
                }}
                #SButton{{
                    border:0px;
                    border-radius:{self._ball_size / 2}px;
                    background-color: white;
                }}
                """
            )
        elif self._label.pos() == self._end_point:
            self._animation.setStartValue(self._end_point)
            self._animation.setEndValue(self._start_point)
            self._animation.start()
            self.opened = False
            self.setStyleSheet(
                f"""
                #SSwitchButton{{
                    border:0px solid #dadada;
                    border-radius:{self._height / 2}px;
                    background-color: #dadada;
                }}
                #SButton{{
                    border:0px;
                    border-radius:{self._ball_size / 2}px;
                    background-color: white;
                }}
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

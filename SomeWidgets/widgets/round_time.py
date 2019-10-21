# -*- coding: utf-8 -*-
# @Time    : 2019/10/18 9:33
# @Author  : llc
# @File    : round_time.py
import math
import time
from datetime import datetime

from PyQt5.QtCore import QPoint, Qt, QPointF, QRectF, QTimer, pyqtProperty, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtWidgets import QWidget


class SRoundTime(QWidget):
    def __init__(self, parent=None):
        super(SRoundTime, self).__init__(parent)
        self.resize(600, 600)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)

        t = datetime.now()
        self.year = t.year
        self.month = t.month
        self.day = t.day
        self.hour = t.hour
        self.minute = t.minute
        self.second = t.second
        self.font_size = 12
        self.current_font_size = 16
        self.frequency = 60
        self._flag_m = False
        self._flag_h = False

        timer = QTimer(self)
        timer.timeout.connect(self.update_second)
        timer.start(1000)

    def _set_second(self, ms):
        t, second = ms.x(), ms.y()
        t = datetime.fromtimestamp(t)
        hour = t.hour
        minute = t.minute
        self.second = second / self.frequency
        if int(self.second) == 59:
            self.minute = minute + math.modf(self.second)[0]
            self._flag_m = True
            if int(self.minute) == 59:
                self.hour = hour + math.modf(self.second)[0]
                self._flag_h = True
        if int(self.second) != 59:
            self._flag_m = False
            self.minute = datetime.now().minute
        if int(self.minute) != 59:
            self._flag_h = False
            self.hour = datetime.now().hour
        self.update()

    _second = pyqtProperty(QPoint, fset=_set_second)

    def update_second(self):
        t = int(time.time())
        now = datetime.now()
        second = now.second
        self.year = now.year
        self.month = now.month
        self.day = now.day
        pa = QPropertyAnimation(self, b'_second', self)
        pa.setEasingCurve(QEasingCurve.OutBounce)
        pa.setDuration(1000)
        pa.setStartValue(QPoint(t, second * self.frequency))
        pa.setEndValue(QPoint(t, (second + 1) * self.frequency))
        pa.start()

    def rotate(self, point, angle):
        arc = angle / 180 * math.pi
        length = math.sqrt(point.x() ** 2 + point.y() ** 2)
        return QPointF(length * math.cos(arc), length * math.sin(arc))

    def paintEvent(self, event):
        fs = self.font_size
        cfs = self.current_font_size
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        center_point = QPointF(self.width() / 2, self.height() / 2)
        p.translate(center_point)
        font = QFont()
        font.setFamily('consolas')
        font.setBold(True)
        font.setPointSize(cfs * 2)
        p.setFont(font)

        rect = QRectF(-10 * fs, - 2 * fs, 20 * fs, 4 * fs)
        p.drawText(rect, Qt.AlignCenter, f'{self.year}/{self.month:02}/{self.day:02}')

        hour = self.hour
        int_hour = int(hour)
        point_hour = QPoint(18 * fs, 0)

        minute = self.minute
        int_minute = int(minute)
        point_minute = QPoint(21 * fs, 0)

        second = self.second
        int_second = int(second)
        point_second = QPoint(24 * fs, 0)

        font.setPointSize(cfs)
        p.setFont(font)
        rect = QRectF(point_hour.x() + fs, point_hour.y() - fs - 1, 2 * fs, 2 * fs)
        p.drawText(rect, Qt.AlignVCenter, ':')

        rect = QRectF(point_minute.x() + fs, point_minute.y() - fs - 1, 2 * fs, 2 * fs)
        p.drawText(rect, Qt.AlignVCenter, ':')

        for H in range(int_hour, 24 + int_hour):
            point_hour = self.rotate(point_hour, (H + math.modf(hour)[0] + 1) * 15)
            H = 24 - H + int_hour - 1
            if H == int_hour + int(self._flag_h):
                font.setBold(True)
                font.setPointSize(cfs)
            elif H == 0 and int_hour == 23 and self._flag_h:
                font.setBold(True)
                font.setPointSize(cfs)
            else:
                font.setBold(False)
                font.setPointSize(fs)
            p.setFont(font)
            rect = QRectF(point_hour.x() - fs, point_hour.y() - fs, 2 * fs, 2 * fs)
            p.drawText(rect, Qt.AlignCenter, f'{H:02}')

        for M in range(int_minute, 60 + int_minute):
            point_minute = self.rotate(point_minute, (M + math.modf(minute)[0] + 1) * 6)
            M = 60 - M + int_minute - 1
            if M == int_minute + int(self._flag_m):
                font.setBold(True)
                font.setPointSize(cfs)
            elif int_minute == 59 and M == 0 and self._flag_m:
                font.setBold(True)
                font.setPointSize(cfs)
            else:
                font.setBold(False)
                font.setPointSize(fs)
            p.setFont(font)
            rect = QRectF(point_minute.x() - fs, point_minute.y() - fs, 2 * fs, 2 * fs)
            p.drawText(rect, Qt.AlignCenter, f'{M:02}')

        for S in range(int_second, 60 + int_second):
            point = self.rotate(point_second, (S + math.modf(second)[0] + 1) * 6)
            S = 60 - S + int_second - 1
            if S == int_second + 1 or S == 0 and int_second == 59:
                font.setBold(True)
                font.setPointSize(cfs)
            else:
                font.setBold(False)
                font.setPointSize(fs)
            p.setFont(font)
            rect = QRectF(point.x() - fs, point.y() - fs, 2 * fs, 2 * fs)
            p.drawText(rect, Qt.AlignCenter, f'{S:02}')


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    window = SRoundTime()
    window.show()
    app.exec_()

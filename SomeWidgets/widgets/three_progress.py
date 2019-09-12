# -*- coding: utf-8 -*-
# @Time    : 2019/9/11 16:02
# @Author  : llc
# @File    : three_progress.py
import math

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QColor, QPolygon, QLinearGradient, QBrush, QPen
from PyQt5.QtWidgets import QWidget


class SWidget(QWidget):
    def __init__(self, color1=QColor(0, 128, 0), color2=QColor(255, 255, 255), parent=None):
        super(SWidget, self).__init__(parent)
        self.p1 = QPoint(0, 0)
        self.p2 = QPoint(0, 0)
        self.p3 = QPoint(0, 0)
        self.p4 = QPoint(0, 0)
        self.color1 = color1
        self.color2 = color2
        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(0.7)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.white)
        painter.save()
        brush = QBrush(self.color1)
        painter.setBrush(brush)
        points = [self.p1,
                  self.p2,
                  QPoint(self.p2.x() + int(self.width() * self._value / 100), self.p2.y()),
                  QPoint(self.p1.x() + int(self.width() * self._value / 100), self.p1.y())]
        painter.drawPolygon(QPolygon(points))
        painter.restore()
        brush = QBrush(self.color2)
        painter.setBrush(brush)
        points = [QPoint(self.p1.x() + int(self.width() * self._value / 100), self.p1.y()),
                  QPoint(self.p2.x() + int(self.width() * self._value / 100), self.p2.y()),
                  self.p3,
                  self.p4]
        painter.drawPolygon(QPolygon(points))


class SThreeProgress(QWidget):
    def __init__(self, parent=None):
        super(SThreeProgress, self).__init__(parent)

        self.setStyleSheet(
            """background-color:rgb(62, 61, 50)""")

        self.sw1 = SWidget(parent=self)
        self.sw2 = SWidget(parent=self)
        self.sw3 = SWidget(parent=self)

        self.resize(self.size())

        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v
        self.sw1.value = v
        self.sw2.value = v
        self.resizeEvent()

    def resizeEvent(self, event=None):
        """
            #####################
           #                  # #
          #        sw1       #  #
         #                  #   #
        #################### sw3#
        #                  #   #
        #          sw2     #  #
        #                  # #
        ####################
        :param event:
        :return:
        """
        self.sw1.resize(self.size())
        sw1_width = self.width()
        sw1_height = self.height() * 0.4
        self.sw1.p1 = QPoint(sw1_height * math.tan(math.pi / 6), 0)
        self.sw1.p2 = QPoint(0, sw1_height)
        self.sw1.p3 = QPoint(sw1_width - sw1_height * math.tan(math.pi / 6), sw1_height)
        self.sw1.p4 = QPoint(sw1_width, 0)

        self.sw2.resize(self.size())
        sw2_width = self.width()
        sw2_height = self.height() * 0.6
        self.sw2.p1 = self.sw1.p2
        self.sw2.p2 = QPoint(0, self.height())
        self.sw2.p3 = QPoint(sw2_width - sw1_height * math.tan(math.pi / 6), self.height())
        self.sw2.p4 = self.sw1.p3

        self.sw3.resize(self.size())
        self.sw3.p1 = self.sw1.p3
        self.sw3.p2 = self.sw2.p3
        self.sw3.p3 = QPoint(self.width(), sw2_height)
        self.sw3.p4 = self.sw1.p4
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(0.5)
        painter.setRenderHint(QPainter.Antialiasing, True)
        pen = QPen(Qt.DashLine)
        pen.setColor(Qt.white)
        brush = QBrush(Qt.green)
        painter.setPen(pen)
        # painter.setBrush(brush)
        painter.save()
        painter.drawPolyline(self.sw1.p1, QPoint(self.height() * 0.4 * math.tan(math.pi / 6), self.height() * 0.6))
        painter.restore()
        painter.drawPolyline(self.sw2.p2, QPoint(self.height() * 0.4 * math.tan(math.pi / 6), self.height() * 0.6))
        painter.save()
        painter.drawPolyline(QPoint(self.height() * 0.4 * math.tan(math.pi / 6), self.height() * 0.6), self.sw3.p3)
        # painter.restore()
        # points = [QPoint(),
        #           self.sw2.p3,
        #           QPoint(self.sw2.p3.x() + self.height() * 0.4 * math.tan(math.pi / 6), self.height() * 0.6),
        #           self.sw1.p4
        #           ]
        # painter.drawPolygon(QPolygon(points))


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    window = SThreeProgress()
    window.show()
    window.resize(600, 200)
    window.value = 95
    app.exec_()

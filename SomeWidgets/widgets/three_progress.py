# -*- coding: utf-8 -*-
# @Time    : 2019/9/11 16:02
# @Author  : llc
# @File    : three_progress.py
import math

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QColor, QPolygon, QBrush, QPen
from PyQt5.QtWidgets import QWidget


class SHWidget(QWidget):
    def __init__(self, color1, color2, parent=None):
        super(SHWidget, self).__init__(parent)
        self.p1 = QPoint(0, 0)
        self.p2 = QPoint(0, 0)
        self.p3 = QPoint(0, 0)
        self.p4 = QPoint(0, 0)
        self.color1 = color1
        self.color2 = color2
        self._value = 0
        self.p = 0
        self.opacity = 0.5

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(self.opacity)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.white)
        painter.save()
        brush = QBrush(self.color1)
        painter.setBrush(brush)
        points = [self.p1,
                  self.p2,
                  QPoint(self.p2.x() + self.p, self.p2.y()),
                  QPoint(self.p1.x() + self.p, self.p1.y())]
        painter.drawPolygon(QPolygon(points))
        painter.restore()
        brush = QBrush(self.color2)
        painter.setBrush(brush)
        points = [
            QPoint(self.p1.x() + self.p, self.p1.y()),
            QPoint(self.p2.x() + self.p, self.p2.y()),
            self.p3,
            self.p4]
        painter.drawPolygon(QPolygon(points))


class SVWidget(QWidget):
    def __init__(self, color, pen_style=Qt.SolidLine, parent=None):
        super(SVWidget, self).__init__(parent)
        self.p1 = QPoint(0, 0)
        self.p2 = QPoint(0, 0)
        self.p3 = QPoint(0, 0)
        self.p4 = QPoint(0, 0)
        self.color = color
        self.pen = QPen(color)
        self.pen.setStyle(pen_style)
        self.opacity = 0.5

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(self.opacity)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(self.pen)
        brush = QBrush(self.color)
        painter.setBrush(brush)
        points = [self.p1, self.p2, self.p3, self.p4]
        painter.drawPolygon(QPolygon(points))


class SThreeProgress(QWidget):
    def __init__(self, color1=QColor(0, 200, 0), color2=QColor(255, 255, 255), opacity=0.5, parent=None):
        super(SThreeProgress, self).__init__(parent)

        self._sw1 = SHWidget(color1, color2, parent=self)
        self._sw2 = SHWidget(color1, color2, parent=self)
        self._sw3 = SVWidget(color=color1, pen_style=Qt.DashLine, parent=self)
        self._sw4 = SVWidget(color=color2, parent=self)

        self._opacity = opacity

        self.resize(self.size())

        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if v < 0:
            v = 0
        elif v > 100:
            v = 100
        self._value = v
        self._sw1.value = v
        self._sw2.value = v
        self.resizeEvent()

    @property
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, o):
        self._opacity = o
        self._sw1.opacity = o
        self._sw2.opacity = o
        self._sw3.opacity = o
        self._sw4.opacity = o
        self.resizeEvent()

    def resizeEvent(self, event=None):
        """
            ##########################################
           #                  # #                  # #
          #        _sw1       #  #         _sw1     #  #
         #                  #   #                #   #
        #################### _sw4################# _sw4#
        #                  #   #                #   #
        #          _sw2     #  #          _sw2    #  #
        #                  # #                  # #
        #########################################
        """
        self.off = self.height() * 0.4 * math.tan(math.pi / 6)
        p = (self.width() - self.off) * self._value / 100
        self._sw1.resize(self.size())
        self._sw1.p1 = QPoint(self.off, 0)
        self._sw1.p2 = QPoint(0, self.height() * 0.4)
        self._sw1.p3 = QPoint(self.width() - self.off, self.height() * 0.4)
        self._sw1.p4 = QPoint(self.width(), 0)
        self._sw1.p = p

        self._sw2.resize(self.size())
        self._sw2.p1 = self._sw1.p2
        self._sw2.p2 = QPoint(0, self.height())
        self._sw2.p3 = QPoint(self.width() - self.off, self.height())
        self._sw2.p4 = self._sw1.p3
        self._sw2.p = p

        self._sw3.resize(self.size())
        self._sw3.p1 = QPoint(p, self.height() * 0.4)
        self._sw3.p2 = QPoint(p, self.height())
        self._sw3.p3 = QPoint(self.off + p, self.height() * 0.6)
        self._sw3.p4 = QPoint(self.off + p, 0)

        self._sw4.resize(self.size())
        self._sw4.p1 = self._sw1.p3
        self._sw4.p2 = self._sw2.p3
        self._sw4.p3 = QPoint(self.width(), self.height() * 0.6)
        self._sw4.p4 = self._sw1.p4

        if p == 100:
            self._sw4.hide()
        else:
            self._sw4.show()

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(self._opacity)
        painter.setRenderHint(QPainter.Antialiasing, True)
        pen = QPen(Qt.DashLine)
        pen.setColor(Qt.white)
        painter.setPen(pen)
        painter.drawPolyline(self._sw1.p1, QPoint(self.off, self.height() * 0.6))
        painter.drawPolyline(self._sw2.p2, QPoint(self.off, self.height() * 0.6))
        painter.drawPolyline(QPoint(self.off, self.height() * 0.6), self._sw4.p3)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    window = SThreeProgress()
    window.setStyleSheet("""background-color:#272822""")
    window.show()
    window.resize(600, 200)
    window.value = 100
    app.exec_()

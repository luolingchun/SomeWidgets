# -*- coding: utf-8 -*-
# @Time    : 2019/9/16 9:36
# @Author  : llc
# @File    : cylinder_progress.py
from PyQt5.QtCore import Qt, QRectF, QPoint
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QColor, QPen
from PyQt5.QtWidgets import QWidget


class SHWidget(QWidget):
    def __init__(self, color1, color2, parent=None):
        super(SHWidget, self).__init__(parent)
        self.p1 = QPoint(0, 0)
        self.p2 = QPoint(0, 0)
        self.p3 = QPoint(0, 0)
        self.p4 = QPoint(0, 0)
        self.p5 = QPoint(0, 0)
        self.p6 = QPoint(0, 0)
        self.p7 = QPoint(0, 0)
        self.p8 = QPoint(0, 0)
        self.p9 = QPoint(0, 0)
        self.color1 = color1
        self.color2 = color2
        self.opacity = 0.5

    def paintEvent(self, event):
        a = self.height() / 2 * 0.4
        painter = QPainter(self)
        painter.setOpacity(self.opacity)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.setPen(Qt.NoPen)
        painter.save()
        brush = QBrush(self.color1)
        painter.setBrush(brush)
        path = QPainterPath()
        path.setFillRule(Qt.OddEvenFill)
        path.moveTo(self.p1)
        rect = QRectF(0, 0, a * 2, self.height())
        path.arcTo(rect, 90, 180)
        path.lineTo(self.p2)
        path.lineTo(self.p3)
        path.lineTo(self.p4)
        path.moveTo(self.p5)
        rect = QRectF(self.p5.x() - a, 0, a * 2, self.height())
        path.arcTo(rect, 90, 180)
        painter.drawPath(path)
        painter.restore()
        if self.p5 == self.p9:
            return
        brush = QBrush(self.color2)
        painter.setBrush(brush)
        path = QPainterPath()
        path.setFillRule(Qt.OddEvenFill)
        path.moveTo(self.p5)
        rect = QRectF(self.p5.x() - a, 0, a * 2, self.height())
        path.arcTo(rect, 90, 180)
        path.lineTo(self.p6)
        path.lineTo(self.p7)
        path.lineTo(self.p8)
        path.moveTo(self.p9)
        rect = QRectF(self.p9.x() - a, 0, a * 2, self.height())
        path.arcTo(rect, 90, 180)
        painter.drawPath(path)
        path = QPainterPath()
        path.setFillRule(Qt.OddEvenFill)
        path.moveTo(self.p1)


class SVWidget(QWidget):
    def __init__(self, color1, color2, parent=None):
        super(SVWidget, self).__init__(parent)
        self.p1 = QPoint(0, 0)
        self.p2 = QPoint(0, 0)
        self.color1 = color1
        self.color2 = color2
        self.opacity = 0.5

    def paintEvent(self, event):
        a = self.height() / 2 * 0.4
        painter = QPainter(self)
        painter.setOpacity(self.opacity)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.setPen(Qt.NoPen)
        painter.save()
        path = QPainterPath()
        brush = QBrush(self.color1)
        painter.setBrush(brush)
        path.moveTo(self.p1)
        rect = QRectF(self.p1.x() - a, 0, a * 2, self.height())
        path.arcTo(rect, 90, 360)
        painter.drawPath(path)
        painter.restore()
        if self.p1 == self.p2:
            return
        path = QPainterPath()
        brush = QBrush(self.color2)
        painter.setBrush(brush)
        path.moveTo(self.p2)
        rect = QRectF(self.p2.x() - a, 0, a * 2, self.height())
        path.arcTo(rect, 90, 360)
        painter.drawPath(path)


class SCylinderProgress(QWidget):
    def __init__(self, color1=QColor(0, 200, 0), color2=QColor(255, 255, 255), opacity=0.5, parent=None):
        super(SCylinderProgress, self).__init__(parent)

        self._sw1 = SHWidget(color1, color2, parent=self)
        self._sw2 = SVWidget(color1, color2, parent=self)

        self._opacity = opacity
        self._value = 0
        self.resize(600, 200)

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
        self.resizeEvent()

    @property
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, o):
        self._opacity = o
        self._sw1.opacity = o
        self._sw2.opacity = o
        self.update()

    def resizeEvent(self, event=None):
        r = self.height() / 2
        a = r * 0.4

        p = (self.width() - a * 2) * self._value / 100

        self._sw1.resize(self.size())
        self._sw1.p1 = QPoint(a, r)
        self._sw1.p2 = QPoint(a + p, self.height())
        self._sw1.p3 = QPoint(a + p, 0)
        self._sw1.p4 = QPoint(a, 0)
        self._sw1.p5 = QPoint(a + p, r)
        self._sw1.p6 = QPoint(self.width() - a, self.height())
        self._sw1.p7 = QPoint(self.width() - a, 0)
        self._sw1.p8 = QPoint(a + p, 0)
        self._sw1.p9 = QPoint(self.width() - a, r)

        self._sw2.resize(self.size())
        self._sw2.p1 = QPoint(a + p, r)
        self._sw2.p2 = QPoint(self.width() - a, r)

        self.update()

    def paintEvent(self, event):
        r = self.height() / 2
        a = r * 0.4

        painter = QPainter(self)
        painter.setOpacity(self._opacity)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.save()
        pen = QPen(Qt.white)
        pen.setStyle(Qt.DashLine)
        painter.setPen(pen)
        rect = QRectF(0, 0, a * 2, self.height())
        painter.drawArc(rect, 270 * 16, 180 * 16)
        painter.restore()
        pen = QPen(Qt.white)
        pen.setStyle(Qt.SolidLine)
        painter.setPen(pen)
        rect = QRectF(self.width() - a * 2, 0, a * 2, self.height())
        painter.drawArc(rect, 90 * 16, 180 * 16)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    window = SCylinderProgress()
    window.setStyleSheet("""background-color:#515151""")
    window.show()
    app.exec_()

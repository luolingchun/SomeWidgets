# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/4/6 13:10

from PyQt5.QtCore import QSize, Qt, pyqtSignal, QRect, QPointF
from PyQt5.QtGui import QLinearGradient, QColor, QImage, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QGridLayout, QComboBox


class PanelWidget(QWidget):
    def __init__(self, parent=None):
        super(PanelWidget, self).__init__(parent)

        self._h = self._s = self._v = 0

    @property
    def h(self):
        return self._h

    @h.setter
    def h(self, h):
        self._h = h
        self.update()

    @property
    def s(self):
        return self._s

    @s.setter
    def s(self, s):
        self._s = s
        self.update()

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, v):
        self._v = v
        self.update()

    def mousePressEvent(self, event):
        super(PanelWidget, self).mousePressEvent(event)
        pos = event.pos()
        self._s = pos.x() / self.width() * 255
        self._v = 255 - pos.y() / self.height() * 255
        self._s = max(0, self._s)
        self._s = min(255, self._s)
        self._v = max(0, self._v)
        self._v = min(255, self._v)
        self.update()

    def mouseMoveEvent(self, event):
        super(PanelWidget, self).mouseMoveEvent(event)
        pos = event.pos()
        self._s = pos.x() / self.width() * 255
        self._v = 255 - pos.y() / self.height() * 255
        self._s = max(0, self._s)
        self._s = min(255, self._s)
        self._v = max(0, self._v)
        self._v = min(255, self._v)
        self.update()

    def paintEvent(self, event):
        super(PanelWidget, self).paintEvent(event)
        self.image = QImage(self.size(), QImage.Format_ARGB32)
        # 新建painter
        painter = QPainter()
        # 饱和度、色调渐变
        sv_gradient = QLinearGradient(0, 0, self.width(), 0)
        sv_color = QColor()
        sv_color.setHsv(self._h, 255, 255)
        sv_gradient.setColorAt(0, Qt.white)
        sv_gradient.setColorAt(1, sv_color)
        # 黑色渐变
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(0, 0, 0, 0))
        gradient.setColorAt(1, QColor(0, 0, 0, 255))
        # 绘制饱和度、色调渐变到image
        painter.begin(self.image)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.fillRect(self.rect(), sv_gradient)
        painter.end()
        # 绘制黑色渐变到image
        painter.begin(self.image)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.fillRect(self.rect(), gradient)
        painter.end()
        # 绘制image
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.drawImage(self.rect(), self.image)
        painter.end()
        # 绘制小圆圈
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.setPen(QPen(Qt.white))
        pos = QPointF(self._s * self.width() / 255, (255 - self._v) * self.height() / 255)
        painter.drawEllipse(pos, 6, 6)
        painter.setPen(QPen(Qt.darkGreen))
        painter.drawEllipse(pos, 7, 7)
        painter.end()


class HueWidget(QWidget):
    hueChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(HueWidget, self).__init__(parent)

        self._y = 0
        self._h = 0

    @property
    def h(self):
        return self._h

    @h.setter
    def h(self, h):
        self._h = h
        self._y = self.height() * h / 360
        self._y = max(0, self._y)
        self._y = min(self.height() - 4, self._y)
        self.update()

    def mousePressEvent(self, event):
        super(HueWidget, self).mousePressEvent(event)
        pos = event.pos()
        self._y = pos.y()
        self._y = max(0, self._y)
        self._y = min(self.height() - 4, self._y)
        self._h = self._y / self.height()
        self.update()
        self.hueChanged.emit(self._h * 360)

    def mouseMoveEvent(self, event):
        super(HueWidget, self).mouseMoveEvent(event)
        pos = event.pos()
        self._y = pos.y()
        self._y = max(0, self._y)
        self._y = min(self.height(), self._y)
        self._h = self._y / self.height()
        self._y = min(self.height() - 4, self._y)
        self.update()
        self.hueChanged.emit(self._h * 360)

    def paintEvent(self, event):
        super(HueWidget, self).paintEvent(event)
        self.image = QImage(QSize(self.width() - 4, self.height()), QImage.Format_ARGB32)
        # 新建painter
        painter = QPainter()
        # 色调渐变
        h_gradient = QLinearGradient(0, 0, 0, self.height())
        i = 0.0
        while i < 1.0:
            h_gradient.setColorAt(i, QColor.fromHsvF(i, 1.0, 1.0))
            i += 1.0 / 16
        h_gradient.setColorAt(1, QColor.fromHsvF(0, 1, 1))
        # 绘制色调渐变到image
        painter.begin(self.image)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.fillRect(self.rect(), h_gradient)
        painter.end()
        # 绘制image
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.drawImage(QRect(2, 0, self.width() - 4, self.height()), self.image)
        painter.end()
        # 绘制滑块
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.setPen(QPen(Qt.white, 1))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(0, self._y, self.width(), 4)
        painter.end()


class SColorPanel(QWidget):
    def __init__(self, parent=None):
        super(SColorPanel, self).__init__(parent)
        self.setupUi()
        self.resize(300, 200)
        # self.setWindowFlags(Qt.Popup)

        self.setObjectName("CP")
        self.setStyleSheet("""#CP{
        background-color:rgb(43, 43, 43);
        
        }""")

        self.hueWidget.hueChanged.connect(self.hueWidgetHueChanged)

        color = QColor(95, 50, 50)

        self.hueWidget.h = color.hue() if color.hue() != -1 else 0
        self.panelWidget.h = color.hue() if color.hue() != -1 else 0
        self.panelWidget.s = color.saturation()
        self.panelWidget.v = color.value()

    def setupUi(self):
        self.gridLayout = QGridLayout(self)
        self.comboBox = QComboBox(self)
        self.gridLayout.addWidget(self.comboBox, 0, 0, 1, 3)
        self.panelWidget = PanelWidget(parent=self)
        self.panelWidget.setMinimumSize(QSize(16777215, 150))
        self.gridLayout.addWidget(self.panelWidget, 1, 0, 1, 1)
        self.widget_2 = QWidget(self)
        self.widget_2.setMinimumSize(QSize(30, 0))
        self.widget_2.setMaximumSize(QSize(30, 16777215))
        self.gridLayout.addWidget(self.widget_2, 1, 1, 1, 1)
        self.hueWidget = HueWidget(self)
        self.hueWidget.setMinimumSize(QSize(30, 0))
        self.hueWidget.setMaximumSize(QSize(30, 16777215))
        self.gridLayout.addWidget(self.hueWidget, 1, 2, 1, 1)

    def hueWidgetHueChanged(self, h):
        self.panelWidget.h = h


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    window = SColorPanel()
    window.show()
    app.exec_()

# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/4/6 13:10

from PyQt5.QtCore import QSize, Qt, pyqtSignal, QRect, QPointF, QPoint
from PyQt5.QtGui import QLinearGradient, QColor, QImage, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QGridLayout, QComboBox, QListView


class PanelWidget(QWidget):
    colorChanged = pyqtSignal(QColor)

    def __init__(self, parent=None):
        super(PanelWidget, self).__init__(parent)

        self._h = self._s = self._v = None
        self._color = None

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self._h = color.hue() if color.hue() != -1 else 0
        self._s = color.saturation()
        self._v = color.value()
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
        if not self._color:
            return
        self.image = QImage(self.size(), QImage.Format_ARGB32)
        # 新建painter
        painter = QPainter()
        # 饱和度、色调渐变
        sv_gradient = QLinearGradient(1, 1, self.width() - 1, 1)
        sv_color = QColor(255, 255, 255)
        sv_color.setHsv(self._h, 255, 255)
        sv_gradient.setColorAt(0, Qt.white)
        sv_gradient.setColorAt(1, sv_color)
        # 黑色渐变
        gradient = QLinearGradient(1, 1, 1, self.height() - 1)
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
        # 发送颜色值
        x = pos.x()
        y = pos.y()
        x = max(x, 0)
        x = min(x, self.width() - 1)
        y = max(y, 0)
        y = min(y, self.height() - 1)

        self.colorChanged.emit(self.image.pixelColor(QPoint(x, y)))


class HueWidget(QWidget):
    hueChanged = pyqtSignal(QColor)

    def __init__(self, parent=None):
        super(HueWidget, self).__init__(parent)

        self._y = self._h = 0
        self._color = None

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self._h = color.hue() if color.hue() != -1 else 0
        self._y = self.height() * self._h / 360
        self._y = max(0, self._y)
        self._y = min(self.height() - 4, self._y)
        self.update()

    def resizeEvent(self, event):
        super(HueWidget, self).resizeEvent(event)
        self._y = self.height() * self._h / 360
        self._y = max(0, self._y)
        self._y = min(self.height() - 4, self._y)
        self.update()

    def mousePressEvent(self, event):
        super(HueWidget, self).mousePressEvent(event)
        pos = event.pos()
        self._y = pos.y()
        self._y = max(0, self._y)
        self._y = min(self.height() - 4, self._y)
        self._h = self._y / self.height() * 360
        self.update()

    def mouseMoveEvent(self, event):
        super(HueWidget, self).mouseMoveEvent(event)
        pos = event.pos()
        self._y = pos.y()
        self._y = max(0, self._y)
        self._y = min(self.height(), self._y)
        self._h = self._y / self.height() * 360
        self._y = min(self.height() - 4, self._y)
        self.update()

    def paintEvent(self, event):
        super(HueWidget, self).paintEvent(event)
        if not self._color:
            return
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

        color = QColor()
        color.setHsv(self._h, self._color.hsvSaturation(), self._color.value())
        self.hueChanged.emit(color)


class AlphaWidget(QWidget):
    alphaChanged = pyqtSignal(QColor)

    def __init__(self, parent=None):
        super(AlphaWidget, self).__init__(parent)

        self._color = None
        self._y = 0
        self._alpha = 0

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self._alpha = color.alpha()
        self._y = (255 - self._alpha) / 255 * self.height()
        self._y = max(0, self._y)
        self._y = min(self.height() - 4, self._y)
        self.update()

    def resizeEvent(self, event):
        super(AlphaWidget, self).resizeEvent(event)
        if not self._color:
            return
        self._y = (255 - self._alpha) / 255 * self.height()
        self._y = max(0, self._y)
        self._y = min(self.height() - 4, self._y)
        self.update()

    def mousePressEvent(self, event):
        super(AlphaWidget, self).mousePressEvent(event)
        pos = event.pos()
        self._y = pos.y()
        self._y = max(0, self._y)
        self._alpha = int(255 - self._y / self.height() * 255)
        self._y = min(self.height() - 4, self._y)
        self.update()

    def mouseMoveEvent(self, event):
        super(AlphaWidget, self).mouseMoveEvent(event)
        pos = event.pos()
        self._y = pos.y()
        self._y = max(0, self._y)
        self._y = min(self.height(), self._y)
        self._alpha = int(255 - self._y / self.height() * 255)
        self._y = min(self.height() - 4, self._y)
        self.update()

    def paintEvent(self, event):
        super(AlphaWidget, self).paintEvent(event)
        if not self._color:
            return
        # 新建painter
        painter = QPainter()
        pixSize = 5
        # 生成黑边相间的模拟透明背景
        self.grid_image = QImage(self.width() - 4, self.height(), QImage.Format_ARGB32)
        painter.begin(self.grid_image)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        for x in range(int(self.width() / pixSize)):
            for y in range(int(self.height() / pixSize)):
                _x, _y = x * pixSize, y * pixSize
                painter.fillRect(_x, _y, pixSize, pixSize, Qt.white if x % 2 != y % 2 else Qt.darkGray)
        painter.end()
        # 透明渐变
        gradient = QLinearGradient(0, 0, 0, self.height())
        self._color.setAlpha(255)
        gradient.setColorAt(0, self._color)
        gradient.setColorAt(1, QColor(0, 0, 0, 150))
        # 绘制image、grid
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.drawImage(QRect(2, 0, self.width() - 4, self.height()), self.grid_image)
        painter.fillRect(QRect(2, 0, self.width() - 4, self.height()), gradient)
        painter.end()
        # 绘制滑块
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.setPen(QPen(Qt.white, 1))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(0, self._y, self.width(), 4)
        painter.end()

        self._color.setAlpha(self._alpha)
        self.alphaChanged.emit(self._color)


class SColorPanel(QWidget):
    colorValue = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SColorPanel, self).__init__(parent)
        self.setupUi()
        self.resize(300, 200)
        # self.setWindowFlags(Qt.Popup)

        self.setObjectName("CP")
        self.setStyleSheet("""
            #CP{
                background-color:rgb(43, 43, 43);
                }
            
            #colorType {
                border: 0px;
                min-height:25px;
                font: bold normal 14px "consolas";
                color: white;
            }
             
            #colorType::drop-down{
                border-style:none;
            }
             
            #colorType QAbstractItemView {
                outline: 0;
                color: white;
                border: 0px;
                min-height:25px;
                font: bold normal 14px "consolas";
            }
        """)

        self.hueWidget.hueChanged.connect(self.hueWidgetHueChanged)
        self.panelWidget.colorChanged.connect(self.panelWidgetColorChanged)
        self.alphaWidget.alphaChanged.connect(self.alphaWidgetAlphaChanged)

        color = QColor(73, 156, 84, 100)
        self.hueWidget.color = color
        self.panelWidget.color = color
        self.alphaWidget.color = color
        # self.panelWidgetColorChanged(color)

    def setupUi(self):
        self.gridLayout = QGridLayout(self)
        self.comboBox = QComboBox(self)
        self.comboBox.setView(QListView())
        self.comboBox.setObjectName("colorType")
        self.gridLayout.addWidget(self.comboBox, 0, 0, 1, 3)
        self.panelWidget = PanelWidget(parent=self)
        self.panelWidget.setMinimumSize(QSize(16777215, 150))
        self.gridLayout.addWidget(self.panelWidget, 1, 0, 1, 1)
        self.alphaWidget = AlphaWidget(self)
        self.alphaWidget.setMinimumSize(QSize(30, 0))
        self.alphaWidget.setMaximumSize(QSize(30, 16777215))
        self.gridLayout.addWidget(self.alphaWidget, 1, 1, 1, 1)
        self.hueWidget = HueWidget(self)
        self.hueWidget.setMinimumSize(QSize(30, 0))
        self.hueWidget.setMaximumSize(QSize(30, 16777215))
        self.gridLayout.addWidget(self.hueWidget, 1, 2, 1, 1)

    def hueWidgetHueChanged(self, color):
        self.panelWidget.color = color

    def panelWidgetColorChanged(self, color):
        self.alphaWidget.color = color

    def alphaWidgetAlphaChanged(self, color):
        self.updateComboBox(color)

    def updateComboBox(self, color):
        # 透明度
        alpha = color.alpha()
        # rgb
        red = color.red()
        green = color.green()
        blue = color.blue()
        # 16进制
        name = color.name()
        # hsv，hsl
        hue = self.hueWidget.color.hue()  # 固定不变
        hsvSaturation = color.hsvSaturation()
        hslSaturation = color.hslSaturation()
        value = color.value()
        lightness = color.lightness()

        if value > 128:
            self.comboBox.setStyleSheet(f"""
                        color:dark;
                        background-color:rgba({red}, {green}, {blue}, {alpha});
                    """)
        else:
            self.comboBox.setStyleSheet(f"""
                        color:white;
                        background-color:rgba({red}, {green}, {blue}, {alpha});
                    """)
        if alpha == 255:
            items = [
                f"rgb({red}, {green}, {blue})",
                f"{name}",
                f"hsv({hue}, {hsvSaturation}, {value})",
                f"hsl({hue}, {hslSaturation}, {lightness})"
            ]
        else:
            items = [
                f"rgba({red}, {green}, {blue}, {alpha})",
                f"{name}",
                f"hsv({hue}, {hsvSaturation}, {value}, {alpha})",
                f"hsl({hue}, {hslSaturation}, {lightness}, {alpha})"
            ]
        if self.comboBox.currentText():
            self.comboBox.setItemText(0, items[0])
            self.comboBox.setItemText(1, items[1])
            self.comboBox.setItemText(2, items[2])
            self.comboBox.setItemText(3, items[3])
        else:
            self.comboBox.addItems(items)
        self.colorValue.emit(self.comboBox.currentText())


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    sColorPanel = SColorPanel()
    sColorPanel.show()
    sColorPanel.colorValue.connect(lambda v: print(v))
    # from pyqss import Qss
    #
    # qss = Qss(sColorPanel)
    # qss.show()

    app.exec_()

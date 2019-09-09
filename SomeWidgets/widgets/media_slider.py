# -*- coding: utf-8 -*-
# @Time    : 2019/9/9 8:52
# @Author  : llc
# @File    : media_slider.py
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSlider


class SMediaSlider(QWidget):
    valueChanged = pyqtSignal(int)

    def __init__(self, max_value=100, parent=None):
        super(SMediaSlider, self).__init__(parent)

        self.setObjectName('SMediaSlider')

        self._setup_ui()

        self._slider.setMaximum(max_value)
        self._slider.setPageStep(1)
        self._slider.valueChanged.connect(self.valueChanged.emit)

        self.setStyleSheet("""
        SMediaSlider > QSlider:horizontal {
            min-height:16px;
            height:16;
        }
        SMediaSlider > QSlider::groove:horizontal {
            background:rgba(255,255,255,0);
            height: 8px;
            border-radius:4px;
        }
        SMediaSlider > QSlider::handle:horizontal {
            background-color: #fff;
            width: 16px;
            border-radius: 8px;
            margin:-4px;
            left:4px;
            right:4px;
        }
        
        SMediaSlider > QSlider::sub-page:horizontal {
            border-radius:4px;
            background-color: qlineargradient(spread:pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(0, 200, 0, 255));
        }
        
        SMediaSlider > QSlider::add-page:horizontal {
            border-radius:4px;
            background-color: rgba(255,255,255,150);
        }
        
        SMediaSlider > QLabel{
            color:#fff;
            font-size:14px;
            font-family:"consolas";
        }
        """)

    def _setup_ui(self):
        self._hl = QHBoxLayout(self)
        self._hl.setContentsMargins(9, 0, 9, 0)
        self._left_label = QLabel(self)
        self._right_label = QLabel(self)
        self._slider = Slider(self)
        self._slider.setOrientation(Qt.Horizontal)

        self._hl.addWidget(self._left_label)
        self._hl.addWidget(self._slider)
        self._hl.addWidget(self._right_label)

    @property
    def left(self):
        return self._left_label.text()

    @left.setter
    def left(self, text):
        self._left_label.setText(text)

    @property
    def right(self):
        return self._right_label.text()

    @right.setter
    def right(self, text):
        self._right_label.setText(text)


class Slider(QSlider):
    def __init__(self, parent=None):
        super(Slider, self).__init__(parent)

    def mousePressEvent(self, e):
        super(Slider, self).mousePressEvent(e)
        x = e.pos().x()
        if self.isSliderDown():
            return
        per = x * 1.0 / self.width()
        value = per * (self.maximum() - self.minimum()) + self.minimum()
        self.setValue(value)

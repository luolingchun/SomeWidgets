# -*- coding: utf-8 -*-
# @Time    : 2019/10/16 8:43
# @Author  : llc
# @File    : round_loading.py
from random import randint

from PyQt5.QtCore import pyqtProperty, QPropertyAnimation, QRectF, QSequentialAnimationGroup, QParallelAnimationGroup, \
    QPoint, QAbstractAnimation, QEasingCurve
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtWidgets import QWidget, QStyleOption, QStyle


class BallWidget(QWidget):
    def __init__(self, radius=5, color=(0, 200, 200), parent=None):
        super(BallWidget, self).__init__(parent)

        self.radius = radius
        self.color = color

        self.resize(radius * 2, radius * 2)

    def _set_style(self, value):
        _style = f"background-color:rgba({self.color[0]}, {self.color[1]}, {self.color[2]},{value});" \
            f"border-radius:{self.radius}px;"
        self.setStyleSheet(_style)

    _style = pyqtProperty(int, fset=_set_style)

    def paintEvent(self, event):
        """解决继承的QWidget qss无效"""
        super(BallWidget, self).paintEvent(event)
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)


class RoundAnimation(QPropertyAnimation):

    def __init__(self, target, prop, parent=None):
        super(RoundAnimation, self).__init__(target, prop, parent)

    def updateCurrentTime(self, currentTime):
        self.path = QPainterPath()
        if self.path.isEmpty():
            end = self.endValue()
            start = self.startValue()
            self.path.addEllipse(QRectF(start, end))

        duration = self.duration()

        if duration == 0:
            progress = 1.0
        else:
            progress = (((currentTime - 1) % duration) + 1) / float(duration)

        easedProgress = self.easingCurve().valueForProgress(progress)

        if easedProgress > 1.0:
            easedProgress -= 1.0
        elif easedProgress < 0:
            easedProgress += 1.0

        pt = self.path.pointAtPercent(easedProgress)
        self.updateCurrentValue(pt)


class SRoundLoading(QWidget):
    def __init__(self, ball_radius=4, ball_color=(100, 200, 100), ball_colour=False, duration=2000, duration_pause=200,
                 ec=QEasingCurve.Linear, parent=None):
        super(SRoundLoading, self).__init__(parent)

        self._balls = []
        self._seq_animations = []
        self._ball_numbers = 6
        self.ball_radius = ball_radius
        self.duration = duration
        self.duration_pause = duration_pause

        self.ec = ec

        for i in range(self._ball_numbers):
            if ball_colour:
                ball_color = (randint(0, 255), randint(0, 255), randint(0, 255))
            self._balls.append(BallWidget(radius=ball_radius, color=ball_color, parent=self))

    def start(self):
        height = self.height()
        width = self.width()
        for i in range(self._ball_numbers):
            self._seq_animations.append(QSequentialAnimationGroup(self))
            # 增加间隔
            self._seq_animations[i].addPause(self.duration_pause * i)
            # 第一段
            par_animation1 = QParallelAnimationGroup(self)
            ra = RoundAnimation(self._balls[i], b'pos', self)
            ra.setEasingCurve(self.ec)
            ra.setDuration(self.duration)
            ra.setStartValue(QPoint(2 * self.ball_radius, 2 * self.ball_radius))
            ra.setEndValue(QPoint(width - 2 * self.ball_radius, height - 2 * self.ball_radius))
            par_animation1.addAnimation(ra)
            pa = QPropertyAnimation(self._balls[i], b'_style', self)
            pa.setEasingCurve(self.ec)
            pa.setDuration(self.duration)
            pa.setStartValue(0)
            pa.setKeyValueAt(0.5, 255)
            pa.setEndValue(0)
            par_animation1.addAnimation(pa)
            self._seq_animations[i].addAnimation(par_animation1)
            # 增加间隔
            self._seq_animations[i].addPause(self.duration_pause * (self._ball_numbers - i - 1))

        for seq in self._seq_animations:
            seq.setLoopCount(-1)
            seq.start(QAbstractAnimation.DeleteWhenStopped)

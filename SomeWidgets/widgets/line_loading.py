# -*- coding: utf-8 -*-
# @Time    : 2019/10/14 10:44
# @Author  : llc
# @File    : line_loading.py
from random import randint

from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QPoint, pyqtProperty, QAbstractAnimation, \
    QSequentialAnimationGroup, QParallelAnimationGroup
from PyQt5.QtGui import QPainter
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


class SLineLoading(QWidget):
    def __init__(self, ball_radius=5, ball_color=(100, 200, 100), ball_colour=False, duration=2000, duration_pause=200,
                 parent=None):
        super(SLineLoading, self).__init__(parent)

        self._ball_radius = ball_radius
        self._ball_numbers = 5
        self.duration = duration
        self._ec = QEasingCurve.OutSine
        self._first_flag = self._three_flag = 0.2
        self._second_flag = 0.6
        self.duration_pause = duration_pause

        self._balls = []
        self._seq_animations = []

        for i in range(self._ball_numbers):
            if ball_colour:
                ball_color = (randint(0, 255), randint(0, 255), randint(0, 255))
            self._balls.append(BallWidget(radius=ball_radius, color=ball_color, parent=self))

    def start(self):
        bh = self.height() / 2 - self._ball_radius
        width = self.width()
        for i in range(self._ball_numbers):
            self._seq_animations.append(QSequentialAnimationGroup(self))
            # 增加间隔
            self._seq_animations[i].addPause(self.duration_pause * i)
            # 第一段
            par_animation1 = QParallelAnimationGroup(self)
            pa = QPropertyAnimation(self._balls[i], b'pos', self)
            pa.setEasingCurve(self._ec)
            pa.setDuration(self.duration * self._first_flag)
            pa.setStartValue(QPoint(0, bh))
            pa.setEndValue(QPoint(width * 0.4, bh))
            par_animation1.addAnimation(pa)
            pa = QPropertyAnimation(self._balls[i], b'_style', self)
            pa.setEasingCurve(self._ec)
            pa.setDuration(self.duration * self._first_flag)
            pa.setStartValue(0)
            pa.setEndValue(255)
            par_animation1.addAnimation(pa)
            self._seq_animations[i].addAnimation(par_animation1)
            # 第二段
            pa = QPropertyAnimation(self._balls[i], b'pos', self)
            pa.setDuration(self.duration * self._second_flag)
            pa.setStartValue(QPoint(width * 0.4, bh))
            pa.setEndValue(QPoint(width * 0.6, bh))
            self._seq_animations[i].addAnimation(pa)
            # 第三段
            par_animation2 = QParallelAnimationGroup(self)
            pa = QPropertyAnimation(self._balls[i], b'pos', self)
            pa.setEasingCurve(self._ec)
            pa.setDuration(self.duration * self._three_flag)
            pa.setStartValue(QPoint(width * 0.6, bh))
            pa.setEndValue(QPoint(width, bh))
            par_animation2.addAnimation(pa)
            pa = QPropertyAnimation(self._balls[i], b'_style', self)
            pa.setEasingCurve(self._ec)
            pa.setDuration(self.duration * self._three_flag)
            pa.setStartValue(255)
            pa.setEndValue(0)
            par_animation2.addAnimation(pa)
            self._seq_animations[i].addAnimation(par_animation2)
            # 增加间隔
            self._seq_animations[i].addPause(self.duration_pause * (self._ball_numbers - i - 1))

        for seq in self._seq_animations:
            seq.setLoopCount(-1)
            seq.start(QAbstractAnimation.DeleteWhenStopped)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    window = SLineLoading(ball_radius=10)
    window.resize(300, 100)
    window.show()

    # from pyqss import Qss
    #
    # qss = Qss(window)
    # qss.show()

    app.exec_()

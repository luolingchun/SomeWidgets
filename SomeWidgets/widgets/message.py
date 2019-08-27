# -*- coding: utf-8 -*-
# @Time    : 2019/8/27 9:03
# @Author  : llc
# @File    : message.py
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, QPoint
from PyQt5.QtWidgets import QLabel, QGraphicsDropShadowEffect


class SMessageBox(QLabel):
    def __init__(self, parent=None, ttl=3):
        super(SMessageBox, self).__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.ttl = ttl
        self._margin = 5

        # QSS
        self._qss = """
                    #Info{
                    	border:0px;
                    	border-radius:5px;
                    	min-width:60px;
                    	min-height:40px;
                    	background-color:rgba(0,200,0,70%)
                    }
                    
                    #Warn{
                    	border:0px;
                    	border-radius:5px;
                    	min-width:60px;
                    	min-height:40px;
                    	background-color:rgba(220,220,0,70%)
                    }
                    
                    #Err{
                    	border:0px;
                    	border-radius:5px;
                    	min-width:60px;
                    	min-height:40px;
                    	background-color:rgba(200,0,0,70%)
                    }
                    """
        self.setStyleSheet(self._qss)

    def push_message(self, text, type='Info'):
        self.setText(f'  {text}  ')
        self.setObjectName(type)
        self.setScaledContents(True)

        ds_effect = QGraphicsDropShadowEffect()
        ds_effect.setOffset(5, 5)
        ds_effect.setColor(Qt.gray)
        ds_effect.setBlurRadius(10)
        self.setGraphicsEffect(ds_effect)

        self.show()

        animation = QPropertyAnimation(self.parent())
        animation.setTargetObject(self)
        animation.setPropertyName(b'pos')
        animation.setDuration(500)
        if self.parent():
            if not hasattr(self.parent(), 'off_y'):
                setattr(self.parent(), 'off_y', 0)
            if not hasattr(self.parent(), 'number'):
                setattr(self.parent(), 'number', 0)

            off_y = self.parent().off_y
            p_width = self.parent().width()
            start = QPoint(p_width, self._margin + off_y)
            end = QPoint(p_width - self.width() - self._margin, self._margin + off_y)
            timer = QTimer(self)
            timer.timeout.connect(lambda: self._close(timer, animation, end, start))
            timer.start(self.ttl * 1000)
            self._show(animation, start, end)
        self.parent().off_y = self.parent().off_y + self.height() + self._margin
        self.parent().number += 1

    def _show(self, animation, start, end):
        animation.setStartValue(start)
        animation.setEndValue(end)
        animation.start()

    def _close(self, timer, animation, start, end):
        animation.setStartValue(start)
        animation.setEndValue(end)
        animation.finished.connect(self.close)
        animation.start()
        timer.stop()
        self.parent().number -= 1
        if self.parent().number == 0:
            self.parent().off_y = 0


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    window = SMessageBox()
    window.push_message('这是一条正常消息', type='Info')
    # window.push_message('这是一条警告消息', type='Warn')
    # window.push_message('这是一条错误消息', type='Err')
    window.show()

    from pyqss import Qss

    qss = Qss(window)
    qss.show()

    app.exec_()

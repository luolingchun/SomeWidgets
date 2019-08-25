# -*- coding: utf-8 -*-
# @Author  : llc
# @Email   : luolingchun.com@gmail.com
# @Time    : 2019/8/25 15:28
# @File    : progress_dialog.py
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QProgressBar, QPushButton, QWidget, QHBoxLayout


class SProgressDialog(QDialog):
    def __init__(self, parent=None, label_text=''):
        super(SProgressDialog, self).__init__(parent)

        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._setup_ui(label_text)
        self.setObjectName('SProgressDialog')
        self.resize(400, 100)

        # QSS
        self._qss = """
            #SProgressDialog > QWidget{
                border:0px solid green;
                border-radius:10px;
                background-color:rgba(0, 200, 0, 150);
            }
            
            #SProgressDialog > QWidget > QLabel{
                border:0px;
                font-size:14px;
            }
            
            #SProgressDialog > QWidget > QPushButton{
                border:0px;
                min-width:40px;
                min-height:20px;
                font-size:12px;
            }
            
            #SProgressDialog > QWidget > QPushButton:hover{
                border-radius:10px;
                font-size:12px;
                background-color:rgba(200, 100, 0,150);
            }
            
            #SProgressDialog > QWidget > QProgressBar{
                border:0px;
                border-radius:5px;
                text-align:center;
                background-color:rgba(255,255,255,150);
            }
            
            #SProgressDialog > QWidget > QProgressBar::chunk {
                border-radius:5px;
                background-color:rgba(0, 100, 200,150);
            }
        """
        self.setStyleSheet(self._qss)

    def _setup_ui(self, label_text):
        self._widget = QWidget(self)
        hl = QHBoxLayout(self)
        hl.addWidget(self._widget)
        self._label = QLabel(label_text, self._widget)
        self._progress_bar = QProgressBar(self._widget)
        self._pushbutton = QPushButton('取消', self._widget)
        gl = QGridLayout(self._widget)
        gl.addWidget(self._label, 0, 0, 1, 2)
        gl.addWidget(self._progress_bar, 1, 0, 1, 1)
        gl.addWidget(self._pushbutton, 1, 1, 1, 1)

    @property
    def cancel_button(self):
        return self._pushbutton

    @property
    def label_text(self):
        return self._label.text()

    @property
    def value(self):
        return self._progress_bar.value()

    @value.setter
    def value(self, value):
        self._progress_bar.setValue(value)

    @property
    def qss(self):
        return self._qss

    def hide_cancel_button(self):
        self._pushbutton.hide()


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    window = SProgressDialog(label_text='正在处理...')
    window.show()

    from pyqss import Qss

    qss = Qss(window)
    qss.show()
    app.exec_()

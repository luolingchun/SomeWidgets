# -*- coding: utf-8 -*-
# @Time    : 2019/8/27 9:50
# @Author  : llc
# @File    : test_message.py
from PyQt5.QtWidgets import QWidget, QPushButton

from SomeWidgets import SMessageBox


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.resize(500, 500)
        pushbutton1 = QPushButton('info', self)
        pushbutton2 = QPushButton('warn', self)
        pushbutton2.move(0, 50)
        pushbutton3 = QPushButton('error', self)
        pushbutton3.move(0, 100)

        pushbutton1.clicked.connect(lambda: self.show_message('这是一条正常消息', type='Info'))
        pushbutton2.clicked.connect(lambda: self.show_message('这是一条警告消息', type='Warn'))
        pushbutton3.clicked.connect(lambda: self.show_message('这是一条错误消息', type='Err'))

        # pushbutton = QPushButton('test', self)
        # pushbutton.move(470, 5)

    def show_message(self, text, type):
        print(text, type)
        smb = SMessageBox(self)
        smb.push_message(text, type)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()

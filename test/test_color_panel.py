# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/4/12 11:02
from PyQt5.QtCore import Qt

from SomeWidgets import SColorPanel
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton


class Window(QDialog):
    def __init__(self):
        super(Window, self).__init__()

        button = QPushButton(self)
        button.resize(150, 30)
        button.move(10, 10)
        cp = SColorPanel(parent=self)
        button.setMenu(cp)

        self.resize(500, 300)

        def show_cp():
            button.showMenu()

        def update_button(color):
            button.setText(color)
            button.setStyleSheet(f"""
            background-color:{color}
            """)

        button.clicked.connect(show_cp)

        cp.colorValueChanged.connect(update_button)


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()

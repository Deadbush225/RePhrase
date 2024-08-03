from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import sys

from lib.TextEdit import PasteFromAuthorDialog


class Sub(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        btn = QPushButton("TU")
        btn.clicked.connect(self.dia)

        lyt = QHBoxLayout()
        lyt.addWidget(btn)
        self.setLayout(lyt)

    def dia(self):
        d = PasteFromAuthorDialog(parent=self)
        d.exec_()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        s = Sub(parent=self)
        self.setCentralWidget(s)


app = QApplication(sys.argv)

w = MainWindow()
w.show()

app.exec_()

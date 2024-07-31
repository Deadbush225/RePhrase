from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QPushButton, QHBoxLayout, QDialog, QMainWindow

import sys


class Dialog(QDialog):
    c = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        mainLayout = QHBoxLayout()

        self.button = QPushButton("Send Signal")
        self.button.clicked.connect(lambda: self.fin())

        mainLayout.addWidget(self.button)
        self.setLayout(mainLayout)

    def fin(self):
        self.done(QDialog.Accepted)
        self.c.emit(1)


class Window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        button = QPushButton("Open Dialog")
        button.clicked.connect(self.openDialog)

        self.setCentralWidget(button)

    def openDialog(self):
        dialog = Dialog()

        dialog.c.connect(self.prints)
        dialog.exec_()

    def prints(self, *args, **kwargs):
        print(args)
        print(kwargs)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    app.exec_()

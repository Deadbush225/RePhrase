from PyQt5.QtGui import QPallete


class DarkPallete(QPallete):
    def __init__(self):
        self.setColor(QPalette.Window, QColor(53, 53, 53))
        self.setColor(QPalette.WindowText, Qt.white)
        self.setColor(QPalette.Base, QColor(35, 35, 35))
        self.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        self.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
        self.setColor(QPalette.ToolTipText, Qt.white)
        self.setColor(QPalette.Text, Qt.white)
        self.setColor(QPalette.Button, QColor(53, 53, 53))
        self.setColor(QPalette.ButtonText, Qt.white)
        self.setColor(QPalette.BrightText, Qt.red)
        self.setColor(QPalette.Link, QColor(42, 130, 218))
        self.setColor(QPalette.Highlight, QColor(42, 130, 218))
        self.setColor(QPalette.HighlightedText, QColor(35, 35, 35))
        self.setColor(QPalette.Active, QPalette.Button, QColor(53, 53, 53))
        self.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
        self.setColor(QPalette.Disabled, QPalette.WindowText, Qt.darkGray)
        self.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
        self.setColor(QPalette.Disabled, QPalette.Light, QColor(53, 53, 53))

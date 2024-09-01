from rephraser.lib.DarkPallete import DarkPalette
from rephraser.RePhraser import MainWindow
from PyQt5.QtWidgets import QApplication, QStyleFactory

# from PyQt5.QtGui import *

import sys
import os

from rephraser import basedir

if __name__ == "__main__":

    # try:
    app = QApplication(sys.argv)

    fusion = QStyleFactory.create("Fusion")
    QApplication.setStyle(fusion)

    # Now use a palette to switch to dark colors:
    dark_palette = DarkPalette()
    QApplication.setPalette(dark_palette)

    # qdarktheme.enable_hi_dpi()
    # qdarktheme.setup_theme(
    #     custom_colors={"primary": "#D0BCFF", "background": "24273a", "statusBar.background": "24273a", "toolbar.background": "24273a", "background>title": "c5c2c5", "foreground": "c5cff5", "border": "#39394a"})
    # qdarktheme.stop_sync()

    app.setStyleSheet("".join(open(os.path.join(basedir, "dark.qss")).readlines()))
    # app.setWindowIcon(QIcon(os.path.join(basedir, "RePhraser.ico")))

    # window = PasteFromAuthorDialog()
    window = MainWindow()
    # window = QMainWindow()
    # lbl = QLabel("Test")
    # window.setCentralWidget(lbl)
    window.show()

    # customTitlebarWindow = CustomTitlebarWindow(window)
    # customTitlebarWindow.setTopTitleBar(icon_filename='dark-notepad.svg')
    # # customTitlebarWindow.setButtonHint(['close'])
    # customTitlebarWindow.setButtons()
    # customTitlebarWindow.show()

    app.exec_()
# except Exception as e:
#     print(traceback.format_exc())

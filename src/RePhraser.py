from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *

import os
import sys
import uuid
import math

import re

# from zipfile import ZipFile

import traceback

from lib.AuthorTable import AuthorTable
from lib.ScrollBar import ScrollBar
from lib.TextEdit import TextEdit
from lib.helper import *
from lib.Toolbar import Toolbar

floor = math.floor

IMAGE_EXTENSIONS = [".jpg", ".png", ".bmp"]
HTML_EXTENSIONS = [".htm", ".html"]

basedir = os.path.dirname(__file__)

import images.images


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon("RePhrase.png"))

        # self.path holds the path of the currently open file.
        # If none, we haven't got a file open yet (or creating new).
        self.path = None

        self.layout = QStackedLayout()

        mandatoryFileOpenContainer = QWidget()

        fileOpen_layout = QVBoxLayout()
        fileOpen_layout.setAlignment(Qt.AlignCenter)

        fileOpen_label = QLabel("Hey, Open a Project Folder first")
        fileOpen_btn = QPushButton("Open Dir")
        fileOpen_btn.clicked.connect(self.open_directory)

        fileOpen_layout.addWidget(fileOpen_label)
        fileOpen_layout.addWidget(fileOpen_btn)

        mandatoryFileOpenContainer.setLayout(fileOpen_layout)

        self.editor = TextEdit(parent=self)
        self.editor.setVerticalScrollBar(ScrollBar(Qt.Vertical))
        self.editor.setTabStopDistance(40)

        # print(self.editor.document().defaultStyleSheet())

        # Setup the QTextEdit editor configuration
        # self.editor.setAutoFormatting(QTextEdit.AutoAll)

        self.layout.addWidget(mandatoryFileOpenContainer)
        self.layout.addWidget(self.editor)
        # layout.setSpacing(0)
        # layout.setContentsMargins(5, 5, 5, 5)

        container = QWidget()
        container.setLayout(self.layout)

        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Uncomment to disable native menubar on Mac
        # self.menuBar().setNativeMenuBar(False)

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Toolbar ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
        file_toolbar = Toolbar("File", parent=self)
        # file_toolbar = Toolbar("File", basedir, self)

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━ Dock Widget ━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
        dockwidget = QDockWidget("Change Author")
        dockwidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        dockwidget.setMaximumWidth(176)
        dockwidget.setMinimumWidth(165)

        dock_innerContainer = QWidget()
        dockwidget.setWidget(dock_innerContainer)
        dock_layout = QVBoxLayout(dock_innerContainer)

        self.author_table = AuthorTable(parent=self)
        dock_layout.addWidget(self.author_table)

        addAuthor_btn = QPushButton("Add Author")
        addAuthor_btn.clicked.connect(lambda: self.author_table.addAuthor())

        resetFmt_btn = QPushButton("Reset Format")
        resetFmt_btn.clicked.connect(lambda: self.editor.removeCharFormatSelection())

        dock_layout.addWidget(addAuthor_btn)
        dock_layout.addWidget(resetFmt_btn)

        # self.author_table.cellClicked.connect(self.table_selection_changed)

        self.addDockWidget(Qt.RightDockWidgetArea, dockwidget)

        # Initialize default font size.
        font = QFont("Lexend", 12)
        self.editor.setFont(font)
        # We need to repeat the size to init the current format.
        self.editor.setFontPointSize(12)

        ### Initialize Contents
        self.file_open(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "test.html")
        )

        # signals
        self.editor.selectionChanged.connect(self.update_format)
        # self.editor.cursorPositionChanged.connect(self.cursor_moved)
        # self.editor.currentCharFormatChanged.connect(self.editor.s_formatChanged)
        # self.editor.selectionChanged.connect(self.editor.s_selectionChanged)
        # self.editor.s_formatChanged(None)

        self.refresh_btn = QPushButton("Refresh stylesheet")
        self.refresh_btn.clicked.connect(self.refresh_stylesheet)
        dock_layout.addWidget(self.refresh_btn)

        # Initialize.
        self.update_format()
        self.update_title()
        # self.cursor_moved()
        self.show()

        # print(self.editor.verticalScrollBar().styleSheet())
        self.editor.verticalScrollBar().setStyle(
            QCommonStyle()
        )  # to make the transparency work

        # cursor = self.editor.textCursor()
        # cursor.setCharFormat(textCharFormat)

        # self.editor.setCurrentCharFormat(self.textCharFormat)

        self.setMinimumSize(QSize(780, 510))

        # def table_selection_changed(self):
        # print("SELECTION CHANGED")
        # selected_rows = {r.row() for r in self.author_table.selectedIndexes()}

        # if len(selected_rows) != 1:
        #     return

        # print("CHANGING AUTHOR")
        # selected_row = list(selected_rows)[0]

        # author_name = self.author_table.item(selected_row, 0).text()

        # prop = self.author_table.author_dictionary[author_name]
        # print(prop)

        # self.editor.textCharFormat.setFontItalic(prop["italic"])
        # self.editor.textCharFormat.setFontWeight(prop["weight"])
        # self.editor.textCharFormat.setForeground(QColor(prop["foreground"]))
        # self.editor.textCharFormat.setBackground(QColor(prop["background"]))
        # self.editor.setCharFormatSelection()

    def refresh_stylesheet(self):
        qApp.setStyleSheet("".join(open(os.path.join(basedir, "dark.qss")).readlines()))

    def block_signals(self, objects, b):
        # print(objects)
        for o in objects:
            o.blockSignals(b)

    def update_format(self):
        """
        Update the font format toolbar/actions when a new text selection is made. This is neccessary to keep
        toolbars/etc. in sync with the current edit state.
        :return:
        """
        # self.editor.textIsSelected = True

        # print("selection changed")
        # Disable signals for all format widgets, so changing values here does not trigger further formatting.
        self.block_signals(self._format_actions, True)

        # self.fonts.setCurrentFont(self.editor.currentFont())
        # Nasty, but we get the font-size as a float but want it was an int
        self.fontsize.setCurrentText(str(int(self.editor.fontPointSize())))

        self.italic_action.setChecked(self.editor.fontItalic())
        self.underline_action.setChecked(self.editor.fontUnderline())
        self.bold_action.setChecked(self.editor.fontWeight() == QFont.Bold)

        self.alignl_action.setChecked(self.editor.alignment() == Qt.AlignLeft)
        self.alignc_action.setChecked(self.editor.alignment() == Qt.AlignCenter)
        self.alignr_action.setChecked(self.editor.alignment() == Qt.AlignRight)
        self.alignj_action.setChecked(self.editor.alignment() == Qt.AlignJustify)

        self.block_signals(self._format_actions, False)

    def open_directory(self):
        self.layout.setCurrentWidget(self.editor)

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def file_open(self, path=""):

        print(path)
        print(type(path))
        if path == "":
            path, _ = QFileDialog.getOpenFileName(
                self,
                "Open file",
                "",
                "HTML documents (*.html);;Text documents (*.txt);;All files (*.*)",
            )

        print(path)
        print(type(path))

        try:
            with open(path, "r") as f:
                text = f.read()

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            # Qt will automatically try and guess the format as txt/html

            self.editor.document().setDefaultStyleSheet(r"{}")

            # print(self.editor.document().defaultStyleSheet())

            self.editor.setHtml(text)
            self.update_title()

    def file_save(self):
        if self.path is None:
            # If we do not have a path, we need to use Save As.
            return self.file_saveas()

        text = (
            self.editor.toHtml()
            if splitext(self.path) in HTML_EXTENSIONS
            else self.editor.toPlainText()
        )

        try:
            with open(self.path, "w") as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save file",
            "",
            "HTML documents (*.html);Text documents (*.txt);All files (*.*)",
        )

        if not path:
            # If dialog is cancelled, will return ''
            return

        text = (
            self.editor.toHtml()
            if splitext(path) in HTML_EXTENSIONS
            else self.editor.toPlainText()
        )

        try:
            with open(path, "w") as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            self.update_title()

    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())

    def update_title(self):
        self.setWindowTitle(
            "%s - RePhraser"
            % (os.path.basename(self.path) if self.path else "Untitled")
        )

    def edit_toggle_wrap(self):
        self.editor.setLineWrapMode(1 if self.editor.lineWrapMode() == 0 else 0)

    def closeEvent(self, e):
        self.file_save()


if __name__ == "__main__":

    try:
        app = QApplication(sys.argv)

        QApplication.setStyle("Fusion")

        # Now use a palette to switch to dark colors:
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.Active, QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)
        dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, Qt.darkGray)
        dark_palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
        dark_palette.setColor(QPalette.Disabled, QPalette.Light, QColor(53, 53, 53))
        QApplication.setPalette(dark_palette)

        # qdarktheme.enable_hi_dpi()
        # qdarktheme.setup_theme(
        #     custom_colors={"primary": "#D0BCFF", "background": "24273a", "statusBar.background": "24273a", "toolbar.background": "24273a", "background>title": "c5c2c5", "foreground": "c5cff5", "border": "#39394a"})
        # qdarktheme.stop_sync()

        # app.setStyleSheet(Path("login.qss").read_text())
        app.setStyleSheet("".join(open(os.path.join(basedir, "dark.qss")).readlines()))
        # app.setWindowIcon(QIcon(os.path.join(basedir, "RePhraser.ico")))

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
    except Exception as e:
        # print(e)
        print(traceback.format_exc())

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

floor = math.floor

FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]
IMAGE_EXTENSIONS = [".jpg", ".png", ".bmp"]
HTML_EXTENSIONS = [".htm", ".html"]

basedir = os.path.dirname(__file__)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon("RePhrase.png"))

        layout = QVBoxLayout()

        self.editor = TextEdit(parent=self)
        self.editor.setVerticalScrollBar(ScrollBar(Qt.Vertical))
        self.editor.setTabStopDistance(40)

        print(self.editor.document().defaultStyleSheet())

        # Setup the QTextEdit editor configuration
        # self.editor.setAutoFormatting(QTextEdit.AutoAll)

        # self.path holds the path of the currently open file.
        # If none, we haven't got a file open yet (or creating new).
        self.path = None

        layout.addWidget(self.editor)
        layout.setSpacing(0)
        layout.setContentsMargins(5, 5, 5, 5)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Uncomment to disable native menubar on Mac
        # self.menuBar().setNativeMenuBar(False)

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Toolbar ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ #
        file_toolbar = QToolBar("File")
        file_toolbar.setIconSize(QSize(14, 14))
        self.addToolBar(file_toolbar)
        file_menu = self.menuBar().addMenu("&File")

        open_file_action = QAction(
            QIcon(os.path.join(basedir, "images", "blue-folder-open-document.png")),
            "Open file...",
            self,
        )
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)

        save_file_action = QAction(
            QIcon(os.path.join(basedir, "images", "disk.png")), "Save", self
        )
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)

        saveas_file_action = QAction(
            QIcon(os.path.join(basedir, "images", "disk--pencil.png")),
            "Save As...",
            self,
        )
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)

        print_action = QAction(
            QIcon(os.path.join(basedir, "images", "printer.png")), "Print...", self
        )
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)

        edit_toolbar = QToolBar("Edit")
        edit_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(edit_toolbar)
        edit_menu = self.menuBar().addMenu("&Edit")

        undo_action = QAction(
            QIcon(os.path.join(basedir, "images", "arrow-curve-180-left.png")),
            "Undo",
            self,
        )
        undo_action.setStatusTip("Undo last change")
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction(
            QIcon(os.path.join(basedir, "images", "arrow-curve.png")), "Redo", self
        )
        redo_action.setStatusTip("Redo last change")
        redo_action.triggered.connect(self.editor.redo)
        edit_toolbar.addAction(redo_action)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction(
            QIcon(os.path.join(basedir, "images", "scissors.png")), "Cut", self
        )
        cut_action.setStatusTip("Cut selected text")
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.triggered.connect(self.editor.cut)
        edit_toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)

        copy_action = QAction(
            QIcon(os.path.join(basedir, "images", "document-copy.png")), "Copy", self
        )
        copy_action.setStatusTip("Copy selected text")
        cut_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.editor.copy)
        edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)

        paste_action = QAction(
            QIcon(os.path.join(basedir, "images", "clipboard-paste-document-text.png")),
            "Paste",
            self,
        )
        paste_action.setStatusTip("Paste from clipboard")
        cut_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.editor.paste)
        edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)

        select_action = QAction(
            QIcon(os.path.join(basedir, "images", "selection-input.png")),
            "Select all",
            self,
        )
        select_action.setStatusTip("Select all text")
        cut_action.setShortcut(QKeySequence.SelectAll)
        select_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_action)

        edit_menu.addSeparator()

        wrap_action = QAction(
            QIcon(os.path.join(basedir, "images", "arrow-continue.png")),
            "Wrap text to window",
            self,
        )
        wrap_action.setStatusTip("Toggle wrap text to window")
        wrap_action.setCheckable(True)
        wrap_action.setChecked(True)
        wrap_action.triggered.connect(self.edit_toggle_wrap)
        edit_menu.addAction(wrap_action)

        format_toolbar = QToolBar("Format")
        format_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(format_toolbar)
        format_menu = self.menuBar().addMenu("&Format")

        # We need references to these actions/settings to update as selection changes, so attach to self.
        self.fonts = QFontComboBox()
        self.fonts.currentFontChanged.connect(self.editor.setCurrentFont)
        format_toolbar.addWidget(self.fonts)

        self.fontsize = QComboBox()
        self.fontsize.addItems([str(s) for s in FONT_SIZES])

        # Connect to the signal producing the text of the current selection. Convert the string to float
        # and set as the pointsize. We could also use the index + retrieve from FONT_SIZES.
        self.fontsize.currentIndexChanged[str].connect(
            lambda s: self.editor.setFontPointSize(float(s))
        )
        format_toolbar.addWidget(self.fontsize)

        bold_image = QImage(os.path.join(basedir, "images", "edit-bold.png"))
        bold_image.invertPixels()
        bold_pixmap = QPixmap.fromImage(bold_image)

        self.bold_action = QAction(QIcon(bold_pixmap), "Bold", self)
        self.bold_action.setStatusTip("Bold")
        self.bold_action.setShortcut(QKeySequence.Bold)
        self.bold_action.setCheckable(True)
        self.bold_action.toggled.connect(
            lambda x: self.editor.setFontWeight(QFont.Bold if x else QFont.Normal)
        )
        format_toolbar.addAction(self.bold_action)
        format_menu.addAction(self.bold_action)

        italic_image = QImage(os.path.join(basedir, "images", "edit-italic.png"))
        italic_image.invertPixels()
        italic_pixmap = QPixmap.fromImage(italic_image)

        self.italic_action = QAction(QIcon(italic_pixmap), "Italic", self)
        self.italic_action.setStatusTip("Italic")
        self.italic_action.setShortcut(QKeySequence.Italic)
        self.italic_action.setCheckable(True)
        self.italic_action.toggled.connect(self.editor.setFontItalic)
        format_toolbar.addAction(self.italic_action)
        format_menu.addAction(self.italic_action)

        underline_image = QImage(os.path.join(basedir, "images", "edit-underline.png"))
        underline_image.invertPixels()
        underline_pixmap = QPixmap.fromImage(underline_image)

        self.underline_action = QAction(QIcon(underline_pixmap), "Underline", self)
        self.underline_action.setStatusTip("Underline")
        self.underline_action.setShortcut(QKeySequence.Underline)
        self.underline_action.setCheckable(True)
        self.underline_action.toggled.connect(self.editor.setFontUnderline)
        format_toolbar.addAction(self.underline_action)
        format_menu.addAction(self.underline_action)

        format_menu.addSeparator()

        alignl_image = QImage(os.path.join(basedir, "images", "edit-alignment.png"))
        alignl_image.invertPixels()
        alignl_pixmap = QPixmap.fromImage(alignl_image)

        self.alignl_action = QAction(QIcon(alignl_pixmap), "Align left", self)
        self.alignl_action.setStatusTip("Align text left")
        self.alignl_action.setCheckable(True)
        self.alignl_action.triggered.connect(
            lambda: self.editor.setAlignment(Qt.AlignLeft)
        )
        format_toolbar.addAction(self.alignl_action)
        format_menu.addAction(self.alignl_action)

        alignc_image = QImage(
            os.path.join(basedir, "images", "edit-alignment-center.png")
        )
        alignc_image.invertPixels()
        alignc_pixmap = QPixmap.fromImage(alignc_image)

        self.alignc_action = QAction(QIcon(alignc_pixmap), "Align center", self)
        self.alignc_action.setStatusTip("Align text center")
        self.alignc_action.setCheckable(True)
        self.alignc_action.triggered.connect(
            lambda: self.editor.setAlignment(Qt.AlignCenter)
        )
        format_toolbar.addAction(self.alignc_action)
        format_menu.addAction(self.alignc_action)

        alignr_image = QImage(
            os.path.join(basedir, "images", "edit-alignment-right.png")
        )
        alignr_image.invertPixels()
        alignr_pixmap = QPixmap.fromImage(alignc_image)

        self.alignr_action = QAction(QIcon(alignr_pixmap), "Align right", self)
        self.alignr_action.setStatusTip("Align text right")
        self.alignr_action.setCheckable(True)
        self.alignr_action.triggered.connect(
            lambda: self.editor.setAlignment(Qt.AlignRight)
        )
        format_toolbar.addAction(self.alignr_action)
        format_menu.addAction(self.alignr_action)

        alignj_image = QImage(
            os.path.join(basedir, "images", "edit-alignment-justify.png")
        )
        alignj_image.invertPixels()
        alignj_pixmap = QPixmap.fromImage(alignj_image)

        self.alignj_action = QAction(QIcon(alignj_pixmap), "Justify", self)
        self.alignj_action.setStatusTip("Justify text")
        self.alignj_action.setCheckable(True)
        self.alignj_action.triggered.connect(
            lambda: self.editor.setAlignment(Qt.AlignJustify)
        )
        format_toolbar.addAction(self.alignj_action)
        format_menu.addAction(self.alignj_action)

        format_group = QActionGroup(self)
        format_group.setExclusive(True)
        format_group.addAction(self.alignl_action)
        format_group.addAction(self.alignc_action)
        format_group.addAction(self.alignr_action)
        format_group.addAction(self.alignj_action)

        format_menu.addSeparator()

        # A list of all format-related widgets/actions, so we can disable/enable signals when updating.
        self._format_actions = [
            self.fonts,
            self.fontsize,
            self.bold_action,
            self.italic_action,
            self.underline_action,
            # We don't need to disable signals for alignment, as they are paragraph-wide.
        ]

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

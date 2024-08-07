from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import os

FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]


class Toolbar(QToolBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print(self.parent())

        self.parent().addToolBar(self)
        self.setIconSize(QSize(14, 14))
        file_menu = self.parent().menuBar().addMenu("&File")

        open_file_action = QAction(
            QIcon(":/icons/blue-folder-open-document.png"),
            "Open file...",
            self.parent(),
        )
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.parent().file_open)
        file_menu.addAction(open_file_action)
        self.addAction(open_file_action)

        save_file_action = QAction(QIcon(":/icons/disk.png"), "Save", self.parent())
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.parent().file_save)
        file_menu.addAction(save_file_action)
        self.addAction(save_file_action)

        saveas_file_action = QAction(
            QIcon(":/icons/disk--pencil.png"),
            "Save As...",
            self.parent(),
        )
        saveas_file_action.setShortcut(QKeySequence.Save)
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.triggered.connect(self.parent().file_saveas)
        file_menu.addAction(saveas_file_action)
        self.addAction(saveas_file_action)

        print_action = QAction(
            QIcon(":/icons/printer.png"),
            "Print...",
            self.parent(),
        )
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.parent().file_print)
        file_menu.addAction(print_action)
        self.addAction(print_action)

        edit_toolbar = QToolBar("Edit")
        edit_toolbar.setIconSize(QSize(16, 16))
        self.parent().addToolBar(edit_toolbar)
        edit_menu = self.parent().menuBar().addMenu("&Edit")

        undo_action = QAction(
            QIcon(":/icons/arrow-curve-180-left.png"),
            "Undo",
            self.parent(),
        )
        undo_action.setStatusTip("Undo last change")
        undo_action.triggered.connect(self.parent().editor.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction(
            QIcon(":/icons/arrow-curve.png"),
            "Redo",
            self.parent(),
        )
        redo_action.setStatusTip("Redo last change")
        redo_action.triggered.connect(self.parent().editor.redo)
        edit_toolbar.addAction(redo_action)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction(QIcon(":/icons/scissors.png"), "Cut", self.parent())
        cut_action.setStatusTip("Cut selected text")
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.triggered.connect(self.parent().editor.cut)
        edit_toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)

        copy_action = QAction(
            QIcon(":/icons/document-copy.png"),
            "Copy",
            self.parent(),
        )
        copy_action.setStatusTip("Copy selected text")
        cut_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.parent().editor.copy)
        edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)

        paste_action = QAction(
            QIcon(":/icons/clipboard-paste-document-text.png"),
            "Paste",
            self.parent(),
        )
        paste_action.setStatusTip("Paste from clipboard")
        cut_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.parent().editor.paste)
        edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)

        select_action = QAction(
            QIcon(":/icons/selection-input.png"),
            "Select all",
            self.parent(),
        )
        select_action.setStatusTip("Select all text")
        cut_action.setShortcut(QKeySequence.SelectAll)
        select_action.triggered.connect(self.parent().editor.selectAll)
        edit_menu.addAction(select_action)

        edit_menu.addSeparator()

        wrap_action = QAction(
            QIcon(":/icons/arrow-continue.png"),
            "Wrap text to window",
            self.parent(),
        )
        wrap_action.setStatusTip("Toggle wrap text to window")
        wrap_action.setCheckable(True)
        wrap_action.setChecked(True)
        wrap_action.triggered.connect(self.parent().edit_toggle_wrap)
        edit_menu.addAction(wrap_action)

        format_toolbar = QToolBar("Format")
        format_toolbar.setIconSize(QSize(16, 16))
        self.parent().addToolBar(format_toolbar)
        format_menu = self.parent().menuBar().addMenu("&Format")

        # We need references to these actions/settings to update as selection changes, so attach to self.parent().
        self.parent().fonts = QFontComboBox()
        self.parent().fonts.currentFontChanged.connect(
            self.parent().editor.setCurrentFont
        )
        font = QFont("Lexend", 12)
        self.parent().fonts.setCurrentFont(font)
        self.parent().editor.setFont(font)
        format_toolbar.addWidget(self.parent().fonts)

        self.parent().fontsize = QComboBox()
        self.parent().fontsize.addItems([str(s) for s in FONT_SIZES])

        # Connect to the signal producing the text of the current selection. Convert the string to float
        # and set as the pointsize. We could also use the index + retrieve from FONT_SIZES.
        self.parent().fontsize.currentIndexChanged[str].connect(
            lambda s: self.parent().editor.setFontPointSize(float(s))
        )
        format_toolbar.addWidget(self.parent().fontsize)

        bold_image = QImage(":/icons/edit-bold.png")
        bold_image.invertPixels()
        bold_pixmap = QPixmap.fromImage(bold_image)

        self.parent().bold_action = QAction(QIcon(bold_pixmap), "Bold", self.parent())
        self.parent().bold_action.setStatusTip("Bold")
        self.parent().bold_action.setShortcut(QKeySequence.Bold)
        self.parent().bold_action.setCheckable(True)
        self.parent().bold_action.toggled.connect(
            lambda x: self.parent().editor.setFontWeight(
                QFont.Bold if x else QFont.Normal
            )
        )
        format_toolbar.addAction(self.parent().bold_action)
        format_menu.addAction(self.parent().bold_action)

        italic_image = QImage(":/icons/edit-italic.png")
        italic_image.invertPixels()
        italic_pixmap = QPixmap.fromImage(italic_image)

        self.parent().italic_action = QAction(
            QIcon(italic_pixmap), "Italic", self.parent()
        )
        self.parent().italic_action.setStatusTip("Italic")
        self.parent().italic_action.setShortcut(QKeySequence.Italic)
        self.parent().italic_action.setCheckable(True)
        self.parent().italic_action.toggled.connect(self.parent().editor.setFontItalic)
        format_toolbar.addAction(self.parent().italic_action)
        format_menu.addAction(self.parent().italic_action)

        underline_image = QImage(":/icons/edit-underline.png")
        underline_image.invertPixels()
        underline_pixmap = QPixmap.fromImage(underline_image)

        self.parent().underline_action = QAction(
            QIcon(underline_pixmap), "Underline", self.parent()
        )
        self.parent().underline_action.setStatusTip("Underline")
        self.parent().underline_action.setShortcut(QKeySequence.Underline)
        self.parent().underline_action.setCheckable(True)
        self.parent().underline_action.toggled.connect(
            self.parent().editor.setFontUnderline
        )
        format_toolbar.addAction(self.parent().underline_action)
        format_menu.addAction(self.parent().underline_action)

        format_menu.addSeparator()

        alignl_image = QImage(":/icons/edit-alignment.png")
        alignl_image.invertPixels()
        alignl_pixmap = QPixmap.fromImage(alignl_image)

        self.parent().alignl_action = QAction(
            QIcon(alignl_pixmap), "Align left", self.parent()
        )
        self.parent().alignl_action.setStatusTip("Align text left")
        self.parent().alignl_action.setCheckable(True)
        self.parent().alignl_action.triggered.connect(
            lambda: self.parent().editor.setAlignment(Qt.AlignLeft)
        )
        format_toolbar.addAction(self.parent().alignl_action)
        format_menu.addAction(self.parent().alignl_action)

        alignc_image = QImage(":/icons/edit-alignment-center.png")
        alignc_image.invertPixels()
        alignc_pixmap = QPixmap.fromImage(alignc_image)

        self.parent().alignc_action = QAction(
            QIcon(alignc_pixmap), "Align center", self.parent()
        )
        self.parent().alignc_action.setStatusTip("Align text center")
        self.parent().alignc_action.setCheckable(True)
        self.parent().alignc_action.triggered.connect(
            lambda: self.parent().editor.setAlignment(Qt.AlignCenter)
        )
        format_toolbar.addAction(self.parent().alignc_action)
        format_menu.addAction(self.parent().alignc_action)

        alignr_image = QImage(":/icons/edit-alignment-right.png")

        alignr_image.invertPixels()
        alignr_pixmap = QPixmap.fromImage(alignr_image)

        self.parent().alignr_action = QAction(
            QIcon(alignr_pixmap), "Align right", self.parent()
        )
        self.parent().alignr_action.setStatusTip("Align text right")
        self.parent().alignr_action.setCheckable(True)
        self.parent().alignr_action.triggered.connect(
            lambda: self.parent().editor.setAlignment(Qt.AlignRight)
        )
        format_toolbar.addAction(self.parent().alignr_action)
        format_menu.addAction(self.parent().alignr_action)

        alignj_image = QImage(":/icons/edit-alignment-justify.png")

        alignj_image.invertPixels()
        alignj_pixmap = QPixmap.fromImage(alignj_image)

        self.parent().alignj_action = QAction(
            QIcon(alignj_pixmap), "Justify", self.parent()
        )
        self.parent().alignj_action.setStatusTip("Justify text")
        self.parent().alignj_action.setCheckable(True)
        self.parent().alignj_action.triggered.connect(
            lambda: self.parent().editor.setAlignment(Qt.AlignJustify)
        )
        format_toolbar.addAction(self.parent().alignj_action)
        format_menu.addAction(self.parent().alignj_action)

        format_group = QActionGroup(self.parent())
        format_group.setExclusive(True)
        format_group.addAction(self.parent().alignl_action)
        format_group.addAction(self.parent().alignc_action)
        format_group.addAction(self.parent().alignr_action)
        format_group.addAction(self.parent().alignj_action)

        format_menu.addSeparator()

        # A list of all format-related widgets/actions, so we can disable/enable signals when updating.
        self.parent()._format_actions = [
            self.parent().fonts,
            self.parent().fontsize,
            self.parent().bold_action,
            self.parent().italic_action,
            self.parent().underline_action,
            # We don't need to disable signals for alignment, as they are paragraph-wide.
        ]

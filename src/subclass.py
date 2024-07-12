from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *

import os
import sys
import uuid
import math

floor = math.floor


def hexuuid():
    return uuid.uuid4().hex


def splitext(p):
    return os.path.splitext(p)[1].lower()


class ScrollBar(QScrollBar):
    def __init__(self, *args, **kwargs):
        super(QScrollBar, self).__init__(*args, **kwargs)

    def enterEvent(self, e):
        self.setStyleSheet(
            """
        QScrollBar::vertical:hover {
            min-height: 0px;
            border: 0px solid red;
            border-radius: 4px;
            /*width: 8px;*/
            width: 4px;
        }"""
        )

    def leaveEvent(self, e):
        self.setStyleSheet("")


class ClickableLabel(QLabel):

    clicked = pyqtSignal()

    def __init__(self, color: QColor):
        super(QLabel, self).__init__()
        self.setGeometry(100, 100, 200, 60)

        self.color = color
        self.redrawLabel()

        self.clicked.connect(self.changeColor)

    def mousePressEvent(self, e):
        self.clicked.emit()

    def changeColor(self):
        print(f"Changing {self.color.name()}")
        color = QColorDialog.getColor(
            initial=self.color,
            title="Select Color",
            options=QColorDialog.ShowAlphaChannel,
        )
        self.color = color if color.isValid() else self.color
        print(f"to {self.color.name()}")

        # setting option
        # dialog.setOption(QColorDialog.ShowAlphaChannel)

        # executing the dialog
        # dialog.exec_()
        self.redrawLabel()

    def redrawLabel(self):
        self.setStyleSheet(
            "QLabel"
            "{"
            f"background-color : {self.color.name()};"
            "border : 1px solid black;"
            "}"
        )


class TextEdit(QTextEdit):
    def __init__(self, *args, **kwargs):
        super(QTextEdit, self).__init__(*args, **kwargs)
        self.textIsSelected = False

        # Setting cursor's current character format
        self.textCharFormat = QTextCharFormat()
        # self.textCharFormat.setFontItalic(True)

        # self.textCharFormat.setBackground(Qt.red)
        self.textCharFormat.setFontWeight(75)

        self.images = {}
        self.DPM = floor(1 * 39.37)

    def canInsertFromMimeData(self, source):

        if source.hasImage():
            return True
        else:
            return super(TextEdit, self).canInsertFromMimeData(source)

    def insertFromMimeData(self, source):

        cursor = self.textCursor()
        document = self.document()

        if source.hasUrls():
            for u in source.urls():
                file_ext = splitext(str(u.toLocalFile()))
                if u.isLocalFile() and file_ext in IMAGE_EXTENSIONS:
                    image = QImage(u.toLocalFile())
                    # document.addResource(QTextDocument.ImageResource, u, image)
                    # uuid = hexuuid()
                    print("IMAGE FROM FILE")
                    uuid = self.addImageResource(image)
                    cursor.insertImage(uuid)

                else:
                    # If we hit a non-image or non-local URL break the loop and fall out
                    # to the super call & let Qt handle it
                    break

            else:
                # If all were valid images, finish here.
                return

        elif source.hasImage():
            print("INSERTING IMAGE")
            image = source.imageData()
            # uuid = hexuuid()

            uuid = self.addImageResource(image)

            # self.images[uuid] = image

            # width = image.width()
            # height = image.height()

            # text_area_width = self.width() - 32
            # # text_area_width = self.document().idealWidth() # still not enough, clipping occurs

            # scaled_image = image
            # # if width >= text_area_width:
            #     # conssider padding
            # factor = text_area_width / width
            # width *= factor
            # height *= factor

            # scaled_image = image.scaledToWidth(floor(width), Qt.SmoothTransformation)

            # # scaled_image.setDotsPerMeterX(self.DPM);
            # # scaled_image.setDotsPerMeterY(self.DPM);

            # document.addResource(QTextDocument.ImageResource, QUrl(uuid), scaled_image)

            # fragment = QTextDocumentFragment.fromHtml(f"<img src='{uuid}' height='{height}' width='{width}'></img>")

            # cursor.insertFragment(fragment)
            cursor.insertImage(uuid)
            # return

        super().insertFromMimeData(source)

    # def s_formatChanged(self, e):
    #     print("Format Changed")
    #     # print("cursor Moved")
    #     # if (not self.editor.textIsSelected):
    #     # if e.fontWeight() == 75:
    #     #     return
    #     if self.cursor.selection().isEmpty():
    #         self.setCurrentCharFormat(self.textCharFormat)
    #         # self.setCharFormat(self.textCharFormat)

    # def keyPressEvent(self, e):
    #     self.setCurrentCharFormat(self.textCharFormat)

    def keyPressEvent(self, e):
        # print("KeyPressed")
        # print(self.m_cursor)

        # cursorIsEmpty = self.m_cursor.selection().isEmpty()

        # if cursorIsEmpty:
        #     self.setCurrentCharFormat(self.textCharFormat)
        #         # self.setCharFormat(self.textCharFormat)
        # elif not cursorIsEmpty:
        #     self.m_cursor.deleteChar()
        #     self.setCurrentCharFormat(self.textCharFormat)

        # if e.key() == Qt.Key_Backspace:
        #     self.textCursor().deletePreviousChar()
        #     return
        print("'" + e.text() + "'")

        # if e.key() == Qt.Key_Backspace:
        #     self.textCursor().deletePreviousChar()
        #     return
        # elif e.key() == Qt.Key_Delete:
        #     self.textCursor().deleteChar()
        #     return

        if e.text().isalnum():
            print("ALPHANUMERIC")
            self.textCursor().insertText(e.text(), self.textCharFormat)
            return
        # else:

        super().keyPressEvent(e)

        # return

    def setCharFormatSelection(self):
        print("SET CHAR FORMAT SELECTION")
        print(self.textCharFormat.fontWeight())
        print(self.textCharFormat.fontItalic())

        self.textCursor().setCharFormat(self.textCharFormat)

    def removeCharFormatSelection(self):
        pass

    def resizeEvent(self, e):
        # print(f"{self.document().idealWidth()} : {self.width()}")

        # cur_pos = 0

        # while cur_pos < self.textCursor().position():
        #     found_cursor = self.document().find(self.image_regex, cur_pos)

        #     if found_cursor.position() == -1:
        #         print("NO IMAGE FOUND")
        #         break

        #     text = found_cursor.selectedText()

        #     self.image_regex.indexIn(text)
        #     print(f"ima: {self.image_regex.cap(1)}")
        #     print(f"cur_pos: {cur_pos}")

        #     cur_pos = found_cursor.position()
        # text_area_width = self.width() - 32
        for uuid in self.images.keys():

            resource = self.document().resource(QTextDocument.ImageResource, QUrl(uuid))

            if resource == None:
                del self.images[uuid]
                continue

            self.addImageResource(self.images[uuid])

        super().resizeEvent(e)
        # resize pictures to match the max width

    def addImageResource(self, ImageResource: QImage, uuid=hexuuid()):
        # cases:
        # pasted image: uuid = generated from hash
        # local file draged: uuid = file path
        if uuid == "":
            raise ValueError("provided 'uuid' is empty")

        self.images[uuid] = ImageResource

        print("INSERTING IMAGE")

        width = ImageResource.width()
        height = ImageResource.height()

        text_area_width = self.width() - 32
        # if width >= text_area_width:
        # conssider padding
        factor = text_area_width / width
        width *= factor
        # height *= factor

        # print(resource.value())
        sc_ImageResource = ImageResource.scaledToWidth(
            floor(width), Qt.SmoothTransformation
        )
        # sc_resource.setDotsPerMeterX(self.DPM);
        # sc_resource.setDotsPerMeterY(self.DPM);

        self.document().addResource(
            QTextDocument.ImageResource, QUrl(uuid), sc_ImageResource
        )

        return uuid


class AuthorTable(QTableWidget):
    def __init__(self):
        super().__init__()

        self.settings = QSettings("DeadBush225", "RePhraser")

        # self.author_dictionary = {}
        self.author_dictionary = self.settings.value("authors")
        # print(retrieved)

        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Author", "Signature"])
        self.verticalHeader().hide()
        # self.author_dictionary = author_dictionary

        if not self.author_dictionary:
            self.author_dictionary = {
                "Ai": {
                    "italic": False,
                    "weight": 800,
                    "foreground": "#fc3737",
                    "background": "#fc6f37",
                },
                "ChatGPT": {
                    "italic": False,
                    "weight": 1200,
                    "foreground": "#3772fc",
                    "background": "#53D85A",
                },
                "Rhixie": {
                    "italic": True,
                    "weight": 700,
                    "foreground": "#fcdb37",
                    "background": "#9037fc",
                },
            }

        print(self.author_dictionary)
        keys = self.author_dictionary.keys()
        for author_name in keys:
            if not author_name in self.author_dictionary:
                print(f"is '{author_name}' in {self.author_dictionary}?")
                continue

            try:
                color = self.author_dictionary[author_name]["foreground"]
                weight = self.author_dictionary[author_name]["weight"]
                background = self.author_dictionary[author_name]["background"]
                italic = self.author_dictionary[author_name]["italic"]
                # italic = "italic" if italic else ""
            except Exception:
                print("INVALID SETTING: PURGING")
                self.author_dictionary.pop(author_name)
                continue

            self.addEntry(author_name, color, background, weight, italic)
            # output = f'<font color="{color}"; weight="{weight}";background-color="{background_color}">Test</font>'

            # author_table.setItem()

        # self.author_table.resizeColumnsToContents()
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.cellDoubleClicked.connect(
            lambda row, col: self.addAuthor(
                author_name=self.item(row, 0).text(), overrideRow=True
            )
        )

    def addAuthor(self, *s, author_name="", overrideRow=False):
        print(f"ADDING AUTHOR: {author_name}")
        # property_dict = {}

        foreground = QColor(Qt.white)
        background = QColor(Qt.white)
        italic = False
        weight = 800

        if overrideRow:
            # color = Qt.white
            foreground = QColor(
                self.author_dictionary[author_name]["foreground"],
            )
            background = QColor(
                self.author_dictionary[author_name]["background"],
            )
            italic = self.author_dictionary[author_name]["italic"]
            weight = self.author_dictionary[author_name]["weight"]

        # property_dict["foreground"] = foreground
        # property_dict["background"] = background
        # property_dict["italic"] = italic
        # property_dict["bold"] = bold

        self.addAuthorWidget = QDialog()

        mainlayout = QVBoxLayout()

        author_cont = QHBoxLayout()
        author_cont.addWidget(QLabel("Author Name: "))
        author_field = QLineEdit(author_name)
        author_cont.addWidget(author_field)

        foreground_cont = QHBoxLayout()
        foreground_cont.addWidget(QLabel("Foreground: "))
        self.colorPrev_foreground = ClickableLabel(foreground)
        foreground_cont.addWidget(self.colorPrev_foreground)

        background_cont = QHBoxLayout()
        background_cont.addWidget(QLabel("Background: "))
        self.colorPrev_background = ClickableLabel(background)
        background_cont.addWidget(self.colorPrev_background)

        weight_cont = QHBoxLayout()
        weight_cont.addWidget(QLabel("Weight: "))
        self.weight_spinbox = QSpinBox()
        self.weight_spinbox.setMinimum(100)
        self.weight_spinbox.setMaximum(1200)
        self.weight_spinbox.setSingleStep(100)
        self.weight_spinbox.setValue(weight)
        weight_cont.addWidget(self.weight_spinbox)

        formatting_cont = QHBoxLayout()
        # self.isBold = QCheckBox("Bold")
        self.isItalic = QCheckBox("Italic")
        self.isItalic.setChecked(italic)
        # formatting_cont.addWidget(self.isBold)
        formatting_cont.addWidget(self.isItalic)

        self.saveAuthor_btn = QPushButton("Save Author")

        # close before adding lambda function
        self.saveAuthor_btn.clicked.connect(
            lambda: (
                self.addAuthorWidget.done(1),
                self.addEntry(
                    author_field.text(),
                    self.colorPrev_foreground.color.name(QColor.HexArgb),
                    self.colorPrev_background.color.name(QColor.HexArgb),
                    self.weight_spinbox.value(),
                    self.isItalic.isChecked(),
                    self.selectedRows()[0] if overrideRow else None,
                ),
            )[-1]
        )
        # set author name

        mainlayout.addLayout(author_cont)
        mainlayout.addLayout(foreground_cont)
        mainlayout.addLayout(background_cont)
        mainlayout.addLayout(weight_cont)
        mainlayout.addLayout(formatting_cont)
        mainlayout.addWidget(self.saveAuthor_btn)

        self.addAuthorWidget.setLayout(mainlayout)

        self.addAuthorWidget.exec_()

        # save the prop dict

    # def saveProp(self, author_name):
    #     print("SAVING AUTHOR")

    # self.addEntry(author_name, color, background, weight, italic)

    def addEntry(self, author_name, color, background, weight, italic, row_count=None):
        prop = {}
        prop["foreground"] = color
        prop["background"] = background
        prop["italic"] = italic
        prop["weight"] = weight

        # self.addAuthorWidget.done(1)

        if row_count == None:
            row_count = self.rowCount()
            self.insertRow(row_count)

            self.author_dictionary[author_name] = prop

        elif row_count != None:
            print("ROW DEFINED: OVERRIDING")

            # row is defined which means it is overriden
            # replace old name with new
            old_name = self.item(self.selectedRows()[0], 0).text()
            self.author_dictionary = {
                (key if key != old_name else author_name): value
                for (key, value) in self.author_dictionary.items()
            }

        print(self.author_dictionary)
        self.saveSettings()
        print(self.settings.value("authors"))

        # if author_name in self.author_dictionary:
        #     # self.reDrawRow(author_name)
        #     row_count = self.selectedRows()[0]
        # else:
        # row_count = self.rowCount()
        # if (self.selectedRows() and (author_name in self.author_dictionary)):
        # print("name already exists, override mode")
        #     row_count = self.selectedRows()[0]
        # else:
        #     row_count = self.rowCount()

        self.setItem(row_count, 0, QTableWidgetItem(author_name))

        signature_preview = QLabel("Test")
        signature_preview.setStyleSheet(
            f"""
            color: {color};
            background: {background};
            font-weight: {weight};
            font-style: {"italic" if italic else ""};
        """
        )

        self.setCellWidget(row_count, 1, signature_preview)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)

        if e.button() != Qt.RightButton:
            return

        print("MOUSE RIGHT CLICK")

        selected_rows = self.selectedRows()
        # selected_rows.sort()

        # print(selected_row)

        if len(selected_rows) == 1:
            selected_row = selected_rows[0]
            print("TRYING TO DELETE")
            name = self.item(selected_row, 0).text()
            print(name)
            print(self.author_dictionary)

            self.author_dictionary.pop(name)
            self.removeRow(selected_row)

            self.saveSettings()

    def saveSettings(self):
        self.settings.setValue("authors", self.author_dictionary)

    # def reDrawRow(self, ):
    def selectedRows(self):
        return list(set([r.row() for r in self.selectedIndexes()]))

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from lib.helper import *
from lib.Stores import store
from lib.qt_helper import HLine

import math


class PasteFromAuthorDialog(QDialog):

    author = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent_ = parent

        self.setWindowTitle("Paste as Author")

        mainlayout = QVBoxLayout()

        author_cont = QHBoxLayout()

        self.author_cmbx = QComboBox()
        self.fillComboBox()

        # print("PARENT of AUTHOR DIALOG")
        # print(self.parent())
        # print(self.parent().parent())
        # self.author_cmbx.addItems(
        # list(self.parent().parent().author_table.author_dictionary.keys())
        # )

        author_cont.addWidget(QLabel("Existing Author: "))
        author_cont.addWidget(self.author_cmbx)

        self.saveAuthor_btn = QPushButton("Ok")
        self.saveAuthor_btn.clicked.connect(lambda: self.fin())

        self.newAuthor_btn = QPushButton("Add as new Author")
        self.newAuthor_btn.clicked.connect(self.addNewAuthor)

        # close before adding lambda function

        mainlayout.addLayout(author_cont)
        mainlayout.addWidget(self.saveAuthor_btn)
        mainlayout.addWidget(HLine())
        mainlayout.addWidget(self.newAuthor_btn)

        self.setLayout(mainlayout)

    def addNewAuthor(self):
        self.parent_.parent_.author_table.addAuthor("")
        self.fillComboBox()

    def fillComboBox(self):
        self.author_cmbx.clear()
        self.author_cmbx.addItems(store.author_dictionary.keys())

    def fin(self):
        self.done(QDialog.Accepted)
        self.author.emit(self.author_cmbx.currentText())


class TextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent_ = parent
        self.textIsSelected = False

        print("PARENT of TEXTEDIT")
        print(self)
        print(self.parent())
        # self.setParent(parent=parent)Z

        # Setting cursor's current character format
        self.textCharFormat = QTextCharFormat()
        # self.textCharFormat.setFontItalic(True)

        # self.textCharFormat.setBackground(Qt.red)
        # self.textCharFormat.setFontWeight(75)

        self.defaultCharFormat = QTextCharFormat()
        # self.defaultCharFormat.setFontWeight(100)

        self.images = {}
        self.DPM = math.floor(1 * 39.37)

    def canInsertFromMimeData(self, source):
        if source.hasImage():
            return True
        else:
            return super(TextEdit, self).canInsertFromMimeData(source)

    def insertFromMimeData(self, source):
        print("INSERT FROM MIME DATA")
        cursor = self.textCursor()
        document = self.document()

        if source.hasText():
            print(cursor.selectedText())
            print(source.text())
            # print(self.parent())
            te = PasteFromAuthorDialog(parent=self)
            te.author.connect(self.setTextCharFormat)
            te.exec_()

            self.setCharFormatSelection()
            self.textCursor().insertText(source.text(), self.textCharFormat)

            return

            # print(source.text())

        elif source.hasUrls():
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

        if e.text().isalnum() or (e.text() == " "):
            print("ALPHANUMERIC")
            self.textCursor().insertText(e.text(), self.defaultCharFormat)
            return
        # else:

        super().keyPressEvent(e)

        # return

    def setCharFormatSelection(self):
        print("SET CHAR FORMAT SELECTION")
        print(self.textCharFormat.fontWeight())
        print(self.textCharFormat.fontItalic())
        print(self.textCharFormat.foreground())
        print(self.textCharFormat.background())

        # self.textCharFormat.setFontWeight(100)

        # text = self.textCursor().selection().toPlainText()

        # style = ""

        # if self.textCharFormat.fontWeight() != self.defaultCharFormat.fontWeight():
        #     style += f"font-weight:{self.textCharFormat.fontWeight() * 8};"
        # if self.textCharFormat.fontItalic() != self.defaultCharFormat.fontItalic():
        #     style += f"font-style:italic;margin-right:5px;"
        # if self.textCharFormat.background() != self.defaultCharFormat.background():
        #     style += f"background-color:{self.textCharFormat.background().color().name(QColor.HexArgb)};"
        # if self.textCharFormat.foreground() != self.defaultCharFormat.foreground():
        #     style += f"color:{self.textCharFormat.foreground().color().name(QColor.HexArgb)};"

        # content = f'<span style="{style}">{text}</span>'

        # self.textCursor().insertHtml(content)

        self.textCursor().setCharFormat(self.textCharFormat)

    def removeCharFormatSelection(self):
        self.textCursor().setCharFormat(self.defaultCharFormat)

    def setTextCharFormat(self, authorName):
        prop = store.author_dictionary[authorName]
        print(prop)

        self.textCharFormat.setFontItalic(prop["italic"])
        self.textCharFormat.setFontWeight(prop["weight"])
        self.textCharFormat.setForeground(QColor(prop["foreground"]))
        self.textCharFormat.setBackground(QColor(prop["background"]))

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
            math.floor(width), Qt.SmoothTransformation
        )
        # sc_resource.setDotsPerMeterX(self.DPM);
        # sc_resource.setDotsPerMeterY(self.DPM);

        self.document().addResource(
            QTextDocument.ImageResource, QUrl(uuid), sc_ImageResource
        )

        return uuid

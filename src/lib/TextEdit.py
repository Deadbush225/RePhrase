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

        author_cont.addWidget(QLabel("Existing Author: "))
        author_cont.addWidget(self.author_cmbx)

        self.saveAuthor_btn = QPushButton("Ok")
        self.saveAuthor_btn.clicked.connect(lambda: self.fin())

        self.newAuthor_btn = QPushButton("Add as new Author")
        self.newAuthor_btn.clicked.connect(self.addNewAuthor)

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
        self.dropped_text = None

        self.textCharFormat = QTextCharFormat()

        self.defaultCharFormat = QTextCharFormat()

        self.images = {}
        self.DPM = math.floor(1 * 39.37)

    def dropEvent(self, event):
        m = event.mimeData()
        if m.hasText():
            self.dropped_text = m.text()

        super().dropEvent(event)

    def canInsertFromMimeData(self, source):
        if source.hasImage():
            return True
        else:
            return super(TextEdit, self).canInsertFromMimeData(source)

    def insertFromMimeData(self, source):
        print("INSERT FROM MIME DATA")
        cursor = self.textCursor()
        document = self.document()

        if source.hasImage():
            print("INSERTING IMAGE")
            image = source.imageData()

            uuid = self.addImageResource(image)
            # fragment = QTextDocumentFragment.fromHtml(
            #     f"<img src='{source.text()}' height='{height}' width='{width}'></img>"
            # )

            # cursor.insertFragment(fragment)
            self.setAlignment(Qt.AlignCenter)
            cursor.insertImage(uuid)
            # cursor.insertImage(uuid)
            return

        elif source.hasText():
            selectedTextIsBeingDragged = self.dropped_text == source.text()

            if not selectedTextIsBeingDragged:
                te = PasteFromAuthorDialog(parent=self)
                te.author.connect(self.setTextCharFormat)
                te.exec_()

                self.setCharFormatSelection()
                self.textCursor().insertText(source.text(), self.textCharFormat)
            elif selectedTextIsBeingDragged:
                self.textCursor().insertHtml(source.html())

            return

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

        super().insertFromMimeData(source)

    def keyPressEvent(self, e):
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

        super().keyPressEvent(e)

    def setCharFormatSelection(self):
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
        # factor = text_area_width / widthv <-
        # width *= factor <-
        # height *= factor

        # print(resource.value())
        # sc_ImageResource = ImageResource.scaledToWidth( <-
        #     math.floor(width), Qt.SmoothTransformation
        # )
        # sc_resource.setDotsPerMeterX(self.DPM);
        # sc_resource.setDotsPerMeterY(self.DPM);

        image_name = f"{uuid}.png"

        # ImageResource.
        ImageResource.save(image_name)

        self.document().addResource(
            QTextDocument.ImageResource, QUrl(image_name), ImageResource
        )

        textImageFormat = QTextImageFormat()
        textImageFormat.setName(image_name)
        if width > text_area_width:
            textImageFormat.setWidth(text_area_width)
        else:
            textImageFormat.setWidth(width)

        # textImageFormat.setHeight(10)

        return textImageFormat
        # return uuid

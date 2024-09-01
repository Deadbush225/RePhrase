from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from rephraser.lib.helper import *
from rephraser.lib.Stores import store
from rephraser.lib.qt_helper import HLine

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

        hline = HLine(parent=self)

        mainlayout.addLayout(author_cont)
        mainlayout.addWidget(self.saveAuthor_btn)
        mainlayout.addWidget(hline)
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

        self.setMinimumWidth(580)

        self.parent_ = parent
        self.textIsSelected = False
        self.dropped_text = None

        self.textCharFormat = QTextCharFormat()

        self.defaultCharFormat = QTextCharFormat()

        self.images = {}
        self.DPM = math.floor(1 * 39.37)

        # print(self.editor.verticalScrollBar().styleSheet())
        self.verticalScrollBar().setStyle(
            QCommonStyle()
        )  # to make the transparency work

        # self.setDisabled(True)

    def dropEvent(self, event):
        m = event.mimeData()
        if m.hasText():
            self.dropped_text = m.text()

        super().dropEvent(event)

    def canInsertFromMimeData(self, source):
        if source.hasImage():
            # print("I CAN INSERT IMAGE")
            # print(self.parent().path)
            # if not os.path.exist(self.parent().path):
            #     self.parent().file_save()

            # # todo: emit a signal indicating that we need to save first
            # if os.path.exists(self.parent().path):
            #     return True

            # return False
            return True
        else:
            return super(TextEdit, self).canInsertFromMimeData(source)

    def insertFromMimeData(self, source):
        print("INSERT FROM MIME DATA")
        cursor = self.textCursor()
        document = self.document()

        if source.hasImage():
            print("I CAN INSERT IMAGE")
            print(self.parent_.path)
            if self.parent_.path is None:
                self.parent_.file_save()

            # recheck after displaying save dialog
            if (self.parent_.path is None) or (not os.path.exists(self.parent_.path)):
                return
                # return True

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
            # self.parent_.update_format()
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
        # maximumImageWidth = self.width() - 32

        # self.removeUnusedResources()

        # resize pictures to match the max width
        # print("TEXT RESIZE EVENT")
        # print(self.images)
        # for uuid in self.images.keys():
        #     print(uuid)
        #     img = self.images[uuid]
        #     # img = QTextImageFormat()
        #     img.setName(uuid)
        #     editorMaxWidth = self.width() - 32
        #     print(f"before: {img.width()} vs. {editorMaxWidth}")

        #     # if img.width() > editorMaxWidth:
        #     print("resizing")
        #     print(f"before: {img.width()} vs. {editorMaxWidth}")
        #     img.setWidth(editorMaxWidth)
        # img.width()

        super().resizeEvent(e)

    def removeUnusedResources(self):
        uuidToRemove = []

        for uuid in self.images.keys():

            resource = self.document().resource(QTextDocument.ImageResource, QUrl(uuid))

            if resource == None:
                uuidToRemove.append(uuid)
                # del self.images[uuid]
                continue

            # self.addImageResource(self.images[uuid])

        for uuid in uuidToRemove:
            del self.images[uuid]

    def addImageResource(self, ImageResource: QImage, uuid=hexuuid()):
        # cases:
        # pasted image: uuid = generated from hash
        # local file draged: uuid = file path
        if uuid == "":
            raise ValueError("provided 'uuid' is empty")

        print("INSERTING IMAGE")

        maximumImageWidth = self.minimumWidth() - 32
        maximumImageHeight = 400 - 32
        print(maximumImageWidth)
        # if width >= maximumImageWidth:
        # conssider padding
        # factor = maximumImageWidth / widthv <-
        # width *= factor <-
        # height *= factor

        # print(resource.value())
        width = ImageResource.width()

        if width > maximumImageWidth:
            print("SCALING TO WIDTH")
            print(f"{width} : {maximumImageWidth}")
            ImageResource = ImageResource.scaledToWidth(
                math.floor(maximumImageWidth), Qt.SmoothTransformation
            )

        height = ImageResource.height()

        if height > maximumImageHeight:
            print("SCALING TO HEIGHT")
            print(f"{height} : {maximumImageHeight}")
            ImageResource = ImageResource.scaledToHeight(
                math.floor(maximumImageHeight), Qt.SmoothTransformation
            )
        # sc_resource.setDotsPerMeterX(self.DPM);
        # sc_resource.setDotsPerMeterY(self.DPM);

        resourcePath = f"{self.parent_.dir}/{self.parent_.baseName}"

        if not os.path.exists(resourcePath):
            os.mkdir(resourcePath)

        image_name = f"{resourcePath}/{uuid}.png"

        # ImageResource.
        ImageResource.save(image_name)

        # textImageFormat = QTextImageFormat()
        # textImageFormat.setName(image_name)
        # if width > maximumImageWidth:
        #     textImageFormat.setWidth(maximumImageWidth)
        # else:
        #     textImageFormat.setWidth(width)

        self.document().addResource(
            QTextDocument.ImageResource, QUrl(image_name), ImageResource
        )

        self.images[image_name] = ImageResource
        # self.images[uuid] = textImageFormat

        return image_name
        # return uuid

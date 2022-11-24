from PyQt5 import QtGui
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QColor, QPainter, QFont, QTextCursor
from PyQt5.QtWidgets import QPlainTextEdit, QWidget


class NumberBar(QWidget):
    def __init__(self, editor, is_show=True):
        QWidget.__init__(self, editor)
        self.editor = editor
        self.editor.blockCountChanged.connect(self.updateWidth)
        self.editor.updateRequest.connect(self.updateContents)
        self.numberBarColor = QColor("#F2F2F2")
        self.is_show = is_show

    def paintEvent(self, event):
        fontsize = self.editor.currentCharFormat().font().pointSize()
        font_=QFont("",fontsize)
        painter = QPainter(self)
        painter.fillRect(event.rect(), self.numberBarColor)
        block = self.editor.firstVisibleBlock()
        while block.isValid():
            blockNumber = block.blockNumber()
            block_top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
            if not block.isVisible() or block_top >= event.rect().bottom():
                break
            if blockNumber == self.editor.textCursor().blockNumber():
                font_.setBold(True)
                painter.setPen(QColor("#000000"))
            else:
                font_.setBold(False)
                painter.setPen(QColor("#717171"))
            painter.setFont(font_)
            paint_rect = QRect(0, block_top, self.width(), self.editor.fontMetrics().height())
            painter.drawText(paint_rect, Qt.AlignRight, str(blockNumber + 1))
            block = block.next()
        painter.end()
        QWidget.paintEvent(self, event)

    def getWidth(self):
        if self.is_show:
            count = self.editor.blockCount()
            fontsize = self.editor.currentCharFormat().font().pointSize()
            font_ = QFont("", fontsize)
            if 0 <= count < 99999:
                width = QtGui.QFontMetrics(font_).width('99999')
            else:
                width = QtGui.QFontMetrics(font_).width(str(count))
            return width + 4
        else:
            return 0

    def updateWidth(self):
        width = self.getWidth()
        self.editor.setViewportMargins(width, 0, 0, 0)

    # 动态更新宽度
    # def updateWidth(self):
    #     width = self.getWidth()
    #     if self.width() != width:
    #         self.setFixedWidth(width)
    #         self.editor.setViewportMargins(width, 0, 0, 0)

    def updateContents(self, rect, scroll):
        if scroll:
            self.scroll(0, scroll)
        else:
            self.update(0, rect.y(), self.width(), rect.height())
        self.updateWidth()


class QReadOnlyEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super(QReadOnlyEditor, self).__init__(parent)
        self.number_bar = NumberBar(self)

    def Init(self, font: QFont = None):
        self.setFont(font)

    def wrap(self):
        self.setLineWrapMode(QPlainTextEdit.WidgetWidth)

    def nowrap(self):
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

    def number_bar_hide(self):
        self.number_bar.is_show = False
        self.number_bar.updateWidth()

    def number_bar_show(self):
        self.number_bar.is_show = True
        self.number_bar.updateWidth()

    def resizeEvent(self, event):
        cr = self.contentsRect()
        rec = QRect(cr.left(), cr.top(), self.number_bar.getWidth(), cr.height())
        self.number_bar.setGeometry(rec)
        QPlainTextEdit.resizeEvent(self, event)

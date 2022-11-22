import hashlib
import os
import traceback
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt, QRect, QWaitCondition, QMutex, QRegExp, QThread
from PyQt5.QtGui import QTextDocument, QTextCharFormat, QTextCursor, QColor, QFont, QPainter, QSyntaxHighlighter
from PyQt5.QtWidgets import QFrame, QMessageBox, QPlainTextEdit, QWidget


class QTextFrame(QFrame):
    def __init__(self, parent=None, *args):
        super().__init__(parent)
        Form=self
        Form.setObjectName("Form")
        Form.resize(792, 521)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.preview = QReadOnlyEditor(self.frame)
        self.preview.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.preview.setFrameShadow(QtWidgets.QFrame.Plain)
        self.preview.setObjectName("preview")
        self.verticalLayout_2.addWidget(self.preview)
        self.frame_14 = QtWidgets.QFrame(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.frame_14.sizePolicy().hasHeightForWidth())
        self.frame_14.setSizePolicy(sizePolicy)
        self.frame_14.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_14.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frame_14.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_14.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_14.setObjectName("frame_14")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frame_14)
        self.horizontalLayout_9.setContentsMargins(8, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.linenumber = QtWidgets.QCheckBox(self.frame_14)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.linenumber.sizePolicy().hasHeightForWidth())
        self.linenumber.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.linenumber.setFont(font)
        self.linenumber.setChecked(True)
        self.linenumber.setObjectName("linenumber")
        self.horizontalLayout_9.addWidget(self.linenumber)
        self.linewrap = QtWidgets.QCheckBox(self.frame_14)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.linewrap.sizePolicy().hasHeightForWidth())
        self.linewrap.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.linewrap.setFont(font)
        self.linewrap.setChecked(True)
        self.linewrap.setObjectName("linewrap")
        self.horizontalLayout_9.addWidget(self.linewrap)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem)
        self.cursor = QtWidgets.QLabel(self.frame_14)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cursor.sizePolicy().hasHeightForWidth())
        self.cursor.setSizePolicy(sizePolicy)
        self.cursor.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cursor.setFont(font)
        self.cursor.setObjectName("cursor")
        self.horizontalLayout_9.addWidget(self.cursor)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem1)
        self.keywords = QtWidgets.QLineEdit(self.frame_14)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.keywords.sizePolicy().hasHeightForWidth())
        self.keywords.setSizePolicy(sizePolicy)
        self.keywords.setMinimumSize(QtCore.QSize(150, 0))
        self.keywords.setMaximumSize(QtCore.QSize(300, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.keywords.setFont(font)
        self.keywords.setStyleSheet("border-color: rgb(160, 160, 160);\n"
                                    "")
        self.keywords.setFrame(True)
        self.keywords.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.keywords.setObjectName("keywords")
        self.horizontalLayout_9.addWidget(self.keywords)
        self.result = QtWidgets.QLabel(self.frame_14)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(16)
        sizePolicy.setHeightForWidth(self.result.sizePolicy().hasHeightForWidth())
        self.result.setSizePolicy(sizePolicy)
        self.result.setMinimumSize(QtCore.QSize(140, 16))
        self.result.setMaximumSize(QtCore.QSize(16777215, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.result.setFont(font)
        self.result.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.result.setAlignment(QtCore.Qt.AlignCenter)
        self.result.setObjectName("result")
        self.horizontalLayout_9.addWidget(self.result)
        self.prev = QtWidgets.QPushButton(self.frame_14)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.prev.sizePolicy().hasHeightForWidth())
        self.prev.setSizePolicy(sizePolicy)
        self.prev.setMinimumSize(QtCore.QSize(70, 0))
        self.prev.setMaximumSize(QtCore.QSize(70, 1666666))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.prev.setFont(font)
        self.prev.setAutoDefault(True)
        self.prev.setDefault(False)
        self.prev.setFlat(False)
        self.prev.setObjectName("prev")
        self.horizontalLayout_9.addWidget(self.prev)
        self.next = QtWidgets.QPushButton(self.frame_14)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.next.sizePolicy().hasHeightForWidth())
        self.next.setSizePolicy(sizePolicy)
        self.next.setMinimumSize(QtCore.QSize(0, 19))
        self.next.setMaximumSize(QtCore.QSize(70, 1122222))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.next.setFont(font)
        self.next.setAutoDefault(True)
        self.next.setObjectName("next")
        self.horizontalLayout_9.addWidget(self.next, 0, QtCore.Qt.AlignRight)
        self.verticalLayout_2.addWidget(self.frame_14)
        self.horizontalLayout.addWidget(self.frame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.linenumber.setText(_translate("Form", "显示行号"))
        self.linewrap.setText(_translate("Form", "自动换行"))
        self.cursor.setText(_translate("Form", "第1行,第1列"))
        self.keywords.setPlaceholderText(_translate("Form", "请输入关键词，回车"))
        self.result.setText(_translate("Form", "0/0"))
        self.prev.setText(_translate("Form", "上一个"))
        self.next.setText(_translate("Form", "下一个"))

        self.__init2__()

    def __init2__(self):
        self.search_running = False
        self.result_text = '{0} 个结果'
        self.result_position_text = '{0}/{1}'
        self.textCursor = self.preview.textCursor()

        self.preview.setReadOnly(True)
        self.preview.wrap()

        # I wrote this code because color of default selection doesn't stand out in the white textedit screen.
        self.preview.setStyleSheet('QReadOnlyEditor { selection-background-color: #A0D2FF; }')
        self.result.setText(self.result_text.format(0))
        self.linenumber.stateChanged.connect(self.CheckBoxLineNumber)
        self.linewrap.stateChanged.connect(self.CheckBoxLineWrap)
        self.keywords.returnPressed.connect(self.Search)
        self.preview.cursorPositionChanged.connect(lambda: self.cursor.setText(
            "第%d行,第%d列" % (self.preview.textCursor().blockNumber() + 1, self.preview.textCursor().positionInBlock())))
        self.prev.clicked.connect(self.onClickPrev)
        self.next.clicked.connect(self.onClickNext)

        self.CursorsInit()
        self.ButtonToggled(False)

    def CheckBoxLineWrap(self):
        if self.linewrap.isChecked():
            self.preview.wrap()
        else:
            self.preview.nowrap()

    def CheckBoxLineNumber(self):
        if self.linenumber.isChecked():
            self.preview.number_bar_show()
        else:
            self.preview.number_bar_hide()

    def Search(self, Loading=False, CurPath=None, FilePath=None, IsError=False, Keywords=None):
        self.setEnabled(False)
        if Keywords is None:
            if self.keywords.text().strip() == "":
                QMessageBox.information(self, '注意', '关键词不允许为空或者全是空格', QMessageBox.Ok)
                return
        else:
            if Keywords.strip() == "":
                QMessageBox.information(self, '注意', '关键词不允许为空或者全是空格', QMessageBox.Ok)
                return

        if not self.search_running:
            self.CursorsInit()
            if Loading:
                self.search_running = True
                self.keywords.setText(Keywords)
                self.HighLight = KeywordsHighlighter(parent=self.preview.document(), keywords=self.keywords.text(),
                                                     cursors=self.cursors)
                self.load_text_thread = LoadTextThread(FilePath=FilePath, CurPath=CurPath, IsError=IsError)
                self.load_text_thread.complete.connect(self.SearchComplete)
                self.load_text_thread.start()
            else:
                self.search_running = True
                self.HighLight = KeywordsHighlighter(parent=self.preview.document(), keywords=self.keywords.text(),
                                                     cursors=self.cursors)
                self.HighLight.rehighlight()
                self.SearchComplete()
        else:
            if Loading:
                reply = QMessageBox.information(self, '注意', '请等待当前加载完成', QMessageBox.Ok)
                # if reply == QMessageBox.Yes:
                #     self.load_text_thread.terminate()
                #     self.search_running = False
            else:
                reply = QMessageBox.information(self, '注意', '请等待当前搜索完成', QMessageBox.Ok)

    def SearchComplete(self, txt=None):
        if txt is not None:
            self.preview.setPlainText(txt)
        self.preview.moveCursor(QTextCursor.Start)
        self.result.setText(self.result_text.format(len(self.cursors)))
        if len(self.cursors) > 0:
            self.ButtonToggled(True)
        else:
            self.ButtonToggled(False)
        self.search_running = False
        try:
            self.load_text_thread.resume()
        except:
            pass
        self.setEnabled(True)

    def ButtonToggled(self, flag=True):
        self.prev.setEnabled(flag)
        self.next.setEnabled(flag)

    def CursorsInit(self):
        self.cursors = []
        self.cursors_id = -1

    def onClickPrev(self):
        cur = self.preview.textCursor()
        cur_ = self.preview.document().find(QRegExp(r'%s' % self.keywords.text()), cur, QTextDocument.FindBackward)
        anchor = cur_.anchor()
        position = cur_.position()
        if anchor == -1:
            QMessageBox.information(self, '注意', '已经处于文件开头。')
        else:
            cur_.setPosition(anchor, QTextCursor.MoveAnchor)
            cur_.setPosition(position, QTextCursor.KeepAnchor)
            cur_.selectedText()
            self.preview.setTextCursor(cur_)
            self.preview.ensureCursorVisible()
            self.result.setText(self.result_position_text.format(self.cursors.index(anchor), len(self.cursors)))

    def onClickNext(self):
        cur = self.preview.textCursor()
        cur_ = self.preview.document().find(QRegExp(r'%s' % self.keywords.text()), cur)
        anchor = cur_.anchor()
        position = cur_.position()
        if anchor == -1:
            QMessageBox.information(self, '注意', '已经处于文件结尾。')
        else:
            cur_.setPosition(anchor, QTextCursor.MoveAnchor)
            cur_.setPosition(position, QTextCursor.KeepAnchor)
            cur_.selectedText()
            self.preview.setTextCursor(cur_)
            self.preview.ensureCursorVisible()
            self.result.setText(self.result_position_text.format(self.cursors.index(anchor) + 1 , len(self.cursors)))

    '''-----------------------------------外部调用-----------------------------------------------'''

    def setReadOnly(self, Flag: bool):
        self.preview.setReadOnly(Flag)

    def zoomIn(self, i: int):
        self.preview.zoomIn(i)

    def clear(self):
        self.preview.clear()


class KeywordsHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None, keywords: str = None, cursors: list = None):
        super(KeywordsHighlighter, self).__init__(parent)
        self.keywords = keywords
        self.highlightingRules = []
        self.cursors = cursors
        KeywordsFormat = QTextCharFormat()
        KeywordsFormat.setFontWeight(QFont.Bold)
        KeywordsFormat.setForeground(QColor("red"))
        self.highlightingRules.append((QRegExp(r'%s' % self.keywords), KeywordsFormat))

    def highlightBlock(self, text):
        position_ = self.currentBlock().position()
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                self.cursors.append(position_ + index)
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)


class NumberBar(QWidget):
    def __init__(self, editor, font):
        QWidget.__init__(self, editor)
        self.editor = editor
        self.editor.blockCountChanged.connect(self.updateWidth)
        self.editor.updateRequest.connect(self.updateContents)
        self.numberBarColor = QColor("#F2F2F2")
        self.font = font
        self.first = True

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(event.rect(), self.numberBarColor)
        block = self.editor.firstVisibleBlock()
        while block.isValid():
            blockNumber = block.blockNumber()
            block_top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
            if not block.isVisible() or block_top >= event.rect().bottom():
                break
            if blockNumber == self.editor.textCursor().blockNumber():
                self.font.setBold(True)
                painter.setPen(QColor("#000000"))
            else:
                self.font.setBold(False)
                painter.setPen(QColor("#717171"))
            painter.setFont(self.font)
            paint_rect = QRect(0, block_top, self.width(), self.editor.fontMetrics().height())
            painter.drawText(paint_rect, Qt.AlignRight, str(blockNumber + 1))
            block = block.next()
        painter.end()
        QWidget.paintEvent(self, event)

    def getWidth(self):
        count = self.editor.blockCount()
        if 0 <= count < 99999:
            width = self.fontMetrics().width('999999')
        else:
            width = self.fontMetrics().width(str(count))
        return width + 4

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
        if rect.contains(self.editor.viewport().rect()):
            self.editor_fontSize = self.editor.currentCharFormat().font().pointSize()
            if self.first:
                self.editor_fontSize = self.font.pointSize()
            self.font.setPointSize(self.editor_fontSize)
            self.font.setStyle(QFont.StyleNormal)
            self.updateWidth()

    def update_(self, editor_fontSize):
        self.editor_fontSize = editor_fontSize
        self.font.setPointSize(self.editor_fontSize)
        self.font.setStyle(QFont.StyleNormal)
        self.updateWidth()


class QReadOnlyEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super(QReadOnlyEditor, self).__init__(parent)
        self.setFont(QFont("", 10))
        self.number_bar = NumberBar(self, self.font())

    def wrap(self):
        self.setLineWrapMode(QPlainTextEdit.WidgetWidth)

    def nowrap(self):
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

    def number_bar_hide(self):
        self.number_bar.hide()

    def number_bar_show(self):
        self.number_bar.show()

    def resizeEvent(self, e):
        cr = self.contentsRect()
        rec = QRect(cr.left(), cr.top(), self.number_bar.getWidth(), cr.height())
        self.number_bar.setGeometry(rec)
        QPlainTextEdit.resizeEvent(self, e)

    def setHtml(self, p_str):
        QPlainTextEdit.clear(self)
        self.textCursor().insertHtml(p_str)
        self.moveCursor(QTextCursor.Start)
        self.number_bar.update_(self.currentCharFormat().font().pointSize())


class LoadTextThread(QThread):
    complete = pyqtSignal(str)

    def __init__(self, FilePath, CurPath, IsError):
        super().__init__()
        self.mutex = QMutex()
        self.cond = QWaitCondition()
        self.FilePath = FilePath
        self.CurPath = CurPath
        self.IsError = IsError

    def run(self):
        self.mutex.lock()
        try:
            with open(self.FilePath, 'rb') as f:
                file_path_md5 = hashlib.md5(f.read()).hexdigest()
            temp_md5_path=os.path.abspath(os.path.join(self.CurPath, ".temp", file_path_md5))
            error_temp_md5_path =os.path.abspath(os.path.join(self.CurPath, ".errortemp", file_path_md5))
            if self.IsError or not os.path.isfile(temp_md5_path):
                path = error_temp_md5_path
            else:
                path = temp_md5_path

            with open(path, "r", encoding="utf8") as f:
                txt = f.read()
        except:
            txt = self.FilePath + "：加载失败。\n" + traceback.format_exc()
        self.complete.emit(txt)
        self.cond.wait(self.mutex)
        self.mutex.unlock()

    def resume(self):
        self.cond.wakeAll()

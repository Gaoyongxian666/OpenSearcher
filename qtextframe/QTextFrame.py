import hashlib
import os
import traceback
from PyQt5.QtCore import pyqtSignal, Qt, QRect, QWaitCondition, QMutex, QRegExp, QThread
from PyQt5.QtGui import QTextDocument, QTextCharFormat, QTextCursor, QColor, QFont, QPainter, QSyntaxHighlighter
from PyQt5.QtWidgets import QFrame, QMessageBox, QPlainTextEdit, QWidget

from qtextframe import QText


class QTextFrame(QFrame):
    def __init__(self, parent=None, *args):
        super().__init__(parent)
        self.child = QText.Ui_Form()
        self.child.setupUi(self)

    def Init(self, fontsize: int, fontfamily: str, linewrap: bool, linenumber: bool, mysetting_dict):
        self.search_running = False
        self.result_text = '{0} 个结果'
        self.result_position_text = '{0}/{1}'
        self.fontsize = fontsize
        self.fontfamily = fontfamily
        self.mysetting_dict = mysetting_dict
        self.font_ = QFont(self.fontfamily, self.fontsize)

        self.child.preview.Init(self.font_)
        self.child.fontComboBox.setCurrentFont(self.font_)
        self.child.linewrap.setChecked(linewrap)
        self.SetCheckBoxLineNumber(linenumber)
        self.child.linenumber.setChecked(linenumber)
        self.SetCheckBoxLineWrap(linewrap)

        self.textCursor = self.child.preview.textCursor()
        self.child.preview.setReadOnly(True)

        # I wrote this code because color of default selection doesn't stand out in the white textedit screen.
        self.child.preview.setStyleSheet('QReadOnlyEditor { selection-background-color: #A0D2FF; }')
        self.child.result.setText(self.result_text.format(0))
        self.child.linenumber.stateChanged.connect(self.CheckBoxLineNumber)
        self.child.linewrap.stateChanged.connect(self.CheckBoxLineWrap)
        self.child.fontComboBox.currentFontChanged.connect(self.FontChange)
        self.child.keywords.returnPressed.connect(self.Search)
        self.child.preview.cursorPositionChanged.connect(lambda: self.child.cursor.setText(
            "第%d行,第%d列" % (
                self.child.preview.textCursor().blockNumber() + 1, self.child.preview.textCursor().positionInBlock())))
        self.child.prev.clicked.connect(self.onClickPrev)
        self.child.next.clicked.connect(self.onClickNext)

        self.CursorsInit()
        self.ButtonToggled(False)

    def FontChange(self, font: QFont):
        self.fontfamily = font.family()
        self.mysetting_dict["_fontfamily"] = self.fontfamily
        font.setPointSize(self.fontsize)
        self.child.preview.setFont(font)

    def SetCheckBoxLineNumber(self,f):
        if f:
            self.child.preview.number_bar_show()
        else:
            self.child.preview.number_bar_hide()

    def SetCheckBoxLineWrap(self,f):
        if f:
            self.child.preview.wrap()
        else:
            self.child.preview.nowrap()

    def CheckBoxLineWrap(self):
        if self.child.linewrap.isChecked():
            self.child.preview.wrap()
        else:
            self.child.preview.nowrap()
        self.mysetting_dict["_linewrap"] = self.child.linewrap.isChecked()

    def CheckBoxLineNumber(self):
        if self.child.linenumber.isChecked():
            self.child.preview.number_bar_show()
        else:
            self.child.preview.number_bar_hide()
        self.mysetting_dict["_linenumber"] = self.child.linenumber.isChecked()

    def Search(self, Loading=False, CurPath=None, FilePath=None, IsError=False, Keywords=None):
        self.setEnabled(False)
        if Keywords is None:
            if self.child.keywords.text().strip() == "":
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
                self.child.keywords.setText(Keywords)
                self.HighLight = KeywordsHighlighter(parent=self.child.preview.document(),
                                                     keywords=self.child.keywords.text(),
                                                     cursors=self.cursors)
                self.load_text_thread = LoadTextThread(FilePath=FilePath, CurPath=CurPath, IsError=IsError)
                self.load_text_thread.complete.connect(self.SearchComplete)
                self.load_text_thread.start()
            else:
                self.search_running = True
                self.HighLight = KeywordsHighlighter(parent=self.child.preview.document(),
                                                     keywords=self.child.keywords.text(),
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
            self.child.preview.setPlainText(txt)
        self.child.preview.moveCursor(QTextCursor.Start)
        self.child.result.setText(self.result_text.format(len(self.cursors)))
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
        self.child.prev.setEnabled(flag)
        self.child.next.setEnabled(flag)

    def CursorsInit(self):
        self.cursors = []
        self.cursors_id = -1

    def onClickPrev(self):
        cur = self.child.preview.textCursor()
        cur_ = self.child.preview.document().find(QRegExp(r'%s' % self.child.keywords.text()), cur,
                                                  QTextDocument.FindBackward)
        anchor = cur_.anchor()
        position = cur_.position()
        if anchor == -1:
            QMessageBox.information(self, '注意', '已经处于文件开头。')
        else:
            cur_.setPosition(anchor, QTextCursor.MoveAnchor)
            cur_.setPosition(position, QTextCursor.KeepAnchor)
            cur_.selectedText()
            self.child.preview.setTextCursor(cur_)
            self.child.preview.ensureCursorVisible()
            self.child.result.setText(self.result_position_text.format(self.cursors.index(anchor), len(self.cursors)))

    def onClickNext(self):
        cur = self.child.preview.textCursor()
        cur_ = self.child.preview.document().find(QRegExp(r'%s' % self.child.keywords.text()), cur)
        anchor = cur_.anchor()
        position = cur_.position()
        if anchor == -1:
            QMessageBox.information(self, '注意', '已经处于文件结尾。')
        else:
            cur_.setPosition(anchor, QTextCursor.MoveAnchor)
            cur_.setPosition(position, QTextCursor.KeepAnchor)
            cur_.selectedText()
            self.child.preview.setTextCursor(cur_)
            self.child.preview.ensureCursorVisible()
            self.child.result.setText(
                self.result_position_text.format(self.cursors.index(anchor) + 1, len(self.cursors)))

    '''-----------------------------------外部调用-----------------------------------------------'''

    def setReadOnly(self, Flag: bool):
        self.child.preview.setReadOnly(Flag)

    def zoomIn(self, i: int):
        self.fontsize = self.fontsize + i
        print(self.fontsize)
        print(self.child.preview.font().pointSize())
        print("---------------------------------------------------")
        self.child.preview.zoomIn(i)
        print(self.child.preview.font().pointSize())
        self.mysetting_dict["_fontsize"] = self.child.preview.font().pointSize()

    def clear(self):
        self.child.preview.clear()


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
            temp_md5_path = os.path.abspath(os.path.join(self.CurPath, ".temp", file_path_md5))
            error_temp_md5_path = os.path.abspath(os.path.join(self.CurPath, ".errortemp", file_path_md5))
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

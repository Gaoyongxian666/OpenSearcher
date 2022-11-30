import os.path
import sys

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from qcustomdialog import help


class HelpWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.child = help.Ui_MainWindow()
        self.child.setupUi(self)

        self.file = parent.HelpPath
        self.setWindowTitle("使用说明")
        self.child.pushButton.clicked.connect(self.openfile)
        self.child.lineEdit.setText(self.file)

        self.RelayUpdate()

    def RelayUpdate(self):
        """耗时操作"""
        self.relay_thread = RelayUpdateThread(self.file)
        self.relay_thread.complete.connect(lambda i: self.child.textBrowser.setMarkdown(i))
        self.relay_thread.start()

    def openfile(self):
        filepath = QFileDialog.getOpenFileName(self, "打开文件", "", "文本类型(*.txt;*.md;*.html;*.py);")[0]
        self.child.lineEdit.setText(filepath)
        relay_thread = RelayUpdateThread(filepath)
        relay_thread.complete.connect(lambda i: self.child.textBrowser.setMarkdown(i))
        relay_thread.start()


class RelayUpdateThread(QThread):
    complete = pyqtSignal(str)

    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath

    def run(self):
        try:
            with open(self.filepath, encoding='utf-8') as f:
                text_list = f.readlines()
                DirPath = os.path.abspath(os.path.dirname(os.path.abspath(sys.argv[0])))
                txt = ""
                for paragraph_text in text_list:
                    if "(./" in paragraph_text:
                        paragraph_text_list = paragraph_text.split("(./")
                    elif "(.\\" in paragraph_text:
                        paragraph_text_list = paragraph_text.split("(.\\")
                    icon_path = os.path.abspath(os.path.join(DirPath, paragraph_text_list[-1].strip().strip(")")))
                    paragraph_text = paragraph_text_list[0] + "(\"" + icon_path + "\")"
                    txt = "".join((txt, paragraph_text, "\n"))
        except:
            with open(self.filepath, encoding='utf-8') as f:
                txt = f.read()
        self.complete.emit(txt)

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
        with open(self.filepath, encoding='utf-8') as f:
            self.text = f.read()
            self.complete.emit(self.text)

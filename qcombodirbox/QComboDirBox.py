import logging
import os.path
import traceback

import psutil
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QComboBox, QLineEdit, QMessageBox, QFileDialog, QListView
from PyQt5 import QtWidgets, QtCore
import sys

logger = logging.getLogger(__name__)


class ClickableLineEdit(QLineEdit):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        else:
            super().mousePressEvent(event)


class QComboDirBox(QComboBox):
    def __init__(self, parent=None):
        super(QComboDirBox, self).__init__(parent)
        self.device_list = []
        self.IconDir = os.path.join(os.path.dirname(sys.argv[0]), "icon")

        self.qLineEdit = ClickableLineEdit()
        self.qLineEdit.setReadOnly(True)


        self.setLineEdit(self.qLineEdit)
        self.qListView = QListView()
        self.setView(self.qListView)

        # self.setStyleSheet('''
        # QAbstractItemView::item {height: 50px;}''')
        # self.setContentsMargins(30,0,0,0)
        # self.qLineEdit.ma(30,0,0,0)
        # self.qListView.setStyleSheet("margin-left: 5px;")

        self.textActivated.connect(self.change)

        self.Init()
        self.setStyleSheet('''
                QComboDirBox { padding-left: 8px; }
                QListView {margin-left: 5px;}
                QListView::item {height:27px;}''')

    def Init(self):
        try:
            for i in psutil.disk_partitions():
                self.device_list.append(i.device)
            if len(self.device_list) == 0:
                raise RuntimeWarning("磁盘读取为空")
            self.addItem(QIcon(os.path.abspath(os.path.join(self.IconDir, "computer.png"))), "全部目录")
            for i in self.device_list:
                self.addItem(QIcon(os.path.abspath(os.path.join(self.IconDir, "disk.png"))), i)
            self.addItem(QIcon(os.path.abspath(os.path.join(self.IconDir, "folder.png"))), "自定义目录")
        except:
            QMessageBox.information(self, "提示", "磁盘读取失败！请自行选择文件夹！\n\n" + traceback.format_exc(), QMessageBox.Ok)
            self.addItem(QIcon(os.path.abspath(os.path.join(self.IconDir, "folder.png"))), "请选择目录")
            self.qLineEdit.clicked.connect(self.onClickedOpenFileDialog)

    def onClickedOpenFileDialog(self):
        self.DirPath = QFileDialog.getExistingDirectory(self, '选择文件夹', os.path.dirname(self.IconDir))
        print(self.DirPath)
        if self.DirPath != "":
            self.qLineEdit.setText(os.path.abspath(self.DirPath))

    def change(self):
        if self.currentText() == "自定义目录":
            self.qLineEdit.setText("")
            self.onClickedOpenFileDialog()

    def text(self):
        return self.qLineEdit.text()

    def get_devices(self):
        logger.info("获取目录：" + str(self.device_list))
        return self.device_list


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    Form.IconDir = os.path.join(os.path.dirname(sys.argv[0]), "icon")
    comboBox1 = QComboDirBox(Form)

    comboBox1.setGeometry(QtCore.QRect(10, 10, 400, 40))
    comboBox1.setMinimumSize(QtCore.QSize(100, 20))
    Form.show()
    sys.exit(app.exec_())

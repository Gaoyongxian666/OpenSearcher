import os
import traceback

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QListView, QAbstractItemView, QMessageBox
from qutils.util import setClipboardFiles


class QFileListView(QListView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.listModel = QStandardItemModel()
        self.setModel(self.listModel)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.ListViewContextMenu)
        self.doubleClicked.connect(self.onDoubleClickedListViewOpenFile)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

    def onDoubleClickedListViewOpenFile(self):
        table_row = self.currentIndex().row()
        if table_row == -1:
            QMessageBox.information(self, '注意', '请先选中一项！', QMessageBox.Yes)
            return
        _item = self.listModel.item(table_row, 0)
        file_path = _item.text().split("-> (")[1][:-1]
        try:
            os.startfile(file_path)
        except:
            QMessageBox.information(self, '打开失败', traceback.format_exc(), QMessageBox.Ok)

    def ListViewContextMenu(self):
        if self.listModel.rowCount() > 0:
            menu = QtWidgets.QMenu()
            open = menu.addAction("打开")
            open.triggered.connect(self.onDoubleClickedListViewOpenFile)
            copy = menu.addAction("复制")
            copy.triggered.connect(self.ListViewCopyFile)
            open_dir = menu.addAction("打开文件所在位置")
            open_dir.triggered.connect(self.ListViewOpenDir)
            cursor = QtGui.QCursor()
            menu.exec_(cursor.pos())

    def ListViewCopyFile(self):
        table_row = self.currentIndex().row()
        if table_row == -1:
            QMessageBox.information(self, '注意', '请先选中一项！', QMessageBox.Yes)
            return
        _item = self.listModel.item(table_row, 0)
        file_path = _item.text().split("-> (")[1][:-1]
        setClipboardFiles([file_path])

    def ListViewOpenDir(self):
        table_row = self.currentIndex().row()
        if table_row == -1:
            QMessageBox.information(self, '注意', '请先选中一项！', QMessageBox.Yes)
            return
        _item = self.listModel.item(table_row, 0)
        file_path = _item.text().split("-> (")[1][:-1]
        dir_path = os.path.abspath(os.path.dirname(file_path))
        try:
            os.startfile(dir_path)
        except:
            QMessageBox.information(self, '打开失败', traceback.format_exc(), QMessageBox.Ok)

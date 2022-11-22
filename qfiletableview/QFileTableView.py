import os

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QMessageBox

from qutils.util import setClipboardFiles


class QFileTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置表格选择整行
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可编辑
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)  # 垂直表头缺省
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableModel = FileModel(data=[], header=['文件名', '大小', '修改时间', '路径', '类型'])  # 设置model
        self.setModel(self.tableModel)
        self.setColumnWidth(0, 200)
        self.setColumnWidth(1, 75)
        self.setColumnWidth(2, 150)
        self.setColumnWidth(3, 700)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.TableViewContextMenu)
        self.doubleClicked.connect(self.onDoubleClickedTableViewOpenFile)

    def onDoubleClickedTableViewOpenFile(self):
        table_row = self.currentIndex().row()
        if table_row == -1:
            QMessageBox.information(self, '注意', '请先选中一项！', QMessageBox.Yes)
            return
        _index = self.tableModel.index(table_row, 3, QModelIndex())
        file_path = (str(_index.data()))
        os.startfile(file_path)

    def TableViewContextMenu(self):
        if self.tableModel.rowCount() > 0:
            menu = QtWidgets.QMenu()
            open = menu.addAction("打开")
            open.triggered.connect(self.onDoubleClickedTableViewOpenFile)
            copy = menu.addAction("复制")
            copy.triggered.connect(self.TableViewCopyFile)
            open_dir = menu.addAction("打开文件所在位置")
            open_dir.triggered.connect(self.TableViewOpenDir)
            cursor = QtGui.QCursor()
            menu.exec_(cursor.pos())

    def TableViewCopyFile(self):
        table_row = self.currentIndex().row()
        if table_row == -1:
            QMessageBox.information(self, '注意', '请先选中一项！', QMessageBox.Yes)
            return
        _index = self.tableModel.index(table_row, 3, QModelIndex())
        file_path = (str(_index.data()))
        setClipboardFiles([file_path])

    def TableViewOpenDir(self):
        table_row = self.currentIndex().row()
        if table_row == -1:
            QMessageBox.information(self, '注意', '请先选中一项！', QMessageBox.Yes)
            return
        _index = self.tableModel.index(table_row, 3, QModelIndex())
        file_path = (str(_index.data()))
        dir_path = os.path.abspath(os.path.dirname(file_path))
        os.startfile(dir_path)


class FileModel(QAbstractTableModel):
    def __init__(self, data, header, *args, **kwargs):
        super(FileModel, self).__init__()
        self.datalist = data
        self.header = header

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.datalist)

    def columnCount(self, parent=None, *args, **kwargs):
        # 会导致没数据不显示
        # if len(self.datalist) > 0:
        #     return len(self.datalist[0])
        # return 0
        return len(self.header)

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DecorationRole:
            return self.datalist[index.row()][index.column()][0]
        elif role == Qt.DisplayRole:
            return self.datalist[index.row()][index.column()][1]
        return None

    # 理解role
    # def data(self, index, role=Qt.DisplayRole):
    #         if not index.isValid():
    #             return None
    #         if role == Qt.DisplayRole or role == Qt.DecorationRole:
    #             return self.datalist[index.row()][index.column()]
    #         else:
    #             return None
    #         # return self.datalist[index.row()][index.column()]

    def headerData(self, col, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

    def append_data(self, x):
        self.datalist.append(x)
        self.layoutChanged.emit()

    def remove_row(self, row):
        self.datalist.pop(row)
        self.layoutChanged.emit()

    def remove_all(self):
        self.datalist.clear()
        self.layoutChanged.emit()

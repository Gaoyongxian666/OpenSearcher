import os
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QAbstractItemView
from qcustomdialog import index, file


class FileWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.child = file.Ui_MainWindow()
        self.child.setupUi(self)
        self.setWindowTitle("常用目录")

        self.CurPath = parent.CurPath
        self.IconDir = parent.IconDir
        self.mysetting_dict = parent.mysetting_dict
        self.queue = parent.queue

        self.child.ok.clicked.connect(self.onClickedOk)
        self.child.delete_2.clicked.connect(self.onClickedDel)
        self.child.create.clicked.connect(self.onClickedCreate)

        self.listModel = QStandardItemModel()
        self.child.listView.setModel(self.listModel)
        self.child.listView.doubleClicked.connect(self.onClickedOk)
        self.child.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.Init()

    def addItem(self, dir_path):
        item = QStandardItem(QIcon(os.path.abspath(os.path.join(self.IconDir, "folder.png"))), dir_path)
        self.listModel.appendRow(item)

    def Init(self):
        _common_dir = self.mysetting_dict["_common_dir"]
        for dir in _common_dir:
            self.addItem(dir)

    def onClickedOk(self):
        table_row = self.child.listView.currentIndex().row()
        if table_row == -1:
            QMessageBox.information(self, '注意', '请先选中一项！', QMessageBox.Yes)
            return
        _item = self.listModel.item(table_row, 0)
        file_path = _item.text()
        self.queue.put(("_common_dir", file_path))
        self.close()

    def onClickedDel(self):
        selected = self.child.listView.selectedIndexes()
        if len(selected) > 0:
            _common_dir = self.mysetting_dict["_common_dir"]
            for i in selected:
                table_row = i.row()
                _item = self.listModel.item(table_row, 0)
                file_path = _item.text()
                self.listModel.removeRow(table_row)
                _common_dir.remove(file_path)
            self.mysetting_dict["_common_dir"] = _common_dir
        else:
            QMessageBox.information(self, '注意', '请先选中一项！', QMessageBox.Yes)

    def onClickedCreate(self):
        _common_dir = self.mysetting_dict["_common_dir"]
        dir_path = QFileDialog.getExistingDirectory(self, '选择文件夹', self.CurPath)
        if dir_path in _common_dir:
            QMessageBox.information(self, "提示", "此文件夹已经存在！", QMessageBox.Ok)
        elif dir_path.strip() == "":
            QMessageBox.information(self, "提示", "没有选择文件夹！", QMessageBox.Ok)
        else:
            self.addItem(dir_path)
            _common_dir.append(dir_path)
            self.mysetting_dict["_common_dir"] = _common_dir

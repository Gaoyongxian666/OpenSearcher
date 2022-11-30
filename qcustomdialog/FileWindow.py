import os
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QAbstractItemView
from qcustomdialog import file
from qutils.util import getparentlist, getsublist


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

        self.child.ok_common.clicked.connect(self.onClickedOk)
        self.child.delete_common.clicked.connect(self.onClickedDel)
        self.child.create_common.clicked.connect(self.onClickedCreate)

        self.child.delete_exclude.clicked.connect(self.onClickedDelExclude)
        self.child.create_exclude.clicked.connect(self.onClickedCreateExclude)

        self.listModel_common = QStandardItemModel()
        self.child.listView_common.setModel(self.listModel_common)
        self.child.listView_common.doubleClicked.connect(self.onClickedOk)
        self.child.listView_common.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.child.listView_common.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.listModel_exclude = QStandardItemModel()
        self.child.listView_exclude.setModel(self.listModel_exclude)
        self.child.listView_exclude.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.Init()

    def AddCommonDirItem(self, dir_path):
        item = QStandardItem(QIcon(os.path.abspath(os.path.join(self.IconDir, "folder.png"))), dir_path)
        self.listModel_common.appendRow(item)

    def AddExcludeDirItem(self, dir_path):
        item = QStandardItem(QIcon(os.path.abspath(os.path.join(self.IconDir, "folder.png"))), dir_path)
        self.listModel_exclude.appendRow(item)

    def Init(self):
        _common_dir = self.mysetting_dict["_common_dir"]
        _exclude_dir = self.mysetting_dict["_exclude_dir"]

        for dir in _common_dir:
            self.AddCommonDirItem(dir)
        for dir in _exclude_dir:
            self.AddExcludeDirItem(dir)

    def onClickedOk(self):
        selected = self.child.listView_common.selectedIndexes()
        if len(selected) > 0:
            dirs_list = []
            for i in selected:
                table_row = i.row()
                _item = self.listModel_common.item(table_row, 0)
                dir_path = _item.text()
                dirs_list.append(dir_path)
            self.queue.put(("_common_dir", "|".join(dirs_list)))
            self.close()
        else:
            QMessageBox.information(self, '注意', '请至少选中一项！', QMessageBox.Yes)

    def onClickedCreate(self):
        _common_dir = self.mysetting_dict["_common_dir"]
        dir_path = QFileDialog.getExistingDirectory(self, '选择文件夹', self.CurPath)
        if dir_path.strip() == "":
            QMessageBox.information(self, "提示", "没有选择文件夹！", QMessageBox.Ok)
        else:
            dir_path = os.path.abspath(dir_path)
            parentlist = getparentlist(dir_path, _common_dir)
            sublist = getsublist(dir_path, _common_dir)
            if dir_path in _common_dir:
                QMessageBox.information(self, "提示", "此文件夹已经存在！", QMessageBox.Ok)
            elif len(parentlist) > 0:
                QMessageBox.information(self, "提示", "此文件夹已经包含！\n" + "\n".join(parentlist), QMessageBox.Ok)
            elif len(sublist) > 0:
                QMessageBox.information(self, "提示", "请先删除此文件夹下的子目录！\n" + "\n".join(sublist), QMessageBox.Ok)
            else:
                self.AddCommonDirItem(dir_path)
                _common_dir.append(dir_path)
                self.mysetting_dict["_common_dir"] = _common_dir

    def onClickedCreateExclude(self):
        _exclude_dir = self.mysetting_dict["_exclude_dir"]
        dir_path = QFileDialog.getExistingDirectory(self, '选择文件夹', self.CurPath)
        if dir_path.strip() == "":
            QMessageBox.information(self, "提示", "没有选择文件夹！", QMessageBox.Ok)
        else:
            dir_path = os.path.abspath(dir_path)
            parentlist = getparentlist(dir_path, _exclude_dir)
            sublist = getsublist(dir_path, _exclude_dir)
            if dir_path in _exclude_dir:
                QMessageBox.information(self, "提示", "此文件夹已经存在！", QMessageBox.Ok)
            elif len(parentlist) > 0:
                QMessageBox.information(self, "提示", "此文件夹已经包含！\n" + "\n".join(parentlist), QMessageBox.Ok)
            elif len(sublist) > 0:
                QMessageBox.information(self, "提示", "请先删除此文件夹下的子目录！\n" + "\n".join(sublist), QMessageBox.Ok)
            else:
                self.AddExcludeDirItem(dir_path)
                _exclude_dir.append(dir_path)
                self.mysetting_dict["_exclude_dir"] = _exclude_dir

    def onClickedDel(self):
        selected = self.child.listView_common.selectedIndexes()
        if 0 < len(selected) < 2:
            _common_dir = self.mysetting_dict["_common_dir"]
            for i in sorted(selected):
                table_row = i.row()
                _item = self.listModel_common.item(table_row, 0)
                file_path = _item.text()
                self.listModel_common.removeRow(table_row)
                _common_dir.remove(file_path)
            self.mysetting_dict["_common_dir"] = _common_dir
        else:
            QMessageBox.information(self, '注意', '请选中一项进行删除！', QMessageBox.Yes)

    def onClickedDelExclude(self):
        selected = self.child.listView_exclude.selectedIndexes()
        if 0 < len(selected) < 2:
            _exclude_dir = self.mysetting_dict["_exclude_dir"]
            for i in sorted(selected):
                table_row = i.row()
                _item = self.listModel_exclude.item(table_row, 0)
                file_path = _item.text()
                self.listModel_exclude.removeRow(table_row)
                _exclude_dir.remove(file_path)
            self.mysetting_dict["_exclude_dir"] = _exclude_dir
        else:
            QMessageBox.information(self, '注意', '请选中一项进行删除！', QMessageBox.Yes)

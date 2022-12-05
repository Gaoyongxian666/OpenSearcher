import traceback
from queue import Queue

from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from qcustomdialog import index
from qutils.searchthread import SearchThread
from qutils.types import GetIndexTypesDict


class IndexWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.child = index.Ui_MainWindow()
        self.child.setupUi(self)
        self.setWindowTitle("建立索引")

        self.CurPath = parent.CurPath
        self.IconDir = parent.IconDir
        self.IconDict = parent.IconDict
        self.logger = parent.logger
        self.mysetting_dict = parent.mysetting_dict

        self.queue = Queue()
        self.Init()

    def Init(self):
        self.child.progressBar.hide()
        self.child.progressBar.stop()
        self.child.pushButton.clicked.connect(self.onClickedSearch)
        self.child.comboBox_type.InitComboBox(GetIndexTypesDict(self.IconDir))

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.UpdateUi)
        self.timer.start(150)

    def UpdateUi(self):
        if not self.queue.empty():
            for i in range(self.queue.qsize()):
                content = self.queue.get()
                if content[0] == "append_text":
                    self.child.textBrowser.append(content[1])
                elif content[0] == "update_top_lable":
                    self.child.top_lable.setText(content[1])
                elif content[0] == "completed":
                    self.SearchComplete()

    def closeEvent(self, event):
        try:
            self.search_thread.terminate()
        except:
            self.logger.info(traceback.format_exc())

    '''-----------------------------------搜索相关-----------------------------------------------'''

    def SearchStartUi(self):
        self.child.progressBar.start()
        self.child.progressBar.show()
        self.child.top_lable.setText("搜索中")
        self.child.pushButton.setText("停止")

    def SearchStopUi(self):
        self.child.pushButton.setText("停止中···")
        self.child.pushButton.setEnabled(False)

    def SearchComplete(self):
        self.child.progressBar.hide()
        self.child.progressBar.stop()
        self.child.top_lable.setText("搜索就绪")
        self.child.pushButton.setText("开始")
        self.child.pushButton.setEnabled(True)
        self.logger.info("搜索完成")

    def isRunning(self):
        try:
            return self.search_thread.isRunning()
        except:
            self.logger.info(traceback.format_exc())
            return False

    def onClickedSearch(self):
        if self.isRunning():
            reply = QMessageBox.information(self, '注意', '是否要停止搜索？', QMessageBox.Yes | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.logger.info("开始停止搜索线程")
                self.search_thread.stop()
        else:
            self.comboBox_dir_text = self.child.comboBox_dir.text()
            self.comboBox_type_text = self.child.comboBox_type.text()
            self.comboBox_type_list = [x for x in self.comboBox_type_text.split(";") if x]
            if self.comboBox_dir_text == "全部目录":
                self.comboBox_dir_list = self.child.comboBox_dir.get_devices()
            else:
                self.comboBox_dir_list = self.comboBox_dir_text.split("|")

            self.child.textBrowser.append("开启搜索线程······")
            self.child.textBrowser.append("搜索目录：" + str(self.comboBox_dir_text))
            self.child.textBrowser.append("搜索类型：" + str(self.comboBox_type_list))
            self.child.textBrowser.append("文件限制：" + str(self.mysetting_dict["_limit_file_size"]) + "M")
            self.child.textBrowser.append("忽略目录：" + str(self.mysetting_dict['_exclude_dir']))
            self.child.textBrowser.append("由于磁盘文件较多，读取文件列表耗时较长，请耐心等待······")

            self.search_thread = SearchThread(
                DirPaths=self.comboBox_dir_list,
                CurPath=self.CurPath,
                types=self.comboBox_type_list,
                logger=self.logger,
                queue=self.queue,
                mysetting_dict=self.mysetting_dict,
                IconDict=self.IconDict)
            self.search_thread.started.connect(self.SearchStartUi)
            self.search_thread.finished.connect(lambda: self.queue.put(("completed", 1)))
            self.search_thread.stoped.connect(self.SearchStopUi)
            self.search_thread.start()

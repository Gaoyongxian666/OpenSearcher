import hashlib
import logging
import os
import traceback
import warnings
from queue import Queue

import psutil
import pythoncom
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from qcustomdialog import index
from qutils.util import file_name_list, get_text



class IndexWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.child = index.Ui_MainWindow()
        self.child.setupUi(self)
        self.setWindowTitle("建立索引")

        self.CurPath = parent.CurPath
        self.IconDir = parent.IconDir
        self.logger=parent.logger

        self._limit_file_size = parent._limit_file_size
        self.search_running = False
        self.queue = Queue()

        self.child.comboBox.setEnabled(False)
        self.child.pushButton.setEnabled(False)
        self.child.progressBar.hide()
        self.child.progressBar.stop()

        self.child.pushButton.clicked.connect(self.onClickedSearch)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.UpdateUi)
        self.timer.start(150)

        self.RelayUpdate()
        self.InitComboBox()

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

    def InitComboBox(self):
        items = ["Microsoft Word 97-2003 文件（.doc）",
                 "Microsoft Word 文件（.docx）",
                 "Microsoft Excel 97-2003 文件（.xls）",
                 "Microsoft Excel 文件（.xlsx）",
                 "Microsoft PowerPoint 97-2003 文件（.ppt）",
                 "Microsoft PowerPoint 文件（.pptx）",
                 "Adobe PDF 文件（.pdf）",
                 "EPUB 文件（.epub）",
                 "MOBI 文件（.mobi）",
                 ]
        items_icon = [os.path.abspath(os.path.join(self.IconDir, 'doc.png')),
                      os.path.abspath(os.path.join(self.IconDir, 'docx.png')),
                      os.path.abspath(os.path.join(self.IconDir, 'xls.png')),
                      os.path.abspath(os.path.join(self.IconDir, 'xlsx.png')),
                      os.path.abspath(os.path.join(self.IconDir, 'ppt.png')),
                      os.path.abspath(os.path.join(self.IconDir, 'pptx.png')),
                      os.path.abspath(os.path.join(self.IconDir, 'pdf.png')),
                      os.path.abspath(os.path.join(self.IconDir, 'epub.png')),
                      os.path.abspath(os.path.join(self.IconDir, 'mobi.png')),
                      ]
        first_item = '全部文件类型'
        first_item_icon = os.path.abspath(os.path.join(self.IconDir, 'sysfile.png'))
        line_edit_icon = os.path.abspath(os.path.join(self.IconDir, 'sysfile.png'))

        self.child.comboBox_2.InitComboBox(
            line_edit_icon=line_edit_icon,
            first_item=first_item, first_item_icon=first_item_icon,
            items=items, items_icon=items_icon)

    def RelayUpdate(self):
        self.child.frame.setEnabled(False)
        self.relay_thread = RelayUpdateThread()
        self.relay_thread.ok.connect(self.complete)
        self.relay_thread.message.connect(lambda text: self.child.textBrowser.append(text))
        self.relay_thread.start()

    def complete(self, device_list):
        items = device_list
        disk_png = os.path.abspath(os.path.join(self.IconDir, "disk.png"))
        items_icon = [disk_png for i in range(len(device_list))]
        first_item = '全部磁盘'
        first_item_icon = disk_png
        line_edit_icon = disk_png

        self.child.comboBox.InitComboBox(line_edit_icon=line_edit_icon,
                                         first_item=first_item, first_item_icon=first_item_icon,
                                         items=items, items_icon=items_icon)
        self.child.textBrowser.append("磁盘读取完成，发现磁盘：" + str(items))
        self.child.comboBox.setEnabled(True)
        self.child.pushButton.setEnabled(True)
        self.child.frame.setEnabled(True)

    def SearchShowUi(self):
        self.child.progressBar.start()
        self.child.progressBar.show()
        self.child.top_lable.setText("搜索中")

    def SearchHideeUi(self):
        self.child.progressBar.hide()
        self.child.progressBar.stop()
        self.child.top_lable.setText("准备就绪")

    def SearchComplete(self):
        self.SearchHideeUi()
        self.child.pushButton.setText("开始")
        self.search_running = False

    def onClickedSearch(self):
        if self.search_running:
            reply = QMessageBox.information(self, '注意', '是否要停止搜索？', QMessageBox.Yes | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.SearchHideeUi()
                self.child.textBrowser.append("停止搜索线程")
                self.search_running = False
                self.search_thread.terminate()
                self.child.pushButton.setText("开始")
        else:
            self.Dirs = self.child.comboBox.get_text()
            self.Dirs_list = [x + "\\" for x in self.Dirs.split(";") if x]
            self.screen_text = self.child.comboBox_2.get_text()
            self.screen = [x for x in self.screen_text.split(";") if x]
            self.SearchShowUi()
            self.search_running = True
            self.child.textBrowser.append("开启搜索线程······")
            self.child.textBrowser.append("搜索目录：" + str(self.Dirs_list))
            self.child.textBrowser.append("搜索类型：" + str(self.screen))
            self.child.textBrowser.append("文件限制：" + str(self._limit_file_size) + "M")
            self.child.textBrowser.append("由于磁盘文件较多，读取文件列表耗时较长，请耐心等待······")

            self.search_thread = SearchThread(
                DirPaths=self.Dirs_list,
                screen=self.screen,
                CurPath=self.CurPath,
                _limit_file_size=self._limit_file_size,
                queue=self.queue)
            self.search_thread.start()
            self.child.pushButton.setText("停止")

    def closeEvent(self, event):
        try:
            self.search_thread.terminate()
        except:
            self.logger.info(traceback.format_exc())


class RelayUpdateThread(QThread):
    ok = pyqtSignal(list)
    message = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            self.message.emit("正在读取磁盘······")
            device_list = []
            for i in psutil.disk_partitions():
                device_list.append(i.device)
            self.ok.emit(device_list)
        except:
            self.message.emit("读取磁盘发生错误：\n" + traceback.format_exc())


class SearchThread(QThread):
    def __init__(self, DirPaths: list, CurPath, screen, queue, _limit_file_size):
        super().__init__()
        self.DirPaths = DirPaths
        self.CurPath = CurPath
        self.screen = screen
        self.queue = queue
        self._limit_file_size = _limit_file_size
        self.temp_path = os.path.abspath(os.path.join(self.CurPath, '.temp'))
        self.file_name_lists = []
        self.icon_dir = os.path.abspath(os.path.join(self.CurPath, 'icon'))
        self.antiword_path = os.path.abspath(os.path.join(self.CurPath, 'antiword/antiword.exe'))

    def run(self):
        pythoncom.CoInitialize()
        if not os.path.isdir(self.temp_path):
            os.makedirs(self.temp_path)
            self.queue.put(("append_text", "不存在就创建目录：" + self.temp_path))
        for dir_path in self.DirPaths:
            self.file_name_lists.extend(file_name_list(file_dir=dir_path, screen=self.screen, icon_dir=self.icon_dir,
                                                       size_limit=self._limit_file_size))
        self.md5_list = [name for name in os.listdir(self.temp_path) if
                         os.path.isfile(os.path.join(self.temp_path, name))]
        file_name_lists_num = str(len(self.file_name_lists))
        file_name_lists_places = len(file_name_lists_num)
        self.queue.put(("append_text", str(self.file_name_lists)))

        for i, file_n_l in enumerate(self.file_name_lists):
            self.queue.put(("append_text", "当前正搜索文件:" + file_n_l[3][1]))
            self.queue.put(("update_top_lable", str(i).rjust(file_name_lists_places) + "/" + file_name_lists_num))
            self.write_temp(absolute_path=file_n_l[3][1], file_suffix=file_n_l[4][1])

        self.queue.put(("append_text", "搜索完成"))
        self.queue.put(("completed", 1))

    def write_temp(self, absolute_path, file_suffix):
        try:
            with open(absolute_path, 'rb') as f:
                file_md5 = hashlib.md5(f.read()).hexdigest()
            md5_path = os.path.abspath(os.path.join(self.temp_path, file_md5))
            if file_md5 in self.md5_list:
                self.queue.put(("append_text", "存在缓存文件：" + md5_path + "\n"))
            else:
                text = get_text(
                    file_suffix=file_suffix, file_absolute_path=absolute_path, file_md5=file_md5,
                    temp_path=self.temp_path, antiword_path=self.antiword_path)

                with open(md5_path, 'w', encoding='utf8') as f:
                    f.write(text)
                self.queue.put(("append_text", "写入完成:" + md5_path + "\n"))
        except:
            self.queue.put(("append_text", "处理文件时发生错误"))
            self.queue.put(("append_text", traceback.format_exc()))

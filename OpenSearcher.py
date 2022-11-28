import datetime
import os
import socket
import sys
import traceback
from queue import Queue

import pythoncom
import win32api
import win32con
import winshell
from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex, QThread, pyqtSignal, QTimer, QProcess, QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDesktopWidget, QMessageBox, qApp
from sqlitedict import SqliteDict

from qcustomdialog.FileWindow import FileWindow
from qcustomdialog.HelpWindow import HelpWindow
from qcustomdialog.IndexWindow import IndexWindow
from qcustomdialog.SettingWindow import SettingWindow
from qcustomdialog.UpdateWindow import UpdateWindow
from MainWindow import Ui_MainWindow
from qutils.searchthread import SearchThread
from qutils.traythread import TrayThread
import logging
from qutils.util import is_user_admin, run_as_admin, create_right_menu, remove_right_menu, create_shortcut

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self, icon, title, Version, UpdateUrl, socket, CurPath, DirPath, Name_, Name, LogoPath, ExePath):
        super().__init__()
        self.icon = icon
        self.title = title
        self.Version = Version
        self.socket = socket
        self.UpdateUrl = UpdateUrl
        self.CurPath = CurPath
        self.DirPath = DirPath
        self.Name_ = Name_
        self.Name = Name
        self.LogoPath = LogoPath
        self.ExePath = ExePath

        self.IconDir = os.path.abspath(os.path.join(self.CurPath, "icon"))
        self.LogPath = os.path.abspath(os.path.join(self.CurPath, "logs"))
        self.HelpPath = os.path.abspath(os.path.join(self.CurPath, 'HELP.md'))
        self.SettingPath = os.path.abspath(os.path.join(self.CurPath, 'setting.db'))
        self.TempPath = os.path.abspath(os.path.join(self.CurPath, '.temp'))
        self.ErrorTempPath = os.path.abspath(os.path.join(self.CurPath, '.errortemp'))
        self.LnkPath = os.path.abspath(os.path.join(winshell.desktop(), self.Name_ + ".lnk"))
        self.LnkPath2 = os.path.abspath(os.path.join(winshell.common_desktop(), self.Name_ + ".lnk"))
        self.settings = QSettings(os.path.abspath(os.path.join(self.CurPath, 'settings.ini')), QSettings.IniFormat)

        self.isMax = False
        self.search_running = False
        self.queue = Queue()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.Init()
        self.InitTrayIcon()
        self.InitLogger()
        self.InitComboBox()
        self.InitGeometry()
        self.InitRelayUpdate()

    def UpdateUi(self):
        if not self.queue.empty():
            for i in range(self.queue.qsize()):
                content = self.queue.get()
                if content[0] == "error":
                    self.ui.listView_error.listModel.appendRow(content[1])
                elif content[0] == "all":
                    self.ui.listView_all.listModel.appendRow(content[1])
                elif content[0] == "trigger":
                    self.ui.tableView.tableModel.append_data(content[1])
                elif content[0] == "completed":
                    self.SearchComplete()
                elif content[0] == "update_top_lable":
                    self.ui.top_lable.setText(content[1])
                elif content[0] == "update_bottom_lable":
                    self.ui.bottom_lable.setText(content[1])
                elif content[0] == "loading":
                    self.ui.bottom_lable.setText(content[1])
                    self.ui.textframe.Search(Loading=True, CurPath=self.CurPath, FilePath=content[1],
                                             Keywords=self.keywords, IsError=content[2])
                elif content[0] == "_show_all":
                    if content[1] == 0:
                        if self.ui.frame_center_left.isVisible():
                            self.ui.frame_center_left.hide()
                elif content[0] == "_common_dir":
                    self.ui.file_edit.setText(content[1])

    '''-----------------------------------主窗体-----------------------------------------------'''

    def Init(self):
        if self.DirPath is not None:
            self.ui.file_edit.setText(self.DirPath)

        # 不允许崩溃
        self.ui.splitter.setCollapsible(0, False)
        self.ui.splitter.setCollapsible(1, False)
        self.ui.splitter.setCollapsible(2, False)
        self.ui.splitter_2.setCollapsible(0, False)
        self.ui.splitter_2.setCollapsible(1, False)

        self.ui.textframe.setReadOnly(True)
        self.ui.file_edit.setReadOnly(True)
        self.ui.frame_center_left.hide()
        self.ui.progressBar.stop()
        self.ui.progressBar.hide()

        self.ui.tableView.setColumnWidth(0, 200)
        self.ui.tableView.setColumnWidth(1, 75)
        self.ui.tableView.setColumnWidth(2, 150)
        self.ui.tableView.setColumnWidth(3, 700)

        self.ui.file_button.clicked.connect(self.onClickedOpenFileDialog)
        self.ui.search_button.clicked.connect(self.onClickedSearch)
        self.ui.keywords_edit.returnPressed.connect(self.onClickedSearch)
        self.ui.text_scale_up.clicked.connect(self.onClickedZoomIn)
        self.ui.text_scale_down.clicked.connect(self.onClickedZoomOut)
        self.ui.update.clicked.connect(self.onClickedUpdate)
        self.ui.show_error_button.clicked.connect(self.onClickedShowErrorListView)
        self.ui.show_all_button.clicked.connect(self.onClickedShowAllListView)
        self.ui.setting.clicked.connect(self.onClickedShowSettingWindow)
        self.ui.help.clicked.connect(self.onClickedHelpWindow)
        self.ui.index_button.clicked.connect(self.onClickedIndexWindow)
        self.ui.common_dir.clicked.connect(self.onClickedFileWindow)
        self.ui.tableView.clicked.connect(self.onClickedTableView)
        self.ui.listView_error.clicked.connect(self.onClickedListView)
        self.ui.listView_all.clicked.connect(self.onClickedListView_)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.UpdateUi)
        self.timer.start(150)

    def onClickedZoomIn(self):
        # 放大
        self.ui.textframe.zoomIn(1)

    def onClickedZoomOut(self):
        self.ui.textframe.zoomIn(-1)

    def onClickedShowAllListView(self):
        if self._show_all:
            if self.ui.frame_center_left.isVisible():
                self.ui.frame_center_left.hide()
            else:
                self.ui.frame_center_left.show()
        else:
            QMessageBox.information(self, '注意', '当前未开启显示全部文件功能（请在设置中开启）', QMessageBox.Ok)

    def onClickedShowErrorListView(self):
        if self.ui.listView_error.isVisible():
            self.ui.listView_error.hide()
        else:
            self.ui.listView_error.show()

    def onClickedOpenFileDialog(self):
        self.search_DirPath = QFileDialog.getExistingDirectory(self, '选择文件夹', self.CurPath)
        self.ui.file_edit.setText(self.search_DirPath)

    def onClickedTableView(self, index):
        table_row = index.row()
        _index = self.ui.tableView.tableModel.index(table_row, 3, QModelIndex())
        file_path = os.path.abspath(str(_index.data()))
        self.queue.put(("loading", file_path, False))

    def onClickedListView(self, index):
        table_row = index.row()
        _item = self.ui.listView_error.listModel.item(table_row, 0)
        file_path = _item.text()
        file_path_ = file_path.split(" -> (")[-1][:-1]
        self.queue.put(("loading", file_path_, True))

    def onClickedListView_(self, index):
        table_row = index.row()
        _item = self.ui.listView_all.listModel.item(table_row, 0)
        file_path = _item.text()
        file_path_ = file_path.split(" -> (")[-1][:-1]
        self.queue.put(("loading", file_path_, False))

    def closeEvent(self, event):
        event.ignore()
        if self.isMaximized():
            self.isMax = True
        else:
            self.isMax = False
        # 执行顺序不能颠倒
        self.showMinimized()
        self.setWindowFlags(QtCore.Qt.SplashScreen | QtCore.Qt.FramelessWindowHint)

    '''-----------------------------------初始化-----------------------------------------------'''

    def InitLogger(self):
        if not os.path.isdir(self.LogPath):
            os.makedirs(self.LogPath)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level='INFO', format='%(asctime)s: %(message)s')
        fmt = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s:%(message)s'
        fh = logging.FileHandler(
            os.path.abspath(os.path.join(self.LogPath, f'{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.txt')),
            encoding="utf8")
        fh.setFormatter(logging.Formatter(fmt=fmt))
        fh.setLevel(logging.INFO)
        self.logger.addHandler(fh)

    def InitGeometry(self):
        if os.path.exists(os.path.join(self.CurPath, "settings.ini")):
            self.restoreGeometry(self.settings.value("geometry", self.saveGeometry()))
            self.restoreState(self.settings.value("state", self.saveState()))
            print(self.ui.splitter.saveGeometry())
            self.ui.splitter.restoreGeometry(self.settings.value("splitter_geometry", self.ui.splitter.saveGeometry()))
            self.ui.splitter.restoreState(self.settings.value("splitter_state", self.ui.splitter.saveState()))
            self.ui.splitter_2.restoreGeometry(
                self.settings.value("splitter_2_geometry", self.ui.splitter_2.saveGeometry()))
            self.ui.splitter_2.restoreState(self.settings.value("splitter_2_state", self.ui.splitter_2.saveState()))
        else:
            screen = QDesktopWidget().screenGeometry()
            height = screen.height() * 6 / 7
            width = screen.width() * 9 / 10
            self.setGeometry(int((screen.width() - width) / 2), int((screen.height() - height) / 2), int(width),
                             int(height))

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
                 "文本文档（.txt）"]
        items_icon = [os.path.abspath(os.path.join(self.IconDir, 'doc.png')),
                      os.path.abspath(os.path.join(self.IconDir, 'docx.png')),
                      os.path.abspath(os.path.join(self.IconDir, 'xls.png')),
                      os.path.abspath(os.path.join(self.IconDir, 'xlsx.png')),
                      os.path.abspath(os.path.join(self.IconDir, 'ppt.png')),
                      os.path.abspath(os.path.join(self.IconDir, 'pptx.png')),
                      os.path.abspath(os.path.join(self.IconDir, 'pdf.png')),
                      os.path.abspath(os.path.join(self.IconDir, 'epub.png')),
                      os.path.abspath(os.path.join(self.IconDir, 'mobi.png')),
                      os.path.abspath(os.path.join(self.IconDir, 'txt.png'))]
        first_item = '全部文件类型'
        first_item_icon = os.path.abspath(os.path.join(self.IconDir, 'sysfile.png'))
        line_edit_icon = os.path.abspath(os.path.join(self.IconDir, 'sysfile.png'))
        self.screen_len = len(items)
        self.ui.comboBox.InitComboBox(
            line_edit_icon=line_edit_icon,
            first_item=first_item,
            first_item_icon=first_item_icon,
            items=items,
            items_icon=items_icon,
        )

    def InitRelayUpdate(self):
        """耗时操作"""
        self.ui.frame.setEnabled(False)
        self.relay_thread = RelayUpdateThread(self.queue, self.socket, self.CurPath, self.SettingPath, self.Name,
                                              self.Name_, self.LogoPath, self.LnkPath, self.LnkPath2)
        self.relay_thread.update_setting.connect(self.InitSetting)
        self.relay_thread.update_dir.connect(self.UpdateDir)
        self.relay_thread.update_screen.connect(self.UpdateScreen)
        self.relay_thread.update_textframe.connect(self.InitTextFrame)
        self.relay_thread.complete.connect(self.InitComplete)
        self.relay_thread.exit_.connect(self.Exit_)

        self.relay_thread.start()

    def Exit_(self):
        try:
            self.backend_thread.OnDestroy()
        except:
            self.logger.info(traceback.format_exc())
        try:
            qApp.quit()
        except:
            self.logger.info(traceback.format_exc())
        sys.exit(0)

    def InitTextFrame(self, content):
        self.ui.textframe.Init(fontsize=content[0], fontfamily=content[1], linewrap=content[2], linenumber=content[3],
                               mysetting_dict=self.mysetting_dict)

    def UpdateScreen(self, l):
        self.ui.comboBox.UpdateComboBox(self.screen_len, l)

    def UpdateDir(self, dir):
        if self.isMinimized() or not self.isVisible():
            self.setWindowFlags(QtCore.Qt.Window)
            self.activateWindow()
            if self.isMax:
                self.showMaximized()
            else:
                self.showNormal()
        self.ui.file_edit.setText(dir)

    def InitSetting(self, setting):
        self.mysetting_dict = setting
        self._auto_run = self.mysetting_dict['_auto_run']
        self._last_dir_flag = self.mysetting_dict['_last_dir_flag']
        self._right_menu = self.mysetting_dict['_right_menu']
        self._remind = self.mysetting_dict['_remind']
        self._show_all = self.mysetting_dict['_show_all']
        self._limit_file_size = self.mysetting_dict['_limit_file_size']
        if self.mysetting_dict["_desktop"]:
            self.InitDesktop()

    def InitDesktop(self):
        # 判断是否有桌面图标
        if not os.path.exists(self.LnkPath) and not os.path.exists(self.LnkPath2):
            logger.info("桌面没有创建快捷方式")
            create_shortcut(sys.argv[0], self.Name_, "一个开源的、本地的、安全的、支持全文检索的搜索器。", self.LogoPath)


    def InitComplete(self):
        self.ui.frame.setEnabled(True)

    '''-----------------------------------后台图标-----------------------------------------------'''

    def InitTrayIcon(self, f=True):
        if f:
            self.backend_thread = TrayThread(icon=self.icon, title=self.title)
            self.backend_thread.start()
            self.backend_thread.setting.connect(self.onClickedShowSettingWindow)
            self.backend_thread.show.connect(self.onClickedShow)
            self.backend_thread.help.connect(self.onClickedHelpWindow)
            self.backend_thread.exit.connect(self.onClickedExit)
            self.backend_thread.update.connect(self.onClickedUpdate)
            self.backend_thread.restart.connect(self.onClickedRestart)

    def onClickedShow(self):
        if self.isMinimized() or not self.isVisible():
            self.setWindowFlags(QtCore.Qt.Window)
            self.activateWindow()
            if self.isMax:
                self.showMaximized()
            else:
                self.showNormal()
        else:
            if self.isMaximized():
                self.isMax = True
            self.close()

    def onClickedRestart(self):
        """ 进程控制实现自动重启"""
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("state", self.saveState())
        self.settings.setValue("splitter_geometry", self.ui.splitter.saveGeometry())
        self.settings.setValue("splitter_state", self.ui.splitter.saveState())
        self.settings.setValue("splitter_2_geometry", self.ui.splitter_2.saveGeometry())
        self.settings.setValue("splitter_2_state", self.ui.splitter_2.saveState())
        self.backend_thread.OnDestroy()
        qApp.quit()
        self.p = QProcess
        s = self.p.startDetached(sys.executable, sys.argv)

    def onClickedExit(self):
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("state", self.saveState())
        self.settings.setValue("splitter_geometry", self.ui.splitter.saveGeometry())
        self.settings.setValue("splitter_state", self.ui.splitter.saveState())
        self.settings.setValue("splitter_2_geometry", self.ui.splitter_2.saveGeometry())
        self.settings.setValue("splitter_2_state", self.ui.splitter_2.saveState())
        self.backend_thread.OnDestroy()
        qApp.quit()
        sys.exit(0)


    def onClickedShowSettingWindow(self):
        if self.isMinimized() or not self.isVisible():
            self.setWindowFlags(QtCore.Qt.Window)
            self.activateWindow()
            if self.isMax:
                self.showMaximized()
            else:
                self.showNormal()
        settingwindow = SettingWindow(self)
        settingwindow.show()

    def onClickedFileWindow(self):
        filewindow = FileWindow(self)
        filewindow.show()

    def onClickedHelpWindow(self):
        if self.isMinimized() or not self.isVisible():
            self.setWindowFlags(QtCore.Qt.Window)
            self.activateWindow()
            if self.isMax:
                self.showMaximized()
            else:
                self.showNormal()
        helpwindow = HelpWindow(self)
        helpwindow.show()

    def onClickedIndexWindow(self):
        if self.isMinimized() or not self.isVisible():
            self.setWindowFlags(QtCore.Qt.Window)
            self.activateWindow()
            if self.isMax:
                self.showMaximized()
            else:
                self.showNormal()
        indexwindow = IndexWindow(self)
        indexwindow.show()

    def onClickedUpdate(self):
        if self.isMinimized() or not self.isVisible():
            self.setWindowFlags(QtCore.Qt.Window)
            self.activateWindow()
            if self.isMax:
                self.showMaximized()
            else:
                self.showNormal()
        updatewindow = UpdateWindow(parent=self)
        updatewindow.show()

    '''-----------------------------------搜索相关-----------------------------------------------'''

    def SearchShowUi(self):
        self.ui.progressBar.start()
        self.ui.progressBar.show()
        self.ui.top_lable.setText("搜索中")
        self.ui.bottom_lable.setText("搜索中·····")

    def SearchHideeUi(self):
        self.ui.progressBar.hide()
        self.ui.progressBar.stop()
        self.ui.top_lable.setText("搜索就绪")
        self.ui.bottom_lable.setText("搜索完毕!")

    def SearchComplete(self):
        self.SearchHideeUi()
        self.logger.info("搜索完成")
        self.ui.search_button.setText("搜索")
        self.search_running = False
        if self._remind:
            self.backend_thread.ShowToast("当前搜索完成")

    def onClickedSearch(self):
        if self.search_running:
            reply = QMessageBox.information(self, '注意', '是否要停止搜索？', QMessageBox.Yes | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.logger.info("停止搜索线程")
                self.SearchHideeUi()
                self.search_running = False
                self.search_thread.terminate()
                self.ui.search_button.setText("搜索")
        else:
            self.ui.tableView.tableModel.remove_all()
            self.ui.listView_error.listModel.clear()
            self.ui.listView_all.listModel.clear()
            self.ui.textframe.clear()
            self.search_dirname = self.ui.file_edit.text()
            self.keywords = self.ui.keywords_edit.text()
            self.screen_text = self.ui.comboBox.get_text()
            self.screen = [x for x in self.screen_text.split(";") if x]

            if self.search_dirname == "":
                self.ui.bottom_lable.setText("请先选择文件夹！")
                QMessageBox.information(self, "提示", "请先选择文件夹！", QMessageBox.Ok)
                self.logger.info("文件夹为空")
            elif self.keywords.strip() == "":
                self.ui.bottom_lable.setText("请先输入关键词！")
                QMessageBox.information(self, "提示", "请先输入关键词！", QMessageBox.Ok)
                self.logger.info("关键词为空")
            elif self.screen_text == "":
                self.ui.bottom_lable.setText("请先指定文件类型！")
                QMessageBox.information(self, "提示", "请先指定文件类型！", QMessageBox.Ok)
                self.logger.info("文件类型为空")
            else:
                self.SearchShowUi()
                self.search_running = True
                self.mysetting_dict["_last_screen"] = self.ui.comboBox.getState()[1:]
                self.mysetting_dict["_last_dir"] = self.search_dirname
                self.logger.info("开启搜索线程")
                self.logger.info("搜索类型：" + str(self.screen))
                self.logger.info("搜索目录：" + self.search_dirname)
                self.logger.info("文件限制：" + str(self._limit_file_size) + "M")

                self.search_thread = SearchThread(
                    DirPaths=[self.search_dirname],
                    screen=self.screen,
                    CurPath=self.CurPath,
                    keywords=self.keywords,
                    logger=self.logger,
                    queue=self.queue,
                    show_all=self._show_all,
                    _limit_file_size=self._limit_file_size
                )
                self.search_thread.start()
                self.ui.search_button.setText("停止")


class RelayUpdateThread(QThread):
    update_setting = pyqtSignal(SqliteDict)
    update_dir = pyqtSignal(str)
    update_textframe = pyqtSignal(list)
    update_screen = pyqtSignal(list)
    complete = pyqtSignal()
    exit_ = pyqtSignal()

    def __init__(self, queue, socket, CurPath, SettingPath, Name, Name_, LogoPath, LnkPath, LnkPath2):
        super().__init__()
        self.queue = queue
        self.CurPath = CurPath
        self.socket = socket
        self.SettingPath = SettingPath
        self.Name = Name
        self.Name_ = Name_
        self.LogoPath = LogoPath
        self.LnkPath = LnkPath
        self.LnkPath2 = LnkPath2

    def run(self):
        self.setting()
        self.init_textframe()
        if self.mysetting_dict["_last_dir_flag"]:
            self.update_dir.emit(self.mysetting_dict["_last_dir"])
        if self.mysetting_dict["_last_screen_flag"]:
            self.update_screen.emit(self.mysetting_dict["_last_screen"])
        self.complete.emit()
        while True:
            data, addr = self.socket.recvfrom(1024)
            data_ = data.decode("utf-8")
            if data_ == "exit_":
                self.exit_.emit()
            else:
                self.update_dir.emit(data_)

    def init_textframe(self):
        self.update_textframe.emit([
            self.mysetting_dict['_fontsize'],
            self.mysetting_dict['_fontfamily'],
            self.mysetting_dict['_linewrap'],
            self.mysetting_dict['_linenumber'],
        ])

    def setting(self):
        if not os.path.exists(self.SettingPath):
            logger.info(1111111)
            self.mysetting_dict = SqliteDict(self.SettingPath, autocommit=True)
            self.mysetting_dict.clear()
            self.mysetting_dict['_auto_run'] = True
            self.mysetting_dict['_last_dir_flag'] = True
            self.mysetting_dict['_last_dir'] = ""
            self.mysetting_dict['_last_screen_flag'] = True
            self.mysetting_dict['_last_screen'] = []
            self.mysetting_dict['_right_menu'] = True
            self.mysetting_dict['_remind'] = True
            self.mysetting_dict['_show_all'] = False
            self.mysetting_dict['_limit_file_size'] = 100
            self.mysetting_dict['_fontsize'] = 10
            self.mysetting_dict['_fontfamily'] = "宋体"
            self.mysetting_dict['_linewrap'] = True
            self.mysetting_dict['_linenumber'] = True
            self.mysetting_dict['_common_dir'] = []
            self.mysetting_dict['_desktop'] = True
            self.update_setting.emit(self.mysetting_dict)
            if not self.init_auto():
                self.mysetting_dict['_auto_run'] = False
            if not self.init_right_click():
                self.mysetting_dict['_right_menu'] = False
        else:
            self.mysetting_dict = SqliteDict(self.SettingPath, autocommit=True)
            self.update_setting.emit(self.mysetting_dict)


    def init_auto(self):
        try:
            path = sys.argv[0]
            # path = os.path.abspath(os.path.join(self.CurPath, "OpenSearcher.exe"))
            KeyName = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key, self.Name, 0, win32con.REG_SZ, path)
            logger.info('成功开启软件自启动')
            return True
        except:
            win32api.MessageBox(0, traceback.format_exc(), self.Name_, win32con.MB_OK)
            return False

    def init_right_click(self):
        if not is_user_admin():
            return run_as_admin("set_menu")
        else:
            try:
                if sys.argv[0][-3:] == ".py":
                    ExePath = " ".join([sys.executable, sys.argv[0]])
                else:
                    ExePath = sys.argv[0]
                create_right_menu(name=self.Name, content=self.Name_ + " 搜索", icon=self.LogoPath,
                                  command=ExePath + " \"%L\"",
                                  type_="DIRECTORY")
                create_right_menu(name=self.Name, content=self.Name_ + " 搜索", icon=self.LogoPath,
                                  command=ExePath + " \"%W\"",
                                  type_="DIRECTORY_BACKGROUND")
                return True
            except Exception:
                win32api.MessageBox(0, traceback.format_exc(), self.Name_, win32con.MB_OK)
                return False


def main():
    print(sys.argv)

    Name_ = "Open Searcher"
    Name = "OpenSearcher"
    Version = "0.0.5"
    UpdateUrl = "https://aidcs-1256440297.cos.ap-beijing.myqcloud.com/OpenSearcher/update.txt"

    CurPath = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.environ['REQUESTS_CA_BUNDLE'] = os.path.abspath(os.path.join(CurPath, 'cacert.pem'))
    LogoPath = os.path.abspath(os.path.join(CurPath, "icon/logo.ico"))
    if sys.argv[0][-3:] == ".py":
        ExePath = " ".join([sys.executable, sys.argv[0]])
    else:
        ExePath = sys.argv[0]

    # 判断是否是设置右键菜单
    if len(sys.argv) > 1:
        if sys.argv[-1] == "set_menu":
            try:
                # icon 设置成 exe文件也可以，Windows系统会自动读取ico
                create_right_menu(name=Name, content=Name_ + " 搜索", icon=LogoPath, command=ExePath + " \"%L\"",
                                  type_="DIRECTORY")
                create_right_menu(name=Name, content=Name_ + " 搜索", icon=LogoPath, command=ExePath + " \"%W\"",
                                  type_="DIRECTORY_BACKGROUND")
            except Exception:
                win32api.MessageBox(0, traceback.format_exc(), Name_, win32con.MB_OK)
            return
        elif sys.argv[-1] == "del_menu":
            try:
                remove_right_menu(Name, type_="DIRECTORY")
                remove_right_menu(Name, type_="DIRECTORY_BACKGROUND")
            except Exception:
                win32api.MessageBox(0, traceback.format_exc(), Name_, win32con.MB_OK)
            return
        else:
            DirPath = sys.argv[-1]
    else:
        DirPath = None

    # 判断是否已经启动
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        host = socket.gethostname()
        s.bind((host, 60111))
    except Exception:
        if len(sys.argv) > 1:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            host = socket.gethostname()
            s.connect((host, 60111))
            data = sys.argv[-1]
            s.sendto(data.encode('utf-8'), (host, 60111))
        else:
            result = win32api.MessageBox(0, "提示：Open Searcher程序后台运行中\n是否停止当前正在运行的Open Searcher？", Name_,
                                         win32con.MB_YESNO)
            if result == 6:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                host = socket.gethostname()
                s.connect((host, 60111))
                data = "exit_"
                s.sendto(data.encode('utf-8'), (host, 60111))
                pass
        return

    app = QApplication(sys.argv)
    window = MainWindow(icon=LogoPath,
                        title=Name_ + " " + Version,
                        socket=s,
                        Version=Version,
                        UpdateUrl=UpdateUrl,
                        CurPath=CurPath,
                        DirPath=DirPath,
                        Name_=Name_,
                        LogoPath=LogoPath,
                        Name=Name,
                        ExePath=ExePath)
    window.setWindowTitle(Name_ + " " + Version + " 开源软件")
    window.setWindowIcon(QIcon(LogoPath))
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

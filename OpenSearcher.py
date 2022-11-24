import datetime
import os
import socket
import sys
import traceback
from queue import Queue
import win32api
import win32con
import winshell
from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex, QThread, pyqtSignal, QTimer, QProcess
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDesktopWidget, QMessageBox, qApp
from sqlitedict import SqliteDict
from qcustomdialog.HelpWindow import HelpWindow
from qcustomdialog.IndexWindow import IndexWindow
from qcustomdialog.SettingWindow import SettingWindow
from qcustomdialog.UpdateWindow import UpdateWindow
from MainWindow import Ui_MainWindow
from qutils.searchthread import SearchThread
from qutils.traythread import TrayThread
import logging
from qutils.util import is_user_admin, run_as_admin, create_right_menu, remove_right_menu, create_shortcut


class MainWindow(QMainWindow):
    def __init__(self, icon, title, version, update_url, socket, CurPath, dir_path):
        super().__init__()
        self.icon = icon
        self.title = title
        self.version = version
        self.update_url = update_url
        self.CurPath = CurPath
        self.socket = socket
        self.dir_path = dir_path

        self.LogPath = os.path.abspath(os.path.join(self.CurPath, "logs"))
        self.HelpPath = os.path.abspath(os.path.join(self.CurPath, 'HELP.md'))
        self.SettingPath = os.path.abspath(os.path.join(self.CurPath, 'setting.db'))
        self.TempPath = os.path.abspath(os.path.join(self.CurPath, '.temp'))
        self.ErrorTempPath = os.path.abspath(os.path.join(self.CurPath, '.errortemp'))
        self.IconPath = os.path.abspath(os.path.join(self.CurPath, "icon"))

        self.isMax = False
        self.search_running = False
        self.queue = Queue()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.__init2__()
        self.InitComboBox()
        self.SetTrayIcon()
        self.InitLogger()
        self.RelayUpdate()

    def __init2__(self):
        if self.dir_path is not None:
            print("参数启动")
            self.ui.file_edit.setText(self.dir_path)

        # 控件初始化
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
        self.ui.tableView.clicked.connect(self.onClickedTableView)
        self.ui.listView_error.clicked.connect(self.onClickedListView)
        self.ui.listView_all.clicked.connect(self.onClickedListView_)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.UpdateUi)
        self.timer.start(150)

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

    '''-----------------------------------主窗体-----------------------------------------------'''

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
        self.search_dir_path = QFileDialog.getExistingDirectory(self, '选择文件夹', self.CurPath)
        self.ui.file_edit.setText(self.search_dir_path)

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

    def InitComboBox(self):
        items = ["Microsoft Word 97-2003 文件（.doc）",
                 "Microsoft Word 文件（.docx）",
                 "Microsoft Excel 97-2003 文件（.xls）",
                 "Microsoft Excel 文件（.xlsx）",
                 "PDF 文件（.pdf）",
                 "文本文档（.txt）"]
        items_icon = [os.path.abspath(os.path.join(self.IconPath, 'doc.png')),
                      os.path.abspath(os.path.join(self.IconPath, 'docx.png')),
                      os.path.abspath(os.path.join(self.IconPath, 'xls.png')),
                      os.path.abspath(os.path.join(self.IconPath, 'xlsx.png')),
                      os.path.abspath(os.path.join(self.IconPath, 'pdf.png')),
                      os.path.abspath(os.path.join(self.IconPath, 'txt.png'))]
        first_item = '全部文件类型'
        first_item_icon = os.path.abspath(os.path.join(self.IconPath, 'sysfile.png'))
        line_edit_icon = os.path.abspath(os.path.join(self.IconPath, 'sysfile.png'))

        self.ui.comboBox.InitComboBox(
            line_edit_icon=line_edit_icon,
            first_item=first_item, first_item_icon=first_item_icon,
            items=items, items_icon=items_icon)

    def InitLogger(self):
        if not os.path.isdir(self.LogPath):
            os.makedirs(self.LogPath)
        self.logger = logging.getLogger()
        logging.basicConfig(level='INFO', format='%(asctime)s: %(message)s')
        fmt = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s:%(message)s'
        fh = logging.FileHandler(
            os.path.abspath(os.path.join(self.LogPath, f'{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.txt')),
            encoding="utf8")
        fh.setFormatter(logging.Formatter(fmt=fmt))
        fh.setLevel(logging.INFO)
        self.logger.addHandler(fh)

    def RelayUpdate(self):
        """耗时操作"""
        self.ui.frame.setEnabled(False)
        self.relay_thread = RelayUpdateThread(self.queue, self.socket, self.CurPath, self.SettingPath)
        self.relay_thread.update_setting.connect(self.InitSetting)
        self.relay_thread.update_dir.connect(self.InitDir)
        self.relay_thread.update_textframe.connect(self.InitTextFrame)
        self.relay_thread.complete.connect(self.InitComplete)
        self.relay_thread.start()

    def InitTextFrame(self, content):
        self.ui.textframe.Init(fontsize=content[0], fontfamily=content[1], linewrap=content[2], linenumber=content[3],
                               mysetting_dict=self.mysetting_dict)

    def InitDir(self, dir):
        self.ui.file_edit.setText(dir)
        if self.isMinimized() or not self.isVisible():
            self.setWindowFlags(QtCore.Qt.Window)
            self.activateWindow()
            if self.isMax:
                self.showMaximized()
            else:
                self.showNormal()

    def InitSetting(self, setting):
        self.mysetting_dict = setting
        self._auto_run = self.mysetting_dict['_auto_run']
        self._last_dir = self.mysetting_dict['_last_dir']
        self._right_click_menu = self.mysetting_dict['_right_click_menu']
        self._remind = self.mysetting_dict['_remind']
        self._show_all = self.mysetting_dict['_show_all']
        self._limit_file_size = self.mysetting_dict['_limit_file_size']

    def InitComplete(self):
        self.ui.frame.setEnabled(True)

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

    '''-----------------------------------系统托盘-----------------------------------------------'''

    def SetTrayIcon(self, f=True):
        if f:
            self.backend_thread = TrayThread(icon=self.icon, title=self.title)
            self.backend_thread.start()
            self.backend_thread.setting.connect(self.onClickedShowSettingWindow)
            self.backend_thread.show.connect(self.onClickedShow)
            self.backend_thread.help.connect(self.onClickedHelpWindow)
            self.backend_thread.exit.connect(self.onClickedExit)
            self.backend_thread.update.connect(self.onClickedUpdate)
            self.backend_thread.restart.connect(self.restart_real_live)

    def restart_real_live(self):
        """ 进程控制实现自动重启"""
        qApp.quit()
        self.p = QProcess
        print(qApp.applicationFilePath())
        print(sys.executable, sys.argv)
        s = self.p.startDetached(sys.executable, sys.argv)

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

    def onClickedExit(self):
        self.setVisible(False)  # 托盘图标会自动消失
        QApplication.instance().quit()
        sys.exit(0)

    def onClickedShowSettingWindow(self):
        if self.isMinimized() or not self.isVisible():
            self.setWindowFlags(QtCore.Qt.Window)
            self.activateWindow()
            if self.isMax:
                self.showMaximized()
            else:
                self.showNormal()
        self.ShowSettingWindow()

    def ShowSettingWindow(self):
        settingwindow = SettingWindow(self, self.queue)
        settingwindow.show()

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
                self.mysetting_dict["_search_dir"]=self.search_dirname
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
    complete = pyqtSignal()

    def __init__(self, queue, socket, CurPath, SettingPath):
        super().__init__()
        self.queue = queue
        self.CurPath = CurPath
        self.socket = socket
        self.SettingPath = SettingPath

    def run(self):
        self.setting()
        self.init_textframe()
        if self.mysetting_dict["_last_dir"]:
            self.update_dir.emit(self.mysetting_dict["_search_dir"])

        self.complete.emit()
        while True:
            data, addr = self.socket.recvfrom(1024)
            dir_path = data.decode("utf-8")
            self.update_dir.emit(dir_path)

    def init_textframe(self):
        self.update_textframe.emit([
            self.mysetting_dict['_fontsize'],
            self.mysetting_dict['_fontfamily'],
            self.mysetting_dict['_linewrap'],
            self.mysetting_dict['_linenumber'],
        ])

    def setting(self):
        if not os.path.exists(self.SettingPath):
            print("第一次运行")
            self.mysetting_dict = SqliteDict(self.SettingPath, autocommit=True)
            self.mysetting_dict.clear()
            self.mysetting_dict['_auto_run'] = True
            self.mysetting_dict['_last_dir'] = True
            self.mysetting_dict['_search_dir'] = ""
            self.mysetting_dict['_right_click_menu'] = True
            self.mysetting_dict['_remind'] = True
            self.mysetting_dict['_show_all'] = False
            self.mysetting_dict['_limit_file_size'] = 100
            self.mysetting_dict['_fontsize'] = 10
            self.mysetting_dict['_fontfamily'] = "宋体"
            self.mysetting_dict['_linewrap'] = True
            self.mysetting_dict['_linenumber'] = True
            self.update_setting.emit(self.mysetting_dict)
            self.init_auto()
            self.init_right_click()
        else:
            self.mysetting_dict = SqliteDict(self.SettingPath, autocommit=True)
            self.update_setting.emit(self.mysetting_dict)

    def init_auto(self):
        name = 'OpenSearcher'
        path = sys.argv[0]
        # path = os.path.abspath(os.path.join(self.CurPath, "OpenSearcher.exe"))
        KeyName = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
        win32api.RegSetValueEx(key, name, 0, win32con.REG_SZ, path)
        print('开启软件自启动')

    def init_right_click(self):
        if not is_user_admin():
            run_as_admin("set_menu")
            return


def main():
    print(sys.argv)

    Name = "Open Searcher"
    KeyName = "OpenSearcher"
    Version = "0.0.2"
    UpdateUrl = "https://aidcs-1256440297.cos.ap-beijing.myqcloud.com/OpenSearcher/update.txt"
    ExePath = sys.argv[0]
    CurPath = os.path.dirname(os.path.abspath(ExePath))
    os.environ['REQUESTS_CA_BUNDLE'] = os.path.abspath(os.path.join(CurPath, 'cacert.pem'))
    LogoPath = os.path.abspath(os.path.join(CurPath, "icon/logo.ico"))
    LnkPath = os.path.abspath(os.path.join(winshell.desktop(), "Open Searcher" + ".lnk"))
    LnkPath2 = os.path.abspath(os.path.join(winshell.common_desktop(), "Open Searcher" + ".lnk"))
    # 判断是否是设置菜单
    if len(sys.argv) > 1:
        if sys.argv[-1] == "set_menu":
            try:
                # icon 设置成 exe文件也可以，Windows系统会自动读取ico
                create_right_menu(name=KeyName, content=Name + " 搜索", icon=LogoPath, command=ExePath + " \"%L\"",
                                  type_="DIRECTORY")
                create_right_menu(name=KeyName, content=Name + " 搜索", icon=LogoPath, command=ExePath + " \"%W\"",
                                  type_="DIRECTORY_BACKGROUND")
            except Exception:
                traceback.print_exc()
            return
        elif sys.argv[-1] == "del_menu":
            try:
                remove_right_menu(KeyName, type_="DIRECTORY")
                remove_right_menu(KeyName, type_="DIRECTORY_BACKGROUND")
            except Exception:
                traceback.print_exc()
            return

    # 判断是否已经启动
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        host = socket.gethostname()
        s.bind((host, 60111))
    except:
        print('程序已经在运行了')
        if len(sys.argv) > 1:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            host = socket.gethostname()
            s.connect((host, 60111))
            data = sys.argv[1]
            s.sendto(data.encode('utf-8'), (host, 60111))
        else:
            win32api.MessageBox(0, "提示：Open Searcher程序已经在运行中了", Name, win32con.MB_OK)
        return

    # 判断是否有桌面图标
    if not os.path.exists(LnkPath) and not os.path.exists(LnkPath2):
        print("桌面没有创建快捷方式")
        create_shortcut(ExePath, Name, "一个开源的、本地的、安全的、支持全文检索的搜索器。", LogoPath)

    app = QApplication(sys.argv)
    if len(sys.argv) > 1:
        dir_path = sys.argv[1]
    else:
        dir_path = None
    screen = QDesktopWidget().screenGeometry()
    height = screen.height() * 6 / 7
    width = screen.width() * 9 / 10
    window = MainWindow(icon=LogoPath, title=Name + " " + Version, version=Version, update_url=UpdateUrl,
                        CurPath=CurPath, socket=s, dir_path=dir_path)
    window.setGeometry(int((screen.width() - width) / 2), int((screen.height() - height) / 2), int(width), int(height))
    window.setWindowTitle(Name + " " + Version)
    window.setWindowIcon(QIcon(LogoPath))
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

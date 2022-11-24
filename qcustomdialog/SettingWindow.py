import sys
import win32api
import win32con
from PyQt5.QtWidgets import QMainWindow
from qcustomdialog import setting
from qutils.util import is_user_admin, run_as_admin, create_right_menu, remove_right_menu


class SettingWindow(QMainWindow):
    def __init__(self, parent_window=None, queue=None):
        super().__init__(parent_window)
        self.mysetting_dict = parent_window.mysetting_dict
        self.queue = queue
        self.parent_window = parent_window
        self.CurPath = parent_window.CurPath

        self.child = setting.Ui_MainWindow()
        self.child.setupUi(self)
        self.setWindowTitle("设置")

        self.__init2__()

    def __init2__(self):
        self.child.spinBox_limit_file_size.setValue(self.mysetting_dict["_limit_file_size"])
        self.child.checkBox_show_all.setChecked(self.mysetting_dict["_show_all"])
        self.child.checkBox_auto_run.setChecked(self.mysetting_dict["_auto_run"])
        self.child.checkBox_remind.setChecked(self.mysetting_dict["_remind"])
        self.child.checkBox_last_dir.setChecked(self.mysetting_dict["_last_dir"])

        self.child.button_fix.clicked.connect(self.right_click_fix)
        self.child.button_del.clicked.connect(self.right_click_del)
        self.child.checkBox_auto_run.stateChanged.connect(self.checkBox_auto_run)
        self.child.checkBox_show_all.stateChanged.connect(self.checkBox_show_all)
        self.child.checkBox_remind.stateChanged.connect(self.checkBox_remind)
        self.child.checkBox_last_dir.stateChanged.connect(self.checkBox_last_dir)
        self.child.spinBox_limit_file_size.valueChanged.connect(self.spinBox_limit_file_size)

    def checkBox_auto_run(self):
        name = 'Y Searcher'
        path = sys.argv[0]
        KeyName = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
        if self.child.checkBox_auto_run.isChecked():
            win32api.RegSetValueEx(key, name, 0, win32con.REG_SZ, path)
            print('开启软件自启动')
        else:
            self.parent_window._auto_run = False
            win32api.RegDeleteValue(key, name)
            print('关闭软件自启动')
        self.mysetting_dict["_auto_run"] = self.child.checkBox_auto_run.isChecked()
        win32api.RegCloseKey(key)

    def checkBox_show_all(self):
        if self.child.checkBox_show_all.isChecked():
            self.parent_window._show_all = True
        else:
            self.parent_window._show_all = False
            self.queue.put(("_show_all", 0))
        self.mysetting_dict["_show_all"] = self.child.checkBox_show_all.isChecked()

    def checkBox_last_dir(self):
        self.mysetting_dict["_last_dir"] = self.child.checkBox_last_dir.isChecked()

    def checkBox_remind(self):
        if self.child.checkBox_remind.isChecked():
            self.parent_window._remind = True
        else:
            self.parent_window._remind = False
        self.mysetting_dict["_remind"] = self.child.checkBox_remind.isChecked()

    def spinBox_limit_file_size(self):
        _limit_file_size = self.child.spinBox_limit_file_size.value()
        self.parent_window._limit_file_size = _limit_file_size
        self.mysetting_dict["_limit_file_size"] = _limit_file_size

    def right_click_fix(self):
        if not is_user_admin():
            run_as_admin("set_menu")
            return

    def right_click_del(self):
        if not is_user_admin():
            run_as_admin("del_menu")
            return

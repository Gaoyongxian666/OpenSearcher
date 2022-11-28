import os
import sys
import traceback

import win32api
import win32con
from PyQt5.QtWidgets import QMainWindow
from qcustomdialog import setting
from qutils.util import is_user_admin, run_as_admin, create_right_menu, remove_right_menu, create_shortcut


class SettingWindow(QMainWindow):
    def __init__(self, parent_window=None):
        super().__init__(parent_window)
        self.mysetting_dict = parent_window.mysetting_dict
        self.queue = parent_window.queue
        self.parent_window = parent_window
        self.CurPath = parent_window.CurPath
        self.Name = parent_window.Name
        self.Name_ = parent_window.Name_
        self.LogoPath = parent_window.LogoPath
        self.ExePath = parent_window.ExePath
        self.LnkPath = parent_window.LnkPath
        self.LnkPath2 = parent_window.LnkPath2

        self.child = setting.Ui_MainWindow()
        self.child.setupUi(self)
        self.setWindowTitle("设置")

        self.Init()

    def Init(self):
        self.child.spinBox_limit_file_size.setValue(self.mysetting_dict["_limit_file_size"])
        self.child.checkBox_show_all.setChecked(self.mysetting_dict["_show_all"])
        self.child.checkBox_desktop.setChecked(self.mysetting_dict["_desktop"])
        self.child.checkBox_remind.setChecked(self.mysetting_dict["_remind"])
        self.child.checkBox_last_dir.setChecked(self.mysetting_dict["_last_dir_flag"])
        self.child.checkBox_last_screen.setChecked(self.mysetting_dict["_last_screen_flag"])
        self.child.groupBox_auto_run.setChecked(self.mysetting_dict["_auto_run"])
        self.child.groupBox_right_menu.setChecked(self.mysetting_dict["_right_menu"])

        self.child.button_fix_right.clicked.connect(self.fix_right)
        self.child.button_fix_auto.clicked.connect(self.fix_auto)
        self.child.groupBox_auto_run.clicked.connect(self.groupBox_auto_run)
        self.child.groupBox_right_menu.clicked.connect(self.groupBox_right_menu)
        self.child.checkBox_show_all.stateChanged.connect(self.checkBox_show_all)
        self.child.checkBox_remind.stateChanged.connect(self.checkBox_remind)
        self.child.checkBox_last_dir.stateChanged.connect(self.checkBox_last_dir)
        self.child.checkBox_last_screen.stateChanged.connect(self.checkBox_last_screen)
        self.child.checkBox_desktop.stateChanged.connect(self.checkBox_desktop)
        self.child.spinBox_limit_file_size.valueChanged.connect(self.spinBox_limit_file_size)

    def groupBox_auto_run(self):
        if self.child.groupBox_auto_run.isChecked():
            if self.fix_auto():
                self.mysetting_dict["_auto_run"] = self.child.groupBox_auto_run.isChecked()
            else:
                self.child.groupBox_auto_run.setChecked(not self.child.groupBox_right_menu.isChecked())
        else:
            if self.del_auto():
                self.mysetting_dict["_auto_run"] = self.child.groupBox_auto_run.isChecked()
            else:
                self.child.groupBox_auto_run.setChecked(not self.child.groupBox_right_menu.isChecked())

    def fix_auto(self):
        try:
            KeyName = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key, self.Name, 0, win32con.REG_SZ, self.ExePath)
            print('开启软件自启动')
            win32api.RegCloseKey(key)
            return True
        except:
            win32api.MessageBox(0, traceback.format_exc(), self.Name_, win32con.MB_OK)
            return False

    def del_auto(self):
        try:
            KeyName = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
            win32api.RegDeleteValue(key, self.Name)
            print('关闭软件自启动')
            win32api.RegCloseKey(key)
            return True

        except:
            win32api.MessageBox(0, traceback.format_exc(), self.Name_, win32con.MB_OK)

            return False

    def groupBox_right_menu(self):
        if self.child.groupBox_right_menu.isChecked():
            if self.fix_right():
                self.mysetting_dict["_right_menu"] = self.child.groupBox_right_menu.isChecked()
            else:
                self.child.groupBox_right_menu.setChecked(not self.child.groupBox_right_menu.isChecked())
        else:
            if self.del_right():
                self.mysetting_dict["_right_menu"] = self.child.groupBox_right_menu.isChecked()
            else:
                self.child.groupBox_right_menu.setChecked(not self.child.groupBox_right_menu.isChecked())

    def fix_right(self):
        if not is_user_admin():
            return run_as_admin("set_menu")
        else:
            try:
                create_right_menu(name=self.Name, content=self.Name_ + " 搜索", icon=self.LogoPath,
                                  command=self.ExePath + " \"%L\"",
                                  type_="DIRECTORY")
                create_right_menu(name=self.Name, content=self.Name_ + " 搜索", icon=self.LogoPath,
                                  command=self.ExePath + " \"%W\"",
                                  type_="DIRECTORY_BACKGROUND")
                return True
            except Exception:
                win32api.MessageBox(0, traceback.format_exc(), self.Name_, win32con.MB_OK)
                return False

    def del_right(self):
        if not is_user_admin():
            return run_as_admin("del_menu")
        else:
            try:
                remove_right_menu(self.Name, type_="DIRECTORY")
                remove_right_menu(self.Name, type_="DIRECTORY_BACKGROUND")
                return True
            except Exception:
                win32api.MessageBox(0, traceback.format_exc(), self.Name_, win32con.MB_OK)
                return False

    def checkBox_show_all(self):
        if self.child.checkBox_show_all.isChecked():
            self.parent_window._show_all = True
        else:
            self.parent_window._show_all = False
            self.queue.put(("_show_all", 0))
        self.mysetting_dict["_show_all"] = self.child.checkBox_show_all.isChecked()

    def checkBox_last_dir(self):
        self.mysetting_dict["_last_dir_flag"] = self.child.checkBox_last_dir.isChecked()

    def checkBox_last_screen(self):
        self.mysetting_dict["_last_screen_flag"] = self.child.checkBox_last_screen.isChecked()

    def checkBox_desktop(self):
        if self.child.checkBox_desktop.isChecked():
            if not os.path.exists(self.LnkPath) and not os.path.exists(self.LnkPath2):
                print("桌面没有创建快捷方式")
                create_shortcut(sys.argv[0], self.Name_, "一个开源的、本地的、安全的、支持全文检索的搜索器。", self.LogoPath)
        self.mysetting_dict["_desktop"] = self.child.checkBox_desktop.isChecked()

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

import json
import os
import sys
import webbrowser

import pywin10
import win32gui
from PyQt5.QtCore import QThread, pyqtSignal


class TrayThread(QThread):
    show = pyqtSignal()
    exit = pyqtSignal()
    update = pyqtSignal()
    help = pyqtSignal()
    restart = pyqtSignal()
    setting = pyqtSignal()

    def __init__(self, icon, title):
        super().__init__()
        self.icon = icon
        self.title = title
        self.promote = False

    def run(self):
        path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "promote.txt"))
        if os.path.exists(path):
            self.promote = True
            with open(path, "r", encoding="utf8") as f:
                self.promote_url = f.readline()
                self.config_dict = json.loads(self.promote_url)

            self.t = pywin10.TaskBarIcon(
                left_click=self.show__,
                icon=self.icon,
                hover_text=self.title,
                menu_options=[
                    ['退出', "exit.ico", self.exit__, 1],
                    ['重新启动', "update.ico", self.restart__, 9],
                    ["分隔符", None, None, 111],

                    ['检查更新', "update.ico", self.update__, 4],
                    ['帮助', "help.ico", self.help__, 3],

                    ["分隔符", None, None, 333],

                    ['开源地址', "help.ico", self.github__, 8],
                    [self.config_dict["name"], "help.ico", self.pojie__, 10],

                    ["分隔符", None, None, 222],
                    ['设置', "home.ico", self.setting__, 2],
                ],
                menu_style="normal",
                icon_x_pad=12
            )
        else:
            self.t = pywin10.TaskBarIcon(
                left_click=self.show__,
                icon=self.icon,
                hover_text=self.title,
                menu_options=[
                    ['退出', "exit.ico", self.exit__, 1],
                    ['重新启动', "update.ico", self.restart__, 9],
                    ["分隔符", None, None, 111],

                    ['检查更新', "update.ico", self.update__, 4],
                    ['帮助', "help.ico", self.help__, 3],

                    ["分隔符", None, None, 333],

                    ['开源地址', "help.ico", self.github__, 8],

                    ["分隔符", None, None, 222],
                    ['设置', "home.ico", self.setting__, 2],
                ],
                menu_style="normal",
                icon_x_pad=12
            )

        win32gui.PumpMessages()

    def pojie__(self):
        webbrowser.open_new_tab(self.config_dict["url"])

    def ShowToast(self, msg):
        self.t.ShowToast("提示", msg=msg)

    def restart__(self):
        self.restart.emit()

    def show__(self):
        self.show.emit()

    def setting__(self):
        self.setting.emit()

    def exit__(self):
        self.exit.emit()

    def update__(self):
        self.update.emit()

    def help__(self, **kwargs):
        self.help.emit()

    def github__(self):
        webbrowser.open("https://github.com/Gaoyongxian666/OpenSearcher")

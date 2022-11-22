import json
import os.path
import traceback
import webbrowser
import requests
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow
from qcustomdialog import update


class UpdateWindow(QMainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.child = update.Ui_MainWindow()
        self.child.setupUi(self)

        self.version = parent.version
        self.logger = parent.logger
        self.CurPath = parent.CurPath
        self.update_url = parent.update_url
        self.software_url = ""

        self.setWindowTitle("检查更新")
        self.child.cancel.clicked.connect(self.cancel_)
        self.child.ok.clicked.connect(self.ok_)
        self.child.ok.hide()
        self.child.cancel.hide()

        self.RelayUpdate()

    def RelayUpdate(self):
        self.relay_thread = RelayUpdateThread(self.CurPath, self.version, self.logger, self.update_url)
        self.relay_thread.need.connect(self.need)
        self.relay_thread.noneed.connect(self.noneed)
        self.relay_thread.error.connect(self.error)
        self.relay_thread.start()

    def need(self, content):
        self.update_version = content[0]
        self.software_url = content[1]
        self.child.label.setText("发现新版本：Open Searcher V" + self.update_version)
        self.child.ok.show()
        self.child.cancel.show()

    def noneed(self):
        self.child.label.setText("当前已经是最新版本")
        self.child.cancel.show()

    def error(self):
        self.child.label.setText("当前网络错误（请检查网络，关闭代理）")
        self.child.cancel.show()

    def ok_(self):
        if self.version != self.update_version:
            webbrowser.open_new_tab(self.software_url)
        self.close()

    def cancel_(self):
        self.close()


class RelayUpdateThread(QThread):
    need = pyqtSignal(tuple)
    noneed = pyqtSignal()
    error = pyqtSignal()

    def __init__(self, dir_path, version, logger, update_url):
        super().__init__()
        self.dir_path = dir_path
        self.version = version
        self.logger = logger
        self.update_url = update_url

    def run(self):
        update_path = os.path.abspath(os.path.join(self.dir_path, "update.txt"))
        try:
            with open(update_path, "wb") as f:
                f.write(requests.get(self.update_url).content)
            with open(update_path, "r", encoding='utf8') as f:
                config = f.readline()
            config_dict = json.loads(config)
            if self.version != config_dict["version"]:
                self.need.emit((config_dict["version"], config_dict["url"]))
            else:
                self.noneed.emit()
        except:
            self.logger.info(traceback.format_exc())
            self.error.emit()

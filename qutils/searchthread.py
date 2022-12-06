import hashlib
import logging
import os
import traceback
import pythoncom
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QStandardItem

from qutils.killwindow import KillAllOffice
from qutils.util import file_name_list, get_text

logger = logging.getLogger(__name__)


class SearchThread(QThread):
    stoped = pyqtSignal()

    def __init__(self, DirPaths: list, CurPath, types, logger, queue, mysetting_dict, IconDict, keywords=None):
        super().__init__()
        self.DirPaths = DirPaths
        self.CurPath = CurPath
        self.IconDict = IconDict
        self.types = types
        self.keywords = keywords
        self.logger = logger
        self.queue = queue
        self.mysetting_dict = mysetting_dict

        self._limit_office_time = self.mysetting_dict["_limit_office_time"]
        self._limit_file_size = self.mysetting_dict["_limit_file_size"]
        self._exclude_dir = self.mysetting_dict["_exclude_dir"]
        self._show_all = self.mysetting_dict["_show_all"]

        self.file_name_lists = []
        self.search_runing = [True]
        self.temp_path = os.path.abspath(os.path.join(self.CurPath, '.temp'))
        self.error_temp_path = os.path.abspath(os.path.join(self.CurPath, '.errortemp'))
        self.icon_dir = os.path.abspath(os.path.join(self.CurPath, 'icon'))
        self.antiword_path = os.path.abspath(os.path.join(self.CurPath, 'antiword/antiword.exe'))

    def run(self):
        pythoncom.CoInitialize()
        if not os.path.isdir(self.temp_path):
            os.makedirs(self.temp_path)
            self.logger.info("不存在就创建目录：" + self.temp_path)
        if not os.path.isdir(self.error_temp_path):
            os.makedirs(self.error_temp_path)
            self.logger.info("不存在就创建目录：" + self.error_temp_path)
        self.md5_list = [name for name in os.listdir(self.temp_path) if
                         os.path.isfile(os.path.join(self.temp_path, name))]
        all = 0
        selected = 0
        haskey = 0
        error = 0
        for dir_path in self.DirPaths:
            if not self.search_runing[0]:
                self.md5_list.clear()
                self.file_name_lists.clear()
                break
            file_name_dict = file_name_list(
                dir_path=dir_path, types=self.types, IconDict=self.IconDict,
                size_limit=self._limit_file_size, exclude=self._exclude_dir, search_running=self.search_runing)
            file_name_list_ = file_name_dict["list"]
            all_ = file_name_dict["all"]
            selected_ = file_name_dict["selected"]
            all = all + all_
            selected = selected + selected_
            self.file_name_lists.extend(file_name_list_)
        file_name_lists_num = str(len(self.file_name_lists))
        file_name_lists_places = len(file_name_lists_num)
        self.logger.info(str(self.file_name_lists))
        self.queue.put(("update_search_info", {"all": all, "selected": selected}))
        self.queue.put(("append_text", str(self.file_name_lists)))
        for i, file_n_l in enumerate(self.file_name_lists):
            if not self.search_runing[0]:
                self.md5_list.clear()
                self.file_name_lists.clear()
                break
            self.logger.info("当前正搜索文件:" + file_n_l[2][1])
            self.queue.put(("append_text", "当前正搜索文件:" + file_n_l[2][1]))
            self.queue.put(("update_top_lable", str(i).rjust(file_name_lists_places) + "/" + file_name_lists_num))
            if self.keywords is None:
                self.write_temp(absolute_path=file_n_l[2][1], file_suffix=file_n_l[3][1])
            else:
                if self._show_all:
                    item1 = QStandardItem(file_n_l[0][0], file_n_l[0][1] + "  -> (" + file_n_l[2][1] + ")")
                    self.queue.put(("all", item1))
                flag = self.write_temp(absolute_path=file_n_l[2][1], file_suffix=file_n_l[3][1])
                if flag == 1:
                    self.queue.put(("trigger", file_n_l))
                    haskey = haskey + 1
                elif flag == 0:
                    item2 = QStandardItem(file_n_l[0][0], file_n_l[0][1] + "  -> (" + file_n_l[2][1] + ")")
                    self.queue.put(("error", item2))
                    error = error + 1
                self.queue.put(("update_search_info", {"haskey": haskey, "error": error}))
        KillAllOffice()

    def stop(self):
        self.search_runing[0] = False
        self.stoped.emit()

    def write_temp(self, absolute_path, file_suffix=".txt") -> int:
        try:
            with open(absolute_path, 'rb') as f:
                file_md5 = hashlib.md5(f.read()).hexdigest()
            temp_md5_path = os.path.abspath(os.path.join(self.temp_path, file_md5))
            if file_md5 in self.md5_list:
                self.logger.info("存在缓存文件：" + temp_md5_path + "\n")
                if self.keywords is not None:
                    with open(temp_md5_path, "r", encoding="utf8") as f:
                        text = f.read()
                    if self.keywords in text:
                        return 1
                    else:
                        self.logger.info("没找到\n")
                        return 2
            else:
                try:
                    text = get_text(file_suffix=file_suffix, file_absolute_path=absolute_path, file_md5=file_md5,
                                    temp_path=self.temp_path, antiword_path=self.antiword_path,
                                    _limit_office_time=self._limit_office_time)
                    with open(absolute_path, 'rb') as f:
                        file_md5 = hashlib.md5(f.read()).hexdigest()
                    temp_md5_path = os.path.abspath(os.path.join(self.temp_path, file_md5))
                    with open(temp_md5_path, 'w', encoding='utf8') as f:
                        f.write(text)
                    self.logger.info("写入完成:" + temp_md5_path + "\n")
                    self.queue.put(("append_text", "写入完成:" + temp_md5_path + "\n"))

                    if self.keywords is not None:
                        if self.keywords in text:
                            self.logger.info("写入完成:找到关键词\n")
                            return 1
                        else:
                            self.logger.info("写入完成:没找到\n")
                            return 2
                except:
                    with open(absolute_path, 'rb') as f:
                        file_md5 = hashlib.md5(f.read()).hexdigest()
                    error_temp_md5_path = os.path.abspath(os.path.join(self.error_temp_path, file_md5))
                    self.queue.put(("append_text", "处理文件时发生错误"))
                    self.queue.put(("append_text", traceback.format_exc()))
                    self.logger.info("处理文件时发生错误")
                    self.logger.info(traceback.format_exc())
                    with open(error_temp_md5_path, 'w', encoding="utf8") as f:
                        f.write(absolute_path + "\n\n" + traceback.format_exc())
                    return 0
        except:
            self.logger.info("发生了无法记录的错误。无法获取文件md5，需要用表格来记录。")
            self.logger.info(traceback.format_exc())
            return 0

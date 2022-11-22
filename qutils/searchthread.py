import hashlib
import os
import traceback
import pythoncom
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QStandardItem
from qutils.util import file_name_list, get_text


class SearchThread(QThread):
    def __init__(self, DirPaths: list, CurPath, screen, keywords, logger, queue, show_all, _limit_file_size):
        super().__init__()
        self.DirPaths = DirPaths
        self.CurPath = CurPath
        self.screen = screen
        self.keywords = keywords
        self.logger = logger
        self.queue = queue
        self._limit_file_size = _limit_file_size
        self.show_all = show_all
        self.temp_path = os.path.abspath(os.path.join(self.CurPath, '.temp'))
        self.error_temp_path = os.path.abspath(os.path.join(self.CurPath, '.errortemp'))
        self.file_name_lists = []
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
        for dir_path in self.DirPaths:
            self.file_name_lists.extend(file_name_list(file_dir=dir_path, screen=self.screen, icon_dir=self.icon_dir,
                                                       size_limit=self._limit_file_size))

        file_name_lists_num = str(len(self.file_name_lists))
        file_name_lists_places = len(file_name_lists_num)
        self.logger.info(str(self.file_name_lists))

        for i, file_n_l in enumerate(self.file_name_lists):
            self.logger.info("当前正搜索文件:" + file_n_l[3][1])
            self.queue.put(("update_top_lable", str(i).rjust(file_name_lists_places) + "/" + file_name_lists_num))
            if self.show_all:
                item1 = QStandardItem(file_n_l[0][0], file_n_l[0][1] + "  -> (" + file_n_l[3][1] + ")")
                self.queue.put(("all", item1))
            flag = self.write_temp(absolute_path=file_n_l[3][1], file_suffix=file_n_l[4][1])
            if flag == 1:
                self.queue.put(("trigger", file_n_l))
            elif flag == 0:
                item2 = QStandardItem(file_n_l[0][0], file_n_l[0][1] + "  -> (" + file_n_l[3][1] + ")")
                self.queue.put(("error", item2))
        self.queue.put(("completed", 1))

    def write_temp(self, absolute_path, file_suffix=".txt") -> int:
        with open(absolute_path, 'rb') as f:
            file_md5 = hashlib.md5(f.read()).hexdigest()
        temp_md5_path = os.path.abspath(os.path.join(self.temp_path, file_md5))
        error_temp_md5_path = os.path.abspath(os.path.join(self.error_temp_path, file_md5))

        if file_md5 in self.md5_list:
            self.logger.info("存在缓存文件：" + temp_md5_path + "\n")
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
                                temp_path=self.temp_path, antiword_path=self.antiword_path)
                with open(temp_md5_path, 'w', encoding='utf8') as f:
                    f.write(text)
                if self.keywords in text:
                    self.logger.info("写入完成:" + temp_md5_path + "\n")
                    return 1
                else:
                    self.logger.info("没找到\n")
                    return 2
            except:
                self.logger.info("处理文件时发生错误")

                with open(error_temp_md5_path, 'w', encoding="utf8") as f:
                    f.write(absolute_path + "\n\n" + traceback.format_exc())
                self.logger.info(traceback.format_exc())
                return 0

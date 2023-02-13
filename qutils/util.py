import ctypes
import hashlib
import logging
import os
import sys
import traceback
import warnings
import winreg
from ctypes import *

import chardet
import pdfminer.high_level
import win32api
import win32clipboard
import win32con
import winshell
from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import qApp
from win32comext.shell.shell import ShellExecuteEx

from qutils import doc2txt, xls2txt, xlsx2txt, pptx2txt, ppt2txt, epub2txt, mobi2txt, image2txt, docx2txt_, wps2txt, \
    et2txt

logger = logging.getLogger(__name__)


def contains_same_path(path, pathlist):
    """是否存在相同路径"""
    for p in pathlist:
        if os.path.samefile(path, p):
            logger.info("找到相同路径：" + p)
            return True
    return False


def getparentlist(path, pathlist):
    """返回pathlist中path的所有父路径"""
    parentlist = []
    for path_ in pathlist:
        if os.path.realpath(path).startswith(os.path.realpath(path_) + os.sep):
            parentlist.append(path_)
    logger.info("寻找父路径：" + path + "存在父路径" + str(parentlist))
    return parentlist


def getsublist(path, pathlist):
    """返回pathlist中path的所有子路径"""
    sublist = []
    for path_ in pathlist:
        if os.path.realpath(path_).startswith(os.path.realpath(path) + os.sep):
            sublist.append(path_)
    logger.info("寻找子路径：" + path + "存在子路径" + str(sublist))
    return sublist


def file_name_list(dir_path: str, types: list, IconDict, exclude=None, size_limit=100,
                   search_running=None):
    """返回指定类型的文件列表"""
    if search_running is None:
        search_running = [True]
    if exclude is None:
        exclude = []
    L = []
    AllFiles = 0
    SelectedFiles = 0
    if len(getparentlist(dir_path, exclude)) == 0 and not contains_same_path(dir_path, exclude):
        for root, dirs, files in os.walk(dir_path, topdown=True):
            if not search_running[0]:
                break
            dirs[:] = [d for d in dirs if not contains_same_path(os.path.abspath(os.path.join(root, d)), exclude)]
            for file in files:
                AllFiles = AllFiles + 1
                if "~$" not in file:
                    filename = os.path.splitext(file)
                    filename_ = filename[0]
                    suffix = filename[1]
                    if suffix in types and filename_[0] != "$":
                        SelectedFiles = SelectedFiles + 1
                        absolute_path = os.path.abspath(os.path.join(root, file))
                        try:
                            icon_ = IconDict["icon_%s" % suffix[1:]]
                        except:
                            icon_ = IconDict["icon_txt"]
                        if os.path.getsize(absolute_path) < size_limit * 1024 * 1024:
                            L.append([(icon_, file),
                                      (None, getDocSize(absolute_path)),
                                      (None, absolute_path),
                                      (None, suffix)])
                        else:
                            logger.info("文件太大：" + str(getDocSize(absolute_path)) + "。文件路径：" + absolute_path)
    return {"list": L, "all": AllFiles, "selected": SelectedFiles}


def formatSize(bytes):
    """字节bytes转化kb"""
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        logger.info("传入的字节格式不对")
        return "Error"
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.2fG" % (G)
        else:
            return "%.2fM" % (M)
    else:
        return "%.2fkb" % (kb)


def getDocSize(path):
    """获取文件大小"""
    try:
        size = os.path.getsize(path)
        return formatSize(size)
    except Exception as err:
        logger.info(err)
        return "获取失败"


def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
    """将警告信息放在一行"""
    return '%s: %s\n' % (category.__name__, message)


warnings.formatwarning = warning_on_one_line


def setClipboardFiles(paths):
    """剪贴板复制文件"""

    class DROPFILES(Structure):
        _fields_ = [
            ("pFiles", c_uint),
            ("x", c_long),
            ("y", c_long),
            ("fNC", c_int),
            ("fWide", c_bool),
        ]

    pDropFiles = DROPFILES()
    pDropFiles.pFiles = sizeof(DROPFILES)
    pDropFiles.fWide = True
    matedata = bytes(pDropFiles)
    files = ("\0".join(paths)).replace("/", "\\")
    data = files.encode("U16")[2:] + b"\0\0"
    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(
            win32clipboard.CF_HDROP, matedata + data)
    finally:
        win32clipboard.CloseClipboard()


def detect_encoding(text_file, min_confidence=0.98, text_length=1024):
    """获取文件编码"""
    try:
        with open(text_file, 'rb') as text:
            _ = chardet.detect(text.read(text_length))
            encoding, confidence = _.get("encoding"), _.get("confidence")
            if encoding == "ascii":
                encoding = "utf8"
        if confidence < min_confidence:
            encoding = "utf8"
    except:
        encoding = "utf8"
    return encoding


def restart_real_live():
    """ 进程控制实现自动重启"""
    qApp.quit()
    # QProcess 类的作用是启动一个外部的程序并与之交互，并且没有父子关系。
    p = QProcess
    # applicationFilePath() 返回应用程序可执行文件的文件路径
    p.startDetached(qApp.applicationFilePath())


def create_right_menu(name, icon, command, content=None, type_="DIRECTORY_BACKGROUND"):
    """ 创建右键菜单:icon 设置成执行文件也可以读取图标"""
    key_root = winreg.HKEY_CLASSES_ROOT
    if type_ == "DIRECTORY_BACKGROUND":
        key_path = fr"Directory\Background\shell\{name}"
    elif type_ == "DIRECTORY":
        key_path = fr"Directory\shell\{name}"
    with winreg.CreateKey(key_root, key_path) as key:
        if content is not None:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, content)
        winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, icon or '')
        with winreg.CreateKey(key, "command") as key2:
            winreg.SetValueEx(key2, "", 0, winreg.REG_SZ, command or '')


def remove_right_menu(name, type_="DIRECTORY"):
    """删除右键菜单"""
    key_root = 0x80000000  # winreg.HKEY_CLASSES_ROOT
    if type_ == "DIRECTORY_BACKGROUND":
        key_path = fr"Directory\Background\shell\{name}"
    elif type_ == "DIRECTORY":
        key_path = fr"Directory\shell\{name}"
    ctypes.windll.Advapi32.RegDeleteTreeW(key_root, key_path)


def create_shortcut(bin_path: str, name: str, desc: str, icon: str = None):
    """快捷方式的路径，exe文件的路径，名称，图标路径，还有描述信息"""
    try:
        shortcut = os.path.join(winshell.desktop(), name + ".lnk")
        if icon is not None:
            winshell.CreateShortcut(
                Path=shortcut,
                Target=bin_path,
                Icon=(icon, 0),
                Description=desc
            )
        else:
            winshell.CreateShortcut(
                Path=shortcut,
                Target=bin_path,
                Icon=(bin_path, 0),
                Description=desc
            )
        return True
    except ImportError as err:
        logger.info("Well, do nothing as 'winshell' lib may not available on current os")
        logger.info("error detail %s" % str(err))
        return False


def is_user_admin():
    """ 检查admin """
    return ctypes.windll.shell32.IsUserAnAdmin()


def run_as_admin(args):
    """ 管理员运行 """
    script = os.path.abspath(sys.argv[0])
    # args = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else ''
    # logger.info(f"{script} {args}")
    # logger.info(sys.executable)
    try:
        ShellExecuteEx(lpFile=sys.executable, lpParameters=f"{script} {args}",
                       nShow=1, lpVerb='runas')
        logger.info(script + args + "：管理员运行，操作成功")
        return True
    except:
        logger.info(script + args + "：管理员运行，操作失败")
        return False


def set_auto(name, exe_path):
    """设置开机自启"""
    try:
        KeyName = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
        win32api.RegSetValueEx(key, name, 0, win32con.REG_SZ, exe_path)
        logger.info('成功开启软件自启动')
        return True
    except:
        win32api.MessageBox(0, traceback.format_exc(), name, win32con.MB_OK)
        logger.info(traceback.format_exc())
        return False


def set_right_menu(name, content, icon, exe_path):
    """设置空白处、文件夹右键菜单"""
    if not is_user_admin():
        return run_as_admin("set_menu")
    else:
        try:
            create_right_menu(name=name, content=content, icon=icon,
                              command=exe_path + " \"%L\"",
                              type_="DIRECTORY")
            create_right_menu(name=name, content=content + " 搜索", icon=icon,
                              command=exe_path + " \"%W\"",
                              type_="DIRECTORY_BACKGROUND")
            return True
        except Exception:
            win32api.MessageBox(0, traceback.format_exc(), name, win32con.MB_OK)
            logger.info(traceback.format_exc())
            return False


def get_text(_image_types_list, _text_types_list, file_suffix, file_absolute_path, file_md5, temp_path, antiword_path,
             _limit_office_time) -> str:
    """转字符串返回处理结果"""

    image_types_list = [".psd", ".png", ".jpg", ".jpeg", ".raw", ".tiff", ".bmp"]
    image_types_list.extend(_image_types_list)
    txt_types_list = [".txt", ".srt", ".json", ".yaml", ".config", ".md", ".markdown", ".html", ".htm"]
    txt_types_list.extend(_text_types_list)
    print(txt_types_list)
    if file_suffix == ".docx":
        temp_docx_path = os.path.abspath(os.path.join(temp_path, file_md5 + ".docx"))
        text = docx2txt_.process(docx_path=file_absolute_path,
                                 temp_docx_path=temp_docx_path,
                                 _limit_office_time=_limit_office_time)
    elif file_suffix == ".doc":
        temp_docx_path = os.path.abspath(os.path.join(temp_path, file_md5 + ".docx"))
        text = doc2txt.process(doc_path=file_absolute_path,
                               temp_docx_path=temp_docx_path,
                               antiword_path=antiword_path,
                               _limit_office_time=_limit_office_time)
    elif file_suffix == ".xls":
        temp_xlsx_path = os.path.abspath(os.path.join(temp_path, file_md5 + ".xlsx"))
        text = xls2txt.process(xls_path=file_absolute_path,
                               temp_xlsx_path=temp_xlsx_path,
                               _limit_office_time=_limit_office_time)
    elif file_suffix == ".xlsx":
        temp_xlsx_path = os.path.abspath(os.path.join(temp_path, file_md5 + ".xlsx"))
        text = xlsx2txt.process(xlsx_path=file_absolute_path,
                                temp_xlsx_path=temp_xlsx_path,
                                _limit_office_time=_limit_office_time)
    elif file_suffix == ".pptx":
        temp_pptx_path = os.path.abspath(os.path.join(temp_path, file_md5 + ".pptx"))
        text = pptx2txt.process(pptx_path=file_absolute_path,
                                temp_pptx_path=temp_pptx_path,
                                _limit_office_time=_limit_office_time)
    elif file_suffix == ".ppt":
        temp_pptx_path = os.path.abspath(os.path.join(temp_path, file_md5 + ".pptx"))
        text = ppt2txt.process(ppt_path=file_absolute_path,
                               temp_pptx_path=temp_pptx_path,
                               _limit_office_time=_limit_office_time)
    elif file_suffix == ".wps":
        temp_docx_path = os.path.abspath(os.path.join(temp_path, file_md5 + ".docx"))
        text = wps2txt.process(wps_path=file_absolute_path,
                               temp_docx_path=temp_docx_path,
                               _limit_office_time=_limit_office_time)
    elif file_suffix == ".et":
        temp_xlsx_path = os.path.abspath(os.path.join(temp_path, file_md5 + ".xlsx"))
        text = et2txt.process(et_path=file_absolute_path,
                              temp_xlsx_path=temp_xlsx_path,
                              _limit_office_time=_limit_office_time)
    elif file_suffix == ".pdf":
        text = pdfminer.high_level.extract_text(file_absolute_path)
    elif file_suffix == ".epub":
        text = epub2txt.process(file_absolute_path)
    elif file_suffix == ".mobi":
        text = mobi2txt.process(file_absolute_path)
    elif file_suffix in image_types_list:
        text = image2txt.process(file_absolute_path)
    elif file_suffix in txt_types_list:
        with open(file_absolute_path, "r", encoding=detect_encoding(file_absolute_path), errors='ignore') as f:
            text = f.read()

    return text

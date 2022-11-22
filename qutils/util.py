import io
import time
import os
import sys
import warnings
import winreg
import ctypes
import chardet
import docx2txt
import winshell
# from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import qApp

from qutils import doc2txt, xls2txt, xlsx2txt
import pdfminer.high_level
from PyQt5.QtCore import QProcess
from PyQt5.QtGui import QIcon
import win32clipboard
from ctypes import *
from win32comext.shell.shell import ShellExecuteEx


def file_name_list(file_dir: str, screen: list, icon_dir: str = "icon", size_limit=100) -> list:
    """返回指定类型的文件列表"""
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if "~$" not in file:
                filename = os.path.splitext(file)
                filename_ = filename[0]
                suffix = filename[1]
                if suffix in screen and filename_[0] != "$":
                    absolute_path = os.path.abspath(os.path.join(root, file))
                    modifytime = time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime(os.path.getmtime(absolute_path)))
                    icon_ = QIcon(os.path.abspath(os.path.join(icon_dir, "%s.png" % suffix[1:])))
                    if os.path.getsize(absolute_path) < size_limit * 1024 * 1024:
                        L.append([(icon_, file), (None, getDocSize(absolute_path)),
                                  (None, modifytime), (None, absolute_path), (None, suffix)])
                    else:
                        print("文件太大：" + absolute_path)
                        print(getDocSize(absolute_path))

    return L


def formatSize(bytes):
    """字节bytes转化kb"""
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
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
        print(err)


def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
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




def is_user_admin():
    """ 检查admin """
    return ctypes.windll.shell32.IsUserAnAdmin()


def run_as_admin(args):
    """ 管理员运行 """
    script = os.path.abspath(sys.argv[0])
    # args = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else ''
    print(f"{script} {args}")
    ShellExecuteEx(lpFile=sys.executable, lpParameters=f"{script} {args}",
                   nShow=1, lpVerb='runas')
    return


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
        print("Well, do nothing as 'winshell' lib may not available on current os")
        print("error detail %s" % str(err))
    return False


def get_text(file_suffix, file_absolute_path, file_md5, temp_path, antiword_path) -> str:
    """转字符串返回处理结果"""
    if file_suffix == ".docx":
        text = docx2txt.process(file_absolute_path)
    elif file_suffix == ".doc":
        temp_docx_path = os.path.abspath(os.path.join(temp_path, file_md5 + ".docx"))
        text = doc2txt.process(doc_path=file_absolute_path, temp_docx_path=temp_docx_path, antiword_path=antiword_path,antiword_try_wrap=True)
    elif file_suffix == ".xls":
        temp_xlsx_path = os.path.abspath(os.path.join(temp_path, file_md5 + ".xlsx"))
        text = xls2txt.process(file_absolute_path, temp_xlsx_path)
    elif file_suffix == ".xlsx":
        text = xlsx2txt.process(file_absolute_path)
    elif file_suffix == ".pdf":
        text = pdfminer.high_level.extract_text(file_absolute_path)
    elif file_suffix == ".txt":
        with open(file_absolute_path, "r", encoding=detect_encoding(file_absolute_path), errors='ignore') as f:
            text = f.read()
    return text

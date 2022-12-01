# https://ask.csdn.net/questions/1094316
# 缘由：
# 脚本都是用来解决实际问题的，我最近碰到的问题是这样的（很罗嗦，只关心代码的请建议直接跳过）。天敏电视卡提供了定时录像的功能，这个功能可以定时开机，录像完成后自动关机，照理说功能也已经够用，但录像结束后没有关闭应用这个功能。有时我录像完成后并不需要关闭电脑（比如说正在bt下载电影），这时前台的电视窗口就一直开着，喇叭里面还不停播放电视对白，非常地不必要。于是想写一个python脚本，定时在每天录像以后执行，用来关闭电视卡应用程序。
# 网上搜了一下，找到相关的介绍。
# 一开始的思路是，根据exe文件找到进程id（类似在任务管理器里面查找），然后中止进程，
# 最漂亮的方法是用WMI对象找到指定进程（见reference 1）。随后发现，更加体面的中止应用的方法是找到应用程序的窗口，发送WM_CLOSE消息，如果失败（比如提示用户保存文件等待用户操作），再用TerminateProcess结束进程，其中要注意，TerminateProcess接受的参数是句柄，而不是进程号。
# 以下的代码是用来结束“记事本”这个应用的，
# 1.       根据窗口的标题找到窗口句柄（EnumWindows，注意，需要用可恶的回调函数，见windowEnumerationHandler），比如“未标题 – 记事本”，字符串匹配末尾的“记事本”可以找到
# 2.       向窗口发送WM_CLOSE消息（PostMessage），等待10秒
# 3.       根据窗口获得进程id（GetWindowThreadProcessId），试图强行中止进程（如果窗口收到WM_CLOSE消息已经关闭，亦无害）
# 附代码killwindow.py
import traceback

import pythoncom
import win32api
import win32con
import win32gui
import win32process
from PyQt5.QtCore import QThread


class KillThread(QThread):
    def __init__(self, suffix,_limit_office_time):
        super(KillThread, self).__init__()
        self.suffix = suffix
        self._limit_office_time=_limit_office_time

    def run(self) -> None:
        pythoncom.CoInitialize()
        self.sleep(self._limit_office_time)
        self.killwindow(self.suffix)
        self.killwindow(self.suffix)

    # We are going to use the win32gui.EnumWindows() function to get our top level window information. This is one of those nasty functions which wants a callback function passed to it (consult the docs if you are really bored). So here's one I made earlier:
    def windowEnumerationHandler(self, hwnd, resultList):
        '''Pass to win32gui.EnumWindows() to generate list of window handle, window text tuples.'''
        resultList.append((hwnd, win32gui.GetWindowText(hwnd)))

    def killwindow(self, suffix):
        # We can pass this, along a list to hold the results, into win32gui.EnumWindows(), as so:
        topWindows = []
        win32gui.EnumWindows(self.windowEnumerationHandler, topWindows)
        for i in topWindows:
            try:
                if i[1].endswith(suffix):
                    hwnd = i[0]
                    print(i[0], i[1])
                    threadId, processId = win32process.GetWindowThreadProcessId(hwnd)
                    print('processId = ', processId)
                    # Ask window nicely to close
                    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                    # Allow some time for app to close
                    self.sleep(2)
                    # If app didn't close, force close
                    handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, processId)
                    if handle:
                        print('handle = ', handle)
                        win32api.TerminateProcess(handle, 0)
                        win32api.CloseHandle(handle)
                        self.sleep(1)
            except Exception:
                print(traceback.format_exc())

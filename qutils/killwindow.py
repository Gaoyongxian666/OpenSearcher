import logging
import time
import traceback

import win32api
import win32con
import win32gui
import win32process

logger = logging.getLogger(__name__)


def windowEnumerationHandler(hwnd, resultList):
    """Pass to win32gui.EnumWindows() to generate list of window handle, window text tuples."""
    resultList.append((hwnd, win32gui.GetWindowText(hwnd)))

def getwindow():
    topWindows = []
    win32gui.EnumWindows(windowEnumerationHandler, topWindows)
    return topWindows

def killwindow(suffixList):
    # We can pass this, along a list to hold the results, into win32gui.EnumWindows(), as so:
    topWindows = []
    win32gui.EnumWindows(windowEnumerationHandler, topWindows)
    for i in topWindows:
        try:
            if judge(i[1], suffixList=suffixList):
                hwnd = i[0]
                threadId, processId = win32process.GetWindowThreadProcessId(hwnd)
                logger.info('processId = '+ str(processId))
                # Ask window nicely to close
                win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                # Allow some time for app to close
                time.sleep(2)
                # If app didn't close, force close
                handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, processId)
                if handle:
                    logger.info('handle = '+str(handle))
                    win32api.TerminateProcess(handle, 0)
                    win32api.CloseHandle(handle)
                    time.sleep(1)
        except Exception:
            logger.info(traceback.format_exc())


def judge(text: str, suffixList):
    for suffix in suffixList:
        if text.lower().endswith(suffix.lower()):
            return True
    return False


def KillAllOffice():
    logger.info("调用关闭全部Office")
    print("调用关闭全部Office")
    killwindow(["Word", "PowerPoint", "Excel", "Office", "文字", "演示", "表格"])


if __name__ == "__main__":
    KillAllOffice()
    # print(getwindow())
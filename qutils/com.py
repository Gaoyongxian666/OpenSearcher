import hashlib
import logging
import time
import traceback

from win32com import client as wc

logger = logging.getLogger(__name__)


def GetExcel():
    try:
        excel = wc.GetActiveObject("Excel.Application")
    except:
        try:
            excel = wc.DispatchEx("Excel.Application")
            excel.Visible = 0  # 后台运行,不显示
            excel.DisplayAlerts = 0  # 不警告
            excel.Workbooks.Add()
        except:
            try:
                excel = wc.GetActiveObject("ket.Application")
            except:
                try:
                    excel = wc.DispatchEx("ket.Application")
                    excel.Visible = 0  # 后台运行,不显示
                    excel.DisplayAlerts = 0  # 不警告
                    excel.Workbooks.Add()
                except:
                    logger.info(traceback.format_exc())
                    raise
    return excel


def GetEtExcel():
    try:
        excel = wc.GetActiveObject("ket.Application")
    except:
        try:
            excel = wc.DispatchEx("ket.Application")
            excel.Visible = 0  # 后台运行,不显示
            excel.DisplayAlerts = 0  # 不警告
            excel.Workbooks.Add()
        except:
            logger.info(traceback.format_exc())
            raise
    return excel


def GetWord():
    try:
        word = wc.GetActiveObject("Word.Application")
    except:
        try:
            word = wc.DispatchEx("Word.Application")
            word.Visible = 0  # 后台运行,不显示
            word.DisplayAlerts = 0  # 不警告
        except:
            try:
                word = wc.GetActiveObject("kwps.Application")
            except:
                try:
                    word = wc.DispatchEx("kwps.Application")
                    word.Visible = 0  # 后台运行,不显示
                    word.DisplayAlerts = 0  # 不警告
                except:
                    logger.info(traceback.format_exc())
                    raise
    return word


def GetWpsWord():
    try:
        word = wc.GetActiveObject("kwps.Application")
    except:
        try:
            word = wc.DispatchEx("kwps.Application")
            word.Visible = 0  # 后台运行,不显示
            word.DisplayAlerts = 0  # 不警告
        except:
            logger.info(traceback.format_exc())
            raise
    return word


def GetPowerPoint():
    try:
        powerpoint = wc.GetActiveObject("PowerPoint.Application")
    except:
        try:
            powerpoint = wc.DispatchEx("PowerPoint.Application")
            powerpoint.DisplayAlerts = 0  # 不警告
            # https://learn.microsoft.com/zh-cn/office/vba/api/powerpoint.presentations.add
            powerpoint.Presentations.Add(False)
        except:
            try:
                powerpoint = wc.GetActiveObject("kwpp.Application")
            except:
                try:
                    powerpoint = wc.DispatchEx("kwpp.Application")
                    powerpoint.DisplayAlerts = 0  # 不警告
                    # https://learn.microsoft.com/zh-cn/office/vba/api/powerpoint.presentations.add
                    powerpoint.Presentations.Add(False)
                except:
                    logger.info(traceback.format_exc())
                    raise
    return powerpoint


def GetTime(f):
    """记录函数消耗时间"""

    def inner(*arg, **kwarg):
        s_time = time.time()
        res = f(*arg, **kwarg)
        e_time = time.time()
        logger.info('耗时：{}秒'.format(e_time - s_time))
        print('耗时：{}秒'.format(e_time - s_time))
        return res

    return inner


def get_md5(path):
    with open(path, 'rb') as f:
        file_md5 = hashlib.md5(f.read()).hexdigest()
    return file_md5

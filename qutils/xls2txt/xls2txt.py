import logging
import os
import time
import traceback
import warnings

import win32api
import win32con
import win32gui
import win32process
import xlrd
from win32com import client as wc
from qutils import xlsx2txt
from qutils.killthread import KillThread
logger = logging.getLogger(__name__)


def _xls2txt(xls_path):
    """xls转txt"""
    try:
        data = xlrd.open_workbook(xls_path)
        text = ""
        for table in data.sheets():
            text = "".join((text, table.name + "\n"))
            nrows = table.nrows
            for ronum in range(0, nrows):
                row = table.row_values(ronum)
                values = ""
                for i in range(len(row)):
                    if i == len(row) - 1:
                        values = values + str(row[i])
                    else:
                        values = values + str(row[i]) + "\t"
                text = "".join((text, values + "\n"))
        return text
    except:
        raise


def xls2txt(xls_path, temp_xlsx_path,_limit_office_time) -> str:
    try:
        try:
            excel = wc.DispatchEx("Excel.Application")
        except:
            logger.info(traceback.format_exc())
            try:
                excel = wc.DispatchEx("kwps.Application")
            except:
                logger.info(traceback.format_exc())
                try:
                    excel = wc.DispatchEx("wps.Application")
                except:
                    logger.info(traceback.format_exc())
                    logger.info("未发现excel组件，将无法查找老版的xls文件")
                    # warnings.warn("未发现excel组件，将无法查找老版的xls文件", RuntimeWarning)
                    raise
        excel.Visible = 0  # 后台运行,不显示
        excel.DisplayAlerts = 0  # 不警告
        suffix = str(excel).split(" ")[-1]
        tr = KillThread(suffix,_limit_office_time)
        tr.start()
        # https://learn.microsoft.com/zh-cn/office/vba/api/excel.workbooks.open
        # Open() got an unexpected keyword argument 'FileName',尼玛的，只有这个excel组件的参数不管用，需要挨个给
        xls = excel.Workbooks.Open(xls_path, 0, True)
        tr.terminate()
        xls.SaveAs(temp_xlsx_path, 51)
        xls.Close()
        excel.Quit()
        time.sleep(2)
        text = xlsx2txt.process(temp_xlsx_path)
        os.remove(temp_xlsx_path)
        return text
    except:
        raise


def process(xls_path, temp_xlsx_path,_limit_office_time):
    try:
        text = _xls2txt(xls_path)
    except:
        logger.info(traceback.format_exc())
        logger.info("尝试Win32转存:" + xls_path)
        # warnings.warn(message=traceback.format_exc(), category=RuntimeWarning)
        # warnings.warn(message="尝试Win32转存:" + xls_path, category=RuntimeWarning)
        text = xls2txt(xls_path, temp_xlsx_path,_limit_office_time)
    return text


if __name__ == "__main__":
    xls2txt(
        r"C:\Users\Gaoyongxian\AppData\Local\Kingsoft\WPS Office\11.1.0.12598\office6\mui\zh_CN\templates\secdoctemplate.xls",
        r"C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\qutils\DEMO.xlsx")

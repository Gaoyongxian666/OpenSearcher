import io
import logging
import os
import time
import traceback
from threading import Timer

from qutils.com import GetExcel, GetTime
from qutils.killwindow import KillAllOffice
from qutils.xlsx2txt.xlsx2csv import Xlsx2csv

logger = logging.getLogger(__name__)


# @GetTime
def xlsx2txt_win32(xlsx_path, temp_xlsx_path, _limit_office_time=5) -> str:
    try:
        excel = GetExcel()
        t = Timer(_limit_office_time, KillAllOffice)
        t.start()
        # https://learn.microsoft.com/zh-cn/office/vba/api/excel.workbooks.open
        # Open() got an unexpected keyword argument 'FileName',尼玛的，只有这个excel组件的参数不管用，需要挨个给
        xls = excel.Workbooks.Open(xlsx_path, 0, True)
        t.cancel()
        xls.SaveAs(temp_xlsx_path, 51)
        xls.Close()
        text = xlsx2txt(temp_xlsx_path)
        os.remove(temp_xlsx_path)
        return text
    except:
        try:
            t.cancel()
        except:
            pass
        KillAllOffice()
        raise


def xlsx2txt(xlsx_path):
    output = io.StringIO()
    Xlsx2csv(xlsx_path, outputencoding="utf-8").convert(output, 0)
    text = output.getvalue()
    return text


def process(xlsx_path, temp_xlsx_path, _limit_office_time=5):
    try:
        text = xlsx2txt(xlsx_path)
    except:
        logger.info(traceback.format_exc())
        logger.info("尝试Win32转存:" + xlsx_path)
        text = xlsx2txt_win32(xlsx_path, temp_xlsx_path, _limit_office_time)
    return text


if __name__ == "__main__":
    while True:
        time.sleep(1)
        xlsx2txt_win32(r"C:\Users\Gaoyongxian\Desktop\test.xlsx",
                       r"C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\qutils\xlsx2txt\a.xlsx")

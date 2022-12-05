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

        t1 = Timer(_limit_office_time, KillAllOffice)
        t2 = Timer(_limit_office_time, KillAllOffice)
        t3 = Timer(_limit_office_time, KillAllOffice)

        t1.start()
        # https://learn.microsoft.com/zh-cn/office/vba/api/excel.workbooks.open
        # Open() got an unexpected keyword argument 'FileName',尼玛的，只有这个excel组件的参数不管用，需要挨个给
        xls = excel.Workbooks.Open(xlsx_path, 0, True)
        t1.cancel()

        t2.start()
        xls.SaveAs(temp_xlsx_path, 51)
        t2.cancel()

        t3.start()
        xls.Close()
        t3.cancel()

        text = xlsx2txt(temp_xlsx_path)
        os.remove(temp_xlsx_path)
        return text
    except:
        try:
            t1.cancel()
        except:
            pass
        try:
            t2.cancel()
        except:
            pass
        try:
            t3.cancel()
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
        xlsx2txt_win32(r"C:\Users\Gaoyongxian\Desktop\test.xlsx",
                       r"C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\qutils\xlsx2txt\a.xlsx")

import io
import os
from threading import Timer

from qutils.com import GetEtExcel, get_md5
from qutils.et2txt.xlsx2csv import Xlsx2csv
from qutils.killwindow import KillAllOffice


def xlsx2txt(xlsx_path):
    output = io.StringIO()
    Xlsx2csv(xlsx_path, outputencoding="utf-8").convert(output, 0)
    text = output.getvalue()
    return text


def et2txt_win32(et_path, temp_xlsx_path, _limit_office_time=5) -> str:
    try:
        excel = GetEtExcel()
        t = Timer(_limit_office_time, KillAllOffice)
        # t.start()
        # https://learn.microsoft.com/zh-cn/office/vba/api/excel.workbooks.open
        # Open() got an unexpected keyword argument 'FileName',尼玛的，只有这个excel组件的参数不管用，需要挨个给
        et = excel.Workbooks.Open(et_path, 0, True)
        t.cancel()
        et.SaveAs(temp_xlsx_path, 51)
        et.Close()
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


def process(et_path, temp_xlsx_path, _limit_office_time=5):
    text = et2txt_win32(et_path, temp_xlsx_path, _limit_office_time)
    return text



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
        t1 = Timer(_limit_office_time, KillAllOffice)
        t2 = Timer(_limit_office_time, KillAllOffice)
        t3 = Timer(_limit_office_time, KillAllOffice)

        t1.start()
        # https://learn.microsoft.com/zh-cn/office/vba/api/excel.workbooks.open
        # Open() got an unexpected keyword argument 'FileName',尼玛的，只有这个excel组件的参数不管用，需要挨个给
        et = excel.Workbooks.Open(et_path, 0, True)
        t1.cancel()

        t2.start()
        et.SaveAs(temp_xlsx_path, 51)
        t2.cancel()

        t3.start()
        et.Close()
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


def process(et_path, temp_xlsx_path, _limit_office_time=5):
    text = et2txt_win32(et_path, temp_xlsx_path, _limit_office_time)
    return text


if __name__=="__main__":
    print(et2txt_win32(
        et_path=r"C:\Users\Gaoyongxian\AppData\Roaming\kingsoft\office6\backup\11月26日情况汇总2.xls.9E2F6B831D973E14C0BB6D6B86F0F7B0.20221127164921369.et",
        temp_xlsx_path=r"C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\qutils\et2txt\a.xlsx"))
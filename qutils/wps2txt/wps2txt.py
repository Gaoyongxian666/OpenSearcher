import os
from threading import Timer

import docx2txt

from qutils.com import GetWpsWord
from qutils.killwindow import KillAllOffice


def wps2txt_win32(wps_path, temp_docx_path, _limit_office_time=5) -> str:
    try:
        word = GetWpsWord()
        t = Timer(_limit_office_time, KillAllOffice)
        t.start()
        # https://learn.microsoft.com/zh-cn/office/vba/api/excel.workbooks.open
        # Open() got an unexpected keyword argument 'FileName',尼玛的，只有这个excel组件的参数不管用，需要挨个给
        wps = word.Documents.OpenNoRepairDialog(wps_path, False, True)
        t.cancel()
        wps.SaveAs(temp_docx_path, 12)
        wps.Close()
        text = docx2txt.process(temp_docx_path)
        os.remove(temp_docx_path)
        return text
    except:
        try:
            t.cancel()
        except:
            pass
        KillAllOffice()
        raise


def process(wps_path, temp_docx_path, _limit_office_time=5):
    text = wps2txt_win32(wps_path, temp_docx_path, _limit_office_time)
    return text



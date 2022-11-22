import os
import time
import traceback
import warnings
import xlrd
from win32com import client as wc

from qutils import xlsx2txt


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


def xls2txt(xls_path, temp_xlsx_path) -> str:
    try:
        try:
            # 用来将dox转docx，注意:如果安装WPS，它会篡改office的COM接口，改成指向它，并且WPS在合并模式下，无法后台操作
            # 尝试多方式启动
            excel = wc.Dispatch("Excel.Application")
            # self.word.Visible = True  # 确定是否可见
        except:
            traceback.print_exc()
            try:
                excel = wc.Dispatch("kwps.Application")
            except:
                traceback.print_exc()
                try:
                    excel = wc.Dispatch("wps.Application")
                except:
                    traceback.print_exc()
                    warnings.warn("未发现excel组件，将无法查找老版的xls文件", RuntimeWarning)
                    raise
        doc = excel.Workbooks.Open(xls_path)
        doc.SaveAs(temp_xlsx_path, 51)
        doc.Close()
        excel.Quit()
        time.sleep(2)
        text = xlsx2txt.process(temp_xlsx_path)
        os.remove(temp_xlsx_path)
        return text
    except:
        raise


def process(xls_path, temp_xlsx_path):
    try:
        text = _xls2txt(xls_path)
    except:
        warnings.warn(message=traceback.format_exc(), category=RuntimeWarning)
        warnings.warn(message="尝试Win32转存:" + xls_path, category=RuntimeWarning)
        text = xls2txt(xls_path, temp_xlsx_path)
    return text

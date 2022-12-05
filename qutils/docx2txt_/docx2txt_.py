import logging
import os
import traceback
from threading import Timer

from docx2txt import docx2txt

from qutils.com import GetWord
from qutils.killwindow import KillAllOffice

logger = logging.getLogger(__name__)


def docx2txt_win32(doc_path, temp_docx_path, _limit_office_time) -> str:
    try:
        word = GetWord()
        t1 = Timer(_limit_office_time, KillAllOffice)
        t2 = Timer(_limit_office_time, KillAllOffice)
        t3 = Timer(_limit_office_time, KillAllOffice)

        t1.start()
        # https://learn.microsoft.com/zh-cn/office/vba/api/word.documents.opennorepairdialog
        # doc = word.Documents.OpenNoRepairDialog(FileName=doc_path, ConfirmConversions=False, ReadOnly=True)
        doc = word.Documents.OpenNoRepairDialog(doc_path, False, True)
        t1.cancel()

        t2.start()
        doc.SaveAs(temp_docx_path, 12)
        t2.cancel()

        t3.start()
        doc.Close()
        t3.cancel()

        text = docx2txt.process(temp_docx_path)
        os.remove(temp_docx_path)
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


def process(docx_path, temp_docx_path, _limit_office_time=5):
    try:
        text = docx2txt.process(docx_path)
    except:
        logger.info(traceback.format_exc())
        logger.info("尝试Win32转存:" + docx_path)
        text = docx2txt_win32(docx_path, temp_docx_path, _limit_office_time)
    return text

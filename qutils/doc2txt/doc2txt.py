import logging
import os
import subprocess
import time
import traceback
import warnings
from threading import Timer

from docx2txt import docx2txt

from qutils.com import GetWord, GetTime
from qutils.killwindow import KillAllOffice

logger = logging.getLogger(__name__)


def doc2txt_win(doc_path, antiword_path, antiword_try_wrap: bool = False) -> str:
    command = "\"" + antiword_path + "\"" + " -m UTF-8.txt " + "\"" + doc_path + "\""
    file_encoding = "utf-8"
    try:
        my_command = subprocess.run(
            args=command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding=file_encoding,
            shell=True,
            env={"Home": os.path.dirname(antiword_path)})
        if my_command.returncode == 0:
            _ = my_command.stdout
            if antiword_try_wrap:
                text = ""
                textlist = _.split("\n")
                for t in textlist:
                    t = t.replace(u'\u3000', u' ').replace(u'\xa0', u' ').replace(u'\u3002', u' ')
                    if len(t) > 0 and t[0] in [" ", "|", "【", "(", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
                                               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                                               'O',
                                               'P',
                                               'Q',
                                               'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                                               'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                                               'o',
                                               'p',
                                               'q',
                                               'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                                               '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        # text = '\n'.join((text, t))
                        text = ''.join((text, t))
                    elif len(t) == 0:
                        text = '\n'.join((text, t))
                    else:
                        text = ''.join((text, t))
            else:
                text = _

            return text
        else:
            err = my_command.stderr
            warnings.warn(message=str(err), category=RuntimeWarning, source=None)
            raise RuntimeError("处理doc出错")
    except:
        raise


# @GetTime
def doc2txt_win32(doc_path, temp_docx_path, _limit_office_time=5) -> str:
    try:
        word = GetWord()
        t = Timer(_limit_office_time, KillAllOffice)
        t.start()
        # https://learn.microsoft.com/zh-cn/office/vba/api/word.documents.opennorepairdialog
        # doc = word.Documents.OpenNoRepairDialog(FileName=doc_path, ConfirmConversions=False, ReadOnly=True)
        doc = word.Documents.OpenNoRepairDialog(doc_path, False, True)
        t.cancel()
        doc.SaveAs(temp_docx_path, 12)
        doc.Close()
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


def process(doc_path, temp_docx_path, antiword_path=None, _limit_office_time=5):
    if antiword_path is not None:
        try:
            text = doc2txt_win(doc_path, antiword_path, antiword_try_wrap=True)
        except:
            logger.info(traceback.format_exc())
            logger.info("尝试Win32转存:" + doc_path)
            text = doc2txt_win32(doc_path, temp_docx_path, _limit_office_time)
        return text
    else:
        return doc2txt_win32(doc_path, temp_docx_path, _limit_office_time)


if __name__ == "__main__":
    while True:
        time.sleep(1)
        doc2txt_win32(r"C:\Users\Gaoyongxian\Desktop\a.doc",
                      r"C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\qutils\doc2txt\a.docx")

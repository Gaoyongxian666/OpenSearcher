import os
import subprocess
import time
import traceback
import warnings
from win32com import client as wc
from docx2txt import docx2txt


def _doc2txt(doc_path, antiword_try_wrap: bool, antiword_path) -> str:
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


def doc2txt(doc_path, temp_docx_path) -> str:
    try:
        try:
            # 用来将dox转docx，注意:如果安装WPS，它会篡改office的COM接口，改成指向它，并且WPS在合并模式下，无法后台操作
            # 尝试多方式启动
            word = wc.Dispatch("Word.Application")
            # self.word.Visible = True  # 确定是否可见
        except:
            traceback.print_exc()
            try:
                word = wc.Dispatch("kwps.Application")
            except:
                traceback.print_exc()
                try:
                    word = wc.Dispatch("wps.Application")
                except:
                    traceback.print_exc()
                    print("未发现WORD组件，将无法查找老版的doc文件")
                    raise
        doc = word.Documents.Open(doc_path)
        doc.SaveAs(temp_docx_path, 12)
        doc.Close()
        word.Quit()
        time.sleep(2)
        text = docx2txt.process(temp_docx_path)
        os.remove(temp_docx_path)
        return text
    except:
        raise


def process(doc_path, temp_docx_path, antiword_try_wrap=False, antiword_path=None):
    if antiword_path is not None:
        try:
            text = _doc2txt(doc_path, antiword_try_wrap, antiword_path)
        except:
            warnings.warn(message=traceback.format_exc(), category=RuntimeWarning)
            warnings.warn(message="尝试Win32转存:" + doc_path, category=RuntimeWarning)
            text = doc2txt(doc_path, temp_docx_path)
        return text
    else:
        return doc2txt(doc_path, temp_docx_path)

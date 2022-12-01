import logging
import os
import time
import traceback
import warnings

from win32com import client as wc

from qutils import pptx2txt
from qutils.killthread import KillThread

logger = logging.getLogger(__name__)


def process(ppt_path, temp_pptx_path,_limit_office_time=5) -> str:
    try:
        try:
            powerpoint = wc.DispatchEx("PowerPoint.Application")
        except:
            logger.info(traceback.format_exc())
            try:
                powerpoint = wc.DispatchEx("kwps.Application")
            except:
                logger.info(traceback.format_exc())
                try:
                    powerpoint = wc.DispatchEx("wps.Application")
                except:
                    logger.info(traceback.format_exc())
                    warnings.warn("未发现ppt组件，将无法查找老版的xls文件", RuntimeWarning)
                    raise

        powerpoint.DisplayAlerts = 0  # 不警告
        suffix = str(powerpoint).split(" ")[-1]
        tr = KillThread(suffix,_limit_office_time)
        tr.start()
        # https://learn.microsoft.com/zh-cn/office/vba/api/PowerPoint.Presentations.Open
        # ppt = powerpoint.Presentations.Open(FileName=ppt_path, ReadOnly=True, WithWindow=False)
        ppt = powerpoint.Presentations.Open(ppt_path, True, False, False)
        tr.terminate()
        ppt.SaveAs(temp_pptx_path)
        ppt.Close()
        powerpoint.Quit()
        time.sleep(2)
        text = pptx2txt.process(temp_pptx_path)
        os.remove(temp_pptx_path)
        return text
    except:
        raise


if __name__ == "__main__":
    print(process(r"C:\Users\Gaoyongxian\Desktop\9科普知识-血气分析的临床应用.ppt",
                  r"C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\qutils\ppt2txt\a.pptx"))

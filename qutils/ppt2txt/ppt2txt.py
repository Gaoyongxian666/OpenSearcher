import logging
import os
import time
import traceback
import warnings

from win32com import client as wc

from qutils import pptx2txt

logger = logging.getLogger(__name__)


def process(ppt_path, temp_pptx_path) -> str:
    try:
        try:
            ppt = wc.Dispatch("PowerPoint.Application")
        except:
            logger.info(traceback.format_exc())
            try:
                ppt = wc.Dispatch("kwps.Application")
            except:
                logger.info(traceback.format_exc())
                try:
                    ppt = wc.Dispatch("wps.Application")
                except:
                    logger.info(traceback.format_exc())
                    warnings.warn("未发现ppt组件，将无法查找老版的xls文件", RuntimeWarning)
                    raise
        # https://learn.microsoft.com/zh-cn/office/vba/api/PowerPoint.Presentations.Open
        doc = ppt.Presentations.Open(ppt_path, ReadOnly=True, WithWindow=False)
        doc.SaveAs(temp_pptx_path)
        doc.Close()
        ppt.Quit()
        time.sleep(2)
        text = pptx2txt.process(temp_pptx_path)
        os.remove(temp_pptx_path)
        return text
    except:
        raise


if __name__ == "__main__":
    print(process(r"C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\qutils\ppt2txt\a.ppt",
                  r"C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\qutils\ppt2txt\a.pptx"))

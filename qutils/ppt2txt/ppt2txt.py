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
        # https://learn.microsoft.com/zh-cn/office/vba/api/PowerPoint.Presentations.Open
        ppt = powerpoint.Presentations.Open(ppt_path, ReadOnly=True, WithWindow=False)
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
    print(process(r"C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\qutils\ppt2txt\a.ppt",
                  r"C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\qutils\ppt2txt\a.pptx"))

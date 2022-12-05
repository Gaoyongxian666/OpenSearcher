import os
import win32con
from uuid import uuid1
from win32clipboard import GetClipboardData, OpenClipboard, CloseClipboard, EmptyClipboard, SetClipboardData, \
    EnumClipboardFormats
from PIL import Image, ImageGrab


class OperationClipboard:
    # 读取剪贴板的数据
    def get_clipboard(self):
        OpenClipboard()  # 打开剪贴板
        formats = []
        lastFormat = 0
        while 1:
            nextFormat = EnumClipboardFormats(lastFormat)
            if 0 == nextFormat:
                break
            else:
                formats.append(nextFormat)
                lastFormat = nextFormat
        if formats == []:
            return None
        elif 13 in formats:
            return {'format': "Unicode", 'data': GetClipboardData(13)}
        elif 1 in formats:
            return {'format': "ANSI", 'data': GetClipboardData(1)}
        elif win32con.CF_BITMAP in formats:
            return {'format': "BITMAP", 'data': GetClipboardData(2)}
        elif 15 in formats:
            return {'format': "HDROP", 'data': GetClipboardData(15)}
        '''
        完整 : win32con.CF_TEXT
        CF_TEXT(1):文本格式。 每行以回车/换行符结尾 (CR-LF) 组合。 空字符指示数据的末尾。 将此格式用于 ANSI 文本。
        CF_UNICODETEXT(13):Unicode 文本格式。 每行以回车/换行符结尾 (CR-LF) 组合。 空字符指示数据的末尾。
        CF_BITMAP(2):位图 (HBITMAP) 的句柄。
        CF_HDROP(15):文件地址元组
        '''
        CloseClipboard()

    # 写入剪贴板数据
    def set_clipboard(self, astr: tuple):
        OpenClipboard()
        EmptyClipboard()
        # 可以sleep一下，防止操作过快报错
        # time.sleep(1)
        SetClipboardData(win32con.CF_HDROP, astr)
        CloseClipboard()

    def savePic(self, Path):
        im = ImageGrab.grabclipboard()
        if isinstance(im, Image.Image):
            imgName = self.getUUID() + '.jpg'
            filePath = os.path.join(Path, "res/img/%s" % imgName)
            rgb_im = im.convert('RGB')
            rgb_im.save(filePath)
            return filePath

    def getUUID(self):
        return uuid1().hex

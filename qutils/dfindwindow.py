import win32gui

from qutils.dsendkeys import send_unicode


# 如果出现未知弹唱：
hld = win32gui.FindWindow(None,u"Microsoft Word")
win32gui.SetForegroundWindow(hld)
send_unicode("y")
print(ord("Y"))
print(hld)
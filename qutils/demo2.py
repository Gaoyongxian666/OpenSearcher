import win32gui

from qutils.demo import send_unicode



hld = win32gui.FindWindow(None,u"Microsoft Word")
win32gui.SetForegroundWindow(hld)
send_unicode("y")
print(ord("Y"))
print(hld)
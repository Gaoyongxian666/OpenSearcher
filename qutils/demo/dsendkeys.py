from ctypes import *
from ctypes import wintypes as w

KEYEVENTF_SCANCODE = 0x8
KEYEVENTF_UNICODE = 0x4
KEYEVENTF_KEYUP = 0x2
SPACE = 0x39
INPUT_KEYBOARD = 1

ULONG_PTR = c_ulong if sizeof(c_void_p) == 4 else c_ulonglong

class KEYBDINPUT(Structure):
    _fields_ = [('wVk' ,w.WORD),
                ('wScan',w.WORD),
                ('dwFlags',w.DWORD),
                ('time',w.DWORD),
                ('dwExtraInfo',ULONG_PTR)]

class MOUSEINPUT(Structure):
    _fields_ = [('dx' ,w.LONG),
                ('dy',w.LONG),
                ('mouseData',w.DWORD),
                ('dwFlags',w.DWORD),
                ('time',w.DWORD),
                ('dwExtraInfo',ULONG_PTR)]

class HARDWAREINPUT(Structure):
    _fields_ = [('uMsg' ,w.DWORD),
                ('wParamL',w.WORD),
                ('wParamH',w.WORD)]

class DUMMYUNIONNAME(Union):
    _fields_ = [('mi',MOUSEINPUT),
                ('ki',KEYBDINPUT),
                ('hi',HARDWAREINPUT)]

class INPUT(Structure):
    _anonymous_ = ['u']
    _fields_ = [('type',w.DWORD),
                ('u',DUMMYUNIONNAME)]

print(sizeof(INPUT))



def send_scancode(code):
    lib = WinDLL('user32')
    lib.SendInput.argtypes = w.UINT, POINTER(INPUT), c_int
    lib.SendInput.restype = w.UINT
    i = INPUT()
    i.type = INPUT_KEYBOARD
    i.ki = KEYBDINPUT(0,code,KEYEVENTF_SCANCODE,0,0)
    lib.SendInput(1,byref(i),sizeof(INPUT))
    i.ki.dwFlags |= KEYEVENTF_KEYUP
    lib.SendInput(1,byref(i),sizeof(INPUT))

def send_unicode(s):
    lib = WinDLL('user32')
    lib.SendInput.argtypes = w.UINT, POINTER(INPUT), c_int
    lib.SendInput.restype = w.UINT
    i = INPUT()
    i.type = INPUT_KEYBOARD
    for c in s:
        i.ki = KEYBDINPUT(0,ord(c),KEYEVENTF_UNICODE,0,0)
        lib.SendInput(1,byref(i),sizeof(INPUT))
        i.ki.dwFlags |= KEYEVENTF_KEYUP
        lib.SendInput(1,byref(i),sizeof(INPUT))

# send_scancode(SPACE)

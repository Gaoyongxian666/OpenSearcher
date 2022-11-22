import os

# “”“
# 这里学委调用了winshell的CreateShortcut函数。
# 传入4个参数，分别为：快捷方式的路径，exe文件的路径，图标路径，还有描述信息。
# ”“”
def create_shortcut(bin_path: str, name: str, desc: str):
    try:
        import winshell
        shortcut = os.path.join(winshell.desktop(), name + ".lnk")
        winshell.CreateShortcut(
            Path=shortcut,
            Target=bin_path,
            Icon=(bin_path, 0),
            Description=desc
        )
        return True
    except ImportError as err:
        print("Well, do nothing as 'winshell' lib may not available on current os")
        print("error detail %s" % str(err))
    return False


if __name__ == "__main__":
    #这里的程序exe路径，请修改为个人库的路径，第二个参数为快捷方式的文件名，第三个为描述信息。
    create_shortcut("C:/LeiXueWei/Python.framework/Versions/3.8/bin/rxq.exe", "Open Searcher", "学委特制清点小程序")
    # print(os.path.exists(r"C:\Users\Gaoyongxian\Desktop\gaoyongx.lnk"))

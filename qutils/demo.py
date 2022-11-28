import hashlib
import os

with open(r"C:\Users\Gaoyongxian\Downloads\Documents\9科普知识-血气分析的临床应用.ppt", 'rb') as f:
    file_path_md5 = hashlib.md5(f.read()).hexdigest()
# temp_md5_path = os.path.abspath(os.path.join(self.CurPath, ".temp", file_path_md5))
# error_temp_md5_path = os.path.abspath(os.path.join(self.CurPath, ".errortemp", file_path_md5))
print(file_path_md5)
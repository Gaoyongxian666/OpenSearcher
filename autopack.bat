set /p version=input your version :
echo on
echo gyx
pip freeze > C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\requirements.txt
cd C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack
echo y|pyinstaller -D -w -i C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\icon\logo.ico C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\OpenSearcher.py
xcopy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pyexiv2 C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist\OpenSearcher\pyexiv2\ /e /y /h /r
xcopy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\antiword C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist\OpenSearcher\antiword\ /e /y /h /r
xcopy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\icon C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist\OpenSearcher\icon\ /e /y /h /r /q
copy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\cacert.pem  C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist\OpenSearcher\cacert.pem /y
copy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\HELP.md  C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist\OpenSearcher\HELP.md /y
 "C:\Program Files (x86)\360\360zip\360zip.exe" -ar "C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist\OpenSearcher" "C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist\OpenSearcher_%version%_green_win10.zip"
cd C:\Program Files (x86)\Inno Setup 6
ISCC C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\OpenSearcher.iss
cd C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist
rename OpenSearcher_%version%.exe OpenSearcher_%version%_win10.exe
copy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\packwin7\vc_redist.x64.exe C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist\OpenSearcher\vc_redist.x64.exe /y
copy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\packwin7\Windows6.1-KB2533623-x64.msu C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist\OpenSearcher\Windows6.1-KB2533623-x64.msu /y
copy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\Win7修复（程序运行失败）64位.bat C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist\OpenSearcher\Win7修复（程序运行失败）64位.bat /y
 "C:\Program Files (x86)\360\360zip\360zip.exe" -ar "C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist\OpenSearcher" "C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist\OpenSearcher_%version%_green_win7.zip"
cd C:\Program Files (x86)\Inno Setup 6
ISCC C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\OpenSearcher_win7.iss
cd C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist
rename OpenSearcher_%version%.exe OpenSearcher_%version%_win7.exe
pause

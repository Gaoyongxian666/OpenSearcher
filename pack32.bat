set /p version=input your version :
call C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\venv\Scripts\activate.bat
echo on
echo gyx
cd C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack32
echo y|pyinstaller -D -w -i C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\icon\logo.ico C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\OpenSearcher.py
xcopy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\antiword C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack32\dist\OpenSearcher\antiword\ /e /y /h /r
xcopy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\icon C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack32\dist\OpenSearcher\icon\ /e /y /h /r /q
copy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\cacert.pem  C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack32\dist\OpenSearcher\cacert.pem /y
copy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\HELP.md  C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack32\dist\OpenSearcher\HELP.md /y
copy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\packwin7\vc_redist.x86.exe C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack32\dist\OpenSearcher\vc_redist.x86.exe /y
copy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\packwin7\Windows6.1-KB2533623-x86.msu C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack32\dist\OpenSearcher\Windows6.1-KB2533623-x86.msu /y 
copy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\Win7修复（程序运行失败）32位.bat C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack32\dist\OpenSearcher\Win7修复（程序运行失败）32位.bat /y 
"C:\Program Files (x86)\360\360zip\360zip.exe" -ar "C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack32\dist\OpenSearcher" "C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist\OpenSearcher_%version%_32wei_win7.zip"
pause
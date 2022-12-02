set /p version=input your version :
call C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\venv\Scripts\activate.bat
echo on
echo gyx
cd C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\packtest
pyinstaller -D -i C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\icon\logo.ico C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\OpenSearcher.py
xcopy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\antiword C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\packtest\dist\OpenSearcher\antiword\ /e /y /h /r
xcopy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\icon C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\packtest\dist\OpenSearcher\icon\ /e /y /h /r /q
copy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\promote52.txt  C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\packtest\dist\OpenSearcher\promote.txt /y
copy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\cacert.pem  C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\packtest\dist\OpenSearcher\cacert.pem /y
copy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\HELP.md  C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\packtest\dist\OpenSearcher\HELP.md /y
pause
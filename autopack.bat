set /p version=input your version :
call C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\venv\Scripts\activate.bat
echo on
echo gyx
pip freeze > C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\requirements.txt
cd C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack
echo y|pyinstaller -D -w -i C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\icon\logo.ico C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\OpenSearcher.py
xcopy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\antiword C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist\OpenSearcher\antiword\ /e /y /h /r
xcopy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\icon C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist\OpenSearcher\icon\ /e /y /h /r /q
copy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\promote52.txt  C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist\OpenSearcher\promote.txt /y
copy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\cacert.pem  C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist\OpenSearcher\cacert.pem /y
copy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\HELP.md  C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist\OpenSearcher\HELP.md /y
 "C:\Program Files (x86)\360\360zip\360zip.exe" -ar "C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist\OpenSearcher" "C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist\OpenSearcher_%version%_ÂÌÉ«°æ.zip"
copy C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\promotexz.txt  C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist\OpenSearcher\promote.txt /y
 "C:\Program Files (x86)\360\360zip\360zip.exe" -ar "C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist\OpenSearcher" "C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist\OpenSearcher_%version%_ÂÌÉ«°æ_.zip"
del C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\pack\dist\OpenSearcher\promote.txt
cd C:\Program Files (x86)\Inno Setup 6
ISCC C:\Users\Gaoyongxian\Documents\GitHub\OpenSearcher\OpenSearcher.iss
pause

@Echo Off
Title 修复Win7
Echo 正在安装Windows必要运行库组件和系统补丁，请选择“是”进行安装。
cd /d %~dp0
vc_redist.x86.exe /install /quiet
start Windows6.1-KB2533623-x86.msu
pause
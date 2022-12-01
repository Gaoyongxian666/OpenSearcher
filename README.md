# OpenSearcher
一个基于 PyQt5 **本地的**、**安全的**、**开源的**、支持**全文检索**的搜索器。本项目使用纯**Python**编写，所使用的**第三方包**都为**开源库**。  

## 文件类型  
* ```doc``` Via [antiword](http://www.winfield.demon.nl/)  
* ```xls``` Via [xlrd](https://github.com/python-excel/xlrd)  
* ```docx ``` Via [docx2txt](https://github.com/ankushshah89/python-docx2txt)  
* ```xlsx``` Via [xlsx2csv](https://github.com/dilshod/xlsx2csv)  
* ```pptx``` Via [python-pptx](https://github.com/scanny/python-pptx)  
* ```mobi``` Via [mobi](https://github.com/iscc/mobi)  
* ```epub``` Via [ebooklib](https://github.com/aerkalov/ebooklib)  
* ```pdf``` Via [pdfminer.six](https://github.com/pdfminer/pdfminer.six)  
* ```doc、xls、ppt``` Via [pywin32](https://github.com/mhammond/pywin32)  


## 使用提示
1. 利用```空闲时间```，提前```建立索引```缓存很重要，将大大加快之后的搜索。（本项目并没有强制要求建立索引缓存，还是由你自己决定是否建立索引缓存，如果你经常进行全盘随机搜索，推荐建立索引缓存）
2. 如果```搜索进行```中，```预览```可能会卡顿。如果卡顿，请等待一下。（出现卡顿的原因是当前搜索速度过快加上用户频繁操作导致的Ui阻塞，通常情况不会出现这种卡顿）  
3. 在```第一次搜索```某个文件目录时，搜索速度很慢，但是下次```搜索相同目录```将会很快。(原因就是第一次搜索的时候还没有建立索引缓存)  
4. 实际上```索引缓存```就是以```文件的MD5值```命名的```Text```文本文件，存放目录就在安装目录下的```.temp```文件夹下.（这意味这如果更新软件，你可以直接将```.temp```文件复制到新安装路径下，而不用耗费时间```重新索引```。）
5. 在```搜索进行```中，必须退出正在打开的```word、excel、ppt```文档，退出```Microsoft Office```或```WPS Office```程序，因为本程序强行关闭Office可能会影响你的文档。（原因是当```doc```、```xls```、```ppt```在经过```antiword```、```xlrd```处理失败后，将选择通过系统中的```Office组件```进行再处理）

## 关于速度
&nbsp;&nbsp;搜索时间大部分都是消耗在第一次处理文件，也就是建立索引缓存那个过程。所以有时你在第一次搜索某个目录的时候感觉不是很快，但是如果你第二次搜索相同的目录将会很快。
原理是我在第一次处理文件时留下缓存文件，之后的搜索会根据文件md5值判断文件是否改变，如果文件内容没有改变直接读取缓存，如果文件内容改变将重新处理，这样就会大大提示搜索速度。
最后，推荐大家在空闲时间要提前建立索引，这样下次搜索会很快。


## 关于项目
&nbsp;&nbsp;这实际上是一个仿照AnyTxT写的项目，只是因为AnyTxT不开源，由于保密原则，某些环境下无法使用，所以自己写了一个开源项目，如果你单位也有保密原则，不妨试试，本项目所有依赖和包都是开源的，你也可以查看项目代码，自行打包。 由于不太懂设计美化，但是项目里面界面都是```.ui```文件，如果有会```qss```美化的可以帮忙```fork```美化一下。


## 开源地址
* https://github.com/Gaoyongxian666/OpenSearcher

## 开发环境

```pip install -r requirements.txt```



## 更新日志
* 0.0.7
  * 2022.12.01 由于win32com在操作Office组件时可能会弹出不确定类型窗口阻塞，为此添加限制时间：在规定时间内用户没有响应Office提示窗口，将直接对当前文档报错并关闭Office，从而让程序能够继续往下处理。 
* 0.0.6
  * 2022.11.30 感谢坛友 @会飞的花 提出的建议：提高底部提示字号、添加目录黑名单。 感谢坛友 @hutuch 提出的建议：按照AnyTxt修改选择目录处理逻辑。
* 0.0.5
  * 2022.11.28 感谢坛友 @会飞的花 提出的建议：取消强制设置桌面图标、记录上次搜索文件类型、记录上次窗体大小布局 ，新增ppt、pptx、epub、mobi文件类型、完善开机自启等。   
* 0.0.4
  * 2022.11.26 感谢坛友 @会飞的花 提出的建议：添加常用目录功能。   
* 0.0.3
  * 2022.11.24 修改部分bug。
* 0.0.2
  * 2022.11.24 完善了一下代码，感谢坛友 @会飞的花 提出的建议：添加了记录字号、字体、换行、行号、上次搜索目录功能。 
* 0.0.1
  * 2022.11.20 第一次完成项目代码。  

## 界面预览

![预览图](https://pic.imgdb.cn/item/637cd07b16f2c2beb17378f1.png) 

![预览图](https://pic.imgdb.cn/item/637cd07b16f2c2beb17378eb.png)  

![预览图](https://pic.imgdb.cn/item/637cd07b16f2c2beb17378f1.png)  

## 文件下载

* 0.0.7
* [绿色版](https://gaoyongxian.lanzouy.com/iWCJj0hgaiqd)  
* [安装包](https://gaoyongxian.lanzouy.com/i3gJg0hgaeud)
* [32位绿色版](https://gaoyongxian.lanzouy.com/ih4oV0hgahab)  

* 百度网盘下载链接
链接: https://pan.baidu.com/s/1iiFdEUzlq85tpfZgrMdv-Q?pwd=6t85 提取码: 6t85 复制这段内容后打开百度网盘手机App，操作更方便哦


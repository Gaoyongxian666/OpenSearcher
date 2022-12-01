import pyexiv2
# img = pyexiv2.Image(r'C:\Users\Gaoyongxian\Downloads\mobi.png',encoding='GBK')
# data = img.read_exif()
# img.close()
with pyexiv2.Image(r'C:\Users\Gaoyongxian\Desktop\20220909125904000-2-1012410.jpg') as img:
    data = img.read_exif()
    data2 = img.read_iptc()
    data3 = img.read_xmp()
    print(data,data3,data2)


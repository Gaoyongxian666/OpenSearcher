import logging
import os

logger = logging.getLogger(__name__)


def GetTypesDict(IconDir):
    types_dict = {
        "all": {
            "name": "全部文件类型",
            "icon": os.path.abspath(os.path.join(IconDir, 'sysfile.png')),
            "types": [],
            "state": False
        },
        "doc": {
            "name": "Microsoft Word 97-2003 文件",
            "icon": os.path.abspath(os.path.join(IconDir, 'doc.png')),
            "types": [".doc"],
            "state": True
        },
        "docx": {
            "name": "Microsoft Word 文件",
            "icon": os.path.abspath(os.path.join(IconDir, 'docx.png')),
            "types": [".docx"],
            "state": True
        },
        "xls": {
            "name": "Microsoft Excel 97-2003 文件",
            "icon": os.path.abspath(os.path.join(IconDir, 'xls.png')),
            "types": [".xls"],
            "state": True
        },
        "xlsx": {
            "name": "Microsoft Excel 文件",
            "icon": os.path.abspath(os.path.join(IconDir, 'xlsx.png')),
            "types": [".xlsx"],
            "state": True
        },
        "ppt": {
            "name": "Microsoft PowerPoint 97-2003 文件",
            "icon": os.path.abspath(os.path.join(IconDir, 'ppt.png')),
            "types": [".ppt"],
            "state": True
        },
        "pptx": {
            "name": "Microsoft PowerPoint 文件",
            "icon": os.path.abspath(os.path.join(IconDir, 'pptx.png')),
            "types": [".pptx"],
            "state": True
        },
        "wps": {
            "name": "WPS 文字",
            "icon": os.path.abspath(os.path.join(IconDir, 'wps.png')),
            "types": [".wps"],
            "state": True
        },
        "et": {
            "name": "WPS 表格",
            "icon": os.path.abspath(os.path.join(IconDir, 'et.png')),
            "types": [".et"],
            "state": True
        },
        "pdf": {
            "name": "Adobe PDF 文件",
            "icon": os.path.abspath(os.path.join(IconDir, 'pdf.png')),
            "types": [".pdf"],
            "state": True
        },
        "epub": {
            "name": "EPUB 文件",
            "icon": os.path.abspath(os.path.join(IconDir, 'epub.png')),
            "types": [".epub"],
            "state": True
        },
        "mobi": {
            "name": "MOBI 文件",
            "icon": os.path.abspath(os.path.join(IconDir, 'mobi.png')),
            "types": [".mobi"],
            "state": True
        },
        "image": {
            "name": "EXIF、XMP、IPTC 图像元数据",
            "icon": os.path.abspath(os.path.join(IconDir, 'image.png')),
            "types": [".psd"],
            "state": True
        },
        "txt": {
            "name": "文本文档",
            "icon": os.path.abspath(os.path.join(IconDir, 'txt.png')),
            "types": [".txt"],
            "state": True}
    }
    return types_dict


def GetTextTypesDict(IconDir):
    types_dict = {
        "all": {
            "name": "全部文件类型",
            "icon": os.path.abspath(os.path.join(IconDir, 'sysfile.png')),
            "types": [],
            "state": False
        },
        "txt": {
            "name": "文本文档",
            "icon": os.path.abspath(os.path.join(IconDir, 'txt.png')),
            "types": [".txt"],
            "state": True
        },
        "srt": {
            "name": "视频字幕文件",
            "icon": os.path.abspath(os.path.join(IconDir, 'srt.png')),
            "types": [".srt"],
            "state": False
        },
        "json": {
            "name": "JSON 文件",
            "icon": os.path.abspath(os.path.join(IconDir, 'json.png')),
            "types": [".json"],
            "state": False
        },
        "yaml": {
            "name": "YAML 配置文件",
            "icon": os.path.abspath(os.path.join(IconDir, 'yaml.png')),
            "types": [".yaml"],
            "state": False
        },
        "conf": {
            "name": "CONF 配置文件",
            "icon": os.path.abspath(os.path.join(IconDir, 'conf.png')),
            "types": [".conf"],
            "state": False
        },
        "md": {
            "name": "Markdown 文件",
            "icon": os.path.abspath(os.path.join(IconDir, 'md.png')),
            "types": [".md", ".markdown"],
            "state": False
        },
        "html": {
            "name": "HTML 文件",
            "icon": os.path.abspath(os.path.join(IconDir, 'sysfile.png')),
            "types": [".html", ".htm"],
            "state": False
        },
    }
    return types_dict


def GetImageTypesDict(IconDir):
    types_dict = {
        "all": {
            "name": "全部文件类型",
            "icon": os.path.abspath(os.path.join(IconDir, 'image.png')),
            "types": [],
            "state": False
        },
        "psd": {
            "name": "Adobe Photoshop 专用格式",
            "icon": os.path.abspath(os.path.join(IconDir, 'psd.png')),
            "types": [".psd"],
            "state": True
        },
        "png": {
            "name": "PNG 格式",
            "icon": os.path.abspath(os.path.join(IconDir, 'png.png')),
            "types": [".png"],
            "state": False
        },
        "jpg": {
            "name": "JPEG 格式",
            "icon": os.path.abspath(os.path.join(IconDir, 'jpg.png')),
            "types": [".jpg", ".jpeg"],
            "state": False
        },
        "raw": {
            "name": "RAW 格式",
            "icon": os.path.abspath(os.path.join(IconDir, 'raw.png')),
            "types": [".raw"],
            "state": False
        },
        "tiff": {
            "name": "TIFF 标签图像格式",
            "icon": os.path.abspath(os.path.join(IconDir, 'tiff.png')),
            "types": [".tiff"],
            "state": False
        },
        "bmp": {
            "name": "Bitmap 格式",
            "icon": os.path.abspath(os.path.join(IconDir, 'bmp.png')),
            "types": [".bmp"],
            "state": False
        }
    }
    return types_dict


def GetIndexTypesDict(IconDir):
    types_dict = {
        "all": {
            "name": "全部文件类型",
            "icon": os.path.abspath(os.path.join(IconDir, 'sysfile.png')),
            "types": [],
            "state": False
        },
        "doc": {
            "name": "Microsoft Word 97-2003 文件",
            "icon": os.path.abspath(os.path.join(IconDir, 'doc.png')),
            "types": [".doc"],
            "state": True
        },
        "docx": {
            "name": "Microsoft Word 文件",
            "icon": os.path.abspath(os.path.join(IconDir, 'docx.png')),
            "types": [".docx"],
            "state": True
        },
        "xls": {
            "name": "Microsoft Excel 97-2003 文件",
            "icon": os.path.abspath(os.path.join(IconDir, 'xls.png')),
            "types": [".xls"],
            "state": True
        },
        "xlsx": {
            "name": "Microsoft Excel 文件",
            "icon": os.path.abspath(os.path.join(IconDir, 'xlsx.png')),
            "types": [".xlsx"],
            "state": True
        },
        "ppt": {
            "name": "Microsoft PowerPoint 97-2003 文件",
            "icon": os.path.abspath(os.path.join(IconDir, 'ppt.png')),
            "types": [".ppt"],
            "state": True
        },
        "pptx": {
            "name": "Microsoft PowerPoint 文件",
            "icon": os.path.abspath(os.path.join(IconDir, 'pptx.png')),
            "types": [".pptx"],
            "state": True
        },
        "wps": {
            "name": "WPS 文字",
            "icon": os.path.abspath(os.path.join(IconDir, 'wps.png')),
            "types": [".wps"],
            "state": True
        },
        "et": {
            "name": "WPS 表格",
            "icon": os.path.abspath(os.path.join(IconDir, 'et.png')),
            "types": [".et"],
            "state": True
        },
        "pdf": {
            "name": "Adobe PDF 文件",
            "icon": os.path.abspath(os.path.join(IconDir, 'pdf.png')),
            "types": [".pdf"],
            "state": True
        },
        "epub": {
            "name": "EPUB 文件",
            "icon": os.path.abspath(os.path.join(IconDir, 'epub.png')),
            "types": [".epub"],
            "state": True
        },
        "mobi": {
            "name": "MOBI 文件",
            "icon": os.path.abspath(os.path.join(IconDir, 'mobi.png')),
            "types": [".mobi"],
            "state": True
        },
        "psd": {
            "name": "Adobe Photoshop 专用格式",
            "icon": os.path.abspath(os.path.join(IconDir, 'psd.png')),
            "types": [".psd"],
            "state": True
        },
        "png": {
            "name": "PNG 格式",
            "icon": os.path.abspath(os.path.join(IconDir, 'png.png')),
            "types": [".png"],
            "state": False
        },
        "jpg": {
            "name": "JPEG 格式",
            "icon": os.path.abspath(os.path.join(IconDir, 'jpg.png')),
            "types": [".jpg", ".jpeg"],
            "state": False
        },
        "raw": {
            "name": "RAW 格式",
            "icon": os.path.abspath(os.path.join(IconDir, 'raw.png')),
            "types": [".raw"],
            "state": False
        },
        "tiff": {
            "name": "TIFF 标签图像格式",
            "icon": os.path.abspath(os.path.join(IconDir, 'tiff.png')),
            "types": [".tiff"],
            "state": False
        },
        "bmp": {
            "name": "Bitmap 格式",
            "icon": os.path.abspath(os.path.join(IconDir, 'bmp.png')),
            "types": [".bmp"],
            "state": False
        }

    }
    return types_dict



import logging
import traceback
try:
    import pyexiv2
except:
    pass

logger = logging.getLogger(__name__)


def judge_encode(word: str):
    for s in word.encode('utf-8').decode('utf-8'):
        if u'\u4e00' <= s <= u'\u9fff':
            return "gbk"
    else:
        return "utf8"


def anti_encode(encode):
    if encode == "gbk":
        return "utf8"
    else:
        return "gbk"


def get_meta(path, encode):
    with pyexiv2.Image(path, encoding=encode) as img:
        exif_ = ["EXIF信息："]
        iptc_ = ["IPTC信息："]
        xmp_ = ["XMP 信息："]

        try:
            exif = img.read_exif()
            for k, v in exif.items():
                try:
                    exif_.append(k + "：" + v)
                except:
                    pass
        except:
            logger.info(traceback.format_exc())

        try:
            iptc = img.read_iptc()
            for k, v in iptc.items():
                try:
                    iptc_.append(k + "：" + v)
                except:
                    pass
        except:
            logger.info(traceback.format_exc())

        try:
            xmp = img.read_xmp()
            for k, v in xmp.items():
                try:
                    xmp_.append(k + "：" + v)
                except:
                    pass
        except:
            logger.info(traceback.format_exc())

        exif_info = "\n".join(exif_)
        iptc_info = "\n".join(iptc_)
        xmp_info = "\n".join(xmp_)

    info = "\n\n".join(["信息编码："+encode, exif_info, iptc_info, xmp_info])
    return info


def process(path):
    encode = judge_encode(path)
    encode_ = anti_encode(encode)
    encode2 = "ISO-8859-1"
    try:
        text = get_meta(path, encode)
    except:
        logger.info(traceback.format_exc())
        try:
            text = get_meta(path, encode_)
        except:
            logger.info(traceback.format_exc())
            try:
                text = get_meta(path, encode2)
            except:
                logger.info(traceback.format_exc())
                raise
    return text

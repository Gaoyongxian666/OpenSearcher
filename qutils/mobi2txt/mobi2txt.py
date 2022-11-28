import shutil
import chardet
import mobi
import html2text


def detect_encoding(text_file, min_confidence=0.98, text_length=1024):
    """获取文件编码"""
    try:
        with open(text_file, 'rb') as text:
            _ = chardet.detect(text.read(text_length))
            encoding, confidence = _.get("encoding"), _.get("confidence")
            if encoding == "ascii":
                encoding = "utf8"
        if confidence < min_confidence:
            encoding = "utf8"
    except:
        encoding = "utf8"
    return encoding


def process(mobi_path):
    tempdir, filepath = mobi.extract(mobi_path)
    encode = detect_encoding(filepath)

    with open(filepath, "r", encoding=encode, errors='ignore') as file:
        content = file.read()
        text = html2text.html2text(content)
    shutil.rmtree(tempdir)
    return text


if __name__ == "__main__":
    print(process(r"C:\Users\Gaoyongxian\Downloads\T@20181006 (小体积版).mobi"))

import ebooklib
import html2text
from ebooklib import epub


def process(epub_path):
    book = epub.read_epub(epub_path)
    lines = []
    for item in book.get_items():
        spe = "\n------------------------------------------\n\n"
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            lines.append('NAME : ' + item.get_name() + spe + html2text.html2text(item.get_content().decode("utf8")))
    text = "\n".join(lines)
    return text


if __name__ == "__main__":
    print(process(r"C:\Users\Gaoyongxian\Downloads\毛泽东选集1.epub"))

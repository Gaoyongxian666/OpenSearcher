import io

from .xlsx2csv import Xlsx2csv


def process(xlsx_name):
    """xlsx转txt：当行数超过1万行，openpyxl太慢了，使用Xlsx2csv"""
    output = io.StringIO()
    Xlsx2csv(xlsx_name, outputencoding="utf-8").convert(output, 0)
    return output.getvalue()

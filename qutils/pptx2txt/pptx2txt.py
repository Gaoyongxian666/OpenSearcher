from pptx import Presentation
from pptx.shapes.group import GroupShape


def treat_shape(shape):
    lines = []
    if shape.has_text_frame:
        for paragraph in shape.text_frame.paragraphs:
            stripped = paragraph.text.strip()
            if stripped:
                lines.append(stripped)
    elif shape.has_table:
        for row in shape.table.rows:
            for cell in row.cells:
                stripped = cell.text.strip()
                if stripped:
                    lines.append(stripped)
    elif isinstance(shape, GroupShape):
        for item in shape.shapes:
            lines += treat_shape(item)
    return lines


def process(pptx_path):
    prs = Presentation(pptx_path)
    lines = []
    for i, slide in enumerate(prs.slides):
        lines.append("\n第" + str(i + 1) + "页")
        for shape in slide.shapes:
            lines += treat_shape(shape)

    text = "\n".join(lines)
    return text


if __name__ == "__main__":
    print(process(r"C:\Users\Gaoyongxian\Desktop\9科普知识-血气分析的临床应用.pptx"))

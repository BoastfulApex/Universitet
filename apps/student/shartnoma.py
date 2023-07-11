from io import BytesIO
import os
from docx.api import Document
from docx.document import Document as Doc
from docx.table import _Cell
from docx.shared import Pt
from docx2pdf import convert
import qrcode
from docx.shared import Cm


def create_shartnoma(name, id, passport, faculty, number, date, price, mode, template):
    COMMAND = "libreoffice --headless --convert-to pdf {doc} --outdir {out}"

    word_file = open(f".{template}", "rb")

    doc: Doc = Document(word_file)
    res = open(f"./files/agreements/{id}.docx", "wb")

    q = qrcode.make(f'http://185.65.202.40:1009/files/agreements/{id}.pdf')
    q.save('./files/qrcode.png')
    for paragraph in doc.paragraphs:
        t: str = paragraph.text

        if (
                ("{id}" in t)
                or ("{name}" in t)
                or ("{address}" in t)
                or ("{passport}" in t)
                or ("{university}" in t)
                or ("{faculty}" in t)
                or ("{number}" in t)
                or ("{end}" in t)
                or ("{delta}" in t)
                or ("{mode}" in t)
                or ("{lang}" in t)
                or ("{date}" in t)
                or ("{price}" in t)
        ):
            paragraph.text = (
                paragraph.text.replace("{id}", f"{id}")
                .replace("{name}", f"{name}")
                .replace("{date}", f"{date}")
                .replace("{address}", f"")
                .replace("{passport}", f"{passport}")
                .replace("{university}", f"universuty")
                .replace("{faculty}", f"{faculty}")
                .replace("{price}", f"{price}")
                .replace("{number}", f"+{number}")
                .replace("{end}", "2027")
                .replace("{mode}", f"{mode}")
                .replace("{delta}", f"4")
            )

    for table in doc.tables:
        for column in table.columns:
            for row in table.rows:
                cell: _Cell = table.cell(row._index, column._index)
                for p in cell.paragraphs:
                    t: str = p.text
                    if (
                            ("{id}" in t)
                            or ("{name}" in t)
                            or ("{address}" in t)
                            or ("{passport}" in t)
                            or ("{university}" in t)
                            or ("{faculty}" in t)
                            or ("{price}" in t)
                            or ("{number}" in t)
                            or ("{end}" in t)
                            or ("{delta}" in t)
                            or ("{mode}" in t)
                            or ("{lang}" in t)
                            or ("{date}" in t)
                    ):
                        cell.text = (
                            cell.text.replace("{id}", f"{id}")
                            .replace("{name}", f"{name}")
                            .replace("{address}", f"")
                            .replace("{passport}", f"{passport}")
                            .replace("{university}", f"universuty")
                            .replace("{faculty}", f"{faculty}")
                            .replace("{price}", f"{price}")
                            .replace("{number}", f"+{number}")
                            .replace("{end}", "2027")
                            .replace("{mode}", f"{mode}")
                            .replace("{lang}", "O'zbek")
                            .replace("{end}", "2027")
                            .replace("{delta}", f"4")
                        )

    for paragraph in doc.paragraphs:
        if '{qr}' in paragraph.text:
            paragraph.text = paragraph.text.replace('{qr}', "")
            run = paragraph.add_run()
            run.add_picture(f'./files/qrcode.png', width=Cm(3))

        for run in paragraph.runs:
            font = run.font
            font.name = "Tmes New Roman"
            font.size = Pt(8)

        for table in doc.tables:
            for column in table.columns:
                for row in table.rows:
                    cell: _Cell = table.cell(row._index, column._index)
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            font = run.font
                            font.name = "Tmes New Roman"
                            font.size = Pt(8)
                        if '{qr}' in paragraph.text:
                            paragraph.text = paragraph.text.replace('{qr}', "")
                            run = paragraph.add_run()
                            run.add_picture(f'./files/qrcode.png', width=Cm(3))

    doc.save(res)
    # convert(f'./agreements/{id}.docx', f'./agreements/{id}.pdf')
    return os.system(f"libreoffice --headless --convert-to pdf ./files/agreements/{id}.docx --outdir ./files/agreements")

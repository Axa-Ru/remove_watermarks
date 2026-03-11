#!/usr/bin/env python3
# coding=utf-8
#  -*- coding: utf-8 -*-

import PyPDF2
import sys
from pathlib import Path

def usage():
    args = sys.argv[1:]

    print("Автоматическое удаление из pdf файла watermark\n"
          "Должно быть активировано виртуальное окружение и\n"
          "установлены зависимости из файла requirements.txt\n")


    if len(args) != 1:
        print("Не указан входной файл\n\n"

              "Usage:\n"
              "wm_del <input_pdf>")
        exit(255)

    in_pdf_file = Path(args[0])
    if not in_pdf_file.is_file():
        print(f"Файл {in_pdf_file} не найден.")
        exit(255)

    out_pdf_file = Path(args[0]).stem + "_wo_wm" + ".pdf"
    return in_pdf_file, out_pdf_file

def remove_image_watermark(input_pdf, output_path):
    writer = PyPDF2.PdfWriter()
    reader = PyPDF2.PdfReader(input_pdf)


    for page in reader.pages:
        obj = page.get("/Resources").get("/XObject")
        new_obj = PyPDF2.generic.DictionaryObject()
        obj.pop(list(obj)[-1])
        for k in obj:
            value = obj[PyPDF2.generic.NameObject(k)]
            if value is None:
                continue
            new_obj[PyPDF2.generic.NameObject(k)] = value
        page[PyPDF2.generic.NameObject("/Resources")][
            PyPDF2.generic.NameObject("/XObject")] = new_obj
        writer.add_page(page)
        print(f"Обработано страниц : {reader.get_page_number(page)}", end="\r")

    with open(output_path, "wb") as output_file:
        writer.write(output_file)
    print("\nУсё", end="\n")

if __name__ == "__main__":
    input_pdf, output_pdf = usage()
    print(f"Убираю watermark в {output_pdf}")
    remove_image_watermark(input_pdf, output_pdf)

import sys
sys.path.append('/braillest/src')
from Book import Book

book = Book()

print("Path of input text file:")
book.text_path = input()
print("Path of output braille file:")
book.braille_path = input()
print("Path of output formatted braille file:")
book.formatted_braille_path = input()
print("Path of output back translation file:")
book.back_translation_path = input()

book.load_text_file()
book.translate_text_file_to_braille()
book.load_braille_file()
book.format_braille_file()
book.back_translate_braille_file_to_text()
book.load_formatted_braille_file()
pages = book.paginate_formatted_braille_file()
for index, page in enumerate(pages):
    with open(f"/braillest/data/pages/{index}.txt", "w") as out_file:
        for line in page:
            out_file.write(line)

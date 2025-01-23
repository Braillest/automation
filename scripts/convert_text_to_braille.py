import sys
sys.path.append('/braillest/src')
from Book import Book

book = Book()

print("Path of input text file:")
book.text_path = input()
print("Path of output braille file:")
book.braille_path = input()

book.load_text_file()
book.translate_text_file_to_braille()

import sys
sys.path.append('/braillest/src')
from Book import Book

book = Book()

book.text_path = "/braillest/data/revisions/Romeo and Juliet by William Shakespeare (2546).txt"
book.braille_path = "/braillest/data/braille/Romeo and Juliet by William Shakespeare (2546).txt"
book.formatted_braille_path = "/braillest/data/formatted/Romeo and Juliet by William Shakespeare (2546).txt"
book.back_translation_path = "/braillest/data/back-translation/Romeo and Juliet by William Shakespeare (2546).txt"
book.pages_directory_path = "/braillest/data/pages/"

book.load_text_file()
book.translate_text_file_to_braille()
book.load_braille_file()
book.format_braille_file()
book.back_translate_braille_file_to_text()
book.load_formatted_braille_file()
book.paginate_formatted_braille_file()

print(book.character_x_count)
print(book.character_y_count)

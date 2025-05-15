import os
import re

RAW_BOOKS_PATH = 'raw_data/books/'
PREPARED_BOOKS_PATH = 'prepared_data/books/'


def prepare_line(text):
    """Process a single paragraph of text."""
    text = text.replace('\n', '').strip()
    if not text or text[-1] not in ['?', '!', '.', ',', '–']:
        return ''
    text = re.sub(r"\[[0-9]+\]", '', text)
    text = re.sub(r"\[{0-9}+\]", '', text)
    for quote in ['«', '»', "'"]:
        text = text.replace(quote, '"')
    text = ' '.join(text.split())
    return text.strip()


def write_prepared_book(book_name):
    with open(os.path.join(RAW_BOOKS_PATH, book_name), encoding='utf-8') as infile:
        lines = [prepare_line(line) for line in infile if line.strip()]
        lines = [line for line in lines if line]
    with open(os.path.join(PREPARED_BOOKS_PATH, book_name), 'w', encoding='utf-8') as outfile:
        for line in lines:
            outfile.write(line + '\n')
    print(f"{book_name} is done!")


if __name__ == "__main__":
    # Specify your list of book file names here
    book_file_names = os.listdir(RAW_BOOKS_PATH)
    for book in book_file_names:
        write_prepared_book(book) 
import os
import pandas as pd
import tqdm

BOOKS_PATH = 'prepared_data/books/'

book_file_names = os.listdir(BOOKS_PATH)

def get_book(book_name):
    with open(os.path.join(BOOKS_PATH, book_name), encoding='utf-8') as file:
        return [line.rstrip('\n') for line in file]

def get_markup(tokens):
    """Return punctuation label for each token."""
    puncts = ['.', ',', '?', '!']
    return [token[-1] if token and token[-1] in puncts else 'o' for token in tokens]

if __name__ == "__main__":
    all_markup = []
    for book in tqdm.tqdm(book_file_names):
        book_text = get_book(book)
        for text in book_text:
            tokens = text.split(' ')
            labels = get_markup(tokens)
            all_markup.append({'text': text, 'tokens': tokens, 'labels': labels})
    df = pd.DataFrame(all_markup)
    df.to_csv('books_markup.csv', index=False)
    # Label statistics
    labels_flat = [label for row in df['labels'] for label in row]
    print('Total labels:', len(labels_flat))
    print(pd.Series(labels_flat).value_counts()) 
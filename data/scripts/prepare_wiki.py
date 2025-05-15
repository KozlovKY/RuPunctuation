import os
import re
import tqdm

WIKI_PATH = 'wiki/'
EDITED_PATH = 'all_articles_edited/'

# Preprocess Wikipedia articles
folders = os.listdir(WIKI_PATH)
for folder in tqdm.tqdm(folders):
    files = os.listdir(os.path.join(WIKI_PATH, folder))
    for filename in files:
        with open(os.path.join(WIKI_PATH, folder, filename), 'r') as infile:
            for line in infile:
                line = re.sub(r'\n', '', line)
                line = re.sub(r'<.*>', '', line)
                line = re.sub(r'/&.*;', '', line)
                line = re.sub(r'&.*;', '', line)
                line = re.sub(r'formula[0-9]+', '', line)
                line = re.sub(r'templatestyles .*"', '', line)
                line = re.sub(r'См. также.', '', line)
                line = re.sub(r'(#ПЕРЕНАПРАВЛЕНИЕ)', '', line)
                line = re.sub(r'\[\[(.*?)\]\]', '', line)
                line = re.sub(r'\s+', ' ', line)
                line = re.sub(r"'", '"', line)
                line = re.sub(r'«', '"', line)
                line = re.sub(r'»', '"', line)
                line = line.strip()
                if not line or (line[-1] not in ['.', '!', '?']) or (len(line.split(' ')) <= 1) or (line[0] in ['.', '!', '?', ',']):
                    continue
                with open(os.path.join(EDITED_PATH, f'{folder}.txt'), 'a') as outfile:
                    outfile.write(line + '\n')

# Corpus statistics
folders = os.listdir(EDITED_PATH)
counter = {'Paragraphs': 0, 'Total labels': 0, '?': 0, 'o': 0, '!': 0, '.': 0, ',': 0}
for file_name in tqdm.tqdm(folders):
    with open(os.path.join(EDITED_PATH, file_name), 'r') as infile:
        for line in infile:
            line = line.rstrip('\n')
            counter['Paragraphs'] += 1
            tokens = line.split(' ')
            counter['Total labels'] += len(tokens)
            for token in tokens:
                if token[-1] == '.':
                    counter['.'] += 1
                elif token[-1] == ',':
                    counter[','] += 1
                elif token[-1] == '?':
                    counter['?'] += 1
                elif token[-1] == '!':
                    counter['!'] += 1
                else:
                    counter['o'] += 1
print(counter) 
# Data Description

This project utilizes data collected from multiple sources for modeling purposes.

## Literary Works

Sixteen books in `.txt` format were manually downloaded from [avidreaders.ru](https://avidreaders.ru), and subsequently cleaned to remove unpredictable lines at the beginning and footnotes at the end. The raw texts (available in `raw_data/books/`) were processed using the `filter_books.ipynb` script (the processed texts can be found in `prepared_data/books/`) and then annotated with the `get_markup_books.ipynb` notebook. In total, this process yielded 47,756 paragraphs containing 1,993,736 labels (1,592,668 `o`, 262,814 `,`, 107,422 `.`, 16,188 `!`, and 14,644 `?`). The final annotated dataset for the books is stored in the `books_markup.csv` file, which is included in the repository due to its manageable size.

## Wikipedia

All articles from the Russian-language Wikipedia were processed using the [`wikiextractor`](https://github.com/attardi/wikiextractor) library. The raw article texts were obtained with the following terminal commands:

```bash
git clone https://github.com/attardi/wikiextractor.git
cd wikiextractor
wget http://dumps.wikimedia.org/ruwiki/latest/ruwiki-latest-pages-articles.xml.bz2
python -m wikiextractor.WikiExtractor ruwiki-latest-pages-articles.xml.bz2
```

This process resulted in the extraction of texts from 4,629,511 articles. The entire data collection took approximately 12 hours, considering the slow internet connection used for downloading the dump. The raw texts were saved in a directory structure (with subfolders containing up to 100 text files each), totaling 9 GB in size. These texts were further processed using the `prepare_wiki.ipynb` script and uploaded as a `.zip` archive to Google Drive [here](https://drive.google.com/drive/folders/1t9F57KvJ0e10PjHJ1ZrlHkt8zQYX0Br9).

At this stage, the exact volume of Wikipedia data to be used for training remains undetermined, and additional quality checks are necessary to filter out noisy texts. Consequently, annotated Wikipedia data has not yet been provided in any file (though generating such annotations would be straightforward, following the approach in `get_markup_books.ipynb`). For completeness, the following metrics were calculated for the processed Wikipedia dataset (using the `prepare_wiki.ipynb` script):

| Metric         | Value        |
|----------------|--------------|
| Paragraphs     | 14,813,389   |
| Labels         | 555,674,748  |
| o              | 474,669,460  |
| .              | 40,085,706   |
| ,              | 40,846,537   |
| !              | 39,084       |
| ?              | 33,961       |

A substantial amount of data has been collected; however, as previously mentioned, its quality has only been superficially assessed. The most common issue observed in the Wikipedia data is the presence of special Unicode characters. It is recommended to exclude such texts during model training.



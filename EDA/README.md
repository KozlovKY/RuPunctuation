# EDA

During the exploratory data analysis, collected texts from Wikipedia (as of October 23) and 14 randomly selected books were reviewed.

## Wikipedia

* The dataset is quite large: 14 million paragraphs and about 500 million labels (36 labels per paragraph). The completeness of the texts hypothetically ensures high training quality. However, resource limitations do not allow the use of the entire dataset.

* There is a label imbalance in the texts (as noted in related articles). After 82% of words, there is no punctuation mark. The most common punctuation marks in Wikipedia are the comma, period, and dash. The least common are exclamation and question marks, as well as ellipses. Wikipedia mainly contains articles, and various intonations typical of journalistic style are rare (hence the addition of fiction in training).

* The data is dominated by short sentences: half of the paragraphs contain no more than 26 words. Most paragraphs contain no more than 2500 characters, which should be sufficient for use with models like BERT.

## Books

* In books, the class imbalance shifts—the share of commas among all marks increases by +6.0 percentage points.
* Emotional marks (? and !) appear more frequently (+0.4 percentage points).
* The proportion of words without punctuation decreases from 82% to 79% compared to Wikipedia.
* The volume is 28 thousand paragraphs, with 1.3 million labels (46 labels per paragraph), indicating that book texts are longer, but short ones are also present.
* The average paragraph length is 46 sentences.

## Summary

* During the exploratory data analysis, errors in the data were identified and corrected: various technical symbols and combinations.
* For the training baseline, it was decided to filter out certain punctuation combinations such as {",-}, {)-}, and similar patterns.
* Some infographics on the data can be found in the `pictures/` folder.

| Label | Wikipedia | Books | Difference with Wikipedia |
|-------|-----------|-------|--------------------------|
| ,     | 7.4%      | 13.3% | 6.0%                     |
| ?     | 0.0%      | 0.4%  | 0.4%                     |
| ;     | 0.2%      | 0.6%  | 0.4%                     |
| !     | 0.0%      | 0.4%  | 0.4%                     |
| ...   | 0.0%      | 0.2%  | 0.2%                     |
| :     | 0.3%      | 0.3%  | 0.0%                     |
| —     | 1.2%      | 0.7%  | -0.5%                    |
| )     | 0.6%      | 0.1%  | -0.6%                    |
| "     | 0.8%      | 0.1%  | -0.7%                    |
| .     | 7.2%      | 5.2%  | -2.0%                    |
| o     | 82.3%     | 78.7% | -3.6%                    |

The final markup was created after data analysis using the `create_markup.ipynb` file. Train, Validation, and Test sets were generated, and label statistics for these sets are provided in the same notebook. In the future, the markup may be reduced, as the current `train.csv` file size exceeds 800 MB.


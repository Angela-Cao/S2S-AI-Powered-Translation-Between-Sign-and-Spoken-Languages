import pandas as pd
import string
import re
import nltk
from pycountry import countries

def clean_gloss(csv_file, out_csv_file):

    nltk.download('words')
    english_words = set(nltk.corpus.words.words())

    df = pd.read_csv()

    df.replace(to_replace=[re.escape(char) for char in string.punctuation], value=' ', regex=True, inplace=True)
    indices_to_drop = []

    for index, row in df.iterrows():
        words = nltk.wordpunct_tokenize(row['gloss'].lower())        
        words_without_desc_x = [word for word in words if word not in ('desc', 'x')]
        non_english_words = [word for word in words_without_desc_x if not (word.isdigit() or word in english_words)]
        valid_country_names = [word for word in words_without_desc_x if countries.get(name=word)]
        if non_english_words:
            print(f"Row {index}: Non-English words found - {non_english_words}")
            indices_to_drop.append(index)
        else:
            print(f"Row {index}: No Non-English words")
        df.at[index, 'gloss'] = ' '.join(map(str, words_without_desc_x + valid_country_names))
    df.drop(indices_to_drop, inplace=True)

    df.to_csv(out_csv_file, index=False)
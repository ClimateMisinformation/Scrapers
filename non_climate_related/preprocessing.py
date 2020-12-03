import pandas as pd
import numpy as np
import re
import string
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))
punctuation = string.punctuation.replace('-', '')


# Counting NA values and transforming NA to empty strings
def na_values(df):
    print("NaN values per column")
    print(df.isna().sum())

    df.dropna(subset=['text'], inplace=True)
    df = df.replace(np.nan, '', regex=True)
    return df


# Exploring len of articles
def article_len_exploration(list_of_texts, new_df):
    text_lens = []

    for text in list_of_texts:
        text_lens.append(len(text.split()))

    new_df['text_lens'] = text_lens
    print('Article length distributon')
    print(new_df['text_lens'].describe())

    print('Histogram lens of articles')
    plt.hist(new_df['text_lens'], bins=50)
    plt.ylabel('len articles')
    plt.show()


# Basic preprocessing
def preprocessing(texts):
    print(len(texts))

    list_clean_text = []
    for text in texts:
        text = text.lower()
        split_text = re.split('-| |\n', text)

        # Remove URLS
        split_text = [re.sub(
            '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})',
            '', sent) for sent in split_text]

        # Remove new line characters
        split_text = [re.sub('\s+', ' ', sent) for sent in split_text]
        split_text = [re.sub('\n', ' ', sent) for sent in split_text]

        # Remove all special characters
        split_text = [re.sub("[^A-Za-z0-9]+", " ", sent) for sent in split_text]

        # Clean punctuation
        table = str.maketrans(' ', ' ', punctuation)
        split_text_no_punct = [w.translate(table) for w in split_text]

        # Remove numbers?
        clean_text = [x for x in split_text_no_punct if not (x.isdigit())]
        list_clean_text.append(clean_text)

    return list_clean_text


df = pd.read_csv('1000_normalised_articles.csv')

print('Dataframe imported')
print('Size of dataframe')
print(df.columns)
print(df.shape)

print(df.head())

df = na_values(df)

list_of_texts = df['text'].tolist()
list_of_titles = df['title'].tolist()

article_len_exploration(list_of_texts, df)

clean_text = preprocessing(list_of_texts)
clean_titles = preprocessing(list_of_titles)

df['clean_text'] = clean_text
df['clean_title'] = clean_titles

print(df.head())

df.to_csv('preprocessed_non_climate_related_articles.csv')

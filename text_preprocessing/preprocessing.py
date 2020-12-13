import pandas as pd
import numpy as np
import re
import string
import matplotlib.pyplot as plt
from nltk import WordNetLemmatizer, SnowballStemmer
from nltk.corpus import stopwords
import emoji
stemmer = SnowballStemmer("english")
lemmatizer = WordNetLemmatizer()

stop_words = set(stopwords.words('english'))
punctuation = string.punctuation.replace("-", "")
punctuation = punctuation.replace("!", "")
punctuation = punctuation.replace("?", "")
punctuation = punctuation.replace(".", "")

print(punctuation)


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

    list_clean_text = []
    for text in texts:
        text = text.lower()
        split_text = re.split('-| |\n', text)
        #split_text = re.findall(r"[\w']+|[!?]", text)
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

        # Remove numbers
        clean_text = [x for x in split_text_no_punct if not (x.isdigit())]


        clean_text = advanced_text_cleaning(clean_text)

        list_clean_text.append(clean_text)

    return list_clean_text


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def hasEmoji(inputString):
    return any(char in emoji.UNICODE_EMOJI for char in inputString)


def advanced_text_cleaning(clean_article):
    advanced_clean_article = []
    for w in clean_article:

        w = w.replace("’s", "")
        w = w.replace("share", "")

        if hasNumbers(w) == True:
            w = ""
        if hasEmoji(w) == True:
            w = ""

        regex = re.compile('[^a-zA-Z]')
        w = regex.sub('', w)

        listWordsLemmatizer = ["us","has", "was", "as"]

        if w not in listWordsLemmatizer:
            w = lemmatizer.lemmatize(w)
            w = lemmatizer.lemmatize(w, pos='v')
            w = lemmatizer.lemmatize(w, pos='n')
            w = lemmatizer.lemmatize(w, pos='a')
        else:
            w = w

        w = w.replace("thisfacebooktwitterin", "")
        w = w.replace("facebooktwitterin", "")
        if w != '':
            advanced_clean_article.append(w)

    clean_splitted_text_no_stopw = []

    for w in advanced_clean_article:
        if w not in stop_words:
            clean_splitted_text_no_stopw.append(w)

    return clean_splitted_text_no_stopw


df = pd.read_csv('../format_data_for_doccano/doccano_data/doccano_data0.csv', names=['text', 'labels'])

print('Dataframe imported')
print('Size of dataframe')
print(df.columns)
print(df.shape)

print(df.head())

df = na_values(df)

list_of_texts = df['text'].tolist()

article_len_exploration(list_of_texts, df)

clean_text = preprocessing(list_of_texts)

df['clean_text'] = clean_text

print(df.head())

df.to_csv('preprocessed_data_test.csv')

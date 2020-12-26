from preprocessing import *
from word2vec import *

#TODO: create import function

df = pd.read_csv('../labelled_data/labelled_data.csv', header = 0)

df.drop(df.columns.difference(['text','label']), 1, inplace=True)

print(df.head())

print('Size of dataframe')
print(df.columns)
print(df.shape)

df = na_values(df)

print(df.shape)

df = class_encoding(df)

list_of_texts = df['text'].tolist()

article_len_exploration(list_of_texts, df)

clean_text = preprocessing(list_of_texts)

df['clean_text'] = clean_text

print(df.head())

docs = clean_text

print("Number of articles",len(docs))

list_of_dicts, list_of_lists, words_not_found_list = get_vectors(docs)
list_of_averages = average_vectors(list_of_lists)

print(len(list_of_averages))
print(len(list_of_averages[0]))

averages_df = pd.DataFrame(list_of_averages)

print(averages_df.head())
print(averages_df.shape)

averages_df['classes']=df['labels'].to_list()

averages_df.to_csv('word2vectest.csv')

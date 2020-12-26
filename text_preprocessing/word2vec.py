import pandas as pd
import numpy as np
import gensim
import gensim.downloader as api



def get_vectors(corpus):
    list_of_dicts = []
    list_of_lists = []

    words_not_found = 0
    words_found = 0
    words_not_found_list = []

    for doc in corpus:
        vector_dictionary = {}
        vector_list = []

        if not doc:
            vector = np.zeros(300)
            vector_list.append(vector)

        else:
            for word in doc:
                try:
                    vector = model.get_vector(word)
                    # print(word, vector)
                    vector_dictionary[word] = vector
                    vector_list.append(vector)
                    words_found += 1
                    words_not_found_list.append(word)
                except KeyError:
                    vector_dictionary[word] = False
                    words_not_found += 1

        list_of_dicts.append(vector_dictionary)
        list_of_lists.append(vector_list)




    print("words not found ", words_not_found)
    print("words found ", words_found)

    print("% of words not found ", (words_not_found / (words_not_found + words_found)) * 100)

    return list_of_dicts, list_of_lists, words_not_found_list


def average_vectors(vector_list):
    list_of_series = []

    for list in vector_list:
        list_of_series.append(pd.Series(list))

    list_of_vector_averages = []

    for list_of_vectors in list_of_series:
        list_of_vector_averages.append(np.mean(list_of_vectors, axis=0))

    return list_of_vector_averages

print("Loading word2vec model")

path = api.load('word2vec-google-news-300', return_path=True)

model = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)

#print("Importing DF")
#df = pd.read_csv('preprocessed_data_test.csv', index_col=0, header = 0, converters={'clean_text': eval})

#df = df[0:10]

#print(df['labels'])

#print(df.shape)
#print(df)
#print(df.columns)


#docs = df['clean_text'].tolist()
#print("Number of articles",len(docs))




#average_final = list_of_averages.tolist()

#print(words_not_found_list[0:100])

#print(list_of_averages[0:1])






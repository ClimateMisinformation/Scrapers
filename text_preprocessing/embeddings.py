from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import gensim
import gensim.downloader as api


######################## WORD2VEC EMBEDDINGS ################################


def word2vec_vectorizer(df):
    print("Loading word2vec model")

    path = api.load('word2vec-google-news-300', return_path=True)

    model = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)

    docs = df['clean_text'].to_list()

    print("Number of articles", len(docs))

    list_of_dicts, list_of_lists, words_not_found_list = get_vectors(docs, model)
    list_of_averages = average_vectors(list_of_lists)

    print(len(list_of_averages))
    print(len(list_of_averages[0]))

    averages_df = pd.DataFrame(list_of_averages)

    print(averages_df.head())
    print(averages_df.shape)

    averages_df['classes'] = df['labels'].to_list()

    return averages_df

def get_vectors(corpus, model):
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


######################## TF IDF EMBEDDINGS ################################


def dummy_fun(doc):
    return doc

def tf_idf_vectorizer(df):

    tfidf = TfidfVectorizer(
        analyzer='word',
        tokenizer=dummy_fun,
        preprocessor=dummy_fun,
        token_pattern=None, min_df=5)

    docs = df['clean_text'].to_list()

    print("Number of articles", len(docs))

    tfidf.fit(docs)

    # These are the feature indices
    vocab = tfidf.vocabulary_
    print("Length vocab: ", len(vocab))

    # Dataframe names
    sorted_vocab_list = [k for k, v in sorted(vocab.items())]
    # print(sorted_vocab_dict)

    print("Constructing vectors...")

    vectors = []

    #TODO: list comprehension
    for doc in docs:
        vector = tfidf.transform([doc])
        # print(vector.shape)
        vectors.append(vector)

    vectors_two = [matrix.toarray() for matrix in vectors]

    vectors_three = []
    for x in vectors_two:
        x = x.flatten()
        x = pd.Series(x)
        vectors_three.append(x)

    final_df = pd.DataFrame(vectors_three)
    final_df.columns = sorted_vocab_list

    classes = df['labels'].tolist()

    final_df['classes'] = classes

    print("Size of dataframe ", final_df.shape)

    return final_df
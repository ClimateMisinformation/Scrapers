from preprocessing import *
from embeddings import *

############################## PREPROCESSING #################################

def preprocessing_pipeline(path, embedding_technique):

    print("Importing data...")
    df = import_data(path)

    print("Dropping na values..")
    df = na_values(df)

    print("Encoding classes..")
    df = class_encoding(df)

    print("Exploring length of articles..")
    article_len_exploration(df)

    print("Starting text preprocessing..")
    clean_text = preprocessing(df)

    df['clean_text'] = clean_text

    print(df.head())

    embedded_df = embedding(embedding_technique)

    return embedded_df

############################## EMBEDDING #################################

def embedding(embedding_technique):

    if embedding_technique == 'word2vec':

        print("Initialising Word2Vec vectorization")
        embedded_df = word2vec_vectorizer(df)
        embedded_df.to_csv('../model_evaluation/embedding_data/word2vectest.csv')

    elif embedding_technique == 'tfidf':

        print("Initialising tf-idf vectorization")
        embedded_df = tf_idf_vectorizer(df)
        embedded_df.to_csv('../model_evaluation/embedding_data/tfidftest.csv')

    else:
        print("ERROR. Please select one of the possible embedding techniques: word2vec, tfidf")


    return embedded_df

############################## MAIN #################################


path = '../labelled_data/labelled_data.csv'
embedding_technique = 'tfidf'

preprocessing_pipeline(path, embedding_technique)

#TODO: change here the name of final output and check if path works

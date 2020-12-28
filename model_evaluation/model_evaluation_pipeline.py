from models import *


def import_data(embedding):

    try:

        data = pd.read_csv("embedding_data/" + embedding + "test.csv", index_col=0)
        print("Data loaded ", embedding)
        print("Dataset shape ", data.shape)
    except:

        print("Error loading embedding data. Possible embedding types are: word2vec and tfidf")

    print("Splitting data into train and test")
    X_train, Y_train, X_test, Y_test = split_train_test(data)

    return X_train, Y_train, X_test, Y_test

def fit_predict(model, X_train, Y_train, X_test, Y_test):

    if model == 'onevsrest':
        One_VS_Rest_SVM(X_train, Y_train, X_test, Y_test)
    elif model == 'onevsone':
        One_vs_One_SVM(X_train, Y_train, X_test, Y_test)
    elif model == 'randomforest':
        RandomForest(X_train, Y_train, X_test, Y_test)
    elif model == 'adaboost':
        AdaBoost(X_train, Y_train, X_test, Y_test)
    else:
        print("Error, potential models are: onevsrest, onevsone, randomfores and adaboost")

    return


embeddings = ['word2vec','tfidf']
models = ['onevsrest', 'onevsone', 'randomforest','adaboost']

for embedding in embeddings:
    print(embedding.upper())
    X_train, Y_train, X_test, Y_test = import_data(embedding)
    for model in models:
        fit_predict(model, X_train, Y_train, X_test, Y_test)
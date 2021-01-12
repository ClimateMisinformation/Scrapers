import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.multiclass import OneVsOneClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier


def split_train_test(data):

    training_set, test_set = train_test_split(data, test_size=0.2, random_state=1)

    print("Training shape ", training_set.shape)
    print("Test shape ", test_set.shape)

    print("Training target distributions ")
    print(training_set['classes'].value_counts())
    print("Test target distributions ")
    print(test_set['classes'].value_counts())

    X_train = training_set.iloc[:, :-1].values
    Y_train = training_set.iloc[:, -1].values
    X_test = test_set.iloc[:, :-1].values
    Y_test = test_set.iloc[:, -1].values

    return X_train, Y_train, X_test, Y_test


def evaluation(Y_test, Y_pred, model):
    cm = confusion_matrix(Y_test, Y_pred)
    accuracy = float(cm.diagonal().sum()) / len(Y_test)
    print("Accuracy of " + model + " on test set : ", accuracy)

    print(cm)

    return

def One_VS_Rest_SVM(X_train, Y_train, X_test, Y_test):

    model = 'one vs rest svm'

    classifier = OneVsRestClassifier(SVC(kernel='linear', class_weight='balanced', probability=True))

    classifier.fit(X_train, Y_train)

    Y_pred = classifier.predict(X_test)

    evaluation(Y_test, Y_pred, model)

    return

def One_vs_One_SVM(X_train, Y_train, X_test, Y_test):
    model = 'one vs one svm'

    classifier = OneVsOneClassifier(SVC(kernel='linear', class_weight='balanced', probability=True, decision_function_shape='ovo'))
    classifier.fit(X_train, Y_train)

    Y_pred = classifier.predict(X_test)

    evaluation(Y_test, Y_pred, model)
    return

def RandomForest(X_train, Y_train, X_test, Y_test):
    model = 'random forest'


    #TODO: FINE TUNE RANDOM FOREST
    classifier = RandomForestClassifier(n_estimators=30)
    classifier.fit(X_train, Y_train)

    Y_pred = classifier.predict(X_test)

    evaluation(Y_test, Y_pred, model)

    return

def AdaBoost(X_train, Y_train, X_test, Y_test):
    model = 'ada boost'

    classifier = OneVsRestClassifier(AdaBoostClassifier(
        base_estimator=None,
        n_estimators=100,
        learning_rate=1.0,
        algorithm='SAMME',
        random_state=123))
    classifier.fit(X_train, Y_train)

    Y_pred = classifier.predict(X_test)

    evaluation(Y_test, Y_pred, model)
    return

# -*- coding:utf-8 -*-

__author__ = 'kevin'


def normalize1(X):
    from sklearn import preprocessing
    # scale the data attributes
    scaled_X = preprocessing.scale(X)
    print scaled_X

    # normalize the data attributes
    normalized_X = preprocessing.normalize(X)
    print normalized_X


def normalize2(X):
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    scaler.fit(X)  # Don't cheat - fit only on training data

    X_train = scaler.transform(X)
    print X_train


def normalize3(X,y):
    from sklearn.grid_search import GridSearchCV
    from sklearn.linear_model import SGDClassifier
    parameters = {'alpha': [0.1, 1, 10]}

    sgd = SGDClassifier()
    clf = GridSearchCV(sgd, parameters)
    clf.fit(X, y)
    print clf

if __name__ == '__main__':
    # 1. 加载数据(Data Loading)

    import numpy as np
    import urllib
    # url with dataset
    url = "http://archive.ics.uci.edu/ml/machine-learning-databases/pima-indians-diabetes/pima-indians-diabetes.data"
    # download the file
    raw_data = urllib.urlopen(url)
    # load the CSV file as a numpy matrix
    dataset = np.loadtxt(raw_data, delimiter=",")
    # separate the data from the target attributes
    X = dataset[:, 0:7]
    y = dataset[:, 8]

    # 2. 数据归一化(Data Normalization)
    # scale
    #normalize1(X)

    # StandardScaler
    #normalize2(X)

    # cv
    normalize3(X,y)

    raw_data.close()

    pass

# -*- coding:utf-8 -*-

__author__ = 'kevin'

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

    # 朴素贝叶斯

    from sklearn import metrics
    from sklearn.naive_bayes import GaussianNB
    model = GaussianNB()
    model.fit(X, y)
    print('MODEL')
    print(model)
    # make predictions
    expected = y
    predicted = model.predict(X)
    # summarize the fit of the model
    print('RESULT')
    print(metrics.classification_report(expected, predicted))
    print('CONFUSION MATRIX')
    print(metrics.confusion_matrix(expected, predicted))
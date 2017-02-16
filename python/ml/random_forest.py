# -*- coding:utf-8 -*-

from sklearn import ensemble
from sklearn import metrics
from sklearn import cross_validation as cv

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

    x_train, x_test, y_train, y_test = cv.train_test_split(X, y, test_size=0.3)
    # fit a CART model to the data
    model = ensemble.RandomForestClassifier(n_jobs=2)
    print(model)
    model.fit(x_train, y_train)

    # make predictions
    expected = y_test
    predicted = model.predict(x_test)
    # summarize the fit of the model
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))
    print '*'*10
    score = model.score(x_test, y_test)
    print score
    print model.classes_
    print model.n_classes_
    print model.min_weight_fraction_leaf
    print model.max_leaf_nodes
    print '*'*10
    ''''' 系数反映每个特征的影响力。越大表示该特征在分类中起到的作用越大 '''
    print(model.feature_importances_)
    # 0:1
    probas = model.predict_proba(X=x_test)
    print probas[0:5, 1]
    pass

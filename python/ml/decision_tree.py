# -*- coding:utf-8 -*-
import numpy as np
import scipy as sp
from sklearn import tree
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

    # 决策树:分类与回归树(Classification and Regression Trees ,CART)算法
    x_train, x_test, y_train, y_test = cv.train_test_split(X, y, test_size=0.3)
    # fit a CART model to the data
    model = tree.DecisionTreeClassifier(criterion='entropy')
    print(model)
    model.fit(x_train, y_train)

    # make predictions
    expected = y_test
    predicted = model.predict(x_test)
    # summarize the fit of the model
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))

    # 把决策树结构写入文件
    path = "/home/kevin/temp/model/%s"
    with open(path % "tree.dot", 'w') as f:
        f = tree.export_graphviz(model, out_file=f)

    ''''' 系数反映每个特征的影响力。越大表示该特征在分类中起到的作用越大 '''
    print(model.feature_importances_)

    probas = model.predict_proba(X=x_test)
    print probas[0:10,:]
    pass

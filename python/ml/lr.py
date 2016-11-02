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

    # 4. 算法的使用：逻辑回归：大多数问题都可以归结为二元分类问题。这个算法的优点是可以给出数据所在类别的概率。

    from sklearn import metrics
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression(penalty='l2',max_iter=10,n_jobs=10)
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
    '''
    查准率，查全率，f1-score是前两者混合运算结果，样本数
    RESULT
                 precision    recall  f1-score   support

            0.0       0.79      0.89      0.84       500
            1.0       0.74      0.55      0.63       268

    avg / total       0.77      0.77      0.77       768

    CONFUSION MATRIX:expected,predicted
    [[447  53]
     [120 148]]
    '''
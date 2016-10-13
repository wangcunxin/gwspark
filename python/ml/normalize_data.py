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

    # 2. 数据归一化(Data Normalization)

    from sklearn import preprocessing
    # scale the data attributes
    scaled_X = preprocessing.scale(X)

    # normalize the data attributes
    normalized_X = preprocessing.normalize(X)
    print normalized_X

    # standardize the data attributes
    standardized_X = preprocessing.scale(X)
    print standardized_X

    raw_data.close()

    pass
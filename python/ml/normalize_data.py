# -*- coding:utf-8 -*-

__author__ = 'kevin'


def scale_normalize(X):
    # 标准化与归一化
    from sklearn import preprocessing
    # scale the data attributes : z-score
    scaled_X = preprocessing.scale(X)
    print scaled_X[0]

    # normalize the data attributes
    normalized_X = preprocessing.normalize(X)
    print normalized_X[0]


def scale(X):
    '''
    数据标准化:标准化的前提是特征值服从正态分布，标准化后，其转换成标准正态分布
    无量纲化方法有标准化和区间缩放法
    标准化:z-score
    区间缩放法:MinMaxScaler
    '''
    # 标准化:z-score
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    scaler.fit(X)
    print X[0]

    x = scaler.transform(X)
    #x = scaler.fit_transform(X)
    print x[0]

    # 区间缩放法:MinMaxScaler
    from sklearn.preprocessing import MinMaxScaler
    # 区间缩放，返回值为缩放到[0, 1]区间的数据
    x = MinMaxScaler().fit_transform(X)
    print x[0]

def normalize(X):

    from sklearn.preprocessing import Normalizer
    # 归一化，返回值为归一化后的数据
    x = Normalizer().fit_transform(X)
    print x[0]

def cv(X,y):

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

    # 2. 数据无量纲化
    '''
    标准化与归一化的区别
    简单来说，标准化是依照特征矩阵的列处理数据，其通过求z-score的方法，将样本的特征值转换到同一量纲下
    归一化是依照特征矩阵的行处理数据，其目的在于样本向量在点乘运算或其他核函数计算相似性时，拥有统一的标准，也就是说都转化为“单位向量”.
    '''
    scale_normalize(X)

    # 数据标准化
    scale(X)

    # 数据归一化[0,1]
    normalize(X)

    # SGD对于数据的缩放很敏感,最好先对数据进行缩放（scale）处理
    # 交叉验证:cv,取得最佳参数值
    cv(X,y)

    raw_data.close()

    pass

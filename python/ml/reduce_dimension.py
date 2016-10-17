# -*- coding:utf-8 -*-
import numpy as np
import urllib

__author__ = 'kevin'

if __name__ == '__main__':
    '''
    降维:
    特征选择完成后，可以直接训练模型了，但是可能由于特征矩阵过大，导致计算量大，训练时间长的问题
    降维方法:主成分分析法（PCA）和线性判别分析（LDA）

    '''
    # url with dataset
    url = "http://archive.ics.uci.edu/ml/machine-learning-databases/pima-indians-diabetes/pima-indians-diabetes.data"
    # download the file
    raw_data = urllib.urlopen(url)
    # load the CSV file as a numpy matrix
    dataset = np.loadtxt(raw_data, delimiter=",")
    # separate the data from the target attributes
    X = dataset[:, 0:7]
    y = dataset[:, 8]

    '''
    要将原始的样本映射到维度更低的样本空间中
    PCA和LDA的映射目标不一样：PCA是为了让映射后的样本具有最大的发散性；
    而LDA是为了让映射后的样本有最好的分类性能。
    所以说PCA是一种无监督的降维方法，而LDA是一种有监督的降维方法。
    '''
    from sklearn.decomposition import PCA
    # 参数n_components为主成分数目
    print PCA(n_components=2).fit_transform(X)

    from sklearn.lda import LDA
    print LDA(n_components=2).fit_transform(X,y)

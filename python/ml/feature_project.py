# -*- coding:utf-8 -*-
from sklearn.datasets import load_iris

__author__ = 'kevin'

if __name__ == '__main__':
    # 导入IRIS数据集
    iris = load_iris()
    # 特征矩阵
    print iris.data[0]

    # 目标向量
    print iris.target[0]

    from numpy import vstack, array, nan
    from sklearn.preprocessing import Imputer

    # 缺失值计算，返回值为计算缺失值后的数据
    # 参数missing_value为缺失值的表示形式，默认为NaN
    # 参数strategy为缺失值填充方式，默认为mean（均值）
    print 'missing_value',Imputer().fit_transform(vstack((array([nan, nan, nan, nan]), iris.data)))[0]

    from sklearn.feature_selection import VarianceThreshold
    # 方差选择法，返回值为特征选择后的数据
    # 参数threshold为方差的阈值
    print 'feature_selection', VarianceThreshold(threshold=3).fit_transform(iris.data)[0]

    from sklearn.feature_selection import SelectKBest
    from scipy.stats import pearsonr

    # 选择K个最好的特征，返回选择特征后的数据
    # 第一个参数为计算评估特征是否好的函数，该函数输入特征矩阵和目标向量，
    # 输出二元组（评分，P值）的数组，数组第i项为第i个特征的评分和P值。
    # 在此定义为计算相关系数
    # 参数k为选择的特征个数
    #print 'SelectKBest',SelectKBest(lambda X, Y: array(map(lambda x:pearsonr(x, Y), X.T)).T, k=2).fit_transform(iris.data, iris.target)[0]


    from sklearn.decomposition import PCA

    # 主成分分析法，返回降维后的数据
    # 参数n_components为主成分数目
    print 'PCA', PCA(n_components=3).fit_transform(iris.data)[0]

    from sklearn.lda import LDA

    # 线性判别分析法，返回降维后的数据
    # 参数n_components为降维后的维数
    print 'LDA', LDA(n_components=2).fit_transform(iris.data, iris.target)[0]

    pass

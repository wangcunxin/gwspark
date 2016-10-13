# -*- coding:utf-8 -*-


__author__ = 'kevin'

if __name__ == '__main__':
    '''
    分析特征对分类的贡献度
    树算法(Tree algorithms)计算特征的信息量
    '''
    sep = ","

    try:
        path = "/home/kevin/temp/users.csv"
        fis = open(path, "r")

        try:
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

            # 3. 特征选择(Feature Selection)

            from sklearn import metrics
            from sklearn.ensemble import ExtraTreesClassifier

            model = ExtraTreesClassifier()
            model.fit(X, y)
            # display the relative importance of each attribute
            print(model.feature_importances_)

        except Exception, e:
            print(e)
    except Exception, e:
        print(e)
    finally:
        fis.close()

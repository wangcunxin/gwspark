# -*- coding:utf-8 -*-

import numpy as np

__author__ = 'kevin'

if __name__ == '__main__':
    '''
    分析特征对分类的贡献度
    树算法(Tree algorithms)计算特征的信息量
    '''
    sep = ","

    try:
        path = "/home/kevin/temp/users.csv"
        raw_data = open(path, "r")

        try:
            # 1. 加载数据(Data Loading)

            # load the CSV file as a numpy matrix
            dataset = np.loadtxt(raw_data, delimiter=",")
            # separate the data from the target attributes
            # 0,1056602,0,0,0,0,0,0,0,0,0,0,0,5,15
            X = dataset[:, 2:15]
            y = dataset[:, 0]

            # 3. 特征选择(Feature Selection)

            from sklearn import metrics
            from sklearn.ensemble import ExtraTreesClassifier

            model = ExtraTreesClassifier()
            model.fit(X, y)

            qualifiers = "label,userid," \
                         "buy_times,buy_quantity,amount,discount_amount,discount_times," \
                         "days,buy_cinemas,buy_cities,ip_cities,match_num," \
                         "refund_times,avg_time,avg_count"
            # display the relative importance of each attribute
            print(model.feature_importances_)

        except Exception, e:
            print(e)
    except Exception, e:
        print(e)
    finally:
        raw_data.close()

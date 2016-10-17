# -*- coding:utf-8 -*-
from sklearn.preprocessing import Imputer
import numpy as np

__author__ = 'kevin'

if __name__ == '__main__':
    '缺失值计算:missing value'

    imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
    X = np.array([[1, 2], [np.nan, 3], [7, 6]])
    Y = [[np.nan, 2], [6, np.nan], [7, 6]]
    print imp.fit(X)
    print imp.transform(Y)

    line = "1,?".replace('?', 'nan')
    print line
    Z = np.array(line.split(","), dtype=float)
    print Z
    print imp.transform(Z)

    pass

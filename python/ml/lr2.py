__author__ = 'kevin'
from sklearn import linear_model

if __name__ == '__main__':
    x = [[0, 0], [1, 1], [2, 2]]
    y = [0, 1, 2]
    clf = linear_model.LinearRegression()
    clf.fit(x,y)
    print clf.coef_
    print clf.intercept_

    print clf.predict([[3,3]])
    print clf.predict([[3,4]])
    print clf.predict([[3,5]])

    print clf.score([[1,1]],[1])
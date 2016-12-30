# -*- coding:utf-8 -*-
import time
import sys
import datetime
import pandas as pd

from sklearn import metrics
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression

__author__ = 'kevin'


def fit_model(df, out):
    # data = df.dropna(how='any').fillna(0)
    data = df.replace('inf',0).replace('-inf',0)
    file_model = '%s/model_lr.bin' % out
    print file_model
    # split data: train,test=7,3
    from sklearn import cross_validation as cv
    X_train, X_test, y_train, y_test = cv.train_test_split(data.iloc[:, 1:16],
                                                           data.iloc[:, 16],
                                                           test_size=0.3,
                                                           random_state=0)
    # modelX_train
    model = LogisticRegression(penalty='l1', max_iter=100, n_jobs=1, C=1.0)
    model.fit(X_train, y_train)

    print model
    print df.columns
    print 'intercept', model.intercept_
    print 'coef', model.coef_

    predicted = model.predict(X_test)
    expected = y_test

    print 'classification_report', metrics.classification_report(expected, predicted)
    print 'confusion_matrix', metrics.confusion_matrix(expected, predicted)
    fpr, tpr, thresholds = metrics.roc_curve(expected, predicted)
    print 'fpr, tpr, thresholds:', fpr, tpr, thresholds
    print 'auc:', metrics.auc(fpr, tpr)

    joblib.dump(model, file_model)


def main(argv):
    dat = argv[0]
    out = argv[1] + "/" + dat
    file_pd_woe = out + "/pd_woe.csv"

    df = pd.read_csv(file_pd_woe)
    del df['Unnamed: 0']
    print df.shape
    print 'completed to load pd file'

    fit_model(df, out)
    print 'completed'


if __name__ == '__main__':
    '''
    score card: lr coef and intercept
    '''
    begin = time.time()
    if len(sys.argv) != 3:
        print 'score_card_coef.py <ym> <out>'
        sys.exit(-1)
    print sys.argv
    try:
        main(sys.argv[1:])
    except Exception, e:
        print 'exception happened:', e
    end = time.time()
    now = datetime.datetime.now()
    dat = now.strftime("%Y-%m-%d %H:%M:%S")
    print dat, 'total cost', round((end - begin) / 60, 3), 'minutes'
    pass

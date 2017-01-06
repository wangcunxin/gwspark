# -*- coding:utf-8 -*-
import time
import sys
import datetime
import numpy as np
import pandas as pd

from sklearn import metrics
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression

__author__ = 'kevin'


def random_sample(original):
    # #0:#1=10:1
    df_score_1 = original[original['label'] == 1]
    num_1 = df_score_1.shape[0]
    num_0 = num_1 * 1

    df_score_0 = original[original['label'] == 0]
    indexs_0 = []
    for i in df_score_0.index:
        indexs_0.append(i)

    sampler_0 = np.random.permutation(indexs_0)
    sample_0 = original.take(sampler_0[0:num_0])

    shard = pd.concat([df_score_1, sample_0])
    return shard


def fit_model(df, out):
    # data = df.dropna(how='any').fillna(0)
    data = df.replace('inf', 0).replace('-inf', 0)
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
    print 'coef', ','.join(str(i) for i in model.coef_[0, :])

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
    print df.shape
    print 'completed to load pd file'

    df_sample = random_sample(df)
    print 'completed to sample'

    fit_model(df_sample, out)
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

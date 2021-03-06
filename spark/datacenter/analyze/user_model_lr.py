# -*- coding:utf-8 -*-
import datetime
import time
import sys
import math
import pandas as pd
import numpy as np

from sklearn import metrics
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression

from sklearn.preprocessing import Normalizer

from spark.datacenter.etl.hbase_client import HBaseClient
from spark.datacenter.etl.mongodb_client import MongodbClient
from userprofile.properties import Properties

__author__ = 'kevin'

sep = ','
sep2 = "_"
qualifiers = "userid,buy_times,buy_quantity,amount,discount_amount,discount_times," \
             "days,buy_cinemas,buy_cities,avg_time,avg_count,score".split(",")


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-float(x)))


def load_data(dat):
    # 1.hbase:load and filter
    hBaseClient = HBaseClient()
    table = "up_dat"

    cfs = ['DF']
    rs = hBaseClient.scanByPrefix(table, dat, cfs)

    lines = []
    for r in rs:
        rowkey = r.row.split('#')[1]
        arr = [rowkey]
        columns = r.columns
        for qualifier in qualifiers[1:11]:
            value = '0'
            val = columns.get('DF:%s' % qualifier)
            if val is not None:
                value = val.value
            arr.append(value)
        lines.append(arr)

    print 'load hbase:', len(lines)

    # 2. mongodb
    conf_file = "../../../userprofile/config-mongodb.properties"
    prop = Properties()
    conf = prop.getProperties(conf_file)
    host = conf.get("bigdata.host")
    port = int(conf.get("bigdata.port"))
    username = conf.get("bigdata.username")
    password = conf.get("bigdata.password")
    dbname = conf.get("bigdata.dbname")

    mongodbClient = MongodbClient(host, port, dbname, username, password)
    colName = "rc_user_rating"
    mongodbClient.setCollection(colName)
    import re
    regex = re.compile('^%s.*$' % dat)
    query = {'_id': {'$regex': regex}}
    rs = mongodbClient.findWithQuery(doc=query)
    fields = ['userid', 'score']
    scores = []
    for r in rs:
        ar = [r[fields[0]], r[fields[1]]]
        scores.append(ar)
    print 'load mongodb:', len(scores)

    df_up = pd.DataFrame(lines, columns=qualifiers[0:11])
    df_up_filter = df_up[(df_up['avg_count'] > 0) & (df_up['buy_quantity'] > 0)].dropna(how='any')
    # df_up.index = df_up['userid'].tolist()
    df_score = pd.DataFrame(scores, columns=fields)
    white_list = ['50000125', '50000949', '50000891', '55859667']
    df_score_filter = df_score[~df_score['userid'].isin(white_list)].dropna(how='any')

    df = pd.merge(df_up_filter, df_score_filter, on='userid', how='inner')
    return df


def preprocess_data(original):
    # #0:#1=10:1
    df_score_1 = original[original['score'] > 0]
    num_1 = df_score_1.shape[0]
    num_0 = num_1 * 1

    df_score_0 = original[original['score'] == 0]
    indexs_0 = []
    for i in df_score_0.index:
        indexs_0.append(i)

    sampler_0 = np.random.permutation(indexs_0)
    sample_0 = original.take(sampler_0[0:num_0])

    shard = pd.concat([df_score_1, sample_0])
    # userid = shard.iloc[:, 0]
    features = shard.iloc[:, 1:11]
    score = shard.iloc[:, 11]
    # 2.normalize fields features
    features_normalize = Normalizer().fit_transform(features)
    # 定量特征二值化
    from sklearn.preprocessing import Binarizer
    score_binary = Binarizer(threshold=0).fit_transform(score)

    df = pd.DataFrame(features_normalize, columns=qualifiers[1:11])
    # bug:insert nan
    # df.insert(0, qualifiers[0], userid)
    df['label'] = score_binary[0]

    row_size = df.shape[0]
    print 'row size:', row_size
    return df


def train_model(data, out, dat):
    file_model = '%s/model/lr_%s.bin' % (out, dat)
    file_plot = '%s/plot/lr_roc_%s.png' % (out, dat)
    # split data: train,test=7,3
    from sklearn import cross_validation as cv
    X_train, X_test, y_train, y_test = cv.train_test_split(data.iloc[:, 0:10],
                                                           data.iloc[:, 10],
                                                           test_size=0.3,
                                                           random_state=0)
    # modelX_train
    model = LogisticRegression(penalty='l1', max_iter=100, n_jobs=1, C=1.0)
    model.fit(X_train, y_train)
    print file_model, file_plot
    print model
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

    # import matplotlib.pyplot as plt
    # plt.plot(fpr, tpr, color='r')
    # plt.show()
    # plt.savefig(file_plot, format='png')


def main(argv):
    dat = argv[0]
    out = argv[1]
    # load data
    original = load_data(dat)
    print 'finish loading data'
    # preprocess
    data = preprocess_data(original)
    print 'finish preprocessing data'
    # model
    train_model(data, out, dat)
    print 'finish to dump model'
    pass


if __name__ == '__main__':
    '''
    computing procedures:
    1.hbase:up_dat,mongodb:rc_user_rating
    2.df:[userid,10 fields,label]
        #0:#1=10:1 or 1:1
    3.normalize:sigmoid
    4.lr:train,test
        train:test=7:3 or 6:4
    5.lr:evaluate,save:model,roc,auc
    '''
    begin = time.time()
    if len(sys.argv) != 3:
        print 'user_model_lr.py <ym> <out>'
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

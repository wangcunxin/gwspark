# -*- coding:utf-8 -*-
import datetime
import time
import sys
import math

import pandas as pd
from sklearn.externals import joblib

from sklearn.preprocessing import Normalizer

from spark.datacenter.etl.hbase_client import HBaseClient
from spark.datacenter.etl.mongodb_client import MongodbClient
from userprofile.properties import Properties

__author__ = 'kevin'

sep = ','
sep2 = "_"
qualifiers = "userid,buy_times,buy_quantity,amount,discount_amount,discount_times," \
             "days,buy_cinemas,buy_cities,avg_time,avg_count".split(",")


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

    df_up = pd.DataFrame(lines, columns=qualifiers[0:11])
    # special account list
    white_list = ['50000125', '50000949', '50000891', '55859667']
    df = df_up[~df_up['userid'].isin(white_list)]

    return df


def preprocess_data(shard):
    # preprocess
    userids = shard.iloc[:, 0]
    features = shard.iloc[:, 1:11]
    # 2.normalize fields features
    features_normalize = Normalizer().fit_transform(features)
    df = pd.DataFrame(features_normalize, columns=qualifiers[1:11])
    # shard.iloc[:, 0]的结果，创建df，不会改变index
    df_userids = pd.DataFrame(userids.tolist(), columns=[qualifiers[0]])
    # union all column:axis=1,row:axis=0
    df2 = pd.concat([df_userids, df], axis=1, join='inner', join_axes=[df_userids.index])

    print 'row size:', df2.shape[0]
    return df2


def max_row(row):
    """
    udf实现求一行2个字段的最大值
    df.apply(max_row,axis=1)
    """
    c1 = row[0]
    c2 = row[1]
    r = c2
    if c1 > c2:
        r = c1
    return r


def predict_user(data, input, dat):
    # /home/kevin/temp/model/lr_201602.bin
    file_model = input
    model = joblib.load(file_model)
    print model
    predicted = model.predict_proba(X=data.iloc[:, 1:11])

    uids = data.iloc[:, 0]
    probas = predicted[:, 1]
    proba_list = []

    for i in range(len(uids)):
        uid = uids[i]
        proba = round(probas[i], 4)
        key = "%s%s%s" % (dat, sep2, uid)
        ele = {'_id': key, 'userid': uid, 'proba': proba}
        proba_list.append(ele)
    # dump to mango
    print 'user predict proba:', len(proba_list)
    conf_file = "../../../userprofile/config-mongodb.properties"
    prop = Properties()
    conf = prop.getProperties(conf_file)
    host = conf.get("bigdata.host")
    port = int(conf.get("bigdata.port"))
    username = conf.get("bigdata.username")
    password = conf.get("bigdata.password")
    dbname = conf.get("bigdata.dbname")

    mongodbClient = MongodbClient(host, port, dbname, username, password)
    colName = "rc_user_proba"
    mongodbClient.setCollection(colName)
    mongodbClient.insertMany(proba_list)


def main(argv):
    dat = argv[0]
    input = argv[1]
    # load data
    original = load_data(dat)
    print 'finish loading data'
    # preprocess
    data = preprocess_data(original)
    print 'finish preprocessing data'
    # model
    predict_user(data, input, dat)
    print 'finish to predict'
    pass


if __name__ == '__main__':
    '''
    computing procedures:
    1.hbase:up_dat
    2.df:[userid,10 fields]
    3.normalize:sigmoid
    4.lr:load,predict
    5.mongodb:rc_user_prediction:{"_id":"ym_userid","userid":"","proba":0}
    '''
    begin = time.time()
    if len(sys.argv) != 3:
        print 'user_predict_lr.py <ym> <input>'
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

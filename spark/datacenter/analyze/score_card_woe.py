# -*- coding:utf-8 -*-
import datetime
import time
import sys
import pandas as pd
import numpy as np

from sklearn import metrics
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from spark.datacenter.analyze.pandas_utils import PandasUtils

from spark.datacenter.etl.hbase_client import HBaseClient
from spark.datacenter.etl.mongodb_client import MongodbClient
from userprofile.properties import Properties

__author__ = 'kevin'

sep = ','
sep2 = "_"
nul = 'NaN'
qualifiers = "userid," \
             "buy_times,buy_quantity,amount,discount_amount,discount_times," \
             "days,buy_cinemas,buy_cities,avg_time,avg_count," \
             "mobile,source,headpic,flowernum,replycount," \
             "score".split(",")


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
        for qualifier in qualifiers[1:16]:
            value = '0'
            val = columns.get('DF:%s' % qualifier)
            if val is not None:
                if qualifier in ('mobile', 'headpic'):
                    value = '1' if len(val.value) > 4 else '0'
                else:
                    value = val.value
            elif qualifier == 'source':
                value = 'other'
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

    df_up = pd.DataFrame(lines, columns=qualifiers[0:16])
    df_up_filter = df_up[(df_up['avg_count'] > 0) & (df_up['buy_quantity'] > 0)]

    df_score = pd.DataFrame(scores, columns=fields)
    white_list = ['50000125', '50000949', '50000891', '55859667']
    df_score_filter = df_score[~df_score['userid'].isin(white_list)]

    df = pd.merge(df_up_filter, df_score_filter, on='userid', how='inner')
    print df.shape
    return df


def preprocess_data(original):
    """
    数据处理原则
    1.加载时处理：连续型数据，非数字，要处理成分类变量，如：mobile，headpic
    2.设置默认值，过滤特殊账号，在加载时处理
    3.preprocess：
    连续型数字，二值化，Binarizer,如：flowernum, replycount, score;
    分类变量,多值化,function encoding(),如：source
    4.process: 分箱,function binning(),如：buy_times,buy_quantity,amount...
    5.
    """
    df_filter = original.dropna(how='any').fillna(0)
    columns = ['flowernum', 'replycount', 'score']
    X = df_filter.loc[:, columns]
    # 定量特征二值化
    from sklearn.preprocessing import Binarizer
    X_binary = Binarizer(threshold=0).fit_transform(X)
    df = df_filter.drop(columns, axis=1)
    # categorical
    df['flowernum'] = X_binary[:, 0].astype(np.int)
    df['replycount'] = X_binary[:, 1].astype(np.int)
    df['label'] = X_binary[:, 2].astype(np.int)

    # multi-values source
    sources_dict = {'email': '1', 'app': '2', 'code': '3', 'mobile': '4', 'unionPayLottery': '5', 'other': '0'}
    df['source'] = PandasUtils.encoding(df['source'], sources_dict)
    # continuous
    fields = qualifiers[1:11]
    for field in fields:
        df[field] = df[field].astype(np.float32)
    return df


def process_data(df, out):
    file_path = out + "/%s.csv"
    fields = qualifiers[1:11]
    bins_dict = {'buy_times': [2, 3, 4, 5],
                 'buy_quantity': [3, 4, 5, 7, 8, 9, 10],
                 'amount': [90, 112, 136, 175, 248],
                 'discount_amount': [29, 45, 106],
                 'discount_times': [1, 2, 3, 4],
                 'days': [2, 3],
                 'buy_cinemas': [2, 3],
                 'buy_cities': [2],
                 'avg_time': [12, 36, 72, 202, 1310],
                 'avg_count': [4, 36, 67]}
    bins_dict = {'buy_times': [1.1, 2.1],
                 'buy_quantity': [1.1, 2.1],
                 'amount': [20.1, 52.1],
                 'discount_amount': [29, 45, 106],
                 'discount_times': [1, 2, 3, 4],
                 'days': [1.2, 1.6],
                 'buy_cinemas': [2],
                 'buy_cities': [2],
                 'avg_time': [1.2, 1.6],
                 'avg_count': [1.2, 1.6]}
    for field in fields:
        bins = bins_dict.get(field)
        print field
        df[field] = PandasUtils.binning(df[field], bins).astype(np.object)
    print df.shape
    # 1.save
    df.to_csv(file_path % "pd_binning", index=None)
    return df


def get_woe(df, column):
    df2 = df.groupby(column, as_index=True)
    rows = df2['label'].count()
    bad = df2['label'].sum()
    good = rows - bad

    df3 = pd.DataFrame(bad, columns=['bad'])
    df3['bad'] = bad
    df3['good'] = good

    bad_ratio = bad / df3['bad'].sum()
    good_ratio = good / df3['good'].sum()
    woe = np.log(good_ratio / bad_ratio)
    iv = woe * (good_ratio - bad_ratio)
    df3['woe'] = woe
    df3['iv'] = iv

    return df3


def compute_woes(df, out):
    print df.head()
    file_path = out + "/woe_%s.csv"
    rets_dict = {}
    for column in qualifiers[1:16]:
        map = {}
        woe_iv = get_woe(df.loc[:, [column, 'label']], column)
        # 2.save
        woe_iv.to_csv(file_path % column)
        for index, row in woe_iv.iterrows():
            map[index] = row['woe']
        rets_dict[column] = map
    print rets_dict
    return rets_dict


def replace_features(df, dic, out):
    file_path = out + "/%s.csv"
    fields = qualifiers[1:16]
    for field in fields:
        df[field] = PandasUtils.encoding(df[field], dic.get(field))
    # 3.save
    df.to_csv(file_path % "pd_woe", index=None)


def main(argv):
    dat = argv[0]
    out = argv[1] + "/" + dat
    # load data
    original = load_data(dat)
    print 'finish loading data'
    # preprocess
    df_pre = preprocess_data(original)
    print 'finish preprocessing data'
    # process
    df_done = process_data(df_pre, out)
    print 'finish processing data and dumping'
    # compute woe iv
    column_woe_dict = compute_woes(df_done, out)
    print 'finish computing woe and dumping'
    # replace all the features
    replace_features(df_done, column_woe_dict, out)
    print 'finish replacing feature with woe and dumping'

    pass


if __name__ == '__main__':
    '''
    score card: woe and iv
    computing procedures:
    1.hbase:up_dat,mongodb:rc_user_rating
    2.filter special data
    3.calculate:bad,good,sum(bad),sum(good)
    4.dump:pd_binning,woe_field,pd_woe
    '''
    begin = time.time()
    if len(sys.argv) != 3:
        print 'score_card_woe.py <ym> <out>'
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

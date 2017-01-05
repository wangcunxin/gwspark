# -*- coding:utf-8 -*-
import json
import time
import sys
import datetime
import numpy as np
import pandas as pd
from pandas.core.common import flatten
from spark.datacenter.analyze.pandas_utils import PandasUtils

__author__ = 'kevin'

qualifiers = "userid," \
             "buy_times,buy_quantity,amount,discount_amount,discount_times," \
             "days,buy_cinemas,buy_cities,avg_time,avg_count," \
             "mobile,source,headpic,flowernum,replycount," \
             "score".split(",")


def load_data(file_score_dict):
    file_object = open(file_score_dict)
    score_dict = {}
    try:
        line = file_object.readline()
        score_dict = json.loads(line)
        print score_dict
    finally:
        file_object.close()
    return score_dict


def mark_score(score_dict, df, out):
    base_score = 508.76
    fields = qualifiers[1:16]
    for field in fields:
        df[field] = PandasUtils.encoding(df[field], score_dict.get(field))

    user_scores = {}
    for index, row in df.iterrows():
        userid = str(row['userid'].astype(np.int))
        scores = base_score
        for field in fields:
            scores += row[field]
        user_scores[userid] = scores
    print user_scores.__len__()
    return user_scores


def dump_data(user_scores_dict):
    userids = []
    scores = []
    for uid in user_scores_dict.keys():
        score = user_scores_dict[uid]
        userids.append(uid)
        scores.append(score)

    df = pd.DataFrame({"userid": pd.Series(np.array(userids)), "score": pd.Series(np.array(scores))})
    print df.head()
    print df.shape
    print df.describe()

    pass


def main(argv):
    dat = argv[0]
    out = argv[1] + "/" + dat
    file_score_dict = out + '/user_score_card.dict'
    file_pd_woe = out + "/pd_binning.csv"

    score_dict = load_data(file_score_dict)

    df = pd.read_csv(file_pd_woe)
    del df['Unnamed: 0']
    print df.shape
    print 'completed to load data'

    user_scores_dict = mark_score(score_dict, df, out)
    dump_data(user_scores_dict)
    print 'completed'


if __name__ == '__main__':
    '''
    user credit score
    '''
    begin = time.time()
    if len(sys.argv) != 3:
        print 'user_credit_score.py <ym> <out>'
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

# -*- coding:utf-8 -*-
import json
import time
import sys
import datetime
import numpy as np

import pandas as pd

from spark.datacenter.analyze.pandas_utils import PandasUtils

__author__ = 'kevin'

qualifiers = "userid," \
             "buy_times,buy_quantity,amount,discount_amount,discount_times," \
             "days,buy_cinemas,buy_cities,avg_time,avg_count," \
             "mobile,source,headpic,flowernum,replycount," \
             "label,score".split(",")


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


def mark_score(base_score, score_dict, df):
    fields = qualifiers[1:16]
    for field in fields:
        df[field] = PandasUtils.encoding(df[field], score_dict.get(field))
    # user_scores = {}
    scores = []
    for index, row in df.iterrows():
        # userid = str(row['userid'].astype(np.int))
        score = base_score
        for field in fields:
            score += row[field]
        #user_scores[userid] = score
        scores.append(score)
    df['score'] = scores

    return df


def dump_data(out, df_score):
    df = df_score.drop(qualifiers[1:16], axis=1)
    print df.head()
    print df.shape
    print df.describe(percentiles=np.array([0.01, 0.02, 0.03, 0.05, 0.1, 0.2, 0.25, 0.5, 0.75, 0.8, 0.9, 0.95]))
    df.to_csv(out + "/pd_user_credit_score.csv", index=None)
    pass


def main(argv):
    dat = argv[0]
    out = argv[1] + "/" + dat
    base_score = float(argv[2])
    file_score_dict = out + '/user_score_card.dict'
    file_pd_woe = out + "/pd_binning.csv"

    score_dict = load_data(file_score_dict)
    df = pd.read_csv(file_pd_woe)
    print df.shape
    print 'completed to load data'

    df_score = mark_score(base_score, score_dict, df)
    print 'completed to mark score'

    dump_data(out, df_score)
    print 'completed'


if __name__ == '__main__':
    '''
    user credit score
    '''
    begin = time.time()
    if len(sys.argv) != 4:
        print 'user_credit_score.py <ym> <out> <base_score>'
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

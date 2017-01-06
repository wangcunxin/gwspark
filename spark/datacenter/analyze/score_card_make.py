# -*- coding:utf-8 -*-
import json
import time
import sys
import datetime
import numpy as np
import pandas as pd

__author__ = 'kevin'

qualifiers = "userid," \
             "buy_times,buy_quantity,amount,discount_amount,discount_times," \
             "days,buy_cinemas,buy_cities,avg_time,avg_count," \
             "mobile,source,headpic,flowernum,replycount," \
             "score".split(",")


def calculate_score(out, coefs):
    # formula:score=-B*coef*woe
    _b = 20 / np.log(2)
    print coefs
    woe_field = out + "/woe_%s.csv"
    json_dict = {}
    i = 0
    for field in qualifiers[1:16]:
        _coef = float(coefs[i])
        i += 1
        df = pd.read_csv(woe_field % field)
        bin_score = {}
        for index, row in df.iterrows():
            bin = int(row[field])
            woe = row['woe']
            score = -_b * _coef * woe
            bin_score[bin] = score

        json_dict[field] = bin_score
    print json_dict
    return json_dict


def save_score_card(binning_score, intercept, out):
    a = 600 + (20.0 / np.log(2.0)) * np.log(1.0 / 50.0)
    b = 20 / np.log(2)
    # 基础分数=A-B*β0
    base_score = a - b * intercept
    print 'a,b,base_score:', a, b, base_score
    # dump
    encode_json = json.dumps(binning_score)
    file_object = open(out + '/user_score_card.dict', 'w')
    try:
        file_object.write(encode_json)
    finally:
        file_object.close()


def main(argv):
    dat = argv[0]
    out = argv[1] + "/" + dat
    coefs = argv[2].split(",")
    intercept = float(argv[3])

    binning_score = calculate_score(out, coefs)
    print 'completed to calculate score'

    save_score_card(binning_score, intercept, out)
    print 'completed to save score card'


if __name__ == '__main__':
    '''
    一、评分卡刻度及基础分
    1、评分卡客户两个假设：
    1）值某个指定的比率设定特定的预期分值，令{1:50}时的分值为600分
    2）制定比率翻番的分数（PDO）,令PDO=20
    首先设定比率为θ的特定点的分值为P，即：P=A-B*log(θ)
    B=PDO/ln(2)=20/ln(2)=28.8539
    A=P+B*ln(θ)=600+20/ln(2)*ln(1/50)=487.1229
    2、评分卡基础分数：
    基础分数=A-B*β0，β0为逻辑回归截距。

    二、特征分数
    formula:score=-B*coef*woe
    '''
    begin = time.time()
    if len(sys.argv) != 5:
        print 'score_card_make.py <ym> <out>'
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

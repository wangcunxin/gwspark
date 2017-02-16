# -*- coding:utf-8 -*-
import sys
import pandas as pd
from spark.datacenter.sparklogger import *

__author__ = 'kevin'


def main(argv):
    dat = argv[0]
    out = argv[1] + "/" + dat
    file_path = out + '/pd_user_credit_score.csv'
    df = pd.read_csv(file_path)
    log = logging.getLogger('gwspark.ucs_optimize')
    log.info(df.shape)
    log.info('completed to load data')

    df_gb = df.groupby(by=['label'])
    print df_gb['score'].describe()
    print df_gb['score'].mean()
    print df_gb['userid'].count()
    print 'completed'

    pass


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'ucs_optimize.py <ym> <out>'
        sys.exit(-1)
    print sys.argv
    try:
        main(sys.argv[1:])
    except Exception, e:
        print 'exception happened:', e

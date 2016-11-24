# -*- coding:utf-8 -*-
import numpy as np
import pandas as pd
import pymysql

__author__ = 'kevin'


def test1():
    conn_mysql= pymysql.connect(host='192.168.8.108', port=3306, user='logcenter', passwd='logcenter123', db='logcenter')
    df = pd.read_sql('select * from agg_day_access limit 10;', con=conn_mysql)
    print df
    conn_mysql.close()
    pass


def test2():
    df = pd.DataFrame(np.random.randn(4, 4), index=np.arange(4), columns=list('ABCD'))
    print df.sort_values(by=['A','B'], ascending=[1,0])
    df['E']=[1,2,3,4]
    df2 = df[~df['E'].isin([2,3])]
    print df2


def test3():
    lines = []
    template = "%s,a,b"
    for i in range(0,10,1):
        lines.append([i,'a','b'])
    df = pd.DataFrame(lines,columns=['id','A','B'])
    print df
    pass


if __name__ == '__main__':

    test2()

    pass
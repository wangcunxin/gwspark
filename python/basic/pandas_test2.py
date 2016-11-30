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
    df3 = df[(df['A']>-0.5) & (df['B']>0.5)]
    print df3


def test3():
    lines = []
    template = "%s,a,b"
    for i in range(0,10,1):
        lines.append([i,'a','b'])
    df = pd.DataFrame(lines,columns=['id','A','B'])
    print df
    pass


def test4():
    df = pd.DataFrame(np.random.randn(4, 2), index=np.arange(4), columns=list('AB'))
    print df
    def max_row(a):
        b=a[0]
        c=a[1]
        d=a[1]
        if b>c:
            d=b
        else:
            d=c
        return d
    print df.apply(max_row,axis=1)
    pass


def test5():
    df = pd.DataFrame(np.random.randn(4, 2), index=np.arange(4), columns=list('AB'))
    print df
    for index, row in df.iterrows():
        print index, row
        for col_name in df.columns:
            print row[col_name]

if __name__ == '__main__':

    test5()

    pass
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
    for i in range(0,5,1):
        lines.append([i,'a','b'])
    df = pd.DataFrame(lines,columns=['id','A','B'])
    print df
    print df.shape
    print df['id'].tolist()
    indexs = ','.join(str(i) for i in df.index)
    print indexs
    for i in df.index:
        print i
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


def test6():
    # random sample
    df = pd.DataFrame(np.random.randn(10, 2), index=np.arange(10), columns=list('AB'))
    # print df
    sampler1 = np.random.randint(0, df.shape[0], size=5)
    sample1 = df.take(sampler1)
    print sample1

    sampler2 = np.random.permutation(5)
    sample2 = df.take(sampler2)
    print sample2

    ar = np.random.randn(10, 2)
    np.random.shuffle(ar)
    print ar


def test7():
    # random sample
    size = 10
    df = pd.DataFrame(np.random.randn(size, 2), index=np.arange(size), columns=list('AB'))
    df2 = pd.DataFrame(np.random.randn(size, 1), index=np.arange(size), columns=list('C'))
    df3 = pd.concat([df,df2], axis=1, join='inner')
    print df3.iloc[:,0].tolist()

if __name__ == '__main__':
    test7()
    pass

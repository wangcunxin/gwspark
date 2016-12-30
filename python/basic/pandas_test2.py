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


def test8():
    df = pd.DataFrame({"id":[1,2,3,4,5,6], "raw_grade":['a', 'd', 'b', 'c', 'a', 'e']})
    print df
    df["grade1"] = df["raw_grade"].astype("category")
    print df
    df["grade2"] = df["grade1"].cat.set_categories([1,2,3,4,5])
    print df


def coding(col, codeDict):
    colCoded = pd.Series(col, copy=True)
    for key, value in codeDict.items():
        colCoded.replace(key, value, inplace=True)
    return colCoded


def get_monotonic_list(min, arr, max):
    return [min] + arr + [max]


def binning(col, cut_points, labels=None):
    minval = col.min()
    maxval = col.max()
    break_points = get_monotonic_list(minval, cut_points, maxval)
    # 如果没有标签，则使用默认标签0 ... (n-1)
    if not labels:
        labels = range(len(cut_points) + 1)
    colBin = pd.cut(col, bins=break_points, labels=labels, include_lowest=True)
    return colBin


def test9():
    df = pd.DataFrame({"id":[1,2,3,4,5,6], "raw_grade":['a', 'b', 'b', 'c', 'a', 'c']})
    df["raw_grade2"] = coding(df["raw_grade"], {'a':0,'b':1,'c':2})
    df["id"] = df["id"].astype(np.object)
    print df
    cut_points = [2,5]
    labels = ['a1','a2','a3']
    df["id2"] = binning(df["id"], cut_points, labels)
    print df
    print df.dtypes
    print df.loc[:,["id"]]
    print df['id'].max
    print range(10)
    pass


if __name__ == '__main__':
    test9()
    pass

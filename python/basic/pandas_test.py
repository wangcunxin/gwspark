# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

__author__ = 'wangcx'


def test1():
    # create obj
    a1 = pd.Series([1, 3, 5, np.nan, 6, 8])
    print a1
    dates = pd.date_range('20130101', periods=6)
    print dates
    df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
    print df.head(), df.tail(3)
    print "-------------------"
    print df.index
    print df.columns
    print df.values
    print df
    print "-------------------"
    df2 = pd.DataFrame({'A': 1.,
                        'B': pd.Timestamp('20130102'),
                        'C': pd.Series(1, index=list(range(4)), dtype='float32'),
                        'D': np.array([3] * 4, dtype='int32'),
                        'E': pd.Categorical(["test", "train", "test", "train"]),
                        'F': 'foo'})
    print df2
    print df2.dtypes


def test2():
    dates = pd.date_range('20130101', periods=6)
    df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
    print df
    print df.describe()
    print df.T
    print df.sort_index(axis=1, ascending=False)
    print df.sort(columns='B')


def test3():
    dates = pd.date_range('20130101', periods=6)
    df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
    print df['A']
    print df[0:3]
    print df['20130102':'20130104']
    print df.loc[dates[0]]
    print df.loc['20130102':'20130104', ['A', 'B']]
    print dates[0], df.loc[dates[0], 'A']
    print df.iloc[0]
    print df.iloc[3:5, 0:2]
    print df.iloc[[1, 2, 4], [0, 2, 3]]
    print df.iloc[1:3, :]
    print df.iloc[:, 1:3]


def test4():
    dates = pd.date_range('20130101', periods=6)
    df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
    print df
    print df[df.A > 0]
    print df[df > 0]
    df2 = df.copy()
    df2['E'] = ['one', 'one', 'two', 'three', 'four', 'three']
    print df2
    print df2[df2['E'].isin(['two', 'four'])]


def test5():
    s1 = pd.Series([1, 2, 3, 4, 5, 6], index=pd.date_range('20130102', periods=6))
    print s1
    dates = pd.date_range('20130101', periods=6)
    df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
    print df, len(df)
    df['F'] = s1
    df.at[dates[0], 'A'] = 0
    df.iat[0, 1] = 1
    df.loc[:, 'D'] = np.array([5] * len(df))
    print np.array([5] * 3)
    print df
    df1 = df.reindex(index=dates[0:4], columns=list(df.columns) + ['E'])
    df1.loc[dates[0]:dates[1], 'E'] = 1
    print df1
    print df1.dropna(how='any')
    print df1.fillna(value=0.001)
    print pd.isnull(df1)


def test6():
    dates = pd.date_range('20130101', periods=6)
    df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
    print df
    print df.mean()
    print df.mean(1)
    df1 = pd.Series([1, 3, 5, np.nan, 6, 8], index=dates)
    print df1
    print df1.shift(2)
    print df
    print df.apply(np.cumsum)
    print df.apply(lambda x: x.max() - x.min())


def test7():
    s = pd.Series(np.random.randint(0, 7, size=10))
    print s
    # 元素的计数
    print s.value_counts()
    s1 = pd.Series(['A', 'B', 'C', 'Aaba', 'Baca', np.nan, 'CABA', 'dog', 'cat'])
    print s1.str.lower()

    df = pd.DataFrame(np.random.randn(10, 4))
    print df
    pieces = [df[:3], df[3:7], df[7:]]
    print pieces
    print pd.concat(pieces)


def test8():
    left = pd.DataFrame({'key': ['pee', 'poo'], 'lval': [1, 2]})
    right = pd.DataFrame({'key': ['pee', 'poo'], 'rval': [4, 5]})
    print left, right
    print pd.merge(left, right, on='key')
    df = pd.DataFrame(np.random.randn(8, 4), columns=['A', 'B', 'C', 'D'])
    print df
    s = df.iloc[3]
    print 'iloc[3]', s
    print df.append(s, ignore_index=True)


def test9():
    df = pd.DataFrame({'A': ['foo', 'bar', 'foo', 'bar', 'foo', 'bar', 'foo', 'foo'],
                       'B': ['one', 'one', 'two', 'three', 'two', 'two', 'one', 'three'],
                       'C': np.random.randn(8),
                       'D': np.random.randn(8)})
    print df
    print df.groupby('A').sum()
    print df.groupby(['A', 'B']).sum()

    print '---------------'
    tuples = list(zip(*[['bar', 'bar', 'baz', 'baz', 'foo', 'foo', 'qux', 'qux'],
                        ['one', 'two', 'one', 'two', 'one', 'two', 'one', 'two']]))
    print tuples
    # 分层索引
    index = pd.MultiIndex.from_tuples(tuples, names=['first', 'second'])
    print index
    df = pd.DataFrame(np.random.randn(8, 2), index=index, columns=['A', 'B'])
    print df
    df2 = df[:4]
    print df2
    stacked = df2.stack()
    print stacked
    print stacked.unstack()
    print '---------------'
    print stacked.unstack(1)
    print stacked.unstack(0)


def test10():
    x = [1, 2, 3]
    y = [4, 5, 6]
    z = [7, 8, 9]
    xyz = zip(x, y, z)
    print xyz

    x = [1, 2, 3]
    y = [4, 5, 6, 7]
    xy = zip(x, y)
    print xy

    u = zip(*xyz)
    print u

    x = [1, 2, 3]
    r = zip(* [x] * 3)
    print r
    '''
    [x]生成一个列表的列表，它只有一个元素x
    [x] * 3生成一个列表的列表，它有3个元素，[x, x, x]
    zip(* [x] * 3)的意思就明确了，zip(x, x, x)
    '''


def test11():
    # 数据透视表
    df = pd.DataFrame({'A' : ['one', 'one', 'two', 'three'] * 3,
                       'B' : ['a', 'b', 'c'] * 4,
                       'C' : ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'] * 2,
                       'D' : np.random.randn(12),
                       'E' : np.random.randn(12)})
    print df

    print pd.pivot_table(df, values='D', index=['A', 'B'], columns=['C'])
    tuples = list(zip(*[['bar', 'bar', 'baz', 'baz', 'foo', 'foo', 'qux', 'qux'],
                        ['one', 'two', 'one', 'two', 'one', 'two', 'one', 'two']]))
    index = pd.MultiIndex.from_tuples(tuples, names=['first', 'second'])
    print pd.DataFrame(np.random.randn(6, 6), index=index[:6], columns=index[:6])


def test12():
    rng = pd.date_range('1/1/2012', periods=10, freq='H')
    print rng
    ts = pd.Series(np.random.randint(0, 50, len(rng)), index=rng)
    print ts.head()
    print ts.resample('2H').sum()
    print '---------'
    converted = ts.asfreq('45Min', method='pad')
    print converted

    rng = pd.date_range('3/6/2012 00:00', periods=5, freq='D')
    ts2 = pd.Series(np.random.randn(len(rng)), rng)
    print ts2.head()
    print ts.head(5).resample('H').mean()


def test13():
    df = pd.DataFrame({"id":[1,2,3,4,5,6], "raw_grade":['a', 'b', 'b', 'a', 'a', 'e']})
    print df
    df["grade"] = df["raw_grade"].astype("category")
    print df["grade"]
    df["grade"].cat.categories = ["very good", "good", "very bad"]
    print df["grade"]
    df["grade"] = df["grade"].cat.set_categories(["very bad", "bad", "medium", "good", "very good"])
    print df["grade"]
    print df.sort_values(by="grade")
    print df.groupby("grade").size()


def test14():
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.style.use('ggplot')
    ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
    ts = ts.cumsum()
    print ts.plot(), ts

    df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list('ABCD'))
    df = df.cumsum()
    plt.figure()
    df.plot()


def test15():
    df = pd.DataFrame(np.random.randn(10, 4), index=np.arange(10), columns=list('ABCD'))
    print df
    df.to_csv('foo.csv')
    df2 = pd.read_csv('foo.csv',dtype=float)
    print df2
    print df2.loc[:,['A','B']]
    # df.to_hdf('foo.h5','df')
    print df2.loc[2:5]
    print df2[df2>0]


def test16():
    print pd.qcut(range(10), 3)
    print pd.qcut(range(6), 3, labels=["good","medium","bad"])
    print pd.qcut(range(5), 3, labels=False)


def test17():
    df = pd.DataFrame(np.random.randn(10, 4), index=np.arange(10), columns=list('ABCD'))
    print df.head(4)
    df["E"] = ["bad", "medium", "good", "very good","bad", "medium", "good", "very good","great","pretty"]
    df["F"] = ["bad1", "medium1", "good1", "very good1","bad1", "medium1", "good1", "very good1","great1","pretty1"]
    print df.head(4)

    # print 'sum',rs.sum()
    # print 'size',rs.size()
    # print 'count',rs.count()
    # print 'min',rs.min().A
    # print 'max',rs.max()
    # print 'mean',rs.mean()
    # print df.groupby(level=['E',"B"]).aggregate(np.sum)
    print '-'*80

    grouped = df.groupby(['E','F'])
    # mean = grouped.mean().B
    # print mean
    # print '-'*80
    # print 'size', grouped.size()
    # print '-'*80
    # mean_unstack = mean.unstack()
    # print mean_unstack
    # print '-'*80
    # print mean_unstack.loc[:,'A']
    # print '-'*80

    # for (k1,k2),group in grouped:
    #     print k1,k2
    #     print group
    # print '-'*80
    # pieces = dict(list(grouped))
    # print pieces['bad','bad1']
    mean = grouped['A'].mean()
    print mean
    print mean['bad','bad1']
    print mean['good','good1']

def test18():
    d = {'one' : pd.Series([1., 2., 3.], index=['a', 'b', 'c']),'two' : pd.Series([1., 2., 3., 4.], index=['a', 'b', 'c', 'd'])}
    df = pd.DataFrame(d)

    ds = [{'one' : 4,'two':2},{'one' : 5,'two' : 3},{'one' : 6,'two' : 4},{'two' : 7,'three':10}]
    #构建一个新的DataFrame，dfs
    dfs = pd.DataFrame(ds,index=['e','f','g','h'])
    df_t=pd.concat([df,dfs])#合并两个DataFrame
    print df_t

    left = pd.DataFrame({'key': ['foo1', 'foo2'], 'lval': [1, 2]})
    right = pd.DataFrame({'key': ['foo1', 'foo2'], 'rval': [4, 5]})
    #构建了两个DataFrame
    print pd.merge(left, right, on='key')#按照key列将两个DataFrame join在一起


def test19():
    df = pd.DataFrame(np.random.randn(10, 4), index=np.arange(10), columns=list('ABCD'))
    print df
    k = 3
    df1 = pd.cut(df['A'],k)
    print df1
    df2 = pd.qcut(df['A'],k)
    print df2


if __name__ == '__main__':
    # .at, .iat, .loc, .iloc 和 .ix.
    test1()

    pass

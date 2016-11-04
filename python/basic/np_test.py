# -*- coding:utf-8 -*-
from numpy.ma import hsplit

__author__ = 'kevin'

import numpy as np


def mean():
    f = "/home/kevin/temp/numpy/t1.txt"
    dnarr = np.arange(20).reshape(4, 5)
    print dnarr
    avg_column = np.mean(dnarr, axis=0)
    print "column", avg_column
    avg_row = np.mean(dnarr, axis=1)
    print "row", avg_row
    np.savetxt(f, avg_row, delimiter=',')
    print "reload", np.loadtxt(f)


def test1():
    dnarr = np.array([1, 2, 3])
    dnarr = np.array([(1, 2, 3), (1, 11, 7), (1, 2, 9)])
    print dnarr
    print 'ndim', dnarr.ndim
    print 'shape', dnarr.shape
    print 'size', dnarr.size
    print 'dtype', dnarr.dtype
    print 'itemsize', dnarr.itemsize
    print 'type', type(dnarr)
    print 'zhi', np.linalg.matrix_rank(dnarr)


def test2():
    print np.arange(3)
    print np.arange(6).reshape(2, 3)
    ndarr = np.arange(24).reshape(2, 3, 4)
    print ndarr.ndim
    print ndarr


def test3():
    # arithmetic
    dnarr1 = np.arange(4)
    dnarr2 = np.array([(10, 20, 30, 40), (10, 20, 30, 40)])
    dnarr3 = np.arange(6).reshape(2, 3)
    dnarr4 = np.arange(12).reshape(3, 4)
    print dnarr1
    print type(dnarr2), dnarr2
    print '*2', dnarr1 * 2
    print '**2', dnarr1 ** 2
    print 'a-b', dnarr1 - dnarr2
    print 'a*b', dnarr1 * dnarr2
    # m:column=n:row
    print 'dot(a,b)', np.dot(dnarr3, dnarr4)

    matrix = np.matrix(dnarr2)
    print type(matrix), matrix


def test4():
    print np.random.normal(size=(4, 4))

    nsteps = 100
    draws = np.random.randint(0, 2, size=nsteps)
    steps = np.where(draws > 0, 1, -1)
    walk = steps.cumsum()
    print walk.min(), walk.max()


def test5():
    x = np.arange(5, 11, 1).reshape(2, 3)
    print x
    x1 = np.log([1, np.e, np.e ** 2, 10])
    x3 = np.log(x)
    print 'e', x1, x3
    x2 = np.log10(x)
    print '10', x2
    print hsplit(x, 1)[0], x[:, 0]
    pass


def test6():
    b = np.arange(6).reshape(2, 3)
    print b
    print b.sum(axis=0)  # 计算每一列的和
    print b.min(axis=0)
    print b.min(axis=1)  # 获取每一行的最小值
    print b.cumsum(axis=1)  # 计算每一列的累积和
    print b.cumsum(axis=0)  # 计算每一行的累积和
    print b.cumsum()  # 计算全部行的累积和


if __name__ == '__main__':
    test6()

    pass

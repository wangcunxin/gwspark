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
    dnarr = np.array([(1, 2, 3), (1, 2, 3)])
    print dnarr
    print 'ndim', dnarr.ndim
    print 'shape', dnarr.shape
    print 'size', dnarr.size
    print 'dtype', dnarr.dtype
    print 'itemsize', dnarr.itemsize
    print 'type', type(dnarr)


def test2():
    print np.arange(3)
    print np.arange(6).reshape(2, 3)
    print np.arange(24).reshape(2, 3, 4)


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
    print walk.min(),walk.max()


if __name__ == '__main__':
    # mean()
    # test1()
    # test2()
    test3()
    #test4()

    pass

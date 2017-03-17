# -*- coding:utf8 -*-

import numpy as np
from python.ml.tensorflow.mnist_div import NeuralNetworks

__author__ = 'kevin'


def test1():
    a = [1, 2, 3]
    print a[:-2]
    print a[1:]
    # row,col
    print np.random.randn(2, 1)
    print zip(a[:-1], a[1:])
    # [(1,2),(2,3)]->[(2,1),(3,2)]
    print [np.random.randn(y, x) for x, y in zip(a[:-1], a[1:])]
    print [np.random.randn(y, 1) for y in a[1:]]


def test2():
    a = [1, 2, 3]
    # sizes = [28 * 28, 40, 10]
    # [(784, 40), (40, 10)]->[(40,748),(10,40)]
    net = NeuralNetworks(a)
    print('weights: ', net.w_)
    print('biases: ', net.b_)


def test3():
    s = "小格"
    s2 = u"矩阵"
    print s, s2
    pass


if __name__ == '__main__':
    test2()

    pass

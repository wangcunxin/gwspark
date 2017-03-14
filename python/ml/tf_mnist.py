# -*- coding:utf8 -*-
import tensorflow as tf

__author__ = 'kevin'


def load_data():
    import tensorflow.examples.tutorials.mnist.input_data as input_data
    mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
    print mnist[0:10]

if __name__ == '__main__':
    load_data()

    pass

# -*- coding:utf8 -*-

__author__ = 'kevin'

import unittest


# test class
class myclass():
    def __init__(self):
        pass

    def sum(self, x, y):
        print x + y
        return x + y

    def sub(self, x, y):
        print x - y
        return x - y


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tclass = myclass()
        print 'set up class'
        pass

    @classmethod
    def tearDownClass(cls):
        print 'tear down class'
        pass

    # 初始化 before function
    def setUp(self):
        print "set up"

    # 退出清理工作
    def tearDown(self):
        print "tear down"

    # function以test开头
    def test_sum(self):
        self.assertEqual(self.tclass.sum(1, 2), 3)

    def test_something(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()

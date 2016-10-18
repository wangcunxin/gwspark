# -*- coding:utf-8 -*-

__author__ = 'kevin'


def test1():
    import urllib2
    response = urllib2.urlopen('http://python.org/')
    html = response.read()
    print html


def test2():
    import urllib2
    req = urllib2.Request('http://www.pythontab.com')
    response = urllib2.urlopen(req)
    html = response.read()
    print html


if __name__ == '__main__':
    # test1()
    test2()

    pass
